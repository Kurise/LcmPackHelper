#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import os
import shutil
import tkFileDialog
import subprocess
import threading
import xml.dom.minidom

from Tkinter import *
from tkinter import messagebox
from tkinter import ttk

reload(sys)
sys.setdefaultencoding('utf-8')


class Manifest(object):
    def __init__(self, filePath):
        self.filePath = filePath

    def getElementTree(self,filePath):
        dom = xml.dom.minidom.parse(filePath)
        root = dom.documentElement
        return root

    # 获取包名
    def getPackage(self,root):
        list = root.getAttribute('package')
        return list

    def change(slef,filePath, old, new):
        with open(filePath) as f:
            s = f.read()
            old = old.encode('utf-8').strip()
            new = new.encode('utf-8').strip()
            s = s.replace(old, new)
        with open(filePath, "w") as f:
            f.write(s)



def MyThread(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


class tabMainFrame(object):
    def __init__(self,tab,value):
        if value == 'tab0':
            self.tab0Frame(tab)
        elif value == 'tab1':
            self.tab1Frame(tab)
        elif value == 'tab2':
            self.tab2Frame(tab)

    def tab0Frame(self,tab):
        frm1 = Frame(tab)
        self.decompile_apk_path = StringVar()
        Label(frm1, text="目标路径:").grid(row=1, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.decompile_apk_path).grid(row=1, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择APK", command=self.get_apk_path).grid(row=1, column=2, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="开始解包", command=lambda: MyThread(self.decompile_apk1)).grid(row=1, column=3, padx=2, pady=2, ipadx=2, ipady=2)

        self.recompile_apk_path = StringVar()
        Label(frm1, text="目标路径:").grid(row=2, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.recompile_apk_path).grid(row=2, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择目录", command=self.get_apk_file).grid(row=2, column=2, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="开始合包", command=lambda: MyThread(self.recompile_apk1)).grid(row=2, column=3, padx=2, pady=2, ipadx=2, ipady=2)

        self.apk_to_jar_path = StringVar()
        Label(frm1, text="目标路径:").grid(row=3, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.apk_to_jar_path).grid(row=3, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择APK", command=self.get_apk_to_jar_path).grid(row=3, column=2, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="APK->JAR", command=lambda: MyThread(self.apk_to_jar)).grid(row=3, column=3, padx=2, pady=2, ipadx=2, ipady=2)

        self.resign_apk_path = StringVar()
        Label(frm1, text="待签APK:").grid(row=4, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.resign_apk_path).grid(row=4, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择APK", command=self.get_apk_unresign).grid(row=4, column=2, padx=2, pady=2, ipadx=2, ipady=2)

        frm1.grid(row=1, column=0, rowspan=1, columnspan=4, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

        frm2 = Frame(tab)
        Label(frm2, text="签名文件:").grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W, padx=2, pady=2, ipadx=2,ipady=2)
        self.var = StringVar()
        self.var.set('1')
        Radiobutton(frm2, text='denachina', variable=self.var, value=1, command=self.var.get()).grid(row=1, column=1, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denacn', variable=self.var, value=2, command=self.var.get()).grid(row=1, column=2, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denatw', variable=self.var, value=3, command=self.var.get()).grid(row=1, column=3, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='当乐', variable=self.var, value=4, command=self.var.get()).grid(row=1, column=4, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='棱镜', variable=self.var, value=5, command=self.var.get()).grid(row=1, column=5, rowspan=1,columnspan=1, sticky=W)
        Button(frm2, text="开始签名", command=lambda: MyThread(self.resign_apk1)).grid(row=2, column=2, padx=3, pady=2, ipadx=2, ipady=2)
        frm2.grid(row=2, column=0, rowspan=1, columnspan=4, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

    def tab1Frame(self,tab):
        frm1 = Frame(tab)
        self.apk_path = StringVar()
        Label(frm1, text="目标路径:").grid(row=1, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.apk_path).grid(row=1, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择APK", command=self.get_apk_dir).grid(row=1, column=2, padx=2, pady=2, ipadx=2, ipady=2)

        self.change_str = StringVar()
        Label(frm1, text="替换字符:").grid(row=2, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.change_str).grid(row=2, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        self.change_str.set('PACKAGE_NAME')

        frm1.grid(row=1, column=0, rowspan=1, columnspan=4, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

        frm2 = Frame(tab)
        Label(frm2, text="签名文件:").grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W, padx=2, pady=2, ipadx=2,ipady=2)
        self.var1 = StringVar()
        self.var1.set('1')
        Radiobutton(frm2, text='denachina', variable=self.var1, value=1, command=self.var1.get()).grid(row=1, column=1, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denacn', variable=self.var1, value=2, command=self.var1.get()).grid(row=1, column=2, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denatw', variable=self.var1, value=3, command=self.var1.get()).grid(row=1, column=3, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='当乐', variable=self.var1, value=4, command=self.var1.get()).grid(row=1, column=4, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='棱镜', variable=self.var1, value=5, command=self.var1.get()).grid(row=1, column=5, rowspan=1,columnspan=1, sticky=W)

        Label(frm2, text="易盾加密:").grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W, padx=2, pady=2, ipadx=2,ipady=2)
        self.var2 = StringVar()
        self.var2.set('1')
        Radiobutton(frm2, text='不加密', variable=self.var2, value=1, command=self.var2.get()).grid(row=2, column=1, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='no dex', variable=self.var2, value=2, command=self.var2.get()).grid(row=2, column=2, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='dex', variable=self.var2, value=3, command=self.var2.get()).grid(row=2, column=3, rowspan=1,columnspan=1, sticky=W)
        self.var3 = StringVar()
        self.var3.set("开始处理")  # 初始的按钮文本
        Button(frm2,textvariable=self.var3,activebackground='brown',activeforeground='black', command=lambda :MyThread(self.modify_single_apk)).grid(row=3, column=2, rowspan=1, columnspan=4, sticky=W, padx=2,pady=2, ipadx=2, ipady=2)
        frm2.grid(row=2, column=0, rowspan=1, columnspan=6, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

    def tab2Frame(self,tab):
        frm1 = Frame(tab)
        self.apk_path_dir = StringVar()
        Label(frm1, text="目标路径:").grid(row=1, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.apk_path_dir).grid(row=1, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        Button(frm1, text="选择目录", command=self.get_apks_dir).grid(row=1, column=2, padx=2, pady=2, ipadx=2, ipady=2)

        self.change_str = StringVar()
        Label(frm1, text="替换字符:").grid(row=2, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        Entry(frm1, textvariable=self.change_str).grid(row=2, column=1, padx=2, pady=2, ipadx=2, ipady=2)
        self.change_str.set('PACKAGE_NAME')

        frm1.grid(row=1, column=0, rowspan=1, columnspan=4, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

        frm2 = Frame(tab)
        Label(frm2, text="签名文件:").grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W, padx=2, pady=2, ipadx=2,ipady=2)
        self.var1 = StringVar()
        self.var1.set('1')
        Radiobutton(frm2, text='denachina', variable=self.var1, value=1, command=self.var1.get()).grid(row=1, column=1, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denacn', variable=self.var1, value=2, command=self.var1.get()).grid(row=1, column=2, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='denatw', variable=self.var1, value=3, command=self.var1.get()).grid(row=1, column=3, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='当乐', variable=self.var1, value=4, command=self.var1.get()).grid(row=1, column=4, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='棱镜', variable=self.var1, value=5, command=self.var1.get()).grid(row=1, column=5, rowspan=1,columnspan=1, sticky=W)

        Label(frm2, text="易盾加密:").grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W, padx=2, pady=2, ipadx=2,ipady=2)
        self.var2 = StringVar()
        self.var2.set('1')
        Radiobutton(frm2, text='不加密', variable=self.var2, value=1, command=self.var2.get()).grid(row=2, column=1, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='no dex', variable=self.var2, value=2, command=self.var2.get()).grid(row=2, column=2, rowspan=1,columnspan=1, sticky=W)
        Radiobutton(frm2, text='dex', variable=self.var2, value=3, command=self.var2.get()).grid(row=2, column=3, rowspan=1,columnspan=1, sticky=W)
        self.var3 = StringVar()
        self.var3.set("开始处理")  # 初始的按钮文本
        Button(frm2,textvariable=self.var3,activebackground='brown',activeforeground='black', command=lambda :MyThread(self.modify_apks)).grid(row=3, column=2, rowspan=1, columnspan=4, sticky=W, padx=2,pady=2, ipadx=2, ipady=2)
        frm2.grid(row=2, column=0, rowspan=1, columnspan=6, sticky=W, padx=2, pady=2, ipadx=2, ipady=2)

    def get_apk_dir(self):
        self.apk_path.set(tkFileDialog.askopenfilename(filetypes=[("bmp格式".decode('gbk'), "apk")]))
        self.var3.set("开始处理")
        return self.apk_path

    def get_apk_path(self):
        apk_path = tkFileDialog.askopenfilename(filetypes=[("bmp格式".decode('gbk'), "apk")])
        self.decompile_apk_path.set(apk_path)
        return apk_path

    def get_apk_to_jar_path(self):
        apk_path = tkFileDialog.askopenfilename(filetypes=[("bmp格式".decode('gbk'), "apk")])
        self.apk_to_jar_path.set(apk_path)
        return apk_path

    def get_apk_unresign(self):
        apk_path = tkFileDialog.askopenfilename(filetypes=[("bmp格式".decode('gbk'), "apk")])
        self.resign_apk_path.set(apk_path)
        return apk_path

    def get_apks_dir(self):
        apk_path = tkFileDialog.askdirectory()
        self.apk_path_dir.set(apk_path)
        self.var3.set("开始处理")
        return apk_path

    def get_apk_file(self):
        apk_path = tkFileDialog.askdirectory()
        self.recompile_apk_path.set(apk_path)
        return apk_path

    def find_apk(self):
        apks_path = self.apk_path_dir.get() + '/'
        apklist = []
        for filename in os.listdir(apks_path):
            if filename.endswith('.apk'):
                apklist.append(os.path.join(apks_path, filename).encode('utf-8'))
        return apklist


    def modify_single_apk(self):
        self.var3.set('处理中，进度：5%')
        # 解包
        self.decompile_apk(self.apk_path.get())
        self.var3.set('处理中，进度：30%')
        game_dir = os.path.splitext(self.apk_path.get())[0]
        print (game_dir)
        # 修改manifest特定字符
        self.modify_manifest(game_dir)
        self.var3.set('处理中，进度：50%')
        # 合包
        self.recompile_apk(game_dir)
        self.var3.set('处理中，进度：75%')
        # 签名apk
        dist_dir = os.path.join(game_dir, 'dist/')
        print (dist_dir)
        dirs = os.listdir(dist_dir)
        for dir1 in dirs:
            print (dir1)
        dis_apk = os.path.join(dist_dir, dir1)
        print ('dis_dir:%s' % dis_apk)
        print ('dist_dir:%s' % dist_dir)
        self.yidun_apk(dist_dir, dis_apk)
        self.var3.set('处理中，进度：85%')
        self.resign_apk(game_dir, dis_apk, dir1,'single')
        self.var3.set('处理中，进度：100%')
        messagebox.showinfo(title='single APK', message='处理完成')

    def modify_apks(self):
        print (u'----------------------------------程序  start--------------------------------------------')
        self.var3.set('处理中，进度：5%')
        for apk in self.find_apk():
            print(apk)
            self.modify_multiple_apk(apk)
        print (u'----------------------------------程序  end--------------------------------------------')
        self.var3.set('所有任务完成')
        messagebox.showinfo(title='Multiple APK', message='所有任务完成')


    def modify_multiple_apk(self,apk):
        final_dir = self.apk_path_dir.get() + '/final_dir'
        self.apk_path_dir.get() + '/'
        print(os.path.exists(final_dir))
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)
        print('final_dir:%s' % final_dir)
        # 解包
        self.decompile_apk(apk)
        self.var3.set('处理中，进度：30%')
        game_dir = os.path.splitext(apk)[0]
        print (u'game_dir:%s' % game_dir)
        # 修改manifest特定字符
        self.modify_manifest(game_dir)
        self.var3.set('处理中，进度：50%')
        # 合包
        self.recompile_apk(game_dir)
        self.var3.set('处理中，进度：75%')
        dist_dir = os.path.join(game_dir, 'dist/')
        print (u'%s' % dist_dir)
        dirs = os.listdir(dist_dir)
        for dir1 in dirs:
            print (u'%s' % dir1)
        dis_apk = os.path.join(dist_dir, dir1)
        print (u'%s' % dis_apk)
        self.yidun_apk(dist_dir, dis_apk)
        self.var3.set('处理中，进度：85%')
        # 签名apk
        self.resign_apk(final_dir, dis_apk, dir1,'multiple')
        self.var3.set('处理中，进度：95%')
        if os.path.isdir(game_dir):
            shutil.rmtree(game_dir)
        if os.path.exists(apk):
            os.remove(apk)
        self.var3.set('完成，进度：100%')

    # 解包apk
    def decompile_apk1(self):
        getApktoolPath = 'java -jar ' + os.getcwd() + '/dex-tools-2.1-SNAPSHOT/lib/apktool.jar'
        subprocess.check_output(getApktoolPath + ' d -f %s -o %s' % (self.decompile_apk_path.get(), os.path.splitext(self.decompile_apk_path.get())[0]), shell=True,stderr=subprocess.STDOUT)
        messagebox.showinfo(title='解包apk', message='解包完成')

    # 解包apk
    def decompile_apk(self,apk):
        if apk.strip() == '':
            messagebox.showwarning(title='温馨提醒', message='请选择一个APK')
        getApktoolPath = 'java -jar ' + os.getcwd() + '/dex-tools-2.1-SNAPSHOT/lib/apktool.jar'
        subprocess.check_output(getApktoolPath + ' d -f %s -o %s' % (apk, os.path.splitext(apk)[0]), shell=True,stderr=subprocess.STDOUT)

    # 合包apk
    def recompile_apk1(self):
        getApktoolPath = 'java -jar ' + os.getcwd() + '/dex-tools-2.1-SNAPSHOT/lib/apktool.jar'
        subprocess.check_output(getApktoolPath + ' b %s' % self.recompile_apk_path.get(), shell=True,stderr=subprocess.STDOUT)
        messagebox.showinfo(title='合包apk', message='合包完成')

    # 合包apk
    def recompile_apk(self,game_dir):
        getApktoolPath = 'java -jar ' + os.getcwd() + '/dex-tools-2.1-SNAPSHOT/lib/apktool.jar'
        subprocess.check_output(getApktoolPath + ' b %s' % game_dir, shell=True, stderr=subprocess.STDOUT)

    # apk转jar
    def apk_to_jar(self):
        get_dex2jar_path = os.getcwd() + '/dex-tools-2.1-SNAPSHOT/d2j-dex2jar.sh '
        get_jd_gui_path = 'java -jar ' + os.getcwd() + '/dex-tools-2.1-SNAPSHOT/lib/jd-gui-1.4.0.jar '
        print('apk_to_jar：', get_dex2jar_path)
        subprocess.check_output(get_dex2jar_path + '%s -o %s' % (
        self.apk_to_jar_path.get(), os.path.splitext(self.apk_to_jar_path.get())[0] + '.jar'), shell=True,stderr=subprocess.STDOUT)
        subprocess.check_output(get_jd_gui_path + '%s' % (os.path.splitext(self.apk_to_jar_path.get())[0] + '.jar'),shell=True, stderr=subprocess.STDOUT)

    # 修改manifest
    def modify_manifest(self,dir):
        game_manifest = os.path.join(dir, 'AndroidManifest.xml')
        print('modify_manifest:%s' % game_manifest)
        manifest = Manifest(game_manifest)
        old = self.change_str.get()
        print (old)
        new = manifest.getPackage(manifest.getElementTree(game_manifest))
        manifest.change(game_manifest, old, new)

    def yidun_apk(self,dist_dir, dis_apk):
        print ('yidun_apk')
        print('var2：', self.var2.get())
        appkey = '47e6808e77ae4a8d9ce1a7b830f4a151b7c0'
        getNHPProtectPath = 'java -jar ' + os.getcwd() + '/NHPProtect.jar'
        if self.var2.get() == '1':
            print ('no need to yidun_apk')
            return
        elif self.var2.get() == '2':
            subprocess.check_output(getNHPProtectPath + ' -appkey %s -yunconfig -input %s' % (appkey, dis_apk),shell=True, stderr=subprocess.STDOUT)
        elif self.var2.get() == '3':
            subprocess.check_output(getNHPProtectPath + ' -appkey %s -yunconfig -dex -input %s' % (appkey, dis_apk),shell=True, stderr=subprocess.STDOUT)

        baseName = os.path.basename(dis_apk)
        print baseName
        for item in os.listdir(dist_dir):
            if item.endswith('_encrypted.apk'):
                os.remove(dis_apk)
                os.rename(os.path.join(dist_dir, item), os.path.join(dist_dir, baseName))
                return

    # 签名apk
    def resign_apk(self,game_dir, dis_dir, dir1,value):
        print('resign_apk')
        print('var1：', self.var1.get())
        if self.var1.get() == '1':
            keystore = os.getcwd() + '/keystore/denachina.keystore'
            password = 'denadena01'
            keypass = 'denadena01'
            alias = 'dena'
        elif self.var1.get() == '2':
            keystore = os.getcwd() + '/keystore/denacn.keystore'
            password = 'denacn'
            keypass = 'denacn'
            alias = 'denacn'
        elif self.var1.get() == '3':
            keystore = os.getcwd() + '/keystore/denatw.keystore'
            password = 'denatw'
            keypass = 'denatw'
            alias = 'denatw'
        elif self.var1.get() == '4':
            keystore = os.getcwd() + '/keystore/downjoy_395_VIJjEhlRLBn72Xq.keystore'
            password = 'downjoy_395'
            keypass = 'downjoy_395'
            alias = '395'
        elif self.var1.get() == '5':
            keystore = os.getcwd() + '/keystore/6d5f6fd2fe3546598cf8b4f001977953.keystore'
            password = 'A4Qi00'
            keypass = 'cn7J99'
            alias = 'zhengyuekeji'
        else:
            messagebox.showwarning(title='签名信息', message='请选择一个签名文件')
        print('keystore：', keystore)
        if value == 'single':
            out_dir = os.path.dirname(os.path.realpath(game_dir)) + '/' + alias + '-' + dir1
        elif value == 'multiple':
            out_dir = game_dir + '/' + alias + '-' + dir1
        print (out_dir)
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        subprocess.check_output('jarsigner -digestalg SHA1 -sigalg MD5withRSA -verbose -keystore %s -storepass %s -keypass %s -signedjar %s %s %s' % (keystore, password, keypass, out_dir, dis_dir, alias), shell=True, stderr=subprocess.STDOUT)
        if os.path.isdir(game_dir) and value == 'single':
            shutil.rmtree(game_dir)

    # 签名apk
    def resign_apk1(self):
        print('var：', self.var.get())
        if self.var.get() == '1':
            keystore = os.getcwd() + '/keystore/denachina.keystore'
            password = 'denadena01'
            keypass = 'denadena01'
            alias = 'dena'
        elif self.var.get() == '2':
            keystore = os.getcwd() + '/keystore/denacn.keystore'
            password = 'denacn'
            keypass = 'denacn'
            alias = 'denacn'
        elif self.var.get() == '3':
            keystore = os.getcwd() + '/keystore/denatw.keystore'
            password = 'denatw'
            keypass = 'denatw'
            alias = 'denatw'
        elif self.var.get() == '4':
            keystore = os.getcwd() + '/keystore/downjoy_395_VIJjEhlRLBn72Xq.keystore'
            password = 'downjoy_395'
            keypass = 'downjoy_395'
            alias = '395'
        elif self.var.get() == '5':
            keystore = os.getcwd() + '/keystore/6d5f6fd2fe3546598cf8b4f001977953.keystore'
            password = 'A4Qi00'
            keypass = 'cn7J99'
            alias = 'zhengyuekeji'
        else:
            messagebox.showinfo(title='签名信息', message='请选择一个签名文件')
        print('keystore：', keystore)
        sign_apk_path = os.path.splitext(self.resign_apk_path.get())[0] + '_' + alias + '_sign.apk'
        subprocess.check_output('jarsigner -digestalg SHA1 -sigalg MD5withRSA -verbose -keystore %s -storepass %s -keypass %s -signedjar %s %s %s' % (keystore, password, keypass, sign_apk_path, self.resign_apk_path.get(), alias), shell=True,stderr=subprocess.STDOUT)
        messagebox.showinfo(title='签名apk', message='签名完成，签名文件别名：' + alias)


class Application(object):
    def __init__(self):
        window = Tk()
        window.title('LcmPackHelper')
        window.geometry('520x400+1200+200')
        window.resizable(width=True, height=True)
        self.MainFrame(window)
        window.mainloop()

    def MainFrame(self,window):
        tabControl = ttk.Notebook(window)

        tab0 = ttk.Frame(tabControl)
        tabControl.add(tab0, text='APK Tool')
        tabMainFrame(tab0,'tab0')
        
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Single APK')
        tabMainFrame(tab1,'tab1')

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Multiple APK')
        tabMainFrame(tab2,'tab2')

        tabControl.pack(expand=1, fill="both")

    #主入口
Application()
