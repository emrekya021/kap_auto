import requests
from lxml import html

# Linkleri dosyadan oku
with open("bildirim_links.txt", "r") as file:
    links = file.readlines()

# Her bir link için verileri çekelim
for link in links:
    link = link.strip()  # Linklerdeki boşlukları temizle

    response = requests.get(link)
    tree = html.fromstring(response.content)

    # Verileri çekelim
    hisse_ticker = tree.xpath('//*[@id="disclosureContent"]/div/div[2]/div[2]/text()')
    brut_kar_payi = tree.xpath('//*[@id="SHARE_DIVIDEND_FLEX_TABLE_2"]/tbody/tr[2]/td[3]/div/text()')
    kar_payi_net_miktar = tree.xpath('//*[@id="SHARE_DIVIDEND_FLEX_TABLE_2"]/tbody/tr[2]/td[6]/div/text()')
    teklif_edilen_kar_payi_tarihi = tree.xpath('//*[@id="SHARE_DIVIDEND_FLEX_TABLE_3"]/tbody/tr[2]/td[2]/div/text()')
    kesinlesen_kar_payi_net_tarih = tree.xpath('//*[@id="SHARE_DIVIDEND_FLEX_TABLE_3"]/tbody/tr[2]/td[3]/div/text()')
    odeme_tarihi = tree.xpath('//*[@id="SHARE_DIVIDEND_FLEX_TABLE_3"]/tbody/tr[2]/td[4]/div/text()')

    # Verileri alıp formatlayalım
    hisse_ticker_text = hisse_ticker[0].strip() if hisse_ticker else "Veri Bulunamadı"
    brut_kar_payi_text = brut_kar_payi[0].strip() if brut_kar_payi else "0"
    kar_payi_net_miktar_text = kar_payi_net_miktar[0].strip() if kar_payi_net_miktar else "0"
    teklif_edilen_kar_payi_tarihi_text = teklif_edilen_kar_payi_tarihi[0].strip() if teklif_edilen_kar_payi_tarihi else "Veri Bulunamadı"
    kesinlesen_kar_payi_net_tarih_text = kesinlesen_kar_payi_net_tarih[0].strip() if kesinlesen_kar_payi_net_tarih else None
    odeme_tarihi_text = odeme_tarihi[0].strip() if odeme_tarihi else "Veri Bulunamadı"

    # Brüt Kar Payı veya Net Kar Payı miktarı 0 ise özel mesaj oluştur
    try:
        brut_kar_payi_value = float(brut_kar_payi_text.replace(',', '.'))
        kar_payi_net_miktar_value = float(kar_payi_net_miktar_text.replace(',', '.'))

        if brut_kar_payi_value == 0 or kar_payi_net_miktar_value == 0:
            formatted_text = f"🔴 #{hisse_ticker_text} temettü dağıtmama kararı aldı."
        elif kesinlesen_kar_payi_net_tarih_text is None and teklif_edilen_kar_payi_tarihi_text != "Veri Bulunamadı":
            formatted_text = f"🟡 #{hisse_ticker_text} {teklif_edilen_kar_payi_tarihi_text} tarihinde pay başı net ₺{kar_payi_net_miktar_text} olmak üzere temettü dağıtma teklifinde bulundu.\n\nÖdeme tarihi {odeme_tarihi_text}."
        else:
            # Normal formatlanmış metin
            formatted_text = f"🟢 #{hisse_ticker_text} {kesinlesen_kar_payi_net_tarih_text} tarihinde pay başı net ₺{kar_payi_net_miktar_text} temettü dağıtacağını açıkladı.\n\nÖdeme tarihi {odeme_tarihi_text}."
    
    except ValueError:
        formatted_text = "Veriler işlenemedi."

    # Çekilen tüm verileri konsola yazdır
    print("")
    print(f"Hisse Tickerı: {hisse_ticker_text}")
    print(f"Brüt Kar Payı: {brut_kar_payi_text}")
    print(f"Kar Payı Net Miktar: {kar_payi_net_miktar_text}")
    print(f"Teklif Edilen Kar Payı Tarihi: {teklif_edilen_kar_payi_tarihi_text}")
    print(f"Kesinleşen Kar Payı Net Tarih: {kesinlesen_kar_payi_net_tarih_text if kesinlesen_kar_payi_net_tarih_text else 'Veri Bulunamadı'}")
    print(f"Ödeme Tarihi: {odeme_tarihi_text}")

    # Formatlanmış metni yazdır
    print("\n" + formatted_text)
