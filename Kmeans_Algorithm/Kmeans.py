import pygame
from random import randint
import math
from sklearn.cluster import KMeans

pygame.init()

screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption("Kmeans")

GREY = (150,150,150)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235)
PURPLE = (128, 0, 128)
k=0
error =0
points = []
clusters = []
labels = []

COLORS =[BLUE,GREEN,PURPLE,RED,YELLOW,PINK,ORANGE,SKY_BLUE]
def Font_Render(string):
	font = pygame.font.SysFont("Arial",45)
	return font.render(string,True,WHITE)


def Check_Mouse_Pos(mouse,x,y):
	if  x < mouse < y:
		return True
	return False

def Draw():
	#draw panel
	pygame.draw.rect(screen,WHITE,pygame.Rect(50,50,850,600))
	
	#draw button
	# +
	pygame.draw.rect(screen,BLACK,pygame.Rect(950,50,50,50))
	screen.blit(Font_Render("+") ,(965,45))
	# -
	pygame.draw.rect(screen,BLACK,pygame.Rect(1015,50,50,50))
	screen.blit(Font_Render("-") ,(1030,45))
	#K Value
	
	screen.blit(Font_Render('K = '+str(k)),(1100,50))
	#Eror Value
	screen.blit(Font_Render('Error = '+str(int(error))),(950,350))
	# Run
	pygame.draw.rect(screen,BLACK,pygame.Rect(950,150,200,50))
	screen.blit(Font_Render("Run"),(965,145))
	#RanDom
	pygame.draw.rect(screen,BLACK,pygame.Rect(950,250,200,50))
	screen.blit(Font_Render("Random"),(965,245))
	#Algorithm
	pygame.draw.rect(screen,BLACK,pygame.Rect(950,450,200,50))
	screen.blit(Font_Render("Algorithm"),(965,445))
	#Reset
	pygame.draw.rect(screen,BLACK,pygame.Rect(950,550,200,50))
	screen.blit(Font_Render("Reset"),(965,545))
	
	#Point
	
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0]+50,points[i][1]+50), 6)
		if len(labels) !=0 :
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0]+50,points[i][1]+50), 5)
		else:
			pygame.draw.circle(screen, WHITE, (points[i][0]+50,points[i][1]+50), 5)
	#Cluster 
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[i], (clusters[i][0]+50,clusters[i][1]+50) , 10)
	
def Random():
	for i in range(k):
		point = (randint(0,850) ,randint(0,600))
		clusters.append(point)

def distance(point,cluster):
	return math.sqrt(pow((point[0]-cluster[0]),2)+pow((point[1]-cluster[1]),2))

def Run():
	for p in points:
		distances_to_cluster = []
		for c in clusters:
			dis = distance(p,c)
			distances_to_cluster.append(dis)
		min_dis = min(distances_to_cluster)
		labels.append(distances_to_cluster.index(min_dis))
		
	for cluster in range(k):
		number =0
		sumx = 0
		sumy = 0
		averagex = 0
		averagey = 0 
		for j in range(len(points)):
		 	if labels[j] == cluster:
		 		sumx += points[j][0]
		 		sumy += points[j][1]
		 		number +=1
		if number!=0:
			averagex = sumx/number
			averagey = sumy/number
			clusters[cluster] =(averagex,averagey)
	

def Check_distance():
	if len(clusters) >0:
		distances_to_cluster = []
		for c in clusters:
			dis = distance(points[len(points)-1],c)
			distances_to_cluster.append(dis)
		min_dis = min(distances_to_cluster)
		
		labels.append(distances_to_cluster.index(min_dis))
	

running = True
clock = pygame.time.Clock()
while running:
	clock.tick(60)
	screen.fill(GREY)
	
	Draw()
	mouse_x,mouse_y = pygame.mouse.get_pos()
	#MouseEnter
	if Check_Mouse_Pos(mouse_x,50,900) and Check_Mouse_Pos(mouse_y,50,650):
		mouse_pos = "   ("+str(mouse_x - 50)+' , '+ str(mouse_y -50)+")"
		font = pygame.font.SysFont("Arial",15)
		screen.blit(font.render(mouse_pos,True,RED),(mouse_x,mouse_y))
		
	#Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if (event.type == pygame.MOUSEBUTTONDOWN):
			#Create Point
			if Check_Mouse_Pos(mouse_x,50,900) and Check_Mouse_Pos(mouse_y,50,650):
				points.append((mouse_x-50,mouse_y-50))
				Check_distance()
			#Change btn+
			if Check_Mouse_Pos(mouse_x,950,1000) and Check_Mouse_Pos(mouse_y,50,100) :		
				if k < 7:
					k = k+1
			#Change btn-
			if  Check_Mouse_Pos(mouse_x,1015,1065)  and Check_Mouse_Pos(mouse_y,50,100):		
				if k > 0:
					k = k-1
				
			#ChangeRun	
			if Check_Mouse_Pos(mouse_x,950,1150) and Check_Mouse_Pos(mouse_y,150,200):
				
				if len(clusters) != 0 :
					labels = []
					Run()
			
			#Change btnRandom	
			if Check_Mouse_Pos(mouse_x,950,1150) and Check_Mouse_Pos(mouse_y,250,300):		
				clusters = []
				labels = []
				Random()	
			#ChangeAlgorithm
			if Check_Mouse_Pos(mouse_x,950,1150) and Check_Mouse_Pos(mouse_y,450,500) and k>0:
				
				kmeans = KMeans(n_clusters=k ,n_init=10).fit(points)
				labels = kmeans.predict(points)
				clusters = kmeans.cluster_centers_
				error = 0
				labels= labels.tolist()
				#pass
			#ChangeReset
			if Check_Mouse_Pos(mouse_x,950,1150) and Check_Mouse_Pos(mouse_y,550,600):		
				k=0
				error =0
				points =[]
				clusters = []
				labels =[]
	error=0
	if len(clusters)> 0 and len(labels) > 0:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])
	
	pygame.display.flip()


pygame.quit()