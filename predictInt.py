import matplotlib.pyplot as plt

from sklearn import datasets 	#sample datsets
from sklearn import svm  		#support vector machine

digits = datasets.load_digits()

#classifier
#gamma = learning rate
clf = svm.SVC(gamma = 0.0001, C = 100) 

print(len(digits.data))

#test set
x,y = digits.data[:-10], digits.target[:-10]

#training
clf.fit(x,y)

print('Prediction :',clf.predict(digits.data[[-16]]))

plt.imshow(digits.images[-16], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()