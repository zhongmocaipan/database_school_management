import tkinter as tk
from tkinter import messagebox
import pymysql

# 连接到数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='school_management',
    cursorclass=pymysql.cursors.DictCursor
)

# 使用连接执行 SQL 查询或其他操作
try:
    with connection.cursor() as cursor:
        # 示例：执行 SQL 查询
        sql = "SELECT * FROM students"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
finally:
    # 关闭数据库连接
    connection.close()

class StudentDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("学生信息面板")

        # 创建两个按钮
        self.course_button = tk.Button(master, text="课程信息", command=self.show_course_info)
        self.course_button.pack()

        self.basic_info_button = tk.Button(master, text="基本信息", command=self.show_basic_info)
        self.basic_info_button.pack()

    def show_course_info(self):
        messagebox.showinfo("课程信息", "这是课程信息")

    def show_basic_info(self):
        messagebox.showinfo("基本信息", "这是基本信息")
        
class TeacherDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("教师信息面板")

        # 创建两个按钮
        self.teach_course_button = tk.Button(master, text="教授课程信息", command=self.show_teach_course_info)
        self.teach_course_button.pack()

        self.basic_info_button = tk.Button(master, text="基本信息", command=self.show_basic_info)
        self.basic_info_button.pack()

    def show_teach_course_info(self):
        messagebox.showinfo("教授课程信息", "这是教授课程信息")

    def show_basic_info(self):
        messagebox.showinfo("基本信息", "这是基本信息")
        
class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("管理员信息面板")

        # 创建三个按钮
        self.delete_info_button = tk.Button(master, text="删除信息", command=self.show_delete_info)
        self.delete_info_button.pack()

        self.modify_info_button = tk.Button(master, text="修改信息", command=self.show_modify_info)
        self.modify_info_button.pack()
        
        self.add_info_button = tk.Button(master, text="增加信息", command=self.show_add_info)
        self.add_info_button.pack()

    def show_delete_info(self):
        messagebox.showinfo("删除信息", "这是删除信息")

    def show_modify_info(self):
        messagebox.showinfo("修改信息", "这是修改信息")
        
    def show_add_info(self):
        messagebox.showinfo("增加信息", "这是增加信息")

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("登录窗口")
        self.master.geometry("300x200")  # 设置窗口大小

        # 创建标签
        self.label = tk.Label(master, text="请选择登录类型:")
        self.label.pack()

        # 创建按钮
        self.teacher_button = tk.Button(master, text="教师登录", command=self.teacher_login)
        self.teacher_button.pack()

        self.admin_button = tk.Button(master, text="管理员登录", command=self.admin_login)
        self.admin_button.pack()

        self.student_button = tk.Button(master, text="学生登录", command=self.student_login)
        self.student_button.pack()

    def teacher_login(self):
        messagebox.showinfo("教师登录", "教师登录界面")
        self.open_id_password_window("教师")

    def admin_login(self):
        messagebox.showinfo("管理员登录", "管理员登录界面")
        self.open_id_password_window("管理员")

    def student_login(self):
        messagebox.showinfo("学生登录", "学生登录界面")
        self.open_id_password_window("学生")

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
        confirm_button = tk.Button(id_password_window, text="确认", command=lambda: self.confirm_login(id_password_window, user_type))
        confirm_button.grid(row=2, columnspan=2)

    def confirm_login(self, window, user_type):
        # 这里可以添加登录验证的逻辑
        messagebox.showinfo("登录成功", "登录成功！")
        window.destroy()
        self.open_dashboard(user_type)

    def open_dashboard(self, user_type):
        dashboard_window = tk.Toplevel()
        if user_type == "学生":
            dashboard = StudentDashboard(dashboard_window)
        elif user_type == "教师":
            dashboard = TeacherDashboard(dashboard_window)
        elif user_type == "管理员":
            dashboard = AdminDashboard(dashboard_window)

# def main():
#     root = tk.Tk()
#     login_window = LoginWindow(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()
