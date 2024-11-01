class FinanceController:
    # Hàm khởi tạo Controller
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._view._controller = self  # Gán controller cho view, giữ protected attribute

        # Kết nối các nút với các hàm xử lý
        self._view.btn_add.config(command=self.add_transaction)
        self._view.btn_set_budget.config(command=self.set_budget)
        self._view.btn_delete.config(command=self.delete_transaction)
        self._view.btn_edit.config(command=self.edit_transaction)
        self._view.btn_chart.config(command=self.show_chart)
        self._view.tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select())

        # Cập nhật báo cáo ban đầu
        self.update_report()
        
    
    # Kiểm tra dữ liệu đầu vào
    def validate_amount_category(self, amount, category):
        try:
            amount = float(amount)
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
                
        budget = self._model.get_budget_db()
        
        if total_expense > budget:
            self._view.display_message("Cảnh báo", "Chi tiêu đã vượt quá ngân sách!")

        self._view.clear_input()
        self._view.update_transaction_view(transactions)
        self._view.update_financial_info(total_income, total_expense, total_income - total_expense, budget)
    
    
    # Hàm thêm giao dịch
    def add_transaction(self):
        data = self._view.get_input()
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        self._model.add_transaction_db(data[0], data[1], data[2], data[3], data[4])
        self.update_report()
        self._view.display_message("Thành công", "Giao dịch đã được thêm!")

    
    # Hàm đặt ngân sách        
    def set_budget(self):
        try:
            budget = float(self._view.get_budget_input())
            self._model.update_budget_db(budget)
            self.update_report()
            self._view.display_message("Thành công", f"Ngân sách đã được đặt thành {budget}")
        except ValueError:
            self._view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho ngân sách!")


    # Hàm hiển thị giao dịch được chọn
    def on_tree_select(self):
        self._view.clear_input()
        selected_item = self._view.get_selected_transaction()
        if selected_item:
            self._view.display_input(selected_item)

            
        
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


    # Hàm sửa giao dịch
    def edit_transaction(self):
        selected_item = self._view.get_selected_transaction()
        if not selected_item:
            self._view.display_error("Lỗi", "Vui lòng chọn một giao dịch để sửa!")
            return
        
        trans_id = selected_item[0]
        data = self._view.get_input()
        
        
        if not self.validate_amount_category(data[0], data[2]):
            return
        
        try:
            self._model.edit_transaction_db(trans_id, data[0], data[1], data[2], data[3], data[4])
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
        budget = self._model.get_budget_db()
        
        self._view.draw_chart(expense_data, income_data, budget)
        
        
        
        
    
    
