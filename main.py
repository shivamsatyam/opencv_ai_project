from tkinter import *
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import face_detector 
import cv2 as cv
import os
import hand_detector
import pymsgbox
import volume_control
import virtual_painter_module 
from mouse_controller import mouse_control

HandDetector = hand_detector.handDetector()

class ImageClassifier(Tk):
	def __init__(self):
		super().__init__()
		self.geometry("800x400")
		# self.title = "Shivam image classsifier"
		self.Notebook = ttk.Notebook(self)
		self.Notebook.pack(expand=1,fill="both")
		self.imgfileTypes = [('All_Files','*.*'),("png",".png"),("jpg",".jpg"),("jpeg",".jpeg"),("bmp",".bmp")]
		self.videofileTypes = [('All_Files','*.*'),("mp4",".mp4"),("vlc",".vlc"),("mp3",".mp3"),("bmp",".bmp")]
		self.color = (0,255,0)
		self.width = IntVar()
		self.height = IntVar()
		

	def run(self):
		self.mainloop()	
	

	def color_chooser_function(self):	
	    color_var = colorchooser.askcolor()
	    print(color_var)
	    self.color = color_var[0]
	    return color_var[0]

	def create_colorChooser(self,frame,x,y):
		#font_color_icon = PhotoImage(file='image/font_color.png')
		font_color_btn = ttk.Button(frame,command=self.color_chooser_function)
		font_color_btn.place(x=x,y=y)

 

	def face_detection_function(self):
		self.face_Detection_Frame_file = filedialog.askopenfilename(defaultextension=".txt",filetypes=self.imgfileTypes)	
		print(self.face_Detection_Frame_file)			
		
		if self.face_Detection_Frame_file!=None:	
			face_detector.detect_faces(self.face_Detection_Frame_file,color=self.color)


	def create_combobox(self,frame,text_var,x,y):		
		
		box = ttk.Combobox(frame, width=12, textvariable = text_var, state='readonly')
		box['values'] = tuple(range(200,1200,40))
		box.current(8)
		box.place(x=x,y=y)
 

	def face_detection_live(self):
		newwidget = Toplevel()	
		newwidget.title("title")
		newwidget.geometry("300x400")	
		face_webcam_url = StringVar('')
		face_webcam_url.set('')
		Label(newwidget,text="Enter the video url",font="sans-serif 20 bold").place(x=25,y=10)
		face_detection_webcam_url = Entry(newwidget,textvariable=face_webcam_url,font=('system-ui',10,'normal'))
		face_detection_webcam_url.place(x=79,y=60)

		def start_live_face_detector(event=None):
			url = face_webcam_url.get()
			print(self.width.get(),self.height.get())
			face_detector.detect_webcam_faces(color=self.color,url=url,width=self.width.get(),height=self.height.get())			


		self.create_combobox(newwidget,self.width,50,120)
		Label(newwidget,text="X",font="algerian 20 bold").place(x=165,y=120)	
		self.create_combobox(newwidget,self.height,200,120)	

		button = Button(newwidget,text="Start",bg="deepskyblue",fg="white",command=start_live_face_detector)	
		button.place(x=130,y=150)

		newwidget.mainloop()


	def create_Face_Detection_Frame(self):
		self.face_Detection_Frame = Frame(self.Notebook,bg="black")
		self.face_Detection_Frame_button = Button(self.face_Detection_Frame,text="Load image",bg="green",fg="white",command=self.face_detection_function)		
		self.face_Detection_Frame_button.place(x=0,y=30)

		self.create_colorChooser(self.face_Detection_Frame,100,30)

		self.face_Detection_Frame_live = Button(self.face_Detection_Frame,text="Live ",bg="green",fg="white",command=self.face_detection_live)		
		self.face_Detection_Frame_live.place(x=180,y=30)

		self.Notebook.add(self.face_Detection_Frame,text="face recognition")


	def create_hand_detection(self,frame):
		hand_detection_width = IntVar(0)	
		hand_detection_height = IntVar(0)	
		hand_detection_url = StringVar('')	

		lis = [hand_detection_width,hand_detection_height]
		text = ["width","height"]

		Label(frame,text="Enter the video url !optional",bg="black",fg="white",font="sans-serif 20 bold").pack()	
		Entry(frame,textvariable=hand_detection_url).pack()

		for i in range(2):
			Label(frame,text=text[i],bg="black",fg="white",font="sans-serif 20 bold").pack()	
			box = ttk.Combobox(frame, width=12, textvariable = lis[i], state='readonly')
			box['values'] = tuple(range(200,1200,40))
			box.current(8)
			box.pack()

		
		print("ff")	
		def start_live_hand_detector(event=None):
			try:
				url,width,height = hand_detection_url.get(),hand_detection_width.get(),hand_detection_height.get()
				if url!='' or url !=None:
					capture = cv.VideoCapture(url)	
				else:	
					capture = cv.VideoCapture(0)	

				while True:
					success,img = capture.read()

					if success:
						img = cv.resize(img,(width,height),interpolation=cv.INTER_AREA)
						img = HandDetector.findHands(img)
						cv.imshow('img',img)
						if cv.waitKey(1)==ord('d'):
							break

				capture.release()			
				cv.destroyAllWindows()
			except Exception as e:
				pymsgbox.alert(e)	

		Button(frame,text="start",bg="green",fg="white",font="sans-serif 15 bold",command=start_live_hand_detector).pack()
	    
	  


	def hand_detection_frame(self):	
		self.hand_detection_frame = Frame(self.Notebook,bg="black")
		self.create_hand_detection(self.hand_detection_frame)
		self.Notebook.add(self.hand_detection_frame,text="hand detection")


	def create_volume_project(self,frame):
		video_project_width = IntVar(0)	
		video_project_height = IntVar(0)	
		video_project_url = StringVar('')	

		lis = [video_project_width,video_project_height]
		text = ["width","height"]

		def start_video_project(event=None):
			url,width,height = video_project_url.get(),video_project_width.get(),video_project_height.get()
			volume_control.volume(url,width,height)	
	
		Label(frame,text="Enter the video url",font="sans-serif 20 bold").pack()
		Entry(frame,textvariable=video_project_url).pack()
	

		for i in range(2):
			Label(frame,text=text[i],bg="black",fg="white",font="sans-serif 20 bold").pack()	
			box = ttk.Combobox(frame, width=12, textvariable = lis[i], state='readonly')
			box['values'] = tuple(range(200,1200,40))
			box.current(8)
			box.pack()
	
		Button(frame,text="start",bg="green",fg="white",font="sans-serif 15 bold",command=start_video_project).pack()
	    
			

	def volume_project(self):
		self.volume_project_frame  = Frame(self.Notebook,bg="black")
		self.create_volume_project(self.volume_project_frame)
		self.Notebook.add(self.volume_project_frame,text="volume project")


	def create_virtual_painter(self,frame):
		virtual_painter_width = IntVar(0)	
		virtual_painter_height = IntVar(0)	
		virtual_painter_url = StringVar('')	

		lis = [virtual_painter_width,virtual_painter_height]
		text = ["width","height"]

		def start_virtual_painter(event=None):
			url =  virtual_painter_url.get()
			virtual_painter_module.virtual_painter(url)
			
		Label(frame,text="Enter the video url",font="sans-serif 20 bold").pack()
		Entry(frame,textvariable=virtual_painter_url).pack()
	

	
		Button(frame,text="start",bg="green",fg="white",font="sans-serif 15 bold",command=start_virtual_painter).pack()
	    
				


	def virtual_painter(self):
		self.virtual_painter_frame  = Frame(self.Notebook,bg="black")	

		self.create_virtual_painter(self.virtual_painter_frame)

		self.Notebook.add(self.virtual_painter_frame,text="virtual painter")


	def create_mouse_controler(self,frame):
		mouse_width = IntVar()	
		mouse_height = IntVar()	
		mouse_url = StringVar('')	

		lis = [mouse_width,mouse_height]
		text = ["width","height"]

		def start_mouse(event=None):
			url =  mouse_url.get()
			print("start mouse")
			# virtual_painter_module.virtual_painter(url)
			mouse_control(url,self.winfo_screenwidth(),self.winfo_screenheight(),mouse_width.get(),mouse_height.get())	

		Label(frame,text="Enter the video url",font="sans-serif 20 bold").pack()	
		Entry(frame,textvariable=mouse_url).pack()
	
		for i in range(2):
			Label(frame,text=text[i],bg="black",fg="white",font="sans-serif 20 bold").pack()	
			box = ttk.Combobox(frame, width=12, textvariable = lis[i], state='readonly')
			box['values'] = tuple(range(500,1900,200))
			box.current(2)
			box.pack()
	
	
		Button(frame,text="start",bg="green",fg="white",font="sans-serif 15 bold",command=start_mouse).pack()
	   	


	def mouse(self):
		self.mouse  = Frame(self.Notebook,bg="black")	

		self.create_mouse_controler(self.mouse)

		self.Notebook.add(self.mouse,text="mouse controller")





window = ImageClassifier()
window.create_Face_Detection_Frame()
window.hand_detection_frame()
window.volume_project()
window.virtual_painter()
window.mouse()

window.run()









































