import tkinter as tk
import loginwindow as LoginWindow  # 导入登录窗口类

def main():
    root = tk.Tk()
    login_window = LoginWindow.LoginWindow(root)  # 创建LoginWindow对象
    root.mainloop()

if __name__ == "__main__":
    main()
