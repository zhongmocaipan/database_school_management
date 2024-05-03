import tkinter as tk
from tkinter import messagebox
import pymysql
import matplotlib.pyplot as plt
import numpy as np

class StudentDashboard:
    def __init__(self, master, student_id):
        self.master = master
        self.master.title("学生信息面板")

        # 保存学生ID
        self.student_id = student_id

        # 创建两个按钮
        self.course_button = tk.Button(master, text="课程信息", command=self.show_course_info)
        self.course_button.pack()

        self.basic_info_button = tk.Button(master, text="基本信息", command=self.show_basic_info)
        self.basic_info_button.pack()

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
                messagebox.showinfo("课程信息", course_info)
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

                # 显示基本信息
                messagebox.showinfo("基本信息", basic_info)
        finally:
            connection.close()

