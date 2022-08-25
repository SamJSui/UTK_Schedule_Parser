import os
import camelot.io as camelot
import ghostscript
import pandas as pd
from datetime import datetime

column_names = 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri'
dict_of_schedules = {}

schedules_path = '../Schedules' # PATH

for file in os.listdir(schedules_path): # ITERATES THROUGH EACH PDF IN SCHEDULES DIR
    schedule_path = os.path.join(schedules_path, file)
    table = camelot.read_pdf(schedule_path) # TABULATE
    df = table[0].df
    schedule = pd.DataFrame(columns=column_names) # DECLARE INITIAL DATAFRAME
    name = str(file).split(sep='.')[0].replace('-', ' ').title() # NAME
    for idx in range(1, len(df)):
        schedule_data = [df[1][idx], df[2][idx], df[3][idx], df[4][idx], df[5][idx]] # APPENDING SCHEDULE DATA TO DATAFRAME
        schedule.loc[len(schedule)] = schedule_data
    schedule = schedule.replace({'\n' : ''}, regex=True) # CLEANING
    schedule = schedule.replace({'ONLINE-AS', ''}, regex=True)
    schedule = schedule.replace({'SHOWN', ''}, regex=True)
    dict_of_schedules[name] = schedule # APPENDING DATAFRAME VALUE TO NAME KEY

def time_parse(data):
    data[0] = data[0].replace('-', '') # FORMATTING
    data[0] = data[0]+'M'
    data[1] = data[1]+'M'
    if len(data[0]) == 5:
        data[0] = '0'+data[0]
    if len(data[1]) == 5:
        data[1] = '0'+data[1]
    start_time = datetime.strptime(data[0], "%I:%M%p") # PARSING TIME
    end_time = datetime.strptime(data[1], "%I:%M%p")
    midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = start_time.time()
    end_time = end_time.time()
    return [start_time, end_time]

times_df = pd.DataFrame(columns=['Day of Week', 'Name', 'Location', 'Class', 'Start Time', 'End Time'])

for key in dict_of_schedules: # Dict of Schedules (DataFrames)
    for col, cell in dict_of_schedules[key].items(): # Cells in Schedules (Frame)
        for row in cell: # Rows within Series
            data = row.split()
            if len(data): # IGNORES BLANK BOXES
                if 'SHOWN' in data:
                    data.remove('SHOWN')
                times = time_parse(data)
                schedule_class = ""
                for i in range(3, len(data)):
                    schedule_class += data[i] + ' '
                times_df.loc[len(times_df)] = [col, key, data[2], schedule_class.rstrip(), times[0], times[1]]
times_df.to_csv('times.csv', index=False)
print(times_df.head())
