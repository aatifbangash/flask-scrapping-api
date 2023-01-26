from api import app
import os


class Root():

    csvHeader = None
    ROOT_DIR = None

    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        self.csvHeader = [
            "clickref",  # 0
            "details",  # 1
            "commission",  # 2
            "cwhen",  # 3
            "click_date",  # 4
            "reference_id",  # 5
            "unique_code",  # 6
            "status",  # 7
            "networkClass",  # 8
            "clickRefHash",  # 9
            "orderDate",  # 10
            "orderValue",  # 11
            "dateCreated"  # 12
        ]
        self.env = app.config['ENV']

    def formatPrice(self, price, symbol='€'):
        return price.replace(',', '.').replace(symbol, '')
