import cv2 
import numpy as np
import time 
import os 
import handModule as htm




brush=5
eraser=50
xp,yp=0,0

folderPath="Header"

mylist=os.listdir(folderPath)
# print(mylist)

overlayLst=[]
for imagePath in mylist:

	image=cv2.imread(f'{folderPath}/{imagePath}')
	# print(image)
	overlayLst.append(image)

# print(overlayLst[0])

header=overlayLst[0]   #image

drawColor=(255,0,255)

cap=cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)


detector =htm.handDetector(detectionCon=0.85)

imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:


	# import the image
	success,img=cap.read()

	img=cv2.flip(img,1)

	# find the hand mark

	img=detector.findHands(img)


	# check which finger is up
	





	# setting the header image


	

	lnlist=detector.findPosition(img,draw=False)
	
	if len(lnlist)!=0:


		# print(lnlist)

		#tip of imdex and middle finger
		x1,y1=lnlist[8][1:]
		x2,y2=lnlist[12][1:]

		# print(x1,x2)





		finger=detector.fingersUp()
		# print(finger)


		# if selection mode -two finger is up then we have to select the color
		# if drawing mode then we have to draw 
		

		if finger[1] and finger[2]:

			xp,yp=0,0

			



			
			# print("This is the selection mode")

			if y1<125:

				if 250<x1<450:

					header=overlayLst[0]
					drawColor=(255,0,255)

				elif 550<x1<750:

					header=overlayLst[1]
					drawColor=(255,0,0)

				elif 800<x1<950:

					header=overlayLst[2]
					drawColor=(0,255,0)

				elif 1000<x1<1200:

					header=overlayLst[3]
					drawColor=(0,0,0)

			cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
			
			


		if finger[1] and finger[2]==False:


			cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
			# print("this is the drawing mode")

			if xp==0 and yp==0:
				xp,yp=x1,y1

			if drawColor==(0,0,0):
				cv2.line(img,(xp,yp),(x1,y1),drawColor,brush)
				cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraser)

			else:
				cv2.line(img,(xp,yp),(x1,y1),drawColor,brush)
				cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brush)

			xp,yp=x1,y1


	imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)

	_, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)

	imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

	img=cv2.bitwise_and(img,imgInv)
	img=cv2.bitwise_or(img,imgCanvas)


	img[0:125,0:1280]=header

	# img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

	cv2.imshow("imgae",img)
	cv2.imshow("image2",imgCanvas)
	cv2.imshow("image3",imgInv)

	cv2.waitKey(1)
