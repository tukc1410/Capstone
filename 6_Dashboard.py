import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
import matplotlib.pyplot as plt
import streamlit as st
#Create app
app = dash.Dash(__name__)
#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
#Task 1 Add the Title to the Dashboard
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
#outer division starts
#Task 2 
     #html.Div([
                   # First inner divsion for  adding dropdown helper text for Selected Drive wheels
                                html.Div([
                                        html.H2('Select Launch Site:', style={'margin-right': '2em'}),

                                #Select sites                 
                                        dcc.Dropdown(id='id',
                                                options=[
                                                    {'label': 'All sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                )
                                        ]),                                          

                #])
            #outer division ends
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                   

])
#layout ends

#Task 4                   
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='id', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]  # Filter for successful launches
        fig = px.pie(filtered_df, 
                    values='class', 
                    names='Launch Site', 
                    title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        title = f"Total Success Launches for site {entered_site}"
        fig = px.pie(filtered_df, values='class count', names='class', title=title)
        return fig

 
if __name__ == '__main__':
    app.run_server()
    