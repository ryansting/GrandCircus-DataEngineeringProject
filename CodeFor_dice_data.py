import pandas as pd

# Read the CSV file into a Pandas dataframe
df = pd.read_csv('cleaned_dice_data_with_skills_cleaned.csv')

# Combine the state and city into a single 'location' column
df['location'] = df['city'] + ', ' + df['state']

# Drop the original 'city' and 'state' columns
df = df.drop(['city', 'state'], axis=1)

# Remove any rows with missing values
df = df.dropna()

# Write the cleaned data to a new CSV file
df.to_csv('dice_data_with_skills_cleaned.csv', index=False)