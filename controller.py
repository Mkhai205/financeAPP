class FinanceController:
    # Hàm khởi tạo Controller
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view._controller = self  # Gán controller cho view, giữ protected attribute

        # Kết nối các nút với các hàm xử lý
        self._view.btn_register.config(command=self.register_user)
        self._view.btn_login.config(command=self.login_user)

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
        transactions = self._model.get_transactions_db()
        total_income = 0
        total_expense = 0
        for trans in transactions:
            if trans[2] == "Thu nhập":
                total_income += trans[1]
            else:
                total_expense += trans[1]
                
        budget = self._model.get_user_budget()
        balance = self._model.get_user_balance()
        
        if total_expense > budget:
            self._view.display_message("Cảnh báo", "Chi tiêu đã vượt quá ngân sách!")

        self._view.clear_data_input()
        self._view.update_transactions_display(transactions)
        self._view.update_financial_info(total_income, total_expense, balance, budget)

    # Hàm đăng ký người dùng
    def register_user(self):
        username, password = self._view.get_login_info()
        if self._model.register_user(username, password):
            self._view.clear_login_info()
            self._view.display_message("Thành công", "Đăng ký thành công!")
        else:
            self._view.display_error("Lỗi", "Tên đăng nhập đã tồn tại!")

    # Hàm đăng nhập người dùng
    def login_user(self):
        username, password = self._view.get_login_info()
        if self._model.verify_user(username, password):
            self._view.show_application_view()
            self._view.set_username(username)
            self.update_report()
            self._view.display_message("Đăng cập thành công \n", f"Chào mừng {username} đến với ứng dụng quản lý tài chính!")
        else:
            self._view.display_error("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
    
    # Hàm đăng xuất người dùng
    def logout_user(self):
        self._model.logout_user()
        self._view.show_login_view()
        self._view.clear_login_info()
    
    # Hàm thêm giao dịch
    def add_transaction(self):
        data = self._view.get_data_input()
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        if not self._model.add_transaction_db(data):
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
        
        trans_id = selected_item[0]
        self._model.delete_transaction_db(trans_id)
        self.update_report()
        self._view.display_message("Thành công", "Giao dịch đã được xóa!")

    # Hàm đặt ngân sách        
    def set_budget(self):
        try:
            budget = int(self._view.get_budget_input())
            self._model.set_user_budget(budget)
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
        
        trans_id = selected_item[0]
        data = self._view.get_data_input()
        
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        try:
            self._model.update_transaction_db(trans_id, data)
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
        budget = self._model.get_user_budget()
        
        self._view.draw_chart(expense_data, income_data, budget)
