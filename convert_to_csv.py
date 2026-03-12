import pandas as pd

df = pd.read_excel("ExportMars2025.xlsx")
df.to_csv("output.csv", index=False, sep=";")