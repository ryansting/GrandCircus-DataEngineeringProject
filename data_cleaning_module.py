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


# insert new column
df.insert(0, 'job_website_source', 'Indeed')


# In[7]:


df.head()


# In[8]:


# drop records where salary is less than 40,000
df = df[df['salary'].str.replace(',', '').str.extract(r'(\d+)', expand=False).fillna('0').astype(int) >= 40000]

# split salary column into separate yearly min and max columns
df[['Yearly Min', 'Yearly Max']] = df['salary'].str.replace(',', '').str.extract(r'(\d+)\D*(\d+)?', expand=True).astype(float).fillna(0)

# set yearly max to yearly min if value is 0
df['Yearly Max'] = df.apply(lambda row: row['Yearly Min'] if row['Yearly Max'] == 0 else row['Yearly Max'], axis=1)

# remove the salary column
df = df.drop('salary', axis=1)

# format yearly min and yearly max columns as strings with two decimal places
df[['Yearly Min', 'Yearly Max']] = df[['Yearly Min', 'Yearly Max']].applymap('{:.2f}'.format)


# In[9]:


df.dtypes


# In[10]:


# add skills column by searching matching list of keywords for each record
if 'Skills' not in df.columns:
    df['Skills'] = ''

# define the list of keywords
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing', 'Data Pipelines', 
            'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker', 'Kubernetes', 'Redshift', 
            'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization', 'Data Analysis', 'Dashboards', 
            'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics', 'Power BI', 'Data Cleansing', 
            'Data Interpretation', 'Google Analytics', 'Data Modelling', 'Predictive Analytics', 'R$', 'Data Mapping', 
            'Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Predictive Modeling', 
            'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

# loop over the records in the dataframe and update the skills column
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
hybrid_pattern = r'\bhybrid\b'  
remote_pattern = r'\bremote\b'


# In[16]:


# create new hybrid/remote columns with Boolean values
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


# convert salary columns from string to float
df['Yearly Min'] = df['Yearly Min'].astype(float)
df['Yearly Max'] = df['Yearly Max'].astype(float)


# In[21]:


# check datatypes particulary for salary to be numeric for calculations
df.dtypes


# In[22]:


# start of SimplyHired data cleaning


# In[23]:


df4.insert(0, 'job_query', 'Data Engineer')
df4.insert(0, 'job_website_source', 'SimplyHired')


# In[24]:


# convert the min salary column to numeric values, replace non-numeric values with NaN
df4['sal_min'] = pd.to_numeric(df4['sal_min'], errors='coerce')

# remove any records where salary is NaN
df4 = df4.dropna(subset=['sal_min'])


# In[25]:


# convert the max salary column to numeric values, replace non-numeric values with NaN
df4['sal_max'] = pd.to_numeric(df4['sal_max'], errors='coerce')

# remove any records where salary is NaN
df4 = df4.dropna(subset=['sal_max'])


# In[26]:


# convert hourly rates to yearly salary

def hourly_to_yearly(hourly_rate):
    return hourly_rate * 40 * 52  # 40 hours per week, 52 weeks per year

# create a new yearly min/max salary columns to standardize hourly and yearly pay rates
df4['Yearly Min'] = df4.apply(lambda x: x['sal_min'] if x['salary_type'] == 'yearly' else hourly_to_yearly(x['sal_min']), axis=1)
df4['Yearly Max'] = df4.apply(lambda x: x['sal_max'] if x['salary_type'] == 'yearly' else hourly_to_yearly(x['sal_max']), axis=1)


# In[27]:


df4 = df4.drop('index', axis=1)


# In[28]:


# regex pattern to search for hybrid and remote work
hybrid_pattern = r'\bhybrid\b'
remote_pattern = r'\bremote\b'


# In[29]:


# create new hybrid/remote columns with Boolean values
df4['hybrid'] = df4['type'].str.contains(hybrid_pattern, case=False)
df4['remote'] = df4['type'].str.contains(remote_pattern, case=False)


# In[30]:


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


# In[31]:


# drop columns not needed for final dataset
df4 = df4.drop(['type', 'salary', 'salary_type', 'sal_min', 'sal_max', 'sal_median', 'posted_date', 'origin'], axis=1)


# In[32]:


# combine Indeed dataset with SimplyHired
df = pd.concat([df, df4])


# In[33]:


df.info()


# In[34]:


df.tail()


# In[35]:


# start of Dice data cleaning


# In[36]:


# insert new columns to categorize job website and job title searched
df5.insert(0, 'job_query', 'Data Scientist')
df5.insert(0, 'job_website_source', 'dice.com')


# In[37]:


# convert hourly rates to yearly salary

def hourly_to_yearly(hourly_rate):
    return hourly_rate * 40 * 52  # 40 hours per week, 52 weeks per year

# create a new yearly min/max salary columns to standardize hourly and yearly pay rates
df5['Yearly Min'] = df5.apply(lambda x: x['sal_min'] if x['type.1'] == 'yearly' else hourly_to_yearly(x['sal_min']), axis=1)
df5['Yearly Max'] = df5.apply(lambda x: x['sal_max'] if x['type.1'] == 'yearly' else hourly_to_yearly(x['sal_max']), axis=1)


# In[38]:


# regex pattern to search for hybrid and remote work
hybrid_pattern = r'\bhybrid\b'
remote_pattern = r'\bremote\b'


# In[39]:


# create new hybrid/remote columns with Boolean values
df5['hybrid'] = df5['title'].str.contains(hybrid_pattern, case=False)
df5['remote'] = df5['title'].str.contains(remote_pattern, case=False)


# In[40]:


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


# In[41]:


# drop extra columns not needed for final dataset
df5 = df5.drop(['index', 'posted_date', 'type', 'salary', 'type.1', 'sal_min', 'sal_max', 'sal_median', 'origin'], axis=1)


# In[42]:


# drop records where salary values are NaN
df5 = df5.dropna(subset=['Yearly Min'])
df5 = df5.dropna(subset=['Yearly Max'])


# In[43]:


# add Dice dataset to final combined dataset with Indeed and SimplyHired
df = pd.concat([df, df5])


# In[44]:


df.info()


# In[45]:


df.tail()


# In[46]:


df.to_csv('Final_Jobs_Dataset.csv')


# In[47]:


# Count the total number of rows in the dataframe -- Each row represents 1 job
num_rows = len(df_new)

print("Total Jobs Analyzed:", num_rows)

# Query, average salary of each search parameter "Data Analyst", "Data Engineer", "Data Scientist"


# In[48]:


df_new['Yearly Max'] = df_new['Yearly Max'].replace(0, 'Null')
# Replace 'Null' values with np.nan
df_new = df_new.replace('Null', np.nan)

# Convert the 'Yearly Max' and 'Yearly Min' columns to float
df_new['Yearly Max'] = df_new['Yearly Max'].astype(float)
df_new['Yearly Min'] = df_new['Yearly Min'].astype(float)

# Calculate the average salary
df_new['Average Salary'] = (df_new['Yearly Max'] + df_new['Yearly Min']) / 2


# In[49]:


# Group by each unique value in the 'Search Parameter' column and take the group's average of the "Average Salary" column
grouped_df = df_new.groupby(['Search Parameter'])['Average Salary'].mean()
grouped_df = grouped_df.apply(lambda x: '${:,.2f}'.format(x))

print(grouped_df)


# In[50]:


top_paying_cities = df_new.groupby(['City', 'State Code'])['Average Salary'].mean().sort_values(ascending = False)

print(top_paying_cities)

