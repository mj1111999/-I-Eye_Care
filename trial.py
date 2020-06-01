import cv2
import numpy as np
import dlib
from math import hypot
import time
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from playsound import playsound
import webbrowser
import ffmpeg
import win32api
root = Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=1)
root.title('I(Eye) Care')
frame.config(background='light blue')
label = Label(frame, text="I(Eye) Care", bg='light blue', font='Times 35 bold')
label.pack(side=TOP)
filename = PhotoImage(file="demo.png")
background_label = Label(frame, image=filename)
background_label.pack(side=TOP)


def hel():
    help(cv2)


def Contri():
    messagebox.showinfo("Contributors",
                        "\n1.Siddharth Thorat\n2. Mohit Jain  \n3. Harshit Srivastav \n4. Girik Tripathi \n5. Ayush Sharma")


def Materials():
    messagebox.showinfo("About", 'Eye care version v1.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3.6')


menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools", menu=subm1)
subm1.add_command(label="Open CV Docs", command=hel)

subm2 = Menu(menu)
menu.add_cascade(label="About", menu=subm2)
subm2.add_command(label="Eye Care", command=Materials)
subm2.add_command(label="Contributors", command=Contri)
def videotype():
    def click_me():
        if i.get()==1:
            capture = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'MPEG-4')
            op = cv2.VideoWriter('BLINK.mp4', fourcc, 11.0, (640, 480))
            while True:
                ret, frame = capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('frame', frame)
                op.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            capture = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            op = cv2.VideoWriter('Sample1.avi', fourcc, 11.0, (640, 480))
            while True:
                ret, frame = capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('frame', frame)
                op.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            op.release()
            capture.release()
    shoot=Tk()
    i=IntVar()
    shoot.geometry("300x300+120+120")
    shoot.title("Video type")
    mp4=Radiobutton(shoot,text="Capture video using .mp4 as extension",value=1,variable=i)
    avi = Radiobutton(shoot, text="Capture video using .avi as extension",value=2,variable=i)
    mp4.pack()
    avi.pack()
    selectbutton=Button(shoot,text="Select",command=click_me)
    selectbutton.pack()
    shoot.mainloop()

def tips():
    root=Tk()
    text = Text(root)
    text.insert(INSERT,"Eye Care Tips",)
    text.insert(INSERT,"\nThere are things you can do to help keep your eyes healthy and make sure you are seeing your best:")
    text.insert(END, "\nEat a healthy, balanced diet."
                      "\nMaintain a healthy weight. "
                      "\nGet regular exercise."
                      "\nWear sunglasses."
                      "\nWear protective eye wear."
                      "\nAvoid smoking."
                      "\nKnow your family medical history."
                      "\nKnow your other risk factors."
                      "\nIf you wear contacts, take steps to prevent eye infections."
                      "\nGive your eyes a rest.")
    text.pack()
    def showinfo():
        try:
            Browser =webbrowser.open('https://medlineplus.gov/eyecare.html')
            messagebox.showinfo("Information", "For more information visit our website at" + Browser)
        except:
            messagebox.showinfo("Information","Redirecting to the browser...")


    infobutton=Button(root,text="More Information",command=showinfo)
    infobutton.pack()




def browse_file():
    file = filedialog.askopenfilename(initialdir="/", title=" Select A File",
                                      filetypes=(("mp4 files", ".mp4"), ("all files", "*.*")))
    return file
def quit():
    quit=messagebox.askyesno("I(Eye) Care","Are you Sure you want to quit?")
    if quit>0:
        root.destroy()

def detectblinkcounts():
    c1 = 0
    c2 = 0
    total_blink = 0
    count = 0
    consecutive_frames = 3
    consec_frame = 0
    counter = 0
    temp = 0
    cap = cv2.VideoCapture(0)
    # cap2 = cv2.VideoCapture("blinking_person.mp4")

    # fps = cap.get(cv2.CAP_PROP_FPS)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    font = cv2.FONT_HERSHEY_PLAIN

    def midpoint(p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

        ratio = ver_line_lenght / hor_line_lenght
        return ratio

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # print("fps = " + str(fps))

        faces = detector(gray)

        for face in faces:

            counter = counter + 1
            print(counter)

            landmarks = predictor(gray, face)

            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

            cv2.putText(frame, "Ratio = " + str(blinking_ratio), (350, 50), font, 2, (0, 0, 255))

            if blinking_ratio < 0.2:
                c1 = 1
                consec_frame = consec_frame + 1

            elif blinking_ratio > 0.3:
                c2 = 1
                consec_frame = consec_frame + 1

                if consec_frame >= consecutive_frames:
                    if c1 == 1 and c2 == 1:
                        total_blink = total_blink + 1
                        c1 = 0
                        c2 = 0
                        consec_frame = 0
                        count = total_blink

            if counter % 1000 == 0:
                if count <= 20:

                    playsound("beep-07.wav")
                    win32api.MessageBox(0, '  PLease BLINK \n Your current blink rate is only ' + str(
                        count) + ' per minute. \n You need to atleast blink 20 times \n per minute', 'Blink Helper',
                                        0x00000030 | 0x00001000)
                    total_blink = 0

                    temp = temp + 1
                    if temp % 3 == 0:
                        counter = 0
                        temp = 0

        cv2.putText(frame, "Blinks = " + str(total_blink), (50, 50), font, 2, (0, 0, 255))

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def detectblinkcounts1():
        address = browse_file()
        c1 = 0
        c2 = 0
        total_blink = 0
        count = 0
        consecutive_frames = 3
        consec_frame = 0
        counter = 0
        temp = 0
        # cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(address)

        # fps = cap.get(cv2.CAP_PROP_FPS)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        font = cv2.FONT_HERSHEY_PLAIN

        def midpoint(p1, p2):
            return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

        def get_blinking_ratio(eye_points, facial_landmarks):
            left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
            right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
            center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
            center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

            hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
            ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

            hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
            ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

            ratio = ver_line_lenght / hor_line_lenght
            return ratio

        while True:
            _, frame = cap2.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # print("fps = " + str(fps))

            faces = detector(gray)

            for face in faces:

                counter = counter + 1
                # print(counter)

                landmarks = predictor(gray, face)

                left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

                cv2.putText(frame, "Ratio = " + str(blinking_ratio), (350, 50), font, 2, (0, 0, 255))

                if blinking_ratio < 0.2:
                    c1 = 1
                    consec_frame = consec_frame + 1

                elif blinking_ratio > 0.3:
                    c2 = 1
                    consec_frame = consec_frame + 1

                    if consec_frame >= consecutive_frames:
                        if c1 == 1 and c2 == 1:
                            total_blink = total_blink + 1
                            c1 = 0
                            c2 = 0
                            consec_frame = 0
                            count = total_blink

                if counter % 1500 == 0:
                    if count <= 20:

                        playsound("beep-07.wav")
                        win32api.MessageBox(0, '  PLease BLINK \n Your current blink rate is only ' + str(
                            count) + ' per minute. \n You need to atleast blink 20 times \n per minute', 'Blink Helper',
                                            0x00000030 | 0x00001000)

                        total_blink = 0

                        temp = temp + 1
                        if temp % 3 == 0:
                            counter = 0
                            temp = 0

            cv2.putText(frame, "Blinks = " + str(total_blink), (50, 50), font, 2, (0, 0, 255))

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

        cap2.release()
        cv2.destroyAllWindows()






livevideo= Button(frame, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=detectblinkcounts,
              text='Open Camera to detect the blinks', font='helvetica 15 bold')
livevideo.place(x=5, y=104)
prerecordedvideo = Button(frame, padx=5, pady=5, width=39, bg='white', fg='black', relief=GROOVE, command=detectblinkcounts1,text='Detect blinks in pre recorded videos', font='helvetica 15 bold')
prerecordedvideo.place(x=5,y=176)
video_type=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=videotype,text='Open Camera to record Video',font=('helvetica 15 bold'))
video_type.place(x=5,y=250)
but4=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=tips,text='Tips',font=('helvetica 15 bold'))
but4.place(x=5,y=322)
exitbutton=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,command=quit,text='Exit',font=('helvetica 15 bold'))
exitbutton.place(x=210,y=478)
root.mainloop()
