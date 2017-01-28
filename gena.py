# coding: utf-8

import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QVBoxLayout, QLineEdit)
from PyQt5.uic import loadUi


class Gena(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.initSignal()

    def initUi(self):
        loadUi('kont_gen.ui', self)
        self.yd_descript1.setEnabled(False)
        self.yd_descript2.setEnabled(False)

    def initSignal(self):
        # Заполняем ключевые запросы и пересекаем и
        self.perese4.clicked.connect(self.show_perese4)
        # self.zapros_1.textChanged.connect(self.zapros_to_lst)
        # self.zapros_2.textChanged.connect(self.zapros_to_lst)
        # Редактирование объявлений Яндекс.Директ
        self.yd_title.textChanged.connect(self.def_yd_len_title)
        self.yd_title.textChanged.connect(self.def_yd_descript1_on)
        self.yd_title.textChanged.connect(self.def_yd_len_descript1)
        self.yd_descript1.textChanged.connect(self.def_yd_descript2_on)
        self.yd_descript1.textChanged.connect(self.def_yd_len_descript2)
        self.yd_descript1.textChanged.connect(self.def_yd_len_descript1)
        self.yd_descript2.textChanged.connect(self.def_yd_len_descript2)
        self.yd_descript2.textChanged.connect(self.def_view_yd_descript2)
        self.yd_title.textChanged.connect(self.def_view_yd_title)
        self.yd_descript1.textChanged.connect(self.def_view_yd_title)
        # Редактирование объявлений Google.Adwords
        self.adw_title1.textChanged.connect(self.def_adw_len_title1)
        self.adw_title2.textChanged.connect(self.def_adw_len_title2)
        self.adw_descript.textChanged.connect(self.def_adw_descript)
        self.adw_title1.textChanged.connect(self.def_view_adw_title)
        self.adw_title2.textChanged.connect(self.def_view_adw_title)

    def show_perese4(self):
        stroka = ''
        zapros3 = self.zapros_to_lst()
        for i in zapros3:
            stroka += i + '\n'
        self.result_zapros.setPlainText(stroka)




    def zapros_to_lst(self):  # сохраняем в списки
        zapros1 = self.zapros_1.toPlainText().split('\n')
        zapros2 = self.zapros_2.toPlainText().split('\n')
        result_zapros = [a + ' ' + b for a in zapros1 for b in zapros2]
        return result_zapros

    def def_view_yd_title(self, text):  # Визуализация Заголовка ДИРЕКТ
        stroka = ''
        if len(self.yd_title.text()) > 0:
            stroka += self.yd_title.text()
        if len(self.yd_descript1.text()) > 0:
            stroka += ' - '
            stroka += self.yd_descript1.text()
        self.view_yd_title.setText(stroka)
        self.view_yd_title.adjustSize()

    def def_view_adw_title(self, text):  # Визуализация Заголовка ADWORDS
        stroka = ''
        if len(self.adw_title1.text()) > 0:
            stroka += self.adw_title1.text()
        if len(self.adw_title2.text()) > 0:
            stroka += ' - '
            stroka += self.adw_title2.text()
        self.view_adw_title.setText(stroka)
        self.view_adw_title.adjustSize()
        # self.label_5.setText(self.adw_title1.text() + ' - ' + self.adw_title2.text()) - альтернативный способ, но "-" остается

    def def_yd_len_title(self, text):  # Замеряем длину заголовка Директ
        max_title = 33
        len_title = len(self.yd_title.text())
        self.yd_len_title.setText(str(max_title - len_title))
        self.view_yd_title.setText(text)  # выводим на визуализацию
        self.view_yd_title.adjustSize()

    def def_yd_descript1_on(
            self):  # Включаем возможность ввода текста в расширенный заголовок, когда известна длина основного загоовка
        len_title = len(self.yd_title.text())
        if len_title > 0:
            self.yd_descript1.setEnabled(True)
        else:
            self.yd_descript1.setEnabled(False)

    def def_yd_descript2_on(self,
                            text):  # Включаем возможность ввода текста, когда известна, длина расширенного заголовка.
        len_descript1 = len(self.yd_descript1.text())
        if len_descript1 > 0:
            self.yd_descript2.setEnabled(True)
        else:
            self.yd_descript2.setEnabled(False)

    def def_yd_len_descript1(self):  # Вычисляем и показываем возможную длину для расширенного заголовка
        advanced_title = 56
        len_title = len(self.yd_title.text())
        len_descript1 = len(self.yd_descript1.text())
        advanced_descript1 = advanced_title - len_title
        self.yd_len_descript1.setText(str(advanced_descript1))
        self.yd_len_descript1.setText(str(advanced_descript1 - len_descript1))

    def def_yd_len_descript2(
            self):  # Вычисляем возможную длину описания, когда уже известна длина расширенного заголовка.
        max_descript = 75
        advanced_title = len(self.yd_descript1.text())
        len_descript2 = max_descript - advanced_title - len(self.yd_descript2.text())
        self.yd_len_descript2.setText(str(len_descript2))

    def def_view_yd_descript2(self, text):  # выводим на визуализацию дискрипшен 2
        self.view_yd_descript2.setText(text)
        self.view_yd_descript2.adjustSize()

    def def_adw_len_title1(self, text):  # Вычисляем и показываем заголовок в ADWORDS
        max_title = 30
        len_adw_title1 = len(self.adw_title1.text())
        self.adw_len_title1.setText(str(max_title - len_adw_title1))

    def def_adw_len_title2(self, text):  # Вычисляем и показываем расширенный заголовок в ADWORDS
        max_title = 30
        len_adw_title2 = len(self.adw_title2.text())
        self.adw_len_title2.setText(str(max_title - len_adw_title2))

    def def_adw_descript(self, text):  # Вычисляем и показываем описание в ADWORDS
        max_title = 80
        len_adw_descript = len(self.adw_descript.text())
        self.adw_len_descript.setText(str(max_title - len_adw_descript))
        self.view_adw_descript.setText(text)
        self.view_adw_descript.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gena = Gena()
    gena.show()
    sys.exit(app.exec_())
