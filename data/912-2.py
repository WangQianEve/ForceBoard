#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
fint=open("913_mod.csv","r")
fout=open("913_mod2.csv","w")

lines=[]

if __name__=="__main__":
	lines=fint.readlines()
	fint.close()
	for i in range(len(lines)):
		if ',' in lines[i]:
			lines[i]=lines[i].replace(',','\n')
	fout.writelines(lines)
	fout.close()
