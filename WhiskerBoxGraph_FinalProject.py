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

# Set color scheme
colors = ['#4C72B0', '#55A868', '#C44E52']

# Loop through the filtered DataFrame and create a whisker-box plot for each job title
fig, ax = plt.subplots(figsize=(10, 6))

for i, job_title in enumerate(job_titles):
    job_df = df[df['Job Title'] == job_title]
    avg_salary = '{:,.2f}'.format(job_df['Yearly Max'].mean())
    
    bp = ax.boxplot([job_df['Yearly Min'], job_df['Yearly Max']], vert=False, showfliers=False,
                    labels=['Yearly Min', 'Yearly Max'], boxprops=dict(color=colors[i], linewidth=2),
                    whiskerprops=dict(linestyle='--', color=colors[i], linewidth=2),
                    medianprops=dict(color='white', linewidth=2))

    # Add legend
    ax.plot([], [], color=colors[i], label=job_title, linewidth=2)
    ax.legend(loc='lower right', fontsize=12)

    # Add average salary to the graph
    ax.text(0.95, 0.95-(i*0.1), f'Avg. Salary: ${avg_salary}', transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', edgecolor=colors[i], pad=5.0))

# Set graph properties
ax.set_title('Yearly Salaries for Data Science Positions', fontsize=20)
ax.set_xlabel('Salary ($)', fontsize=16)
ax.set_ylabel('Yearly Min/Max', fontsize=16)
ax.set_xlim(left=25000)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
ax.tick_params(axis='both', which='major', labelsize=14)

# Remove unnecessary whitespace
plt.tight_layout()

plt.show()
