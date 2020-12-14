import sys
import re

from UI.ui_win import Ui_Form
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox
from rsa_class import rsa_class


class MainWindow(QFrame, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setFixedSize(self.width(), self.height())

        self.rsa = rsa_class()
        self.rsa.Sig_auth.connect(self.close)
        self.rsa.start()

        self.pushButton.clicked.connect(self.run)

        self.var()

    def var(self):
        self.result_true = []
        self.result_false = []
        self.chinese_true = []
        self.chinese_false = []

    def close(self):
        QMessageBox.warning(self, '错误', '已过期')
        sys.exit(0)

    def run(self):
        if not self.textEdit.toPlainText() or not self.textEdit_2.toPlainText(): return
        self.var()
        text_list = [li.strip() for li in self.textEdit.toPlainText().split('\n') if li.strip()]  # type:list
        condition_list = [li.strip() for li in self.textEdit_2.toPlainText().split('\n') if li.strip()]  # type:list
        condition_list = map(self.condition_create, condition_list)  # type:list
        self.parser(text_list, condition_list)

    def condition_create(self, word):
        if word[0] == '*' and word[-1] == '*':
            return word.replace('*', '.*?')
        elif word[0] != '*' and word[-1] == '*':
            return '^' + word.replace('*', '.*?')
        elif word[0] == '*' and word[-1] != '*':
            return word.replace('*', '.*?') + '$'
        else:
            return '^' + word + '$'

    def condition_parser(self, word, condition_list):
        for c in condition_list:
            if re.search(c, word):
                return True
        return False

    def parser(self, text_list, condition_list):
        for word in text_list:
            if self.condition_parser(word, condition_list):
                self.result_true.append(word)
            else:
                self.result_false.append(word)
            if re.search('[\u4e00-\u9fa5]', word):
                self.chinese_true.append(word)
            else:
                self.chinese_false.append(word)
        self.textEdit_3.setText('\n'.join(self.result_true))
        self.textEdit_4.setText('\n'.join(self.result_false))
        self.textEdit_5.setText('\n'.join(self.chinese_true))
        self.textEdit_6.setText('\n'.join(self.chinese_false))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
