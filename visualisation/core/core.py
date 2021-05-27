import numpy as np
from mayavi import mlab
import os

def get_exp_size(path_points):
    if(path_points == ""):
        return "###"
    tmp = 0
    data = ""
    x1 = ""
    y1 = ""
    z1 = ""
    x=0

    with open(path_points, 'r') as file:
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
            print("[ERROR] CANNOT CALCULATE EXPECTED FILE SIZE")

    
    file.close()

    x = np.array([float(i) for i in x1])
    return round((x.size*7)/1024,2)


def visualize(path_points, path_output):

    tmp = 0
    fileName = ""
    data = ""
    x1 = ""
    y1= ""
    z1 = ""
    x = 0
    y = 0
    z = 0

    if(path_points == ""):
        return
    
    i=1

    while True:
        if(os.path.exists(path_output+"/output"+str(i)+".obj")):
            i=i+1
            continue
        else:
            fileName = path_output + "/output"+str(i)+".obj"
            break

    fileName = fileName.replace("/","\\\\")
    
    

    with open(path_points, 'r') as file:
        data = file.read().replace('\n', '')

    if '@' in data:
        data = data.split("@")
    else:
        print("[ERROR] DECRYPTED FILE IS INVALID")
        return

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
            print("[ERROR] WRONG DECRYPTED FILE FORMAT")
            return

    print("[SUCCESS] DECRYPTED FILE READ SUCCESSFULLY")

    x = np.array([float(i) for i in x1])
    y = np.array([float(i) for i in y1])
    z = np.array([float(i) for i in z1])
    
    mlab.options.offscreen = True
    mlab.points3d(x, y, z, scale_factor=0.03)
    mlab.savefig(fileName)

    # mlab.outline()
    # mlab.show()
    print("[SUCCESS] FILE GENERATED SUCCESSFULLY")

    dir_name = fileName
    dir_name = dir_name.replace("/", "\\").split("\\")
    dir_final = ""
    for i in range(0, len(dir_name) - 1):
        dir_final += dir_name[i] + "\\"

    test = os.listdir(dir_final)

    for item in test:
        if item.endswith(".mtl"):
            os.remove(os.path.join(dir_final, item))


    file.close()