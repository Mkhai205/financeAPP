import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image, ImageTk

class FinanceView(tk.Tk):
    # Hàm khởi tạo giao diện (GUI)
    def __init__(self):
        super().__init__()
        self._controller = None  # protected attribute, controller is set in controller.py
        self.setup_general_view()
        self.create_login_view()
        self.create_application_view()
        
        # Hiển thị giao diện đăng cập khi khởi động
        self.show_login_view()


# Phương thức thiết lập giao diện
    # Hàm thiết lập giao diện chung
    def setup_general_view(self):
        # Thiết lập tiêu đề cho cửa sổ
        self.title("Ứng dụng Quản lý Tài chính Cá nhân")
        
        # Thiết lập kích thước cửa sổ
        self.window_width = 635
        self.window_height = 700
        
        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Tính toán tọa độ để căn giữa cửa sổ
        center_x = int((screen_width - self.window_width) / 2)
        center_y = int((screen_height - self.window_height) / 2)
        
        # Thiết lập vị trí của cửa sổ chính giữa màn hình
        self.geometry(f"{self.window_width}x{self.window_height}+{center_x}+{center_y}")
        
        # Thiết lập icon cho cửa sổ
        icon_path = "img\\us.png"
        icon_image = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon_image)
        
        # Khóa kích thước cửa sổ
        self.resizable(False, False)
    
    # Hàm tạo giao diện đăng nhập
    def create_login_view(self):
        # Tạo frame chứa các widget
        self.login_frame = tk.Frame(self)
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Thiết lập ảnh nền cho cửa sổ
        background_path = "img\\bg_login.png"
        bg_image = Image.open(background_path)
        bg_image = bg_image.resize((self.window_width, self.window_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.login_frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Thiết lập giao diện đăng nhập
        tk.Label(self.login_frame, text="Đăng nhập", font=("Times New Roman", 20, "bold"), bg="#D7E6D3").place(x=250, y=120)
        
        img_user_login = Image.open("img\\user.png").resize((30, 30), Image.LANCZOS)
        self.icon_user_login = ImageTk.PhotoImage(img_user_login)  
        
        self.lbl_icon_username_login = tk.Label(self.login_frame, image=self.icon_user_login, bg="#D7E6D3").place(x=180, y=215)
        tk.Label(self.login_frame, text="Tên đăng nhập:", font=("Times New Roman", 12, "bold"), bg="#D7E6D3").place(x=240, y=200)
        self.entry_username = tk.Entry(self.login_frame, width=30)
        self.entry_username.place(x=240, y=230)
        
        img_password = Image.open("img\\password.png").resize((30, 30), Image.LANCZOS)
        self.icon_password = ImageTk.PhotoImage(img_password)
        
        self.lbl_icon_password = tk.Label(self.login_frame, image=self.icon_password, bg="#D7E6D3").place(x=180, y=275)
        tk.Label(self.login_frame, text="Mật khẩu:", font=("Times New Roman", 12, "bold"), bg="#D7E6D3").place(x=240, y=260)
        self.entry_password = tk.Entry(self.login_frame, width=30, show="*")
        self.entry_password.place(x=240, y=290)
        
        # Nút đăng nhập và đăng ký
        self.btn_login = tk.Button(self.login_frame, text="Đăng nhập", font=("Times New Roman", 12, "bold"), bg="#38B6FF", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_login.place(x=220, y=350)
        
        self.btn_register = tk.Button(self.login_frame, text="Đăng ký", font=("Times New Roman", 12, "bold"), bg="#7ED957", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_register.place(x=330, y=350) 
        
        self.btn_register_premium = tk.Button(self.login_frame, text="Đăng ký Premium", font=("Times New Roman", 12, "bold"), bg="#FFD900", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_register_premium.place(x=250, y=400)
              
    # Hàm thiết lập giao diện chính của ứng dụng
    def create_application_view(self):
        # Tạo frame chứa các widget
        self.app_frame = tk.Frame(self)
        self.app_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Thiết lập ảnh nền cho cửa sổ
        background_path = "img\\bg_main.png"
        bg_image = Image.open(background_path)
        bg_image = bg_image.resize((self.window_width, self.window_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.app_frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Thiết lập tên tài khoản người dùng
        img_user = Image.open("img\\lemon.png").resize((30, 30), Image.LANCZOS)
        self.icon_user = ImageTk.PhotoImage(img_user)  # Keep a reference to avoid garbage collection
        
        self.lbl_icon_username = tk.Label(self.app_frame, image=self.icon_user, bg="#68869A").place(x=20, y=10)
        self.lbl_username = tk.Label(self.app_frame, text="", font=("Times New Roman", 13, "bold"), bg="#68869A", fg="#FFFBF0")
        self.lbl_username.place(x=60, y=15)
        
        # Thiết lập biểu tượng premium
        img_premium = Image.open("img\\premium.png").resize((30, 30), Image.LANCZOS)
        self.icon_premium = ImageTk.PhotoImage(img_premium)  # Keep a reference to avoid garbage collection
        self.lbl_premium = tk.Label(self.app_frame, image=self.icon_premium, bg="#68869A")
        self.lbl_premium.place(x=300, y=10)
        
        # Nút đăng xuất
        self.btn_logout = tk.Button(self.app_frame, text="Đăng xuất", font=("Times New Roman", 10, "bold"), bg="#FF3131", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_logout.place(x=540, y=10)
        
        
        # Thiết lập giao diện đầu vào
        tk.Label(self.app_frame, text="Số tiền:", bg="#FFFBF0", font=("Times New Roman", 10, "bold")).place(x=10, y=60)
        self.entry_amount = tk.Entry(self.app_frame, width=20)
        self.entry_amount.place(x=80, y=60)
        
        tk.Label(self.app_frame, text="Ngày:", bg="#FFFBF0", font=("Times New Roman", 10, "bold")).place(x=300, y=60)
        self.entry_date = DateEntry(self.app_frame, width=18, background="lightblue", foreground="white", date_pattern='yyyy-MM-dd')
        self.entry_date.place(x=380, y=60)
        
        tk.Label(self.app_frame, text="Loại:", bg="#FFFBF0", font=("Times New Roman", 10, "bold")).place(x=10, y=100)
        self.var_type = tk.StringVar(value="Thu nhập")
        tk.Radiobutton(self.app_frame, text="Thu nhập", variable=self.var_type, value="Thu nhập", command=self.update_category_options, bg="#FFFBF0", font=("Times New Roman", 9, "italic")).place(x=80, y=100)
        tk.Radiobutton(self.app_frame, text="Chi tiêu", variable=self.var_type, value="Chi tiêu", command=self.update_category_options, bg="#FFFBF0", font=("Times New Roman", 9, "italic")).place(x=180, y=100)
        
        tk.Label(self.app_frame, text="Danh mục:", bg="#FFFBF0", font=("Times New Roman", 10, "bold")).place(x=300, y=100)
        self.category_combobox = ttk.Combobox(self.app_frame, width=18)
        self.category_combobox.place(x=380, y=100)
        self.update_category_options()

        tk.Label(self.app_frame, text="Mô tả:", bg="#FFFBF0", font=("Times New Roman", 10, "bold")).place(x=10, y=140)
        self.entry_description = tk.Entry(self.app_frame, width=50)
        self.entry_description.place(x=80, y=140)


        # Nút thêm, sửa, xóa giao dịch và cập nhật ngân sách
        self.lbl_budget_inp = tk.Label(self.app_frame, text="Ngân sách:", bg="#FFFBF0", font=("Times New Roman", 10, "bold"))
        self.lbl_budget_inp.place(x=170, y=180)
        self.entry_budget = tk.Entry(self.app_frame, width=20)
        self.entry_budget.place(x=250, y=180)
        self.btn_set_budget = tk.Button(self.app_frame, text="Đặt ngân sách", font=("Times New Roman", 10, "bold"), bg="#7ED957", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_set_budget.place(x=390, y=180)
        
        self.btn_add = tk.Button(self.app_frame, text="Thêm giao dịch", font=("Times New Roman", 10, "bold"), bg="#38B6FF", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_add.place(x=120, y=220)
        
        self.btn_edit = tk.Button(self.app_frame, text="Sửa giao dịch", font=("Times New Roman", 10, "bold"), bg="#FFBD59", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_edit.place(x=270, y=220)
        
        self.btn_delete = tk.Button(self.app_frame, text="Xóa giao dịch", font=("Times New Roman", 10, "bold"), bg="#FF5757", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_delete.place(x=410, y=220)
        


        # Bảng hiển thị giao dịch
        columns = ("ID", "Số tiền", "Loại", "Danh mục", "Mô tả", "Ngày")
        self.tree = ttk.Treeview(self.app_frame, columns=columns, show="headings", height=8)
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Số tiền", width=100, anchor="center")
        self.tree.column("Loại", width=80, anchor="center")
        self.tree.column("Danh mục", width=100, anchor="center")
        self.tree.column("Mô tả", width=150, anchor="center")
        self.tree.column("Ngày", width=100, anchor="center")
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        self.tree.place(x=10, y=260, width=615, height=200)


        # Hiển thị thông tin tài chính
        self.lbl_income = tk.Label(self.app_frame, text="Thu nhập: 0", font=("Times New Roman", 10, "bold"), bg="#FFFBF0")
        self.lbl_expense = tk.Label(self.app_frame, text="Chi tiêu: 0", font=("Times New Roman", 10, "bold"), bg="#FFFBF0")
        self.lbl_balance = tk.Label(self.app_frame, text="Số dư: 0", font=("Times New Roman", 10, "bold"), bg="#FFFBF0")
        self.lbl_budget = tk.Label(self.app_frame, text="Ngân sách: 0", font=("Times New Roman", 10, "bold"), bg="#FFFBF0")
        self.lbl_income.place(x=20, y=470)
        self.lbl_expense.place(x=170, y=470)
        self.lbl_balance.place(x=350, y=470)
        self.lbl_budget.place(x=510, y=470)

        # Nút phân tích biểu đồ
        self.btn_chart = tk.Button(self.app_frame, text="Thống kê tài chính", font=("Times New Roman", 10, "bold"), bg="#00BB61", activebackground="#2F4F4F", activeforeground="#FFFFFF")
        self.btn_chart.place(x=210, y=510, width=200)

    def hide_premium_features(self):
        self.lbl_budget_inp.place_forget()
        self.entry_budget.place_forget()
        self.btn_set_budget.place_forget()
        self.lbl_premium.place_forget()
        self.lbl_budget.place_forget()
        self.btn_chart.place_forget()
            
    def show_premium_features(self):
        self.lbl_budget_inp.place(x=170, y=180)
        self.entry_budget.place(x=250, y=180)
        self.btn_set_budget.place(x=390, y=180)
        self.lbl_premium.place(x=300, y=10)
        self.lbl_budget.place(x=510, y=470)
        self.btn_chart.place(x=210, y=510, width=200)
        

# Phương thức chung
    # Chuyển sang gía diện đăng nhập
    def show_login_view(self):
        self.app_frame.place_forget()
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Chuyển sang giao diện ứng dụng
    def show_application_view(self):
        self.login_frame.place_forget()
        self.app_frame.place(x=0, y=0, relwidth=1, relheight=1)
   
   # Hàm hiển thị thông báo
    def display_message(self, title, message):
        messagebox.showinfo(title, message)
         
    # Hàm hiển thị lỗi
    def display_error(self, title, message):
        messagebox.showerror(title, message)


# Phương thức tương tác với login view
    # Hàm lấy thông tin đăng nhập
    def get_login_info(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        return username, password 
    
    # Hàm xóa thông tin đăng nhập
    def clear_login_info(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    
# Phương thức tương tác với application view
    # Hàm thiết lập tên người dùng
    def set_username(self, username):
        self.lbl_username.config(text=username)

    # Hàm lấy dữ liệu giao dịch
    def get_data_input(self):
        amount = int(self.entry_amount.get())
        transaction_type = self.var_type.get()
        category = self.category_combobox.get()
        description = self.entry_description.get()
        date = self.entry_date.get_date().strftime("%Y-%m-%d")
        return amount, transaction_type, category, description, date

    # Hàm xóa dữ liệu đầu vào
    def clear_data_input(self):
        self.entry_amount.delete(0, tk.END)
        self.var_type.set("Thu nhập")
        self.update_category_options()
        self.category_combobox.set('')
        self.entry_description.delete(0, tk.END)
        self.entry_date.set_date(datetime.now())
        self.entry_budget.delete(0, tk.END)

    # Hàm cập nhật danh mục dựa trên loại giao dịch
    def update_category_options(self):
        if self.var_type.get() == "Thu nhập":
            self.category_combobox.config(values=["Tiền lương", "Thưởng", "Part-time", "Đầu tư", "Khác"])
        else:
            self.category_combobox.config(values=["Ăn uống", "Mua sắm", "Xăng", "Sức khỏe", "Giải trí", "Du lịch", "Khác"])
    
    # Hàm hiển thị dữ liệu giao dịch lên giao diện
    def display_transaction_input(self, data):
        self.entry_amount.insert(0, data[1])
        self.var_type.set(data[2])
        self.update_category_options()
        self.category_combobox.set(data[3])
        self.entry_description.insert(0, data[4])
        self.entry_date.set_date(data[5])
        
    # Hàm cập nhật nhật các giao dịch ra bảng hiển thị
    def update_transactions_display(self, transactions):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for trans in transactions:
            self.tree.insert("", tk.END, values=trans)
    
    # Hàm cập nhật thông tin tài chính
    def update_financial_info(self, income, expense, balance, budget):
        self.lbl_income.config(text=f"Thu nhập: {income}")
        self.lbl_expense.config(text=f"Chi tiêu: {expense}")
        self.lbl_balance.config(text=f"Số dư: {balance}")
        self.lbl_budget.config(text=f"Ngân sách: {budget}")
         
    # Hàm lấy ngân sách
    def get_budget_input(self):
        return self.entry_budget.get()

    # Hàm lấy giao dịch được chọn
    def get_selected_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        return self.tree.item(selected_item, "values")       
    
    def draw_chart(self, expense_data, income_data, budget):
        # Lấy dữ liệu chi tiêu
        categories_expense = [row[0] for row in expense_data]
        amounts_expense = [row[1] for row in expense_data]
        
        # Dữ liệu thu nhập
        categories_income = [row[0] for row in income_data]
        amounts_income = [row[1] for row in income_data]
        
        # Tổng chi tiêu và thu nhập
        total_income = sum(amounts_income)
        total_expense = sum(amounts_expense)
        
        fig, axs = plt.subplots(1, 3, figsize=(12, 4))

        # Biểu đồ chi tiêu
        axs[0].pie(amounts_expense, labels=categories_expense, autopct='%1.1f%%')
        axs[0].set_title('Biểu đồ Chi tiêu')

        # Biểu đồ thu nhập
        axs[1].pie(amounts_income, labels=categories_income, autopct='%1.1f%%')
        axs[1].set_title('Biểu đồ Thu nhập')

        # Biểu đồ so sánh ngân sách
        axs[2].bar(['Thu nhập', 'Chi tiêu'], [total_income, total_expense], color=['blue', 'red'])
        axs[2].axhline(y=budget, color='green', linestyle='--', label=f'Ngân sách: {budget}')
        axs[2].legend()
        axs[2].set_title('So sánh Thu nhập, Chi tiêu và Ngân sách')
        axs[2].set_ylabel('Số tiền')

        plt.tight_layout()
        plt.show() 
        
    # Hàm chạy giao diện
    def run(self):
        self.mainloop()
