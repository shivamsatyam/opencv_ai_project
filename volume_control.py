def volume(url,width,height):
	print(f"{url} {width} {height}")

	try:
		import cv2
		import mediapipe as mp
		import time
		import hand_detector as htm
		import math
		from ctypes import cast,POINTER
		from comtypes import CLSCTX_ALL
		from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
		from numpy import interp
		import pymsgbox

		pymsgbox.alert("press q to quit the window")

		wCam,hCam = 800,600

		if url:
			capture = cv2.VideoCapture(url)

		else:
			capture = cv2.VideoCapture(0)
		# capture.set(3,wCam)
		# capture.set(4,hCam)

		pTime = 0

		detector = htm.handDetector(detectionCon=0.7)


		devices = AudioUtilities.GetSpeakers()
		interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
		volume = cast(interface,POINTER(IAudioEndpointVolume))
		#volume.GetMute()
		#volume.GetMasterVolumeLevel()
		#print(volume.GetVolumeRange()) #(-65.25, 0.0, 0.03125)

		volRange = volume.GetVolumeRange()
		#volume.SetMasterVolumeLevel(0,None)
		minVol = volRange[0]
		maxVol = volRange[1]

		vol = 0
		volBar = 400
		volPer = 0

		while True:
			success,img = capture.read()
			img = cv2.resize(img,(int(width),int(height)),interpolation=cv2.INTER_AREA)	

			img = detector.findHands(img)

			lmList = detector.findPosition(img,draw=False)
			
			if len(lmList)!=0:

				x1,y1 = lmList[4][1],lmList[4][2]
				x2,y2 = lmList[8][1],lmList[8][2]
				cx,cy = (x1+x2)//2 , (y1+y2)//2

				cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
				cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)

				cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
				cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

				length = math.hypot(x2-x1,y2-y1)


				# print(length)

				# Hand Range 50-300
				# volume Range -65 - 0

				vol = interp(length,[50,250],[minVol,maxVol])
				volBar = interp(length,[50,250],[400,150])
				volPer = interp(length,[50,250],[0,100])

				volume.SetMasterVolumeLevel(vol,None)
				if length<50:
					print('circle')
					cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)


			cv2.rectangle(img,(50,150),(85,400),(0,0,255))		
			cv2.rectangle(img,(50,int(volBar)),(85,400),(0,0,255),cv2.FILLED)		
			cv2.putText(img,f"{int(volPer)}%",(40,450),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),3)

			cTime = time.time()		
			fps = 1/(cTime-pTime)
			pTime = cTime


			cv2.putText(img,f"{int(fps)}",(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)


			cv2.imshow('image',img)		

			if cv2.waitKey(1)== ord('q'):
				break

		capture.release()
		cv2.destroyAllWindows()		

	except Exception as e:
		pymsgbox.alert(e)	