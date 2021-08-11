import re
import os
import string
from datetime import datetime
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active


def getHakim(file_path):
    key_ketua = "sebagai Hakim Ketua"
    key_anggota = "sebagai Hakim Anggota"

    hakim_ketua = ""
    hakim_anggota = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for t in f:
            if key_ketua in t:
                hakim_ketua = t.split(key_ketua)[0].strip()

            if key_anggota in t:
                hakim_anggota.append(t.split(key_anggota)[0].strip())

    hakim_anggota = list(set(hakim_anggota))
    hakim_anggota_1 = hakim_anggota[-1]
    hakim_anggota_2 = hakim_anggota[0]

    return hakim_ketua, hakim_anggota_1, hakim_anggota_2

def getLokasiPP(tx):
    r1 = re.search("diputus di Jakarta|Pengadilan Pajak Jakarta", tx)
    if r1:
        return 1

    return 0

def getTipeKetetapan(tx):
    r1 = re.search("SKPKB|Surat Ketetapan Pajak Kurang Bayar", tx)
    if r1:
        return 1

    return 0

def getUnitPeriksa(tx):
    r2 = re.search("MEMUTUSKAN", tx)
    tx_setelah = ""
    if r2:
        start = r2.start()
        end = r2.end()
        tx_setelah = tx[end:]

    r1 = None
    if len(tx_setelah) > 0:
        r1 = re.search(re.escape("WPJ."), tx_setelah)
    else:
        r1 = re.search(re.escape("WPJ."), tx)


    if r1:
        start = r1.start()
        end = r1.end()

        put = tx[start:end+2]
        if put.endswith('07') or put.endswith('19'):
            return 1
        
        return 0

    return 0

def getPutusanPertama(tx):
    r1 = re.search("ditolak", tx, re.IGNORECASE)
    if r1:
        return 1

    return 0

def getFakturFiktif(tx):
    r1 = re.search("TBTS|tidak berdasarkan transaksi sebenarnya|faktur fiktif|Faktur Pajak fiktif|fiktif", tx)
    if r1:
        return 1

    return 0

def getKuasa(tx):
    r1 = re.search("kuasa hukum", tx, re.IGNORECASE)
    if r1:
        return 1

    return 0

def getMajelis(tx):
    r1 = re.search("demikian diputus", tx, re.IGNORECASE)
    if r1:
        start = r1.start()
        end = r1.end()

        return tx[end:end+250].split("Majelis")[1].strip().split()[0]

    return 0

def getTanggalByKeyword(tx, key):
    r2 = re.search(key, tx)
    tx_setelah = ""
    if r2:
        start = r2.start()
        end = r2.end()
        t = tx[end:end+300].split("tanggal")[1][:100].split()
        if len(t) > 0:
            tanggal = [removePunc(t[0]), removePunc(t[1].replace("November", "Nopember").replace("Pebruari", "Februari")), removePunc(t[2])]
            
            return tanggal

def getSelisihHari(start, end):
    if start is None:
        return None

    if end is None:
        return None

    bulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","Nopember","Desember"]
    
    try:
        d1 = datetime.strptime("{}-{}-{}".format(end[2],bulan.index(end[1])+1,end[0]), "%Y-%m-%d")
        d2 = datetime.strptime("{}-{}-{}".format(start[2],bulan.index(start[1])+1,start[0]), "%Y-%m-%d")
    except:
        return None

    return abs((d2 - d1).days)


def getLamaPutusan(tx):
    start = getTanggalByKeyword(tx, "MEMUTUSKAN")
    if start is None:
        return None

    end = getTanggalByKeyword(tx, "Demikian diputus")
    if end is None:
        return None

    return getSelisihHari(start, end)

# CASE SPECIFIC LEGAL FACT
def getPemusatan(tx):
    r1 = re.search("Pemusatan|Dipusatkan", tx)
    if r1:
        start = r1.start()
        end = r1.end()

        text_putusan = tx[end-100:end+100]
        negasi = ["tidak","non","belum"]
        for neg in negasi:
            if neg in text_putusan.lower():
                return 0

    return 1

def getLawanPKP(tx):
    r1 = re.search("penjual dikukuhkan sebagai Pengusaha Kena Pajak|penjual dikukuhkan sebagai PKP", tx)
    if r1:
        return 0

    return 1

def getFPLengkap(tx):
    r1 = re.search("Faktur Pajak tidak lengkap|FP tidak lengkap|Faktur Pajak tidak memenuhi ketentuan formal|FP tidak memenuhi ketentuan formal|tidak mengisi faktur pajak secara lengkap|Pasal 14", tx)
    if r1:
        return 0

    return 1

def getFPTepatWaktu(tx):
    r1 = re.search("Faktur Pajak tidak tepat waktu|FP tidak tepat waktu|terlambat menerbitkan", tx)
    if r1:
        return 0

    return 1

def getPPNDibayar(tx):
    r1 = re.search("MENGADILI", tx)
    if r1:
        start = r1.start()
        end = r1.end()

        text_putusan = tx[end:end+100]
        if "kurang bayar" in text_putusan.lower() or "tidak bayar" in text_putusan.lower():
            return 0
        else:
            return 1
    else:
        return 1

# FINAL LABEL
def getPutusan(tx):
    r1 = re.search("MENGADILI", tx)
    if r1:
        start = r1.start()
        end = r1.end()

        text_putusan = tx[end:end+100]
        if "menolak" in text_putusan.lower():
            return "Menolak"
        elif "sebagian" in text_putusan.lower():
            return "Mengabulkan Sebagian"
        else:
            return "Mengabulkan Seluruhnya"
    else:
        return "Not Found"

def removePunc(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s

dir_class = {
    "Mengabulkan Seluruhnya" : "Data Kedua/TXTs/Mengabulkan seluruhnya TXT",
    "Mengabulkan Sebagian" : "Data Kedua/TXTs/Mengabulkan Sebagian TXT",
    "Menolak" : "Data Kedua/TXTs/Menolak TXT"

}

data = ["File", "Class", "Hakim Ketua", "Hakim Anggota 1", "Hakim Anggota 2", "Lokasi PP", "Tipe Ketetetapan", "Unit Periksa", "Majelis", "Putusan Pertama", "Faktur Fiktif", "Kuasa", "Lama Putusan", "Pemusatan", "Lawan PKP", "FP Lengkap", "FP Tepat Waktu", "PPN Dibayar"]

sheet.append(data)

for class_name, data_folder in dir_class.items():
    for file_tax in os.listdir(data_folder):
        if file_tax.endswith(".txt"):
            file_path = os.path.join(data_folder, file_tax)
            with open(os.path.join(data_folder, file_tax), 'r', encoding="utf-8") as f:
                tx = f.read()

                getMajelis(tx)

                hakim_ketua, hakim_anggota_1, hakim_anggota_2 = getHakim(file_path)

                data = []
                data.append(file_tax)
                data.append(class_name)
                data.append(hakim_ketua)
                data.append(hakim_anggota_1)
                data.append(hakim_anggota_2)
                data.append(getLokasiPP(tx))
                data.append(getTipeKetetapan(tx))
                data.append(getUnitPeriksa(tx))
                data.append(getMajelis(tx))
                data.append(getPutusanPertama(tx))
                data.append(getFakturFiktif(tx))
                data.append(getKuasa(tx))
                data.append(getLamaPutusan(tx))
                data.append(getPemusatan(tx))
                data.append(getLawanPKP(tx))
                data.append(getFPLengkap(tx))
                data.append(getFPTepatWaktu(tx))
                data.append(getPPNDibayar(tx))

                sheet.append(data)

wb.save(filename='data_v2.xlsx')

