from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from db import Session, JobName, Employee

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add")
        self.setMinimumSize(300, 350)
        self.setWindowIcon(QIcon("./logo.svg"))

        layout = QVBoxLayout()

        self.name_i = QLineEdit(placeholderText="name")
        self.last_name_i = QLineEdit(placeholderText="last name")
        self.middle_name_i = QLineEdit(placeholderText="middle name")
        self.jobname_c = QComboBox()
        session = Session()
        for job in session.query(JobName).all():
            self.jobname_c.addItem(job.name, job.id)

        widgets = [self.name_i, self.last_name_i, self.middle_name_i, self.jobname_c]
        for w in widgets:
            layout.addWidget(w)

        btn_layout = QVBoxLayout()
        self.btn_save = QPushButton("save")
        self.btn_save.clicked.connect(self.save_data)
        self.btn_cancel = QPushButton("cancel")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def save_data(self):
        session = Session()
        employee = Employee(
            name = self.name_i.text(),
            last_name = self.last_name_i.text(),
            middlename = self.middle_name_i.text(),
            jobname_id = self.jobname_c.currentData()
        )

        session.add(employee)
        session.commit()
        self.accept()


        
        
