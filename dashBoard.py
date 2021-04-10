from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from time import strftime
from datetime import datetime
import mysql.connector
import os
import numpy as np
import cv2
from student import Student
from attendance import Attendance

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1199x600+100+50")
        self.root.title("St. Vincent Pallotti College of Engineering & Technology")
        self.root.resizable(False, False)

        # =====header image=====
        self.bg=ImageTk.PhotoImage(file="images/college_bg.jpg")
        self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        # =====buttons====
        Attendance_btn = Button(self.root, command=self.attendance, cursor="hand2", text="Take Attendance", fg="white", bg="#3ebca0", font=("Rockwell", 15)).place(x=210, y=340, width=180, height=40)
        Register_btn = Button(self.root, command=self.personal_details, cursor="hand2", text="Registration", fg="white", bg="#3ebca0", font=("Rockwell", 15)).place(x=500, y=340, width=180, height=40)
        Train_btn = Button(self.root, command=self.train_classifer, cursor="hand2", text="Train Image", fg="white", bg="#3ebca0", font=("Rockwell", 15)).place(x=815, y=340, width=180, height=40)
        Detection_btn = Button(self.root, command=self.face_detection, cursor="hand2", text="Face Detection", fg="white", bg="#3ebca0", font=("Rockwell", 15)).place(x=355, y=515, width=180, height=40)
        CheckAttendance_btn = Button(self.root, command=self.Attendance_data, cursor="hand2", text="Check Attendance", fg="white", bg="#3ebca0", font=("Rockwell", 15)).place(x=675, y=515, width=185, height=40)


    # ===Functions buttons=====



    def personal_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)


    def Attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)


    # =====Method to train custom classifier to recognize face=====
    def train_classifer(self):
        # =====Read all the images in custom data-set=====
        data_dir = ("data")
        path = [os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        # =====Store images in a numpy format and ids of the user on the same index in imageNp and id lists=====
        for image in path:
            # =====Gray Scale Image=====
            img = Image.open(image).convert('L')

            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13

        ids = np.array(ids)

        # =====Train and save classifier=====
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.yml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Info", "Training images completed")


    # =====mark attendance=====
    def mark_attendance(self, i, c, n, d):
        with open("Attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (c not in name_list) and (n not in name_list) and (d not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{c},{n},{d},{dtString},{d1}, Present")



    # =====real time attendance=====
    def attendance(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            # =====Converting image to gray-scale=====
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # =====detecting features in gray-scale image, returns coordinates, width and height of features=====
            features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)

            coord = []

            # =====drawing rectangle around the feature and labeling it=====
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                # =====Predicting the id of the user=====
                id, predict= clf.predict(gray_img[y:y + h, x:x + w])
                confidence = int((100*(1-predict/300)))

                conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                my_cursor = conn.cursor()


                my_cursor.execute("select userID from student where userID="+str(id))
                i = my_cursor.fetchone()
                i = "+".join(i)

                my_cursor.execute("select collegeUID from student where userID=" + str(id))
                c = my_cursor.fetchone()
                c = "+".join(c)

                my_cursor.execute("select name from student where userID="+str(id))
                n = my_cursor.fetchone()
                n = "+".join(n)

                my_cursor.execute("select dep from student where userID="+str(id))
                d = my_cursor.fetchone()
                d = "+".join(d)



                if confidence > 77:
                    cv2.putText(img, f"ID:{i}", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    cv2.putText(img, f"{c}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    cv2.putText(img, f"{n}", (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    self.mark_attendance(i, c, n, d)

                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown Face", (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    coord = [x, y, w, h]

            return coord


        # =====Method to recognize the person=====
        def recognize(img, clf, faceCascade):
            color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
            coord = draw_boundary(img, faceCascade, 1.1, 10, color["white"], "Face", clf)
            return img

        # =====Loading classifier=====
        faceCascade = cv2.CascadeClassifier('haarcascade_files/haarcascade_frontalface_default.xml')

        # =====Loading custom classifier to recognize=====
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.yml")

        # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        # url = 'http://192.168.0.182:8080/shot.jpg'

        # =====Remove this code if using external camera=====
        video_capture = cv2.VideoCapture(0)

        while True:
            # Reading image from video stream
            # img_resp = requests.get(url)
            # imgNp = np.array(bytearray(img_resp.content), dtype=np.uint8)
            # img = cv2.imdecode(imgNp, -1)
            # cv2.imshow('Android Cam', img)

            # Remove this code if using external camera
            _, img = video_capture.read()

            # =====Call method we defined above=====
            img = recognize(img, clf, faceCascade)
            # =====Writing processed image in a new window=====
            cv2.imshow("Attendance", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # =====Destroying output window=====
        cv2.destroyAllWindows()

    # =====face detection=====
    def face_detection(self):
        # Method to draw boundary around the detected feature
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
            # Converting image to gray-scale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # detecting features in gray-scale image, returns coordinates, width and height of features
            features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
            coords = []
            # drawing rectangle around the feature and labeling it
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                coords = [x, y, w, h]
            return coords

        # Method to detect the features
        def detect(img, faceCascade, eyeCascade, noseCascade, mouthCascade):
            color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
            coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")

            # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
            if len(coords) == 4:
                # Updating region of interest by cropping image
                roi_img = img[coords[1]:coords[1] + coords[3], coords[0]:coords[0] + coords[2]]
                # Passing roi, classifier, scaling factor, Minimum neighbours, color, label text
                coords = draw_boundary(roi_img, eyeCascade, 1.1, 12, color['red'], "Eye")
                coords = draw_boundary(roi_img, noseCascade, 1.1, 4, color['green'], "Nose")
                coords = draw_boundary(roi_img, mouthCascade, 1.1, 20, color['white'], "Mouth")
            return img

        # Loading classifiers
        faceCascade = cv2.CascadeClassifier('haarcascade_files/haarcascade_frontalface_default.xml')
        eyesCascade = cv2.CascadeClassifier('haarcascade_files/haarcascade_eye.xml')
        noseCascade = cv2.CascadeClassifier('haarcascade_files/Nariz.xml')
        mouthCascade = cv2.CascadeClassifier('haarcascade_files/Mouth.xml')

        # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE

        # url = "http://192.168.0.182:8080/shot.jpg"
        # Remove this code if using external camera
        video_capture = cv2.VideoCapture(0)

        while True:
            # Reading image from video stream
            # img_resp = requests.get(url)
            # imgNp = np.array(bytearray(img_resp.content), dtype=np.uint8)
            # img = cv2.imdecode(imgNp, -1)
            # cv2.imshow('Android Cam', img)

            # Remove this code if using external camera
            _, img = video_capture.read()

            # Call method we defined above
            img = detect(img, faceCascade, eyesCascade, noseCascade, mouthCascade)
            # Writing processed image in a new window
            cv2.imshow("face detection", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Destroying output window
        cv2.destroyAllWindows()


root = Tk()
obj = Face_Recognition_System(root)
root.mainloop()


