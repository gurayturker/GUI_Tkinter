from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd


window = Tk()
window.title('Palet Yerleştirme')
window.geometry('1920x1080')



def select_from_combobox():
    selected_palet_number = int(combo_palet_list.get().split(" ")[1])
    palet_number_cb.set("Seçilen Palet : " + str(selected_palet_number))

    selected_palet_en = df[df["Palet numarası"] == selected_palet_number]["Palet en"].values[0]
    palet_en_cb.set("Palet En : " + str(selected_palet_en))

    selected_palet_boy = df[df["Palet numarası"] == selected_palet_number]["Palet boy"].values[0]
    palet_boy_cb.set("Palet Boy : " + str(selected_palet_boy))

def draw_palet():
    sectim_palet = int(combo_palet_list.get().split(" ")[1])
    palet_sayisi = df[df["Palet numarası"] == sectim_palet]["Stok kodu"].nunique()
    cihazlar = list(df[df["Palet numarası"] == sectim_palet]["Stok kodu"].unique())
    palet_boy = df[df["Palet numarası"] == sectim_palet]["Palet boy"].values[0]
    palet_en = df[df["Palet numarası"] == sectim_palet]["Palet en"].values[0]

    # Paletleri Scale Etme
    standart_en = 350
    scaling_perc = (standart_en * 100) / palet_en
    palet_en = int(palet_en * scaling_perc / 100)
    palet_boy = int(palet_boy * scaling_perc / 100)

    w = Canvas(window, width=1200, height=860)
    w.place(x=10, y=100)

    # Palet Çizim
    palet_baslangic_array = []
    start_pos = 30
    for palet in range(palet_sayisi):
        x = start_pos * (palet + 1) + palet_en * palet
        z = x + palet_en
        w.create_rectangle(x, 10, z, palet_boy, outline="black", width=3, fill="#fb0")
        palet_baslangic_array.append(x)

    cihaz_info_dict = {}
    for cihaz in cihazlar:
        cihaz_boy = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz)].drop_duplicates()[
            "cihaz boy"].values[0]
        cihaz_boy = int(cihaz_boy * scaling_perc / 100)
        cihaz_en = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz)].drop_duplicates()[
            "cihaz en"].values[0]
        cihaz_en = int(cihaz_en * scaling_perc / 100)
        cihaz_adet = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz)]["toplam adet"].sum()

        if cihaz_boy > palet_boy:
            boy_sigan = 1
            en_sigan = palet_en // cihaz_en
        if cihaz_en > palet_en:
            en_sigan = 1
            boy_sigan = palet_boy // cihaz_boy
        else:
            boy_sigan = palet_boy // cihaz_boy
            en_sigan = palet_en // cihaz_en
        kat = cihaz_adet // (boy_sigan * en_sigan)
        cihaz_info_dict[cihaz] = [cihaz_boy, cihaz_en, cihaz_adet, en_sigan, boy_sigan, kat]
    print(cihaz_info_dict)

    string_palet = "{} Numaralı Palet İçin\n\n".format(2)
    for i in cihaz_info_dict.keys():
        string_urun_bilgi = "Stok Kodu : {}\nKat Sayısı : {}\nKat Başı : {}\nToplam Adet: {}\nolacak şekilde yerleştirilmiştir.\n\n".format(
            i, cihaz_info_dict[i][5], cihaz_info_dict[i][3] * cihaz_info_dict[i][4], cihaz_info_dict[i][2])
        string_palet = string_palet + string_urun_bilgi
    label_cihaz_info_string.set(string_palet)
    colors = ["green", "blue", "#f50", "#05f", "#fb0", "red"]
    for item in range(len(cihazlar)):
        item_boy = cihaz_info_dict[cihazlar[item]][0]
        item_en = cihaz_info_dict[cihazlar[item]][1]
        item_sayisi = cihaz_info_dict[cihazlar[item]][4]
        item_sayisi_yatay = cihaz_info_dict[cihazlar[item]][3]
        start_pos_x = palet_baslangic_array[item]
        start_pos_y = 10
        item_color = colors[item]
        item_name = str(cihazlar[item])
        for k in range(item_sayisi_yatay):
            for i in range(item_sayisi):
                x = start_pos_y + (item_boy * i)
                z = x + item_boy
                w.create_rectangle(start_pos_x, x, start_pos_x + item_en, z, outline="black", width=3,
                                   fill=item_color)
                w.create_text((start_pos_x + 150, x + 70), text=" Ürün Kodu : {}".format(item_name),
                              font=("Times New Roman", 15, "bold"))
            start_pos_x = start_pos_x + item_en


    cihaz_info = ""
    for cihaz in df[df["Palet numarası"] == sectim_palet]["Stok kodu"].unique():
        cihaz_kodu = cihaz
        cihaz_adedi = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz_kodu)]["toplam adet"].sum()
        cihaz_boy = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz_kodu)].drop_duplicates()["cihaz boy"].values[0]
        cihaz_en = df[(df["Palet numarası"] == sectim_palet) & (df["Stok kodu"] == cihaz_kodu)].drop_duplicates()["cihaz en"].values[0]
        cihaz_info = cihaz_info + "Yerleştirilecek Cihaz {}  \nCihaz Adedi  {}  - Cihaz Boy {} - Cihaz En {}".format(
            cihaz_kodu, cihaz_adedi, cihaz_boy, cihaz_en) + "\n\n"
    cihaz_info_var.set(cihaz_info)
    messagebox.showinfo("Palet No : " + str(sectim_palet), str(sectim_palet) + " Numaralı Palete Ürünler Başarıyla Yerleştirildi.\n"+
                        "Arayüze sığdırmak için palet ve ürün boyutları görseller üzerinde %"+str(scaling_perc)+" ölçeklendirilmiş halde bulunmaktadır.")


# Veri Setinin Okunması
df = pd.read_excel("veri_palet.xlsx")
df.columns = [col.strip() for col in df.columns]
palet_numaralari = ["Palet " + str(number) for number in list(df["Palet numarası"].unique())]


# Palet Seçiniz Label
label_palet = ttk.Label(window, text="Palet Seçiniz: ",font=("Times New Roman", 15)).place(x=10, y=10)
# Selected Palet Label
palet_number_cb = StringVar()
label_selected_palet = ttk.Label(window, textvariable=palet_number_cb, font=("Times New Roman", 15))
label_selected_palet.place(x=10, y=50)
# Palet Boy Label
palet_boy_cb = StringVar()
label_selected_palet_boy = ttk.Label(window, textvariable=palet_boy_cb, font=("Times New Roman", 15))
label_selected_palet_boy.place(x=200, y=50)
# Palet En Label
palet_en_cb = StringVar()
label_selected_palet_en = ttk.Label(window, textvariable=palet_en_cb, font=("Times New Roman", 15))
label_selected_palet_en.place(x=400, y=50)
# Cihaz Info Label
cihaz_info_var = StringVar()
label_cihaz_info = ttk.Label(window, textvariable=cihaz_info_var, font=("Times New Roman", 15))
label_cihaz_info.place(x=1300, y=100)
# Palet Info Label
label_cihaz_info_string = StringVar()
label_cihaz_info = ttk.Label(window, textvariable=label_cihaz_info_string, font=("Times New Roman", 15))
label_cihaz_info.place(x=1300, y=500)
# Urun Bilgilerini Getir Button
button_urun_bilgi_getir = ttk.Button(window, text ="Ürünler Bilgilerini Getir", width=50, command=select_from_combobox)
button_urun_bilgi_getir.place(x=1175, y=10)
# Ürünleri Yerlestir Button
button_urun_yerlestir = ttk.Button(window, text ="Ürünleri Yerleştir", width=50,command=draw_palet)
button_urun_yerlestir.place(x=1500, y=10)
# Combobox Yaratma
var = StringVar()
combo_palet_list = ttk.Combobox(window, width=100, height=50, textvariable=var, font=("Times New Roman", 15))
combo_palet_list['values'] = palet_numaralari
combo_palet_list.place(x=130, y=10)
combo_palet_list.current(0)

window.mainloop()