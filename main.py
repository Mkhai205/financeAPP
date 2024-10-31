from model import FinanceModel
from view import FinanceView
from controller import FinanceController

def main():
    model = FinanceModel()
    view = FinanceView()
    controller = FinanceController(model, view)
    view.run()

if __name__ == "__main__":
    main()
