#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp2/"
modpath="./modify/exp2/"

lines=[]

fout=open("913_mod.csv","w")
# fout.write("begin,end,pressure,user,group,id,mode,sentence_first,word_first,isValid\n")
			
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
	isValid=False
	while i<i_t:
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
			isValid=True
			i+=length*5
			continue
		#each character
		prev_begin=0
		t_begin=float(lines[i].strip())
		t_time=0
		is_sentence_first=True
		is_word_first=True
		expected=' '
		for k in range(length):
			k+=1
			begin=float(lines[i].strip())
			if begin==prev_begin:
				i+=5
				continue
			prev_begin=begin
			i+=1
			end=float(lines[i].strip())
			i+=1
			pressure=float(lines[i].strip())
			i+=1
			if pressure==100:
				i+=2
				continue
			if float(end-begin)<0.17 and pressure<-2:
				i+=2
				continue
			elif float(end-begin)<0.25:
				i+=2
				continue
			group=lines[i].strip()
			i+=1
			input=lines[i].strip()
			i+=1
			if len(input)>1:
				if input[-2]==' ':
					is_word_first=True
				else:
					is_word_first=False
			if len(input)>len(sentence):
				expected='#'
			else:
				expected=sentence[len(input)-1]
			fout.write(expected+","+str(begin)+","+str(end)+","+str(pressure)+","+user+","+str(group)+","+str(number)+","+mode+","+str(is_sentence_first)+","+str(is_word_first)+","+str(isValid)+"\n")
			is_sentence_first=False
		if isValid==True:
			isValid=False

			
raw=[]
if __name__=="__main__":
	for i in os.walk(modpath):
		raw=i[2]
		for i in raw:
			read_data1(i)
			write_data1(i)				
				