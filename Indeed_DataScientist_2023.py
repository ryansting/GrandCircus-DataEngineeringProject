import pandas as pd
from google.colab import files

# Upload the CSV file to the Google Colab environment
uploaded = files.upload()

# Read in the CSV file using Pandas
df = pd.read_csv('Indeedjobs.csv')

# Remove rows where Job_Title is 'N'
df = df[df.Job_Title != 'N']

# Replace cells with 'N' with blank cells
df.replace('N', '', inplace=True)

# Clean the data (e.g., remove duplicates)
df = df.drop_duplicates()

# Export the cleaned data to a new CSV file
df.to_csv('cleaned_Indeedjobs.csv', index=False)

# Download the cleaned CSV file to your local machine
files.download('cleaned_Indeedjobs.csv')
