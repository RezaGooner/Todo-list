import sys
import os
import threading
from datetime import datetime, timedelta
from plyer import notification
import random
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QAbstractItemView,
    QListWidgetItem,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QDateTimeEdit,
    QDialog,
    QComboBox, 
    QMessageBox
    )

from PyQt6.QtGui import (
    QIcon,
    QCursor,
    QFont ,
    QColor
    )
from PyQt6.QtCore import (
    QSize ,
    QTime ,
    Qt ,
    QDateTime ,
    QTimer
    )




listFont = QFont("forte", 13)


EnMainFontSize = 12
EnFont1 =  QFont("Georgia", EnMainFontSize)

EnDateTimeFontSize = 16
EnFont2 =  QFont("Georgia", EnDateTimeFontSize)

FaMainFontSize = 12
FaFont1 =  QFont("B Homa", EnMainFontSize)

FaDateTimeFontSize = 16
FaFont2 =  QFont("B Homa", EnDateTimeFontSize)

loadFile = "load.txt"
langFile = "Language/Lang.txt"

changeLanIcon = 'icons/changeLan.png'
deleteIcon = 'icons/trash.png'
saveIcon = 'icons/save.png'
editIcon = 'icons/edit.png'
loadIcon = 'icons/spreadsheet.png'
exitIcon = 'icons/exit.png'
newIcon = "icons/new.png"
icon = 'icons/icon.png'


lines = []


with open(langFile, 'r', encoding='utf-8') as file:
    line = file.readline()

    if line == "En" :
        tempFile = "Language/English.txt"
        mainFont , dateTimeFont = EnFont1 , EnFont2
    elif line == "Fa" :
        tempFile = "Language/Persian.txt"
        mainFont , dateTimeFont = FaFont1 ,  FaFont2
        
    with open(tempFile, 'r', encoding='utf-8') as file:
        global successMessage, removeSuccess, deleteMessage, remindTitle, addMessage, saveMessage
        global loadTitle, loadMessage, loadErrorTitle, loadErrorMessage, editSuccess
        global editWord, textWord, dateWord, timeWord, okWord, cancelWord, todoWord
        global placeHolderWord, addWord, deleteWord, saveWord, loadWord, clearAllWord, setTimeWord

        lines = file.readlines()

        successMessage = lines[0].strip()
        removeSuccess = lines[1].strip()
        deleteMessage = lines[2].strip()
        remindTitle = lines[3].strip()
        addMessage = lines[4].strip()
        saveMessage = lines[5].strip()
        loadTitle = lines[6].strip()
        loadMessage = lines[7].strip()
        loadErrorTitle = lines[8].strip()
        loadErrorMessage = lines[9].strip()
        editSuccess = lines[10].strip()

        editWord = lines[11].strip()
        textWord = lines[12].strip()
        dateWord = lines[13].strip()
        timeWord = lines[14].strip()
        okWord = lines[15].strip()
        cancelWord = lines[16].strip()
        todoWord = lines[17].strip()
        placeHolderWord = lines[18].strip()
        addWord = lines[19].strip()
        deleteWord = lines[20].strip()
        saveWord = lines[21].strip()
        loadWord = lines[22].strip()
        clearAllWord = lines[23].strip()
        setTimeWord = lines[24].strip()
        changeLanWord = lines[25].strip()
        exitWord = lines[26].strip()
        clearAllToolTip = lines[27].strip()
        setTimeToolTip = lines[28].strip()
        selectLanWord = lines[29].strip()
            




class LanguageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(changeLanIcon))
        self.setWindowTitle(changeLanWord)
        self.comboBox = QComboBox()
        self.comboBox.addItem("English")
        self.comboBox.addItem("فارسی")

        label = QLabel(selectLanWord)
        button = QPushButton(okWord)
        button.setStyleSheet('color: black;')
        button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.comboBox)
        layout.addWidget(button)

        self.setLayout(layout)

    def get_selected_language(self):
        return self.comboBox.currentText()

    


def changeLan():
    language_dialog = LanguageDialog()
    result = language_dialog.exec()

    if result == QDialog.DialogCode.Accepted:
        selected_language = language_dialog.get_selected_language()
        if selected_language == "English":
            with open(langFile, "w", encoding='utf-8') as file:
                file.write("En")
            pass
        elif selected_language == "فارسی":
            with open(langFile, "w", encoding='utf-8') as file:
                file.write("Fa")
            pass


def setListWidgetFont():
    for index in range(list_widget.count()):
        item = list_widget.item(index)
        item.setFont(listFont)
        


def clearAllTask():
    list_widget.clear()
    textbox.clear()
    date_edit.clear()
    time_edit.clear()

    with open(loadFile, "w" , encoding='utf-8') as new_file:
        new_file.write('')

    showNotification(successMessage , removeSuccess)


def showNotification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10,
    )

def setNotification(hour, minute, message, date_edit):
    current_datetime = datetime.now()
    target_datetime = date_edit.dateTime().toPyDateTime()
    target_datetime = target_datetime.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if current_datetime > target_datetime:
        target_datetime = target_datetime + timedelta(days=1)
    time_difference = (target_datetime - current_datetime).total_seconds()
    timer = threading.Timer(time_difference, showNotification, args=(remindTitle, message))
    timer.start()


def removeIcon(item):
    item.setIcon(QIcon())
    
    
def addTask():
    task_text = textbox.text()
    date_text = date_edit.date().toString("yyyy-MM-dd")
    time_text = time_edit.time().toString("HH:mm")

    if task_text != "":
        task = f"{task_text} \n {date_text} - {time_text}"

        list_widget.insertItem(0, task)
        item = list_widget.item(0)

        item.setFont(listFont)

        item_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        item.setForeground(item_color)

        item.setIcon(QIcon(newIcon))

        newLabelTimer = QTimer()
        newLabelTimer.timeout.connect(lambda: removeIcon(item))
        newLabelTimer.start(150000) #2.5 min
        
        textbox.clear()
        date_edit.clear()
        time_edit.clear()

        time = QTime.fromString(time_text, "HH:mm")
        setNotification(time.hour(), time.minute(), task_text, date_edit)

        showNotification(successMessage, addMessage)

        setListWidgetFont()

        list_widget.setCurrentRow(0)
      


def deleteTask():
    if list_widget.selectedItems():
        for i in list_widget.selectedItems():
            task_index = list_widget.row(i)
            print(list_widget.item(task_index).text())
            list_widget.takeItem(task_index)

        showNotification(successMessage , deleteMessage )


def saveTask():
    if list_widget.selectedItems():
        with open(loadFile, "a+", encoding='utf-8') as file:
            for i in reversed(list_widget.selectedItems()):
                task_index = list_widget.row(i)
                task_text = list_widget.item(task_index).text()

                task_text = task_text
                task_text = task_text.replace('\n', '$$')
                file.write(task_text + '\n')

        showNotification(successMessage,saveMessage)


def loadTask():
    try:
        if os.stat(loadFile).st_size != 0:
            list_widget.clear()
            with open(loadFile, "r", encoding='utf-8') as file:
                for i in file.readlines():
                    i = i.replace('$$', '\n').strip()
                    item = QListWidgetItem(i)
                    item_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    item.setForeground(item_color)
                    list_widget.addItem(item)

            showNotification(loadTitle, loadMessage)

        setListWidgetFont()
    except Exception as e:
        print(f"An error occurred while loading tasks: {e}")
        showNotification(loadErrorTitle, loadErrorMessage)


class EditDialog(QDialog):
    def __init__(self, initial_text, parent=None):
        super().__init__(parent)

        self.setFixedSize(400, 500)

        self.setWindowTitle(editWord)
        self.setWindowIcon(QIcon(editIcon))
        layout = QVBoxLayout()

        self.label_text = QLabel(textWord)
        self.text_edit = QLineEdit()
        self.text_edit.setText(initial_text)

        self.label_date = QLabel(dateWord)
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setDateTime(QDateTime.currentDateTime())

        self.label_time = QLabel(timeWord)
        self.time_edit = QDateTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setDateTime(QDateTime.currentDateTime())

        self.ok_button = QPushButton(okWord)
        self.ok_button.setStyleSheet('color: black;')
        self.cancel_button = QPushButton(cancelWord)
        self.cancel_button.setStyleSheet('color: black;')


        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.label_text)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.label_date)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.label_time)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_new_text(self):
        return self.text_edit.text()

    def get_new_date(self):
        return self.date_edit.dateTime().toString("yyyy-MM-dd")

    def get_new_time(self):
        return self.time_edit.dateTime().toString("HH:mm")


def editTask():
    selected_items = list_widget.selectedItems()
    if selected_items:
        selected_item = selected_items[0]
        initial_text = selected_item.text()

        edit_dialog = EditDialog(initial_text.split("\n")[0])

        if edit_dialog.exec() == QDialog.DialogCode.Accepted:
            new_text = edit_dialog.get_new_text()
            new_date = edit_dialog.get_new_date()
            new_time = edit_dialog.get_new_time()
            selected_index = list_widget.row(selected_item)

            updated_text = f"{new_text} \n {new_date} - {new_time}"
            updateTask(selected_item, updated_text, selected_index)
            showNotification(successMessage, editSuccess)
            


def updateTask(item, new_text, selected_index):
    item.setText(new_text)

    list_widget.item(selected_index).setText(new_text)


def setCurrentDateTime():
    current_datetime = QDateTime.currentDateTime()
    date_edit.setDateTime(current_datetime)
    time_edit.setDateTime(current_datetime)

def stopApplication():
    msg_box = QMessageBox()
    msg_box.setWindowTitle(exitWord)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setText(f"{exitWord}؟")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.No)
    
    result = msg_box.exec()

    if result == QMessageBox.StandardButton.Yes:    
        global isEnd
        isEnd = False
        app.quit()



app = QApplication(sys.argv)
app.setFont(mainFont)


app.setStyleSheet('''
    *{
        background-color:        #ffffff;
    }

    #header{
       font-size:               30px; 
       color:                   #787c80;
       margin:                  0px  5px;
    }

    QListWidget{
        background-color:       rgba(241, 243, 244, 1);
        border:                 1px solid rgba(241, 243, 244,1);
        border-radius:          8px;
        padding:                0.8em 0.5em 0.8em 0.5em ;
        outline:                0;
        font-size:              15px;
        margin:                 2px 5px 8px 5px;
    }
    QListWidget::item {
        background-color:       #ffffff;
        border-radius:          8px;
        margin-top:             0.4em;
        padding:                0.5em;       
    }
    QListWidget::item:selected {
        background-color:       #d2e3fc;
        border :                none;
        color:                  #0275d8;
    }

    QPushButton{
        font-size:              15px;
        border-radius:          8px;
        color:                  #ffffff;
        font-weight:            bold;
        background-color:       #F3F3F2;

    }  
    QPushButton::hover{
        background-color:       #1967d2;
    }
    QPushButton::pressed{
        background-color:       #185abc;
    }

    QLineEdit{
        background-color:       rgba(241, 243, 244, 1);
        border:                 1px solid rgba(241, 243, 244,1);
        border-radius:          8px;
        min-height:             2em;
        padding:                0.5em;
        font-size:              16px;
        margin:                 5px 5px 0px 5px;
    }

    QScrollBar{
        border:                 none;
        background-color:       rgba(241, 243, 244, 1);  
    }
    QScrollBar:vertical {              
        width:                  18px;
    }
    QScrollBar:horizontal {              
        height:                 10px;     
    }
    QScrollBar::handle:vertical{
        background :            #CFD1D0;
        border-radius:          5px;   
        margin-left:            0.5em; 
    }
    QScrollBar::handle:horizontal{
        background :            #CFD1D0;
        border-radius:          5px;    
    }
    QScrollBar::add-line:horizontal {
        border:                 none;
        background:             none;
        width:                  20px;
        subcontrol-position:    right;
        subcontrol-origin:      margin;
    }
    QScrollBar::add-line:vertical {
        border:                 none;
        background:             none;
        height:                 20px;
        margin-left:            5px;
        subcontrol-position:    top;
        subcontrol-origin:      margin;
    }
    QScrollBar::sub-line:horizontal {
        border:                 none;
        background:             none;
        width:                  20px;
        subcontrol-position:    left;
        subcontrol-origin:      margin;
    }
    QScrollBar::sub-line:vertical {
        border:                 none;
        background:             none;
        height:                 20px;
        subcontrol-position:    bottom;
        subcontrol-origin:      margin;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background:             none;
    } 
    QPushButton{
        font-size:              15px;
        border-radius:          8px;
        color:                  #ffffff;
        font-weight:            bold;
    }  
    QPushButton::hover{
        background-color:       #1967d2;
    }
    QPushButton::pressed{
        background-color:       #185abc;
    }
''')


horizontalLayout1 = QHBoxLayout()
horizontalLayout2 = QHBoxLayout()
horizontalLayoutforbutton = QVBoxLayout()
verticalLayout = QVBoxLayout()

label = QLabel(todoWord)
label.setObjectName('header')
list_widget = QListWidget()
list_widget.setAutoScroll(True)
list_widget.setWordWrap(True)
list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
list_widget.setMinimumSize(400, 300)


textbox = QLineEdit()
textbox.setPlaceholderText(placeHolderWord)
textbox.setFocus()
textbox.setCursor(QCursor(Qt.CursorShape.IBeamCursor))

date_edit = QDateTimeEdit()
date_edit.setDisplayFormat("yyyy-MM-dd")
date_edit.setDateTime(QDateTime.currentDateTime())

time_edit = QDateTimeEdit()
time_edit.setDisplayFormat("HH:mm")
time_edit.setDateTime(QDateTime.currentDateTime())


btn_addTask = QPushButton(addWord)
btn_addTask.clicked.connect(addTask)
btn_addTask.setStyleSheet('color: black;')

btn_deleteTask = QPushButton()
btn_deleteTask.clicked.connect(deleteTask)
btn_deleteTask.setIcon(QIcon(deleteIcon))
btn_deleteTask.setIconSize(QSize(20, 20))
btn_deleteTask.setToolTip(deleteWord)

btn_saveTask = QPushButton()
btn_saveTask.clicked.connect(saveTask)
btn_saveTask.setIcon(QIcon(saveIcon))
btn_saveTask.setIconSize(QSize(20, 20))
btn_saveTask.setToolTip(saveWord)

btn_editTask = QPushButton()
btn_editTask.clicked.connect(editTask)
btn_editTask.setIcon(QIcon(editIcon))
btn_editTask.setIconSize(QSize(20, 20))
btn_editTask.setToolTip(editWord)

btn_loadTask = QPushButton()
btn_loadTask.clicked.connect(loadTask)
btn_loadTask.setIcon(QIcon(loadIcon))
btn_loadTask.setIconSize(QSize(20, 20))
btn_loadTask.setToolTip(loadWord)

btn_clearAll = QPushButton(clearAllWord)
btn_clearAll.clicked.connect(clearAllTask)
btn_clearAll.setStyleSheet('color: black;')
btn_clearAll.setToolTip(clearAllToolTip)

btn_setTime = QPushButton(setTimeWord)
btn_setTime.clicked.connect(setCurrentDateTime)
btn_setTime.setStyleSheet('color: black;')
btn_setTime.setToolTip(setTimeToolTip)

btn_changeLan = QPushButton()
btn_changeLan.setStyleSheet('color: black;')
btn_changeLan.clicked.connect(changeLan)
btn_changeLan.setIcon(QIcon(changeLanIcon))
btn_changeLan.setToolTip(changeLanWord)


btn_exit = QPushButton()
btn_exit.clicked.connect(stopApplication)
btn_exit.setIcon(QIcon(exitIcon))
btn_exit.setStyleSheet('color: black;')
btn_exit.setToolTip(exitWord)


verticalLayout.addWidget(label)

horizontalLayout1.addWidget(btn_loadTask, stretch=1)
horizontalLayout1.addWidget(btn_editTask, stretch=1)
horizontalLayout1.addWidget(btn_saveTask, stretch=1)

horizontalLayout2.addWidget(btn_deleteTask, stretch=1)
horizontalLayout2.addWidget(btn_changeLan, stretch=1)
horizontalLayout2.addWidget(btn_exit, stretch=1)

horizontalLayoutforbutton.addLayout(horizontalLayout1)
horizontalLayoutforbutton.addLayout(horizontalLayout2)
verticalLayout.addLayout(horizontalLayout1)
verticalLayout.addLayout(horizontalLayout2)
verticalLayout.addWidget(list_widget)
verticalLayout.addWidget(textbox)
verticalLayout.addWidget(date_edit)
verticalLayout.addWidget(time_edit)
horizontalLayoutforbutton.addWidget(btn_clearAll, stretch=1)
horizontalLayoutforbutton.addWidget(btn_setTime, stretch=1)
horizontalLayoutforbutton.addWidget(btn_addTask, stretch=1)  
verticalLayout.addLayout(horizontalLayoutforbutton)


main_layout = QVBoxLayout()
main_layout.addLayout(verticalLayout)

current_time_label = QLabel()
current_time_label.setFont(dateTimeFont)  
current_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
current_time_label.setStyleSheet('color: #787c80;')

def updateCurrentTime():
    current_time = QDateTime.currentDateTime()
    formatted_time = current_time.toString("hh:mm:ss AP")
    current_time_label.setText(formatted_time)


timer = QTimer()
timer.timeout.connect(updateCurrentTime)
timer.start(1000) 



current_date_label = QLabel()
current_date_label.setFont(QFont(dateTimeFont)) 
current_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
current_date_label.setStyleSheet('color: #787c80;')


def updateCurrentDate():
    current_date = QDateTime.currentDateTime()
    formatted_date = current_date.toString("yyyy-MM-dd")
    current_date_label.setText(formatted_date)


date_timer = QTimer()
date_timer.timeout.connect(updateCurrentDate)
date_timer.start(1000)


main_layout.addWidget(current_time_label)
main_layout.addWidget(current_date_label)



global main_window
main_window = QWidget()
main_window.setWindowIcon(QIcon(icon))
main_window.setWindowTitle("ToDo")

isEnd = True

def closeEvent(event):
    if isEnd :
        event.ignore()
        main_window.setWindowState(Qt.WindowState.WindowMinimized)

main_window.closeEvent = closeEvent

main_window.setLayout(main_layout)

main_window.show()

loadTask()

sys.exit(app.exec())


#Reza Asadi (Github : RezaGooner)
#	2024/02/24
#	  23:15
#
#
