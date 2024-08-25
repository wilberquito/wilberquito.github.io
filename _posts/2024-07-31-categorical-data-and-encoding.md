---
title: Categorical data and encoding
author: wilberquito
date: 2024-07-31 15:33:00 +0800
categories: [Machine Learning, Bases]
tags: [programming, encoding, onehot, embedding]
pin: false
math: true
mermaid: true
---

> *Check out the original notebook [here](https://github.com/wilberquito/Hands-On-ML/blob/main/uvadlc_notebooks/categorical-data-and-encoding.ipynb){:target="_blank"}.*
{: .prompt-info }


Categorical data requires special care. Data like language characters ‘a’, ‘b’, ‘c’ etc. are usually represented as integers 0, 1, 2, etc. Do not use integers as input for categorical data. If you would enter those integers as inputs to the model, two problems arise.

1) You bias the model to see relations where there are none. In the language example above, the model would think that ‘a’ is closer to ‘b’ than to ‘o’, although ‘a’ and ‘o’ are both vocals, and the closeness of ‘a’ and ‘b’ does not necessarily say anything about their usage.

2) If you have many categories, you will have input values between 0 and >50. The model will have a hard time separating all those >50 categories without blending over some. Hence, the model loses a lot of information although this is not necessary.

The much better option in the case of categorical data is to use one-hot vectors, or embeddings.


```python
import pandas as pd

blood_type_categories = pd.DataFrame(
    {"blood_type": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]}
)
blood_type_categories
```

| |blood_type|
|:----|:----|
|0|A+|
|1|A-|
|2|B+|
|3|B-|
|4|AB+|
|5|AB-|
|6|O+|
|7|O-|


## OneHot Encoding

A one-hot vector represents each category by a vector of 0s, with one index being 1.

### Sklearn OneHotEncoder


```python
from sklearn.preprocessing import OneHotEncoder

onehot = OneHotEncoder(sparse_output=False)
onehot_encoding = onehot.fit_transform(blood_type_categories)
onehot_encoding
```




    array([[1., 0., 0., 0., 0., 0., 0., 0.],
           [0., 1., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 1., 0., 0., 0.],
           [0., 0., 0., 0., 0., 1., 0., 0.],
           [0., 0., 1., 0., 0., 0., 0., 0.],
           [0., 0., 0., 1., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 1., 0.],
           [0., 0., 0., 0., 0., 0., 0., 1.]])




```python
onehot_encoding.shape
```




    (8, 8)



### PyTorch OneHotEncoder


```python
from sklearn.preprocessing import LabelEncoder
import torch.nn.functional as F
import torch
import numpy as np

encoder = LabelEncoder()
labels_blood_type = encoder.fit_transform(blood_type_categories["blood_type"])
labels_blood_type.tolist()
```




    [0, 1, 4, 5, 2, 3, 6, 7]




```python
tensor = torch.tensor(labels_blood_type.tolist())
tensor
```




    tensor([0, 1, 4, 5, 2, 3, 6, 7])




```python
onehot_encoding = F.one_hot(tensor)
onehot_encoding
```




    tensor([[1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]])




```python
onehot_encoding.shape
```




    torch.Size([8, 8])



## Embedding Encoding

It allows for the conversion of categorical data, such as words or items, into vectors of continuous numbers. The beauty of embeddings lies in their ability to capture the underlying semantics and relationships between different categories.

 Properties:

1) **Dense Representation:** While methods like one-hot encoding lead to sparse vectors (mostly zeros with a single one), embeddings result in dense vectors where every dimension can contain any real number.Advantages: Dense vectors are more memory-efficient and can capture more information in fewer dimensions compared to sparse representations.

2) **Semantic Meaning:** One of the primary goals of embeddings is to represent data in such a way that the spatial distances between vectors correlate with semantic similarities.Example: In a well-trained word embedding space, synonyms or related words will be closer to each other. For instance, "king" and "monarch" would have vectors that are near each other.

3) **Dimensionality Reduction:** Embeddings help in reducing the dimensionality of data. Instead of having a dimension for every possible category, the data is represented in a much smaller, fixed-size space. Advantages: This leads to more efficient storage and computation, especially when dealing with a large number of categories.

The Embedding layer requires at least 2 arguments; `num_embeddings` and `embedding_dim`. There are others optional parameters though.

- **num_embeddings**: it means the size of the diccionary. If you have a vocabulary of 100 words, then the size of the dict is 100.
- **embedding_dim**: this is the size of the embedding resulting vector.


We want to encode the blood type, there are 8 different blood types. So, the number of embeddings must be 8. The dim of each embedded vector can varie but lets say we set it to 16.


```python
blood_type_categories["blood_type"].values.tolist()
```




    ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']




```python
word2idx = {
    blood_type: i for i, blood_type in enumerate(blood_type_categories["blood_type"])
}
word2idx
```




    {'A+': 0, 'A-': 1, 'B+': 2, 'B-': 3, 'AB+': 4, 'AB-': 5, 'O+': 6, 'O-': 7}




```python
vocab_size = len(word2idx)
vocab_size
```




    8




```python
embedding_dim = 16
embedding_dim
```




    16




```python
encoded_type_categories = [
    word2idx[word] for word in blood_type_categories["blood_type"].values
]
encoded_type_categories
```




    [0, 1, 2, 3, 4, 5, 6, 7]




```python
input_tensor = torch.tensor(encoded_type_categories).reshape((vocab_size, -1))
input_tensor
```




    tensor([[0],
            [1],
            [2],
            [3],
            [4],
            [5],
            [6],
            [7]])




```python
from sklearn.preprocessing import LabelEncoder
import torch.nn.functional as F
import torch
import torch.nn as nn

torch.manual_seed(42)

embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
embed_vectors = embedding(input_tensor)

print("Input shape:", input_tensor.shape)
print("Output shape:", embed_vectors.shape)
```

    Input shape: torch.Size([8, 1])
    Output shape: torch.Size([8, 1, 16])



```python
input_tensor[0, :]
```




    tensor([0])




```python
embed_vectors[0, :, :]
```




    tensor([[ 1.9269,  1.4873,  0.9007, -2.1055,  0.6784, -1.2345, -0.0431, -1.6047,
             -0.7521,  1.6487, -0.3925, -1.4036, -0.7279, -0.5594, -0.7688,  0.7624]],
           grad_fn=<SliceBackward0>)
