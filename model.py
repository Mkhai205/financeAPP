import sqlite3

class FinanceModel:
    # Phương thức khởi tạo
    def __init__(self, db_name="finance.db"):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        self.__curent_user_id = None
        self.create_tables()
        
    # Phương thức tạo bảng
    def create_tables(self):
        # Tạo bảng users để lưu thông tin người dùng
        self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    balance INTEGER DEFAULT 0,
                    budget INTEGER DEFAULT 0
                )
            """)
        # Tạo bảng transactions để lưu thông tin giao dịch
        self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount INTEGER,
                    type TEXT,
                    category TEXT,
                    description TEXT,
                    date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
        self.__conn.commit()   
    
# Làm việc với bảng người dùng
    # Phương thức đăng ký người dùng
    def register_user(self, username, password):
        try:
            self.__cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.__conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    # Phương thức xóa người dùng
    def delete_user(self, user_id):
        try:
            self.__cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.__cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
            self.__conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    # Phương thức xác thực người dùng
    def verify_user(self, username, password):
        self.__cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user_id = self.__cursor.fetchone()
        if user_id:
            self.__curent_user_id = user_id[0]
            return True
        return False
    
    # Phương thức đăng xuất người dùng
    def logout_user(self):
        self.__curent_user_id = None
           
    # Phương thức lấy thông tin người dùng hiện tại
    def get_current_user(self):
        return self.__curent_user_id
    
    # Phương thức cập nhật số dư người dùng
    def set_user_balance(self, amount, transaction_type):
        if transaction_type == "Thu nhập":
            self.__cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, self.__curent_user_id))
        else:
            self.__cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, self.__curent_user_id))
        self.__conn.commit()

    # Phương thức lấy số dư người dùng
    def get_user_balance(self):
        self.__cursor.execute("SELECT balance FROM users WHERE user_id = ?", (self.__curent_user_id,))
        return self.__cursor.fetchone()[0]
    
    # Phương thức cập nhật ngân sách người dùng
    def set_user_budget(self, amount):
        self.__cursor.execute("UPDATE users SET budget = ? WHERE user_id = ?", (amount, self.__curent_user_id))
        self.__conn.commit()

    # Phương thức lấy ngân sách người dùng
    def get_user_budget(self):
        self.__cursor.execute("SELECT budget FROM users WHERE user_id = ?", (self.__curent_user_id,))
        return self.__cursor.fetchone()[0]
    
# Làm việc với bảng giao dịch
    # Phương thức thêm giao dịch
    def add_transaction_db(self, transaction_input):
        amount, transaction_type, category, description, date = transaction_input
        if self.__curent_user_id is None:
            return False
        try:
            self.__cursor.execute("""
                INSERT INTO transactions (user_id, amount, type, category, description, date) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.__curent_user_id, amount, transaction_type, category, description, date))
            self.set_user_balance(amount, transaction_type)
            self.__conn.commit()
            return True
        except:
            return False

    # Phương thức xóa giao dịch
    def delete_transaction_db(self, transaction_id):
        # Lấy chi tiết giao dịch để cập nhật số dư tài khoản
        self.__cursor.execute("SELECT amount, type FROM transactions WHERE transaction_id = ?", (transaction_id))
        transaction = self.__cursor.fetchone()
        if transaction:
            amount, transaction_type = transaction
            # Cập nhật số dư tài khoản
            self.set_user_balance(amount, "Chi tiêu" if transaction_type == "Thu nhập" else "Thu nhập")
            # Xóa giao dịch
            self.__cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id))
            self.__conn.commit()

    # Phương thức cập nhật giao dịch
    def update_transaction_db(self, transaction_id, transaction_input):
        amount, transaction_type, category, description, date = transaction_input
        # Lấy giao dịch cũ để điều chỉnh số dư tài khoản
        self.__cursor.execute("SELECT amount, type FROM transactions WHERE transaction_id = ?", (transaction_id))
        old_transaction = self.__cursor.fetchone()
        if old_transaction:
            old_amount, old_transaction_type = old_transaction
            # Cập nhật số dư tài khoản
            self.set_user_balance(old_amount, "Chi tiêu" if old_transaction_type == "Thu nhập" else "Thu nhập")
            self.set_user_balance(amount, transaction_type)
            # Cập nhật giao dịch
            self.__cursor.execute("""
                UPDATE transactions 
                SET amount = ?, type = ?, category = ?, description = ?, date = ?
                WHERE transaction_id = ?
            """, (amount, transaction_type, category, description, date, transaction_id))
            self.__conn.commit()

    # Phương thức lấy danh sách giao dịch
    def get_transactions_db(self):
        self.__cursor.execute("""
                              SELECT transaction_id, amount, type, category, description, date
                              FROM transactions WHERE user_id = ?
                              """, (self.__curent_user_id,))        
        return self.__cursor.fetchall()
        
    # Phuơng thức lấy tổng chi tiêu theo danh mục
    def get_total_expense_by_category(self):
        self.__cursor.execute("""
            SELECT category, SUM(amount) FROM transactions 
            WHERE type = 'Chi tiêu' AND user_id = ?
            GROUP BY category
        """, (self.__curent_user_id,))
        return self.__cursor.fetchall()

    # Phương thức lấy tổng thu nhập theo danh mục
    def get_total_income_by_category(self):
        self.__cursor.execute("""
            SELECT category, SUM(amount) FROM transactions 
            WHERE type = 'Thu nhập' AND user_id = ?
            GROUP BY category
        """, (self.__curent_user_id,))
        return self.__cursor.fetchall()
    
    # Phương thức ngắt kết nối với cơ sở dữ liệu
    def close(self):
        self.__conn.close()
