#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp1/"
modpath="./modify/exp1/"

HAND_UP=-5
char_fout=open("character1.csv","w")
char_fout.write("char, time, pressure, rel_pressure, prev, rel_prev, user, group, id, \n")
delete_fout=open("delete.csv","w")
delete_fout.write("user, group, time,\n")
lines=[]

def modify1(file,name):
	fint=open(file,'r')
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		if ',' in lines[i]:
			lines[i]=lines[i].replace(',','\n')
		if ' ' in lines[i]:
			lines[i]=lines[i].replace(' ','')
	fout=open(modpath+name,'w')
	fout.writelines(lines)
	fout.close()

def read_data1( file):
	global lines
	fint=open(modpath+file,'r')
	print(modpath+file)
	lines.clear()
	lines=fint.readlines()
	fint.close()
	
def write_data1( name):
	global lines
	user=name[:-6]
	#each word
	i=0
	i_t=len(lines)
	while i<i_t:
		word=lines[i].strip()
		word_length=len(word)
		i+=1
		length=int(lines[i].strip())
		i+=2
		number=int(lines[i].strip())
		i+=1
		if number==0:
			i+=4*length
			continue
		elif number>77:
			break
		#each character
		begin=[]
		end=[]
		pressure=[]
		group=[]
		for k in range(length):#输入次数
			begin.append(float(lines[i].strip()))
			i+=1
			end.append(float(lines[i].strip()))
			i+=1
			pressure.append(float(lines[i].strip()))
			i+=1
			group.append(float(lines[i].strip()))
			i+=1
		p=length-1
		index=2
		for k in range(length):
			if group[p]==1:#写delete表
				delete_fout.write(user+", "+str(group[p])+", "+str(end[p]-begin[p])+",\n")
				p-=1
				index+=1
			else:
				try:
					if index<3:
						char_fout.write(word[index]+", "+str(end[p]-begin[p])+", "+str(pressure[p])+", "+str(pressure[p]-ord(word[index])+ord('a')+0.5)+", "+str(pressure[p-1])+", "+str(pressure[p]-pressure[p-1])+", "+user+", "+str(group[p])+", "+str(number)+",\n")
					p-=1
					index-=1
					if index==-1:
						break
				except IndexError:
					print("error")

raw=[]
if __name__=="__main__":
	for dir in os.walk(path):
		raw=dir[2]
		p=dir[0]
		for i in raw:
			if i.endswith("_c.txt"):
				modify1(p+'/'+i,i)
				read_data1(i)
				write_data1(i)
				print(i)
	char_fout.close()
	delete_fout.close()
