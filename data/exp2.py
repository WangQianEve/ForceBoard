#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
path="./data/exp2/"
modpath="./modify/exp2/"
TAP=-5
DEL=100

fout=open("exp2-2.csv","w")
fout.write("sentence,time,uncorrected,corrected,user,id,mode,reset,cut\n")
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
	input=" "
	flag=False
	reset=False
	cut=False
	t_time=0
	miss=0
	while i<i_t:
		if flag:
			c_miss=levenshtein_distance(sentence,lines[i-1].strip())
			fout.write(sentence+","+str(t_time)+","+str(c_miss)+","+str(c_miss+miss)+","+user+","+str(number)+","+mode+","+str(reset)+","+str(cut)+"\n")
			if reset==True:
				reset=False
		flag=True
		cut=False
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
			flag=False
			reset=True
			i+=length*5
			continue
		#each character
		sen_list=sentence.split()
		miss=0
		input_len=1
		prev_begin=0
		t_begin=float(lines[i].strip())
		t_time=0
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
			if float(end-begin)<0.17 and pressure<-2:
				i+=2
				# print("tap "+str(begin))
				continue
			elif float(end-begin)<0.25:
				i+=2
				continue
			group=lines[i].strip()
			i+=1
			if input=="":
				cut=True
				t_begin=begin
				miss=0
			input=lines[i].strip()
			i+=1
			if pressure==100:
				if input_len==len(input.split()):
					miss+=1
				else:
					cmp=" "
					if input_len<=len(sen_list):
						cmp=sen_list[input_len-1]
					# print(input)
					# print(begin)
					# miss+=levenshtein(input_list[input_len-1],cmp)
					miss+=len(input_list[input_len-1])
			input_list=input.split()
			input_len=len(input_list)
		t_time=end-t_begin
	c_miss=levenshtein_distance(sentence,lines[i-1].strip())
	fout.write(sentence+","+str(t_time)+","+str(c_miss)+","+str(c_miss+miss)+","+user+","+str(number)+","+mode+","+str(reset)+","+str(cut)+"\n")
			
def levenshtein(a,b):  
    n, m = len(a), len(b)  
    if n > m:  
        a,b = b,a  
        n,m = m,n  
    current = range(n+1)  
    for i in range(1,m+1):  
        previous, current = current, [i]+[0]*n  
        for j in range(1,n+1):  
            add, delete = previous[j]+1, current[j-1]+1  
            change = previous[j-1]  
            if a[j-1] != b[i-1]:  
                change = change + 1  
            current[j] = min(add, delete, change)  
    return current[n]  
  
def levenshtein_distance(first, second):  
    if len(first) > len(second):  
        first, second = second, first  
    if len(second) == 0:  
        return len(first)  
    first_length = len(first) + 1  
    second_length = len(second) + 1  
    distance_matrix = [list(range(second_length)) for x in range(first_length)]  
    for i in range(1, first_length):  
        for j in range(1, second_length):  
            deletion = distance_matrix[i-1][j] + 1  
            insertion = distance_matrix[i][j-1] + 1  
            substitution = distance_matrix[i-1][j-1]  
            if first[i-1] != second[j-1]:  
                substitution += 1  
            distance_matrix[i][j] = min(insertion, deletion, substitution)  
    return distance_matrix[first_length-1][second_length-1] 

raw=[]
if __name__=="__main__":
	for i in os.walk(modpath):
		raw=i[2]
	for i in raw:
		if i.endswith("_tasks.txt"):
			# modify1(i)
			read_data1(i)
			write_data1(i)
