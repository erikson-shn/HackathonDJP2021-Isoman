import pandas as pd
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    return Counter(WORD.findall(text))

def get_similarity(a, b):
    try:
        a = text_to_vector(a.strip().lower())
        b = text_to_vector(b.strip().lower())
        
        return get_cosine(a, b)
    except:
        return 0

def get_gender_djp(hakim, sim_data):
    data = dict(sorted(sim_data.items(), key=lambda item: item[1], reverse=True))
    res = list(data.keys())[0]
    if data[res] > 0.85:
        gender = 1 if hakim[res]["Gender"] == "P" else 0
        djp = hakim[res]["DJP"]

        return gender, djp

    return None, None

        

df = pd.read_excel("data latar belakang hakim v2.xlsx")

hakim = {}
for index, row in df.iterrows():
    djp = 0
    if row["DJP/ NON"] == "DJP":
        djp = 1

    hakim[row['Nama']] = {"Gender":row["Gender"], "Tahun Lahir":row["Tahun lahir"], "DJP":djp}

df2 = pd.read_excel("data_v2.xlsx")

gender_ketua_lst, djp_ketua_lst = [], []
gender_anggota_1_lst, djp_anggota_1_lst = [], []
gender_anggota_2_lst, djp_anggota_2_lst = [], []

for index, row in df2.iterrows():
    sim_ketua = {}
    sim_anggota_1 = {}
    sim_anggota_2 = {}
    for nama_hakim, vals in hakim.items():
        sim_ketua[nama_hakim] = get_similarity(nama_hakim, row["Hakim Ketua"])
        sim_anggota_1[nama_hakim] = get_similarity(nama_hakim, row["Hakim Anggota 1"])
        sim_anggota_2[nama_hakim] = get_similarity(nama_hakim, row["Hakim Anggota 2"])

    gender_ketua, djp_ketua = get_gender_djp(hakim, sim_ketua)
    gender_anggota_1, djp_anggota_1 = get_gender_djp(hakim, sim_anggota_1)
    gender_anggota_2, djp_anggota_2 = get_gender_djp(hakim, sim_anggota_2)

    gender_ketua_lst.append(gender_ketua)
    djp_ketua_lst.append(djp_ketua)

    gender_anggota_1_lst.append(gender_anggota_1)
    djp_anggota_1_lst.append(djp_anggota_1)

    gender_anggota_2_lst.append(gender_anggota_2)
    djp_anggota_2_lst.append(djp_anggota_2)

df2["Gender Ketua"] = gender_ketua_lst
df2["DJP Ketua"] = djp_ketua_lst
df2["Gender Anggota 1"] = gender_anggota_1_lst
df2["DJP Anggota 1"] = djp_anggota_1_lst
df2["Gender Anggota 2"] = gender_anggota_2_lst
df2["DJP Anggota 2"] = djp_anggota_2_lst

print(df2.head())

df2.to_excel("data_plus_profile.xlsx")



