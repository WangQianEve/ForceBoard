#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp2/"
modpath="./modify/exp2/"

fout=open("exp2-selection.csv","w")
fout.write("word,time,elapse,selection,user,id,in_sentence,mode,sentence_first,reset\n")
lines=[]

def modify1(file):
	fint=open(path+file,'r')
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		lines[i]=lines[i].replace(', ','\n')
	fout=open(modpath+file,'w')
	fout.writelines(lines)
	fout.close()

def read_data1( file):
	global lines
	fint=open(modpath+file,'r')
	lines=fint.readlines()
	fint.close()
	
def write_data1( file):
	print(file)
	global lines
	user=file[:-10]
	#each sentence
	i=0
	i_t=len(lines)
	sentence=""
	input=""
	flag=False
	reset=False
	delete=False
	t_time=0
	miss=0
	while i<i_t:
		reset=False
		sentence=lines[i].strip()
		i+=1
		length=int(lines[i].strip())
		i+=1
		mode=lines[i].strip()
		i+=1
		number=lines[i].strip()
		i+=1
		if length==0:
			continue
		if (i+length*5)<i_t and sentence==lines[i+length*5].strip():
			reset=True
			i+=length*5
			continue
		#each character
		if mode=="char":
			i+=length*5
			continue
		word_begin=float(lines[i].strip())
		word_end=0
		prev_begin=0
		prev_end=0
		prev_list=0
		input_list=[]
		input_prev=0
		prev_in=0
		for k in range(length):
			k+=1
			begin=float(lines[i].strip())
			i+=1
			end=float(lines[i].strip())
			i+=1
			pressure=float(lines[i].strip())
			i+=1
			group=lines[i].strip()
			i+=1
			prev_in=len(input)
			input=lines[i].strip()
			i+=1
			prev_list=len(input_list)
			if prev_list>0:
				cur_word=input_list[-1]
			input_list=input.split()
			if begin==prev_begin and pressure!=100:
				continue
			# if (len(input_list)>1 and input[-2]==" " and prev_list<len(input_list)) or pressure==100:
			if prev_list>0 and ((prev_list!=len(input_list) and delete==False) or ((len(input_list)>0 and len(input_list[-1])==1) and pressure!=100)):
				if prev_list==1:
					sentence_first=True
				else:
					sentence_first=False
# fout.write("word,time,elapse,selection,user,id,in_sentence,mode,sentence_first\n")
				# fout.write(str(word_begin)+","+str(word_end)+"\n")
				fout.write(cur_word+","+str(word_end-word_begin)+","+str(begin-prev_end)+","+str(prev_end-word_end)+","+user+","+number+","+str(prev_list-1)+","+mode+","+str(sentence_first)+","+str(reset)+"\n")
			if pressure==100:
				delete=True
			else:
				delete=False

			if len(input_list)>0 and len(input_list[-1])==1 and pressure!=100:
				word_begin=begin
			prev_begin=begin
			prev_end=end
			if float(end-begin)<0.25 and pressure<-2:
				pass
			elif pressure<-4:
				pass
			elif float(end-begin)<0.17:
				pass
			else:
				word_end=end
			
raw=[]
if __name__=="__main__":
	for i in os.walk(modpath):
		raw=i[2]
	for i in raw:
		if i.endswith("_tasks.txt"):
			# modify1(i)
			read_data1(i)
			write_data1(i)
