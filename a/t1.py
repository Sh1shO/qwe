from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from db import Session, Employee, JobName
from sqlalchemy import or_
from add_jobname import AddJobNameDialog
from addEmployeeDialog import AddEmployeeDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tq")
        self.setMinimumSize(600, 700)

        container = QTableWidget()
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.btn_add_jobname = QPushButton("Add JobName")
        control_layout.addWidget(self.btn_add_jobname)
        self.btn_add_jobname.clicked.connect(self.open_add_jobname_dialog)

        self.filter = QComboBox()
        self.filter.addItem("All Jobnames")
        control_layout.addWidget(self.filter)
        self.filter.currentIndexChanged.connect(self.load_data)

        self.btn_add_employee = QPushButton("+")
        control_layout.addWidget(self.btn_add_employee)
        self.btn_add_employee.clicked.connect(self.open_add_dialog)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        control_layout.addWidget(self.search)
        self.search.textChanged.connect(self.load_data)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Фамилия", "Должность"])
        main_layout.addWidget(self.table)

        self.load_data()
        self.load_jobnames()

    def open_add_jobname_dialog(self):
        dialog = AddJobNameDialog(self)
        if dialog.exec():
            self.filter.clear()
            self.filter.addItem("All Jobnames")
            self.load_jobnames()

    def open_add_dialog(self):
        dialog = AddEmployeeDialog()
        if dialog.exec():
            self.load_data()

    def load_data(self):
        session = Session()
        query = session.query(Employee)

        selectedJob_id = self.filter.currentData()
        if selectedJob_id:
            query = query.filter(Employee.jobname_id == selectedJob_id)

        search = self.search.text().lower()
        if search:
            query = query.filter(or_(
                Employee.last_name.ilike(f"%{search}%")
            ))

        employees = query.all()
        self.table.setRowCount(len(employees))
        for row, e in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(e.last_name))
            self.table.setItem(row, 1, QTableWidgetItem(e.jobname.name))

    def load_jobnames(self):
        session = Session()
        jobnames = session.query(JobName).all()
        for j in jobnames:
            self.filter.addItem(j.name, j.id)
