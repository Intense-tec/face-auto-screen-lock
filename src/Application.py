import cv2
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from FaceRecognition import FaceRecognition


class Application(tk.Tk):
    def __init__(self, title):
        tk.Tk.__init__(self)
        self.vid = None
        self.photo = None
        self.canvas = None
        self.title(title)
        self.geometry("900x600")
        self.configure(bg='#e6f3fc')
        self.minsize(900, 600)
        self.maxsize(900, 600)
        self.add_button("Cancel", "app_quit", 780, 550, 100)
        self.add_button("Save", "", 670, 550, 100)
        self.add_button("About", "about", 10, 550, 100)
        self.face_recognition = FaceRecognition()

    def add_button(self, label, btn_type, x, y, width):
        command = None
        match btn_type:
            case 'app_quit':
                command = self.quit
            case 'about':
                command = self.about_window

        button_font = font.Font(family='Helvetica', weight='bold')
        btn = tk.Button(self, text=label, command=command, bg="#92c3d1", fg="#f0f0f0", font=button_font)
        btn.pack()
        btn.place(x=x, y=y, width=width)

    # Define function to show frame
    def show_frames(self):
        self.vid = cv2.VideoCapture(0)
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas()
        self.canvas.pack()
        self.canvas.config(width=600, height=400)
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.face_recognition.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.after(1, self.update)

    def about_window(self):
        about_window = tk.Toplevel(self)
        about_window.title("About")
        about_window.geometry("200x200")

if __name__ == "__main__":
    app = Application("Face auto screen lock")
    app.show_frames()
    app.mainloop()
