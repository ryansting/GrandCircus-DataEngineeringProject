import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

# Load data from CSV file
df = pd.read_csv('Combined_Version_3.csv')

# Exclude jobs with Yearly Min salary under $30,000
df = df[df['Yearly Max'] >= 30000]

# Select data scientist, engineer, and analyst positions
job_titles = ['Data Scientist', 'Data Engineer', 'Data Analyst']
df = df[df['Search Parameter'].isin(job_titles)]

# Set color scheme
colors = ['#4C72B0', '#55A868', '#C44E52']

# Create a list to hold box traces
traces = []

# Loop through the filtered DataFrame and create a whisker-box trace for each job title
for i, job_title in enumerate(job_titles):
    job_df = df[df['Job Title'] == job_title]
    trace = go.Box(x=job_df['Yearly Max'], name=job_title, boxpoints='all',
                   jitter=0.3, whiskerwidth=0.2, marker_size=8, line_width=2,
                   showlegend=True, marker=dict(color=colors[i]),
                   hovertemplate='<b>Job Title:</b> ' + job_title +
                                 '<br><b>Yearly Max:</b> %{x:$,.2f}')
    trace.update_customdata(job_df[['Company Name', 'Location', 'Job Description']])
    traces.append(trace)

# Create the figure layout
layout = go.Layout(title='Yearly Salaries for Data Science Positions',
                   xaxis_title='Job Title',
                   yaxis_title='Salary ($)',
                   yaxis=dict(automargin=True),
                   xaxis=dict(range=[25000, 300000]))

# Create the figure object
fig = go.Figure(data=traces, layout=layout)

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='Yearly Salaries for Data Science Positions'),
    dcc.Graph(
        id='salary-graph',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
 
