from model import PremiumAccount, BasicAccount
from model import Transaction

class FinanceController:
    # Hàm khởi tạo Controller
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view._controller = self  # Gán controller cho view, giữ protected attribute

        # Kết nối các nút với các hàm xử lý
        self._view.btn_register.config(command=self.register_user)
        self._view.btn_login.config(command=self.login_user)
        self._view.btn_register_premium.config(command=self.register_premium)

        self._view.btn_logout.config(command=self.logout_user)
        self._view.btn_add.config(command=self.add_transaction)
        self._view.btn_delete.config(command=self.delete_transaction)
        self._view.btn_edit.config(command=self.edit_transaction)
        self._view.btn_set_budget.config(command=self.set_budget)
        self._view.btn_chart.config(command=self.show_chart)
        self._view.tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select())

    # Hàm kiểm tra số tiền và danh mục
    def validate_amount_category(self, amount, category):
        try:
            amount = int(amount)
        except ValueError:
            self._view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho số tiền!")
            return False
        
        if not category:
            self._view.display_error("Lỗi", "Vui lòng chọn một danh mục!")
            return False
        
        return True

    # Hàm cập nhật báo cáo
    def update_report(self):
        transactions = self._model.get_transactions()
        total_income = 0
        total_expense = 0
        for trans in transactions:
            if trans[2] == "Thu nhập":
                total_income += trans[1]
            else:
                total_expense += trans[1]
                
        budget = self._model.get_budget()
        balance = self._model.get_balance()
        
        if self._model.get_account_type == "premium" and total_expense > budget:
            self._view.display_message("Cảnh báo", "Chi tiêu đã vượt quá ngân sách!")

        self._view.clear_data_input()
        self._view.update_transactions_display(transactions)
        self._view.update_financial_info(total_income, total_expense, balance, budget)

    def verify(self, username, password, account_type):
        self._model.set_account_info(username, password, account_type)
        if self._model.register():
            self._view.clear_login_info()
            if account_type == "premium":    
                self._view.display_message("Thành công", "Đăng ký thành công tài khoản Premium!")
            else:
                self._view.display_message("Thành công", "Đăng ký thành công!")
        else:
            self._view.display_error("Lỗi", "Tên đăng nhập đã tồn tại!")
        
    
    # Hàm đăng ký người dùng
    def register_user(self):
        username, password = self._view.get_login_info()
        account_type = "basic"
        self.verify(username, password, account_type)
        

    def register_premium(self):
        username, password = self._view.get_login_info()
        account_type = "premium"
        self.verify(username, password, account_type)
    
    # Hàm đăng nhập người dùng
    def login_user(self):
        username, password = self._view.get_login_info()
        self._model.set_account_info(username, password)
        if self._model.login():
            self._view.show_application_view()
            self._view.set_username(username)
            if self._model.get_account_type() == "premium":
                self._view.show_premium_features()
                self._model = PremiumAccount(username=username, password=password, account_type="premium")
            else:
               self._view.hide_premium_features() 
               self._model = BasicAccount(username=username, password=password, account_type="basic")
            
            self._model.update_account_info()
            self.update_report()
            self._view.display_message("Đăng cập thành công \n", f"Chào mừng {username} đến với ứng dụng quản lý tài chính!")
        else:
            self._view.display_error("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    # Hàm đăng xuất người dùng
    def logout_user(self):
        self._model.logout()
        self._view.show_login_view()
        self._view.clear_login_info()
    
    # Hàm thêm giao dịch
    def add_transaction(self):
        data = self._view.get_data_input()
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        if not self._model.add_transaction(data):
            print(f"Error: {data}")
            self._view.display_error("Lỗi", "Có lỗi xảy ra khi thêm giao dịch!")
            return
        
        self.update_report()
        self._view.display_message("Thành công", "Giao dịch đã được thêm!")
        
    # Hàm xóa giao dịch
    def delete_transaction(self):
        selected_item = self._view.get_selected_transaction()
        if not selected_item:
            self._view.display_error("Lỗi", "Vui lòng chọn một giao dịch để xóa!")
            return
        
        self._model.delete_transaction(selected_item)
        self.update_report()
        self._view.display_message("Thành công", "Giao dịch đã được xóa!")

    # Hàm đặt ngân sách        
    def set_budget(self):
        try:
            budget = int(self._view.get_budget_input())
            self._model.set_budget(budget)
            self.update_report()
            self._view.display_message("Thành công", f"Ngân sách đã được đặt thành {budget}")
        except ValueError:
            self._view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho ngân sách!")

    # Hàm hiển thị giao dịch được chọn
    def on_tree_select(self):
        self._view.clear_data_input()
        selected_item = self._view.get_selected_transaction()
        if selected_item:
            self._view.display_transaction_input(selected_item)

    # Hàm sửa giao dịch
    def edit_transaction(self):
        selected_item = self._view.get_selected_transaction()
        if not selected_item:
            self._view.display_error("Lỗi", "Vui lòng chọn một giao dịch để sửa!")
            return
        
        data = self._view.get_data_input()
        
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        try:
            self._model.update_transaction(selected_item, data)
            self.update_report()
            self._view.display_message("Thành công", "Giao dịch đã được sửa!")
        except Exception as e:
            self._view.display_error("Lỗi", f"Có lỗi xảy ra: {str(e)}")

    # Hàm hiển thị biểu đồ
    def show_chart(self):
        # Lấy dữ liệu chi tiêu
        expense_data = self._model.get_total_expense_by_category()
        
        # Lấy dữ liệu thu nhập
        income_data = self._model.get_total_income_by_category()
        
        # Lấy ngân sách
        budget = self._model.get_budget()
        
        self._view.draw_chart(expense_data, income_data, budget)
