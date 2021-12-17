import re
import pandas as pd
from datetime import *

def preprocess(data):

    #f = open('WhatsApp Chat with Akshay Shah.txt','r',encoding='utf-8')
    #data=f.read()

    pattern3 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-z]*\s-\s'
    messages = re.split(pattern3, data)[1:]

    pattern_date = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    dates = re.findall(pattern_date, data)

    df = pd.DataFrame({'user_message':messages, 'date':dates})
    df['date'] = pd.to_datetime(df['date'])

    users=[]
    msg=[]

    for message in df['user_message']:
        entry = re.split('([\w\W]+/?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            msg.append(entry[2])
        else: 
            users.append('group_notification')
            msg.append(entry[0])
     
        
    df['user'] = users
    df['message']=msg
    df.drop(columns = ['user_message'],inplace= True)

    df['month']= df['date'].dt.month_name()
    df['date'].dt.month_name()
    df['year']= df['date'].dt.year
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']= df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date']= df['date'].dt.date
    df['day_name']= df['date'].dt.day_name()
    df.drop(columns = ['date'],inplace= True)
    return df