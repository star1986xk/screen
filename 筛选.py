import sys
import re
import chardet

from UI.ui_win import Ui_Form
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QFileDialog
from rsa_class import rsa_class
from mylogclass import MyLogClass


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
        self.pushButton_condition_2.clicked.connect(self.run_condition_2)
        self.pushButton_chinese_2.clicked.connect(self.run_chinese_2)
        self.pushButton_txt.clicked.connect(self.intxt)

        self.datas = []
        self.var_1()
        self.var_2()

        self.mylog = MyLogClass()

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

    def intxt(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, '选取文件', './', '文本文件 (*.txt)')
            data = self.read(filename)
            self.datas = [d.strip().lower() for d in data.split('\n') if d.strip()]
            self.label.setText(str(len(self.datas)))
        except Exception as e:
            pass

    def run_condition(self):
        if not self.textEdit.toPlainText() or not self.textEdit_2.toPlainText(): return
        self.var_1()
        text_list = [li.strip().lower() for li in self.textEdit.toPlainText().split('\n') if li.strip()]  # type:list
        condition_list = [li.strip().lower() for li in self.textEdit_2.toPlainText().split('\n') if
                          li.strip()]  # type:list
        self.parser_condition(text_list, condition_list, 1)

    def run_condition_2(self):
        try:
            if not self.datas or not self.textEdit_2.toPlainText(): return
            self.var_1()
            condition_list = [li.strip().lower() for li in self.textEdit_2.toPlainText().split('\n') if
                              li.strip()]  # type:list
            self.parser_condition(self.datas, condition_list, 0)
        except Exception as e:
            self.mylog.logger.warning('run_condition_2:' + str(e))

    def run_chinese(self):
        if not self.textEdit.toPlainText(): return
        self.var_2()
        text_list = [li.strip() for li in self.textEdit.toPlainText().split('\n') if li.strip()]  # type:list
        self.parser_chinese(text_list, 1)

    def run_chinese_2(self):
        if not self.datas: return
        self.var_2()
        self.parser_chinese(self.datas, 0)

    def condition_parser(self, word, condition_list):
        for c in condition_list:
            if self.radioButton_in.isChecked() and c in word:
                return c
            elif self.radioButton_start.isChecked() and len(word) >= len(c) and c == word[:len(c)]:
                return c
            elif self.radioButton_end.isChecked() and len(word) >= len(c) and c == word[-len(c):]:
                return c
            elif self.radioButton_be.isChecked() and word == c:
                return  c
        return None

    def parser_condition(self, text_list, condition_list, tpye):
        try:
            for word in text_list:
                c = self.condition_parser(word, condition_list)
                if c:
                    self.result_true.append([word, c])
                    if self.checkBox.isChecked():
                        self.textBrowser.append(word + '---' + c)
                else:
                    self.result_false.append(word)
            if tpye:
                self.textEdit_3.setText('\n'.join([li[0] for li in self.result_true]))
                self.textEdit_4.setText('\n'.join(self.result_false))
            else:
                self.out_txt('./符合结果.txt', [li[0] for li in self.result_true])
                self.out_txt('./不符合结果.txt', self.result_false)
            QMessageBox.information(self, '提示', '完成')
        except Exception as e:
            self.mylog.logger.warning('parser_condition:' + str(e))

    # 导出
    def out_txt(self, filename, txt_list):
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(txt_list))
        except Exception as e:
            self.mylog.logger.warning('out_txt:' + str(e))

    # 检测编码格式，读取内容
    def read(self, path):
        with open(path, 'rb') as f:
            text = f.read()
        encode = chardet.detect(text).get('encoding')
        with open(path, 'r', encoding=encode) as f:
            text = f.read()
        return text

    def parser_chinese(self, text_list, type):
        for word in text_list:
            if re.search('[\u4e00-\u9fa5]', word):
                self.chinese_true.append(word)
            else:
                self.chinese_false.append(word)
        if type:
            self.textEdit_5.setText('\n'.join(self.chinese_true))
            self.textEdit_6.setText('\n'.join(self.chinese_false))
        else:
            self.out_txt('./含汉字.txt', self.chinese_true)
            self.out_txt('./不含汉字.txt', self.chinese_false)
        QMessageBox.information(self, '提示', '完成')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
