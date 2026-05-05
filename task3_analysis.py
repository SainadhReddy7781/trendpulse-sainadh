import pandas as pd
import numpy as np
import os

# -------- 1. LOAD AND EXPLORE --------

file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# average values
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score:", int(avg_score))
print("Average comments:", int(avg_comments))


# -------- 2. NUMPY ANALYSIS --------

scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score   :", int(np.mean(scores)))
print("Median score :", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score    :", int(np.max(scores)))
print("Min score    :", int(np.min(scores)))

# category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# story with most comments
max_comments_row = df.loc[df["num_comments"].idxmax()]

print("\nMost commented story:")
print(f'"{max_comments_row["title"]}" — {max_comments_row["num_comments"]} comments')


# -------- 3. ADD NEW COLUMNS --------

# engagement = comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average score
df["is_popular"] = df["score"] > avg_score


# -------- 4. SAVE FILE --------

if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print("\nSaved to", output_file)