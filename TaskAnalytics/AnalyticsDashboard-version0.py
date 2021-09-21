import plotly
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output #altrimenti non vanno le @app.callback

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


"""
Versione TESTING:
"""

data = ['2021-08-28 17:50:50','2021-08-28 17:51:10','2021-08-28 17:51:30','2021-08-28 17:51:50','2021-08-28 17:52:20','2021-08-28 17:52:50','2021-08-28 17:53:10','2021-08-28 17:54:10','2021-08-28 17:54:50','2021-08-28 17:55:10']


text = ["Bello de","Super!","Va bene","Continua così","Mitico!","Male","Malino","Non bene","Ahia ahiai..","Non bene"]
polarity = [1,1,1,1,1,-1,-1,-1,-1,-1]
dataset = {'polarity':polarity}
df = pd.DataFrame(dataset, index = data)


# --------------

app.layout = html.Div(style={'padding':'20px'}, children=[
    html.H2('Monitoraggio mega per la Apple', style={
        'textAlign':'center'
    }),
    html.Div(id='live-update-graph'),
    #html.Div(id='live-update-graph'), non dovrebbe servire
    
    dcc.Interval(
        id='interval-component-slow', #cambiarli nome tipo 'fire...'
        interval= 1000*60*1, # 1 minutes in milliseconds
        n_intervals=1
    )
    ])

var = "ciao"
print(var)
        
@app.callback(Output('live-update-graph','children'),
              [Input('interval-component-slow','n_intervals')])#dubbio: non ho capito perchè Input è tra parentesi quadre
def update_graph(n):
    
    
    
    time_series = ["17:30","17:35","17:40"]
    y1 = [2,5,6]
    y2 = [-1,-3,-5]
    y3 = [11,8,12]
    print("Dentro la callback!!")
    labels = ['Neutral','Negative','Positive']
    values = {
        "positives": 30,
        "negatives": 10,
        "neutrals": 20,
    }
    
    
    children = html.Div([
            
            html.Div([#scatter
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                figure={
                    'data': [
                        go.Scatter(
                            x=time_series,
                            y=y1,
                            name="Neutrals",
                            opacity=0.8,
                            mode='lines',
                            line=dict(width=0.5, color='rgb(131, 90, 241)'),
                            stackgroup='one' 
                        ),
                        go.Scatter(
                            x=time_series,
                            y=y2,
                            name="Negatives",
                            opacity=0.8,
                            mode='lines',
                            line=dict(width=0.5, color='rgb(255, 50, 50)'),
                            stackgroup='two' 
                        ),
                        go.Scatter(
                            x=time_series,
                            y=y3,
                            name="Positives",
                            opacity=0.8,
                            mode='lines',
                            line=dict(width=0.5, color='rgb(184, 247, 212)'),
                            stackgroup='three' 
                            )
                        ]
                    }
                )
                ], style={'width': '70%', 'display': 'inline-block', 'padding': '0 0 0 20'}),#html.Div scatter
                html.Div([#pie-chart
                dcc.Graph(
                    id='pie-chart',
                    figure={
                        'data': [
                            go.Pie(
                                labels=labels, 
                                values=[values["positives"], values["negatives"], values["neutrals"]],
                                name="View Metrics",
                                marker_colors=['rgba(184, 247, 212, 0.6)','rgba(255, 50, 50, 0.6)','rgba(131, 90, 241, 0.6)'],
                                textinfo='value',
                                hole=0.65)
                        ],
                        'layout':{
                            'showlegend':False,
                            'title':'Total Tweets per category',
                            'annotations':[
                                dict(
                                    #text='{0:.1f}K'.format((values["positives"] + values["negatives"] + values["neutrals"])/1000), 
                                    text='{}'.format(values["positives"] + values["negatives"] + values["neutrals"]),
                                    font=dict(
                                        size=40
                                    ),
                                    showarrow=False
                                )
                            ]
                        }

                    }
                )
            ], style={'width': '27%', 'display': 'inline-block'}),#html.Div pie-chart
            html.Div([#html.Div Bar
                dcc.Graph(
                    id='x-time-series',
                    figure = {
                        'data':[
                            go.Bar(                          
                               # x=fd["Frequency"].loc[::-1],
                                #y=fd["Word"].loc[::-1], 
                                x = [5,10,26,60,80,140],
                                y = ["Hello","Ciao","Bonsuar","Hola","Helo","Dazvidania"],
                                name="Neutrals", 
                                orientation='h',
                                marker_color='rgba(131, 90, 241, 0.6)',
                                marker=dict(
                                    line=dict(
                                        color='rgba(131, 90, 241, 0.6)',
                                        width=1),
                                    ),
                            )
                        ],
                        'layout':{
                            'hovermode':"closest"
                        }
                    }        
                )
            ], style={'width': '70%', 'display': 'inline-block', 'padding': '20 0 0 20'}),#html.Div Bar
    ])#html.Div father
    return children
                


if __name__ == '__main__':
    app.run_server(debug=True)