from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import neighbors
import pandas as pd
import numpy
import math
import operator
import tkinter as tk
from tkinter import Text
from tkinter import messagebox 
from tkinter import font

#Reand IMDB Dataset
data = pd.read_csv('IMDB Dataset.csv', index_col=None)


#Get review,sentiment columns 
#Data train

reviews = data['review'].to_numpy().tolist()

sentiments_train = data['sentiment'].to_numpy().tolist()[:500]


vectorizer = TfidfVectorizer()
reviews_matrix= vectorizer.fit_transform(reviews)
reviews_train_matrix = reviews_matrix[:500]



def calculate_distance(p1,p2):
    return numpy.linalg.norm(p1 - p2)

def get_k_neighbors(reviews_train_matrix,sentiments_train,point,k):
    distances = []
    neighbors = []
    
    for i in range(reviews_train_matrix.shape[0]):
        dis = calculate_distance(reviews_train_matrix[i].toarray(),point)
        distances.append((dis,sentiments_train[i]))

    #sort by distance
    distances.sort(key =operator.itemgetter(0))

    for i in range(k):
        neighbors.append(distances[i][1])
    return neighbors

def predict(reviews_train_matrix,sentiments_train,point,k):
    neighbors_labels = get_k_neighbors(reviews_train_matrix,sentiments_train,point,k)
    
    return highest_votes(neighbors_labels)

def highest_votes(neighbors):
    #x[p,p,p,p,n,n,p,n]
    max_count =0

    for i in range(len(neighbors)): 
        max_count = 0
        count =0
        for j in range(len(neighbors)):
            if neighbors[j] == neighbors[i]:
                count+=1
        if count >max_count:
            max_count = count

    for i in range(len(neighbors)):
        count =0
        for j in range(len(neighbors)):
            if neighbors[j] == neighbors[i]:
                count+=1
        if count == max_count:
            label_final=neighbors[i] 

    return label_final


def classify_text():
    # Lấy văn bản từ ô nhập liệu
    text = text_entry.get("1.0", "end").strip()
    
    # Kiểm   tra xem người dùng đã nhập văn bản hay chưa
    if not text:
        messagebox.showinfo("Notification", "Please enter text to classify.")
        return
    new_list = []
    new_list.append(text)
    print(new_list)
    #Phan loai van ban moi den
    point_test = vectorizer.transform(new_list)
    k=5
    new_label = predict(reviews_train_matrix,sentiments_train,point_test.toarray(),k)
    print(new_label)
    result_label.config(text="Result:  " +new_label)   

    # Use KNN in Sklearn
    # knn = neighbors.KNeighborClassifier(n_neighbors= k)
    # knn.fit(reviews_train_matrix,sentiments_train)
    # knn.predict(new_list)
 
# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Classify Text By KNN")
custom_font = font.Font(family="Arial", size=20, weight="bold")
root.title_font = custom_font  


# Tạo ô nhập liệu
text_label = tk.Label(root, text="Enter Text :",font = ("Arial",15))
text_label.pack()
text_entry = Text(root, font = ("Arial",15 ),height=25, width=75)
text_entry.pack()

# Tạo nút phân loại
classify_button = tk.Button(root, text=" Classify ",font = ("Arial",15), command=classify_text,bg = "aqua")
classify_button.pack()


# Kết quả phân loại
result_label = tk.Label(root, text="Result :  ",font = ("Arial",17,"bold"),fg="red")
result_label.pack()

# Khởi chạy ứng dụng
root.mainloop()
