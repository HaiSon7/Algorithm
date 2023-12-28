import cv2
import numpy as np

link1 = r"C:\Python\pythonProject\beautiful-face-young-woman-clean-skin-fresh-isolated-white-38897486.webp"
link2 = r"C:\Python\pythonProject\woman-6328478_1280.webp"
link3 = r"C:\Python\pythonProject\images.jpg"
link4 = r"C:\Users\sonng\OneDrive\Pictures\Saved Pictures\IMG_4043.JPG"

img = cv2.imread(link2)
#Resize image to (500,500)
img = cv2.resize(img, (500, 500))
#Convert color to Gray (Balck White)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

class Convu2d:

    def __init__(self, input, kernel_size=3,numOfKernel = 8, padding=0, stride=1):
        
        self.input = np.pad(input, pad_width=(padding, padding), mode='constant')
        self.width, self.height = self.input.shape
        self.stride = stride

        #Kernel Chuẩn
        #self.gaussian_kernel_1d = cv2.getGaussianKernel(kernel_size, sigma=1)
        #self.gaussian_kernel_2d = np.outer(self.gaussian_kernel_1d, self.gaussian_kernel_1d)

        #Keernel random
        self.gaussian_kernel_2d = np.random.randn(numOfKernel,kernel_size,kernel_size)

        self.results = np.zeros((int((self.height - kernel_size) / self.stride) + 1,int((self.width - kernel_size) / self.stride) + 1,numOfKernel))

    def print_test(self):
        print("kernel")
        print(self.gaussian_kernel_2d)
        print("kernel.shape")
        print(self.gaussian_kernel_2d.shape)

    def getROI(self):

        #roi : Vung Dien tich quan tam
        for row in range(0, int((self.height - self.gaussian_kernel_2d.shape[1]) / self.stride) + 1):
            for col in range(0, int((self.width - self.gaussian_kernel_2d.shape[2]) / self.stride) + 1):
                roi = self.input[row*self.stride: row*self.stride + self.gaussian_kernel_2d.shape[1],col*self.stride: col*self.stride + self.gaussian_kernel_2d.shape[2]]
                yield row, col, roi

    def calculate(self):
        for layer in range(self.gaussian_kernel_2d.shape[0]):
            for row, col, roi in self.getROI():
                self.results[row,col,layer] = np.sum(roi * self.gaussian_kernel_2d[layer])

        print(self.results.shape)
        #Convert to int to show img
        return self.results

class LeakyRelu:
    def __init__(self,input):
        self.input = input
        self.results = np.zeros((self.input.shape[0],
                                self.input.shape[1],
                                self.input.shape[2]))

    def calculate(self):
        for layer in range(self.input.shape[2]):
            for row in range(self.input.shape[0]):
                for col in range(self.input.shape[1]):
                    if self.input[row,col,layer] < 0:
                        self.results[row,col,layer] = self.input[row,col,layer] *0.1
                    else:
                        self.results[row,col,layer] = self.input[row,col,layer]

        return self.results


class MaxPooling:
    def __init__(self,input,pooling_size = 2):
        self.input = input
        if pooling_size < 2:
            self.pooling_size =2
        else:
            self.pooling_size = pooling_size
        self.results = np.zeros((int(self.input.shape[0]/self.pooling_size),int(self.input.shape[1]/self.pooling_size),self.input.shape[2]))

    def calculate(self):
        for layer in range(self.input.shape[2]):
            for row in range(0,int(self.input.shape[0]/self.pooling_size)):
                for col in range(0,int(self.input.shape[1]/self.pooling_size)):
                    self.results[row,col,layer] = np.max(self.input[row*self.pooling_size : row*self.pooling_size+ self.pooling_size,col*self.pooling_size:col*self.pooling_size + self.pooling_size,layer])

        return self.results

class Flatten:
    def __init__(self,input):
        self.input = input
        self.results = np.zeros((self.input.shape[0],self.input.shape[1],self.input.shape[2]))
    def flatten(self):
        self.results = self.input.flatten()
        return self.results

class Softmax:
    def __init__(self,input,output_size):
        self.input = input
        self.output_size = output_size
        self.weights = np.random.randn(self.input.shape[0])/self.input.shape[0]
        self.bias = np.random.randn(self.output_size)
        
    def calculate(self):
        totals = np.dot(self.input,self.weights) + self.bias
        exp = np.exp(totals)
        return exp/sum(exp)


convu2d = Convu2d(img_gray, numOfKernel = 8, padding = 0,stride = 1)
new_img = convu2d.calculate()


convu2d_relu = LeakyRelu(new_img)
new_img_relu = convu2d_relu.calculate()

max_pooling = MaxPooling(new_img_relu,2)
new_img_relu_max_pooling = max_pooling.calculate()

flatten_data = Flatten(new_img_relu_max_pooling)
new_img_relu_max_pooling_flatten = flatten_data.flatten() 

x = Softmax(new_img_relu_max_pooling_flatten,10)
print(x.calculate())

# x = np.hstack((new_img[:,:,0],new_img[:,:,1],new_img[:,:,2]))
# x_relu = np.hstack((new_img_relu[:,:,0],new_img_relu[:,:,1],new_img_relu[:,:,2]))


if img is not None:
    cv2.imshow("Image", img)
    cv2.imshow("Image_Convu",new_img[:,:,0].astype(np.uint8))
    cv2.imshow("Image_LeakyRelu",new_img_relu[:,:,0].astype(np.uint8))
    cv2.imshow("Image_LeakyRelu_MaxPooling",new_img_relu_max_pooling[:,:,0].astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    # #cv2.imshow("Convolution Result Relu", new_img_relu)
    
else:
    print("Không thể đọc ảnh.")

