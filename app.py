import streamlit as st
from matplotlib.figure import Figure
from streamlit import pyplot
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title='StartUp Funding Analyze')
df = pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year



def load_overall_analysis():
    st.title('Overall Analysis')

    ##total invested amount
    total = round(df['amount'].sum())


    ##max funding in startup
    max_funding=df.groupby('startup')['amount'].max(
    ).sort_values(ascending=False).head(1).values[0]

    #mean of fumnding
    mean=df.groupby('startup')['amount'].sum().mean()
    ##total funded startup
    funding=df['startup'].nunique()



    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total funding', str(total) + 'Cr')
    with col2:
        st.metric('Max Funding', str(round(max_funding))+'Cr')
    with col3:
        st.metric('Average Funding', str(round(mean))+'Cr')
    with col4:
        st.metric('Total Startup',funding)


    st.header('MOM')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    st.subheader('Month Of Month Chart')
    fig3, ax3= plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)

def load_investors(investor):
        st.title(investor)
        last5_df = df[df['investors'].str.contains(investor)].head(5)[
            ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
        st.subheader('Most Recent Investments')
        st.dataframe(last5_df)

        col1, col2 = st.columns(2)
        with col1:
            big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum(
            ).sort_values(ascending=False).head(5)
            st.subheader('Biggest Investments')
            fig, ax = plt.subplots()
            ax.bar(big_df.index, big_df.values)
            st.pyplot(fig)
        with col2:
            vert = df[df['investors'].str.contains(investor)].groupby(
                'vertical')['amount'].sum()
            st.subheader('Sector In Investments')
            fig1, ax1 = plt.subplots()
            ax1.pie(vert, labels=vert.index, autopct='%0.01f%%')
            st.pyplot(fig1)

st.sidebar.title('StartUp Funding Analyze')
option1 = st.sidebar.selectbox('Select One', ['Overall Analysis','Investor'])





if option1 == 'Overall Analysis':
    load_overall_analysis()

else:
    selected_investors = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    b2 = st.sidebar.button('Find Investor')
    if b2:
        load_investors(selected_investors)

