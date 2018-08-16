import pandas as pd
import os
import time
from datetime import datetime

#use Path objects to adjust path format to match operating system format
from pathlib import Path


path = Path("C:/stockData/intraQuarter")


# @param gather = value to be collected from files
def Key_Stats(gather = "Total Debt/Equity (mrq)"):
	statspath = path / '_KeyStats'
	
	#for loop uses os.walk to list out all contents within a directory
	#stock_list is file names within specified path 'statspath'
	stock_list = [x[0] for x in os.walk(statspath)]
	
	#specify columns for data frame
	df = pd.DataFrame(columns = ['Date','Unix','Ticker','Debt/Equity Ratio'])

	#for every file in the directory
	for each_dir in stock_list[1:5]:
		
		#list files in each directory
		each_file = os.listdir(each_dir)
		
		#read stock ticker/file name
		ticker = each_dir.split('\\')[4]

		#for every file that has been listed that is not empty
		if len(each_file) > 0 :
			
			for file in each_file:
				
				#strip time from file names 
				date_stamp = datetime.strptime(file,"%Y%m%d%H%M%S.html")

				#produce in unix time
				unix_time = time.mktime(date_stamp.timetuple())				
				
				#file path
				full_file_path = each_dir + '/'+ file
				#print(full_file_path)
				
				#open file with intention to read 'r'
				source = open(full_file_path,'r').read()
				
				
				#Elemment on the right of first split is the target value hence we use first element 
				#then split again by table tag to collect element from beginning/left of the remaining paragraph. 
				#try-except is due to some files having an extra space or indent between table tags, 
				#leading to index out of range errors.
				try:
					
					value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
					
 
					df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'Debt/Equity Ratio':value},ignore_index = True)
				
				except Exception as e:
					#print(str(e))
					pass
				
				
	save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
	print(save)
	df.to_csv(save)				
				
				

Key_Stats()