from tkinter import*
def submit():
    #print(u.get())
    #p.set(u.get())
    a=u.get()    
    n=p.get()
    #print('m =', m)
    #print('n =',n)
    #a=input ('请输入起始MAC后六位:')
    #n=input ('请输入需要生存MAC的数量:')
    m=int(n)
    aa='c445ec'+a
    b=int(aa,16)  #字符串转成16进制
    #print ("%#x"%(b))
    c=int(b)     #16进制转成10进制    
    for num in range(1,m+1):
        d=c+0
        e=hex(d)     #10进制转成16进制
        f=c+1048576 
        g=hex(f)     #10进制转成16进制
        h=c+2097152
        i=hex(h)     #10进制转成16进制
        #生产需要的MAC
        Mac1=e[2:]
        Mac2=e[2:4]+'-'+e[4:6]+'-'+e[6:8]+'-'+e[8:10]+'-'+e[10:12]+'-'+e[12:14]          #取e的后12位，并且每2位中间加'-'
        Mac=Mac2.upper()                                                                   #将字符串的全部之母转换为大写
        LANMac1=g[2:]
        LANMac2=g[2:4]+'-'+g[4:6]+'-'+g[6:8]+'-'+g[8:10]+'-'+g[10:12]+'-'+g[12:14]       #取g的后12位，并且每2位中间加'-'
        LANMac=LANMac2.upper()                                                             #将字符串的全部之母转换为大写 
        USBHostMac1=i[2:]
        USBHostMac2=i[2:4]+'-'+i[4:6]+'-'+i[6:8]+'-'+i[8:10]+'-'+i[10:12]+'-'+i[12:14]   #取i的后12位，并且每2位中间加'-'
        USBHostMac=USBHostMac2.upper()                                                     #将字符串的全部之母转换为大写
        USBDevMac1=g[2:]
        USBDevMac2=g[2:4]+'-'+g[4:6]+'-'+g[6:8]+'-'+g[8:10]+'-'+g[10:12]+'-'+g[12:14]    #取g的后12位，并且每2位中间加'-'
        USBDevMac=USBDevMac2.upper()
        MTAMac=str("C4-45-EC-FF-FF-FF")    
        Used=0        
        import pymysql   #调用pymysql模块
        db = pymysql.connect("192.168.1.45","root","123456","nokeydb")  #连接数据库
        cursor = db.cursor()
        #通过查询判断要写入数据库的Mac是否在数据库里面存在，如果存在就跳过      
        sql = "SELECT * FROM MACINFOTABLE WHERE Mac = '%s'" % Mac
        try :
            cursor.execute(sql)
            print('sql exec ok')
        except:
            print ("sql exec 有问题")
        rows = cursor.fetchall()        
        print("rows len is ", len(rows))           
        if len(rows) == 0:    
                        
            #print ("已有CMMac :",row[1])
            #获取数据库最后一次插入的MacID值
            #sql = "SELECT MacID FROM MACINFOTABLE " 
            #cursor.execute(sql)
            #MacID=cursor.rowcount+1  #数据库的行数+1
            #MacID=cursor.lastrowid
            #print ('MacID=',MacID)
            #向数据库插入数据
            sql = "INSERT INTO MACINFOTABLE (Mac,LANMac,USBHostMac,USBDevMac,MTAMac,PatchNo,PcbNo,Used)\
               VALUES('%s','%s','%s','%s','%s','%s' ,'%s' ,'%s' )"%(Mac,LANMac,USBHostMac,USBDevMac,MTAMac,' ',' ',Used)
            #sql= "insert macinfotable VALUES('%s','%s','%s','%s','%s','%s','%s' ,'%s' ,'%s' )"%(MacID,Mac,LANMac,USBHostMac,USBDevMac,MTAMac,' ',' ',Used)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print('sql exec NG ')
                db.rollback()
            db.close() 
            print ('cmmac:',Mac)
            print ('lanmac:',LANMac)
            print ('usbmac:',USBHostMac)
            print ('************************')
            #print (type(cmmac),type(lanmac),type(usbmac))
            c=c+1
            #MacID=MacID+1
        else:
            print ("Mac重复")
            c=c+1
                
    print (m,'个MAC生成完成')
    
root=Tk()
root.title("NO KEY MAC生成器")
frame=Frame(root)
frame.pack(padx=8,pady=8,ipadx=4)
lab1=Label(frame,text="输入起始MAC：")
lab1.grid(row=0,column=0,padx=5,pady=5,sticky=W)
#绑定对象到Entry
u=StringVar()
#m=StringVar()
ent1=Entry(frame,textvariable=u)
ent1.grid(row=0,column=1,sticky='ew',columnspan=2)
lab2=Label(frame,text="生成MAC的数量：")
lab2.grid(row=1,column=0,padx=5,pady=5,sticky=W)
p=StringVar()
ent2=Entry(frame,textvariable=p)
ent2.grid(row=1,column=1,sticky='ew',columnspan=2)
button=Button(frame,text="确认",command=submit,default='active')
button.grid(row=2,column=1)
#lab3=Label(frame,text="")
#lab3.grid(row=2,column=0,sticky=W)
#button2=Button(frame,text="退出",command=quit)
#button2.grid(row=2,column=2,padx=5,pady=5)
#以下代码居中显示窗口
root.update_idletasks()
x=(root.winfo_screenwidth()-root.winfo_reqwidth())/2
y=(root.winfo_screenheight()-root.winfo_reqheight())/2
root.geometry("+%d+%d"%(x,y))
root.mainloop()

    


