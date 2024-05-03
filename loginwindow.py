import tkinter as tk
from tkinter import messagebox
import pymysql
import studentdashboard as StudentDashboard
import teacherdashboard as TeacherDashboard
import admindashboard as AdminDashboard

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("登录窗口")
        self.master.geometry("500x500")  # 设置窗口大小

        # 创建标签
        self.label = tk.Label(master, text="请选择登录类型:")
        self.label.pack()

        # 创建按钮
        self.teacher_button = tk.Button(master, text="教师登录", command=lambda: self.open_id_password_window("教师"))
        self.teacher_button.pack()

        self.admin_button = tk.Button(master, text="管理员登录", command=lambda: self.open_id_password_window("管理员"))
        self.admin_button.pack()

        self.student_button = tk.Button(master, text="学生登录", command=lambda: self.open_id_password_window("学生"))
        self.student_button.pack()

        self.logged_in_id = None  # 初始化成功登录的学生或教师的ID为None

    def open_id_password_window(self, user_type):
        id_password_window = tk.Toplevel()
        id_password_window.title(f"{user_type} ID和密码输入界面")
        id_password_window.geometry("300x150")  # 设置窗口大小

        # 创建标签和输入框
        id_label = tk.Label(id_password_window, text="ID:")
        id_label.grid(row=0, column=0)
        id_entry = tk.Entry(id_password_window)
        id_entry.grid(row=0, column=1)

        password_label = tk.Label(id_password_window, text="密码:")
        password_label.grid(row=1, column=0)
        password_entry = tk.Entry(id_password_window, show="*")
        password_entry.grid(row=1, column=1)

        # 创建确认按钮
        confirm_button = tk.Button(id_password_window, text="确认", command=lambda: self.confirm_login(id_password_window, user_type, id_entry.get(), password_entry.get()))
        confirm_button.grid(row=2, columnspan=2)

    def confirm_login(self, window, user_type, username, password):
        if user_type == "管理员" :
            if username == "admin" and password == "admin_password":
                self.logged_in_id = "admin"
                messagebox.showinfo("登录成功", "登录成功！")
                window.destroy()
                self.open_dashboard(user_type)
            else:
                messagebox.showerror("登录失败", "用户名或密码错误！")
            return
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='school_management',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                if user_type == "学生":
                    sql = "SELECT * FROM student_credentials WHERE student_id = %s AND password = %s"
                elif user_type == "教师":
                    sql = "SELECT * FROM teacher_credentials WHERE teacher_id = %s AND password = %s"
                elif user_type == "管理员":
                    sql = "SELECT * FROM admin_credentials WHERE admin_id = %s AND password = %s"
                
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()

            if result:
                self.logged_in_id = result.get('student_id') or result.get('teacher_id')  # 记录成功登录的学生或教师的ID
                messagebox.showinfo("登录成功", "登录成功！")
                window.destroy()
                self.open_dashboard(user_type)
            else:
                messagebox.showerror("登录失败", "用户名或密码错误！")
        finally:
            connection.close()

    def open_dashboard(self, user_type):
        dashboard_window = tk.Toplevel()
        if user_type == "学生":
            dashboard = StudentDashboard(dashboard_window, self.logged_in_id)  # 传递成功登录的学生ID
        elif user_type == "教师":
            dashboard = TeacherDashboard(dashboard_window, self.logged_in_id)  # 传递成功登录的教师ID
        elif user_type == "管理员":
            dashboard = AdminDashboard(dashboard_window)
