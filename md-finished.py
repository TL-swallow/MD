from tkinter import *
import tkinter.filedialog
import re
import base64
import requests
from io import BytesIO
import imghdr

root = Tk()
root.title('MD文件在线图片base64转码保存')
root.geometry('380x300')
filedirs = []

def xz():
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:
        string_filename = ""
        for i in range(0,len(filenames)):
            string_filename += str(filenames[i])+"\n"
            filedirs.append(str(filenames[i]))
        lb.config(text = "您选择的文件是：\n"+string_filename)
    else:
        lb.config(text = "您没有选择任何文件")

def getimage(url):
    imgurl = url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"}
    result = requests.request("GET", imgurl, headers=headers)
    ls_f=base64.b64encode(BytesIO(result.content).read())
    imgtype= imghdr.what(None,result.content)
    if imgtype == 'webp': 
        result = 'data:image/jpg;base64,'+str(ls_f.decode('utf8'))
    else:
        result = 'data:image/'+imgtype+';base64,'+str(ls_f.decode('utf8'))
    return result

def main():
    for file in filedirs:
        file_obj = open(file,'r+',encoding='utf-8')
        content = file_obj.read()
        pattern = re.compile(r"!\[.*\]\((.*?)\)")
        rule = pattern.findall(content)
        print('共转化'+str(len(rule))+'张图片')
        for url in rule:
            try:
                result = getimage(url)
                content = content.replace(url,result)
                with open(file,"w",encoding="utf-8") as f:
                    f.write(content)
            except:
                url1 = re.sub(r'////', '//', url)
                result = getimage(url1)
                content = content.replace(url,result)
                with open(file,"w",encoding="utf-8") as f:
                    f.write(content)
    lb.config(text = "转换完成",fg="red",font=("微软雅黑", 24, "bold", "italic"),height=50,width=100)

lb = Label(root,text = '')
lb.pack()
btn = Button(root,text="选择MD文件",command=xz,font=("微软雅黑", 18))
btn.pack()
startbtn = Button(root,text="开始转换",command=main,font=("微软雅黑", 18))
startbtn.pack()
root.mainloop()