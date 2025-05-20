import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(
    page_title="Ecommerce Dataset Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

print("test debug print")
st.title("Ecommerce Dataset Dashboard")
st.markdown("Alethea Agung Yodha Pratama - 24072262")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/yodhasu/Data-Analytics/refs/heads/main/Assignment%201/data-2.csv")
    print("Data loaded successfully")
    df.drop(df[df['CustomerID'].isna() | df['Description'].isna()].index, inplace=True)
    df.drop(df.query('Country == "Unspecified"').index, inplace=True)
    print("Data dropped successfully")
    df = df.astype({'InvoiceDate':'datetime64[ns]','CustomerID':'int'})
    df['Revenue'] = abs(df['UnitPrice'] * df['Quantity'])
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month_name()
    df['Date'] = df[['Month','Year']].astype(str).apply('-'.join, axis=1)
    df['Day'] = df['InvoiceDate'].dt.day_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    print("Data transformed successfully")
    
    return df

def total_revenue_plot():
    total_revenue = Sales.groupby('Date', as_index=False)['Revenue'].sum().round(2)

    # Ensure your dates are ordered correctly (optional manual ordering)
    order_list = ["05","09","01","13","03","02","08","07","04","06","12","11","10"]
    total_revenue['Order'] = order_list
    total_revenue.sort_values(by='Order', inplace=True)
    total_revenue.drop('Order', axis=1, inplace=True)

    fig = px.line(
        total_revenue,
        x='Date',
        y='Revenue',
        title='',
        markers=True,
        labels={'Revenue': 'Revenue ($)'}
    )

    fig.update_traces(line=dict(color='crimson'), name='Revenue')
    fig.update_layout(
        title_x=0.5,
        xaxis_title='Date',
        yaxis_title='Revenue',
        yaxis_tickprefix='$',
        xaxis_tickangle=30
    )
    fig.update_layout(title_text='', title_x=0.5)
    return fig

def total_revenue_product():
    product_revenue = Sales.groupby(['StockCode','Description'], as_index=False)['Revenue'].sum().round(2)
    product_revenue.sort_values(by='Revenue', ascending=False, inplace=True)

    plt.figure(figsize=(10, 6))
    plt.xticks(rotation=45)

    top_10_products = product_revenue.head(10)
    
    fig = px.pie(top_10_products, values='Revenue', names='StockCode', title='', hover_data=['Description'])
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    fig.update_layout(title_text='', title_x=0.5)
    
    return fig

def sales_quantity_product():
    quantity_revenue = Sales.groupby(['StockCode','Description'], as_index=False)['Quantity'].sum().round(2)
    quantity_revenue.sort_values(by='Quantity', ascending=False, inplace=True)

    plt.figure(figsize=(10, 6))
    plt.xticks(rotation=45)

    top_10_quantity = quantity_revenue.head(10)
    
    fig = px.pie(top_10_quantity, values='Quantity', names='StockCode', title='', hover_data=['Description'])
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    fig.update_layout(title_text='', title_x=0.5)
    
    return fig

def total_revenue_by_day_plot():
    day_revenue = Sales.groupby('Day', as_index=False)['Revenue'].sum()
    day_revenue['Day'] = pd.Categorical(
        day_revenue['Day'],
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ordered=True
    )
    day_revenue.sort_values(by='Day', inplace=True)

    fig = px.bar(
        day_revenue,
        x='Revenue',
        y='Day',
        orientation='h',
        title='',
        text='Revenue',
        color='Day',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig.update_traces(
        texttemplate='$%{x:,.0f}',
        textposition='outside'
    )

    fig.update_layout(
        xaxis_title='Revenue',
        yaxis_title='Day',
        xaxis_tickprefix='$',
        xaxis_tickformat=',.1s',  # Format to show e.g. 2.5M
        title_x=0.5,
        showlegend=False
    )

    fig.update_layout(title_text='', title_x=0.5)
    return fig

def top_10_country_revenue_plot():
    country_revenue = Sales.groupby('Country', as_index=False)['Revenue'].sum().round(2)
    country_revenue.sort_values(by='Revenue', ascending=False, inplace=True)
    top_10 = country_revenue.head(10)

    fig = px.bar(
        top_10,
        x='Country',
        y='Revenue',
        title='',
        text='Revenue',
        color='Country',
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_traces(
        texttemplate='$%{y:,.0f}',
        textposition='outside'
    )

    fig.update_layout(
        xaxis_tickangle=45,
        yaxis_tickprefix='$',
        yaxis_title='Revenue',
        title_x=0.5,
        showlegend=False
    )
    fig.update_layout(title_text='', title_x=0.5)
    return fig

df = load_data()
Sales = df[~df['InvoiceNo'].str.contains('C')]
with st.expander("View Cleaned Data", expanded=False):
    st.dataframe(df)
    st.markdown("""
    This is a cleaned version of the dataset. The original dataset was obtained from [Kaggle](https://www.kaggle.com/datasets/lissetteg/ecommerce-dataset).
    My anaylysis processed can be found in the [Github repository](https://github.com/yodhasu/Data-Analytics.git).
    """)
    
left, right = st.columns([1, 1])

with left:
    st.markdown("### Total Revenue Over Time")
    fig = total_revenue_plot()
    st.plotly_chart(fig, use_container_width=True)

with left:
    div1, div2 = st.columns([1, 1])
    with div1:
        st.markdown("#### Top 10 Products by Revenue")
        fig = total_revenue_product()
        st.plotly_chart(fig, use_container_width=True)
    
    with div2:
        st.markdown("#### Top 10 Sales by Product")
        fig = sales_quantity_product()
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Total Revenue by Day of the Week")
    fig = total_revenue_by_day_plot()
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Top 10 Total Revenue by Country")
    fig = top_10_country_revenue_plot()
    st.plotly_chart(fig, use_container_width=True)