import matplotlib.pyplot as plt  
import numpy as np
from sklearn.cluster import KMeans 

#ReadImage
img = plt.imread("IMG_4043.JPG")

print(img.shape)

witdh = img.shape[0]
height = img.shape[1]

img = img.reshape(witdh*height,3)

#Kmeans with each element
kmeans = KMeans(n_clusters=30 ,n_init=10).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_


img2 = np.zeros_like(img)   

for i in range(len(img2)):
    img2[i] = clusters[labels[i]]
#
img2 = img2.reshape(witdh,height,3)
plt.imshow(img2)
plt.show()