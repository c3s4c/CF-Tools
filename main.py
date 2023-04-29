import os
import sys
import json
import base64
import argparse
import binascii
import urllib.parse
import pyperclip
import threading
import webbrowser
from requests import get
from tkinter import *
from tkinter import ttk
from tkinter  import messagebox
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText

vmscheme = "vmess://"
vlessscheme = "vless://"
cIpsLink = "https://raw.githubusercontent.com/vfarid/cf-clean-ips/main/list.json"
opList = [
    "ایرانسل",
    "همراه اول",
    "مخابرات",
    "رایتل",
    "های وب",
    "آسیاتک",
    "شاتل",
    "پارس آنلاین",
    "مبین نت",
    "اندیشه سبز",
    "رسپینا",
    "افرانت",
    "زی تل",
    "پیشگامان",
    "آراکس",
    "سامانتل",
    "شاتل موبایل",
    "فن آوا",
    "دیده بان نت",
    "آپتل",
    "فناپ تلکام",
    "رای نت"
]
FONT = ("Comic Sans MS",10,"bold")
VERSION = "1.0.0"

def parseLink(link):
    if link.startswith(vmscheme):
        return parseVmess(link)
    elif link.startswith(vlessscheme):
        return parseVless(link)
    else:
        messagebox.showerror("error","ERROR: unsupported line: "+link)
        stateLabel["text"] = "-- Error --"
        stateLabel["bg"] = "red"
        return None


def parseVless(link):
    if link.startswith(vlessscheme):
        uuid = link.split("@")[0].replace(vlessscheme,'')
        add = link.split("@")[1].split(":")[0]
        port = link.replace(vlessscheme,'').split(":")[1].split("?")[0]
        remark = link.replace(vlessscheme,'').split("#")[1]
        qs = urllib.parse.parse_qs(link.split("?")[1].split("#")[0])
        type = qs["type"][0]
        if type=='ws':
            return dict(conType="vless",net="vless",uuid=uuid,add=add,port=port,sni=qs["sni"][0],security=qs["security"][0],type=qs["type"][0],path=qs["path"][0],host=qs["host"][0],remark=remark)
        else:
            return dict(conType="vless",net="vless",uuid=uuid,add=add,port=port,sni=qs["sni"][0],security=qs["security"][0],type=qs["type"][0],serviceName=qs["serviceName"][0],remark=remark)

def parseVmess(vmesslink):
    if vmesslink.startswith(vmscheme):
        bs = vmesslink[len(vmscheme):]
        # paddings
        blen = len(bs)
        if blen % 4 > 0:
            bs += "=" * (4 - blen % 4)

        vms = base64.b64decode(bs).decode()
        js = json.loads(vms)
        js.update({"conType":"vmess"})
        return js
    else:
        raise Exception("vmess link invalid")

def startSer():
    if  len(ipsInput.get("1.0",END)) > 0 and len(configEntry.get()) > 0:
        stateLabel["text"] = "-- Working --"
        stateLabel["bg"] = "orange"
        ips = ipsInput.get("1.0",END).split("\n")
        while '' in ips:
            ips.remove('')
        mconfig = parseLink(configEntry.get())

        outConfigs = []
        for ip in ips:
            config = mconfig
            config["add"] = ip
            if config["conType"] == "vmess":
                new=vmscheme+str(base64.b64encode( json.dumps(config).encode()))
            else:
                if config["type"] == "ws":
                    new=vlessscheme+config["uuid"]+"@"+config["add"]+":"+config["port"]+"?sni="+config["sni"]+"&security="+config["security"]+"&type="+config["type"]+"&path="+config["path"]+"&host="+config["host"]+"#"+config["remark"]
                else:
                    new=vlessscheme+config["uuid"]+"@"+config["add"]+":"+config["port"]+"?sni="+config["sni"]+"&security="+config["security"]+"&type="+config["type"]+"&serviceName="+config["serviceName"]+"#"+config["remark"]
            outConfigs.append(new)
        out=''
        for c in outConfigs:
            if config["conType"] == "vmess":
                out=out+c.replace("b", "",1).replace("'", "")+"\n"
            else:
                out=out+c.replace("'", "")+"\n"
        configOutput.insert(INSERT, out)
        stateLabel["text"] = "-- Done --"
        stateLabel["bg"] = "green"
        
    else:
        messagebox.showerror("error","ip list or config input is empty !")
        stateLabel["text"] = "-- Error --"
        stateLabel["bg"] = "red"

def copyOutPut():
        pyperclip.copy(configOutput.get("1.0", END))

def ipsOpen(): 
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()
    ipsInput.delete(0.0, END)
    ipsInput.insert(0.0, t)

def showVer():
    messagebox.showinfo("INFO",f" Version : {VERSION}")

def configSave():    
        fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
        if fd!= None:
            data = configOutput.get('1.0', END)
        try:
            fd.write(data)
        except:
            messagebox.showerror(title="Error", message = "Not able to save file!")

def whatIsOpr(input):
    if input == opList[0]:
        return 'MTN'
    elif input == opList[1]:
        return 'MCI'
    elif input == opList[2]:
        return 'MKH'
    elif input == opList[3]:
        return 'RTL'
    elif input == opList[4]:
        return 'HWB'
    elif input == opList[5]:
        return 'AST'
    elif input == opList[6]:
        return 'SHT'
    elif input == opList[7]:
        return 'PRS'
    elif input == opList[8]:
        return 'MBT'
    elif input == opList[9]:
        return 'ASK'
    elif input == opList[10]:
        return 'RSP'
    elif input == opList[11]:
        return 'AFN'
    elif input == opList[12]:
        return 'ZTL'
    elif input == opList[13]:
        return 'PSM'
    elif input == opList[14]:
        return 'ARX'
    elif input == opList[15]:
        return 'SMT'
    elif input == opList[16]:
        return 'SHM'
    elif input == opList[17]:
        return 'FNV'
    elif input == opList[18]:
        return 'DBN'
    elif input == opList[19]:
        return 'APT'
    elif input == opList[20]:
        return 'FNP'
    elif input == opList[21]:
        return 'RYN'
    #camel see no see :/ 

def getIpC():
    opr = whatIsOpr(c.get())
    cIpsList =[]
    out = ''
    stateLabel["text"] = "-- Getting IPs... --"
    stateLabel["bg"] = "orange"
    ipsInput.delete("1.0",END)
    try:
        IPs = json.loads(get(cIpsLink).text)
        for ip in IPs["ipv4"]:
            if ip["operator"] == opr:
                cIpsList.append(ip["ip"])
        for ip in cIpsList:
            out=out+(ip+"\n")
        ipsInput.insert(INSERT, out)
        messagebox.showinfo(":)",str(len(cIpsList))+" ip added !")
        stateLabel["text"] = "-- Done --"
        stateLabel["bg"] = "green"
    except Exception as e:
        messagebox.showerror("error","Error : \n "+str(e))
        stateLabel["text"] = "-- Error --"
        stateLabel["bg"] = "red"

def getIpCstarter():
    threading.Thread(target=getIpC).start()

def openCsO():
    webbrowser.open("https://ircfspace.github.io/scanner")

root = Tk()
root.title("C3S4C Tool(config tester)")
#root.configure(background='orange')
root.resizable(0, 0)
root.geometry("525x330")

#menu ---
mMenu = Menu(root)
root.configure(menu=mMenu)
fileMenu = Menu(mMenu, tearoff = False)
mMenu.add_cascade(label='File', menu = fileMenu)
fileMenu.add_command(label='Load IP from file', command =ipsOpen)
fileMenu.add_command(label='Save configs to file', command =configSave)
#---
toolsMenu = Menu(mMenu,tearoff=True)
mMenu.add_cascade(label='Tools',menu = toolsMenu)
toolsMenu.add_command(label='CF IP Scanner online', command = openCsO)
#---
helpMenu = Menu(mMenu, tearoff = False)
mMenu.add_cascade(label='Help', menu = helpMenu)
helpMenu.add_command(label='About', command = showVer)
#---
startButton = Button(root,text=" \n -- START -- \n ",command=startSer)
ipsInput = ScrolledText(root, width = 30, height = 8)
configOutput = ScrolledText(root, width = 30, height = 8)
ipsInputLabel = Label(root,text="- Cloudflare clean IPs :")
configOutputLabel = Label(root,text="- Built configs :")
configOutputButton = Button(root,text="- copy -",command=copyOutPut)
configEntry = Entry(root,borderwidth=2,relief="sunken")
configEntryLabel = Label(root,text="- Your Config :")
stateLabel = Label(root,text="-- Noting --",bg="blue",borderwidth=1, relief="solid")
stateLabelText = Label(root,text="- Status : ")
getIpLabel = Label(root,text="- Need clean IP ? ",font=FONT)
getIpButton = Button(root,text="- Get ",command=getIpCstarter)
#option menu
c = StringVar()
c.set(opList[0])
opsMenu = OptionMenu(root, c, *opList)
#conf
ipsInput.configure(font=FONT)
ipsInputLabel.configure(font=FONT)
configOutput.configure(font=FONT)
configOutputLabel.configure(font=FONT)
configEntryLabel.configure(font=FONT)
startButton.configure(font=FONT)
stateLabel.configure(font=FONT)
stateLabelText.configure(font=FONT)
#---
ipsInput.pack(anchor = "s", side = "left")
ipsInputLabel.place(x=1,y=149)
configOutputButton.place(x=471,y=149)
configOutput.pack(anchor = "s", side = "right")
configOutputLabel.place(x=270,y=149)
configEntry.place(x=120,y=129)
configEntryLabel.place(x=10,y=125)
startButton.place(x=412,y=0)
stateLabel.place(x=80,y=102)
stateLabelText.place(x=1,y=100)
getIpLabel.place(x=2,y=1)
opsMenu.place(x=5,y=25)
getIpButton.place(x=85,y=27)


root.mainloop()
