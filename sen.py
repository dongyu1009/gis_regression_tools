# -*- coding: utf-8 -*-

"""

Theil-Sen 回归

本例生成一个数据集，然后在该数据集上测试Theil-Sen回归

"""

print __doc__

import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, TheilSenRegressor,\
                                 RANSACRegressor

estimators = [('OLS', LinearRegression()),
              ('Theil-Sen', TheilSenRegressor())]

# 异常值仅仅出现在y轴
np.random.seed((int)(time.time() % 100))
n_samples = 200

# 线性模型的函数形式为： y = 3 * x + N(2, .1 ** 2)
x = np.random.randn(n_samples)
w = 3.
c = 2.
noise = c + 0.1 * np.random.randn(n_samples)
y = w * x + noise

# 加入10%的异常值,最后20个值称为异常值
y[-20:] += -20 * x[-20:]

print x
print y 

X = x[:, np.newaxis]
print X
plt.plot(X, y, 'k+', mew=2, ms=8)
line_x = np.array([-3, 3])

print line_x

for name, estimator in estimators:
    t0 = time.time()
    estimator.fit(X, y)
    elapsed_time = time.time() - t0
    y_pred = estimator.predict(line_x.reshape(2, 1))
    plt.plot(line_x, y_pred, label='%s (fit time: %.2fs)'
             %(name, elapsed_time))

plt.axis('tight')
plt.legend(loc='upper left')

plt.show()