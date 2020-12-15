import sys
import re

from UI.ui_win import Ui_Form
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QTableWidgetItem
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

        self.pushButton_condition.clicked.connect(self.run_condition)
        self.pushButton_chinese.clicked.connect(self.run_chinese)

        self.var_1()
        self.var_2()

    def var_1(self):
        self.textBrowser.clear()
        self.result_true = []
        self.result_false = []

    def var_2(self):
        self.chinese_true = []
        self.chinese_false = []

    def close(self):
        QMessageBox.warning(self, '错误', '已过期')
        sys.exit(0)

    def run_condition(self):
        if not self.textEdit.toPlainText() or not self.textEdit_2.toPlainText(): return
        self.var_1()
        text_list = [li.strip() for li in self.textEdit.toPlainText().split('\n') if li.strip()]  # type:list
        condition_list = [li.strip() for li in self.textEdit_2.toPlainText().split('\n') if li.strip()]  # type:list
        condition_list = list(map(self.condition_create, condition_list))  # type:list
        self.parser_condition(text_list, condition_list)

    def run_chinese(self):
        if not self.textEdit.toPlainText(): return
        self.var_2()
        text_list = [li.strip() for li in self.textEdit.toPlainText().split('\n') if li.strip()]  # type:list
        self.parser_chinese(text_list)

    def condition_create(self, word):
        if self.radioButton_in.isChecked():
            condition = '.*?' + word + '.*?'
        elif self.radioButton_start.isChecked():
            condition = '^' + word + '.*?'
        elif self.radioButton_end.isChecked():
            condition = '.*?' + word + '$'
        else:
            condition = '^' + word + '$'
        return condition, word

    def condition_parser(self, word, condition_list):
        for c, w in condition_list:
            if re.search(c, word):
                return w
        return None

    def parser_condition(self, text_list, condition_list):
        for word in text_list:
            c = self.condition_parser(word, condition_list)
            if c:
                self.result_true.append([word,c])
                if self.checkBox.isChecked():
                    self.textBrowser.append(word+'---'+c)
            else:
                self.result_false.append(word)
        self.textEdit_3.setText('\n'.join([li[0] for li in self.result_true]))
        self.textEdit_4.setText('\n'.join(self.result_false))

    def parser_chinese(self, text_list):
        for word in text_list:
            if re.search('[\u4e00-\u9fa5]', word):
                self.chinese_true.append(word)
            else:
                self.chinese_false.append(word)
        self.textEdit_5.setText('\n'.join(self.chinese_true))
        self.textEdit_6.setText('\n'.join(self.chinese_false))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
