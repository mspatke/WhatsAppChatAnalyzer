import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    user_list = df['user'].unique().tolist()[1:3]
    #user_list.remove('group notification')
    #user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show Analysis wrt",user_list)

    words, num_msg, no_media_msg, links = helper.fetch_stats(selected_user, df)
    
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total words")
            st.title(len(words))
        with col3:
            st.header("Total Media shared")
            st.title(no_media_msg)
        with col4:
            st.header("Total links shared")
            st.title(links)

        # if selected_user == "Overall":
        #     st.title("Most Busy User")
        #     x = helper.most_busy_user(df)
        #     fig, ax = plt.subplots()
        #     ax.bar()

        st.title("World Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc,interpolation='bilinear')
        st.pyplot(fig)
        
        #most comman words

        most_comman_df = helper.most_comman_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_comman_df[0],most_comman_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Comman words")
        st.pyplot(fig)

        #emoji analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        
        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax= plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax= plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='blue', linestyle='dashed', marker='o',markerfacecolor='red', markersize=6)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #Daily Timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax= plt.subplots()
        #plt.figure(figsize=(18,10))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black',linewidth=1)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map 
        st.title('Activity Map')
        col1 , col2 =st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values , color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values , color = 'black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax= plt.subplots()
        ax = sns.heatmap(user_heatmap)
        #plt.figure(figsize=(18,10))
        #plt.xticks(rotation='vertical')
        st.pyplot(fig)


        
