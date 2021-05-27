import math

def loadtab(fil):
    res=[]
    a=0
    f=open(fil,'r')
    for line in f:
        tab=[]
        for i in line:
            if i!="\n":
                tab.append(int(i))
        res.append(tab)
    return res

def count_points(tab):
    a=0
    for i in tab:
        for d in i:
            if d==1:
                a+=1
    return a

def densit(fil,a,b,c):
    try:
        tab=loadtab(fil)
        zenn=count_points(tab)
        std_tan=math.tan(math.radians(40))
        z=min([a,b,c])
        v_a=a*b*c
        v_s=(z**3)*std_tan**2*4/3
        nnn=zenn*v_a/v_s
        h=len(tab[0])
        v=len(tab)
        if h>=v:
            return math.ceil(nnn*h/v)
        else:
            return math.ceil(nnn*v/h)
    except:
        return "Error! Wrong file"
    
    
#print(densit("cus.txt",10,10,10))
