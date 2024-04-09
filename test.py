import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit

class TransactionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Transaction Tracker")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload CSV File")
        self.upload_button.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_button)

        self.transaction_display = QTextEdit()
        self.layout.addWidget(self.transaction_display)

        self.central_widget.setLayout(self.layout)


        self.conn = sqlite3.connect('transactions.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                     TransactionID TEXT PRIMARY KEY,
                     CustomerName TEXT NOT NULL,
                     TransactionDate TEXT NOT NULL,
                     Amount REAL NOT NULL,
                     Status TEXT NOT NULL,
                     InvoiceURL TEXT
                     )''')
        self.conn.commit()

    def upload_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, 'r') as file:
                data = file.read().splitlines()
                transactions = [line.split('\t') for line in data]
                for transaction in transactions:
                    self.c.execute('''INSERT OR REPLACE INTO transactions (TransactionID, CustomerName, TransactionDate, Amount, Status, InvoiceURL)
                                     VALUES (?, ?, ?, ?, ?, ?)''', (transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5]))
                self.conn.commit()
                self.display_transactions()

    def display_transactions(self):
        self.c.execute('SELECT * FROM transactions')
        transactions = self.c.fetchall()
        self.transaction_display.clear()
        for transaction in transactions:
            self.transaction_display.append('\t'.join(map(str, transaction)))

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransactionApp()
    window.show()
    sys.exit(app.exec_())
