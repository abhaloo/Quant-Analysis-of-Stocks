#Followed a quick tutorial from pythonprogramming.net on Support Vector Machines
#Used it to classify and plot a simple dataset 
#
#
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm 
from matplotlib import style
style.use("ggplot")

x = [1,5,1.5,8,1,9]
y = [2,8,1.8,8,0.6,11]


#numpy array of arrays
X = np.array([[1,2],
			[5,8],
			[1.5,1.8],
			[8,8],
			[1,0.6],
			[9,11]])

y = [0,1,0,1,0,1]

#classifier
# C can be adjusted accordingly
clf = svm.SVC(kernel = 'linear', C = 1.0)
#fit data in classifier
clf.fit(X,y)

#prediction varies according to the degree of difference from orginal dataset
print(clf.predict([[10.58,10.76]]))

w = clf.coef_[0]
print(w)

a = -w[0]/w[1]

xx = np.linspace(0,12)
yy = a * xx - clf.intercept_[0] / w[1]

#plot 
h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

plt.scatter(X[:,0],X[:,1],c =y)
plt.show()
plt.legend()
