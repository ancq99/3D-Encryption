import os 

os.system("")

def col_print(text, style):
    if(style == "E"):
        print('\x1b[3;30;41m' + text + '\x1b[0m')

    if(style == "S"):
        print('\x1b[3;30;42m' + text + '\x1b[0m')

    if(style == "I"):
        print('\x1b[0;30;47m' + text + '\x1b[0m')

    if(style == "W"):
    	print('\x1b[0;30;43m' + text + '\x1b[0m')