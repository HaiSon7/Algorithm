import numpy 
import matplotlib
import matplotlib.pyplot as plt
from sklearn import linear_model
A = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
b = [2,5,7,9,11,16,19,23,22,29,29,35,37,40,46,42,39,31,30,28,20,15,10,6]


maxA = max(A)


plt.plot(A,b,'ro')
A= numpy.array([A]).T
b= numpy.array([b]).T
x_square = numpy.array([A[:,0]**2 ]).T

ones = numpy.ones((A.shape[0],1),dtype = numpy.uint8)

A = numpy.concatenate((x_square,A,ones),axis = 1)
print(A)
	
x = numpy.linalg.inv(A.transpose().dot(A)).dot(A.transpose()).dot(b)

print(x)

#x0 = numpy.linspace(1,maxA,10000)

#y0 = x[0][0]*x0*x0+ x[1][0]*x0 + x[2][0]




# Use sklearn
lr = linear_model.LinearRegression()
lr.fit(A,b)
print(type(lr.intercept_))
x0 = numpy.linspace(1,maxA,10000)
y0 = lr.coef_[0][0]*x0*x0+ lr.coef_[0][1]*x0 + lr.intercept_[0]
plt.plot(x0,y0)
plt.show()