# encoding: UTF-8

import os
import threading
import time
import shutil
import configparser

from tkinter import *

from tkinter import messagebox
# 导入ttk
from tkinter import ttk
# 导入filedialog
from tkinter import filedialog

class Application:
	def __init__(self,master):
		master.title('Easy Copy')
		self.master = master
		self.initWidgets()
		
	def initWidgets(self):
		self.initConfigFiles()
		self.initDisp()
		self.initButtons()
		
	def initDisp(self):
		f=Frame(self.master)
		f.pack(side=LEFT)
		self.TextStrBuf=''
		Label(f, text='运行日志:', font=('', 10)).pack(side=LEFT)
		self.text = Text(f, width=70, height=10, padx=10, font=('', 10), bg='#FFFFFF', foreground='black')
		#self.text.insert(1.0, 'hello\nhello')
		self.text.config(state=DISABLED)
		self.text.pack(side=LEFT, fill=BOTH, expand=YES)	
		self.RefreshDisp()
		
	def initConfigFiles(self):
		self.cfg = ReadIni('cfg.ini')
		self.filenames = self.cfg.get_options('CopyFiles')
		self.dstPath=''
		var = self.cfg.get_options('CopyPath')
		if len(var):
			self.dstPath = var[0]

		self.VarDstPath=StringVar()
		
		f=Frame(self.master)
		f.pack(side=TOP, anchor=SW)
		Label(f, text='当前拷贝文件路径:', font=('', 10)).pack(side=LEFT)
		self.CopyText = Text(f, width=60, height=8, padx=10, font=('', 10), bg='#F0F0F0')
		self.CopyText.pack(side=TOP, fill=BOTH, expand=YES)
		Label(f, textvariable=self.VarDstPath, font=('', 10)).pack(side=LEFT)
		self.VarDstPath.set('目标路径:'+ self.dstPath)
		self.RefreshDispCopyFiles()
		
		
		
	def initButtons(self):
		self.VarRunStr = StringVar()
		self.stop = True
		self.VarRunStr.set('Stop')
		
		f=Frame(self.master)
		f.pack(side=RIGHT)
		ttk.Button(f, text='手动拷贝', command=self.CopyFile).pack(side=BOTTOM, fill=Y, expand=YES)
		ttk.Button(f, text='选择拷贝文件', command=self.OpenConfigFiles).pack(side=BOTTOM, fill=Y, expand=YES)
		ttk.Button(f, text='选择目标路径', command=self.OpenCopyPath).pack(side=BOTTOM, fill=Y, expand=YES)
		ttk.Button(f, text='停止', command=self.Stop).pack(side=BOTTOM, fill=Y, expand=YES)
		ttk.Button(f, text='启动', command=self.Start).pack(side=BOTTOM, fill=Y, expand=YES)
		Label(f, textvariable=self.VarRunStr, font=('', 13), fg='blue').pack(side=BOTTOM)
		self.RefreshDisp()	
		
#------------------init  END-------------------------------------------	
	def RefreshDisp(self):
		self.text.config(state=NORMAL)
		self.text.insert(1.0, '')
		#for i in range(len(self.TextStrBuf)) :
		#print('{} : {}'.format(i, self.TextStrBuf[i]))
		print(len(self.TextStrBuf))
		self.text.insert(INSERT, self.TextStrBuf)
		self.text.config(state=DISABLED)

			
	def RefreshDispCopyFiles(self):
		TmpStr = ''
		self.CopyText.config(state=NORMAL)
		print('files num : %d' % len(self.filenames))
		for i in range(len(self.filenames)):
			print('{}: {}'.format(i, self.filenames[i]))
			TmpStr = TmpStr + self.filenames[i] + '\n'
		print(TmpStr)
		self.CopyText.delete(1.0, 'end')
		self.CopyText.insert(1.0, TmpStr)
		self.CopyText.config(state=DISABLED)
	
	def ShowCopyMessage(self, info):
		messagebox.showinfo("Info", info)
	
	def CopyFile_1(self, src, dst):
		shutil.copy(src, dst)
		return True
		
	def CopyFile_2(self, src, dst):
		src = src.replace('/', '\\')				
		dst = dst.replace('/', '\\')
		os.system ('copy \"{}\" \"{}\"'.format(src, dst))
		return True
		
	def CopyFile_3(self, src, dst):
		dst = dst + '/' + src.split("/")[-1]
		src_size = os.path.getsize(src)
		print(src_size)
		if src_size > 1024*1024*100:
			src_size = 1024*1024*100	#max size 100 Mb
		f_dst = open(dst, 'wb')
		f_src = open(src, 'rb')
		print('>>> %s to %s' % (src, dst))
		print(f_src)
		print(f_dst)
		try:
			while True:
				data = f_src.read(src_size)
				if len(data)==0:
					break
				f_dst.write(data)
			return True
		except : 
			return False
		finally:
			print('end')
			f_dst.close()
			f_src.close()
			
		
	def CopyFile(self):
		ret = False
		src = ''
		dst = ''
		if os.path.exists(self.dstPath) is False:
			print('{} is not valid!!'.format(self.dstPath))
			return None
		for i in range(len(self.filenames)):
			if self.filenames[i]:
				src = self.filenames[i]
				dst = self.dstPath
				
				#ret = self.CopyFile_1(src, dst)
				#ret = self.CopyFile_2(src, dst)
				ret = self.CopyFile_3(src, dst)
				
				if ret:
					self.SetFlushLog('Copy {} to {}\n'.format(src, dst), 'green')
					self.ShowCopyMessage('拷贝成功')	
				else:
					self.SetFlushLog('Copy {} to {} fail!\n'.format(src, dst), 'red')
					self.ShowCopyMessage('拷贝失败')	
				print('Copy {} to {}'.format(self.filenames[i], self.dstPath))
		return None
			
		
	def OpenConfigFiles(self):
		self.filenames=filedialog.askopenfilenames(title='选择拷贝文件', filetypes=[("拷贝文件","*")],
		initialdir=os.getcwd())
		if len(self.dstPath)<=0:
			self.SetFlushLog('files is not open!!!\n', 'red')
			return None
		print(self.filenames)
		self.cfg.del_options('CopyFiles')
		self.RefreshDispCopyFiles()
		for i in range(len(self.filenames)):
			self.cfg.set_value('CopyFiles', str(i), self.filenames[i])
		self.cfg.save_cfg()
		
	def OpenCopyPath(self):
		path='目标路径:'
		self.dstPath = filedialog.askdirectory(title='复制到', initialdir=os.getcwd())
		if len(self.dstPath)<=0:
			self.SetFlushLog('Path is invalid!!!\n', 'red')
			return None
		path=path + self.dstPath
		print(path)
		self.cfg.del_options('CopyPath')
		self.VarDstPath.set(path)
		self.cfg.set_value('CopyPath', 'path', self.dstPath)
		self.cfg.save_cfg()
	
	def SetFlushLog(self, str, color='#000000'):
		#self.text['fg']=color
		str_time = time.strftime('[%Y-%m-%d %H:%M:%S]\n')
		self.TextStrBuf = str + str_time
		self.RefreshDisp()
		
	def Start(self):
		print('start run...')
		self.SetFlushLog('start run...\n')
		self.stop = False
				
		if self.stop:
			self.VarRunStr.set('Stop')
		else:
			self.VarRunStr.set('Run')
		
	def Stop(self):
		print('Stop run...')
		self.SetFlushLog('Stop run...\n')
		self.stop = True	
		if self.stop:
			self.VarRunStr.set('Stop')
		else:
			self.VarRunStr.set('Run')
	
	def GetCopyFiles(self):
		return self.filenames

	def GetDstPath(self):
		return self.dstPath
		
	def GetStopFlag(self):
		return self.stop	
		
class FileOperation:
	def __init__(self):
		self.filesModifyTime = []
		
	def CheckCopyFiles(self, app):
		if app.GetStopFlag():
			return None
		files=()
		filesTime=[]
		files = app.GetCopyFiles()
		path = app.GetDstPath()
		result=[x*0 for x in range(len(files))]
		filesTime=[x*0 for x in range(len(files))]
		
		num = len(files) - len(self.filesModifyTime)
		if num > 0:
			self.filesModifyTime.extend([x for x in range(num)])
		
		if os.path.exists(path) is False:
			#print('path is not valid!!')
			return None
			
		for i in range(len(files)):
			filesTime[i]=os.path.getmtime(files[i])
			print('file :{} [{} {}]'.format(files[i], filesTime[i], self.filesModifyTime[i]))
			if filesTime[i] > self.filesModifyTime[i]:
				self.filesModifyTime[i] = filesTime[i]
				result[i]= 1

		for i in range(len(result)):
			if result[i]:
				#app.TextStrBuf = 'Copy {} to {}\n'.format(files[i], path)
				#app.RefreshDisp()
				#print('Copy {} to {}'.format(files[i], path))
				app.CopyFile()

class ReadIni(object):
	def __init__(self,file_name=None,node=None):
		if file_name == None:
			file_name = 'cfg.ini'
		else:
			self.file_name=file_name
		if node == None:
			self.node = "CopyFiles"
		else:
			self.node = node
		self.cf = self.load_ini(file_name)
		if self.cf.has_section('CopyFiles')==False:
			self.cf.add_section('CopyFiles')
		if self.cf.has_section('CopyPath')==False:
			self.cf.add_section('CopyPath')
			
	def load_ini(self,file_name):
		cf = configparser.ConfigParser()
		cf.read(file_name,encoding='utf-8')
		return cf

	def save_cfg(self):
		self.cf.write(open(self.file_name, 'w'))
		
	def get_value(self, node, key):
		data = self.cf.get(node,key)
		return data
		
	def set_value(self, node, option, key):
		self.cf.set(node, option, key)

	def get_options(self, node):
		value=[]
		key=self.cf.options(node)
		for i in range(len(key)):
			value.append(self.get_value(node, key[i]))
		return tuple(value)

	def del_options(self, node):
		key=self.cf.options(node)
		for i in range(len(key)):
			self.cf.remove_option(node, key[i])
		
def timer_run():
	#print('1s timer is run...')
	gFileOpt.CheckCopyFiles(gApp)
	if quit==False :
		threading.Timer(1, timer_run) .start()
	
if __name__ == '__main__':
	quit = False
	timer = threading.Timer(1, timer_run)
	timer.start()
	
	root = Tk()
	gApp = Application(root)
	gFileOpt = FileOperation()
	try:
		root.mainloop()
	finally:
		quit = True
	
