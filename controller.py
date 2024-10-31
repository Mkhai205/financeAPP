class FinanceController:
    # Hàm khởi tạo Controller
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self  # Gán controller cho view

        # Kết nối các nút với các hàm xử lý
        self.view.btn_add.config(command=self.add_transaction)
        self.view.btn_set_budget.config(command=self.set_budget)
        self.view.btn_delete.config(command=self.delete_transaction)
        self.view.btn_edit.config(command=self.edit_transaction)
        self.view.btn_chart.config(command=self.show_chart)

        # Cập nhật báo cáo ban đầu
        self.update_report()

    # Hàm cập nhật báo cáo
    def update_report(self):
        transactions = self.model.get_transactions_db()

        total_income = 0
        total_expense = 0
        for trans in transactions:
            if trans[2] == "Thu nhập":
                total_income += trans[1]
            else:
                total_expense += trans[1]
                
        budget = self.model.get_budget_db()

        self.view.clear_input()
        self.view.update_transaction_view(transactions)
        self.view.update_financial_info(total_income, total_expense, total_income - total_expense, budget)
    
    
    # Hàm thêm giao dịch
    def add_transaction(self):
        data = self.view.get_input()
        try:
            amount = float(data[0])
        except ValueError:
            self.view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho số tiền!")
            return
        
        if not data[2]:
            self.view.display_error("Lỗi", "Vui lòng chọn một danh mục!")
            return
        
        self.model.add_transaction_db(data[0], data[1], data[2], data[3], data[4])
        self.update_report()
        self.view.display_message("Thành công", "Giao dịch đã được thêm!")

    
    # Hàm đặt ngân sách        
    def set_budget(self):
        try:
            budget = float(self.view.get_budget_input())
            self.model.update_budget_db(budget)
            self.update_report()
            self.view.display_message("Thành công", f"Ngân sách đã được đặt thành {budget}")
        except ValueError:
            self.view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho ngân sách!")


    # Hàm xóa giao dịch
    def delete_transaction(self):
        selected_item = self.view.get_selected_transaction()
        if not selected_item:
            self.view.display_error("Lỗi", "Vui lòng chọn một giao dịch để xóa!")
            return
        
        trans_id = selected_item[0]
        self.model.delete_transaction_db(trans_id)
        self.update_report()
        self.view.display_message("Thành công", "Giao dịch đã được xóa!")

    # Hàm sửa giao dịch
    def edit_transaction(self):
        selected_item = self.view.get_selected_transaction()
        if not selected_item:
            self.view.display_error("Lỗi", "Vui lòng chọn một giao dịch để sửa!")
            return
        
        trans_id = selected_item[0]
        data = self.view.get_input()
        try:
            amount = float(data[0])
        except ValueError:
            self.view.display_error("Lỗi", "Vui lòng nhập một số hợp lệ cho số tiền!")
            return
        
        if not data[2]:
            self.view.display_error("Lỗi", "Vui lòng chọn một danh mục!")
            return
        
        self.model.edit_transaction_db(trans_id, data[0], data[1], data[2], data[3], data[4])
        self.update_report()
        self.view.display_message("Thành công", "Giao dịch đã được sửa!")
    
    def show_chart(self):
        # Lấy dữ liệu chi tiêu
        expense_data = self.model.get_total_expense_by_category()
        
        # Lấy dữ liệu thu nhập
        income_data = self.model.get_total_income_by_category()
        
        # Lấy ngân sách
        budget = self.model.get_budget_db()
        
        self.view.draw_chart(expense_data, income_data, budget)
