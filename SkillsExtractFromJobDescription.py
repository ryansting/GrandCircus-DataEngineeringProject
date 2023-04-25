import pandas as pd

# Define the keywords to search for in the 'Job Description'
keywords = ['SQL', 'Python', 'Big Data', 'AWS', 'ETL', 'Hadoop', 'Spark', 'Kafka', 'Data Warehousing',
            'Data Pipelines', 'Data Modeling', 'Java', 'Database Management', 'NoSQL', 'Airflow', 'Docker',
            'Kubernetes', 'Redshift', 'Snowflake', 'Data Integration', 'Excel', 'Tableau', 'Data Visualization',
            'Data Analysis', 'Dashboards', 'Reporting', 'Business Intelligence', 'Data Mining', 'Statistics',
            'Power BI', 'Data Cleansing', 'Data Interpretation', 'Google Analytics', 'Data Modelling',
            'Predictive Analytics', ' R ', 'Data Mapping', 'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Predictive Modeling', 'Mathematical Modeling', 'TensorFlow', 'Keras', 'Computer Vision', 'Artificial Intelligence']

# Read in the CSV file
df = pd.read_csv('Indeed_Job_Data_Combined.csv')

# Add a 'Skills' column if one doesn't exist
if 'Skills' not in df.columns:
    df['Skills'] = ''

# Iterate over the 'Job Description' column and add keywords to the 'Skills' column if they are not already present
for i, desc in enumerate(df['Job Description']):
    skills = df.loc[i, 'Skills'].split(', ') if df.loc[i, 'Skills'] != '' else []
    for keyword in keywords:
        if keyword.lower() in desc.lower() and keyword not in skills:
            skills.append(keyword)
    df.loc[i, 'Skills'] = ', '.join(skills)

# Export the updated DataFrame to a new CSV file
df.to_csv('Indeed_Job_Data_Combined_output1.csv', index=False)
