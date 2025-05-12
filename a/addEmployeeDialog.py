from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QDateEdit
from PySide6.QtCore import QDate
from db import Session, Company, JobName, Document, Address, Employee

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника")

        layout = QVBoxLayout()

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Фамилия")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Отчество")

        self.series_input = QLineEdit()
        self.series_input.setPlaceholderText("Серия паспорта")
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Номер паспорта")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Адрес проживания")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.company_input = QComboBox()
        self.jobname_input = QComboBox()

        session = Session()
        for c in session.query(Company).all():
            self.company_input.addItem(c.name, c.id)
        for j in session.query(JobName).all():
            self.jobname_input.addItem(j.name, j.id)

        widgets = [
            self.last_name_input, self.name_input, self.middle_name_input,
            self.series_input, self.number_input, self.address_input,
            self.phone_input, self.email_input, self.start_date_input,
            self.company_input, self.jobname_input
        ]
        for w in widgets:
            layout.addWidget(w)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        save_btn.clicked.connect(self.save_employee)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_employee(self):
        session = Session()

        document = Document(series=self.series_input.text(), number=self.number_input.text())
        session.add(document)
        session.commit()

        address = Address(address=self.address_input.text())
        session.add(address)
        session.commit()

        employee = Employee(
            last_name=self.last_name_input.text(),
            name=self.name_input.text(),
            middlename=self.middle_name_input.text(),
            document_id=document.id,
            address_id=address.id,
            phone=self.phone_input.text(),
            email=self.email_input.text(),
            start_date=self.start_date_input.date().toPython(),
            company_id=self.company_input.currentData(),
            jobname_id=self.jobname_input.currentData()
        )
        session.add(employee)
        session.commit()
        self.accept()
