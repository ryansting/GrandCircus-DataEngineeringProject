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
df4 = pd.read_csv('FinalJobDataUpdated.csv')

# initialize the dash app
app = Dash(__name__)

# set the background color and text
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# skills keyword list
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

# states keyword dictionary
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

# chart1 code start
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
# chart1 code end

# chart2 code start
filename = 'Combined_Version_4.csv'
location_column_name = 'Location'

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
# chart5 code end

# chart6 code start
fig6 = px.scatter(df, x="Yearly Min", y="Yearly Max",
                 #size="population",
                 color="Search Parameter", hover_name="Location",
                 log_x=True, size_max=60, title="Salary Range by Job Title")
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

fig15 = go.Figure(data=data, layout=layout)

fig15.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
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

skill_counts = df3['Skills'].str.split(',').explode().str.strip().value_counts().nlargest(10)

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
    title='Top 10 Data Science Skills',
    color=skill_counts.index,
    labels={'x':'Skills','y':'Count'}
)

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
# chart 18 code end

# chart 19 code start
# chart 19 code end

# chart 20 code start
data = pd.read_csv('Final Data For Jobs.csv')
pattern = r'([0-9]+) years of experience'

experience_data = data['Job Description'].str.extract(pattern)
experience_data = pd.to_numeric(experience_data[0], errors='coerce')
experience_data.fillna(experience_data.median(), inplace=True)

data['Years of Experience'] = experience_data
salary_experience_data = data[['Yearly Max', 'Years of Experience', 'Job Title']]
salary_experience_data = salary_experience_data[salary_experience_data['Years of Experience'] <= 25]

fig20 = px.scatter(salary_experience_data, x='Years of Experience', y='Yearly Max', hover_name='Job Title', hover_data=['Yearly Max'])
fig20.update_yaxes(range=[0, salary_experience_data['Yearly Max'].max() * 1.1])

fig20.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 20 code end

# chart 21 code start
company_counts = df3['Company Name'].value_counts().head(15)

company_names = company_counts.index[::-1]
entry_counts = company_counts.values[::-1]

bar_trace = go.Bar(
    x=entry_counts,
    y=company_names,
    orientation='h',  # Set orientation to horizontal
    marker_color='orchid',  # Set marker color
)

fig21 = go.Figure()
fig21.add_trace(bar_trace)

fig21.update_layout(
    xaxis_title='Number of Entries',
    yaxis_title='Company',
    title='<b>Top 15 Companies with the Most Openings</b>',  # Bold and center the title
    bargap=0.2,  # Set the gap between bars
    plot_bgcolor='rgb(153, 201, 69)'
)

fig21.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
# chart 21 code end

# chart 22 code start
fig22 = px.histogram(df2, x="Yearly Max", nbins=10, title="Minimum Salary Distribution")
# chart 22 code end

# chart 23 code start

state_salary = df3.groupby('State Code')['Yearly Max'].max()
top_states = state_salary.sort_values(ascending=False)[:5]
state_names = [state_keywords[state_code] for state_code in top_states.index]

frames = []  #establishes the frame of the graph during the animation
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

fig23 = go.Figure(
    data=[go.Bar(
        x=state_names,
        y=top_states,
        marker_color='rgb(158, 202, 225)',
    )],
    frames=frames
)



fig23.update_layout(
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

fig23.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# code chart 23 end

# code chart 24 start
# chart 24 code end

# chart 25 code start
# chart 25 code end

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
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            children="Top Skill for each respective position: Data Analyst = Excel, Data Engineer = SQL, Data Scientist = Python",
            style=page_style
        ),
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
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Top 10 Skills Insights: SQL, Python, and Excel are the top 3 In-Demand Data Science Skills. However, these skills vary by job title.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 17',
            figure=fig17
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Excel and Reporting skills stand out as additional requirements for Data Analysts.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 8',
            figure=fig8
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Cloud Computing and Big Data skills such as AWS and Spark stand out as additional requirements for Data Engineers.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 9',
            figure=fig9
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Machine Learning and Statistics skills stand out as additional requirements for Data Scientists.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 10',
            figure=fig10
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Majority of the job postings we analyzed was from Indeed due to it being the most popular website for job searching.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 16',
            figure=fig16
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Over 75% of the job postings we collected was from Indeed.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 1',
            figure=fig1
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Top Skills in Data Science went along with our assumption including Python and SQL leading the way. Rest of skills lineup depending on what position you are seeking.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 12',
            figure=fig12
        ),
    ]),
    dcc.Tab(
        label='Location',
        style={'color': '#222222','backgroundColor': '#999999'}, children=[
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "This map shows the highest paying jobs that require an employee to come into a physical office. As expected, many of the higher cost of living states such as Massachusetts, California, New York & New Jersey also have some of the highest paying jobs. Outside of the cost of living, many companies are headquartered in these tax-haven locations. ",
            style=page_style
        ),
        dcc.Graph(
            id='figure 4',
            figure=fig4
        ),
        html.H2(
            children="",
            style=page_style
        ),
        html.P(
            "This map displays the minimum salaries per state and while some states will have a smaller sample size due to fewer listings, it can help give a good baseline of where entry jobs can be found.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 3',
            figure=fig3
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "This map shows the frequency of jobs by location around the US. While it excludes fully remote job posts, we’re able to see that regardless of job title, places like Silicon Valley known for Tech and New York known for Finance/ analytics have the most job listings. Other states such as New Jersey feeds off New York City jobs and Texas has many oil & gas companies such as Chevron in the area.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 15',
            figure=fig15
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Top 10 States With Job Openings: We had originally predicted that California, Texas, and New York would have the most job openings due to having the highest population. Our data showed that #1 is California, #2 is New York, and #3 is Washington DC. Texas was listed as #9",
            style=page_style
        ),
        dcc.Graph(
            id='figure 2',
            figure=fig2
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Highest paying states lineup mostly with our assumptions based on cost of living in top states like New York and California.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 23',
            figure=fig23
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Prominent tech companies such as TikTok, IBM, and Meta have a high number of openings in the field. Premier Staffing Solution is an outlier in the fact that it is a staffing company.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 21',
            figure=fig21
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "The ratio of remote vs non remote jobs were split about 50-50 down the middle.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 14',
            figure=fig14
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Overall across our data we found that Data Scientist has the most postings",
            style=page_style
        ),
        dcc.Graph(
            id='figure 13',
            figure=fig13
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Using a pie chart to find the Job Types by search parameter in Michigan show that Data Analyst has the most positions available followed by Data Scientist and Data Engineer, which is contrast to the overall postings which has data scientist having the most. with Data Analyst and Data Engineer relative close to each other behind.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 11',
            figure=fig11
        ),
    ]),
    dcc.Tab(
        label='Salary',
        style={'color': '#222222','backgroundColor': '#999999'}, children=[
        html.Div([
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "This graph shows the expected salaries for data science positions, allowing easy comparison of data scientist, data engineer, and data analyst salaries. It also helps identify salary ranges, outliers, and distribution of data to make informed career decisions. Overall, it is a useful tool for exploring the data science field or negotiating salaries.",
            style=page_style
        ),
        html.Br(
        ),
        html.P(
            "Median Salary for Data Analyst: $100K, Data Engineer: $140K, Data Scientist: $140K",
            style=page_style
        ),
        dcc.Graph(
            id='figure 7',
            figure=fig7
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Data Analyst scatters around the low end range of salary, Data Engineer middle range of salary, and Data Scientist high end range of salary",
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
            id='fig-6-slider'),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Highest Frequency of Min Salary Range for Data Analyst: $60K-$80K, Data Engineer: $120K-$140K, Data Scientist: $80-$90K",
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
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "Highest Frequency of Max Salary Range for Data Analyst: $100K-$150K, Data Engineer: $100K-$150K, Data Scientist: $100K-$150K",
            style=page_style
        ),
        dcc.RadioItems(
            options=['Data Analyst', 'Data Engineer', 'Data Scientist'],
            value='Data Analyst',
            inline=True,
            style={'color': '#222222','backgroundColor': '#999999'},
            id='fig-22-radio'
        ),
        dcc.Graph(
            id='figure 22',
            figure=fig22
        ),
        html.H2(
            children="Assumptions & Conclusions",
            style=page_style
        ),
        html.P(
            "The purpose of this graph is to visualize the relationship between years of experience and yearly maximum salary for various job titles. The scatter plot allows for easy comparison of salary and experience levels across different job titles, and the hover data provides additional information about each point. The code also filters out any rows with more than 25 years of experience, which may be useful for removing outliers or focusing on a specific segment of the data. Overall, this graph can provide insights into the job market and help identify trends in salary and experience levels across different job titles.",
            style=page_style
        ),
        dcc.Graph(
            id='figure 20',
            figure=fig20
        ),
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
    title="Top 10 Data Science Skills",
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

# callback function for radio fig 22
@app.callback(
    Output('figure 22', 'figure'),
    Input('fig-22-radio', 'value'))
def update_figure(selected_job_title):
    filtered_df = df[df['Search Parameter'] == selected_job_title]

    fig = px.histogram(filtered_df, x="Yearly Max", nbins=10, title="Maximum Salary Distribution")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
        )

    fig.update_layout(transition_duration=500)

    return fig

# connect to the server
if __name__ == '__main__':
    app.run_server(debug=True)
