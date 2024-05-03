import tkinter as tk
from tkinter import messagebox
import pymysql
import matplotlib.pyplot as plt
import numpy as np

class StudentDashboard:
    def __init__(self, master, student_id):
        self.master = master
        self.master.title("学生信息面板")
        self.master.geometry("800x600")  # 设置窗口大小
        master.config(bg="#FFFFFF")

        button_color = "#EC98FA"
        button_font = ("Arial", 20)
        # 保存学生ID
        self.student_id = student_id

        # 创建两个按钮
        self.course_button = tk.Button(master, text="课程信息", font=button_font,bg=button_color,command=self.show_course_info)
        self.course_button.pack(side="left", fill="y")

        self.basic_info_button = tk.Button(master, text="基本信息", font=button_font,bg=button_color,command=self.show_basic_info)
        self.basic_info_button.pack(side="left", fill="y")

        # 创建文本框用于显示信息
        self.info_text = tk.Text(master, width=60, height=20)
        self.info_text.pack(side="left", fill="both", expand=True)
        self.info_text.config(state="disabled")  # 禁用编辑功能

    def show_course_info(self):
        # 连接数据库，查询学生的课程信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "SELECT c.course_name, s.score FROM courses c INNER JOIN scores s ON c.course_id = s.course_id WHERE s.student_id = %s"
                cursor.execute(sql, (self.student_id,))
                result = cursor.fetchall()

                # 构建课程信息字符串
                course_info = "课程信息：\n"
                for row in result:
                    course_info += f"课程名称：{row['course_name']}，分数：{row['score']}\n"

                # 显示课程信息
                # 在文本框中显示课程信息
                self.info_text.config(state="normal")  # 允许编辑
                self.info_text.delete(1.0, tk.END)  # 清空文本框内容
                self.info_text.insert(tk.END, course_info)  # 插入课程信息
                self.info_text.config(state="disabled")  # 禁用编辑功能
        finally:
            connection.close()

    def show_basic_info(self):
        # 连接数据库，查询学生的基本信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students WHERE student_id = %s"
                cursor.execute(sql, (self.student_id,))
                result = cursor.fetchone()

                # 构建基本信息字符串
                basic_info = f"学生ID：{result['student_id']}\n"
                basic_info += f"姓名：{result['student_name']}\n"
                basic_info += f"年龄：{result['age']}\n"
                basic_info += f"性别：{result['gender']}\n"
                basic_info += f"班级：{result['class']}\n"

                # 在文本框中显示基本信息
                self.info_text.config(state="normal")  # 允许编辑
                self.info_text.delete(1.0, tk.END)  # 清空文本框内容
                self.info_text.insert(tk.END, basic_info)  # 插入基本信息
                self.info_text.config(state="disabled")  # 禁用编辑功能
        finally:
            connection.close()

