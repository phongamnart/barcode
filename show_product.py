import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class BarcodeViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("แสดงบาร์โค้ดจากฐานข้อมูล")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("รายการบาร์โค้ด:")
        layout.addWidget(self.label)

        barcode_list = self.get_barcodes_from_database()
        barcode_text = "\n".join(barcode_list)
        self.label.setText("รายการบาร์โค้ด:\n" + barcode_text)

        central_widget.setLayout(layout)

    def get_barcodes_from_database(self):
        barcode_list = []

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="nart",
                password="tamarin17",
                database="product"
            )

            cursor = connection.cursor()

            # คำสั่ง SQL สำหรับดึงบาร์โค้ดทั้งหมด
            query = "SELECT barcode FROM add_product"
            cursor.execute(query)

            for row in cursor.fetchall():
                barcode_list.append(row[0])

        except mysql.connector.Error as error:
            print(f"เกิดข้อผิดพลาดในการเชื่อมต่อกับ MySQL: {str(error)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return barcode_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeViewerApp()
    window.show()
    sys.exit(app.exec_())
