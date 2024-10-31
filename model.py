import sqlite3

class FinanceModel:
    # Khởi tạo cơ sở dữ liệu
    def __init__(self):
        self.conn = sqlite3.connect("finance.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS transactions
                          (id INTEGER PRIMARY KEY, amount REAL, type TEXT, category TEXT, description TEXT, date TIMESTAMP)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS budget (amount REAL)''')
        self.conn.commit()
        

    # Hàm thêm giao dịch
    def add_transaction_db(self, amount, type_, category, description, date):
        self.c.execute("INSERT INTO transactions (amount, type, category, description, date) VALUES (?, ?, ?, ?, ?)",
                       (amount, type_, category, description, date))
        self.conn.commit()

    # Hàm lấy tất cả giao dịch
    def get_transactions_db(self):
        self.c.execute("SELECT * FROM transactions")
        return self.c.fetchall()

    # Hàm cập nhật ngân sách
    def update_budget_db(self, amount):
        self.c.execute("SELECT COUNT(*) FROM budget")
        if self.c.fetchone()[0] == 0:
            self.c.execute("INSERT INTO budget (amount) VALUES (?)", (amount,))
        else:
            self.c.execute("UPDATE budget SET amount = ?", (amount,))
        self.conn.commit()

    # Hàm lấy ngân sách
    def get_budget_db(self):
        self.c.execute("SELECT amount FROM budget")
        budget = self.c.fetchone()  # Lấy kết quả vào biến
        return budget[0] if budget else 0  # Kiểm tra và trả về giá trị
    
    # Hàm xóa giao dịch
    def delete_transaction_db(self, trans_id):
        self.c.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
        self.conn.commit()

    # Hàm sửa giao dịch
    def edit_transaction_db(self, trans_id, amount, type_, category, description, date):
        self.c.execute("UPDATE transactions SET amount=?, type=?, category=?, description=?, date=? WHERE id=?",
                       (amount, type_, category, description, date, trans_id))
        self.conn.commit()
        
    # Hàm lấy tổng chi tiêu cho từng mục
    def get_total_expense_by_category(self):
        self.c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Chi tiêu' GROUP BY category")
        return self.c.fetchall()
    
    # Hàm lấy tổng thu nhập cho từng mục
    def get_total_income_by_category(self):
        self.c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Thu nhập' GROUP BY category")
        return self.c.fetchall()
    
    # Đóng kết nối khi kết thúc
    def __del__(self):
        self.conn.close()
