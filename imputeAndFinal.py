import pandas as pd
import math

df = pd.read_excel("data_plus_profile.xlsx")

df["Lama Putusan"].fillna(math.floor(df['Lama Putusan'].mean()), inplace = True)
rata_rata_lama_putusan = df['Lama Putusan'].mean()

lama_putusan = []
for index, row in df.iterrows():
   lama_putusan.append(0 if row["Lama Putusan"] < rata_rata_lama_putusan else 1)

df["Lama Putusan"] = lama_putusan

df["Gender Ketua"].fillna(math.ceil(df['Gender Ketua'].mean()), inplace = True)
df["Gender Anggota 1"].fillna(math.ceil(df['Gender Anggota 1'].mean()), inplace = True)
df["Gender Anggota 2"].fillna(math.ceil(df['Gender Anggota 2'].mean()), inplace = True)
df["DJP Ketua"].fillna(0, inplace = True)
df["DJP Anggota 1"].fillna(0, inplace = True)
df["DJP Anggota 2"].fillna(0, inplace = True)
df["Majelis"] = df["Majelis"].str.replace(".","")


df["Persen Gender"] = (df["Gender Ketua"] + df["Gender Anggota 1"] + df["Gender Anggota 2"]) / 3
df["Persen DJP"] = (df["DJP Ketua"] + df["DJP Anggota 1"] + df["DJP Anggota 2"]) / 3

df.to_excel("data_imputed.xlsx",index=False)

