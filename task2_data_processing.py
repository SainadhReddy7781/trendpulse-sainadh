import pandas as pd
import os

# path of the json file generated in task 1
file_path = "data/trends_20260505.json"   # change date if needed

# -------- 1. load data --------
df = pd.read_json(file_path)

print("Loaded", len(df), "stories from", file_path)

# -------- 2. cleaning --------

# remove duplicate post ids
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# remove rows with missing important fields
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# convert score and num_comments to integer
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# remove low quality stories (score < 5)
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# remove extra spaces in title
df["title"] = df["title"].str.strip()

# -------- 3. save as csv --------

# create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print("\nSaved", len(df), "rows to", output_file)

# -------- summary --------
print("\nStories per category:")
print(df["category"].value_counts())