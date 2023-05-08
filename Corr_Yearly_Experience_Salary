import pandas as pd
import plotly.express as px
import re

# Read in the data
data = pd.read_csv('Copy of Final Data For Jobs - Sheet1.csv')

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
fig = px.scatter(salary_experience_data, x='Years of Experience', y='Yearly Max', hover_name='Job Title', hover_data=['Yearly Max'])

# Set the y-axis range to be a bit more spread out
fig.update_yaxes(range=[0, salary_experience_data['Yearly Max'].max() * 1.1])

# Show the plot
fig.show()
