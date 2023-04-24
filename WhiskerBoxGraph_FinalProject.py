import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('Combined_Version_2.csv')

# Clean salary data by removing extra $ symbols
df['Yearly Min'] = df['Yearly Min'].apply(lambda x: float(str(x).replace('$', '').replace(',', '')) if isinstance(x, str) else x)
df['Yearly Max'] = df['Yearly Max'].apply(lambda x: float(str(x).replace('$', '').replace(',', '')) if isinstance(x, str) else x)

# Exclude jobs with Yearly Min salary under $30,000
df = df[df['Yearly Max'] >= 30000]

# Create a boxplot of yearly salaries
fig, ax = plt.subplots(figsize=(10, 6))
bp = ax.boxplot([df['Yearly Min'], df['Yearly Max']], vert=False, showfliers=False,
                labels=['Yearly Min', 'Yearly Max'], boxprops=dict(color='purple'),
                whiskerprops=dict(linestyle='--'))

# Add a title and axis labels
ax.set_title('Yearly Salaries', fontsize=18)
ax.set_xlabel('Salary', fontsize=14)
ax.set_ylabel('Yearly Min/Max', fontsize=14)

# Add grid lines
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

# Adjust the font size of the tick labels
ax.tick_params(axis='both', which='major', labelsize=12)

# Calculate and print common salary findings
avg_min = df['Yearly Min'].mean()
avg_max = df['Yearly Max'].mean()
median_min = df['Yearly Min'].median()
median_max = df['Yearly Max'].median()
max_min = df['Yearly Min'].max()
max_max = df['Yearly Max'].max()
min_min = df['Yearly Min'].min()
min_max = df['Yearly Max'].min()
avg_salary = df[['Yearly Min', 'Yearly Max']].mean().mean()

# Get the job title with the highest and lowest Yearly Min and Max salaries
highest_min = df.loc[df['Yearly Min'].idxmax()]
lowest_min = df.loc[df['Yearly Min'].idxmin()]
highest_max = df.loc[df['Yearly Max'].idxmax()]
lowest_max = df.loc[df['Yearly Max'].idxmin()]

# Show the plot
plt.show()


print(f"Average Yearly Min Salary: ${avg_min:,.2f}")
print(f"Average Yearly Max Salary: ${avg_max:,.2f}\n")
print(f"Average Yearly Salary: ${avg_salary:,.2f}\n")
print(f"Median Yearly Min Salary: ${median_min:,.2f}")
print(f"Median Yearly Max Salary: ${median_max:,.2f}\n")
print(f"Maximum Yearly Min Salary: ${max_min:,.2f} ({highest_min['Job Title']})")
print(f"Maximum Yearly Max Salary: ${max_max:,.2f} ({highest_max['Job Title']})")
print(f"Minimum Yearly Min Salary: ${min_min:,.2f} ({lowest_min['Job Title']})")
print(f"Minimum Yearly Max Salary: ${min_max:,.2f} ({lowest_max['Job Title']})\n")
print(f"Number of job postings: {len(df)}")
