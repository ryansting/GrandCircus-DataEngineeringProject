import pandas as pd
import plotly.express as px

# Load data from CSV file
df = pd.read_csv('Copy of Final Data For Jobs - Sheet1.csv')

# Exclude jobs with Yearly Min salary under $30,000
df = df[df['Yearly Max'] >= 30000]

# Select data scientist, engineer, and analyst positions
job_titles = ['Data Scientist', 'Data Engineer', 'Data Analyst']
df = df[df['Job Title'].isin(job_titles)]

# Group the data by state and job title to find the max salary for each state and job
state_job_max_salary = df.groupby(['State Code', 'Job Title'])['Yearly Max'].max().reset_index()

# Find the top paying job title for each state
top_jobs = state_job_max_salary.groupby(['State Code'])['Yearly Max'].transform(max) == state_job_max_salary['Yearly Max']
top_jobs_data = state_job_max_salary[top_jobs]

# Create a Choropleth map
fig = px.choropleth(top_jobs_data, locations='State Code', locationmode="USA-states", color='Job Title',
                    hover_name='State Code', hover_data=['Job Title', 'Yearly Max'],
                    scope="usa", title='Top Paying Data Science Job Title in Each State')

fig.show()
