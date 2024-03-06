import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog
from PyQt6.QtGui import QAction
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        content = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(content):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add course widget
        self.courses = QComboBox()
        self.courses.addItems(['Math', 'Astronomy', 'Biology', 'Physics'])
        layout.addWidget(self.courses)

        # Add mobile widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_number)

        # Add submit button
        submit_button = QPushButton("Register")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.courses.currentText()
        mobile = self.mobile_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ? ,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
sys.exit(app.exec())

