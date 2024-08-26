import pandas as pd

# Example DataFrame
data = {
    'Col1': [0.126313, 0.134785, 0.142609]
}
df = pd.DataFrame(data)

# List of values to add to each entry in Col1
values_to_add = [0.01, 0.02, 0.03]

# Add the list of values to each entry in Col1
df['Col1'] = df['Col1'] + values_to_add

# Print the modified DataFrame
print(df)
