import pandas as pd

df = pd.read_csv('https://www.dropbox.com/s/txbep2ps7h54e7g/Combined_Version_2.csv?dl=1')

grouped_df = df.groupby('Search Parameter')['Job Title'].nunique().reset_index()

import plotly.graph_objs as go

data = [
    go.Bar(
        x=grouped_df['Search Parameter'],
        y=grouped_df['Job Title Count']
    )
]

layout = go.Layout(
    title='Number of Job Titles Available for Each Search Parameter',
    xaxis={'title': 'Search Parameter'},
    yaxis={'title': 'Number of Job Titles'}
)

fig = go.Figure(data=data, layout=layout)

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Number of Job Titles Available for Each Search Parameter'),

    dcc.Graph(
        id='job-title-bar-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)


