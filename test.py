from tkinter import *
from PIL import Image

root = Tk()
root.geometry("800x550")
root.config(background='#108cff')

gifImage = "loading.gif"
openImage = Image.open(gifImage)
frames = openImage.n_frames
imageObject = [PhotoImage(file=gifImage, format=f"gif -index {i}") for i in range(frames)]
count = 0
showAnimation = None

def animation(count):
    global showAnimation
    newImage = imageObject[count]

    gif_Label.configure(image=newImage)
    count += 1
    if count == frames:
        count = 0
    
    showAnimation = root.after(50, lambda: animation(count))

gif_Label = Label(root, image="")
gif_Label. place(x=155, y=20, width=450, height=500)

animation(count)

root.mainloop()