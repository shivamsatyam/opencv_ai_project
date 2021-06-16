def virtual_painter(url):
	try:
		import pymsgbox
		import cv2
		# import mediapipe as mp
		#import math
		import os
		import numpy as np
		import hand_detector as htm

		pymsgbox.alert("press q to quit the window")

		##############################

		brushThickness = 15
		eraserThickness = 50
		xp,yp = 0,0
		##############################
		imgCanvas = np.zeros((700,1109,3),np.uint8)

		folderPath = "Header"
		myList = os.listdir(folderPath)
		overlayList = []

		for imPath in myList:
			image = cv2.imread(f"{folderPath}/{imPath}")
			overlayList.append(image)


		header = overlayList[0]
		drawColor = (255,0,255)

		if url:
			cap = cv2.VideoCapture(url)
		else:
			cap = cv2.VideoCapture(0)
			

		detector = htm.handDetector(detectionCon=0.85)

		while True:
			sucees,img = cap.read()
			img = cv2.flip(img,1)
			img = cv2.resize(img,(1109,700),interpolation=cv2.INTER_AREA)
			# 2  find hand landmarks
			
			img = detector.findHands(img)
			lmList = detector.findPosition(img,draw=False)

			if len(lmList)!=0:

				#print(lmList)
		        # x1,y1 = lmList[8][1:]
		        # x2,y2 = lmList[12][1:]

				x1,y1 = lmList[8][1:]
				x2,y2 = lmList[12][1:]



				# 3 check which finder is up

				fingers = detector.fingersUp()
				# print(fingers)

			# 4 if selection mode - two finger are up
				if fingers[1] and fingers[2]:
					xp,yp = 0,0
					# print("selection mode")

					if y1<107:
						if 190<x1<300:
							header = overlayList[0]
							drawColor = (255,0,255)

						elif 450<x1<570:
							header = overlayList[1]
							drawColor = (255,0,0)
						
						elif 730<x1<840:
							header = overlayList[2]
							drawColor = (0,255,0)

						elif 980<x1<1070:
							header = overlayList[3]
							drawColor = (0,0,0)
							

					cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)



			# 5 if drawing mode - Index finger is up
				if fingers[1] and fingers[2]==False:
					cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)	
					# print("drawing mode")

					if xp==0 &  yp==0:
						xp,yp = x1,y1

					if drawColor == (0,0,0):
						cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
						cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
					else:
						cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
						cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
						# print(drawColor)	
					

					xp,yp = x1,y1


			imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)		
			_,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
			# cv2.imshow('a',imgInv)

			imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
			# cv2.imshow('b',imgInv)
				
			img = cv2.bitwise_and(img,imgInv)
			# cv2.imshow('bitwise_and',img)
			img = cv2.bitwise_or(img,imgCanvas)
			# cv2.imshow('bitwise_or',img)



			img[0:98,0:1109] = header
			#img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)


			cv2.imshow('Image',img)
			# cv2.imshow('Images',imgCanvas)
			if cv2.waitKey(1)==ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()		

	except Exception as e:
		pymsgbox.alert(e)		