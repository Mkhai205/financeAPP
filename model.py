import sqlite3

class FinanceModel:
    # Khởi tạo cơ sở dữ liệu
    def __init__(self):
        self.__db = sqlite3.connect("finance.db") # private attribute
        self.__cursor = self.__db.cursor() # private attribute
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                          (id INTEGER PRIMARY KEY, amount REAL, type TEXT, category TEXT, description TEXT, date TIMESTAMP)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS budget (amount REAL)''')
        self.__db.commit()
        

    # Hàm thêm giao dịch
    def add_transaction_db(self, amount, type_, category, description, date):
        self.__cursor.execute("INSERT INTO transactions (amount, type, category, description, date) VALUES (?, ?, ?, ?, ?)",
                       (amount, type_, category, description, date))
        self.__db.commit()

    # Hàm lấy tất cả giao dịch
    def get_transactions_db(self):
        self.__cursor.execute("SELECT * FROM transactions")
        return self.__cursor.fetchall()

    # Hàm cập nhật ngân sách
    def update_budget_db(self, amount):
        self.__cursor.execute("SELECT COUNT(*) FROM budget")
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("INSERT INTO budget (amount) VALUES (?)", (amount,))
        else:
            self.__cursor.execute("UPDATE budget SET amount = ?", (amount,))
        self.__db.commit()

    # Hàm lấy ngân sách
    def get_budget_db(self):
        self.__cursor.execute("SELECT amount FROM budget")
        budget = self.__cursor.fetchone()  # Lấy kết quả vào biến
        return budget[0] if budget else 0  # Kiểm tra và trả về giá trị
    
    # Hàm xóa giao dịch
    def delete_transaction_db(self, trans_id):
        self.__cursor.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
        self.__db.commit()

    # Hàm sửa giao dịch
    def edit_transaction_db(self, trans_id, amount, type_, category, description, date):
        self.__cursor.execute("UPDATE transactions SET amount=?, type=?, category=?, description=?, date=? WHERE id=?",
                       (amount, type_, category, description, date, trans_id))
        self.__db.commit()
        
    # Hàm lấy tổng chi tiêu cho từng mục
    def get_total_expense_by_category(self):
        self.__cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Chi tiêu' GROUP BY category")
        return self.__cursor.fetchall()
    
    # Hàm lấy tổng thu nhập cho từng mục
    def get_total_income_by_category(self):
        self.__cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Thu nhập' GROUP BY category")
        return self.__cursor.fetchall()
    
    # Đóng kết nối khi kết thúc
    def __del__(self):
        self.__db.close()
