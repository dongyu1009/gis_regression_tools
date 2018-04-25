
import numpy as np
import time
from sklearn import linear_model,datasets

X = [[1],[2],[3],[4],[5]]
y = [1,2,3,4,6]
model = linear_model.LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)


model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
model_ransac.fit(X, y)

model_san = linear_model.TheilSenRegressor()
model_san.fit(X, y)

print "model.coef_: ", model.coef_
print "model.r2: ", r2
print "model.model_san: ", model_san.coef_[0]
print "model_ransac.coef_: ", model_ransac.estimator_.coef_