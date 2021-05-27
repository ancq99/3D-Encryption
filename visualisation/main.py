from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import os
from core.core import *

cwd = os.getcwd().replace("\\","/")
dir_V_decrypted_file = ""
dir_V_output = ""
v_file_size = 0;

class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.successFormat = QtGui.QTextCharFormat()
        self.successFormat.setForeground(QtGui.QColor(0,168,16))
        self.successFormat.setFontWeight(75)
        self.successFormat.setFontLetterSpacing(100)
        self.successFormat.setFontPointSize(10)

        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)
        self.errorFormat.setFontWeight(75)
        self.errorFormat.setFontLetterSpacing(100)
        self.errorFormat.setFontPointSize(10)

        self.infoFormat = QtGui.QTextCharFormat()
        self.infoFormat.setForeground(QtGui.QColor(66,104,255))
        self.infoFormat.setFontWeight(75)
        self.infoFormat.setFontLetterSpacing(100)
        self.infoFormat.setFontPointSize(10)

    def highlightBlock(self, text):
        if text.startswith('[SUCCESS]'):
            self.setFormat(0, len(text), self.successFormat)
        elif text.startswith('[ERROR]'):
            self.setFormat(0, len(text), self.errorFormat)
        elif text.startswith('[INFO]'):
            self.setFormat(0, len(text), self.infoFormat)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)

        self.setWindowTitle("3D ENCRYPTION")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
       
        self.process = self.findChild(QtWidgets.QTextEdit, 'console_output')
        self.highlighter = Highlighter(self.process.document())

        self.file_size = self.findChild(QtWidgets.QLabel, 'file_size')

        # visualize tab
        self.V_button = self.findChild(QtWidgets.QPushButton, 'V_generate')
        self.V_button.clicked.connect(self.button_pressed_V_generate)

        self.dir_V_output = self.findChild(QtWidgets.QPushButton, 'V_output')
        self.dir_V_output.clicked.connect(self.getpath_V_output)

        self.dir_V_decrypted_file = self.findChild(QtWidgets.QPushButton, 'V_decrypted_file')
        self.dir_V_decrypted_file.clicked.connect(self.getpath_V_decrypted_file)

        self.dir_V_output_text = self.findChild(QtWidgets.QTextEdit, 'V_output_text')
        self.dir_V_decrypted_file_text = self.findChild(QtWidgets.QTextEdit, 'V_decrypted_file_text')

        self.dir_V_output_text.setText(cwd)
       
        sys.stdout = Stream(newText=self.onUpdateText)
        print("[INFO] ALL FIELDS ARE REQUIRED")
        self.show()
        
       

    def onUpdateText(self, text):
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def button_pressed_V_generate(self):
        dir_V_output = self.dir_V_output_text.toPlainText()
        dir_V_decrypted_file = self.dir_V_decrypted_file_text.toPlainText()

        self.dir_V_output_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.dir_V_decrypted_file_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

        if(dir_V_output == "" and dir_V_decrypted_file == ""):
            print("[ERROR] FIELDS CANNOT BE EMPTY")
            self.dir_V_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.dir_V_decrypted_file_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
        elif(dir_V_decrypted_file == ""):
            print("[ERROR] DECRYPTED FILE FIELD CANNOT BE EMPTY")
            self.dir_V_decrypted_file_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
        elif(dir_V_output == ""):
            print("[ERROR] OUTPUT FIELD CANNOT BE EMPTY")
            self.dir_V_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
        else:
            print("[INFO] OUTPUT DIR: " + dir_V_output)
            print("[INFO] FILE DIR: "+ dir_V_decrypted_file)
            visualize(dir_V_decrypted_file, dir_V_output)


    def getpath_V_output(self):
        dir_V_output = QtWidgets.QFileDialog().getExistingDirectory().replace("\\","/")
        self.dir_V_output_text.setText(dir_V_output)

    def getpath_V_decrypted_file(self):
        dir_V_decrypted_file = QtWidgets.QFileDialog.getOpenFileName()[0].replace("\\","/")
        self.dir_V_decrypted_file_text.setText(dir_V_decrypted_file)
        V_file_size = get_exp_size(dir_V_decrypted_file);
        self.file_size.setText(str(V_file_size) + " MB")


if __name__ == '__main__':
    # Run the application.
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    gui = Ui()
    sys.exit(app.exec_())
