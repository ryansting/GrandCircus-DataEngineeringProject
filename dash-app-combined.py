# import python libraries
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import csv
import re
from collections import Counter

# read in the csv to dataframe
df = pd.read_csv('final_jobs_data.csv')
df2 = pd.read_csv('Combined_Version_3.csv')
df3 = pd.read_csv('Combined_Version_4.csv')

# initialize the dash app
app = Dash(__name__)

# set the background color and text
colors = {
    'background': '#111111',
    #background': '#333333',
    'text': '#7FDBFF'
}

# chart1 code start
'''
counts = df3['Job Website'].value_counts()

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
'''
# chart1 code end

# chart2 code start
filename = 'Combined_Version_4.csv'
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
df3 = df3[(df3['Yearly Min'].notnull()) & (df3['Yearly Min'] != 0)] # filter out null and 0 values

min_salaries = df3.groupby('State Code')['Yearly Min'].min().reset_index()

fig3 = go.Figure(data=go.Choropleth(
    locations=min_salaries['State Code'], # Spatial coordinates
    z = min_salaries['Yearly Min'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Emrld',
    colorbar_title = "Salary Range",
))

fig3.update_layout(
    title_text = 'Minimum Yearly Salary By State',
    geo_scope='usa', # limit map scope to USA
)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig.show()
# chart3 code end

# chart4 code start
# Group the dataframe by 'State Code' and take the max of 'Yearly Max' column
Max_Salary = df3.groupby('State Code')['Yearly Max'].max()

fig4 = go.Figure(data=go.Choropleth(
    locations=Max_Salary.index, # Spatial coordinates
    z = Max_Salary.values.astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Salary Max",
))

fig4.update_layout(
    title_text = 'Maximum Yearly Salary By State',
    geo_scope='usa', # limit map scope to USA
)

fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig.show()
# chart4 code end

# chart5 code start
fig5 = px.histogram(df2, x="Yearly Min", nbins=10, title="Minimum Salary Distribution")

'''
fig5.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
'''
# chart5 code end

# chart6 code start
fig6 = px.scatter(df, x="Yearly Min", y="Yearly Max",
                 #size="population",
                 color="Search Parameter", hover_name="Location",
                 log_x=True, size_max=60, title="Salary Range by Job Title")
'''
fig6.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
'''
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

# chart11 code start
mi_jobs = df[df['Location'].str.contains('MI|Michigan')]
job_counts = mi_jobs['Search Parameter'].value_counts()
fig11 = px.pie(job_counts, values=job_counts.values, names=job_counts.index, title="Job Types in MI")

fig11.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 11 code end

# chart 12 code start
df_new = df3.query("`Job Website` == 'Indeed'")
df_new = df_new[df['Skills'].notnull()]
df_new = df_new['Skills'].str.split(',').explode('Skills').value_counts().head(20)

fig12 = px.bar(df_new, labels={}, title ="Indeed Top Skills")

fig12.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# chart 12 code end

# chart 13 code start
grouped_df = df.groupby('Search Parameter')['Job Title'].nunique().reset_index()

data = [
    go.Bar(
        x=grouped_df['Search Parameter'],
        y=grouped_df['Job Title']
    )
]

layout = go.Layout(
    title='Number of Job Titles Available for Each Search Parameter',
    xaxis={'title': 'Search Parameter'},
    yaxis={'title': 'Number of Job Titles'}
)

fig13 = go.Figure(data=data, layout=layout)

fig13.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 13 code end

# chart 14 code start
df['Remote'] = df['Remote'].fillna("Non-Remote")
remote_jobs = df2['Remote'].value_counts()


fig14 = px.pie(remote_jobs, values=remote_jobs.values, names=['Remote', 'Non-Remote'],
             title='Remote vs Non-Remote Jobs',
             labels={'Remote': 'Remote Jobs', 'Non-Remote': 'Non-Remote Jobs'},
             hole=0.5,
             )

fig14.update_traces(marker=dict(colors=['#636EFA', '#EF553B']))

fig14.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 14 code end

# chart 15 code start
# Load the data from the CSV file
#df = pd.read_csv('Combined_Version_3.csv')

# Filter out rows with null or zero values in Search Parameter column
df3 = df3[df3['Search Parameter'].notnull() & (df3['Search Parameter'] != 0)]

# Define the job titles and colors for the legend
job_titles = ['Data Analyst', 'Data Scientist', 'Data Engineer', 'All']
colors3 = ['Teal', 'Purpor', 'Oryel', 'Turbid']

# Create an empty list to store the traces for each job title
data = []

# Loop through each job title and create a choropleth trace
for i, title in enumerate(job_titles):
    # Filter the data for the current job title
    if title == 'All':
        filtered_df = df3
    else:
        filtered_df = df3[df3['Job Title'] == title]
    # Group the data by state and find the count of jobs for each state
    state_freq = filtered_df.groupby('State Code')['Search Parameter'].count()
    # Create the choropleth trace for the current job title
    trace = go.Choropleth(
        locations=state_freq.index, # Spatial coordinates
        z=state_freq.astype(float), # Data to be color-coded
        locationmode='USA-states', # set of locations match entries in `locations`
        colorscale=colors3[i],
        colorbar_title="Job Frequency",
        visible=(i==0) # Only show the first trace by default
    )
    # Add the trace to the list of traces
    data.append(trace)

# Create the layout for the figure
layout = go.Layout(
    title_text='Job Frequency By State',
    geo_scope='usa', # limit map scope to USA,
    updatemenus=[dict(
        type='buttons',
        showactive=True,
        buttons=[dict(
            label=title,
            method='update',
            args=[{'visible': [i==j for j in range(len(job_titles))]}]
        ) for i, title in enumerate(job_titles)]
    )]
)

# Create the figure using the data and layout
fig15 = go.Figure(data=data, layout=layout)

fig15.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Show the figure
# fig.show()
# chart 15 code end

# chart 16 code start
count_data = df3['Job Website'].value_counts().reset_index()
count_data.columns = ['Job Website', 'Count']

# Create the treemap chart
fig16 = px.treemap(count_data, path=['Job Website'], values='Count',
                 color='Job Website', color_discrete_map={'Indeed': 'blue'})

# Customize the font and color
fig16.update_traces(textfont_size=16, textfont_color='white')

fig16.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 16 code end

# chart 17 code start
#Top Skills In Data Science

import csv
import re

# List of keywords to search for
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

# Create a dictionary to store the keyword counts
keyword_counts = {keyword: 0 for keyword in keywords}

# Open the CSV file and iterate over each row
with open('Combined_Version_4.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert the text to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', row['Skills']).lower()

        # Count the occurrences of each keyword in the text
        for keyword in keywords:
            if keyword.lower() in text:
                keyword_counts[keyword] += 1

# Sort the keyword counts in descending order
sorted_counts = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)


for keyword, count in sorted_counts:
    print(f'{keyword}: {count}')

#Pie Chart of Top 10 Skills
skill_counts = df3['Skills'].str.split(',').explode().str.strip().value_counts().nlargest(10)

# Create a pie chart using Plotly Express
fig17 = px.pie(
    skill_counts,
    values=skill_counts.values,
    names=skill_counts.index,
    title='Top 10 Data Science Skills'
)

fig17.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 17 code end

# chart 18 code start
skill_counts = df3['Skills'].str.split(',').explode().str.strip().value_counts().nlargest(10)

skill_counts = skill_counts.rename_axis('Skills')

fig18 = px.bar(
    skill_counts,
    x=skill_counts.index,
    y=skill_counts.values,
    color=skill_counts.index,
    labels={'x':'Skills','y':'Count'}
)

# Center the chart title
fig18.update_layout(
    title={
        'text': 'Top 10 Data Science Skills',
        'x': 0.5,
        'xanchor': 'center'
    }
)

fig18.update_xaxes(title='Skills')
fig18.update_yaxes(title='Count')
fig18.update_layout(xaxis={'categoryorder':'total descending'})

fig18.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig.show()
# chart 18 code end

# chart 19 code start
'''
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

state_salary = df3.groupby('State Code')['Yearly Max'].max()
top_states = state_salary.sort_values(ascending=False)[:5]
state_names = [state_keywords[state_code] for state_code in top_states.index]

frames = []  #establishes the frame of the graph during the animation

fig19 = go.Figure(
    data=[go.Bar(
        x=state_names,
        y=top_states,
        marker_color='rgb(158, 202, 225)',
        frames=frames
    )],
)

for i in range(1, len(top_states) + 1):
    frame = go.Frame(
        data=[go.Bar(
            x=state_names[:i+1],
            y=top_states[:i+1],
            marker_color='rgb(158, 202, 225)',
        )],
        layout=go.Layout(
            xaxis_title='State',
            yaxis_title='Yearly Max Salary ($)',
            title='Top 5 States by Yearly Max Salary'
        )
    )
    frames.append(frame)



fig19.update_layout(
    xaxis_title='State',
    yaxis_title='Yearly Max Salary ($)',
    title='Top 5 States by Yearly Max Salary',
    updatemenus=[  #start of the play button and animation
        dict(
            type='buttons',
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
                ),
                dict(
                    label='Pause',
                    method='animate',
                    args=[[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}]
                )
            ],
            showactive=False,
            x=1,
            y=1.5,
            pad=dict(t=30, r=10),
        )
    ]
)
'''
# chart 19 code encoding

# chart 20 code start
# Read in the data
data = pd.read_csv('Final Data For Jobs.csv')

# Define the pattern to extract years of experience from the job description
pattern = r'([0-9]+) years of experience'

# Use the pattern to search for years of experience in the job descriptions
experience_data = data['Job Description'].str.extract(pattern)

# Convert the resulting string values to numeric values
experience_data = pd.to_numeric(experience_data[0], errors='coerce')

# Replace missing values with the median years of experience
experience_data.fillna(experience_data.median(), inplace=True)

# Add the years of experience data to the original dataframe
data['Years of Experience'] = experience_data

# Select the columns for salary and years of experience
salary_experience_data = data[['Yearly Max', 'Years of Experience', 'Job Title']]

# Filter out any rows with more than 25 years of experience
salary_experience_data = salary_experience_data[salary_experience_data['Years of Experience'] <= 25]

# Create a scatter plot with salary on the y-axis and years of experience on the x-axis
fig20 = px.scatter(salary_experience_data, x='Years of Experience', y='Yearly Max', hover_name='Job Title', hover_data=['Yearly Max'])

# Set the y-axis range to be a bit more spread out
fig20.update_yaxes(range=[0, salary_experience_data['Yearly Max'].max() * 1.1])

fig20.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Show the plot
#fig.show()
# chart 20 code end

# chart 21 code start
'''
df_new = df3.query("`Location` == 'Remote'")
df_new = df3.groupby('Job Website').count()
fig21 = px.bar(df2, y='Search Parameter', labels={}, title ="Indeed Top Skills")
'''
# chart 21 code end


page_style = {'textAlign': 'center','color': colors['text']}
#style={'textAlign': 'center','color': colors['text']}

# set the app layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Data Analytics and Engineering',
        style=page_style,
    ),
    html.Div(children='Job Market Insights', style=page_style
    ),
    dcc.Tabs([
    dcc.Tab(
        label='Skills',
        style={'color': '#222222','backgroundColor': '#999999'}, children=[
        html.Button('Download CSV', id='btn-download-csv'),
        dcc.Download(id='download-csv'),
        dcc.Dropdown(
        options=['Data Analyst', 'Data Engineer', 'Data Scientist'],
        value='Data Analyst',
        style={'color': '#222222','backgroundColor': '#999999'},
        id='fig-18-dropdown'
        ),
        dcc.Graph(
            id='figure 18',
            figure=fig18
        ),
        html.H5(
            children="Graph 18 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 18...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 17',
            figure=fig17
        ),
        html.H5(
            children="Graph 17 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 17...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 8',
            figure=fig8
        ),
        html.H5(
            children="Graph 8 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 8...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 9',
            figure=fig9
        ),
        html.H5(
            children="Graph 9 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 9...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 10',
            figure=fig10
        ),
        html.H5(
            children="Graph 10 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 10...",
            style=page_style
        ),
        #dcc.Graph(
            #id='figure 1',
            #figure=fig1
        #),
        #html.H5(
            #children="Graph 1 Insights",
            #style=page_style
        #),
        #html.P(
            #"Here are our conclusions on Graph 1...",
            #style=page_style
        #),
        #dcc.Dropdown(
        #options=['Data Analyst', 'Data Engineer', 'Data Scientist'],
        #value='Data Analyst',
        #style={'color': '#222222','backgroundColor': '#999999'},
        #id='fig-3-dropdown'
        #),

        #dcc.RangeSlider(
            #df['Yearly Min'].min(),
            #df['Yearly Min'].max(),
            #10000,
            #value=[80000, 150000],
            #style={'backgroundColor': 'green'},
            #id='fig-12-slider'),
        dcc.Graph(
            id='figure 16',
            figure=fig16
        ),
        html.H5(
            children="Graph 16 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 16...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 12',
            figure=fig12
        ),
        html.H5(
            children="Graph 12 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 12...",
            style=page_style
        ),
    ]),
    dcc.Tab(
        label='Location',
        style={'color': '#222222','backgroundColor': '#999999'}, children=[
        dcc.Graph(
            id='figure 4',
            figure=fig4
        ),
        html.H5(
            children="Graph 4 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 4...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 3',
            figure=fig3
        ),
        html.H5(
            children="Graph 3 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 3...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 15',
            figure=fig15
        ),
        html.H5(
            children="Graph 15 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 15...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 2',
            figure=fig2
        ),
        html.H5(
            children="Graph 2 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 2...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 14',
            figure=fig14
        ),
        html.H5(
            children="Graph 14 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 14...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 13',
            figure=fig13
        ),
        html.H5(
            children="Graph 13 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 13...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 11',
            figure=fig11
        ),
        html.H5(
            children="Graph 11 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 11...",
            style=page_style
        ),
    ]),
    dcc.Tab(
        label='Salary',
        style={'color': '#222222','backgroundColor': '#999999'}, children=[
        html.Div([
        dcc.Graph(
            id='figure 7',
            figure=fig7
        ),
        html.H5(
            children="Graph 7 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 7...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 6',
            figure=fig6
        ),
        dcc.RangeSlider(
            df['Yearly Min'].min(),
            df['Yearly Min'].max(),
            10000,
            value=[80000, 150000],
            #style={'backgroundColor': 'green'},
            id='fig-6-slider'),
        html.H5(
            children="Graph 6 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 6...",
            style=page_style
        ),
        dcc.RadioItems(
            options=['Data Analyst', 'Data Engineer', 'Data Scientist'],
            value='Data Analyst',
            inline=True,
            style={'color': '#222222','backgroundColor': '#999999'},
            id='fig-5-radio'
        ),
        dcc.Graph(
            id='figure 5',
            figure=fig5
        ),
        html.H5(
            children="Graph 5 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 5...",
            style=page_style
        ),
        dcc.Graph(
            id='figure 20',
            figure=fig20
        ),
        html.H5(
            children="Graph 5 Insights",
            style=page_style
        ),
        html.P(
            "Here are our conclusions on Graph 5...",
            style=page_style
        ),
        #dcc.Graph(
            #id='figure 21',
            #figure=fig21
        #),
        #html.H5(
            #children="Graph 21 Insights",
            #style=page_style
        #),
        #html.P(
            #"Here are our conclusions on Graph 21...",
            #style=page_style
        #),
        #dcc.Graph(
            #id='figure 19',
            #figure=fig19
        #),
        #html.H5(
            #children="Graph 19 Insights",
            #style=page_style
        #),
        #html.P(
            #"Here are our conclusions on Graph 19...",
            #style=page_style
        #),
    ]),
    ]),
])
])

# callback function download csv button
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True)

def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, 'data_science_jobs.csv')

#@app.callback(
    #Output('slider-output-container', 'children'),
    #Input('my-slider', 'value'))
#def update_output(value):
    #return 'You have selected "{}"'.format(value)

# callback function for slider fig 6
@app.callback(
    Output('figure 6', 'figure'),
    Input('fig-6-slider', 'value'))
def update_figure(selected_salary):
    filtered_df = df[df['Yearly Min'].between(selected_salary[0], selected_salary[1])]

    fig = px.scatter(filtered_df, x="Yearly Min", y="Yearly Max",
                     #size="pop",
                     color="Search Parameter", hover_name="Location",
                     log_x=True, size_max=55)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig

# callback function for radio fig 5
@app.callback(
    Output('figure 5', 'figure'),
    Input('fig-5-radio', 'value'))
def update_figure(selected_job_title):
    filtered_df = df[df['Search Parameter'] == selected_job_title]

    fig = px.histogram(filtered_df, x="Yearly Min", nbins=10, title="Minimum Salary Distribution")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig

# callback function for dropdown fig 3
'''
@app.callback(
    Output('figure 3', 'figure'),
    Input('fig-3-dropdown', 'value'))
def update_figure(selected_job_title):
    filtered_df = df[df['Search Parameter'] == selected_job_title]

    fig = go.Figure(data=go.Choropleth(
        locations=filtered_df['State Code'], # Spatial coordinates
        z = filtered_df['Yearly Max'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Salary Max",
    ))
    fig.update_layout(
        title_text = 'Max Salary By State',
        geo_scope='usa', # limite map scope to USA
    )

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig
'''
# callback function for dropdown fig 18

@app.callback(
    Output('figure 18', 'figure'),
    Input('fig-18-dropdown', 'value'))
def update_figure(selected_job_title):
    filtered_df = df3[df3['Search Parameter'] == selected_job_title]
    skill_counts = filtered_df['Skills'].str.split(',').explode().str.strip().value_counts().nlargest(10)
    skill_counts = skill_counts.rename_axis('Skills')

    fig = px.bar(
    skill_counts,
    x=skill_counts.index,
    y=skill_counts.values,
    color=skill_counts.index,
    labels={'x':'Skills','y':'Count'}
    )

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig

# callback function for dropdown fig 12
'''
@app.callback(
    Output('figure 12', 'figure'),
    Input('fig-12-slider', 'value'))
def update_figure(selected_salary):
    filtered_df = df_new[df_new['Yearly Min'].between(selected_salary[0], selected_salary[1])]

    #filtered_df = df3.query("`Job Website` == 'Indeed'")
    #filtered_df = filtered_df[df3['Skills'].notnull()]
    #filtered_df = filtered_df['Skills'].str.split(',').explode('Skills').value_counts().head(20)

    fig = px.bar(filtered_df, labels={}, title ="Indeed Top Skills")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig
'''


# connect to the server
if __name__ == '__main__':
    app.run_server(debug=True)
