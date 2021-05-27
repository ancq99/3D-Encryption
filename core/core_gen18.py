
""" I M P O R T
================================================================================
"""


# importing stuff

import time,math,random as ran,numpy as np,matplotlib.pyplot as mpl
from core.text_highlight import *

""" A D D I T I O N A L   M A T H   F U N C T I O N S
================================================================================
"""


# scaling vector down so its length is 1

def wek_to_wer(wek):
    div=math.sqrt(wek[0]*wek[0]+wek[1]*wek[1]+wek[2]*wek[2])
    return [wek[0]/div,wek[1]/div,wek[2]/div]

# whether the sign is positive or negative

def negnum(x):
    if x>=0:
        return 1
    else:
        return -1

# two angles to a vector 

def ang_to_wek(flat,up):
    
    if int(up)==-90:
        return [0,0,-1]
    if int(up)==90:
        return [0,0,1]
    if (int(up)==180 or int(up)==-180):
        z=0
    else:
        z=math.tan(math.radians(up))
    if (int(flat)==180 or int(flat)==-180):
        return [-1,0,z]
    if int(flat)==-90:
        return [0,-1,z]
    if int(flat)==90:
        return [0,1,z]
    y=math.tan(math.radians(flat))
    return [1,y,z]


# angle correction to the format used in the programme

def corran(ang):
    if ang>0:
        return ang-180
    if ang<0:
        return ang+180
    if ang==0:
        return 180
    if ang==180 or ang==-180:
        return 0

# displaying how much time is left

def how_much_time(tojm):
    if tojm<60: 
        col_print(str(round(tojm,2)) + " seconds left to compelete", "I")
    else:
        if tojm<3600:
            col_print(str(int(tojm//60))+" minutes "+str(int(tojm%60))+" seconds left to compelete", "I")
        else:
            if tojm<86400:
                col_print(str(round(tojm/3600,2))+" hours left to compelete", "I")
            else:
                if tojm<31536000:
                    col_print(str(round(tojm/86400,2))+" days left to compelete", "I")
                else:
                    col_print(str(round(tojm/31536000,2))+" years left to compelete", "I")

    


""" L O A D I N G   A N D   S A V I N G
================================================================================
"""


# loading the image

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

# loading points

def loadpoints(fil):
    tab=[[],[],[]]
    res=[]
    f=open(fil,'r')
    a=""
    b=0
    for i in f:
        for d in i:
            if d=="@":
                tab[b].append(float(a))
                a=""
                b+=1        
            else:
                if d!=";":
                    a+=d
                else:
                    tab[b].append(float(a))
                    a=""
    tab[b].append(float(a))        
    for i in range(len(tab[0])):
        res.append([tab[0][i],tab[1][i],tab[2][i]])
    return res

# loading encryption key

def loadkey(fil):
    tab=[]
    f=open(fil,'r')
    i=0
    for d in f:
        if i<3:
            tab.append(float(d[4:-1]))
        if i==3:
            tab.append(float(d[6:-1]))
        if i==4:
            tab.append(float(d[7:-1]))
        if i==5:
            tab.append(float(d[5:-1]))
        if i==6:
            tab.append(int(d[9:-1]))
        i+=1
    return tab

# saving decrypted image

def savtofil2d(tab,sav):
    
    f=open(sav,'w')
    for i in tab:
        for d in i:
            f.write(str(int(d)))
        f.write("\n")



# saving points to a file

def savtofil3d(tab,sav):
    ln=len(tab)
    f=open(sav,'w')
    a=""
    b=""
    c=""
    for i in range(ln):
        a+=(str(tab[i][0]))
        b+=(str(tab[i][1]))
        c+=(str(tab[i][2]))
        if i<ln-1:
            a+=(";")
            b+=(";")
            c+=(";")
    f.write(a+"@"+b+"@"+c)
    f.close()


""" T I E R   III   F U N C T I O N S
================================================================================
"""


# comparing lists

def comparelist(tab,res):
    check=0
    for i in range(len(tab)):
        for d in range(len(tab[0])):
            if tab[i][d]!=res[i][d]:
                check+=1
    return check

# counting how many points are in the image

def count_points(tab):
    a=0
    for i in tab:
        for d in i:
            if d==1:
                a+=1
    return a

# calculating how many points will the program create

def calc_poi(flat,up,x,y,z,a,b,c,fov,n):
    centr=wek_to_wer(ang_to_wek(flat,up))
    cent_p=pierce(centr[0],centr[1],centr[2],x,y,z,a,b,c)
    cent_r=math.sqrt( (x-cent_p[0])*(x-cent_p[0])+(y-cent_p[1])*(y-cent_p[1])+(z-cent_p[2])*(z-cent_p[2]))
    st_r=cent_r*math.tan(math.radians(fov/2))
    st_v=cent_r*st_r*st_r*math.pi/3
    n_poi=n*a*b*c/st_v
    return n_poi

# checking if created cone is not cut too much

def eije(x,y,z,fov,lgt,a,b,c,r,flat,up,rad):
    stab=wek_to_wer(ang_to_wek(flat,up))
    ouch=pierce(stab[0],stab[1],stab[2],x,y,z,a,b,c)
    tes=math.sqrt( (x-ouch[0])*(x-ouch[0])+(y-ouch[1])*(y-ouch[1])+(z-ouch[2])*(z-ouch[2]))
    if math.fabs(rad-tes)>0.0001:
        return 0
    if lgt%2==0:
        gg=1
    else:
        gg=0
    tabzi=ghostdeg(lgt)
    for i in range(lgt):
        for d in range(lgt):
            dc=d-lgt//2
            ic=lgt//2-i
            if dc>=0:
                dc+=gg
            if ic<=0:
                ic-=gg
            for num in tabzi:
                if [ic,dc]==num[0]:
                    xeh=num[1]
                    heh=num[2]
                    break
                else:
                    xeh=0
                    heh=0
            if math.fabs(dc)>=math.fabs(ic):
                kuk=math.fabs(dc)
            else:
                kuk=math.fabs(ic)
            fag=kuk/(lgt//2)
            cor_flat=flat+xeh*fov/2*fag
            cor_up=up+heh*fov/2*fag
            stab=wek_to_wer(ang_to_wek(cor_flat,cor_up))
            ouch=pierce(stab[0],stab[1],stab[2],x,y,z,a,b,c)
            radius=math.sqrt( (x-ouch[0])*(x-ouch[0])+(y-ouch[1])*(y-ouch[1])+(z-ouch[2])*(z-ouch[2]))
            if radius<0.5*r:
                return 0
    return 1


""" T I E R   II   F U N C T I O N S
================================================================================
"""

# squaring tables

def sq_tab(tab,zenn):
    hgt=len(tab)
    lgt=len(tab[0])
    if hgt==lgt:
        return tab
    if hgt>lgt:
        res=[]
        dif=hgt-lgt
        pp=math.floor(dif/lgt*zenn)
        for i in range(hgt):
            temp=[]
            for d in range(dif):
                temp.append(0)
            res.append(temp)
        a=0
        while a<pp:
            mul=dif*hgt
            x=ran.randint(0,mul-1)
            if res[x//dif][x%dif]!=1:
                res[x//dif][x%dif]=1
                a+=1
        for i in range(len(res)):
            for d in res[i]:
                tab[i].append(d)
    else:
        res=[]
        dif=lgt-hgt
        pp=math.floor(dif/hgt*zenn)
        for d in range(dif):
            temp=[]
            for i in range(lgt):
                temp.append(0)
            res.append(temp)
        a=0
        while a<pp:
            mul=dif*lgt
            x=ran.randint(0,mul-1)
            if res[x//lgt][x%lgt]!=1:
                res[x//lgt][x%lgt]=1
                a+=1
        for i in res:
            tab.append(i)
    return 0

# angle distribution for coordinates

def ghostdeg(x):
    dab=[]
    while x>0:
        s=x 
        p=s//2
        summ=-135
        fl=s%2
        j=-p
        i=-p
        while(j<p):
            while(i<p):
                lolz=math.fabs(math.tan(math.radians(summ)))
                xaw=1/math.sqrt(1+lolz*lolz)*negnum(i)
                haw=lolz*1/math.sqrt(1+lolz*lolz)*negnum(j)
                addu=[[i,j],xaw,haw]
                if addu not in dab:
                    dab.append(addu)
                if(True):
                    lolz=math.fabs(math.tan(math.radians(summ+180)))
                    xaw=1/math.sqrt(1+lolz*lolz)*negnum(-i)
                    haw=lolz*1/math.sqrt(1+lolz*lolz)*negnum(-j)
                    addu=[[-i,-j],xaw,haw]
                    if addu not in dab:
                        dab.append(addu)

                    lolz=math.fabs(math.tan(math.radians(summ+90)))
                    xaw=1/math.sqrt(1+lolz*lolz)*negnum(-j)
                    haw=lolz*1/math.sqrt(1+lolz*lolz)*negnum(i)
                    addu=[[-j,i],xaw,haw]
                    if addu not in dab:
                        dab.append(addu)
                    
                    lolz=math.fabs(math.tan(math.radians(summ+270)))
                    xaw=1/math.sqrt(1+lolz*lolz)*negnum(j)
                    haw=lolz*1/math.sqrt(1+lolz*lolz)*negnum(-i)
                    addu=[[j,-i],xaw,haw]
                    if addu not in dab:
                        dab.append(addu)
                summ+=90/(s-1)
                if i+1==0:
                    i+=2-fl
                else:
                    i+=1
            if j+1==0:
                j+=2-fl
            else:
                j+=1
            summ=-135
            s-=2
            p=s//2
        x-=2
    return dab

# main function searching for correct cone location   

def aspecialf(p,a,b,c,lgt,zenn):
    std_tan=math.tan(math.radians(40))
    zet=min([a,b,c])
    v_a=a*b*c
    v_s=(zet**3)*std_tan**2*math.pi/3
    nnn=zenn*v_a/v_s
    col_print("Minimal number of points required : "+str(nnn), "I")
    for stirr in range(1000):
        fov=ran.random()*70+10
        tanr=math.tan(math.radians(fov/2))/std_tan
        rad=zet*(1/(tanr*tanr*p))**(1/3)
        for i in range(100):
            r=ran.randint(0,5)
            flat=ran.random()*360-180
            up=ran.random()*360-180
            dupa=wek_to_wer(ang_to_wek(flat,up))
            if r==0:
                bd=ran.random()*b
                cd=ran.random()*c
                x=a-(rad*dupa[0])
                y=bd+(rad*(dupa[1]))
                z=cd+(rad*(dupa[2]))
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return a,bd,cd,x,y,z,corran(flat),corran(up),fov
            if r==1:
                bd=ran.random()*b
                cd=ran.random()*c  
                x=0-(rad*dupa[0])
                y=bd+(rad*(dupa[1]))
                z=cd+(rad*(dupa[2]))
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return 0,bd,cd,x,y,z,corran(flat),corran(up),fov
            if r==2:
                ad=ran.random()*a
                cd=ran.random()*c  
                x=ad+(rad*(dupa[0]))
                y=b-(rad*dupa[1])
                z=cd+(rad*(dupa[2]))
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return ad,b,cd,x,y,z,corran(flat),corran(up),fov
            if r==3:
                ad=ran.random()*a
                cd=ran.random()*c  
                x=ad+(rad*(dupa[0]))
                y=0-(rad*dupa[1])
                z=cd+(rad*(dupa[2]))
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return ad,0,cd,x,y,z,corran(flat),corran(up),fov
            if r==4:
                ad=ran.random()*a
                bd=ran.random()*b  
                x=ad+(rad*(dupa[0]))
                y=bd*b+(rad*(dupa[1]))
                z=c-(rad*dupa[2])
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return ad,bd,z,x,y,z,corran(flat),corran(up),fov
            if r==5:
                ad=ran.random()*a
                bd=ran.random()*b  
                x=ad+(rad*(dupa[0]))
                y=bd+(rad*(dupa[1]))
                z=0-(rad*dupa[2])
                if x>=0 and x<=a and y>=0 and y<=b and z>=0 and z<=c:
                    if eije(x,y,z,fov,lgt,a,b,c,rad,flat,up,rad):
                        return ad,bd,0,x,y,z,corran(flat),corran(up),fov
    col_print("Failed to find the eye location","E")
    return ["z"]

# checking where the ray has pierced the BOX

def pierce(xv,yv,zv,x,y,z,a,b,c):
    
    if xv!=0:
        xf=(a-x)/xv
        nxf=(-x)/xv
    
        yxf=float(format(y+yv*xf,'.12g'))
        zxf=float(format(z+zv*xf,'.12g'))
        nyxf=float(format(y+yv*nxf,'.12g'))
        nzxf=float(format(z+zv*nxf,'.12g'))
    
        if (yxf>=0 and xv>0 and yxf<=b):
            if (zxf>=0 and zxf<=c):
                return [a,yxf,zxf,"p"]
        if (x!=0 and xv<0 and nyxf>=0 and nyxf<=b):
            if (x!=0 and nzxf>=0 and nzxf<=c):
                return [0,nyxf,nzxf,"n"]
            
    if yv!=0:
        yf=(b-y)/yv
        nyf=(-y)/yv
        
        xyf=float(format(x+xv*yf,'.12g'))
        zyf=float(format(z+zv*yf,'.12g'))
        nxyf=float(format(x+xv*nyf,'.12g'))
        nzyf=float(format(z+zv*nyf,'.12g'))
  
        if (xyf>=0 and yv>0 and xyf<=a):
            if (zyf>=0 and zyf<=c):
                return [xyf,b,zyf,"p"]
        if (y!=0 and yv<0 and nxyf>=0 and nxyf<=a):
            if (y!=0 and nzyf>=0 and nzyf<=c):
                return [nxyf,0,nzyf,"n"]
    if zv!=0:
        zf=(c-z)/zv
        nzf=(-z)/zv
        
        xzf=float(format(x+xv*zf,'.12g'))
        yzf=float(format(y+yv*zf,'.12g'))
        nxzf=float(format(x+xv*nzf,'.12g'))
        nyzf=float(format(y+yv*nzf,'.12g'))

        if (xzf>=0 and zv>0 and xzf<=a):
            if (yzf>=0 and yzf<=b):
                return [xzf,yzf,c,"p"]
        if (z!=0 and zv<0 and nxzf>=0 and nxzf<=a):
            if (z!=0 and nyzf>=0 and nyzf<=b):
                return [nxzf,nyzf,0,"n"]
    print(xv,yv,zv,x,y,z,a,b,c)
    return -1


""" T I E R   I   F U N C T I O N S
================================================================================
"""


# encrypting
        
def encrypting(tab,lgt,a,b,c,p,zenn,noise):
    while True:
        dud=aspecialf(p,a,b,c,lgt,zenn)
        if dud[0]!="z":
            break
        else:
            input("Do you want to try again?")
    x=dud[3]
    y=dud[4]
    z=dud[5]
    flat=dud[6]
    up=dud[7]
    fov=dud[8]
    res=[]
    stabh=wek_to_wer(ang_to_wek(flat,up))
    print(pierce(stabh[0],stabh[1],stabh[2],x,y,z,a,b,c))
    if lgt%2==0:
        gg=1
    else:
        gg=0
    tabzi=ghostdeg(lgt)
    for i in range(lgt):
        for d in range(lgt):
            if tab[i][d]==1:
                
                dc=d-lgt//2
                ic=lgt//2-i

                if dc>=0:
                    dc+=gg
                if ic<=0:
                    ic-=gg

                for num in tabzi:
                    if [ic,dc]==num[0]:
                        xeh=num[1]
                        heh=num[2]
                        break
                    else:
                        xeh=0
                        heh=0
                if math.fabs(dc)>=math.fabs(ic):
                    kuk=math.fabs(dc)
                else:
                    kuk=math.fabs(ic)
                fag=kuk/(lgt//2)
                cor_flat=flat+xeh*fov/2*fag
                cor_up=up+heh*fov/2*fag
                stab=wek_to_wer(ang_to_wek(cor_flat,cor_up))
                ouch=pierce(stab[0],stab[1],stab[2],x,y,z,a,b,c)
                radius=math.sqrt( (x-ouch[0])*(x-ouch[0])+(y-ouch[1])*(y-ouch[1])+(z-ouch[2])*(z-ouch[2]))
                skal=math.sqrt(ran.random())*radius
                res.append([x+stab[0]*skal,y+stab[1]*skal,z+stab[2]*skal])
    n_poi=calc_poi(flat,up,x,y,z,a,b,c,fov,len(res))
    drott=0
    ddd=0
    col_print("Points added outside of the cone  : "+str(math.ceil(n_poi-zenn)),"I")
    while drott<math.ceil(0):
        noix=ran.random()*a
        noiy=ran.random()*b
        noiz=ran.random()*c
        dabb=wek_to_wer(ang_to_wek(flat,up))
        radd=wek_to_wer([noix-x,noiy-y,noiz-z])
        fff=dabb[0]*radd[0]+dabb[1]*radd[1]+dabb[2]*radd[2]
        if math.fabs(fff-1)<0.00001:
            ang_2w=0
        else:
            ang_2w=math.degrees(math.acos(fff))
        if ang_2w>fov/2:
            res.append([noix,noiy,noiz])
            drott+=1
        else:
            ddd+=1
    for i in range(math.ceil(n_poi*noise)):
        noix=ran.random()*a
        noiy=ran.random()*b
        noiz=ran.random()*c
        res.append([noix,noiy,noiz])
    return [res,x,y,z,fov,flat,up,lgt]

# decrypting

def scan_space(tab,x,y,z,fov,flat,up,lgt):
    res=np.zeros((lgt,lgt))
    tabzi=ghostdeg(lgt)
    if lgt%2==0:
        gg=1
    else:
        gg=0
    flag=1
    dok=len(tab)
    angle_tab=[]
    for i in range(lgt):
        for d in range(lgt):               
            dc=d-lgt//2
            ic=lgt//2-i
            if dc>=0:
                dc+=gg
            if ic<=0:
                ic-=gg
            for num in tabzi:
                if [ic,dc]==num[0]:
                    xeh=num[1]
                    heh=num[2]
                    break
                else:
                    xeh=0
                    heh=0
            if math.fabs(dc)>=math.fabs(ic):
                kuk=math.fabs(dc)
            else:
                kuk=math.fabs(ic)
            fag=kuk/(lgt//2)
            angle_tab.append([flat+xeh*fov/2*fag,up+heh*fov/2*fag,i,d])
    for g in tab:
        if flag==2:
            tojm=(time.perf_counter()-tim1)*dok
            how_much_time(tojm)
            flag=0
        if flag==1:
            tim1=time.perf_counter()
            flag+=1
        dist=math.sqrt( (x-g[0])*(x-g[0])+(y-g[1])*(y-g[1])+(z-g[2])*(z-g[2]))
        zium=wek_to_wer([g[0]-x,g[1]-y,g[2]-z])
        for disco in angle_tab:
            cor_flat=disco[0]
            cor_up=disco[1]
            stab=wek_to_wer(ang_to_wek(cor_flat,cor_up))
            win=zium[0]*stab[0]+zium[1]*stab[1]+zium[2]*stab[2]
            if int(win)==1:
                angle_2w=0
            else:
                angle_2w=math.acos(win)
            angd=math.tan(math.fabs(angle_2w))*dist
            if angd<0.0001 and (angd>0 or angd==0):
                res[disco[2]][disco[3]]=1
    return res

# deleting noise

def scan_cleanup(tab,x,y,z,fov,flat,up,lgt,corr):
    todelete=[]
    tabzi=ghostdeg(lgt)
    if lgt%2==0:
        gg=1
    else:
        gg=0
    for g in tab:
        dist=math.sqrt( (x-g[0])*(x-g[0])+(y-g[1])*(y-g[1])+(z-g[2])*(z-g[2]))
        zium=wek_to_wer([g[0]-x,g[1]-y,g[2]-z])
        for i in range(lgt):
            for d in range(lgt):
                
                dc=d-lgt//2
                ic=lgt//2-i

                if dc>=0:
                    dc+=gg
                if ic<=0:
                    ic-=gg

                for num in tabzi:
                    if [ic,dc]==num[0]:
                        xeh=num[1]
                        heh=num[2]
                        break
                    else:
                        xeh=0
                        heh=0
                if math.fabs(dc)>=math.fabs(ic):
                    kuk=math.fabs(dc)
                else:
                    kuk=math.fabs(ic)
                fag=kuk/(lgt//2)
                cor_flat=flat+xeh*fov/2*fag
                cor_up=up+heh*fov/2*fag
                stab=wek_to_wer(ang_to_wek(cor_flat,cor_up))
                win=zium[0]*stab[0]+zium[1]*stab[1]+zium[2]*stab[2]
                if int(win)==1:
                    angle_2w=0
                else:
                    angle_2w=math.acos(win)
                if math.fabs(math.tan(math.fabs(angle_2w))*dist)<0.00001:
                    if corr[i][d]!=1:
                        if g in tab:
                            todelete.append(g)
    for i in todelete:
        if i in tab:
            tab.remove(i)
    return tab


""" M A I N   F U N C T I O N S
================================================================================
"""


def encryption(path_input, path_output, slider, noise):
    col_print("Starting encryption.", "I")
    tab=loadtab(path_input)
    zenn=count_points(tab)
    sq_tab(tab,zenn)
    lgt=len(tab)
    zenn=count_points(tab)
    col_print("Points located inside of the cone : "+str(zenn),"I")
    points=encrypting(tab,lgt,10,10,10,slider,zenn,noise)
    col_print("Total number of points generated  : "+str(len(points[0])),"I")
    #check1=scan_cleanup(points[0],points[1],points[2],points[3],points[4],points[5],points[6],lgt,tab)
    #print(len(check1))
    f=open(path_output+"\\key.txt",'w')
    savtofil3d(points[0], path_output+"\\decrypted_file")
    f.write("x = "+str(points[1])+"\n")
    f.write("y = "+str(points[2])+"\n")
    f.write("z = "+str(points[3])+"\n")
    f.write("fov = "+str(points[4])+"\n")
    f.write("flat = "+str(points[5])+"\n")
    f.write("up = "+str(points[6])+"\n")
    f.write("length = "+str(points[7])+"\n")
    f.close()
    col_print("Encryption finished! Result saved to"+path_output,"S")




def decryption(path_input, path_output, path_key):
    col_print("Starting decryption.","I")
    tab=loadpoints(path_input)
    keytab=loadkey(path_key)
    res=scan_space(tab,keytab[0],keytab[1],keytab[2],keytab[3],keytab[4],keytab[5],keytab[6])
    savtofil2d(res,path_output)
    col_print("Decryption finished! Result saved to"+path_output,"S")



