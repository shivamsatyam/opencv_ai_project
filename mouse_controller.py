def mouse_control(url,monitorWidth,monitorHeight,width,height):
	print(f"{url} {monitorWidth} {monitorHeight} {width} {height} ")

	try:
		import cv2 as cv
		import hand_detector as htm
		from numpy import interp
		import pymsgbox
		# from win32api import GetSystemMetrics
		from  autopy import mouse

		pymsgbox.alert('press q to quit')
		# monitorWidth =GetSystemMetrics(0)
		# monitorHeight = GetSystemMetrics(1)

		detector = htm.handDetector(detectionCon=0.85)


		if url:
			capture =cv.VideoCapture(url)
		else:
	
			capture =cv.VideoCapture(0)

		# width,height = 1200,800
		detectorWidth = width-200
		detectorHeight = height-200

		while True:
			success,img = capture.read()
			if success:
				# cv.rectangle(img,(0,400),(0,400),(255,0,255),cv.FILLED)
				img = cv.flip(img,1)
				img = cv.resize(img,(width,height),interpolation=cv.INTER_AREA)
				img = detector.findHands(img)
				lmList = detector.findPosition(img,draw=False)
				
				if len(lmList)!=0:
					# print(lmList)
					x1,y1 = lmList[8][1:]
					# print(f"{lmList[8][1:]}  {lmList[12][1:]}")

					fingers = detector.fingersUp()	
					print(fingers)	
					moveWidth = int(interp(x1,[200,detectorWidth],[0,monitorWidth]))
					moveHeight = int(interp(y1,[200,detectorHeight],[0,monitorHeight]))

					count = fingers.count(1)
					# print(f"\n\n\n\n count {count} \n\n\n\n\n\n")
					if fingers[1]==1 and count==1:

						# print(f"{moveWidth} {moveHeight}")
						try:	
							mouse.move(moveWidth,moveHeight)
						except Exception as e:
							pass	
						print("moving mode")	


					if fingers[1]==1 and fingers[2]==1 and count==2:
						try:	
							mouse.move(moveWidth,moveHeight)
							print("click mode")
							mouse.click()	
						except Exception as e:
							pass	
						print("click mode")	

				cv.imshow('aa',img)

			if cv.waitKey(1)==ord('q'):
				break	

		capture.release()
		cv.destroyAllWindows()


	except Exception as e:
		pymsgbox.alert(e)	