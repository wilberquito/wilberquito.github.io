---
title: Why is initialization essential to deep networks?
author: wilberquito
date: 2024-08-07 15:33:00 +0800
categories: [Machine Learning, Bases]
tags: [xavier initialization, activation functions, vanishing gradient problem]
pin: true
math: true
mermaid: true
---

> Check out the original notebook [here](https://github.com/wilberquito/Hands-On-ML/blob/main/uvadlc_notebooks/initialization-of-nn.ipynb){:target="_blank"}.
{: .prompt-info }

*Why is initialization essential to deep networks?* It turns out that if you do it wrong, **it can lead to exploding or vanishing weights and gradients**. That means that either the weights of the model explode to infinity, or they vanish to 0. And the deeper the network, the harder it becomes to keep the weights at reasonable values. We’ll see why that’s the case in the following sections. And the deeper the network, the harder it becomes to keep the weights at reasonable values.

When initializing a neural network, there are a few properties we would like to have.

1) The variance of the input should be propagated through the model to the last layer.
It means, the *std* for the output neurons should be similar to the
rest of the layers of the neural network.

2) The variance of the gradient distribution should be equal across layers. Hence, all weight on all layer would be capable of being updated.


```python
import os
import json
import math
import numpy as np
import copy

import matplotlib.pyplot as plt
from matplotlib import cm
%matplotlib inline
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg', 'pdf') # For export
import seaborn as sns
sns.set()

from tqdm.notebook import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
import torch.optim as optim
```


```python
# Path to the folder where the datasets are/should be downloaded (e.g. MNIST)
DATASET_PATH = "../data"
# Path to the folder where the pretrained models are saved
CHECKPOINT_PATH = "../saved_models/tutorial4"


# Function for setting the seed
def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


set_seed(42)

# Ensure that all operations are deterministic on GPU (if used) for reproducibility
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Fetching the device that will be used throughout this notebook
device = (
    torch.device("cpu") if not torch.cuda.is_available() else torch.device("cuda:0")
)
print("Using device", device)
```

    Using device cuda:0



```python
from torchvision.datasets import FashionMNIST
from torchvision import transforms

# Transformations applied on each image => first make them a tensor, then normalize them with mean 0 and std 1
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.2861,), (0.3530,))]
)

# Loading the training dataset. We need to split it into a training and validation part
train_dataset = FashionMNIST(
    root=DATASET_PATH, train=True, transform=transform, download=True
)
train_set, val_set = torch.utils.data.random_split(train_dataset, [50000, 10000])

# Loading the test set
test_set = FashionMNIST(
    root=DATASET_PATH, train=False, transform=transform, download=True
)

# We define a set of data loaders that we can use for various purposes later.
# Note that for actually training a model, we will use different data loaders
# with a lower batch size.
train_loader = data.DataLoader(
    train_set, batch_size=1024, shuffle=True, drop_last=False
)
val_loader = data.DataLoader(val_set, batch_size=1024, shuffle=False, drop_last=False)
test_loader = data.DataLoader(test_set, batch_size=1024, shuffle=False, drop_last=False)
```


```python
print("Mean", (train_dataset.data.float() / 255).mean().item())
print("Std", (train_dataset.data.float() / 255).std().item())
```

    Mean 0.28604060411453247
    Std 0.3530242443084717



```python
imgs, _ = next(iter(train_loader))
print(f"Mean: {imgs.mean().item():5.3f}")
print(f"Std: {imgs.std().item():5.3f}")
```

    Mean: 0.020
    Std: 1.011



```python
class BaseNetwork(nn.Module):

    def __init__(
        self, act_fn, input_size=784, num_classes=10, hidden_sizes=[512, 256, 256, 128]
    ):
        super().__init__()

        layers = []
        layer_sizes = [input_size] + hidden_sizes
        for layer_idx in range(1, len(layer_sizes)):
            layers += [
                nn.Linear(
                    in_features=layer_sizes[layer_idx - 1],
                    out_features=layer_sizes[layer_idx],
                ),
                act_fn,
            ]
        layers += [nn.Linear(in_features=layer_sizes[-1], out_features=num_classes)]
        self.layers = nn.ModuleList(layers)

        self.config = {
            "act_fn": act_fn.__class__.__name__,
            "input_size": input_size,
            "num_classes": num_classes,
            "hidden_sizes": hidden_sizes,
        }

    def forward(self, x):
        x = x.view(x.size(0), -1)
        for l in self.layers:
            x = l(x)
        return x
```


```python
class Identity(nn.Module):
    def forward(self, x):
        return x


act_fn_by_name = {"tanh": nn.Tanh, "relu": nn.ReLU, "identity": Identity}
```


```python
model = BaseNetwork(act_fn=Identity()).to(device)
model
```




    BaseNetwork(
      (layers): ModuleList(
        (0): Linear(in_features=784, out_features=512, bias=True)
        (1): Identity()
        (2): Linear(in_features=512, out_features=256, bias=True)
        (3): Identity()
        (4): Linear(in_features=256, out_features=256, bias=True)
        (5): Identity()
        (6): Linear(in_features=256, out_features=128, bias=True)
        (7): Identity()
        (8): Linear(in_features=128, out_features=10, bias=True)
      )
    )




```python
##############################################################

def plot_dists(val_dict, color="C0", xlabel=None, stat="count", use_kde=True):
    columns = len(val_dict)
    fig, ax = plt.subplots(1, columns, figsize=(columns * 3, 2.5))
    fig_index = 0
    for key in sorted(val_dict.keys()):
        key_ax = ax[fig_index % columns]
        sns.histplot(
            val_dict[key],
            ax=key_ax,
            color=color,
            bins=50,
            stat=stat,
            kde=use_kde and ((val_dict[key].max() - val_dict[key].min()) > 1e-8),
        )  # Only plot kde if there is variance
        key_ax.set_title(
            f"{key} "
            + (
                r"(%i $\to$ %i)" % (val_dict[key].shape[1], val_dict[key].shape[0])
                if len(val_dict[key].shape) > 1
                else ""
            )
        )
        if xlabel is not None:
            key_ax.set_xlabel(xlabel)
        fig_index += 1
    fig.subplots_adjust(wspace=0.4)
    return fig

##############################################################

def visualize_weight_distribution(model, color="C0"):
    weights = {}
    for name, param in model.named_parameters():
        if name.endswith(".bias"):
            continue
        key_name = f"Layer {name.split('.')[1]}"
        weights[key_name] = param.detach().view(-1).cpu().numpy()

    ## Plotting
    fig = plot_dists(weights, color=color, xlabel="Weight vals")
    fig.suptitle("Weight distribution", fontsize=14, y=1.05)
    plt.show()
    plt.close()

##############################################################

def visualize_gradients(model, color="C0", print_variance=False):
    """
    Inputs:
        net - Object of class BaseNetwork
        color - Color in which we want to visualize the histogram (for easier separation of activation functions)
    """
    model.eval()
    small_loader = data.DataLoader(train_set, batch_size=1024, shuffle=False)
    imgs, labels = next(iter(small_loader))
    imgs, labels = imgs.to(device), labels.to(device)

    # Pass one batch through the network, and calculate the gradients for the weights
    model.zero_grad()
    preds = model(imgs)
    loss = F.cross_entropy(
        preds, labels
    )  # Same as nn.CrossEntropyLoss, but as a function instead of module
    loss.backward()
    # We limit our visualization to the weight parameters and exclude the bias to reduce the number of plots
    grads = {
        name: params.grad.view(-1).cpu().clone().numpy()
        for name, params in model.named_parameters()
        if "weight" in name
    }
    model.zero_grad()

    ## Plotting
    fig = plot_dists(grads, color=color, xlabel="Grad magnitude")
    fig.suptitle("Gradient distribution", fontsize=14, y=1.05)
    plt.show()
    plt.close()

    if print_variance:
        for key in sorted(grads.keys()):
            print(f"{key} - Variance: {np.var(grads[key])}")

##############################################################

def visualize_activations(model, color="C0", print_variance=False):
    model.eval()
    small_loader = data.DataLoader(train_set, batch_size=1024, shuffle=False)
    imgs, labels = next(iter(small_loader))
    imgs, labels = imgs.to(device), labels.to(device)

    # Pass one batch through the network, and calculate the gradients for the weights
    feats = imgs.view(imgs.shape[0], -1)
    activations = {}
    with torch.no_grad():
        for layer_index, layer in enumerate(model.layers):
            feats = layer(feats)
            if isinstance(layer, nn.Linear):
                activations[f"Layer {layer_index}"] = (
                    feats.view(-1).detach().cpu().numpy()
                )

    ## Plotting
    fig = plot_dists(activations, color=color, stat="density", xlabel="Activation vals")
    fig.suptitle("Activation distribution", fontsize=14, y=1.05)
    plt.show()
    plt.close()

    if print_variance:
        for key in sorted(activations.keys()):
            print(f"{key} - Variance: {np.var(activations[key])}")
```

## Constant initialization

The first initialization we can consider is to initialize all weights with the same constant value. Zero is not a good idea as the propagated gradient would be zero,
but what if we initialize it slightly larger or smaller than zero?


```python
def const_init(model, c=0.0):
    for _, param in model.named_parameters():
        param.data.fill_(c)

model = BaseNetwork(act_fn=Identity()).to(device)
const_init(model, c=5e-03)
```


```python
model.layers[0].weight[:4]
```




    tensor([[0.0050, 0.0050, 0.0050,  ..., 0.0050, 0.0050, 0.0050],
            [0.0050, 0.0050, 0.0050,  ..., 0.0050, 0.0050, 0.0050],
            [0.0050, 0.0050, 0.0050,  ..., 0.0050, 0.0050, 0.0050],
            [0.0050, 0.0050, 0.0050,  ..., 0.0050, 0.0050, 0.0050]],
           device='cuda:0', grad_fn=<SliceBackward0>)




```python
model.layers[0].bias[:4]
```




    tensor([0.0050, 0.0050, 0.0050, 0.0050], device='cuda:0',
           grad_fn=<SliceBackward0>)




```python
visualize_weight_distribution(model)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_16_0.svg)




```python
visualize_gradients(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_17_0.svg)



    layers.0.weight - Variance: 7.095252856568407e-20
    layers.2.weight - Variance: 2.7083389842945504e-35
    layers.4.weight - Variance: 1.2037062152420224e-35
    layers.6.weight - Variance: 0.0
    layers.8.weight - Variance: 0.16812226176261902



```python
visualize_activations(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_18_0.svg)



    Layer 0 - Variance: 2.0582756996154785
    Layer 2 - Variance: 13.489119529724121
    Layer 4 - Variance: 22.100570678710938
    Layer 6 - Variance: 36.209571838378906
    Layer 8 - Variance: 14.831441879272461


The gradients of layers *[2, 4 and 6]* are basically the same. It seams that is zero but it is a value very close to it.
This is a big problem because those neurons were initialized with the same value and the gradients after back-propagation are basically the same,
which *mean* that those layers and neurons will learn the same features learning, there is a symmetry which is not desirable because it reduces the model's capability to learn diverse features.

Furthermore, the variance of the activations are slightly different. And we are looking to maintain the flux of the variance through the network.

## Constant variance

Constant initialization did not work, what if we randomly initialize the weights using a gaussian distribution?


```python
def gauss_init(model, std=0.01):
    for _, param in model.named_parameters():
        param.data.normal_(std)


model = BaseNetwork(act_fn=Identity()).to(device)
gauss_init(model)
```


```python
visualize_weight_distribution(model)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_23_0.svg)




```python
visualize_gradients(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_24_0.svg)



    layers.0.weight - Variance: 637654.875
    layers.2.weight - Variance: 1891422.875
    layers.4.weight - Variance: 4253399.5
    layers.6.weight - Variance: 8013594.0
    layers.8.weight - Variance: 265435744.0



```python
visualize_activations(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_25_0.svg)



    Layer 0 - Variance: 821.2817993164062
    Layer 2 - Variance: 445128.03125
    Layer 4 - Variance: 110167632.0
    Layer 6 - Variance: 33995933696.0
    Layer 8 - Variance: 2410235297792.0


There are two things here, the varience of the gradients in the first layers are smaller than the gradients in the last layers and the variance of the activations tends to increase and explote by layers pass.

## Xavier initialization

We need to sample the weights from a distribution, but we are not sure which one exactly.
We will try to find an optimal initialization from the activation distribution perspective.
The are two requirements:

1) The *mean* of every activation should be zero (**not all activation functions generate a mean of zero, e.g., ReLU!!**)

2) The variance of the activations should stay the same across every layer

Lets say that we want to design an initialization for the following layer $l$:

 $$y_{l} = W_{l}x_{l} + b_{l}, \quad y_{l} \in \mathbb{R}^{d_y}, \quad x_{l} \in \mathbb{R}^{d_x}$$

Where:
- $x_{l}$ is a $n_{l}-by-1$ vector that represents the activations of the previous layer $y_{l-1}$ that were passed through an activation function $f$, i.e., $x_{l} = f(y_{l-1})$.
- $W_{l}$ is a $d_{l}-by-n_{l}$ matrix of all connections (weights) from layer  $l-1$ and layer $l$.
- $b_{l}$ is a vector of biases of layer $l$ (usually initialized at 0).
- and $y_{l}$ is the vector of the activations before passing through the activation function.


There are some hypothesis made on those vectors and matrixes:

- The initialization of elements in $W_{l}$ are independent and share the same distribution.
- Likewise, elements of $x_{l}$ are mutually independent and share the same distribution.
- $x_{l}$ and $W_{l}$ are mutually independent.

Our goal is that the variance of $y_l$ is the same as the input, i.e. $Var(y_l) = Var(x_l) = \sigma_x^2$ and a *mean* of zero, i.e. $\mu = 0$. We assume that $x_{l}$ has a $\mu = 0$
as result of passing through the activation function $f$ and we do not take into account the vector bias $b$ because all of them will be initialized to zero.

$$
Var(y_l)= Var(W_{l}x_{l}) = \sigma_{x_l}^2
$$

Lets reduce the problem and study the output of a neuron $i$ in layer $l$ without the term bias $b$:

$$y_i^l = \sum_{j}w_{ij}^{l}x_{j}^{l}$$


For every single layer $l$ in the set of layers $\mathcal{L}$ this must hold; *the input and output of the neurons should respect the variance constraint $\sigma^2_{x_l}$*.

$$
Var(y_i)= Var(\sum_{j}w_{ij}x_{j}) = \sigma_{x_l}^2
$$

$j$ here represents the number of activations from previous layer. Notice that in the first layer it $max(j)$ is equal to the number of features.

Remember, we are looking for a good initialization for the neuron's weights.
This good initialization can be determined if we compute first the variance of the weights $Var(w)$,
in such manner that the input activations and output activations holds the variance constraint.

$$
\sigma_{x_l}^2 \Longleftrightarrow Var(\sum_{j}w_{ij}x_{j})
$$

As inputs and weights are independent each other:

$$
\sigma_{x_l}^2 \Longleftrightarrow \sum_{j}Var(w_{ij}x_{j})
$$

Given two independent variables (in our case; the neuron's weight $w$ and the activations of the previous layer $x_l$), the variance of their product follows the following equivalence:

$$
Var(X \cdot Y) = \mathbb{E}(Y)^2Var(X) + \mathbb{E}(X)^2Var(Y) + Var(X)Var(Y)
$$

The symbol $\mathbb{E}$ represents "the expected value". The expected value of a Gaussian distribution of $\mu = 0$ of course is zero. By this rule:

$$
\sigma_{x_l}^2 \Longleftrightarrow \sum_{j}(Var(w_{ij}) \cdot Var(x_{j}))
$$

Because every element of $x_l$ are independent and share the same distribution, i.e., variance equal for all $x_j \in x_l$:

$$
\sigma_{x_l}^2 \Longleftrightarrow d_x \cdot Var(w_{ij}) \cdot Var(x_{j})
$$

And because all elements of $x_j \in x_l$ follows the same distribution of $x_l$ hence, $\sigma_{x_l}^2 = Var(x_j)$.

$$
\sigma_{x_l}^2 = d_x \cdot Var(w_{ij}) \cdot \sigma_{x_l}^2
$$

We can conclude that the weights of the neurons should be initialized with a variance equal to:


$$
 \Longrightarrow \sigma_W^2 = \frac{1}{d_x}
$$

Concluding that; *the weights of each neuron should follow a normal distribution with a variance equal to the inverse of the size $d_x$, i.e.,
the inverse of the root of the number of activations from layer $l-1$.*


```python
def equal_var_init(model):
    for name, param in model.named_parameters():
        if name.endswith(".bias"):
            param.data.fill_(0)
        else:
            param.data.normal_(std=1 / np.sqrt(param.shape[0]))


model = BaseNetwork(act_fn=act_fn_by_name["tanh"]()).to(device)
equal_var_init(model)
```


```python
visualize_weight_distribution(model)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_37_0.svg)




```python
visualize_activations(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_38_0.svg)



    Layer 0 - Variance: 1.6039454936981201
    Layer 2 - Variance: 0.9554153680801392
    Layer 4 - Variance: 0.38129329681396484
    Layer 6 - Variance: 0.4804670810699463
    Layer 8 - Variance: 3.7180206775665283


If we do the same compute but instead of focusing on the variance of the activation functions we would like to stabilize the gradients, starting from $\triangle x = W \triangle y$ we would
conclude that layers should be initialized with a standard deviation equal to:

$$
\Longrightarrow \sigma_W^2 = \frac{1}{d_y}
$$


```python
def equal_var_grad(model):
    for name, param in model.named_parameters():
        if name.endswith(".bias"):
            param.data.fill_(0)
        else:
            param.data.normal_(std=1 / np.sqrt(param.shape[1]))


model = BaseNetwork(act_fn=act_fn_by_name["tanh"]()).to(device)
equal_var_grad(model)
```


```python
visualize_weight_distribution(model)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_41_0.svg)




```python
visualize_gradients(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_42_0.svg)



    layers.0.weight - Variance: 8.416534001298714e-06
    layers.2.weight - Variance: 1.4514725080516655e-05
    layers.4.weight - Variance: 1.3293202755448874e-05
    layers.6.weight - Variance: 2.5526887839077972e-05
    layers.8.weight - Variance: 0.00030599694582633674


Xavier initialization focuses on the **harmonic mean of the variances**.

$$
H(x_1, x_2, ..., x_n) = \frac{n}{\sum^{n}_{i = 1} \frac{1}{x_i}}
$$

Hence;

$$
\sigma^2_{harmonic} = H(\frac{1}{d_x}, \frac{1}{d_y}) = \frac{2}{\frac{1}{\frac{1}{d_x}} + \frac{1}{\frac{1}{d_y}}} = \frac{2}{d_x + d_y}
$$

Taking the square root to get the standard deviation:

$$
\sigma_{harmonic} = \sqrt{\frac{2}{d_x + d_y}}
$$

This leads us to the well-known Xavier initialization:

$$
W \sim \mathcal{N}\biggl(0, \sqrt{\frac{2}{d_x + d_y}}\biggr)
$$


```python
def xavier_normal(model):
    for name, param in model.named_parameters():
        if name.endswith(".bias"):
            param.data.fill_(0)
        else:
            param.data.normal_(std=np.sqrt(2 / (param.shape[0] + param.shape[1])))


model = BaseNetwork(act_fn=act_fn_by_name["tanh"]()).to(device)
xavier_normal(model)
```


```python
visualize_weight_distribution(model)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_46_0.svg)




```python
visualize_gradients(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_47_0.svg)



    layers.0.weight - Variance: 2.057873825833667e-05
    layers.2.weight - Variance: 3.505633503664285e-05
    layers.4.weight - Variance: 4.9378442781744525e-05
    layers.6.weight - Variance: 7.525320688728243e-05
    layers.8.weight - Variance: 0.0006904705078341067



```python
visualize_activations(model, print_variance=True)
```



![svg](assets/img/2024-08-07-initialization-of-nn/initialization-of-nn_48_0.svg)



    Layer 0 - Variance: 1.2162493467330933
    Layer 2 - Variance: 0.5854033827781677
    Layer 4 - Variance: 0.2972699701786041
    Layer 6 - Variance: 0.24673429131507874
    Layer 8 - Variance: 0.2928749620914459

