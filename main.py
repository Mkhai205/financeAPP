# main.py
from model import Account, Transaction
from view import FinanceView
from controller import FinanceController

def main():
    # Khởi tạo Model
    account_model = Account(username="", password="")
    
    # Khởi tạo View
    view = FinanceView()
    
    # Khởi tạo Controller
    controller = FinanceController(account_model, view)
    
    # Hiển thị giao diện
    view.run()

if __name__ == "__main__":
    main()
