# import python libraries
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import csv
import re
import plotly.graph_objs as go

# read in the csv to dataframe
df = pd.read_csv('final_jobs_data.csv')
df2 = pd.read_csv('Combined_Version_3.csv')

# initialize the dash app
app = Dash(__name__)

# set the background color and text
colors = {
    'background': '#111111',
    #background': '#333333',
    'text': '#7FDBFF'
}

# chart1 code start
counts = df['Job Website'].value_counts()

fig1 = px.pie(
    counts,
    values=counts.values,
    names=counts.index,
    title='Job Websites'
)

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart1 code end

# chart2 code start
import pandas as pd
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px

filename = 'final_jobs_data.csv'
location_column_name = 'Location'
state_keywords = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'Washington DC'
}

data = pd.read_csv(filename)
location_column = data[location_column_name]
state_counts = Counter()
unmatched_states = set(state_keywords.values())
for location in location_column:
    location_states = []
    for word in location.split():
        if word in state_keywords.values() or word in state_keywords.keys():
            if word in state_keywords.values():
                location_states.append(word)
            else:
                location_states.append(state_keywords[word])
    if location_states:
        state_counts.update(location_states)
        for state in location_states:
            unmatched_states.discard(state)
sorted_state_counts = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)

top_10 = dict(sorted_state_counts[:10])

fig2 = go.Figure(data=[go.Bar(x=list(top_10.keys()), y=list(top_10.values()))])
fig2.update_layout(title='Top 10 States with the Most Job Openings')
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart2 code end

# chart3 code start
fig3 = go.Figure(data=go.Choropleth(
    locations=df2['State Code'], # Spatial coordinates
    z = df2['Yearly Max'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Salary Max",
))
fig3.update_layout(
    title_text = 'Max Salary By State',
    geo_scope='usa', # limite map scope to USA
)
fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart3 code end

# chart4 code start
fig4 = go.Figure(data=go.Choropleth(
    locations=df2['State Code'], # Spatial coordinates
    z = df2['Yearly Min'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Emrld',
    colorbar_title = "Salary Max",
))
fig4.update_layout(
    title_text = 'Min Salary By State',
    geo_scope='usa', # limite map scope to USA
)
fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart4 code end

# chart5 code start
fig5 = px.histogram(df2, x="Yearly Min", nbins=10, title="Minimum Salary Distribution")

fig5.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart5 code end

# chart6 code start
fig6 = px.scatter(df, x="Yearly Min", y="Yearly Max",
                 #size="population",
                 color="Search Parameter", hover_name="Location",
                 log_x=True, size_max=60, title="Salary Range by Job Title")

fig6.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart6 code end

# chart7 code start
# Load data from CSV file
df = pd.read_csv('Combined_Version_3.csv')

# Exclude jobs with Yearly Min salary under $30,000
df = df[df['Yearly Max'] >= 30000]

# Select data scientist, engineer, and analyst positions
job_titles = ['Data Scientist', 'Data Engineer', 'Data Analyst']
df = df[df['Search Parameter'].isin(job_titles)]

# Set color scheme
colors2 = ['#4C72B0', '#55A868', '#C44E52']

# Create a list to hold box traces
traces = []

# Loop through the filtered DataFrame and create a whisker-box trace for each job title
for i, job_title in enumerate(job_titles):
    job_df = df[df['Job Title'] == job_title]
    trace = go.Box(x=job_df['Yearly Max'], name=job_title, boxpoints='all',
                   jitter=0.3, whiskerwidth=0.2, marker_size=8, line_width=2,
                   showlegend=True, marker=dict(color=colors2[i]),
                   hovertemplate='<b>Job Title:</b> ' + job_title +
                                 '<br><b>Yearly Max:</b> %{x:$,.2f}')
    traces.append(trace)

# Create the figure layout
layout = go.Layout(title='Yearly Salaries for Data Science Positions',
                   xaxis_title='Job Title',
                   yaxis_title='Salary ($)',
                   yaxis=dict(automargin=True),
                   xaxis=dict(range=[25000, 300000]))

# Create the figure object
fig7 = go.Figure(data=traces, layout=layout)

fig7.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Display the figure
#fig.show()
# chart7 code end

# chart8 code start
import csv
import re
import plotly.graph_objs as go

keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

keyword_counts = {keyword: 0 for keyword in keywords}

with open('IndeedDataAnalyst_2023.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        text = re.sub(r'[^\w\s]', '', row['Job_Description']).lower()
        for keyword in keywords:
            if keyword.lower() in text:
                keyword_counts[keyword] += 1

sorted_counts = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

counts = [count for _, count in sorted_counts]
labels = [keyword for keyword, _ in sorted_counts]

hist_trace = go.Bar(x=labels, y=counts)

hist_layout = go.Layout(title='Top Skills per Job (Data Analyst)',
                        xaxis={'title': 'Skill'},
                        yaxis={'title': '# of Jobs'})

fig8 = go.Figure(data=[hist_trace], layout=hist_layout)

fig8.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
#fig.show()
# chart8 code end

# chart9 code start
import csv
import re
import plotly.graph_objs as go

keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

keyword_counts = {keyword: 0 for keyword in keywords}

with open('IndeedDataEngineer_2023.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        text = re.sub(r'[^\w\s]', '', row['Job_Description']).lower()
        for keyword in keywords:
            if keyword.lower() in text:
                keyword_counts[keyword] += 1

sorted_counts = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

counts = [count for _, count in sorted_counts]
labels = [keyword for keyword, _ in sorted_counts]

hist_trace = go.Bar(x=labels, y=counts)

hist_layout = go.Layout(title='Top Skills per Job (Data Engineer)',
                        xaxis={'title': 'Skill'},
                        yaxis={'title': '# of Jobs'})

fig9 = go.Figure(data=[hist_trace], layout=hist_layout)
#fig.show()
fig9.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart9 code end

# chart10 code start
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

keyword_counts = {keyword: 0 for keyword in keywords}

with open('Indeed_DataScientist_2023.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        text = re.sub(r'[^\w\s]', '', row['Job_Description']).lower()
        for keyword in keywords:
            if keyword.lower() in text:
                keyword_counts[keyword] += 1

sorted_counts = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

counts = [count for _, count in sorted_counts]
labels = [keyword for keyword, _ in sorted_counts]

hist_trace = go.Bar(x=labels, y=counts)

hist_layout = go.Layout(title='Top Skills per Job (Data Scientist)',
                        xaxis={'title': 'Skill'},
                        yaxis={'title': '# of Jobs'})

fig10 = go.Figure(data=[hist_trace], layout=hist_layout)

fig10.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart10 code end

# set the app layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Data Analytics and Engineering',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Job Market Insights', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='figure 1',
        figure=fig1
    ),
    dcc.Graph(
        id='figure 2',
        figure=fig2
    ),
    dcc.Graph(
        id='figure 3',
        figure=fig3
    ),
    dcc.Graph(
        id='figure 4',
        figure=fig4
    ),
    dcc.Graph(
        id='figure 5',
        figure=fig5
    ),
    dcc.Graph(
        id='figure 6',
        figure=fig6
    ),
    dcc.Graph(
        id='figure 7',
        figure=fig7
    ),
    dcc.Graph(
        id='figure 8',
        figure=fig8
    ),
    dcc.Graph(
        id='figure 9',
        figure=fig9
    ),
    dcc.Graph(
        id='figure 10',
        figure=fig10
    )
])

# connect to the server
if __name__ == '__main__':
    app.run_server(debug=True)
