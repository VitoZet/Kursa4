# coding: utf-8
import pickle
import sys
import csv
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.uic import loadUi


class Gena(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.initSignal()

    def initUi(self):
        loadUi('kont_gen.ui', self)
        self.viewHistory()
        self.yd_descript1.setEnabled(False)
        self.yd_descript2.setEnabled(False)
        self.openHistoryPickle()

    def initSignal(self):
        # удаляем выбранный Pickle
        self.DeleteGroupButton.clicked.connect(self.DelSelectedPickle)
        # чистим папку с pickle
        self.ClearPushButton.clicked.connect(self.deletePickleFolder)
        # панель истории c группами объявлений, файлы pickle
        self.actionViewHistory.triggered.connect(self.viewHistory)
        self.listNameGroupWidget.clicked.connect(self.viewPickle)
        # Заполняем ключевые запросы и пересекаем их
        self.perese4.clicked.connect(self.showPerese4)
        # Записать в шаблон
        self.test_button.clicked.connect(self.SaveInCSV)
        # Записать в pickle
        self.NextButton.clicked.connect(self.savePickle)
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

    def GiveNamePickle(self):  # получаем имя выделленого Pickle
        selected = self.listNameGroupWidget.selectedItems()[0].text()
        return selected

    def DelSelectedPickle(self):  # удаляем выбранный Pickle и обновляем виджет
        os.remove('pickle_file/' + self.GiveNamePickle())
        self.listNameGroupWidget.clear()
        self.openHistoryPickle()

    def SaveInCSV(self):
        lst1_in_csv_ADW = ['adgroup;headline;description line 1;description line 2;final url']
        lst2_in_csv_ADW = ['keyword;adgroup']
        lst_in_csv_YD = ['Название группы;Фраза (с минус-словами);Заголовок;Текст;Ссылка']
        pickle_files = os.listdir('pickle_file/')
        for i in pickle_files:
            with open('pickle_file/' + i, 'rb') as f:
                pic_file = pickle.load(f)
            name_group = pic_file['name_group']
            adw_title1 = pic_file['adw_title1']
            adw_descript1 = pic_file['adw_descript1']
            adw_descript2 = pic_file['adw_descript2']
            url = pic_file['url']
            yd_title = pic_file['yd_title']
            yd_descript1 = pic_file['yd_descript1']
            yd_descript2 = pic_file['yd_descript2']
            yd_descript = yd_descript1 + ' '+ yd_descript2
            result_zapros = pic_file['result_zapros'].split('\n')

            # создаем лист1 для шаблон1 для Гугл Адвордс
            lst1_in_csv_ADW.append(
                name_group + ';' + adw_title1 + ';' + adw_descript1 + ';' + adw_descript2 + ';' +
                url)

            # создаем шаблон2 для Гугл Адвордс
            for key_adw2 in result_zapros:
                lst2_in_csv_ADW.append(key_adw2 + ';' + name_group)

            # создаем лист для Яндекс Директ
            for yd_key in result_zapros:
                lst_in_csv_YD.append(
                    name_group + ';' + yd_key + ';' + yd_title + ';' + yd_descript + ';' + url)

        # Записываем шаблон в Яндекс Директ
        with open('Yandex_DIRECT.csv', 'w', newline='') as csv_file_yd:
            csv_writer1 = csv.writer(csv_file_yd)
            for item in lst_in_csv_YD:
                csv_writer1.writerow([item])

        # Записываем шаблон 1 Гугл Адворос
        with open('Google_ADW_1.csv', 'w', newline='') as csv_file_adw1:
            csv_writer2 = csv.writer(csv_file_adw1)
            for item in lst1_in_csv_ADW:
                csv_writer2.writerow([item])

        # Записываем шаблон 2 Гугл Адворос
        with open('Google_ADW_2.csv', 'w', newline='') as csv_file_adw2:
            csv_writer3 = csv.writer(csv_file_adw2)
            for item in lst2_in_csv_ADW:
                csv_writer3.writerow([item])

    def deletePickleFolder(self, name):  # Чистим папку pickle
        pickle_files = os.listdir('pickle_file/')
        for i in pickle_files:
            os.remove('pickle_file/' + i)
        self.listNameGroupWidget.clear()

    def openHistoryPickle(self):  # Отображаем список групп объявлений в истории
        pickle_files = os.listdir('pickle_file/')
        self.listNameGroupWidget.addItems(pickle_files)

    def viewPickle(self, name):  # отображаем данные из файлов Pickle
        with open('pickle_file/' + self.GiveNamePickle(), 'rb') as f:
            pic_file = pickle.load(f)
            self.zapros_1.setText(pic_file['zapros_1'])
            self.zapros_2.setText(pic_file['zapros_2'])
            self.result_zapros.setText(pic_file['result_zapros'])
            self.yd_title.setText(pic_file['yd_title'])
            self.yd_descript1.setText(pic_file['yd_descript1'])
            self.yd_descript2.setText(pic_file['yd_descript2'])
            self.adw_title1.setText(pic_file['adw_title1'])
            self.adw_descript1.setText(pic_file['adw_descript1'])
            self.adw_descript2.setText(pic_file['adw_descript2'])
            self.name_group.setText(pic_file['name_group'])
            self.url.setText(pic_file['url'])

    def savePickle(self):  # сохраняем все введенные данные словарём в pickle
        vse_polja = {
            'zapros_1': self.zapros_1.toPlainText(),
            'zapros_2': self.zapros_2.toPlainText(),
            'result_zapros': self.result_zapros.toPlainText(),
            'yd_title': self.yd_title.text(),
            'yd_descript1': self.yd_descript1.text(),
            'yd_descript2': self.yd_descript2.text(),
            'adw_title1': self.adw_title1.text(),
            'adw_descript1': self.adw_descript1.text(),
            'adw_descript2': self.adw_descript2.text(),
            'name_group': self.name_group.text(),
            'url': self.url.text()
        }
        with open('pickle_file/' + self.name_group.text() + '.pickle', 'wb') as f:
            pickle.dump(vse_polja, f)
        # Очищаем Виджет с файлами пикл и добавляем заного с новым файлом
        self.listNameGroupWidget.clear()
        self.openHistoryPickle()

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
        max_title = 33
        len_title = len(self.yd_title.text())
        self.yd_len_title.setText(str(max_title - len_title))
        self.view_yd_title.setText(self.yd_title.text())  # выводим на визуализацию
        self.view_yd_title.adjustSize()
        self.yd_descript1.setMaxLength(56 - len(self.yd_title.text()))

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
        self.yd_descript2.setMaxLength(max_descript - advanced_title)

    def viewYdDescript2(self, text):  # выводим на визуализацию дискрипшен 2
        self.view_yd_descript2.setText(text)
        self.view_yd_descript2.adjustSize()

    def lenAdwTitle1(self, text):  # Вычисляем и показываем заголовок в ADWORDS
        max_title = 30
        len_adw_title1 = len(self.adw_title1.text())
        self.adw_len_title1.setText(str(max_title - len_adw_title1))

    def lenAdwTitle2(self, text):  # Вычисляем и показываем расширенный заголовок в ADWORDS
        max_title = 38
        len_adw_descript1 = len(self.adw_descript1.text())
        self.adw_len_title2.setText(str(max_title - len_adw_descript1))

    def viewAdwDescript(self, text):  # Вычисляем и показываем описание в ADWORDS
        max_title = 38
        len_adw_descript = len(self.adw_descript2.text())
        self.adw_len_descript.setText(str(max_title - len_adw_descript))
        self.view_adw_descript.setText(text)
        self.view_adw_descript.adjustSize()

    def viewHistory(self):  # Открываем панель с списком групп объявлений
        self.historyDockWidget.setVisible(self.actionViewHistory.isChecked())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gena = Gena()
    gena.show()
    sys.exit(app.exec_())
