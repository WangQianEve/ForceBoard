#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp0-0/"
modpath="./modify/exp0-0/"
TAP=-4
DEL=34

char_fout=open("character1.csv","a")
delete_fout=open("delete.csv","a")
word_fout=open("word.csv","a")
choose_fout=open("choose.csv","a")
correct_fout=open("correct.csv","a")

lines=[]

def modify1( file):
	fint=open(path+file,'r')
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		if ',' in lines[i]:
			lines[i]=lines[i].replace(',','\n')
		if ' ' in lines[i]:
			lines[i]=lines[i].replace(' ','')
	fout=open(modpath+file,'w')
	fout.writelines(lines)
	fout.close()

def read_data1( file):
	global lines
	fint=open(modpath+file,'r')
	lines=fint.readlines()
	fint.close()
	
def write_data1( file):
	global lines
	user=file[:-6]
	correct_fout.write(user)
	prev_input=TAP
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
		if length==0:
			continue
		#计算正确率 以及分组
		total_input+=1
		if correct=="true":
			count+=1
			if count==32:
				count=0
				correct_fout.write(str(32/total_input)+",\n")
				total_input=0
				group+=1
				if group==2:
					break
		#each character
		if length>1:
			word_time=float(lines[i].strip())
		for k in range(length):#输入次数
			begin=float(lines[i].strip())
			i+=1
			end=float(lines[i].strip())
			i+=1
			pressure=float(lines[i].strip())
			i+=1
			if pressure==TAP:
				prev_input=TAP
			elif pressure>=(DEL*0.99):#写delete表
				prev_input=DEL
				delete_fout.write(user+", "+str(group+3)+", "+str(end-begin)+",\n")
				word_index=max(word_index-1,0)
			else:
				try:
					input=ord(word[min(word_index,word_length-1)])-ord('a')#0~25
					char_fout.write(word[min(word_index,word_length-1)]+", "+str(end-begin)+", "+str(pressure)+", "+str(pressure-input+0.5)+", "+str(prev_input)+", "+str(input-prev_input)+", "+user+", "+str(group+3)+",\n")
					prev_input=input
					word_index+=1
					if correct=="true":
						if word_index==(word_length-1):
							choose_start=end
				except IndexError:
					print(str(word_index)+" "+word)
		if length>1:
			word_time=end-word_time
			word_fout.write(word+", "+str(word_time)+", "+correct+", "+user+", "+str(group+3)+",\n")
		# #写choose表
		if correct=="true":
			choose_end=end
			choose_fout.write(str(choose_end-choose_start)+", "+user+", "+str(group+3)+",\n")

raw=[]
if __name__=="__main__":
	for i in os.walk(path):
		raw=i[2]
	for i in raw:
		if i.endswith("_c.txt"):
			modify1(i)
			read_data1(i)
			write_data1(i)
	char_fout.close()
	word_fout.close()
	delete_fout.close()
	choose_fout.close()
	correct_fout.close()
