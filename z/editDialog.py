from PySide6.QtWidgets import QDialog, QPushButton, QComboBox, QLineEdit, QVBoxLayout
from PySide6.QtGui import QIcon
from db import Session, Employee, JobName

class EditDialog(QDialog):
    def __init__(self, employee, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Employee")
        self.setMinimumSize(600, 700)
        self.setWindowIcon(QIcon("./logo.svg"))
        self.employee = employee  # сохраняем переданного сотрудника

        layout = QVBoxLayout()

        self.last_name_i = QLineEdit()
        self.name_i = QLineEdit()
        self.middlename_i = QLineEdit()
        self.jobname_c = QComboBox()

        # Загрузка должностей
        session = Session()
        self.jobs = session.query(JobName).all()
        for job in self.jobs:
            self.jobname_c.addItem(job.name, job.id)

        # Установка текущих данных сотрудника
        self.last_name_i.setText(employee.last_name)
        self.name_i.setText(employee.name)
        self.middlename_i.setText(employee.middlename)
        self.jobname_c.setCurrentIndex(self.jobname_c.findData(employee.jobname_id))

        # Кнопки
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_data)
        self.btn_close = QPushButton("Cancel")
        self.btn_close.clicked.connect(self.reject)

        # Добавление в layout
        for widget in [
            self.last_name_i, self.name_i, self.middlename_i,
            self.jobname_c, self.btn_save, self.btn_close
        ]:
            layout.addWidget(widget)

        self.setLayout(layout)

    def save_data(self):
        session = Session()
        emp = session.query(Employee).get(self.employee.id)
        emp.last_name = self.last_name_i.text()
        emp.name = self.name_i.text()
        emp.middlename = self.middlename_i.text()
        emp.jobname_id = self.jobname_c.currentData()
        session.commit()
        self.accept()
