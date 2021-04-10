from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
import mysql.connector
import requests
import numpy as np
import ssl
import cv2


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1199x600+100+50")
        self.root.title("St. Vincent Pallotti College of Engineering & Technology")
        self.root.resizable(False, False)

        # =====variables=====
        self.var_dep = StringVar()
        self.var_year = StringVar()
        self.var_sem = StringVar()
        self.var_userID = StringVar()
        self.var_name = StringVar()
        self.var_class_division = StringVar()
        self.var_roll_no = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_collegeUID = StringVar()
        self.var_radio1 = StringVar()

        # =====header image=====
        self.bg=ImageTk.PhotoImage(file="images/student_bg.jpg")
        self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        # =====left label frame=====
        Left_frame=LabelFrame(self.root, bd=3, bg="white", relief=RIDGE, text="PERSONAL DETAILS", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=111, width=600, height=480)

        # =====course information=====
        course_frame=LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Course Information", font=("times new roman", 12, "bold"))
        course_frame.place(x=10, y=20, width=575, height=120)

        # =====department=====
        dep_label=Label(course_frame, text="Department", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10)

        dep_combo=ttk.Combobox(course_frame, textvariable=self.var_dep, font=("times new roman", 12, "bold"), width=20,  state="read only")
        dep_combo['values'] = ("Select Department", "Administration", "Civil Engineering", "Computer Engineering", "Electrical Engineering", "Electronic and Telecommunication", "Information Technology", "Mechanical Engineering")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # =====year=====
        year_label=Label(course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        year_label.grid(row=0, column=2, padx=10, sticky=W)

        year_combo = ttk.Combobox(course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), width=20, state="read only")
        year_combo['values'] = ("Select Year", "1st Year", "2nd Year", "3rd Year", "4th Year")
        year_combo.current(0)
        year_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # =====semester=====
        sem_label=Label(course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white")
        sem_label.grid(row=1, column=0, padx=10, sticky=W)

        sem_combo = ttk.Combobox(course_frame, textvariable=self.var_sem, font=("times new roman", 12, "bold"), width=20, state="read only")
        sem_combo['values'] = ("Select Semester", "1", "2", "3", "4", "5", "6", "7", "8", "Not Applicable")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # =====personal information=====
        personal_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Personal Information", font=("times new roman", 12, "bold"))
        personal_frame.place(x=10, y=150, width=575, height=300)

        # =====user id=====
        userID_label = Label(personal_frame, text="User ID:", font=("times new roman", 12, "bold"), bg="white")
        userID_label.grid(row=0, column=0, padx=8, sticky=W)

        userID_entry = ttk.Entry(personal_frame, textvariable=self.var_userID, width=18, font=("times new roman", 12, "bold"))
        userID_entry.grid(row=0, column=1, padx=8, sticky=W)

        # =====name=====
        name_label = Label(personal_frame, text="Full Name:", font=("times new roman", 12, "bold"), bg="white")
        name_label.grid(row=0, column=2, padx=8, pady=6, sticky=W)

        name_entry = ttk.Entry(personal_frame, textvariable=self.var_name, width=20, font=("times new roman", 12, "bold"))
        name_entry.grid(row=0, column=3, padx=8, pady=6, sticky=W)

        # =====class division=====
        class_division_label = Label(personal_frame, text="Class Division:", font=("times new roman", 12, "bold"), bg="white")
        class_division_label.grid(row=1, column=0, padx=8, pady=6, sticky=W)

        class_division_combo = ttk.Combobox(personal_frame, textvariable=self.var_class_division, font=("times new roman", 12, "bold"), width=16, state="read only")
        class_division_combo['values'] = ("Select Division", "A", "B", "Not Applicable")
        class_division_combo.current(0)
        class_division_combo.grid(row=1, column=1, padx=8, pady=6, sticky=W)

        # =====roll no=====
        roll_no_label = Label(personal_frame, text="Roll No:", font=("times new roman", 12, "bold"), bg="white")
        roll_no_label.grid(row=1, column=2, padx=8, pady=6, sticky=W)

        roll_no_label = ttk.Entry(personal_frame, textvariable=self.var_roll_no, width=20, font=("times new roman", 12, "bold"))
        roll_no_label.grid(row=1, column=3, padx=8, pady=6, sticky=W)

        # =====gender=====
        gender_label = Label(personal_frame, text="Gender:", font=("times new roman", 12, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=8, pady=6, sticky=W)

        gender_combo = ttk.Combobox(personal_frame, textvariable=self.var_gender, font=("times new roman", 12, "bold"), width=16, state="read only")
        gender_combo['values'] = ("Select Gender", "Male", "Female", "Transgender")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=8, pady=6, sticky=W)

        # =====dob=====
        dob_label = Label(personal_frame, text="DOB:", font=("times new roman", 12, "bold"), bg="white")
        dob_label.grid(row=2, column=2, padx=8, pady=6, sticky=W)

        dob_label = DateEntry(personal_frame, textvariable=self.var_dob, date_pattern='dd/mm/yyyy', width=18, font=("times new roman", 12, "bold"))
        dob_label.grid(row=2, column=3, padx=8, pady=6, sticky=W)

        # =====email=====
        email_label = Label(personal_frame, text="Email ID:", font=("times new roman", 12, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=8, pady=6, sticky=W)

        email_label = ttk.Entry(personal_frame, textvariable=self.var_email, width=18, font=("times new roman", 12, "bold"))
        email_label.grid(row=3, column=1, padx=8, pady=6, sticky=W)


        # =====phone=====
        phone_label = Label(personal_frame, text="Phone No:", font=("times new roman", 12, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=8, pady=6, sticky=W)

        phone_label = ttk.Entry(personal_frame, textvariable=self.var_phone, width=20, font=("times new roman", 12, "bold"))
        phone_label.grid(row=3, column=3, padx=8, pady=6, sticky=W)

        # =====address=====
        address_label = Label(personal_frame, text="Address:", font=("times new roman", 12, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=8, pady=6, sticky=W)

        address_label = ttk.Entry(personal_frame, textvariable=self.var_address, width=18, font=("times new roman", 12, "bold"))
        address_label.grid(row=4, column=1, padx=8, pady=6, sticky=W)

        # =====college uid=====
        collegeID_label = Label(personal_frame, text="College UID:", font=("times new roman", 12, "bold"), bg="white")
        collegeID_label.grid(row=4, column=2, padx=4, sticky=W)

        collegeID_entry = ttk.Entry(personal_frame, textvariable=self.var_collegeUID, width=20, font=("times new roman", 12, "bold"))
        collegeID_entry.grid(row=4, column=3, padx=4, sticky=W)

        # =====radio button=====
        self.var_radio1 = StringVar()
        radionbtn1 = ttk.Radiobutton(personal_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radionbtn1.grid(row=6, column=0)

        radionbtn2 = ttk.Radiobutton(personal_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radionbtn2.grid(row=6, column=1)

        # =====buttons frame1=====
        btn_frame1 = Frame(personal_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=210, width=570, height=35)


        save_btn = Button(btn_frame1, cursor="hand2", text="Save", command=self.add_data, padx=8, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame1, cursor="hand2", text="Update", command=self.update_data, padx=8, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame1, cursor="hand2", text="Delete", command=self.delete_data, padx=8, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame1, cursor="hand2", text="Reset", command=self.reset_data, padx=8, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        reset_btn.grid(row=0, column=3)

        # =====buttons frame2=====
        btn_frame2 = Frame(personal_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame2.place(x=0, y=240, width=570, height=35)

        take_photo_btn = Button(btn_frame2, cursor="hand2", text="Take Photo Sample", command=self.take_photo, padx=8, width=26, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        take_photo_btn.grid(row=2, column=0)

        update_photo_btn = Button(btn_frame2, cursor="hand2", text="Update Photo Sample", padx=8, width=26, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        update_photo_btn.grid(row=2, column=1)



        # =====right label frame=====
        Right_frame = LabelFrame(self.root, bd=3, bg="white", relief=RIDGE, text="Personal Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=610, y=111, width=580, height=480)

        # =====Search System======
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=0, y=20, width=570, height=70)

        # =====phone=====
        search_label = Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="#eb0c46", fg="white")
        search_label.grid(row=0, column=0, padx=8, pady=6, sticky=W)

        self.var_combo_search = StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_combo_search, font=("times new roman", 11, "bold"), width=12, state="read only")
        search_combo['values'] = ("Select Option", "College_UID", "Roll_No", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=16, font=("times new roman", 11, "bold"))
        search_entry.grid(row=0, column=2, padx=8, pady=6, sticky=W)

        search_btn = Button(search_frame, command=self.search_data, cursor="hand2", text="Search", width=10, fg="white", bg="#3ebca0", font=("Rockwell", 10, "bold"))
        search_btn.grid(row=0, column=3, padx=4)

        showALL_btn = Button(search_frame, command=self.fetch_data, cursor="hand2", text="Show All", width=10, fg="white", bg="#3ebca0", font=("Rockwell", 10, "bold"))
        showALL_btn.grid(row=0, column=4, padx=4)

        # =====Table Frame======
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=110, width=570, height=335)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.personal_details_table=ttk.Treeview(table_frame, column=("dep", "sem", "year", "userID", "name", "class_division", "roll_no", "gender", "dob", "email", "phone", "address", "collegeUID", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.personal_details_table.xview)
        scroll_y.config(command=self.personal_details_table.yview)

        self.personal_details_table.heading("dep", text="Department")
        self.personal_details_table.heading("sem", text="Semester")
        self.personal_details_table.heading("year", text="Year")
        self.personal_details_table.heading("userID", text="User ID")
        self.personal_details_table.heading("name", text="Name")
        self.personal_details_table.heading("class_division", text="Class Division")
        self.personal_details_table.heading("roll_no", text="Roll No")
        self.personal_details_table.heading("gender", text="Gender")
        self.personal_details_table.heading("dob", text="DOB")
        self.personal_details_table.heading("email", text="Email ID")
        self.personal_details_table.heading("phone", text="Phone")
        self.personal_details_table.heading("address", text="Address")
        self.personal_details_table.heading("collegeUID", text="College UID")
        self.personal_details_table.heading("photo", text="Photo Sample Status")
        self.personal_details_table["show"] = "headings"

        self.personal_details_table.column("dep", width=140)
        self.personal_details_table.column("sem", width=70)
        self.personal_details_table.column("year", width=70)
        self.personal_details_table.column("userID", width=50)
        self.personal_details_table.column("name", width=140)
        self.personal_details_table.column("class_division", width=100)
        self.personal_details_table.column("roll_no", width=50)
        self.personal_details_table.column("gender", width=60)
        self.personal_details_table.column("dob", width=70)
        self.personal_details_table.column("email", width=200)
        self.personal_details_table.column("phone", width=90)
        self.personal_details_table.column("address", width=200)
        self.personal_details_table.column("collegeUID", width=70)
        self.personal_details_table.column("photo", width=80)

        self.personal_details_table.pack(fill=BOTH, expand=1)
        self.personal_details_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # =====function declaration=====
    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_userID.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                                                                                                self.var_dep.get(),
                                                                                                                self.var_sem.get(),
                                                                                                                self.var_year.get(),
                                                                                                                self.var_userID.get(),
                                                                                                                self.var_name.get(),
                                                                                                                self.var_class_division.get(),
                                                                                                                self.var_roll_no.get(),
                                                                                                                self.var_gender.get(),
                                                                                                                self.var_dob.get(),
                                                                                                                self.var_email.get(),
                                                                                                                self.var_phone.get(),
                                                                                                                self.var_address.get(),
                                                                                                                self.var_collegeUID.get(),
                                                                                                                self.var_radio1.get()

                                                                                                         ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Info!", "Registration Completed Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error!", f"Due To :{str(es)}", parent=self.root)


    # =====fetch data=====
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data)!=0:
            self.personal_details_table.delete(*self.personal_details_table.get_children())
            for i in data:
                self.personal_details_table.insert("",END, values=i)
            conn.commit()
        conn.close()

    # =====get cursor=====
    def get_cursor(self, event=""):
        cursor_focus=self.personal_details_table.focus()
        content = self.personal_details_table.item(cursor_focus)
        data = content["values"]

        self.var_dep.set(data[0])
        self.var_sem.set(data[1]),
        self.var_year.set(data[2]),
        self.var_userID.set(data[3])
        self.var_name.set(data[4]),
        self.var_class_division.set(data[5]),
        self.var_roll_no.set(data[6]),
        self.var_gender.set(data[7]),
        self.var_dob.set(data[8]),
        self.var_email.set(data[9]),
        self.var_phone.set(data[10]),
        self.var_address.set(data[11]),
        self.var_collegeUID.set(data[12]),
        self.var_radio1.set(data[13])


    # =====update function=====
    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_userID.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Info!", "Do you want to update the current data", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set dep=%s, sem=%s, year=%s, name=%s, class_division=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, collegeUID=%s, photo=%s where userID=%s", (
                                                                                                                                                                                                                self.var_dep.get(),
                                                                                                                                                                                                                self.var_sem.get(),
                                                                                                                                                                                                                self.var_year.get(),
                                                                                                                                                                                                                self.var_name.get(),
                                                                                                                                                                                                                self.var_class_division.get(),
                                                                                                                                                                                                                self.var_roll_no.get(),
                                                                                                                                                                                                                self.var_gender.get(),
                                                                                                                                                                                                                self.var_dob.get(),
                                                                                                                                                                                                                self.var_email.get(),
                                                                                                                                                                                                                self.var_phone.get(),
                                                                                                                                                                                                                self.var_address.get(),
                                                                                                                                                                                                                self.var_collegeUID.get(),
                                                                                                                                                                                                                self.var_radio1.get(),
                                                                                                                                                                                                                self.var_userID.get()
                                                                                                                                                                                                            ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Info!", "Updating Completed Successfully", parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    # =====delete function=====
    def delete_data(self):
        if self.var_userID.get()=="":
            messagebox.showerror("Error", "User ID required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Warning", "Remove Data", parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                        my_cursor = conn.cursor()
                        sql="delete from student where userID=%s"
                        val=(self.var_userID.get(),)
                        my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Info!", "Data Successfully Deleted", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)


    # =====reset function=====
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_sem.set("Select Semester"),
        self.var_year.set("Select Year"),
        self.var_userID.set(""),
        self.var_name.set(""),
        self.var_class_division.set("Select Division"),
        self.var_roll_no.set(""),
        self.var_gender.set("Select Gender"),
        self.var_dob.set(""),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),
        self.var_collegeUID.set(""),
        self.var_radio1.set("")


    # =====generate data set or take photo samples=====
    def take_photo(self):
        user = self.var_userID.get()
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_userID.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myresult=my_cursor.fetchall()
                id=0

                for x in myresult:
                    id+=1
                my_cursor.execute("update student set dep=%s, sem=%s, year=%s, name=%s, class_division=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, collegeUID=%s, photo=%s where userID=%s", (
                                                                                                                                                                                                            self.var_dep.get(),
                                                                                                                                                                                                            self.var_sem.get(),
                                                                                                                                                                                                            self.var_year.get(),
                                                                                                                                                                                                            self.var_name.get(),
                                                                                                                                                                                                            self.var_class_division.get(),
                                                                                                                                                                                                            self.var_roll_no.get(),
                                                                                                                                                                                                            self.var_gender.get(),
                                                                                                                                                                                                            self.var_dob.get(),
                                                                                                                                                                                                            self.var_email.get(),
                                                                                                                                                                                                            self.var_phone.get(),
                                                                                                                                                                                                            self.var_address.get(),
                                                                                                                                                                                                            self.var_collegeUID.get(),
                                                                                                                                                                                                            self.var_radio1.get(),
                                                                                                                                                                                                            self.var_userID.get()==id+1
                                                                                                                                                                                                        ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()


                # =====Method to generate dataset to recognize a person=====
                def generate_dataset(img, id, img_id):
                    # =====write image in data dir=====
                    cv2.imwrite("data/user."+str(id)+"."+str(img_id)+".jpg", img)

                # =====Method to draw boundary around the detected feature=====
                def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
                    # =====Converting image to gray-scale=====
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # =====detecting features in gray-scale image, returns coordinates, width and height of features=====
                    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
                    coords = []
                    # =====drawing rectangle around the feature and labeling it=====
                    for (x, y, w, h) in features:
                        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                        coords = [x, y, w, h]
                    return coords

                # =====Method to detect the features=====
                def detect(img, faceCascade, img_id):
                    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
                    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")

                    # =====if feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0=====
                    if len(coords)==4:
                        # ===== updating region of interest by cropping image=====
                        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]

                        generate_dataset(roi_img, user, img_id)
                    return img

                # =====Loading classifiers=====
                faceCascade = cv2.CascadeClassifier('haarcascade_files/haarcascade_frontalface_default.xml')

                # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
                # ctx = ssl.create_default_context()
                # ctx.check_hostname = False
                # ctx.verify_mode = ssl.CERT_NONE

                # url = 'http://192.168.0.182:8080/shot.jpg'

                # =====Remove this code if using internal camera (0) external camera (1)=====
                video_capture = cv2.VideoCapture(0)

                # =====Initialize img_id with 0=====
                img_id = 0

                while True:
                    if img_id % 200 == 0:
                        print("Collected ", img_id, "images")

                    # Reading image from video stream
                    # img_resp = requests.get(url)
                    # imgNp = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    # img = cv2.imdecode(imgNp, -1)
                    # cv2.imshow('Android Cam', img)

                    # =====remove this code if using external camera=====
                    _, img = video_capture.read()

                    # =====call method we defined above=====
                    img = detect(img, faceCascade, img_id)

                    # =====writing processed image in a window=====
                    cv2.imshow("face detection", img)
                    img_id += 1

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # =====destroying output window=====
                cv2.destroyAllWindows()
                messagebox.showinfo("Info!", "Generating data sets completed")

            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)


    # =====search data=====
    def search_data(self):
        if self.var_combo_search.get()=="" or self.var_search.get()=="Select Option":
            messagebox.showerror("Error", "Please Select Option", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="college_data")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student where " +str(self.var_combo_search.get())+" LIKE '%"+str(self.var_search.get())+"%'")
                rows = my_cursor.fetchall()
                if len(rows) != 0:
                    self.personal_details_table.delete(*self.personal_details_table.get_children())
                    for i in rows:
                        self.personal_details_table.insert("", END, values=i)
                    if rows == None:
                        messagebox.showerror("Error", "Data Not Found", parent=self.root)
                        conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To :{str(es)}", parent=self.root)


root = Tk()
obj = Student(root)
root.mainloop()
