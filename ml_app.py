import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import os
from modules.ml_models_code import multi_target_linear_regression
from modules.clean_data import stock_close_analysis_df, stock_analysis_df, stock_data, corr_matrix, app_description, ml_results_description_dict 
from modules.load_models import linear_regression_dict, lgbm_regressor_dict, svr_dict, nu_svr_dict, linear_svr_dict, sgd_regressor_dict,  decision_tree_regressor_dict, gradient_boosting_regressor_dict, mlp_regressor_dict, kernel_ridge_dict, bayesian_ridge_dict

import streamlit as st
import streamlit.components.v1 as components


pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

# Header 
st.markdown(
    """
    <style>
     /* Define font size and color for st.write text */
    body {
        color: grey;
        text-shadow: 2px 2px white;
        font-size: 12 px;
    }
    </style>
    """,
    unsafe_allow_html=True)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url(https://c0.wallpaperflare.com/preview/968/798/549/5be98a7d18e35.jpg);
background-position: bottom;
background-size: cover;
}

[data-testid="stSidebar"] {
background-image: url(https://coolbackgrounds.io/images/backgrounds/white/white-unsplash-9d0375d2.jpg);
background-size: cover;
background-position: right;
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}

</style>
"""
html_string = '''

<script>
  window.chatbaseConfig = {
    chatbotId: "BVBAK0IYTdwsPWu5mCyZh",
  }
</script>
<script
  src="https://www.chatbase.co/embed.min.js"
  id="BVBAK0IYTdwsPWu5mCyZh"
  defer>
</script>

    '''
st.markdown(page_bg_img, unsafe_allow_html=True)
# st.sidebar.header("Banks")
  # JavaScript works

#Header
def main():
    st.title("Banking Stock Portfolio with Machine Learning and Algorithms")
    st.write("*Chris Cummock, Eyasu Alemu,Gregory Krulin,John Garcia, Mark Beers, and Samuel Jew*", unsafe_allow_html=True)
    st.write('---', unsafe_allow_html=True)
 
   
if __name__ == '__main__':
    main()
    
#Outline
st.write("In our solution we used a selection of bank stock data we gathered to determine potential gains throughout ones' portfolio. In order to do this we have used a ML(machine learning) algorithm to drop a portfolio inside of our questionnaire and it will return potential gains/loses.", unsafe_allow_html=True)
st.write("One model will focus on Macroeconomic/fundamental analysis data, while the other will focus on technical indicators. Ideal will be using the first model to “teach” 2nd some parameters.", unsafe_allow_html=True)
st.write("Steps to build the solution", unsafe_allow_html=True)
st.write("- Steps 1: Data Collection", unsafe_allow_html=True)
st.write("- Steps 2: EDA", unsafe_allow_html=True)
st.write("- Steps 3: Create Baseline", unsafe_allow_html=True)
st.write("- Steps 4: Create 2 ML Models", unsafe_allow_html=True)
st.write("- Steps 5: Create Analysis Platform", unsafe_allow_html=True)

#Script
stock_ml_dict = linear_regression_dict

ml_features = list(stock_ml_dict['BAC_Close'].keys())


#Functions
def get_lin_reg_results(reg_dict, stock, result):
    st.markdown(ml_results_description_dict[result])
    return reg_dict[stock][result]

def corr_heat_plot(corr_matrix_df):#, target):
    fig = px.imshow(
        corr_matrix_df, 
        #x= corr_matrix_df[target].index, 
        y= corr_matrix.columns,  width = 1000, height = 800
        ).update_layout(yaxis_nticks=len(list(corr_matrix_df.columns)),
                        xaxis_nticks = 1)
    return fig

def corr_heat_plot2(corr_matrix_df):#, targets):
    fig = px.imshow(corr_matrix_df)#, x= corr_matrix_df[targets])
    return fig


#Widget Functions
def stock_select():
    return  st.selectbox("Stock", list(stock_ml_dict.keys()))

def results_widget():
    return st.selectbox("Linear Regression Results", ml_features )

def variable_widget():
    return st.selectbox("variable", list(stock_close_analysis_df.columns))

def stock_graph_multi_select():
    return st.multiselect('MultiSelect', list(stock_close_analysis_df.columns), default= ['BAC_Close'])

def variable_widget2():
    return st.multiselect("variable", list(corr_matrix.columns), default=['BAC_Close', 'C_Close'])


#Bound functions
def bound_plot():
    return get_lin_reg_results(stock_ml_dict, stock_select(),   results_widget())

def bound_bar_plot():
    return corr_heat_plot(corr_matrix)#, variable_widget())

def bound_bar_multi_plot2():
    return corr_heat_plot2(corr_matrix, variable_widget2())


#Apps
def ml_results_tab():
    return st.title('Bank Stock Portfolio Analysis'), st.header('ML Results'), st.write(bound_plot())
       
def stock_graphs():
    return st.header('Data Graphs'), st.plotly_chart(px.line(stock_analysis_df, y= stock_graph_multi_select(), width = 1000, height = 600))

def corr_graph1():
    return st.header('Stock and Economic Data Correlation'), st.plotly_chart(bound_bar_plot())

def corr_graph2():
    return st.header('Stock Corr App2'), st.plotly_chart(bound_bar_multi_plot2())


#Full Application
def app_tabs_application():
    tab01, tab1, tab2, tab4 =st.tabs([ "App instructions", "Correlation", "Stock Graphs", "Machine Learning Results"])

    with tab01:
        st.markdown(app_description , unsafe_allow_html=True)
    
    with tab1:
        corr_graph1()

    with tab2:
        stock_graphs()

    #with tab3:
        #corr_graph2()

    with tab4:
        ml_results_tab()

app_tabs = app_tabs_application()

components.html(html_string, width=1000, height=450, scrolling=False)
