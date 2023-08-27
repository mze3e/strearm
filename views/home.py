import time # for simulating a real-time data, time loop
import numpy as np # np mean, np random
import pandas as pd # read csv, df manipulation
import plotly.express as px # interactive charts
import streamlit as st # data web application development

from components.utils import show_md_content

def home(st):
    st.title('HOME')
    #st.write('This is a simple CRM built on Streamlit. It is a free and open source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks. All in pure Python. All for free. All open source!')
    # st.set_page_config(
    #     page_title = "Real-Time Data Dashboard",
    #     page_icon = "✅",
    #     layout = "wide",
    # )

    # read csv from a github repo
    df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

    # dashboard title

    st.title("Real-Time / Live Data Science Dashboard")

    # top-level filters 

    job_filter = st.selectbox("Select the Job", pd.unique(df['job']))


    # creating a single-element container.
    placeholder = st.empty()

    # dataframe filter 

    df = df[df['job']==job_filter]

    # near real-time / live feed simulation 

    for seconds in range(10):
    #while True: 
        
        df['age_new'] = df['age'] * np.random.choice(range(1,5))
        df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

        # creating KPIs 
        avg_age = np.mean(df['age_new']) 

        count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))
        
        balance = np.mean(df['balance_new'])

        with placeholder.container():
            # create three columns
            kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

            # fill in those three columns with respective metrics or KPIs 
            kpi1.metric(label="📺 Attention", value=round(avg_age), delta= round(avg_age) - 10)
            kpi2.metric(label="💙 Acquisition", value= int(count_married), delta= - 10 + count_married)
            kpi3.metric(label="＄ Revenue", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)
            kpi4.metric(label="♾️ Retention", value= int(count_married), delta= - 10 + count_married)
            kpi5.metric(label="😃 Referral", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

            # create two columns for charts 

            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                st.markdown("### First Chart")
                fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
                st.write(fig)
            with fig_col2:
                st.markdown("### Second Chart")
                fig2 = px.histogram(data_frame = df, x = 'age_new')
                st.write(fig2)
            st.markdown("### Detailed Data View")
            st.dataframe(df)
            time.sleep(1)
        #placeholder.empty()

    show_md_content('home')
    