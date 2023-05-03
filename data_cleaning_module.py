#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# import the datasets from web scraper
df1 = pd.read_csv('IndeedDataAnalyst_2023.csv')
df2 = pd.read_csv('IndeedDataEngineer_2023.csv')
df3 = pd.read_csv('IndeedDataScientist_2023.csv')
df4 = pd.read_csv('simplyhiredjobs.csv')
df5 = pd.read_csv('dice_data_with_skills.csv')
df_new = pd.read_csv('FinalJobDataUpdated.csv')


# In[3]:


# Indeed datasets
df1.insert(0, 'job_query', 'Data Analyst')
df2.insert(0, 'job_query', 'Data Engineer')
df3.insert(0, 'job_query', 'Data Scientist')


# In[4]:


# combine datasets together
df = pd.concat([df1, df2, df3])


# In[5]:


# format column headers
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()
df = df.drop(columns='unnamed:_0')


# In[6]:


#df.head()


# In[7]:


# insert new column
df.insert(0, 'job_website_source', 'Indeed')


# In[8]:


df.head()


# In[9]:


# Drop rows where 'Salary' is less than 40,000
df = df[df['salary'].str.replace(',', '').str.extract(r'(\d+)', expand=False).fillna('0').astype(int) >= 40000]

# Split 'Salary' column into 'Yearly Min' and 'Yearly Max' columns
df[['Yearly Min', 'Yearly Max']] = df['salary'].str.replace(',', '').str.extract(r'(\d+)\D*(\d+)?', expand=True).astype(float).fillna(0)

# Set 'Yearly Max' to 'Yearly Min' if it is 0
df['Yearly Max'] = df.apply(lambda row: row['Yearly Min'] if row['Yearly Max'] == 0 else row['Yearly Max'], axis=1)

# Remove the 'Salary' column
df = df.drop('salary', axis=1)

# Format 'Yearly Min' and 'Yearly Max' columns as strings with two decimal places
df[['Yearly Min', 'Yearly Max']] = df[['Yearly Min', 'Yearly Max']].applymap('{:.2f}'.format)


# In[10]:


# Add a 'Skills' column if one doesn't exist
if 'Skills' not in df.columns:
    df['Skills'] = ''

# Define the list of keywords
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing', 'Data Pipelines', 
            'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker', 'Kubernetes', 'Redshift', 
            'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization', 'Data Analysis', 'Dashboards', 
            'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics', 'Power BI', 'Data Cleansing', 
            'Data Interpretation', 'Google Analytics', 'Data Modelling', 'Predictive Analytics', 'R$', 'Data Mapping', 
            'Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Predictive Modeling', 
            'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

# Loop over the rows in the DataFrame and update the 'Skills' column
for index, row in df.iterrows():
    job_description = row['job_description']
    skills = []
    for keyword in keywords:
        if keyword.lower() in job_description.lower():
            if keyword.lower() == 'r$':
                if 'ruby' in job_description.lower():
                    continue
            skills.append(keyword)
    row['Skills'] = ', '.join(skills)


# In[11]:


df.head()


# In[12]:


# regex pattern to parse city and state from location column
city_pattern = r'([A-Za-z]+(?: [A-Za-z]+)*)'
state_pattern = r'([A-Z]{2})'


# In[13]:


# create new columns for city and state
df['city'] = df['location'].str.extract(city_pattern, expand=False)
df['state'] = df['location'].str.extract(state_pattern, expand=False)


# In[14]:


df.head(10)


# In[15]:


# regex pattern for searching hybrid and remote work in location column
hybrid_pattern = r'\bhybrid\b'  # Matches the word "hybrid" surrounded by word boundaries
remote_pattern = r'\bremote\b'  # Matches the word "remote" surrounded by word boundaries


# In[16]:


# create new columns with Boolean values
df['hybrid'] = df['location'].str.contains(hybrid_pattern, case=False)
df['remote'] = df['location'].str.contains(remote_pattern, case=False)


# In[17]:


df.head(10)


# In[18]:


# rename columns for final dataset
df = df.rename(columns={"job_website_source": "Job Website",
                   "job_query": "Search Parameter",
                   "job_title": "Job Title",
                   "company": "Company",
                  "location": "Location",
                  "job_description": "Job Description",
                  "city": "City",
                   "state": "State Code",
                   "hybrid": "Hybrid",
                   "remote": "Remote",
                  })


# In[19]:


df.head()


# In[20]:


df.dtypes


# In[21]:


# convert salary columns from string to float
df['Yearly Min'] = df['Yearly Min'].astype(float)
df['Yearly Max'] = df['Yearly Max'].astype(float)


# In[22]:


#df.head()


# In[23]:


df.dtypes


# In[24]:


# start of df4 SimplyHired data cleaning


# In[25]:


df4.insert(0, 'job_query', 'Data Engineer')
df4.insert(0, 'job_website_source', 'SimplyHired')


# In[26]:


# Convert the salary column to numeric values, replace non-numeric values with NaN
df4['sal_min'] = pd.to_numeric(df4['sal_min'], errors='coerce')

# Remove any rows where salary is NaN
df4 = df4.dropna(subset=['sal_min'])


# In[27]:


# Convert the salary column to numeric values, replace non-numeric values with NaN
df4['sal_max'] = pd.to_numeric(df4['sal_max'], errors='coerce')

# Remove any rows where salary is NaN
df4 = df4.dropna(subset=['sal_max'])


# In[28]:


# convert hourly rates to yearly salary

def hourly_to_yearly(hourly_rate):
    return hourly_rate * 40 * 52  # 40 hours per week, 52 weeks per year

# Create a new 'yearly_salary' column based on the values in 'salary_type' and 'salary'
df4['Yearly Min'] = df4.apply(lambda x: x['sal_min'] if x['salary_type'] == 'yearly' else hourly_to_yearly(x['sal_min']), axis=1)
df4['Yearly Max'] = df4.apply(lambda x: x['sal_max'] if x['salary_type'] == 'yearly' else hourly_to_yearly(x['sal_max']), axis=1)


# In[29]:


df4 = df4.drop('index', axis=1)


# In[30]:


# regex pattern to search for hybrid and remote work
hybrid_pattern = r'\bhybrid\b'  # Matches the word "hybrid" surrounded by word boundaries
remote_pattern = r'\bremote\b'  # Matches the word "remote" surrounded by word boundaries


# In[31]:


df4['hybrid'] = df4['type'].str.contains(hybrid_pattern, case=False)
df4['remote'] = df4['type'].str.contains(remote_pattern, case=False)


# In[32]:


df4 = df4.rename(columns={"job_website_source": "Job Website",
                   "job_query": "Search Parameter",
                   "title": "Job Title",
                   "company": "Company",
                  "location": "Location",
                    "skills": "Skills",
                  "job_description": "Job Description",
                  "city": "City",
                   "state": "State Code",
                   "hybrid": "Hybrid",
                   "remote": "Remote",
                  })


# In[33]:


df4 = df4.drop(['type', 'salary', 'salary_type', 'sal_min', 'sal_max', 'sal_median', 'posted_date', 'origin'], axis=1)


# In[34]:


# combine Indeed dataset with SimplyHired
df = pd.concat([df, df4])


# In[35]:


df.info()


# In[36]:


#df.tail()


# In[37]:


# start of df5 Dice data cleaning


# In[38]:


df5.insert(0, 'job_query', 'Data Scientist')
df5.insert(0, 'job_website_source', 'dice.com')


# In[39]:


def hourly_to_yearly(hourly_rate):
    return hourly_rate * 40 * 52  # 40 hours per week, 52 weeks per year

# Create a new 'yearly_salary' column based on the values in 'salary_type' and 'salary'
df5['Yearly Min'] = df5.apply(lambda x: x['sal_min'] if x['type.1'] == 'yearly' else hourly_to_yearly(x['sal_min']), axis=1)
df5['Yearly Max'] = df5.apply(lambda x: x['sal_max'] if x['type.1'] == 'yearly' else hourly_to_yearly(x['sal_max']), axis=1)


# In[40]:


hybrid_pattern = r'\bhybrid\b'  # Matches the word "hybrid" surrounded by word boundaries
remote_pattern = r'\bremote\b'  # Matches the word "remote" surrounded by word boundaries


# In[41]:


df5['hybrid'] = df5['title'].str.contains(hybrid_pattern, case=False)
df5['remote'] = df5['title'].str.contains(remote_pattern, case=False)


# In[42]:


df5 = df5.rename(columns={"job_website_source": "Job Website",
                   "job_query": "Search Parameter",
                   "title": "Job Title",
                   "company": "Company",
                  "location": "Location",
                  "job_description": "Job Description",
                  "city": "City",
                   "state": "State Code",
                   "hybrid": "Hybrid",
                   "remote": "Remote",
                  })


# In[43]:


df5 = df5.drop(['index', 'posted_date', 'type', 'salary', 'type.1', 'sal_min', 'sal_max', 'sal_median', 'origin'], axis=1)


# In[44]:


df5 = df5.dropna(subset=['Yearly Min'])
df5 = df5.dropna(subset=['Yearly Max'])


# In[45]:


#df5


# In[46]:


# create final dataset with Indeed, SimplyHired, and Dice all together

df = pd.concat([df, df5])


# In[47]:


df.info()


# In[53]:


df.tail()


# In[48]:


df.to_csv('Final_Jobs_Dataset.csv')


# In[49]:


# Count the total number of rows in the dataframe -- Each row represents 1 job
num_rows = len(df_new)

print("Total Jobs Analyzed:", num_rows)

#Query, average salary of each search parameter "Data Analyst", "Data Engineer", "Data Scientist"


# In[50]:


df_new['Yearly Max'] = df_new['Yearly Max'].replace(0, 'Null')
# Replace 'Null' values with np.nan
df_new = df_new.replace('Null', np.nan)

# Convert the 'Yearly Max' and 'Yearly Min' columns to float
df_new['Yearly Max'] = df_new['Yearly Max'].astype(float)
df_new['Yearly Min'] = df_new['Yearly Min'].astype(float)

# Calculate the average salary
df_new['Average Salary'] = (df_new['Yearly Max'] + df_new['Yearly Min']) / 2


# In[51]:


# Group by each unique value in the 'Search Parameter' column and take the group's average of the "Average Salary" column
grouped_df = df_new.groupby(['Search Parameter'])['Average Salary'].mean()
grouped_df = grouped_df.apply(lambda x: '${:,.2f}'.format(x))

print(grouped_df)


# In[52]:


top_paying_cities = df_new.groupby(['City', 'State Code'])['Average Salary'].mean().sort_values(ascending = False)

print(top_paying_cities)


# In[ ]:




