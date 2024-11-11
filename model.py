# Model Layer
import sqlite3

class FinanceModel:
    def __init__(self):
        self._conn = sqlite3.connect("financeDB.db")
        self._cursor = self._conn.cursor()
        self.create_database()
    
    def create_database(self):
        # Tạo bảng account để lưu thông tin người dùng
        self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_type TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    balance INTEGER DEFAULT 0,
                    budget INTEGER DEFAULT 0
                )
            """)
        # Tạo bảng transactions để lưu thông tin giao dịch
        self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
                    amount INTEGER,
                    transaction_type  TEXT,
                    category TEXT,
                    description TEXT,
                    date TEXT,
                    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
                )
            """)
        self._conn.commit()
        
    def close_database(self):
        self._conn.close()

class Account(FinanceModel):
    def __init__(self, username, password, account_type=None, account_id=None, balance=0, budget=0):
        super().__init__()
        # Các thuộc tính cơ bản của tài khoản
        self._account_id = account_id
        self._account_type = account_type 
        self._username = username
        self._password = password
        self._balance = balance
        self._budget = budget
        self._transactions = Transaction()
    
    def update_account_info(self):
        # Cập nhật thông tin tài khoản
        self._cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", 
                             (self._username, self._password))
        result = self._cursor.fetchone()
        if result:
            self._account_id, self._account_type, self._username, self._password, self._balance, self._budget = result
            self._transactions.set_account_id(self._account_id)
        
    def login(self):
        # Đăng nhập vào tài khoản
        self._cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", 
                             (self._username, self._password))
        result = self._cursor.fetchone()
        if result:
            self._account_id, self._account_type, self._username, self._password, self._balance, self._budget = result
            self._transactions.set_account_id(self._account_id)
            return True
        return False
    
    def logout(self):
        # Đăng xuất khỏi tài khoản
        self._account_id = None
        self._account_type = None
        self._username = None
        self._password = None
        self._balance = 0
        self._budget = 0
    
    def register(self):
        # Đăng ký tài khoản mới
        try:
            self._cursor.execute("INSERT INTO accounts (account_type, username, password) VALUES (?, ?, ?)", 
                                (self._account_type, self._username, self._password))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_account(self):
        # Cập nhật thông tin tài khoản
        pass
    
    def delete_account(self):
        # Xóa tài khoản khỏi database
        try:
            self._cursor.execute("DELETE FROM accounts WHERE account_id = ?", (self._account_id,))
            self._cursor.execute("DELETE FROM transactions WHERE account_id = ?", (self._account_id,))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_username(self):
        # Lấy thông tin người dùng
        return self._username
    
    def set_account_info(self, username, password, account_type=None):
        self._account_type = account_type
        self._username = username
        self._password = password
    
    def get_balance(self):
        # Lấy thông tin số dư
        return self._balance
    
    def get_account_type(self):
        # Lấy thông tin loại tài khoản
        return self._account_type
    
    def get_account_id(self):
        # Lấy thông tin id tài khoản
        return self._account_id
    
    def get_budget(self):
        # Lấy thông tin ngân sách
        return self._budget
    
    def get_password(self):
        # Lấy thông tin mật khẩu
        return self._password
          
    def set_balance(self, amount, transaction_type):
        # Cập nhật số dư
        if transaction_type == "Chi tiêu":
            self._balance -= int(amount)
        elif transaction_type == "Thu nhập":
            self._balance += int(amount)
        self._cursor.execute("UPDATE accounts SET balance = ? WHERE account_id = ?", (self._balance, self._account_id))
        self._conn.commit()
        
    def get_transactions(self):
        # Lấy thông tin tất cả giao dịch
        return self._transactions.get_transactions()
    
    def add_transaction(self, transaction_input):
        # Thêm giao dịch
        amount, transaction_type, category, description, date = transaction_input
        self._transactions.set_amount(amount)
        self._transactions.set_transaction_type(transaction_type)
        self._transactions.set_category(category)
        self._transactions.set_description(description)
        self._transactions.set_date(date)
        if self._transactions.add_transaction():
            self.set_balance(amount, transaction_type)
            return True
        return False

    def update_transaction(self, old_transaction, transaction_input):
        # Cập nhật thông tin giao dịch
        transaction_id = old_transaction[0]
        if self._transactions.update_transaction(transaction_id, transaction_input):
            self.set_balance(old_transaction[1], "Thu nhập" if old_transaction[2] == "Chi tiêu" else "Chi tiêu")
            self.set_balance(transaction_input[0], transaction_input[1])
            return True
        return False
    
    def delete_transaction(self, transaction):
        # Xóa giao dịch
        transaction_id = transaction[0]
        amount = transaction[1]
        if self._transactions.delete_transaction(transaction_id):
            self.set_balance(amount, "Thu nhập" if transaction[2] == "Chi tiêu" else "Chi tiêu")
            return True
        return False
    

class BasicAccount(Account):
    def __init__(self, username, password, account_type, account_id=None, balance=0, budget=None):
        super().__init__(username, password, account_type, account_id, balance, budget)
        # Các thuộc tính và phương thức dành riêng cho basicAccount


class PremiumAccount(Account):
    def __init__(self, username, password, account_type, account_id=None, balance=0, budget=None):
        super().__init__(username, password, account_type, account_id, balance, budget)
        # Các thuộc tính và phương thức dành riêng cho premiumAccount
        
    def get_budget(self):
        # Lấy thông tin ngân sách
        return self._budget
    
    def set_budget(self, budget):
        # Cập nhật ngân sách
        self._budget = budget
        self._cursor.execute("UPDATE accounts SET budget = ? WHERE account_id = ?", (self._budget, self._account_id))
        self._conn.commit()
        
    def get_total_expense_by_category(self):
        # Lấy thông tin tổng chi tiêu theo từng loại
        return self._transactions.get_total_expense_by_category()
    
    def get_total_income_by_category(self):
        # Lấy thông tin tổng thu nhập theo từng loại
        return self._transactions.get_total_income_by_category()
        


class Transaction(FinanceModel):
    def __init__(self, account_id=None, amount=None, transaction_type=None, category=None, description=None, date=None, transaction_id=None):
        super().__init__()
        # Các thuộc tính cơ bản của giao dịch
        self._transaction_id = transaction_id
        self._account_id = account_id
        self._amount = amount
        self._transaction_type = transaction_type
        self._category = category
        self._description = description
        self._date = date
        
    def set_account_id(self, account_id):
        # Cập nhật account_id
        self._account_id = account_id
        
    def set_amount(self, amount):
        # Cập nhật số tiền
        self._amount = amount
        
    def set_transaction_type(self, transaction_type):
        # Cập nhật loại giao dịch
        self._transaction_type = transaction_type
        
    def set_category(self, category):
        # Cập nhật loại giao dịch
        self._category = category
        
    def set_description(self, description):
        # Cập nhật mô tả
        self._description = description
        
    def set_date(self, date):
        # Cập nhật ngày tháng
        self._date = date
        
    def add_transaction(self):
        # Thêm giao dịch vào database
        try:
            self._cursor.execute("""
                INSERT INTO transactions (account_id, amount, transaction_type, category, description, date) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (self._account_id, self._amount, self._transaction_type, self._category, self._description, self._date))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_transaction(self, transaction_id, transaction_input):
        # Cập nhật thông tin giao dịch
        amount, transaction_type, category, description, date = transaction_input
        try:
            self._cursor.execute("""
                UPDATE transactions 
                SET amount = ?, transaction_type = ?, category = ?, description = ?, date = ?
                WHERE transaction_id = ?""",
                (amount, transaction_type, category, description, date, transaction_id))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def delete_transaction(self, transaction_id):
        # Xóa giao dịch khỏi database
        try:
            self._cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def get_transactions(self):
        # Lấy thông tin tất cả giao dịch
        self._cursor.execute("""
                             SELECT transaction_id, amount, transaction_type, category, description, date
                             FROM transactions WHERE account_id = ?
                             """, (self._account_id,))
        return self._cursor.fetchall()
    
    def get_total_expense_by_category(self):
        # Lấy thông tin tổng chi tiêu theo từng loại
        self._cursor.execute("""
                             SELECT category, SUM(amount) FROM transactions 
                             WHERE account_id = ? AND transaction_type = 'Chi tiêu'
                             GROUP BY category
                             """, (self._account_id,))
        return self._cursor.fetchall()
    
    def get_total_income_by_category(self):
        # Lấy thông tin tổng thu nhập theo từng loại
        self._cursor.execute("""
                             SELECT category, SUM(amount) FROM transactions 
                             WHERE account_id = ? AND transaction_type = 'Thu nhập'
                             GROUP BY category
                             """, (self._account_id,))
        return self._cursor.fetchall()
