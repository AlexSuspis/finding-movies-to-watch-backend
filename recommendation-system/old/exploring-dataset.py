import pandas as pd
import numpy as np

movies_df = pd.read_csv('./input/big_dataset/movies_metadata.csv')

print(movies_df[['original_title','id']])
print(movies_df[['title','id']])


print(movies_df.columns)
