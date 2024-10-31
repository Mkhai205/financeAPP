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
        self.controller = None  # Sẽ được gán trong Controller
        self.title("Ứng dụng Quản lý Tài chính Cá nhân")
        
        self.setup_gui()
    
    
    # Hàm thiết lập giao diện
    def setup_gui(self):
        # Thiết lập kích thước cửa sổ
        window_width = 600
        window_height = 700
        
        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Tính toán tọa độ để căn giữa cửa sổ
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Thiết lập vị trí của cửa sổ chính giữa màn hình
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Thiết lập ảnh nền cho cửa sổ
        background_path = "bg.jpg"
        bg_image = Image.open(background_path)
        bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Thiết lập icon cho cửa sổ
        icon_path = "us.png"
        icon_image = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon_image)
        
        
        # Thiết lập giao diện đầu vào
        self.frame_input = tk.Frame(self, padx=10, pady=10, bg="#184A89")
        self.frame_input.pack(fill="x")
        
        tk.Label(self.frame_input, text="Số tiền:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_amount = tk.Entry(self.frame_input, width=20)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame_input, text="Loại:").grid(row=1, column=0, padx=5, pady=5)
        self.var_type = tk.StringVar(value="Thu nhập")
        tk.Radiobutton(self.frame_input, text="Thu nhập", variable=self.var_type, value="Thu nhập", command=self.update_category_options).grid(row=1, column=1, padx=5, pady=5)
        tk.Radiobutton(self.frame_input, text="Chi tiêu", variable=self.var_type, value="Chi tiêu", command=self.update_category_options).grid(row=1, column=2, padx=5, pady=5)
        
        tk.Label(self.frame_input, text="Danh mục:").grid(row=2, column=0, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.frame_input, width=18)
        self.category_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.update_category_options()

        tk.Label(self.frame_input, text="Mô tả:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_description = tk.Entry(self.frame_input, width=30)
        self.entry_description.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        tk.Label(self.frame_input, text="Ngày:").grid(row=0, column=3, padx=5, pady=5)
        self.entry_date = DateEntry(self.frame_input, width=16, background="lightblue", foreground="white", date_pattern='yyyy-MM-dd')
        self.entry_date.grid(row=0, column=4, columnspan=2, padx=5, pady=5)


        # Nút thêm, sửa, xóa giao dịch và cập nhật ngân sách
        self.frame_actions = tk.Frame(self, padx=10, pady=10, bg="#184A89")
        self.frame_actions.pack(fill="x")
        
        self.btn_add = tk.Button(self.frame_actions, text="Thêm giao dịch")
        self.btn_add.grid(row=0, column=0, padx=60)
        
        self.btn_edit = tk.Button(self.frame_actions, text="Sửa giao dịch")
        self.btn_edit.grid(row=0, column=1, padx=30)
        
        self.btn_delete = tk.Button(self.frame_actions, text="Xóa giao dịch")
        self.btn_delete.grid(row=0, column=2, padx=60)
        
        tk.Label(self.frame_actions, text="Ngân sách:").grid(row=1, column=0)
        self.entry_budget = tk.Entry(self.frame_actions)
        self.entry_budget.grid(row=1, column=1)
        self.btn_set_budget = tk.Button(self.frame_actions, text="Đặt ngân sách")
        self.btn_set_budget.grid(row=1, column=2)


        # Bảng hiển thị giao dịch
        columns = ("ID", "Số tiền", "Loại", "Danh mục", "Mô tả", "Ngày")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self.tree.column("ID", width=30)
        self.tree.column("Số tiền", width=100)
        self.tree.column("Loại", width=80)
        self.tree.column("Danh mục", width=100)
        self.tree.column("Mô tả", width=150)
        self.tree.column("Ngày", width=100)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

    
        
        # Hiển thị thông tin tài chính
        self.lbl_income = tk.Label(self, text="Thu nhập: 0")
        self.lbl_expense = tk.Label(self, text="Chi tiêu: 0")
        self.lbl_balance = tk.Label(self, text="Số dư: 0")
        self.lbl_budget = tk.Label(self, text="Ngân sách: 0")
        self.lbl_income.pack()
        self.lbl_expense.pack()
        self.lbl_balance.pack()
        self.lbl_budget.pack()
        

        # Nút phân tích biểu đồ
        self.btn_chart = tk.Button(self, text="Phân tích biểu đồ")
        self.btn_chart.pack(pady=10)


    # Hàm lấy dữ liệu giao dịch
    def get_input(self):
        amount = self.entry_amount.get()
        type_ = self.var_type.get()
        category = self.category_combobox.get()
        description = self.entry_description.get()
        date = self.entry_date.get_date().strftime("%Y-%m-%d")
        return amount, type_, category, description, date


    # Hàm xóa dữ liệu đầu vào
    def clear_input(self):
        self.entry_amount.delete(0, tk.END)
        self.var_type.set("Thu nhập")
        self.category_combobox.set('')
        self.entry_description.delete(0, tk.END)
        self.entry_date.set_date(datetime.now())
        self.entry_budget.delete(0, tk.END)


    # Hàm hiển thị dữ liệu giao dịch lên giao diện
    def display_input(self, data):
        self.entry_amount.insert(0, data[1])
        self.var_type.set(data[2])
        self.update_category_options()
        self.category_combobox.set(data[3])
        self.entry_description.insert(0, data[4])
        self.entry_date.set_date(data[5])
        
        
    # Hàm cập nhật danh mục dựa trên loại giao dịch
    def update_category_options(self):
        if self.var_type.get() == "Thu nhập":
            self.category_combobox.config(values=["Tiền lương", "Thưởng", "Part-time", "Khác"])
        else:
            self.category_combobox.config(values=["Ăn uống", "Mua sắm", "Xăng", "Sức khỏe", "Giải trí", "Du lịch", "Khác"])
        
        
    # Hàm cập nhật nhật các giao dịch ra bảng hiển thị
    def update_transaction_view(self, transactions):
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


    # Hàm hiển thị thông báo
    def display_message(self, title, message):
        messagebox.showinfo(title, message)
        
        
    # Hàm hiển thị lỗi
    def display_error(self, title, message):
        messagebox.showerror(title, message)


    # Hàm lấy giao dịch được chọn
    def get_selected_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.display_error("Lỗi", "Vui lòng chọn một giao dịch!")
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
