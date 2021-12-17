
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    no_msg = df.shape[0]

    words=[]
    for msg in df['message']:
        words.extend(msg.split())
    
    no_media_msg = df[ df['message'] =='<Media omitted>\n'].shape[0]

    links=[]

    for msg in df['message']:
        links.extend(extract.find_urls(msg))
    
    return words, no_msg, no_media_msg, len(links)


    # def most_busy_user(df):
    #     x = df['user'].values.tolist()[1:3]
    #     return x
    
def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user']!='group notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    
    wc = WordCloud(width=500, height=500, min_font_size = 10,max_font_size =80, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_comman_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user']!='group notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    words=[]

    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    most_comman_df = pd.DataFrame(Counter(words).most_common(20))
    
    return most_comman_df

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    emojis=[]

    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time']=time

    return timeline

def daily_timeline(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()



def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

    return user_heatmap

    

    
