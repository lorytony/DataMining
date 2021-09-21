from datetime import datetime
from datetime import timedelta

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


#per TESTING - nella versione finale va tolto!
t_now = datetime.strptime("2021-09-19 10:48:47",'%Y-%m-%d %H:%M:%S')
#per FINAL - version
#t_now = datetime.now() - timedelta(days=0,hours=2,minutes=0)
t_prec = t_now - timedelta(days=0,hours=0,minutes=10)

# --------------

app.layout = html.Div(style={'padding':'20px'}, children=[
    html.H2('Apple Sentimental Analysis Dashboard', style={
        'textAlign':'center'
    }),
    html.Div(id='live-update-graph'),
    #html.Div(id='live-update-graph'), non dovrebbe servire
    
    dcc.Interval(
        id='interval-component-slow', #cambiarli nome tipo 'fire...'
        interval= 1000*60*4, # 1 minutes in milliseconds
        n_intervals=1
    )
    ])


        
@app.callback(Output('live-update-graph','children'),
              [Input('interval-component-slow','n_intervals')])#dubbio: non ho capito perchè Input è tra parentesi quadre
def update_graph(n):
    
    global t_now
    global t_prec
    
    labels = ['Neutral','Negative','Positive']
    
    
    values = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }
    
    
    
    
    '''
    
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root"
        password="root",
        database="Twitterdb",
        charset = 'utf8'
        )
    
    
    '''
    
    
    #t_now = datetime.strptime("2020-08-25 10:12:00",'%Y-%m-%d %H:%M:%S')   #t_now = datetime.utcnow()
    
    
    print("timestamp now: {}, timestampOld: {}".format(t_now.strftime('%Y-%m-%d %H:%M:%S'),t_prec.strftime('%Y-%m-%d %H:%M:%S')))
          
          
    #interrogazione query     -----
          
          
    # ---- alternativa:   ----  --------  --------  --------  --------  --------  --------  ----
    
    df_db = pd.read_csv("CleanedTweetsMonitoring.csv",index_col=False)
    df_db['Tweet Datetime'] = pd.to_datetime(df_db['Tweet Datetime'], format='%Y-%m-%d %H:%M:%S')

    del(df_db['index']) #Se non levavo questa colonna non funzionava il groupBy di pandas. 
                        #I conti non venivano fatti a modo...
    
    time_mask = (df_db['Tweet Datetime'] > t_prec) & \
        (df_db['Tweet Datetime'] <= t_now)


    df = df_db[time_mask].reset_index()   
    
    # ----  --------  --------  --------  --------  --------  --------  --------  --------  ----  
    
    
    result = df.groupby([pd.Grouper(key='Tweet Datetime',freq='20s'),'tag']).count().unstack(fill_value=0).stack().reset_index()


    result = result.rename(columns={"Tweet Text":"Num of '{}' mentions".format("Apple"),
                         "Tweet Datetime":"Time in UTC"})
   

    time_series = result["Time in UTC"][result['tag']=='positive'].reset_index(drop=True)

    print(time_series)
          
    y1 = result["Num of '{}' mentions".format("Apple")][result['tag']=='neutral'].reset_index(drop=True)

   
    y2 = result["Num of '{}' mentions".format("Apple")].apply(lambda x: x*-1)[result['tag']=='negative'].reset_index(drop=True)
    y3 = result["Num of '{}' mentions".format("Apple")][result['tag']=='positive'].reset_index(drop=True)
    
    
    list_tags = df['tag'] #result['tag'] ne avrebbe contati di meno
    
    for value in list_tags:
        if(value == 'neutral'):
            values["neutral"] += 1
            
        if(value == 'negative'):
            values["negative"] += 1
            
        if(value == 'positive'):
            values["positive"] += 1
        
        
    
    
    
    
    
    
    #Time counter
    t_interval = timedelta(days=0,hours=0,minutes=10)
    t_prec = t_now 
    t_now = t_now + t_interval
    
    
    
    
    
    children = html.Div([
            
            #html.Div scatter
                html.Div([#pie-chart
                dcc.Graph(
                    id='pie-chart',
                    figure={
                        'data': [
                            go.Pie(
                                labels=labels, 
                                values=[values["positive"], values["negative"], values["neutral"]],
                                name="View Metrics",
                                marker_colors=['rgba(51, 255, 51, 0.6)','rgba(255, 50, 50, 0.6)','rgba(51, 51, 255, 0.6)'],
                                textinfo='value',
                                hole=0.65)
                        ],
                        'layout':{
                            'showlegend':False,
                            'title':'Total Tweets per category',
                            'annotations':[
                                dict(
                                    #text='{0:.1f}K'.format((values["positives"] + values["negatives"] + values["neutrals"])/1000), 
                                    text='{}'.format(values["positive"] + values["negative"] + values["neutral"]),
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
                            line=dict(width=0.5, color='rgb(51, 51, 255)'),
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
                            line=dict(width=0.5, color='rgb(51, 255, 51)'),
                            stackgroup='three' 
                            )
                        ]
                    }
                )
                ], style={'width': '70%', 'display': 'inline-block', 'padding': '0 0 0 20'}),
    ])#html.Div father
    return children
                


if __name__ == '__main__':
    app.run_server(debug=True)