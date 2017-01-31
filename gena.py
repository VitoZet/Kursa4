# coding: utf-8

import sys
import csv

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
        # Заполняем ключевые запросы и пересекаем их
        self.perese4.clicked.connect(self.showPerese4)
        self.test_button.clicked.connect(self.csvYD)  # Записать в шаблон
        # Редактирование объявлений Яндекс.Директ
        self.yd_title.textChanged.connect(self.lenYdTitle)
        self.yd_title.textChanged.connect(self.onYdDescript1)
        self.yd_title.textChanged.connect(self.lenYdDescript1)
        self.yd_descript1.textChanged.connect(self.onYdDescript2)
        self.yd_descript1.textChanged.connect(self.lenYdDescript2)
        self.yd_descript1.textChanged.connect(self.lenYdDescript1)
        self.yd_descript2.textChanged.connect(self.lenYdDescript2)
        self.yd_descript2.textChanged.connect(self.viewYdDescript2)
        self.yd_title.textChanged.connect(self.viewYdTitle)
        self.yd_descript1.textChanged.connect(self.viewYdTitle)
        # Редактирование объявлений Google.Adwords
        self.adw_title1.textChanged.connect(self.lenAdwTitle1)
        self.adw_descript1.textChanged.connect(self.lenAdwTitle2)
        self.adw_descript2.textChanged.connect(self.viewAdwDescript)
        self.adw_title1.textChanged.connect(self.viewAdwTitle)
        self.adw_descript1.textChanged.connect(self.viewAdwTitle)

    def csvYD(self):  # соеденяем списки и записываем в csv
        # переменные для шаблона Яндекс.Директ
        lst_in_csv_YD = ['Название группы;Фраза (с минус-словами);Заголовок;Текст;Ссылка']
        csv_yd_title = self.lenYdTitle()
        csv_key = self.zapros_to_lst()
        csv_yd_descript = [self.yd_descript1.text() + ' ' + self.yd_descript2.text()]
        # переменные для шаблона Google.Adwords
        lst1_in_csv_ADW = ['adgroup;headline;description line 1;description line 2;final url']
        lst2_in_csv_ADW = ['keyword;adgroup']
        csv_ADW_title = [self.adw_title1.text()]
        csv_ADW_descript1 = [self.adw_descript1.text()]
        csv_ADW_descript2 = [self.adw_descript2.text()]
        # общие переменные
        csv_name_group = [self.name_group.text()]
        csv_url = [self.url.text()]

        #Создаем списки Google.Adwords для двух отдельных шаблонов
        lst1_in_csv_ADW.append(csv_name_group[0] + ';' + csv_ADW_title[0] + ';' + csv_ADW_descript1[0] + ';' + csv_ADW_descript2[0] + ';' + csv_url[0])
        for adw_key in csv_key:
            lst2_in_csv_ADW.append(adw_key + ';' + csv_name_group[0])

        # создаем Яндекс.Директ список и записываем в CSV
        for yd_key in csv_key:
            lst_in_csv_YD.append(
                csv_name_group[0] + ';' + yd_key + ';' + csv_yd_title[0] + ';' + csv_yd_descript[0] + ';' + csv_url[0])

        # Записываем Яндекс.Шаблон
        with open('Yandex_DIRECT.csv', 'w', newline='') as csv_file_yd:
            csv_writer1 = csv.writer(csv_file_yd)
            for item in lst_in_csv_YD:
                csv_writer1.writerow([item])

        # Записываем Adwords Шаблон
        with open('Google_ADW_1.csv', 'w', newline='') as csv_file_adw1:
            csv_writer2 = csv.writer(csv_file_adw1)
            for item in lst1_in_csv_ADW:
                csv_writer2.writerow([item])
        # Записываем Adwords Шаблон2
        with open('Google_ADW_2.csv', 'w', newline='') as csv_file_adw2:
            csv_writer3 = csv.writer(csv_file_adw2)
            for item in lst2_in_csv_ADW:
                csv_writer3.writerow([item])

    def showPerese4(self):  # показываем пересеченные запросы
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

    def viewYdTitle(self, text):  # Визуализация Заголовка ДИРЕКТ
        stroka = ''
        if len(self.yd_title.text()) > 0:
            stroka += self.yd_title.text()
        if len(self.yd_descript1.text()) > 0:
            stroka += ' - '
            stroka += self.yd_descript1.text()
        self.view_yd_title.setText(stroka)
        self.view_yd_title.adjustSize()

    def viewAdwTitle(self, text):  # Визуализация Заголовка ADWORDS
        stroka = ''
        if len(self.adw_title1.text()) > 0:
            stroka += self.adw_title1.text()
        if len(self.adw_descript1.text()) > 0:
            stroka += ' - '
            stroka += self.adw_descript1.text()
        self.view_adw_title.setText(stroka)
        self.view_adw_title.adjustSize()
        # self.label_5.setText(self.adw_title1.text() + ' - ' + self.adw_descript1.text()) - альтернативный способ, но "-" остается

    def lenYdTitle(self):  # Замеряем длину заголовка Директ
        csv_title = [self.yd_title.text()]  # для записи в CSV
        max_title = 33
        len_title = len(self.yd_title.text())
        self.yd_len_title.setText(str(max_title - len_title))
        self.view_yd_title.setText(self.yd_title.text())  # выводим на визуализацию
        self.view_yd_title.adjustSize()
        # print(csv_title)
        return csv_title

    def onYdDescript1(
            self):  # Включаем возможность ввода текста в расширенный заголовок, когда известна длина основного загоовка
        len_title = len(self.yd_title.text())
        if len_title > 0:
            self.yd_descript1.setEnabled(True)
        else:
            self.yd_descript1.setEnabled(False)

    def onYdDescript2(self,
                            text):  # Включаем возможность ввода текста, когда известна, длина расширенного заголовка.
        len_descript1 = len(self.yd_descript1.text())
        if len_descript1 > 0:
            self.yd_descript2.setEnabled(True)
        else:
            self.yd_descript2.setEnabled(False)

    def lenYdDescript1(self):  # Вычисляем и показываем возможную длину для расширенного заголовка
        advanced_title = 56
        len_title = len(self.yd_title.text())
        len_descript1 = len(self.yd_descript1.text())
        advanced_descript1 = advanced_title - len_title
        self.yd_len_descript1.setText(str(advanced_descript1))
        self.yd_len_descript1.setText(str(advanced_descript1 - len_descript1))

    def lenYdDescript2(
            self):  # Вычисляем возможную длину описания, когда уже известна длина расширенного заголовка.
        max_descript = 75
        advanced_title = len(self.yd_descript1.text())
        len_descript2 = max_descript - advanced_title - len(self.yd_descript2.text())
        self.yd_len_descript2.setText(str(len_descript2))

    def viewYdDescript2(self, text):  # выводим на визуализацию дискрипшен 2
        self.view_yd_descript2.setText(text)
        self.view_yd_descript2.adjustSize()

    def lenAdwTitle1(self, text):  # Вычисляем и показываем заголовок в ADWORDS
        max_title = 30
        len_adw_title1 = len(self.adw_title1.text())
        self.adw_len_title1.setText(str(max_title - len_adw_title1))

    def lenAdwTitle2(self, text):  # Вычисляем и показываем расширенный заголовок в ADWORDS
        max_title = 30
        len_adw_descript1 = len(self.adw_descript1.text())
        self.adw_len_title2.setText(str(max_title - len_adw_descript1))

    def viewAdwDescript(self, text):  # Вычисляем и показываем описание в ADWORDS
        max_title = 80
        len_adw_descript = len(self.adw_descript2.text())
        self.adw_len_descript.setText(str(max_title - len_adw_descript))
        self.view_adw_descript.setText(text)
        self.view_adw_descript.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gena = Gena()
    gena.show()
    sys.exit(app.exec_())
