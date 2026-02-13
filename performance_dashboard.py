import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import textwrap

st.set_page_config(layout="wide")
st.markdown("""
<style>
.block-container {
    max-width: 78%;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv('data.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df_orders = df[df['Action'] == 'purchase'].copy()
df_orders['Month'] = df_orders['DateTime'].dt.to_period('M')
orders_by_month = df_orders.groupby('Month')['Quantity'].sum().reset_index()

def dashboard():
    if 'config_set' not in st.session_state:
        st.set_page_config(layout="wide")
        st.session_state.config_set = True

    st.subheader("App Performance Dashboard")
    # Month slicer
    months = df['DateTime'].dt.to_period('M').unique().sort_values()
    default_month = pd.Period('2019-10', freq='M')
    selected_month = st.selectbox('Select Month', months, index=list(months).index(default_month), key='unique_month_selector')

    mask = df['DateTime'].dt.to_period('M') == selected_month
    mask_orders = df_orders['DateTime'].dt.to_period('M') == selected_month
    df_latest = df[mask]
    df_orders_latest = df_orders[mask_orders]

    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    # Calculate previous month metrics
    prev_month = (selected_month.to_timestamp() - pd.DateOffset(months=1)).to_period('M')
    df_prev_month = df_orders[df_orders['DateTime'].dt.to_period('M') == prev_month]
    prev_monthly_sessions = df[df['DateTime'].dt.to_period('M') == prev_month].shape[0]
    prev_monthly_users = df[df['DateTime'].dt.to_period('M') == prev_month]['User_id'].nunique()
    prev_monthly_buyers = df_prev_month['User_id'].nunique()
    prev_monthly_orders = len(df_prev_month)
    prev_monthly_revenue = df_prev_month['Total Price'].sum()

    # Calculate current month metrics
    monthly_sessions = df[mask].shape[0]
    monthly_users = df[mask]['User_id'].nunique()
    monthly_buyers = df_orders_latest['User_id'].nunique()
    monthly_orders = len(df_orders_latest)
    monthly_revenue = df_orders_latest['Total Price'].sum()

    # Calculate percentage change
    sessions_change = ((monthly_sessions - prev_monthly_sessions) / prev_monthly_sessions) * 100 if prev_monthly_sessions != 0 else 0
    users_change = ((monthly_users - prev_monthly_users) / prev_monthly_users) * 100 if prev_monthly_users != 0 else 0
    buyers_change = ((monthly_buyers - prev_monthly_buyers) / prev_monthly_buyers) * 100 if prev_monthly_buyers != 0 else 0
    orders_change = ((monthly_orders - prev_monthly_orders) / prev_monthly_orders) * 100 if prev_monthly_orders != 0 else 0
    revenue_change = ((monthly_revenue - prev_monthly_revenue) / prev_monthly_revenue) * 100 if prev_monthly_revenue != 0 else 0

    with col1:
        change_color = 'red' if sessions_change < 0 else 'cornflowerblue'
        st.markdown(f"""
        <div style='background-color:#E1E8F0; padding:10px; border-radius:10px;'>
        <h6 style='color:#6c757d;'>Sessions</h6>
        <h4>{monthly_sessions}</h4>
        <h6 style='color:{change_color};'>{"+" if sessions_change > 0 else ""}{sessions_change:.1f}%</h6>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        change_color = 'red' if users_change < 0 else 'cornflowerblue'
        st.markdown(f"""
        <div style='background-color:#E1E8F0; padding:10px; border-radius:10px;'>
        <h6 style='color:#6c757d;'>Users</h6>
        <h4>{monthly_users}</h4>
        <h6 style='color:{change_color};'>{"+" if users_change > 0 else ""}{users_change:.1f}%</h6>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        change_color = 'red' if buyers_change < 0 else 'cornflowerblue'
        st.markdown(f"""
        <div style='background-color:#E1E8F0; padding:10px; border-radius:10px;'>
        <h6 style='color:#6c757d;'>Buyers</h6>
        <h4>{monthly_buyers}</h4>
        <h6 style='color:{change_color};'>{"+" if buyers_change > 0 else ""}{buyers_change:.1f}%</h6>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        change_color = 'red' if orders_change < 0 else 'cornflowerblue'
        st.markdown(f"""
        <div style='background-color:#E1E8F0; padding:10px; border-radius:10px;'>
        <h6 style='color:#6c757d;'>Orders</h6>
        <h4>{monthly_orders}</h4>
        <h6 style='color:{change_color};'>{"+" if orders_change > 0 else ""}{orders_change:.1f}%</h6>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        change_color = 'red' if revenue_change < 0 else 'cornflowerblue'
        revenue_display = f"${monthly_revenue/1000:.0f}K"
        st.markdown(f"""
        <div style='background-color:#E1E8F0; padding:10px; border-radius:10px;'>
        <h6 style='color:#6c757d;'>Revenue</h6>
        <h4>{revenue_display}</h4>
        <h6 style='color:{change_color};'>{"+" if revenue_change > 0 else ""}{revenue_change:.1f}%</h6>
        </div>
        """, unsafe_allow_html=True)

    st.write(" ")

    # Line chart and Funnel chart
    col1, col2 = st.columns([3.25, 1.75])
    with col1:
        sessions_by_month = df.groupby('DateTime').apply(lambda x: x.shape[0]).resample('M').sum()
        users_by_month = df.groupby('DateTime').apply(lambda x: x['User_id'].nunique()).resample('M').sum()
        orders_by_month = df_orders.groupby('DateTime').apply(lambda x: len(x)).resample('M').sum()
        fig1 = px.line(x=sessions_by_month.index.strftime('%b %Y'), y=[sessions_by_month.values, users_by_month.values, orders_by_month.values], title='Sessions, Users and Orders Over Time', labels={'x': ' ', 'y': 'Total Count'}, height=400)
        fig1.update_layout(legend_title_text='Metric', legend=dict(x=0, y=1.1, orientation='h'))
        fig1.data[0].name = 'Sessions'
        fig1.data[1].name = 'Users'
        fig1.data[2].name = 'Orders'
        # Add a dot to the line chart for the selected month
        selected_month_str = selected_month.to_timestamp().strftime('%b %Y')
        x_index = list(sessions_by_month.index.strftime('%b %Y')).index(selected_month_str)
        fig1.add_trace(go.Scatter(
            x=[selected_month_str, selected_month_str, selected_month_str],
            y=[sessions_by_month.values[x_index], users_by_month.values[x_index], orders_by_month.values[x_index]],
            mode='markers',
            marker=dict(size=10),
            showlegend=False
        ))
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        funnel_actions = ['search', 'product_view', 'add_to_wishlist', 'add_to_cart', 'checkout', 'purchase']
        funnel_data = df_latest[df_latest['Action'].isin(funnel_actions)].groupby('Action')['User_id'].count().reset_index()
        funnel_data.columns = ['Action', 'Count']
        funnel_data['Action'] = funnel_data['Action'].replace({
            'search': 'Search',
            'product_view': 'View Product',
            'add_to_wishlist': 'Add to Wishlist',
            'add_to_cart': 'Add to Cart',
            'checkout': 'Checkout',
            'purchase': 'Purchase'
        })
        action_order = ['Purchase', 'Checkout', 'Add to Cart', 'Add to Wishlist', 'View Product', 'Search']
        fig_funnel = px.funnel(funnel_data, x='Count', y='Action', title='User Funnel', category_orders={'Action': action_order}, height=400)
        fig_funnel.update_yaxes(title_text="", title_standoff=0)
        fig_funnel.update_layout(margin=dict(l=0))
        st.plotly_chart(fig_funnel, use_container_width=True)

    # Bar charts
    col1, col2 = st.columns(2)
    with col1:
        top_categories_quantity = df_orders_latest.groupby('Category')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False).head(10)
        top_categories_quantity['Category'] = top_categories_quantity['Category'].apply(lambda x: x.replace(' ', '<br>'))
        fig2 = px.bar(top_categories_quantity, x='Category', y='Quantity', title='Top Categories by Units Sold', text='Quantity', height=450, color='Quantity', color_continuous_scale=px.colors.sequential.Blues[2:])
        fig2.update_traces(textposition='outside')
        fig2.update_layout(yaxis_range=[0, top_categories_quantity['Quantity'].max() * 1.1], coloraxis_showscale=False)
        fig2.update_xaxes(tickangle=0, tickfont=dict(size=8))
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        top_categories_revenue = df_orders_latest.groupby('Category')['Total Price'].sum().reset_index().sort_values('Total Price', ascending=False).head(10)
        top_categories_revenue['Category'] = top_categories_revenue['Category'].apply(lambda x: x.replace(' ', '<br>'))
        fig3 = px.bar(top_categories_revenue, x='Category', y='Total Price', title='Top Categories by Revenue', text='Total Price', height=450, color='Total Price', color_continuous_scale=px.colors.sequential.Blues[2:])
        fig3.update_traces(textposition='outside')
        fig3.update_layout(yaxis_range=[0, top_categories_revenue['Total Price'].max() * 1.1], coloraxis_showscale=False)
        fig3.update_xaxes(tickangle=0, tickfont=dict(size=8))
        st.plotly_chart(fig3, use_container_width=True)
    