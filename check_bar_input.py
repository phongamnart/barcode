import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class NumberCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Check Barcode")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Enter your barcode:")
        layout.addWidget(self.label)

        self.input_box = QLineEdit()
        layout.addWidget(self.input_box)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.check_button = QPushButton("Check")
        self.check_button.clicked.connect(self.check_number)
        layout.addWidget(self.check_button)

        central_widget.setLayout(layout)

    def check_number(self):
        num1 = self.input_box.text()

        query = "SELECT barcode FROM add_product WHERE barcode = %s"

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="nart",
                password="tamarin17",
                database="product"
            )

            cursor = connection.cursor()

            cursor.execute(query, (num1,))
            result = cursor.fetchone()

            if result:
                self.result_label.setText(f"Barcode: {result[0]}")
            else:
                self.result_label.setText("False")

        except mysql.connector.Error as error:
            self.result_label.setText(f"Error not connect to MySQL: {str(error)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumberCheckerApp()
    window.show()
    sys.exit(app.exec_())
