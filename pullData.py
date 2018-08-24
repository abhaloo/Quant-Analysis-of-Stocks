import pandas as pd
import os
import time
from datetime import datetime

#use Path objects to adjust path format to match operating system format
from pathlib import Path

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('dark_background')

#regular expressions
import re


path = Path("C:/stockData/intraQuarter")


# @param gather = value to be collected from files
def Key_Stats(gather = ("Total Debt/Equity (mrq)","Trailing P/E")):
	statspath = path + '/_KeyStats'
	
	#for loop uses os.walk to list out all contents within a directory
	#stock_list is file names within specified path 'statspath'
	stock_list = [x[0] for x in os.walk(statspath)]
	
	#specify columns for data frame
	df = pd.DataFrame(columns = [
		'Date',
		'Unix',
		'Ticker',
		'Debt/Equity Ratio',
		'Stock Price',
		'Stock Percent Change',
		'SP500',
		'SP500 Percent Change',
		'Difference',
		'Status',
		'Trailing P/E'])

	#read S&P 500 index data into dataframe 
	sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")


	ticker_list = []


	#for every file in the directory
	for each_dir in stock_list[1:5]:
		
		#list files in each directory
		each_file = os.listdir(each_dir)
		
		#read stock ticker/file name
		ticker = each_dir.split('\\')[4]
		#add tickers to list
		ticker_list.append(ticker)

		#every time we read a new ticker we require a new starting point
		#to perform percentage change
		starting_stock_value = False
		starting_sp500_value = False



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
				
				try: 
					value_list = []

					for each_data in gather:
				
						#try-except is due to some files having an extra space or indent between table tags, 
						#leading to index out of range errors.
						#tried to use replace('\n','') to account for extra indents but it appears thats not 
						#the only reason the scrape is failing
						try:
							
							#build regular expression:
						  #\d{1,8} = looking for a number of length 1-8
						  #
							regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
							#search via regular expression
							value = re.search(regex,source)
							value = (value.group(1))

						#for values with a 'B' after them to represent billions
							if "B" in value:
								value = float(value.replace("B",''))*1000000000
						
						#for values with a 'M' after them to represent millions
							elif "M" in value:
								value = float(value.replace("M",''))*1000000

							value_list.append(value)

						except Exception as e:
							print(ticker,"     :::    ",str(e))
							value = "N/A"
							value_list.append(value)

				


					#Extacting stock price from S&P 500 Index as a benchmark to compare sample data against
					try:
						#Extract date 
						sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')	
						#print("date extracted")

						#Set date as index of sp500 Dataframe
						row = sp500_df[sp500_df["Date"] == sp500_date]
						#print("row extracted")												
							
						#some rows have an extra indent or space which causes an error, 
						#so this if-else just skips over them
						if len(row) != 0:

							#extract S&P 500 stock price from Adj Close row
							sp500_value = float(row["Adj Close"])
							#print("s&p value extracted")
								
						else:
							print("\nrow empty\n")
							pass

					
					except:
						sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row["Adj close"])

					try:
						#Extract stock price from sample data
						stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					except Exception as e:
						#span id="yfs_l10_afl">43.27</span>
						try:
							stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
							stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
							stock_price = float(stock_price.group(1))
							

						except Exception as e:
							
							try:
								stock_price = (source.split('<span class-"time_rtq_ticker">')[1].split('</span>')[0])
								stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
								stock_price = float(stock_price.group(1))
							
							except Exception as e:
								print(ticker,':::::',str(e),file)
								pass


											
						#time.sleep(15)
						
						

					if not starting_stock_value:
							starting_stock_value = stock_price
					if not starting_sp500_value:
							starting_sp500_value = sp500_value
						
	 					
	 				#calculate percent change of stock price from sample data
					stock_percent_change = ((stock_price - starting_stock_value)/starting_stock_value) * 100
						
					#calculate percent chnage of stock prices from sp500 index data
					sp500_percent_change = ((sp500_value - starting_sp500_value)/starting_sp500_value) * 100


					difference = stock_percent_change - sp500_percent_change

					#@var status labels tickers according to whether the difference in their stock prices
					# (between outdated sample data and the current S&P500 Index) is -ve or +ve
					if difference > 0:
						status = "outperform"
					else:
						status = "underperform"



					df = df.append({
						'Date':date_stamp,
						'Unix':unix_time,'Ticker':ticker,
						'Debt/Equity Ratio':value,
						'Stock Price':stock_price,
						'Stock Percent Change':stock_percent_change,
						'SP500 Percent Change':sp500_percent_change,
						'SP500':sp500_value,
						'Difference':difference,
						'Status':status,
						'Trailing P/E':value_list[1]},ignore_index = True)
				
				except Exception as e:
					print(ticker,"     :::    ",str(e))
					pass
				
				
	#plot difference on graph for each ticker
	#for each_ticker in ticker_list:
	#	try:
			#redefine data frame
	#		plot_df = df[(df['Ticker'] == each_ticker)]
			#set index as date
	#		plot_df = plot_df.set_index(['Date'])
			
			#color plots according to status
			#red = underpeform, green = outperfrom  
	#		if plot_df['Status'][-1] == 'underperform':
	#			color = 'r'
	#		else:
	#			color = 'g'

			#set value to plot with label
	#		plot_df['Difference'].plot(label = each_ticker, color = color)
			


			#show legend
	#		plt.legend()
	#	except:
	#		pass

	#print graph
	#plt.show()

	#reformat file name		
	#save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
	df.to_csv("keyStats.csv")				
	print("key stats has been saved")
				
				

Key_Stats()