import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import tweetanalytics as twan
import usertweetsanalytics as uta
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.scripts.config.serve_locally = False
app.scripts.append_script({'external_url': 'https://hk-dash-app.herokuapp.com/assets/async_src.js'})
app.scripts.append_script({'external_url': 'https://hk-dash-app.herokuapp.com/assets/gtag.js'})

searchtype = "KS"

cleanfig = {
			'data': [
				{'x': [], 'y': [], 'type': 'bar', 'name': 'words'},
				{'x': [], 'y': [], 'type': 'bar', 'name': 'count'},
			],
			'layout': {
				'title': 'Tweet Analytics'
			}
		}

app.layout = html.Div([
    dcc.Input(id='input-id', type='text'),
    html.Button('Search', id='button'),
	html.Div(id='div-id'),
	dcc.RadioItems(
		id='search-type',
		options=[
			{'label': 'Keyword', 'value': 'KS'},
			{'label': 'User Handle', 'value': 'UH'}
		],
		value='KS'
	), 
	dcc.Graph(
		id='tweet-graph',
		figure=cleanfig
    ),
    html.Div( 
	id='hidden-element',
	style= {'display': 'none'} # Dummy Output placeholder
    )
])

def generate_tidydf(searchword):
	global searchtype
	log.debug('In generate_tidydf() searchtype = {} searchword = {}'.format(searchtype, searchword))
	if searchtype == "UH": 
		tweetdata = uta.get_all_user_tweets(searchword)
	else:
		tweetdata = twan.get_tweet_data(searchword)
	
	if tweetdata is not None:
		df = tweetdata.melt("words")
		return df
	return None

@app.callback(
	Output(component_id='tweet-graph', component_property='figure'),
	[dash.dependencies.Input('button', 'n_clicks')],
	[dash.dependencies.State('input-id', 'value')])
def make_figure(n_clicks, input_value):
	log.info('In make_figure() input_value = {}'.format(input_value))
	if n_clicks is not None:
		tidydf = generate_tidydf(input_value)
		if tidydf is not None:
			return px.bar(tidydf, x="words", y="value", color="variable", barmode="group") 
		return cleanfig
	return dash.no_update

@app.callback(
	Output(component_id='hidden-element', component_property='style'),
	[dash.dependencies.Input('search-type', 'value')]
	)
def update_search_type(input_value):
	global searchtype
	searchtype = input_value
	log.info("In update_search_type() searchtype = {}".format(searchtype))
	
	#no element update needed as only updating global variable
	return dash.no_update
		

if __name__ == '__main__':
    app.run_server(debug=True)
