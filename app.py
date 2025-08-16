import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title='StartUp-Analysis',page_icon="🧊",layout='wide')

df = pd.read_csv('archive/startup_cleaned.csv')

df['date'] = pd.to_datetime(df['date'],errors='coerce') 

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_investor(investor):
    st.title(investor)

    # load the recent 5 investment of the investors
    last5_df = df[df['investors'].str.contains(investor)].head(5)[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)

    with col1:
        # biggest investments
        big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        st.dataframe(big_df)
    
    
    with col2:  
        # Sector Investing
        sector_df = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().reset_index()

        # st.subheader("Investment Distribution by Sector")
        fig1 = px.pie(sector_df, values="amount", names="vertical",
                    title="Sector-wise Investment Share",
                    hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig1, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Round Investing
        round_df = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().reset_index()
        # st.subheader("Investment by Funding Round")
        fig2 = px.pie(round_df, values="amount", names="round",
                    title="Investment by Funding Round",
                    hole=0.3, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig2, use_container_width=True)

    with col4:
        # City Investing
        city_df = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().reset_index()
        # st.subheader("City-wise Investment")
        fig3 = px.pie(city_df, values="amount", names="city",
                    title="Investment Across Cities",
                    hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig3, use_container_width=True)

    # Year on Year Investment
    df['year'] = df['date'].dt.year
    yoy_df = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().reset_index()

    # st.subheader("Year-on-Year Investment Trend")
    fig4 = px.line(yoy_df, x="year", y="amount", markers=True,
                title="YOY Investment Growth",
                labels={"year": "Year", "amount": "Total Investment Amount"})
    st.plotly_chart(fig4, use_container_width=True)


def General_Analysis():
    
    # Total money Invested in Indian StartUp Ecosystem
    total = round(df['amount'].sum())

    # max amount infused in as startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # avg amount invested in each startup
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    # Total funded startups
    funded_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total Amount Invested',str(total)+'CR')
    with col2:
        st.metric('Max.',str(max_funding)+'CR')
    with col3:
        st.metric('Avg.',str(avg_funding)+'CR')
    with col4:
        st.metric('funded startups',str(funded_startup))

    # MOM 

    col1,col2 = st.columns(2)


    with col1:
        # st.subheader("MOM Amount Invested")
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

        # Plotly Line Chart
        fig1 = px.line(temp_df, x='x_axis', y='amount', markers=True,
                    title="Month on Month Amount Invested")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # st.subheader("MOM Count")
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

        # Plotly Line Chart
        fig2 = px.line(temp_df, x='x_axis', y='amount', markers=True,
                    title="Month on Month Count")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Sector Analysis
    col1,col2 = st.columns(2)

    with col1:
        sector_invested = df.groupby('vertical')['amount'].sum().sort_values(ascending=False)

        top_n = 5
        sector_top = sector_invested.head(top_n)
        sector_other = pd.Series({"Others": sector_invested[top_n:].sum()})
        sector_final = pd.concat([sector_top, sector_other])

        sector_df = sector_final.reset_index()
        sector_df.columns = ["Sector", "Count"]

        fig = px.pie(sector_df, values="Count", names="Sector",
                    title=f"Top {top_n} Sectors (Others grouped)",
                    hole=0.3,  # donut style for clarity
                    color_discrete_sequence=px.colors.qualitative.Set3)

        st.plotly_chart(fig)

    with col2:
        sector_count = df.groupby('vertical')['amount'].count().sort_values(ascending=False)

        top_n = 5
        sector_top = sector_count.head(top_n)
        sector_other = pd.Series({"Others": sector_count[top_n:].sum()})
        sector_final = pd.concat([sector_top, sector_other])

        sector_df = sector_final.reset_index()
        sector_df.columns = ["Sector", "Count"]

        fig3 = px.pie(sector_df, values="Count", names="Sector",
                    title=f"Top {top_n} Sectors (Others grouped) in Max. Investors Invested",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3)

        st.plotly_chart(fig3)

    # Type of Funding

    max_funded_round = df.groupby('round')['amount'].sum().sort_values(ascending=False)

    top_n = 5
    round_top = max_funded_round.head(top_n)
    round_other = pd.Series({"Others": max_funded_round[top_n:].sum()})
    round_final = pd.concat([round_top, round_other])

    round_df = round_final.reset_index()
    round_df.columns = ["Funding", "Amount"]

    fig4 = px.pie(round_df, values="Amount", names="Funding",
        title=f"Top {top_n} Funded Rounds (Others grouped)",
        hole=0.3,  # donut style for clarity
        color_discrete_sequence=px.colors.qualitative.Set3)

    st.plotly_chart(fig4)

    # City wise Funding

    max_funded_city = df.groupby('city')['amount'].sum().sort_values(ascending=False)

    top_n = 5
    city_top = max_funded_city.head(top_n)
    city_other = pd.Series({"Others": max_funded_city[top_n:].sum()})
    city_final = pd.concat([city_top, city_other])

    city_df = city_final.reset_index()
    city_df.columns = ["City", "Amount"]

    fig5 = px.pie(city_df, values="Amount", names="City",
        title=f"Top {top_n} Funded City (Others grouped)",
        hole=0.3,  # donut style for clarity
        color_discrete_sequence=px.colors.qualitative.Set3)

    st.plotly_chart(fig5)

    # Top StartUps Year Wise and Overall

    col1,col2 = st.columns(2)

    with col1:
        startup_yearly = df.groupby(['year', 'startup'])['amount'].sum().reset_index()
        top_startups_yearwise = startup_yearly.sort_values(['year','amount'], ascending=[True, False]).groupby('year').first().reset_index()

        fig6 = px.bar(top_startups_yearwise, x="year", y="amount", color="startup",
            text="startup", title="Top Funded Startup Each Year")
        st.plotly_chart(fig6)

    with col2:
        top_startups_overall = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)

        fig7 = px.bar(top_startups_overall.reset_index(), x="startup", y="amount",
            title="Top Funded Startups Overall")
        st.plotly_chart(fig7)

    st.subheader("Funding Heatmap Dashboard")

    # User selects dimensions
    row_dim = st.selectbox("Select Row Dimension", ["vertical", "city", "investors"])
    col_dim = st.selectbox("Select Column Dimension", ["year", "vertical", "city"])


    # Prevent invalid case where row == col
    if row_dim == col_dim:
        st.warning("⚠️ Row and Column dimensions must be different.")
    else:
        # Create pivot safely
        try:
            pivot_df = df.pivot_table(
                index=row_dim,
                columns=col_dim,
                values="amount",
                aggfunc="sum"
            ).fillna(0)

            if pivot_df.empty:
                st.info("ℹ️ No data available for the selected combination.")
            else:
                # Plot heatmap
                fig = px.imshow(
                    pivot_df,
                    text_auto=True,
                    color_continuous_scale="YlGnBu",
                    title=f"Funding Heatmap ({row_dim.capitalize()} vs {col_dim.capitalize()})"
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error while creating heatmap: {e}")



# Data Cleaning

df['investors'] = df['investors'].fillna('undisclosed').str.strip()  # assign missing value as undisclosed


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    btn = st.sidebar.button('Show Overall Analysis')
    if btn:
        General_Analysis()
elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Detail')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Detail')
    if btn2:
        load_investor(selected_investor)
