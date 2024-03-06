import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QMessageBox, \
    QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_student)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a click
        self.table.clicked.connect(self.cell_click)

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

    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()

    def cell_click(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_dialog)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_dialog)

        children = self.findChildren(QPushButton)
        for child in children:
            self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit_dialog(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_dialog(self):
        dialog = DeleteDialog()
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
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * from students WHERE name=?", (name,))
        rows = list(result)
        print(rows)
        items = student_management.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            student_management.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = student_management.table.currentRow()
        self.id = student_management.table.item(index, 0).text()
        print(self.id)

        # Add Name widget
        student_name = student_management.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        # Add course widget
        course = student_management.table.item(index, 2).text()
        self.courses = QComboBox()
        self.courses.addItems(['Math', 'Astronomy', 'Biology', 'Physics'])
        self.courses.setCurrentText(course)
        layout.addWidget(self.courses)

        # Add mobile widget
        mobile = student_management.table.item(index, 3).text()
        self.mobile_number = QLineEdit(mobile)
        layout.addWidget(self.mobile_number)

        # Add submit button
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_record)
        layout.addWidget(edit_button)

        self.setLayout(layout)

    def edit_record(self):
        name = self.student_name.text()
        course = self.courses.currentText()
        mobile = self.mobile_number.text()
        print (name, course, mobile, self.id)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
                       (name, course, mobile, self.id))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Record")

        # Get selected row index and student id
        index = student_management.table.currentRow()
        self.id = student_management.table.item(index, 0).text()
        print(self.id)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        yes.clicked.connect(self.delete_record)
        no = QPushButton("No")
        no.clicked.connect(self.close)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

    def delete_record(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (self.id, ))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()

        self.close()
        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Success")
        confirmation_box.setText("The record was deleted successfully!")
        confirmation_box.exec()


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
sys.exit(app.exec())
