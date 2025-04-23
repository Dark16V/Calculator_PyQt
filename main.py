import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.setWindowIcon(QIcon('images/icon.ico'))

        self.list = []
        self.min_list = []
        self.after_equals = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(50)
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedHeight(50)
            button.clicked.connect(self.the_button_was_clicked)
            self.grid_layout.addWidget(button, row, col)
            if text == '=':
                button.setStyleSheet("background-color: orange")
            elif text == 'C':
                button.setStyleSheet("background-color: red")
                self.grid_layout.addWidget(button, row, col, 1, 4)

    def the_button_was_clicked(self):
        button = self.sender()
        text = button.text()
        current_text = self.display.text()

        if text == '=':
            if self.min_list:
                num = ''
                for i in self.min_list:
                    num += i

                num = int(num)
                self.list.append(num)
                self.min_list = []
            else:
                self.list.pop()

            if '*' in self.list: 
                self.multiplication_division('*')

            if '/' in self.list:
                self.multiplication_division('/')
        
            while len(self.list) != 1:
                if self.list[1] == '+':
                    self.plus_minus('+')

                elif self.list[1] == '-':
                    self.plus_minus('-')
                    
            self.display.setText(str(self.list[0]))
            self.list = []
            self.min_list = []
            self.after_equals = True

        elif text == 'C':
            self.display.setText("")
            self.list = []
            self.min_list = []
        else:
            if self.after_equals:
                self.display.setText("")
                self.after_equals = False

            button = self.sender()
            text = button.text()
            current_text = self.display.text()

            if text in ['-', '+', '*', '/']:
                if self.min_list:
                    num = ''
                    for i in self.min_list:
                        num += i
                    num = int(num)
                    self.list.append(num)
                    self.list.append(text)
                    self.display.setText(current_text + text)
                    self.min_list = []
                else:
                    current_text = self.display.text()
                    self.list[-1] = text
                    temp = list(current_text)
                    temp[-1] = text
                    new_current_text = "".join(temp)
                    self.display.setText(new_current_text)
            else:
                self.min_list.append(text)
                self.display.setText(current_text + text)



    def multiplication_division(self, sign: str):
        while sign in self.list:
            i = self.list.index(sign)
            if sign == '*':
                    result = self.list[i-1] * self.list[i+1]
            else:
                if self.list[i+1] == 0:
                    result = 'Error: division by zero'
                else:
                    result = self.list[i-1] / self.list[i+1]

            if result != 'Error: division by zero':
                self.list[i-1] = result
                self.list.pop(i)
                self.list.pop(i)
            else:
                self.list = ['Error: division by zero']

    def plus_minus(self, sign: str):
        if sign == '+':
            result = self.list[0] + self.list[2]
        else:
            result = self.list[0] - self.list[2]

        self.list[0] = result
        self.list.pop(1)
        self.list.pop(1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
