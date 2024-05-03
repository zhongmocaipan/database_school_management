import tkinter as tk
from tkinter import messagebox
import pymysql
import matplotlib.pyplot as plt
import numpy as np

class TeacherDashboard:
    def __init__(self, master, teacher_id):
        self.master = master
        self.master.title("教师信息面板")
        self.master.geometry("800x600")  # 设置窗口大小
        self.master.geometry("800x600")  # 设置窗口大小
        master.config(bg="#FFFFFF")

        button_color = "#EC98FA"
        button_font = ("Arial", 20)
        # 保存教师ID
        self.teacher_id = teacher_id

        # 创建两个按钮
        self.teach_course_button = tk.Button(master, text="教授课程信息", font=button_font,bg=button_color,command=self.show_teach_course_info)
        self.teach_course_button.pack(side="left", fill="none", expand=True)

        self.basic_info_button = tk.Button(master, text="基本信息", font=button_font,bg=button_color,command=self.show_basic_info)
        self.basic_info_button.pack(side="left", fill="none", expand=True)

        # 添加图表分析按钮
        self.analyze_scores_button = tk.Button(master, text="图表分析", font=button_font,bg=button_color,command=self.analyze_student_scores)
        self.analyze_scores_button.pack(side="left", fill="none", expand=True)

        # 创建文本框用于显示基本信息
        self.info_text = tk.Text(master, width=60, height=20)
        self.info_text.pack(side="left", fill="both", expand=True)
        self.info_text.config(state="disabled")  # 禁用编辑功能

    def show_teach_course_info(self):
        # 连接数据库，查询教师的教授课程信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # 获取教师所教授的课程ID
                sql_course_id = "SELECT course_id FROM course_statistics WHERE teacher_id = %s"
                cursor.execute(sql_course_id, (self.teacher_id,))
                course_ids = [row['course_id'] for row in cursor.fetchall()]

                # 获取学生的成绩以及这门课的平均分、最低分和最高分
                course_info = ""
                for course_id in course_ids:
                    # 获取学生的成绩
                    sql_scores = "SELECT student_id, score FROM scores WHERE course_id = %s"
                    cursor.execute(sql_scores, (course_id,))
                    scores = cursor.fetchall()

                    # 获取这门课的平均分、最低分和最高分
                    sql_course_stats = "SELECT average_score, min_score, max_score FROM course_statistics WHERE course_id = %s"
                    cursor.execute(sql_course_stats, (course_id,))
                    course_stats = cursor.fetchone()

                    # 构建课程信息字符串
                    course_info += f"课程ID：{course_id}\n"
                    course_info += "学生成绩：\n"
                    for score in scores:
                        student_id = score['student_id']
                        student_name = ""
                        sql_student_name = "SELECT student_name FROM students WHERE student_id = %s"
                        cursor.execute(sql_student_name, (student_id,))
                        student = cursor.fetchone()
                        if student:
                            student_name = student['student_name']
                        course_info += f"学生ID：{student_id}，学生姓名：{student_name}，分数：{score['score']}\n"
                    course_info += f"平均分：{course_stats['average_score']}，最低分：{course_stats['min_score']}，最高分：{course_stats['max_score']}\n\n"

                # 显示教授课程信息
                if course_info:
                    messagebox.showinfo("教授课程信息", course_info)
                else:
                    messagebox.showinfo("教授课程信息", "无教授课程信息")
        finally:
            connection.close()


    def show_basic_info(self):
        # 连接数据库，查询教师的基本信息
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM teachers WHERE teacher_id = %s"
                cursor.execute(sql, (self.teacher_id,))
                result = cursor.fetchone()

                # 构建基本信息字符串
                basic_info = f"教师ID：{result['teacher_id']}\n"
                basic_info += f"姓名：{result['teacher_name']}\n"
                basic_info += f"科目：{result['subject']}\n"

                # 在文本框中显示基本信息
                self.info_text.config(state="normal")  # 允许编辑
                self.info_text.delete(1.0, tk.END)  # 清空文本框内容
                self.info_text.insert(tk.END, basic_info)  # 插入基本信息
                self.info_text.config(state="disabled")  # 禁用编辑功能
        finally:
            connection.close()
    def analyze_student_scores(self):
        # 连接数据库，查询学生成绩
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # 获取教师所教授的课程ID
                sql_course_id = "SELECT course_id FROM course_statistics WHERE teacher_id = %s"
                cursor.execute(sql_course_id, (self.teacher_id,))
                course_ids = [row['course_id'] for row in cursor.fetchall()]

                # 初始化课程成绩字典
                course_scores = {}

                # 获取每门课程的学生成绩
                for course_id in course_ids:
                    # 获取学生成绩
                    sql_scores = "SELECT score FROM scores WHERE course_id = %s"
                    cursor.execute(sql_scores, (course_id,))
                    scores = [row['score'] for row in cursor.fetchall()]

                    # 将成绩存储到课程成绩字典中
                    course_scores[course_id] = scores

                # 绘制学生成绩图表
                self.plot_scores(course_scores)
        finally:
            connection.close()

    def plot_scores(self, course_scores):
        # 创建 Matplotlib 图表
        plt.figure(figsize=(10, 6))

        # 绘制每门课程的成绩箱线图
        for course_id, scores in course_scores.items():
            plt.boxplot(scores, positions=[course_id], widths=0.5, patch_artist=True, boxprops=dict(facecolor='skyblue'))

        # 设置图表标题和轴标签
        plt.title("学生成绩分析")
        plt.xlabel("课程ID")
        plt.ylabel("分数")

        # 设置 x 轴刻度标签
        plt.xticks(list(course_scores.keys()), list(course_scores.keys()))

        # 显示图表
        plt.grid(True)
        plt.show()
        