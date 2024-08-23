---
title: Modeling life satisfaction with a linear regressor
author: wilberquito
date: 2024-06-14 11:33:00 +0800
categories: [Machine Learning, Regressor]
tags: [programming, linear modeling, math, statistics]
pin: false
math: true
mermaid: true
---


<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import Markdown, display
from scipy.stats import normaltest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

sns.set_style("whitegrid")
sns.set_palette("viridis")
```

</details>


```python
data_root = "https://github.com/ageron/data/raw/main/"
lifesat = pd.read_csv(join(data_root, "lifesat", "lifesat.csv"))
lifesat.sort_values(by="Life satisfaction", ascending=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Country</th>
      <th>GDP per capita (USD)</th>
      <th>Life satisfaction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>25</th>
      <td>Denmark</td>
      <td>55938.212809</td>
      <td>7.6</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Finland</td>
      <td>47260.800458</td>
      <td>7.6</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Iceland</td>
      <td>52279.728851</td>
      <td>7.5</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Netherlands</td>
      <td>54209.563836</td>
      <td>7.4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Canada</td>
      <td>45856.625626</td>
      <td>7.4</td>
    </tr>
    <tr>
      <th>15</th>
      <td>New Zealand</td>
      <td>42404.393738</td>
      <td>7.3</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Sweden</td>
      <td>50683.323510</td>
      <td>7.3</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Australia</td>
      <td>48697.837028</td>
      <td>7.3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Israel</td>
      <td>38341.307570</td>
      <td>7.2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Austria</td>
      <td>51935.603862</td>
      <td>7.1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Germany</td>
      <td>50922.358023</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>United States</td>
      <td>60235.728492</td>
      <td>6.9</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Belgium</td>
      <td>48210.033111</td>
      <td>6.9</td>
    </tr>
    <tr>
      <th>13</th>
      <td>United Kingdom</td>
      <td>41627.129269</td>
      <td>6.8</td>
    </tr>
    <tr>
      <th>14</th>
      <td>France</td>
      <td>42025.617373</td>
      <td>6.5</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Spain</td>
      <td>36215.447591</td>
      <td>6.3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Poland</td>
      <td>32238.157259</td>
      <td>6.1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Italy</td>
      <td>38992.148381</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Lithuania</td>
      <td>36732.034744</td>
      <td>5.9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Slovenia</td>
      <td>36547.738956</td>
      <td>5.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Latvia</td>
      <td>29932.493910</td>
      <td>5.9</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Russia</td>
      <td>26456.387938</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Estonia</td>
      <td>35638.421351</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hungary</td>
      <td>31007.768407</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Turkey</td>
      <td>28384.987785</td>
      <td>5.5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Greece</td>
      <td>27287.083401</td>
      <td>5.4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Portugal</td>
      <td>32181.154537</td>
      <td>5.4</td>
    </tr>
  </tbody>
</table>
</div>




```python
X = lifesat[["GDP per capita (USD)"]].values
y = lifesat[["Life satisfaction"]].values
X.shape, y.shape
```




    ((27, 1), (27, 1))




```python
lifesat.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GDP per capita (USD)</th>
      <th>Life satisfaction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>27.000000</td>
      <td>27.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>41564.521771</td>
      <td>6.566667</td>
    </tr>
    <tr>
      <th>std</th>
      <td>9631.452319</td>
      <td>0.765607</td>
    </tr>
    <tr>
      <th>min</th>
      <td>26456.387938</td>
      <td>5.400000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>33938.289305</td>
      <td>5.900000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>41627.129269</td>
      <td>6.800000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>49690.580269</td>
      <td>7.300000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>60235.728492</td>
      <td>7.600000</td>
    </tr>
  </tbody>
</table>
</div>




```python
xmin, xmax = 23500, 62500
ymin, ymax = 4, 9

markdown = f"""
These are the boundaries of the axis we are going to use:

$
xmin, \ xmax = {xmin}, \ {xmax}
$
\\
$
ymin, \ ymax = {ymin}, \ {ymax}
$
"""

display(Markdown(markdown))
```



These are the boundaries of the axis we are going to use:

$
xmin, \ xmax = 23500, \ 62500
$
\
$
ymin, \ ymax = 4, \ 9
$



If both **GDP per capita** and **Life satisfaction** follow a normal distribution it makes sense to compute the correlation between them.
We can know that a feature follows a Gaussian distribution by plotting them (and see if they follow a normal distribution) or with statistical tests.


<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
fig, axes = plt.subplots(1, 2, figsize=(9, 3))

sns.kdeplot(X, ax=axes[0])
axes[0].set_title("GDP per capita (USD)")

sns.kdeplot(y, ax=axes[1])
axes[1].set_title("Life satisfaction")

plt.tight_layout()
plt.show()
```

</details>



![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_7_0.png)


 $H0$ also known as null hypothesis of `normaltest` is based on the asumption that it follows a normal form. A typical value use
to be sure that the null hypothesis is false is when the percentil is smaller than 0.05, i.e., $p < 0.05$.


```python
print("GDP per capita (USD)")
normaltest(X)
```

    GDP per capita (USD)
    NormaltestResult(statistic=array([3.26038932]), pvalue=array([0.19589144]))




```python
print("Life satisfaction")
normaltest(y)
```

    Life satisfaction
    NormaltestResult(statistic=array([14.71794254]), pvalue=array([0.00063685]))



From the visual and static normal test we can conclude that only **GDP per capita** follows a normal distribution. From this information
we know that probably the compute of the correlation and the use of linear regressor is not the best aprouch to make generalitations from the distribution data. Yet the linear correlation, points out that there is a high linear relation between the independent and dependent variable.


```python
corr = lifesat[["GDP per capita (USD)", "Life satisfaction"]].corr()
corr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GDP per capita (USD)</th>
      <th>Life satisfaction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>GDP per capita (USD)</th>
      <td>1.000000</td>
      <td>0.852796</td>
    </tr>
    <tr>
      <th>Life satisfaction</th>
      <td>0.852796</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



Modeling with a regressor means creating a line that minimizes the distance between the samples.

$Life \ satisfaction = \theta_{0} + \theta_{1} * GDP$


```python
def life_satisfaction(x, t0, t1):
    return t0 + t1 * x
```


```python
model = LinearRegression()
model.fit(X, y)

t0 = round(model.intercept_[0], 3)
t1 = model.coef_[0][0]

t0, t1
```




    (3.749, 6.778899694341222e-05)




```python
markdown = f"""
The linear equation that minimizes the error in the hole dataset is the follow:

$Life \ satisfaction = {t0} + {t1} * GDP$
"""

display(Markdown(markdown))
```



The linear equation that minimizes the error in the hole dataset is the follow:

$Life \ satisfaction = 3.749 + 6.778899694341222e-05 * GDP$




```python
yhat = life_satisfaction(X, t0, t1)
yhat[:5]
```




    array([[5.542452  ],
           [5.59876401],
           [5.67318985],
           [5.77809374],
           [5.85098552]])




```python
yhat_m = model.predict(X)
yhat_m[:5]
```




    array([[5.54250143],
           [5.59881344],
           [5.67323928],
           [5.77814317],
           [5.85103495]])



The values predicted by the model and the function `life_satisfaction`
are very similar, as you can appreciate it by the compute of the median error using the Manhattan distance.

$$
error = \frac{\sum_{i=0}^{n} | y_i - \hat{y}_i |}{n}
$$


```python
err = np.abs(np.sum((yhat - yhat_m))) / len(yhat)
err
```




    4.942737690907909e-05




<details markdown="1">

<summary><i>Hidden code</i></summary>

```python
fig, ax = plt.subplots(1, 1, figsize=(6, 4))

sns.lineplot(x=X.ravel(), y=yhat.ravel(), color="#d69cff")
sns.scatterplot(x=X.ravel(), y=y.ravel())

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_xlabel("GDP per capita (USD)")
ax.set_ylabel("Life satisfaction")

plt.show()
```

</details>



![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_21_0.png)



As you probably noticed, this model is kinda useless. It is cool to explain maths but we make no prediction on unseen data. So lets simulate that we have two dataset, one for training the model and one for actual testing the model and lets see its performance.


```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train.shape, X_test.shape, y_train.shape, y_test.shape
```




    ((21, 1), (6, 1), (21, 1), (6, 1))


<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
fig, ax = plt.subplots(1, 1, figsize=(6, 4))

sns.scatterplot(x=X_train.ravel(), y=y_train.ravel())
sns.scatterplot(x=X_test.ravel(), y=y_test.ravel(), color="orange", marker="$\circ$")

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_xlabel("GDP per capita (USD)")
ax.set_ylabel("Life satisfaction")

plt.show()
```

</details>



![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_24_0.png)




```python
model = LinearRegression()
model.fit(X_train, y_train)

t0 = round(model.intercept_[0], 3)
t1 = model.coef_[0][0]

t0, t1
```




    (3.533, 7.18650303768337e-05)




```python
markdown = f"""
The linear equation that minimizes the error in the train dataset is the follow:

$Life \ satisfaction = {t0} + {t1} * GDP$
"""

display(Markdown(markdown))
```



The linear equation that minimizes the error in the train dataset is the follow:

$Life \ satisfaction = 3.533 + 7.18650303768337e-05 * GDP$




```python
yhat_train = model.predict(X_train)
yhat_train[:5]
```




    array([[6.8281986 ],
           [6.92910967],
           [6.33488274],
           [7.42848276],
           [5.49369788]])



<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
fig, ax = plt.subplots(1, 1, figsize=(6, 4))

sns.scatterplot(x=X_test.ravel(), y=y_test.ravel(), color="orange", marker="$\circ$")
sns.scatterplot(x=X_train.ravel(), y=y_train.ravel())
sns.lineplot(x=X_train.ravel(), y=yhat_train.ravel(), color="#d69cff")

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_xlabel("GDP per capita (USD)")
ax.set_ylabel("Life satisfaction")

plt.show()
```

</details>



![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_28_0.png)




```python
yhat_test = model.predict(X_test)
yhat_test[:5]
```




    array([[6.13533505],
           [6.52424572],
           [6.15921518],
           [7.19224761],
           [5.43399993]])



In the following figure we can appreciate the predicted values which are projected in the regression line vs the real values gave by the test dataset.


<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
fig, ax = plt.subplots(1, 1, figsize=(6, 4))

sns.lineplot(x=X_train.ravel(), y=yhat_train.ravel(), color="#d69cff")
sns.scatterplot(x=X_train.ravel(), y=y_train.ravel())

for i, x in enumerate(y_test):
    stack_y = np.vstack((x, yhat_test[i]))
    stack_x = np.repeat(X_test[i], len(stack_y))

    sns.lineplot(x=stack_x.ravel(), y=stack_y.ravel(), color="orange")

sns.scatterplot(x=X_test.ravel(), y=y_test.ravel(), color="orange", marker="$\circ$")
sns.scatterplot(x=X_test.ravel(), y=yhat_test.ravel(), color="orange")

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_xlabel("GDP per capita (USD)")
ax.set_ylabel("Life satisfaction")

plt.show()
```

</details>



![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_31_0.png)



<details markdown="1">

<summary><i>Hidden code</i></summary>


```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.scatterplot(x=X.ravel(), y=y.ravel(), ax=axes[0])
sns.lineplot(x=X.ravel(), y=yhat.ravel(), color="#d69cff", ax=axes[0])

sns.lineplot(x=X_train.ravel(), y=yhat_train.ravel(), color="#d69cff", ax=axes[1])
sns.scatterplot(x=X_train.ravel(), y=y_train.ravel(), ax=axes[1])

for i, x in enumerate(y_test):
    stack_y = np.vstack((x, yhat_test[i]))
    stack_x = np.repeat(X_test[i], len(stack_y))
    sns.lineplot(x=stack_x.ravel(), y=stack_y.ravel(), color="orange", ax=axes[1])

sns.scatterplot(x=X_test.ravel(), y=y_test.ravel(), color="orange", marker="$\circ$")
sns.scatterplot(x=X_test.ravel(), y=yhat_test.ravel(), color="orange", ax=axes[1])

for ax in axes:
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_xlabel("GDP per capita (USD)")
    ax.set_ylabel("Life satisfaction")

axes[0].set_title("Linear model with the hole dataset")
axes[1].set_title("Linear model with train and test dataset")

plt.show()
```

</details>


![png](/assets/img/2024-06-18-lifesat-linear-regressor/Life-Satisfaction_32_0.png)
