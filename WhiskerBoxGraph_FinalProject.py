import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('Combined_Version_2.csv')

# Clean salary data by removing extra $ symbols
df['Yearly Min'] = df['Yearly Min'].apply(lambda x: float(str(x).replace('$', '').replace(',', '')) if isinstance(x, str) else x)
df['Yearly Max'] = df['Yearly Max'].apply(lambda x: float(str(x).replace('$', '').replace(',', '')) if isinstance(x, str) else x)

# Exclude jobs with Yearly Min salary under $30,000
df = df[df['Yearly Max'] >= 30000]

# Select data scientist, engineer, and analyst positions
job_titles = ['Data Scientist', 'Data Engineer', 'Data Analyst']
df = df[df['Job Title'].isin(job_titles)]

# Loop through the filtered DataFrame and create a whisker-box plot for each job title
for job_title in job_titles:
    job_df = df[df['Job Title'] == job_title]
    avg_salary = '{:,.2f}'.format(job_df['Yearly Max'].mean())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot([job_df['Yearly Min'], job_df['Yearly Max']], vert=False, showfliers=False,
                    labels=['Yearly Min', 'Yearly Max'], boxprops=dict(color='purple'),
                    whiskerprops=dict(linestyle='--'))

    ax.set_title(f'Yearly Salaries for {job_title}', fontsize=18)
    ax.set_xlabel('Salary', fontsize=14)
    ax.set_ylabel('Yearly Min/Max', fontsize=14)

    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Add average salary to the graph
    ax.text(0.95, 0.95, f'Avg. Salary: ${avg_salary}', transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='black', pad=5.0))
    
    plt.show()
