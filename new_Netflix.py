import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sb 

# Load dataset
df = pd.read_csv(__Path__, lineterminator='\n')

# Convert 'releaseYear' to numeric (some may fail, so use 'coerce')
df['releaseYear'] = pd.to_numeric(df['releaseYear'], errors='coerce')

# Drop unwanted columns
df.drop(['availableCountries', 'imdbId'], axis=1, inplace=True)

# Function to categorize a column into quartiles
def categorize_column(df, col, labels):
    desc = df[col].describe()
    edges = [desc['min'], desc['25%'], desc['50%'], desc['75%'], desc['max']]
    df[col] = pd.cut(df[col], bins=edges, labels=labels, duplicates='drop')
    return df

# Categorize 'imdbAverageRating' column
labels = ['Not Popular', 'Below Avg', 'Average', 'Popular']
df = categorize_column(df, 'imdbAverageRating', labels)

# Remove missing values
df.dropna(inplace=True)

# Split genres into separate rows
df['genres'] = df['genres'].str.split(', ')
df = df.explode('genres').reset_index(drop=True)

# Convert genres to category
df['genres'] = df['genres'].astype('category')

# ---------------------- Data Visualization ----------------------

# Most frequent genres on Netflix
sb.catplot(
    y='genres',
    data=df,
    kind='count',
    order=df['genres'].value_counts().index,
    color="#E50914"
)
plt.title('Genres Distribution on Netflix')
plt.show()

# Distribution of IMDb average ratings
sb.catplot(
    y='imdbAverageRating',
    data=df,
    kind='count',
    order=df['imdbAverageRating'].value_counts().index,
    color="#E50914"
)
plt.title('IMDb Average Ratings Distribution')
plt.show()

# Most popular movie (highest IMDb votes)
most_popular = df[df['imdbNumVotes'] == df['imdbNumVotes'].max()]
print("Most popular movie:")
print(most_popular)

# Least popular movie (lowest IMDb votes)
least_popular = df[df['imdbNumVotes'] == df['imdbNumVotes'].min()]
print("Least popular movie:")
print(least_popular)

# Distribution of release years
df['releaseYear'].hist()
plt.title('Release Year Distribution')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()

