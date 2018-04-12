import pandas as pd
import numpy as np
import time as tm
import argparse

def edgar_analytics(args):

	#Start_time is for simple program profiling 
	start_time = tm.time()


	#Reading input data:
	print('Reading input data ...')


	#Initialize dict for big data:
	big_data = []

	#Reading in csv data:
	for chunk in  pd.read_csv(args.data, sep=',', header=0
                          , chunksize=20000):
    		big_data.append(chunk)
	#write data into pandas DataFrame
	data = pd.concat(big_data, axis= 0)
	#discard unneeded data dict
	del big_data

	#Read inactivity time:
	delta_time = open(args.inactivity_period, "r").readlines()
	delta_time = int(delta_time[0])
	print('Reading Complete')



	#Formatting data:
	print('Formatting data ...')

	#Keep only needed fields

	data = pd.concat([data['ip'], data['date'], data['time'],
                  	data['cik'], data['accession'], data['extention']],axis=1);

	# initialize column to track time in seconds
	data['time_in_seconds'] = int(0)
	data['date_plus_time'] = data['date'] + ' ' + data['time']
	data['num_requests'] = int(1)

	print('Data formatting complete')


	#Process data line by line and write to csv file:
	print('writing to sessionization.txt ...')


	#initialize time window to check for inactivity:
	time = 0

	#initialize data frame for active ip's only,
	#inactive ip's will be removed post data writing:
	data_active = pd.DataFrame(columns=data.columns)

	for i in range(0,len(data)):
    		#find and store request time in sec:
    		t0 = int(data['time'][i][-2:])
    		t1 = 60*int(data['time'][i][3:5])
    		t2 = 3600*int(data['time'][i][:2])
    		t = t0 + t1 + t2
    		data.iloc[i,6] = int(t)
    
    		#reset current time to find inactivities
    		if t > time:
        		time = t
   
    		# dataFrame of active ip's
    		data_active = data_active.append(data[i:i+1])
    
    		#data entries from the current time:
    		active_now = data_active[(time - data_active['time_in_seconds'] == delta_time - 2 + 1)]
    		# data entries from 1 sec ago:
    		active_one_sec_ago = data_active[(time - data_active['time_in_seconds'] == delta_time - 1 + 1 )]
    		# data entries from 2 sec ago:
    		active_two_sec_ago = data_active[(time - data_active['time_in_seconds'] == delta_time - 0 + 1 )]
    
    		# Find inactive ip's
    		notNow = active_two_sec_ago['ip'] != active_now['ip'].any()
    		notOneSecAgo = active_two_sec_ago['ip'] != active_one_sec_ago['ip'].any()

    		inactive_now = active_two_sec_ago[notNow & notOneSecAgo]
    
    		#If end of file, then close all sessions:
    		if i == len(data)-1:
        		inactive_now = data_active
    
    
    		# If inactive ip's exist, gather and write data for all inactive ip's
    		if inactive_now.empty == False:
        
        		#Inactive ip names:
        		inactive_ips = pd.Series.unique(inactive_now['ip'])
        		#number of inactive ip's:
        		inactive_ips_num = pd.Series.nunique(inactive_now['ip'])
        
        		#write data for each inactive ip:
        		for j in range(0,inactive_ips_num):
            			data_write = inactive_now[inactive_now['ip']==inactive_ips[j]]
            			data_write = data_write.reset_index(drop=True)

            			data_write = [data_write.iloc[0,0], data_write.iloc[0,7],
                          		data_write.iloc[-1,7],
                          		int(data_write.iloc[-1,6] - data_write.iloc[0,6] + 1),
                          		int(data_write.iloc[:,8].sum())]
            			data_write = pd.DataFrame(data=data_write).transpose()
            
            			with open(args.output, 'a') as f:
                			data_write.to_csv(f,sep=',', header=False, index=False)
            
        		# Drop inactive ip's from active ip dataFrame:
        		if i != len(data) -1:
            			data_active = data_active.drop(inactive_now.index.values)
    
	print('program complete. Data written in sessionization.txt')
	print('total program time = ',tm.time()-start_time,' seconds')
    
    
    
def main():
	"""
	Tally the number of campaign contributions from repeat donors of specific zip codes.
	
	Parameters
	==========
	data       : path to EDGAR weblog input data (log.csv or similar file)
	
	inactivity_period : path to file containing inactivity time value (inactivity_period.txt).
	
	output     : path to output file for data writing (sessionization.txt)
	"""
	descr = 'Identify number and duration of EDGAR document requests from IPs.'
	parser = argparse.ArgumentParser(description=descr)
	descr = 'path to EDGAR weblog input data file (log.csv). Default: %(default)s'
	parser.add_argument('--data', default='./input/log.csv',help=descr)
	descr = 'path to inactivity period input data file (inactivity_period.txt). Default: %(default)s'
	parser.add_argument('--inactivity_period', default='./input/inactivity_period.txt', help=descr)
	descr = 'path to output file'
	parser.add_argument('--output', default='./output/sessionization.txt', help=descr)
	args = parser.parse_args()

	edgar_analytics(args)


if __name__ == "__main__":
    main()   

