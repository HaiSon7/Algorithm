import numpy 
import matplotlib
import matplotlib.pyplot as plt
A =[1,2,5,7,8,9,11,16,18,27,30]
b =[0,2,3,5,6,9,10,14,15,23,27]
print(A)
minA = min(A)
maxA = max(A)

plt.plot(A,b,'ro')
A= numpy.array([A]).T
b= numpy.array([b]).T
print(A)

ones = numpy.ones((A.shape[0],1),dtype = numpy.uint8)
print(ones)
A = numpy.concatenate((A,ones),axis = 1)
print(A)
	
x = numpy.linalg.inv(A.transpose().dot(A)).dot(A.transpose()).dot(b)
print(x)
x0 = numpy.array([minA,maxA]).T
print(x0)
y0 = x[0][0]*x0 + x[1][0]
plt.plot(x0,y0)
plt.show()