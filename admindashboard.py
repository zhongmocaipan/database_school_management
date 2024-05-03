import tkinter as tk
from tkinter import messagebox
import pymysql
import matplotlib.pyplot as plt
import numpy as np

class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("管理员信息面板")
        self.master.geometry("800x600")  # 设置窗口大小
        self.master.geometry("800x600")  # 设置窗口大小
        master.config(bg="#FFFFFF")

        button_color = "#EC98FA"
        button_font = ("Arial", 20)
        # 创建三个按钮
        self.delete_info_button = tk.Button(master, text="删除信息", font=button_font,bg=button_color,command=self.show_delete_info)
        self.delete_info_button.pack(side="left", fill="none", expand=True)

        self.modify_info_button = tk.Button(master, text="修改信息", font=button_font,bg=button_color,command=self.show_modify_info)
        self.modify_info_button.pack(side="left", fill="none", expand=True)
        
        self.add_info_button = tk.Button(master, text="增加信息", font=button_font,bg=button_color,command=self.show_add_info)
        self.add_info_button.pack(side="left", fill="none", expand=True)

    def show_delete_info(self):
        # 创建窗口
        delete_window = tk.Toplevel(self.master)
        delete_window.title("删除信息")

        # 连接数据库，获取学生信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students"
                cursor.execute(sql)
                students = cursor.fetchall()
        finally:
            connection.close()

        # 显示学生信息和勾选框
        for student in students:
            student_frame = tk.Frame(delete_window)
            student_frame.pack(side="left", fill="x")
            tk.Label(student_frame, text=f"ID: {student['student_id']}, Name: {student['student_name']}").pack(side="left")
            tk.Checkbutton(student_frame, variable=tk.BooleanVar()).pack(side="right")

        # 创建删除按钮
        delete_button = tk.Button(delete_window, text="删除", command=lambda: self.confirm_delete(delete_window, students))
        delete_button.pack(side="left", fill="x")

    def confirm_delete(self, window, students):
        # 连接数据库，删除勾选的学生信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                for student in students:
                    # 检查是否勾选
                    if tk.BooleanVar().get():
                        sql = "DELETE FROM students WHERE student_id = %s"
                        cursor.execute(sql, (student['student_id'],))
                        connection.commit()
        finally:
            connection.close()
        
        messagebox.showinfo("删除成功", "学生信息已成功删除！")
        window.destroy()

    def show_modify_info(self):
        # 创建窗口
        modify_window = tk.Toplevel(self.master)
        modify_window.title("修改信息")

        # 连接数据库，获取学生和教师信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # 获取学生信息
                sql_students = "SELECT * FROM students"
                cursor.execute(sql_students)
                students = cursor.fetchall()

                # 获取教师信息
                sql_teachers = "SELECT * FROM teachers"
                cursor.execute(sql_teachers)
                teachers = cursor.fetchall()
        finally:
            connection.close()

        # 显示学生信息和修改按钮
        for student in students:
            student_frame = tk.Frame(modify_window)
            student_frame.pack(side="left", fill="x")
            tk.Label(student_frame, text=f"ID: {student['student_id']}, Name: {student['student_name']}").pack(side="left")
            tk.Button(student_frame, text="修改", command=lambda s=student: self.show_modify_dialog(s)).pack(side="right")

        # 显示教师信息和修改按钮
        for teacher in teachers:
            teacher_frame = tk.Frame(modify_window)
            teacher_frame.pack(side="left", fill="x")
            tk.Label(teacher_frame, text=f"ID: {teacher['teacher_id']}, Name: {teacher['teacher_name']}").pack(side="left")
            tk.Button(teacher_frame, text="修改", command=lambda t=teacher: self.show_modify_dialog(t)).pack(side="right")

    def show_modify_dialog(self, data):
        # 创建窗口
        modify_dialog = tk.Toplevel(self.master)
        modify_dialog.title("修改信息")

        # 根据数据类型设置标题和标签
        if 'student_id' in data:
            modify_dialog.title("修改学生信息")
            tk.Label(modify_dialog, text="学生姓名:").grid(row=0, column=0)
            tk.Label(modify_dialog, text="年龄:").grid(row=1, column=0)
            tk.Label(modify_dialog, text="性别:").grid(row=2, column=0)
            tk.Label(modify_dialog, text="班级:").grid(row=3, column=0)
        elif 'teacher_id' in data:
            modify_dialog.title("修改教师信息")
            tk.Label(modify_dialog, text="教师姓名:").grid(row=0, column=0)
            tk.Label(modify_dialog, text="科目:").grid(row=1, column=0)

        # 创建输入框
        name_entry = tk.Entry(modify_dialog)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, data.get('student_name') if 'student_name' in data else data.get('teacher_name'))

        if 'student_id' in data:
            age_entry = tk.Entry(modify_dialog)
            age_entry.grid(row=1, column=1)
            age_entry.insert(0, data.get('age'))

            gender_entry = tk.Entry(modify_dialog)
            gender_entry.grid(row=2, column=1)
            gender_entry.insert(0, data.get('gender'))

            class_entry = tk.Entry(modify_dialog)
            class_entry.grid(row=3, column=1)
            class_entry.insert(0, data.get('class'))
        elif 'teacher_id' in data:
            subject_entry = tk.Entry(modify_dialog)
            subject_entry.grid(row=1, column=1)
            subject_entry.insert(0, data.get('subject'))

        # 创建确认按钮
        confirm_button = tk.Button(modify_dialog, text="确认", command=lambda: self.confirm_modify(modify_dialog, data, name_entry.get(), age_entry.get(), gender_entry.get(), class_entry.get() if 'student_id' in data else None, subject_entry.get() if 'teacher_id' in data else None))
        confirm_button.grid(row=4, columnspan=2)

    def confirm_modify(self, window, data, name, age, gender, class_, subject):
        # 连接数据库，修改信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                if 'student_id' in data:
                    sql = "UPDATE students SET student_name = %s, age = %s, gender = %s, class = %s WHERE student_id = %s"
                    cursor.execute(sql, (name, age, gender, class_, data['student_id']))
                elif 'teacher_id' in data:
                    sql = "UPDATE teachers SET teacher_name = %s, subject = %s WHERE teacher_id = %s"
                    cursor.execute(sql, (name, subject, data['teacher_id']))
                connection.commit()
        finally:
            connection.close()

        messagebox.showinfo("修改成功", "信息已成功修改！")
        window.destroy()

    def show_add_info(self):
        # 创建窗口
        add_window = tk.Toplevel(self.master)
        add_window.title("增加信息")

        # 创建两个按钮
        student_button = tk.Button(add_window, text="增加学生信息", command=lambda: self.show_add_student_dialog(add_window))
        student_button.pack(side="left", fill="x")

        teacher_button = tk.Button(add_window, text="增加教师信息", command=lambda: self.show_add_teacher_dialog(add_window))
        teacher_button.pack(side="left", fill="x")

    def show_add_student_dialog(self, window):
        # 创建窗口
        add_student_dialog = tk.Toplevel(window)
        add_student_dialog.title("增加学生信息")

        # 创建标签和输入框
        tk.Label(add_student_dialog, text="学生姓名:").grid(row=0, column=0)
        tk.Label(add_student_dialog, text="年龄:").grid(row=1, column=0)
        tk.Label(add_student_dialog, text="性别:").grid(row=2, column=0)
        tk.Label(add_student_dialog, text="班级:").grid(row=3, column=0)

        name_entry = tk.Entry(add_student_dialog)
        name_entry.grid(row=0, column=1)

        age_entry = tk.Entry(add_student_dialog)
        age_entry.grid(row=1, column=1)

        gender_entry = tk.Entry(add_student_dialog)
        gender_entry.grid(row=2, column=1)

        class_entry = tk.Entry(add_student_dialog)
        class_entry.grid(row=3, column=1)

        # 创建确认按钮
        confirm_button = tk.Button(add_student_dialog, text="确认", command=lambda: self.confirm_add_student(add_student_dialog, name_entry.get(), age_entry.get(), gender_entry.get(), class_entry.get()))
        confirm_button.grid(row=4, columnspan=2)

    def confirm_add_student(self, window, name, age, gender, class_):
        # 连接数据库，插入学生信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (student_name, age, gender, class) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, age, gender, class_))
                connection.commit()
        finally:
            connection.close()

        messagebox.showinfo("增加成功", "学生信息已成功增加！")
        window.destroy()

    def show_add_teacher_dialog(self, window):
        # 创建窗口
        add_teacher_dialog = tk.Toplevel(window)
        add_teacher_dialog.title("增加教师信息")

        # 创建标签和输入框
        tk.Label(add_teacher_dialog, text="教师姓名:").grid(row=0, column=0)
        tk.Label(add_teacher_dialog, text="科目:").grid(row=1, column=0)

        name_entry = tk.Entry(add_teacher_dialog)
        name_entry.grid(row=0, column=1)

        subject_entry = tk.Entry(add_teacher_dialog)
        subject_entry.grid(row=1, column=1)

        # 创建确认按钮
        confirm_button = tk.Button(add_teacher_dialog, text="确认", command=lambda: self.confirm_add_teacher(add_teacher_dialog, name_entry.get(), subject_entry.get()))
        confirm_button.grid(row=2, columnspan=2)

    def confirm_add_teacher(self, window, name, subject):
        # 连接数据库，插入教师信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO teachers (teacher_name, subject) VALUES (%s, %s)"
                cursor.execute(sql, (name, subject))
                connection.commit()
        finally:
            connection.close()

        messagebox.showinfo("增加成功", "教师信息已成功增加！")
        window.destroy()
