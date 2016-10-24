#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp1/"
modpath="./modify/exp1-t/"
modpath2="./modify/exp1-t2/"
dis=0.017
fout=open("exp1-t.csv","w")
fout.write("goal,max,time,elapse,fall,isFirst,id\n")
def modify(file):
	fint=open(path+file,'r')
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
	fout=open(modpath+file,'w')
	fout.writelines(lines)
	fout.close()

def modify2(file):
	print(file)
	global lines
	fin=open(modpath+file,"r")
	fout=open(modpath2+file,"w")
	lines=fin.readlines()
	fin.close()
	time=[]
	pressure=[]
	fileLength=len(lines)
	curLine=2
	while curLine<fileLength:
		while lines[curLine].strip()!="]":
			time.append(lines[curLine].strip())
			curLine+=1
		curLine+=2
		while lines[curLine].strip()!="]":
			pressure.append(lines[curLine].strip())
			curLine+=1
		curLine+=2
		temp=0
		while temp<len(time):
			fout.write(time[temp]+'\n'+pressure[temp]+'\n')
			temp+=1
		time.clear()
		pressure.clear()
		fout.write('*\n')
	fout.close()
	
if __name__=="__main__":
	# for i in os.walk(path):
		# raw=i[2]
		# for i in raw:
			# if i.endswith("_t.txt"):
				# modify(i)
				# modify2(i)
	fin=open("912_mod2.csv","r")
	lines=fin.readlines()
	fin.close
	cur_user=""
	#each word
	i=0
	i_t=len(lines)
	finc=0
	begin_t=0.0
	prev_end=0
	while i<i_t:
		goal=lines[i].strip()
		i+=1
		begin=float(lines[i].strip())
		i+=1
		end=float(lines[i].strip())
		i+=1
		pressure=float(lines[i].strip())
		i+=1
		user=lines[i].strip()
		i+=1
		group=lines[i].strip()
		i+=1
		number=int(lines[i].strip())
		i+=1
		is_first=lines[i].strip()
		i+=1
		if user=="panxingyu_1472550787":
			continue
		if user!=cur_user:
			if cur_user!="":
				finc.close()
			finc=open(modpath2+user+"_t.txt","r")
			cur_user=user
			lines_t=finc.readlines()
			lines_t_index=0	
			begin_t=0.0
			print(cur_user)
		# print(goal+" "+str(begin)+" ")
		# print(lines_t_index)
		while float(begin)-float(lines_t[lines_t_index].strip())>dis:
			while lines_t[lines_t_index].strip()!="*":
				lines_t_index+=1
			lines_t_index+=1
		if float(lines_t[lines_t_index].strip())-float(begin)>dis:
			continue
		if is_first=="TRUE":
			prev_end=begin
		max_pressure=0.0
		max_time=0.0
		while lines_t[lines_t_index].strip()!="*":
			p=float(lines_t[lines_t_index+1].strip())
			if p>=max_pressure:
				max_pressure=p
				max_time=float(lines_t[lines_t_index].strip())
			lines_t_index+=2
		lines_t_index+=1
		fout.write(goal+","+str(max_pressure)+","+str(end-prev_end)+","+str(begin-prev_end)+","+str(end-max_time)+","+str(is_first)+","+str(number)+","+user+","+group+"\n")
		prev_end=end