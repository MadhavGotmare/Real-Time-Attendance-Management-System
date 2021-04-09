from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector
import requests
import numpy as np
import ssl
import cv2
import os
import csv


mydata=[]
class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1199x600+100+50")
        self.root.title("St. Vincent Pallotti College of Engineering & Technology")
        self.root.resizable(False, False)

        # =====variables=====
        self.var_userID = StringVar()
        self.var_collegeUID = StringVar()
        self.var_name = StringVar()
        self.var_dep = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()
        self.var_status = StringVar()


        # =====header image=====
        self.bg = ImageTk.PhotoImage(file="images/student_bg.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # =====left label frame=====
        Left_frame = LabelFrame(self.root, bd=3, bg="white", fg="red", relief=RIDGE, text="ATTENDANCE DETAILS", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=111, width=600, height=480)

        # =====information=====
        information_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, font=("times new roman", 12, "bold"))
        information_frame.place(x=10, y=20, width=575, height=420)

        # =====user id=====
        userID_label = Label(information_frame, text="User ID:", font=("times new roman", 12, "bold"), bg="white")
        userID_label.grid(row=0, column=0, padx=8, pady=20,sticky=W)

        userID_entry = ttk.Entry(information_frame, width=20, textvariable=self.var_userID, font=("times new roman", 12, "bold"))
        userID_entry.grid(row=0, column=1, padx=8, pady=20, sticky=W)

        # =====college uid=====
        collegeID_label = Label(information_frame, text="College UID:", font=("times new roman", 12, "bold"), bg="white")
        collegeID_label.grid(row=0, column=2, padx=8, pady=20, sticky=W)

        collegeID_entry = ttk.Entry(information_frame, width=20, textvariable=self.var_collegeUID, font=("times new roman", 12, "bold"))
        collegeID_entry.grid(row=0, column=3, padx=8, pady=20, sticky=W)

        # =====name=====
        name_label = Label(information_frame, text="Full Name:", font=("times new roman", 12, "bold"), bg="white")
        name_label.grid(row=1, column=0, padx=8, pady=20, sticky=W)

        name_entry = ttk.Entry(information_frame, width=20, textvariable=self.var_name,font=("times new roman", 12, "bold"))
        name_entry.grid(row=1, column=1, padx=8, pady=20, sticky=W)

        # =====department=====
        dep_label = Label(information_frame, text="Department:", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=1, column=2, padx=8, pady=20, sticky=W)

        dep_combo = ttk.Combobox(information_frame, font=("times new roman", 12, "bold"), width=18, textvariable=self.var_dep, state="read only")
        dep_combo['values'] = ("Select Department", "Administration", "Civil Engineering", "Computer Engineering", "Electrical Engineering", "Electronic and Telecommunication", "Information Technology", "Mechanical Engineering")
        dep_combo.current(0)
        dep_combo.grid(row=1, column=3, padx=8, pady=20, sticky=W)

        # =====date=====
        date_label = Label(information_frame, text="Date:", font=("times new roman", 12, "bold"), bg="white")
        date_label.grid(row=2, column=0, padx=8, pady=20, sticky=W)

        date_label = DateEntry(information_frame, date_pattern='dd/mm/yyyy', width=18, textvariable=self.var_date, font=("times new roman", 12, "bold"))
        date_label.grid(row=2, column=1, padx=8, pady=20, sticky=W)

        # =====time=====
        time_label = Label(information_frame, text="Time:", font=("times new roman", 12, "bold"), bg="white")
        time_label.grid(row=2, column=2, padx=8, pady=20, sticky=W)

        time_entry = ttk.Entry(information_frame, width=20, textvariable=self.var_time, font=("times new roman", 12, "bold"))
        time_entry.grid(row=2, column=3, padx=8, pady=20, sticky=W)

        # =====attendance status=====
        status_label = Label(information_frame, text="Status:", font=("times new roman", 12, "bold"), bg="white")
        status_label.grid(row=3, column=0, padx=8, pady=20, sticky=W)

        status_combo = ttk.Combobox(information_frame, font=("times new roman", 12, "bold"), width=18, textvariable=self.var_status, state="read only")
        status_combo['values'] = ("Attendance Status", "Present", "Absent")
        status_combo.current(0)
        status_combo.grid(row=3, column=1, padx=8, pady=20, sticky=W)

        # =====buttons frame1=====
        btn_frame1 = Frame(information_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=375, width=570, height=35)

        import_btn = Button(btn_frame1, cursor="hand2", text="Import CSV",  command=self.importCsv, padx=6, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        import_btn.grid(row=0, column=0)

        export_btn = Button(btn_frame1, cursor="hand2", text="Export CSV", command=self.exportCsv, padx=6, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        export_btn.grid(row=0, column=1)

        update_btn = Button(btn_frame1, cursor="hand2", text="Update", command=self.update_data, padx=7, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        update_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame1, cursor="hand2", text="Reset", command=self.reset_data, padx=8, width=12, fg="white", bg="#3ebca0", font=("Rockwell", 11, "bold"))
        reset_btn.grid(row=0, column=3)

        # =====right label frame=====
        Right_frame = LabelFrame(self.root, bd=3, bg="white", fg="red", relief=RIDGE, text="Attendance Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=610, y=111, width=580, height=480)

        # =====table System======
        table_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE,)
        table_frame.place(x=4, y=10, width=565, height=430)

        # =====scroll bar table=====
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame, column=("userID", "collegeUID", "name", "dep", "date", "time", "status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("userID", text="User ID")
        self.AttendanceReportTable.heading("collegeUID", text="College UID")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("dep", text="Department")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("time", text="Time")
        self.AttendanceReportTable.heading("status", text="Status")
        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("userID", width="50")
        self.AttendanceReportTable.column("collegeUID", width="70")
        self.AttendanceReportTable.column("name", width="140")
        self.AttendanceReportTable.column("dep", width="140")
        self.AttendanceReportTable.column("date", width="70")
        self.AttendanceReportTable.column("time", width="70")
        self.AttendanceReportTable.column("status", width="70")

        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

    # =====fetch data=====
    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)

    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)

    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("Error", "No Data found to export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
            with open(fln, mode="w", newline="") as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export", "Your data exported to " +os.path.basename(fln)+" successfully")
        except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        rows = content['values']
        self.var_userID.set(rows[0])
        self.var_collegeUID.set(rows[1])
        self.var_name.set(rows[2])
        self.var_dep.set(rows[3])
        self.var_time.set(rows[4])
        self.var_date.set(rows[5])
        self.var_status.set(rows[6])


    def update_data(self):
        userID = self.var_userID.get()
        collegeUID = self.var_collegeUID.get()
        name = self.var_name.get()
        dep = self.var_dep.get()
        time = self.var_time.get()
        date = self.var_date.get()
        status = self.var_status.get()

        try:
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save CSV",filetypes=(("CSV file","*.csv"),("All File","*.*")),parent=self.root)
            with open(fln,mode="a",newline="\n") as f:
                dict_writer = csv.DictWriter(f, fieldnames=(["User ID", "College UID", "Name", "Department", "Time", "Date", "Attendance"]))
                dict_writer.writeheader()
                dict_writer.writerow({"User ID":userID, "College UID":collegeUID, "Name":name, "Department":dep, "Time":time, "Date":date, "Attendance":status})
            messagebox.showinfo("Data Exported","Your data exported to " +os.path.basename(fln)+ " Successfully",parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To :{str(es)}", parent=self.root)




    def reset_data(self):
        self.var_userID.set("")
        self.var_collegeUID.set("")
        self.var_name.set("")
        self.var_dep.set("Select Department")
        self.var_time.set("")
        self.var_date.set("")
        self.var_status.set("Attendance Status")



root = Tk()
obj = Attendance(root)
root.mainloop()



