# Library Import
from tkinter import *
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
# Main window creation
root = Tk()
cap = None
# Screen size
W = root.winfo_screenwidth()
H = root.winfo_screenheight()
# Container size screen1, screen2
wscreen1 = W*0.30
hscreen1 = H*0.7
wscreen2 = W*0.8
hscreen2 = H*0.8
wvideo = int(wscreen2*0.267)
hvideo = int(hscreen2*0.447)
positionvideoX = (W-wscreen2)/2+(wscreen2/2-wscreen2*0.3)/2
positionvideoY = (H-hscreen2)/2+(hscreen2-hscreen2*0.5)/2
# Logo size, screen1, screen2
percentageIconScreen1 = 50
percentageIconScreen2 = 40
logoscreen1 = cv2.imread('./img/logo.png', cv2.IMREAD_UNCHANGED)
logoscreen2 = logoscreen1.copy()
logoscreen1 = cv2.resize(
    logoscreen1, 
    (int(logoscreen1.shape[1] * percentageIconScreen1 / 100), 
    int(logoscreen1.shape[0] * percentageIconScreen1 / 100)))
logoscreen2 = cv2.resize(
    logoscreen2, 
    (int(logoscreen2.shape[1] * percentageIconScreen2 / 100), 
    int(logoscreen2.shape[0] * percentageIconScreen2 / 100)))
cv2.imwrite('./img/logoR.png', logoscreen1)
cv2.imwrite('./img/logoR2.png', logoscreen2)
background = cv2.resize(cv2.imread('./img/Fondo.png', 1), (W, H))
cv2.imwrite('./img/FondoR.png', background)
imagenL  = PhotoImage(file="./img/FondoR.png")
logoscreen1 = PhotoImage(file="./img/logoR.png")
logoscreen2 = PhotoImage(file="./img/logoR2.png")
images = []

# Container opacity

def create_rectangle(x, y, a, b, hight, width, wscreen1, hscreen1, **options):
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', 
            (a-x, b-y), 
            fill)
        images.append(ImageTk.PhotoImage(image))
        canvasRectangleTransparect = canvas.create_image(
            width, 
            hight, 
            image=images[-1], 
            anchor='nw')
        canvasBordeRectangle = canvas.create_rectangle(
            width, 
            hight, 
            width+wscreen1, 
            hight+hscreen1, 
            **options)
        return canvasRectangleTransparect, canvasBordeRectangle

# Upload video

def visualizar():
    global cap, lbl, frame2
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(
                frame, 
                (wvideo, 
                hvideo))
            frame = cv2.cvtColor(
                frame, 
                cv2.COLOR_BGR2RGB)
            frame2 = cv2.cvtColor(
                frame, 
                cv2.COLOR_RGB2GRAY)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lbl = canvas.create_window(
                positionvideoX+20, 
                positionvideoY+17, 
                window=lblVideo, 
                anchor="nw")
            canvasScreen2.append(lbl)
            BrightnessContrast()
            lblVideo.after(25, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def BrightnessContrast(brightness=0):
    global frame2
    # position of the specified scale
    brightness = sclBrillo.get() + 255

    contrast = sclContraste.get() + 127

    effect = controller(frame2, brightness,
                        contrast)
    # The function imshow displays an image
    # in the specified window
    imGris = Image.fromarray(effect)
    imgGris = ImageTk.PhotoImage(image=imGris)
    lblVideoGris.configure(image=imgGris)
    lblVideoGris.image = imgGris
    lblGris = canvas.create_window(
                positionvideoX+wscreen2/2+21, 
                positionvideoY+17, 
                window=lblVideoGris, 
                anchor="nw")
    canvasScreen2.append(lblGris)

##Controller
def controller(img, brightness=255,
			contrast=127):
	brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
	contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
	if brightness != 0:
		if brightness > 0:
			shadow = brightness
			max = 255
		else:
			shadow = 0
			max = 255 + brightness
		al_pha = (max - shadow) / 255
		ga_mma = shadow
		# The function addWeighted calculates
		# the weighted sum of two arrays
		cal = cv2.addWeighted(img, al_pha,
							img, 0, ga_mma)
	else:
		cal = img
	if contrast != 0:
		Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
		Gamma = 127 * (1 - Alpha)
		cal = cv2.addWeighted(cal, Alpha,
							cal, 0, Gamma)
	# putText renders the specified text string in the image.
	cv2.putText(cal, 'B:{},C:{}'.format(brightness,
										contrast), (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
	return cal

def watchVideo():
    global cap
    video_path = filedialog.askopenfilename(filetypes=[
        ("all video format", ".mp4"),
        ("all video format", ".avi")
    ])
    if len(video_path) > 0:
        cap = cv2.VideoCapture(video_path)
        visualizar()
        sclBrillo.configure(
            orient=HORIZONTAL,
            from_=-255, 
            to=255, 
            length=int(wscreen2*0.295), 
            command=BrightnessContrast)
        sclContraste.configure(
            orient=HORIZONTAL,
            from_=-127, 
            to=127, 
            length=int(wscreen2*0.295), 
            command=BrightnessContrast)
        toggleBtn("disabled", "normal")
        lblBrightness = canvas.create_text(
            (W-wscreen2)/2+wscreen2/2-300, 
            positionvideoY+375, 
            text="BRIGHTNESS",
            anchor="n", 
            font="Times 22 italic bold")
        lblContrast = canvas.create_text(
            (W-wscreen2)/2+wscreen2/2-300, 
            positionvideoY+450, 
            text="CONTRAST",
            anchor="n", 
            font="Times 22 italic bold")
        sclBrillo2 = canvas.create_window(
                (W-wscreen2)/2+wscreen2/2, 
                positionvideoY+375, 
                window=sclBrillo, 
                anchor="n")
        sclContraste2 = canvas.create_window(
                (W-wscreen2)/2+wscreen2/2, 
                positionvideoY+450,
                window=sclContraste, 
                anchor="n")
        canvasScreen2.append(lblBrightness)
        canvasScreen2.append(lblContrast)
        canvasScreen2.append(sclBrillo2)
        canvasScreen2.append(sclContraste2)
        canvas.mainloop()
    else:
        print("No ha escogido un video")

def toggleBtn(stateBtnUpload, stateBtnClean):
    btnUpload = Button(
        root, 
        text="Upload Video", 
        font=50,
        state=stateBtnUpload, command=watchVideo)
    btnUpload = canvas.create_window(
                    (W-wscreen2)/2+wscreen2/2, 
                    (H-hscreen2)/2+300, 
                    anchor="n", 
                    window=btnUpload)
    btnClean = Button(
        root, 
        text="Clean", 
        font=50,
        state=stateBtnClean, 
        command=endVideo)
    btnClean = canvas.create_window(
                    (W-wscreen2)/2+wscreen2/2, 
                    (H-hscreen2)/2+380,
                    anchor="n", 
                    window=btnClean)

def endVideo():
    cap.release()
    for i in range(len(canvasScreen2)):
        canvas.delete(canvasScreen2[i])
    toggleBtn("normal", "disabled")

def nextScreen():
    for i in range(len(canvasScreen1)):
        canvas.delete(canvasScreen1[i])
    newCanvas()

def newCanvas():
    create_rectangle(
        0, 
        0, 
        int(wscreen2), 
        int(hscreen2), 
        (H-hscreen2)/2, 
        (W-wscreen2)/2, 
        wscreen2, 
        hscreen2, 
        fill='white', 
        alpha=0.75)
    canvas.create_text(
        (W-wscreen2)/2+wscreen2/4, 
        (H-hscreen2)/2+80, 
        text="ORIGINAL VIDEO",
        anchor="n", 
        font="Times 22 italic bold")
    canvas.create_text(
        (W-wscreen2)/2+wscreen2/4+wscreen2/2, 
        (H-hscreen2)/2+80,
        text="WORKED VIDEO", 
        anchor="n", 
        font="Times 22 italic bold")
    image = cv2.imread('./img/vacio.png', cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (int(wscreen2*0.3), int(hscreen2*0.5)))
    cv2.imwrite('./img/vacio.png', image)
    imagen = PhotoImage(file='./img/vacio.png')
    global imagenOriginal, imagenTrabajada, btnClean, btnUpload
    imagenOriginal = canvas.create_image(
        positionvideoX, 
        positionvideoY, 
        image=imagen, 
        anchor="nw")
    imagenTrabajada = canvas.create_image(
        positionvideoX+wscreen2/2, 
        positionvideoY, 
        image=imagen, 
        anchor="nw")
    canvas.create_image((W-wscreen2)/2+wscreen2/2, 
    (H-hscreen2)/8, 
    image=logoscreen2, 
    anchor="n")
    toggleBtn("normal","disabled")
    canvas.mainloop()
# Canvas creation
canvas = Canvas(root, width=W, height=H)
canvas.create_image(
    0, 
    0, 
    image=imagenL, 
    anchor="nw")
canvas.pack()
canvasRectangleTransparect, canvasBordeRectangle = create_rectangle(
    0, 
    0, 
    int(wscreen1), 
    int(hscreen1), 
    (H-hscreen1)/2, 
    (W-wscreen1)/2, 
    wscreen1, 
    hscreen1, 
    fill='white', 
    alpha=0.75)
# Labels screen1
labelsList = [
                "UNIVERSIDAD DEL AZUAY", 
                "ELECTRONIC ENGINEERING", 
                "DIGITAL SIGNAL PROCESSING", 
                "CARLOS MENDEZ", 
                "FILTER STUDY"
            ]
canvasLabelsList = []
canvasScreen1 = []
canvasScreen2 = []
for count, value in enumerate(labelsList):
    canvasLabelsList.append(
        canvas.create_text(
            (W-wscreen1)/2+wscreen1/2, 
            (H-hscreen1)/2+count*80 + 80, 
            text=value, anchor="n", 
            font="Times 22 italic bold"))
# Canvas widgets
canvasLogoScreen1 = canvas.create_image(
    (W-wscreen1)/2+wscreen1/2, 
    (H-hscreen1)/8, 
    image=logoscreen1, 
    anchor="n")
btnGoProject = Button(
    canvas, 
    text="Go to Project", 
    font=30, 
    command=nextScreen)
btnGoProject = canvas.create_window(
    (W-wscreen1)/2+wscreen1/2, 
    (H-hscreen1)/2+480, 
    anchor="n", 
    window=btnGoProject)
canvasScreen1.extend([
    canvasBordeRectangle, 
    canvasRectangleTransparect, 
    btnGoProject, 
    canvasLogoScreen1])
canvasScreen1.extend(canvasLabelsList)
lblVideo = Label(canvas)
lblVideoGris = Label(canvas)
sclBrillo = Scale(canvas)
sclContraste = Scale(canvas)
# Main window settings
root.resizable(width=False, height=False)
root.title("FILTER STUDY")
root.mainloop()