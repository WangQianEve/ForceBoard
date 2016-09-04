#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1.重新写一个time对应force的文件，画个图出来

# 2.字母表 每个用户一张表，整体一张表 时间26-列力度0-25一列 60列一组
	# log表 每个用户6行
		# 第一行记录所有长度
		# 第二行算平均时间
		# 第三行平均力度
		# 第4-6行空出来是每个字母的分布数据
	
# 3.choose_time 整体一张表 也记录del
	# 如果是true，读够了以后记下时间，到最后一次tap结束，算出间隔
import  xdrlib ,sys
import xlwt,xlrd
from xlrd import open_workbook
from xlutils.copy import copy
# raw_input='data\chengzijie_1471512278'
# user_id=0
# raw_input='data\yumingke_1472348880'
# user_id=0
# raw_input='data\guyizheng_1471945015'
# user_id=1
raw_input='data\zmy_1472063859'
user_id=2

lines=[]

def ini_files():
	wb=xlwt.Workbook()
	ws=wb.add_sheet('sheet1',cell_overwrite_ok=True)
	wb.save("user.xls")
	wb.save("correct.xls")
	wb.save("delete.xls")
	wb.save("choose.xls")
	for i in range(26*6):
		ws.write(0,i,0)
	wb.save("log.xls")

def modify():
	fint=open(raw_input+'_t.txt','r')
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		if '[' in lines[i]:
			lines[i]=lines[i].replace('[','[\n')
		if ']' in lines[i]:
			lines[i]=lines[i].replace(']','\n]')
		if ',' in lines[i]:
			lines[i]=lines[i].replace(',','\n')
		if ' ' in lines[i]:
			lines[i]=lines[i].replace(' ','')
	fout=open('./data/'+chr(48+user_id)+'_t.txt','w')
	fout.writelines(lines)
	fout.close()
	
def modify1():
	fint=open(raw_input+'_c.txt','r')
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		if ',' in lines[i]:
			lines[i]=lines[i].replace(',','\n')
		if ' ' in lines[i]:
			lines[i]=lines[i].replace(' ','')
	fout=open('./data/'+chr(48+user_id)+'_c.txt','w')
	fout.writelines(lines)
	fout.close()

def read_data():
	global lines
	fint=open('./data/'+chr(48+user_id)+'_t.txt','r')
	lines=fint.readlines()
	fint.close()

def read_data1():
	global lines
	fint=open('./data/'+chr(48+user_id)+'_c.txt','r')
	lines=fint.readlines()
	fint.close()
	
def write_data():
	wb=xlwt.Workbook()
	ws=wb.add_sheet(chr(user_id+48),cell_overwrite_ok=True)
	flag=True
	time=0
	pressure=0
	for i in range(len(lines)):
		lines[i]=lines[i].strip()
		if lines[i]=='[':
			continue
		if lines[i]==']':
			flag=not flag
			continue
		if flag:
			ws.write(time,0,float(lines[i]))
			time+=1
		else:
			ws.write(pressure,1,float(lines[i]))
			pressure+=1
	lines.clear()
	wb.save("timeline.xls")

def write_data1():
	global lines
	old_log_wb=open_workbook('log.xls')
	old_log_ws=old_log_wb.sheet_by_index(0)
	log_wb=copy(old_log_wb)
	log_ws=log_wb.get_sheet(0)
	
	old_user_wb=open_workbook('user.xls')
	user_wb=copy(old_user_wb)
	user_ws=user_wb.get_sheet(0)
	
	old_delete_wb=open_workbook('delete.xls')
	delete_wb=copy(old_delete_wb)
	delete_ws=delete_wb.get_sheet(0)

	old_choose_wb=open_workbook('choose.xls')
	choose_wb=copy(old_choose_wb)
	choose_ws=choose_wb.get_sheet(0)
	
	old_correct_wb=open_workbook('correct.xls')
	correct_wb=copy(old_correct_wb)
	correct_ws=correct_wb.get_sheet(0)

	wb=xlwt.Workbook()
	ws=wb.add_sheet('alphabets',cell_overwrite_ok=True)

	#raw_info
	word=""
	length=0
	correct=""
	begin=0.0
	end=0.0
	pressure=0.0
	#my info
	total_input=0
	word_index=0
	input=-1
	group=0
	count=0
	current_user_index=[0 for i in range(26*4)]
	user_index=old_log_ws.row_values(0)
	choose_index=[0,0,0]
	delete_index=0
	#each word
	i=0
	i_t=len(lines)
	while i<i_t:
		choose_start=0.0
		choose_end=0.0
		word=lines[i].strip()
		word_index=0
		word_length=len(word)
		i+=1
		length=int(lines[i].strip())
		i+=1
		correct=lines[i].strip()
		i+=1
		#计算正确率 以及分组
		total_input+=1
		if correct=="true":
			count+=1
			if count==32:
				count=0
				correct_ws.write(user_id,group,total_input)
				total_input=0
				group+=1
				if group==2:
					break
		#each character
		# print(word)
		for k in range(length):#输入次数
			begin=float(lines[i].strip())
			i+=1
			end=float(lines[i].strip())
			i+=1
			pressure=float(lines[i].strip())
			i+=1
			if pressure==-5.0:
				# print('tap')
				pass
			elif pressure>=(33.0*0.99):#写delete表
				# print('delete')
				delete_ws.write(delete_index , user_id , end-begin)
				delete_index+=1
				word_index=max(word_index-1,0)
			else:
				try:
					input=ord(word[word_index])-ord('a')#0~25
					#leave out 明显看错的输入
					# if abs(input-pressure)>6:
						# continue
					# print(word[word_index])
					word_index=min(word_index+1,word_length-1)
					if correct=="true":
						if word_index==(word_length-1):
							choose_start=end
				except IndexError:
					print(word_index)
			goal=input*4+group*2
			#写用户表
			ws.write(int(current_user_index[goal]),goal,end-begin)
			ws.write(int(current_user_index[goal+1]),goal+1,pressure-input+0.5)
			current_user_index[goal]+=1
			current_user_index[goal+1]+=1
			#写总表
			user_ws.write(int(user_index[goal]),goal,end-begin)
			user_ws.write(int(user_index[goal]),goal+1,pressure-input+0.5)
			user_index[goal]+=1
			user_index[goal+1]+=1			
		#写choose表
		if correct=="true":
			choose_end=end
			choose_ws.write(choose_index[group],user_id*2+group,choose_end-choose_start)
			choose_index[group]+=1
	#写user表
	for i in range(26*4):
		log_ws.write(0,i,user_index[i])
	#save all
	wb.save(chr(user_id+48)+'.xls')
	user_wb.save("user.xls")
	log_wb.save("log.xls")
	choose_wb.save("choose.xls")
	delete_wb.save("delete.xls")
	correct_wb.save("correct.xls")

if __name__=="__main__":
	# ini_files()
	# modify()
	# read_data()
	# write_data()
	modify1()
	read_data1()
	write_data1()

