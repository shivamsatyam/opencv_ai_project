import cv2 as cv
import pymsgbox


def detect_faces(img,Factor=1.1,Neighbors=1,thickness=2,color =(0,255,0) ):	
	filename = img
	img = cv.imread(img)

	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	haar_cascade = cv.CascadeClassifier('files/har_face.xml')
	faces_rect = haar_cascade.detectMultiScale(img,scaleFactor=Factor,minNeighbors=Neighbors)

	for (x,y,w,h) in faces_rect:
		cv.rectangle(img,(x,y),(x+w,y+h),color,thickness=thickness)	
	cv.imshow(filename,img)
	cv.waitKey(0)	


def detect_webcam_faces(Factor=1.1,Neighbors=3,thickness=2,color =(0,255,0),url='',width=None,height=None):
	print(width,height)
	try:



		if url!='' or url !=None:
			capture = cv.VideoCapture(url)
		else:
			capture = cv.VideoCapture(0)
		
		# capture = cv.VideoCapture('https://10.173.90.239:8080/video')

		haar_cascade = cv.CascadeClassifier('files/har_face.xml')
		
		pymsgbox.alert("press q to quit the window")

		while True:
			success,img = capture.read()
			if width and height!=None:
				height,width = img.shape[1:]

			if success:		
				# filename = img
				# img = cv.imread(img)
				img = cv.resize(img,(800,600),interpolation=cv.INTER_AREA)
				gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
				faces_rect = haar_cascade.detectMultiScale(img,scaleFactor=Factor,minNeighbors=Neighbors)

				for (x,y,w,h) in faces_rect:
					cv.rectangle(img,(x,y),(x+w,y+h),color,thickness=thickness)	
				cv.imshow("image",img)
		
			# if cv.getWindowProperty('frame',cv.WND_PROP_VISIBLE)<1:
			# 	break	

			print(cv.getWindowProperty('frame',cv.WND_PROP_VISIBLE))

			
			if cv.waitKey(1)==ord('q'):
				break
	


		capture.release()
		cv.destroyAllWindows()	
	except Exception as e:
	
		pymsgbox.alert(e)

					