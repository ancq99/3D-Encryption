from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import os
from core.core_gen18 import *
from core.densit import *
from core.text_highlight import *

cwd = os.getcwd().replace("\\","/")
dir_key = ""
dir_D_output = ""
dir_D_decrypted_file = ""
dir_input = ""
dir_E_output = ""
encryption_level_slider = 1
noise_slider = 1

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)

        self.setWindowTitle("3D ENCRYPTION")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # decrypt_tab
        self.D_button = self.findChild(QtWidgets.QPushButton, 'D_decrypt')
        self.D_button.clicked.connect(self.button_pressed_D_decrypt)

        self.dir_key = self.findChild(QtWidgets.QPushButton, 'D_key')
        self.dir_key.clicked.connect(self.getpath_D_key)

        self.dir_D_output = self.findChild(QtWidgets.QPushButton, 'D_output')
        self.dir_D_output.clicked.connect(self.getpath_D_output)

        self.dir_D_decrypted_file = self.findChild(QtWidgets.QPushButton, 'D_decrypted_file')
        self.dir_D_decrypted_file.clicked.connect(self.getpath_D_decrypted_file)

        self.dir_key_text = self.findChild(QtWidgets.QTextEdit, 'D_key_text')
        self.dir_D_output_text = self.findChild(QtWidgets.QTextEdit, 'D_output_text')
        self.dir_D_decrypted_file_text = self.findChild(QtWidgets.QTextEdit, 'D_decrypted_file_text')

        # default value of output dir is 'current working directory'
        self.dir_D_output_text.setText(cwd)

        # encrypt tab
        self.E_button = self.findChild(QtWidgets.QPushButton, 'E_encrypt')
        self.E_button.clicked.connect(self.button_pressed_E_encrypt)

        self.dir_E_input = self.findChild(QtWidgets.QPushButton, 'E_input')
        self.dir_E_input.clicked.connect(self.getpath_E_input)

        self.dir_E_output = self.findChild(QtWidgets.QPushButton, 'E_output')
        self.dir_E_output.clicked.connect(self.getpath_E_output)

        self.dir_E_input_text = self.findChild(QtWidgets.QTextEdit, 'E_input_text')
        self.dir_E_output_text = self.findChild(QtWidgets.QTextEdit, 'E_output_text')

        self.dir_E_output_text.setText(cwd)

        self.encryption_level_slider = self.findChild(QtWidgets.QSlider, 'encryption_level_slider')
        self.encryption_level_slider.valueChanged.connect(self.slider_change)

        self.noise_slider = self.findChild(QtWidgets.QSlider, 'noise_slider')
        self.noise_slider.valueChanged.connect(self.slider_change)

        self.selected_noise = self.findChild(QtWidgets.QLabel, 'selected_noise')
        self.num_o_points = self.findChild(QtWidgets.QLabel, 'number_of_points')

        self.current_tab = self.findChild(QtWidgets.QTabWidget, 'tabWidget')  

        self.current_tab.currentChanged.connect(self.tabswitch)
       
        self.slider_change()

        self.show()
        
        self.tabswitch()

    def tabswitch(self):
        self.cls();

        
        

    def slider_change(self):
        encryption_level_slider = self.encryption_level_slider.value()
        noise_slider = self.noise_slider.value()
        self.selected_noise.setText(str(noise_slider))
        dir_input = self.dir_E_input_text.toPlainText()
        if(dir_input != ""):
            self.numofpoints(dir_input)

    def button_pressed_E_encrypt(self):
        dir_E_output = self.dir_E_output_text.toPlainText()
        dir_input = self.dir_E_input_text.toPlainText()
        encryption_level_slider = self.encryption_level_slider.value()
        noise_slider = self.noise_slider.value()

        self.dir_E_output_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.dir_E_input_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

        if(os.path.exists(dir_E_output) and os.path.isdir(dir_E_output)):
            print("")
        else:
            self.error_display(3)
            return

        if(dir_E_output == "" and dir_input == ""):
            col_print("[ERROR] FIELDS CANNOT BE EMPTY", "E")
            self.dir_E_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.dir_E_input_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        elif(dir_E_output == ""):
            col_print("[ERROR] OUTPUT FIELD CANNOT BE EMPTY", "E")
            self.dir_E_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        elif(dir_input == ""):
            col_print("[ERROR] INPUT FIELD CANNOT BE EMPTY","E")
            self.dir_E_input_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        else:
            self.cls()
            col_print("[INFO] File locations: ", "I")
            print(dir_input)
            print(dir_E_output)
            print("Slider lvl: ",encryption_level_slider)
            try:
                encryption(dir_input, dir_E_output, encryption_level_slider, noise_slider)
            except:
                self.error_display(1)

    def getpath_E_output(self):
        dir_E_output = QtWidgets.QFileDialog().getExistingDirectory().replace("\\","/")
        self.dir_E_output_text.setText(dir_E_output)

    def getpath_E_input(self):
        dir_input = QtWidgets.QFileDialog.getOpenFileName()[0].replace("\\","/")
        self.dir_E_input_text.setText(dir_input)
        self.slider_change()


    def button_pressed_D_decrypt(self):
        dir_key = self.dir_key_text.toPlainText()
        dir_D_output = self.dir_D_output_text.toPlainText()
        dir_D_decrypted_file = self.dir_D_decrypted_file_text.toPlainText()

        self.dir_D_output_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.dir_key_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.dir_D_decrypted_file_text.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

        if(os.path.exists(dir_D_output) and os.path.isdir(dir_D_output)):
            print("")
            dir_D_output = dir_D_output + "/encrypted_file.txt"
        else:
            self.error_display(3)
            return

        if(dir_key == "" and dir_D_output == "" and dir_D_decrypted_file == ""):
            col_print("[ERROR] FIELDS CANNOT BE EMPTY", "E")
            self.dir_D_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.dir_key_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.dir_D_decrypted_file_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        elif(dir_D_decrypted_file == ""):
            col_print("[ERROR] DECRYPTED FILE FIELD CANNOT BE EMPTY", "E")
            self.dir_D_decrypted_file_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        elif(dir_key == ""):
            col_print("[ERROR] KEY FIELD CANNOT BE EMPTY", "E")
            self.dir_key_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        elif(dir_D_output == ""):
            col_print("[ERROR] OUTPUT FIELD CANNOT BE EMPTY","E")
            self.dir_D_output_text.setStyleSheet("background-color: rgba(193, 66, 66, 0.4);")
            self.error_display(9) 
        else:
            self.cls()
            col_print("[INFO] File locations: ", "I")
            print(dir_D_decrypted_file)
            print(dir_key)
            print(dir_D_output)
            

            try:
                decryption(dir_D_decrypted_file, dir_D_output, dir_key)
            except:
                self.error_display(0)  

    def getpath_D_key(self):
        dir_key = QtWidgets.QFileDialog.getOpenFileName()[0].replace("\\","/")
        self.dir_key_text.setText(dir_key)
        self.validate_file(dir_key, "k")

    def getpath_D_output(self):
        dir_D_output = QtWidgets.QFileDialog().getExistingDirectory().replace("\\","/")
        self.dir_D_output_text.setText(dir_D_output)

    def getpath_D_decrypted_file(self):
        dir_D_decrypted_file = QtWidgets.QFileDialog.getOpenFileName()[0].replace("\\","/")
        self.dir_D_decrypted_file_text.setText(dir_D_decrypted_file)
        self.validate_file(dir_D_decrypted_file, "d")

    
    def numofpoints(self, dir_i):
        n = densit(dir_i,10,10,10)
        if(type(n) == str):
            self.warning_display(0)
        else:
            self.num_o_points.setText(str( n * (self.encryption_level_slider.value() + self.noise_slider.value())))
    
    def validate_file(self, path, what):
        if(what=="d"):
            tmp = 0
            with open(path, 'r') as file:
                data = file.read().replace('\n', '')

            if '@' in data:
                data = data.split("@")
            else:
                tmp = 1

            if len(data) == 3:
                if ';' in data[0]:
                    x1 = data[0].split(";")
                else:
                    tmp = 1
                if ';' in data[1]:
                    y1 = data[1].split(";")
                else:
                    tmp = 1
                if ';' in data[2]:
                    z1 = data[2].split(";")
                else:
                    tmp = 1
            else:
                if len(data) != 3 or tmp == 1:
                    self.warning_display(1)
        elif(what=="k"):
            tmp = 0
            with open(path, 'r') as file:
                data = file.read()

            data = data.rstrip()
            if('=' not in data or len(data.split('\n')) != 7):
                self.warning_display(2)



    def error_display(self,n):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")

        if(n==0):
            msg.setInformativeText('Decryption Stopped. Probably wrong file was selected')
            col_print("[ERROR] Decryption Stopped. Probably wrong file was selected", "E")
        elif(n==1):
            msg.setInformativeText('Encryption Stopped. Probably wrong file was selected')
            col_print("[ERROR] Encryption Stopped. Probably wrong file was selected", "E")
        elif(n==2):
            msg.setInformativeText('Invalid file has been selected')
            col_print("[WARNING] Invalid input file was selected", "W")
        elif(n==3):
            msg.setInformativeText('Output field should be a path to existing directory, not file')
            col_print("[ERROR] Wrong output path", "E")
        elif(n==9):
            msg.setInformativeText('An error has occured. Check console for more detailed information')

        print('\r')
        msg.setWindowTitle("Error")
        msg.exec_()

    def warning_display(self, n):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Warning!")
        if(n==0):
            msg.setInformativeText('Invalid file has been selected')
            col_print("[WARNING] Invalid input file was selected", "W")
        elif(n==1):
            msg.setInformativeText('Invalid decrypted file selected')
            col_print("[WARNING] Invalid decrypted file selected", "W")
        elif(n==2):
            msg.setInformativeText('Invalid key file selected')
            col_print("[WARNING] Invalid key file selected", "W")
        print('\r')
        msg.setWindowTitle("Warning!")
        msg.exec_()

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')
   

if __name__ == '__main__':
    # Run the application.
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    gui = Ui()
    sys.exit(app.exec_())