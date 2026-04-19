import pygame
import time
import random
import os

# Başlatma
pygame.init()
pygame.mixer.init()

# Renkler
siyah = (0, 0, 0)
kirmizi = (213, 50, 80)
sari = (255, 255, 102)
gri = (100, 100, 100)
yesil = (0, 255, 0)
mavi = (50, 153, 213)
beyaz = (255, 255, 255)
mor = (155, 48, 255)
turuncu = (255, 165, 0)

# Ekran Ayarları
genislik, yukseklik = 600, 460
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption('Yılan oyunu -kardessait')

saat = pygame.time.Clock()
yilan_bloku = 20

def ses_cal(ses_adi):
    if ses_adi == "yemek": os.system("afplay /System/Library/Sounds/Ping.aiff &")
    elif ses_adi == "powerup": os.system("afplay /System/Library/Sounds/Hero.aiff &")
    elif ses_adi == "yandi": os.system("afplay /System/Library/Sounds/Sosumi.aiff &")

skor_stili = pygame.font.SysFont("comicsansms", 20)
mesaj_stili = pygame.font.SysFont("arial", 25)

def yuksek_skor_al():
    if not os.path.exists("rekor.txt"): return 0
    with open("rekor.txt", "r") as f:
        try: return int(f.read())
        except: return 0

def arayuz_ciz(skor, rekor, hiz, enerji, miknatis_vakti, hayalet_vakti, dash_aktif):
    pygame.draw.rect(ekran, (30, 30, 30), [0, 0, genislik, 60])
    simdi = time.time()
    status = f"Skor: {skor}  Rekor: {rekor}  Hız: {hiz}"
    color = beyaz
    if simdi - hayalet_vakti < 5: status = "!!! HAYALET MODU !!!"; color = mor
    elif simdi - miknatis_vakti < 5: status = "!!! MIKNATIS AKTİF !!!"; color = sari
    skor_yazisi = skor_stili.render(status, True, color)
    ekran.blit(skor_yazisi, [10, 15])
    pygame.draw.rect(ekran, gri, [genislik - 160, 20, 150, 20], 2)
    bar_rengi = turuncu if dash_aktif else (yesil if enerji > 50 else kirmizi)
    pygame.draw.rect(ekran, bar_rengi, [genislik - 158, 22, (enerji * 146 / 100), 16])

# --- PATLAMA EFEKTİ DÜZELTİLDİ ---
def patlama_animasyonu(yilan_listesi):
    ses_cal("yandi")
    for _ in range(15): # 15 karelik bir patlama
        for parca in yilan_listesi:
            # Her parçanın etrafına rastgele küçük kırmızı noktalar saç
            for _ in range(3):
                px = parca[0] + random.randint(-10, 20)
                py = parca[1] + random.randint(-10, 20)
                pygame.draw.circle(ekran, kirmizi, (px, py), random.randint(2, 6))
        pygame.display.update()
        time.sleep(0.05)

def yilan_ciz(yilan_listesi, hayalet_aktif):
    for i, x in enumerate(yilan_listesi):
        if hayalet_aktif:
            pygame.draw.rect(ekran, mor, [x[0], x[1], yilan_bloku, yilan_bloku], 2)
        else:
            ton = max(50, 255 - (len(yilan_listesi) - i) * 10)
            pygame.draw.rect(ekran, (0, ton, 0), [x[0], x[1], yilan_bloku, yilan_bloku])
        
        # Gözler her zaman en üstte
        if i == len(yilan_listesi) - 1:
            pygame.draw.circle(ekran, beyaz, (int(x[0] + 6), int(x[1] + 6)), 4)
            pygame.draw.circle(ekran, beyaz, (int(x[0] + 14), int(x[1] + 6)), 4)
            pygame.draw.circle(ekran, siyah, (int(x[0] + 6), int(x[1] + 6)), 2)
            pygame.draw.circle(ekran, siyah, (int(x[0] + 14), int(x[1] + 6)), 2)

def oyun_dongusu():
    oyun_bitti = False; oyun_kapandi = False
    x1, y1 = 300, 240; x1_d, y1_d = 0, 0
    yilan_listesi = []; yilan_uzunlugu = 1; mevcut_hiz = 5 
    rekor = yuksek_skor_al(); enerji = 100.0; miknatis_v = 0; hayalet_v = 0

    def rastgele_konum():
        return [random.randrange(0, genislik - yilan_bloku, yilan_bloku),
                random.randrange(60, yukseklik - yilan_bloku, yilan_bloku)]

    yemek = rastgele_konum(); engeller = [rastgele_konum() for _ in range(3)]
    miknatis_item = [-100, -100]; hayalet_item = [-100, -100]

    while not oyun_bitti:
        while oyun_kapandi:
            ekran.fill(siyah)
            msg = mesaj_stili.render(f"Skor: {yilan_uzunlugu-1} C:Tekrar Q:Çıkış", True, kirmizi)
            ekran.blit(msg, [genislik/4, yukseklik/2])
            if yilan_uzunlugu-1 > rekor:
                with open("rekor.txt", "w") as f: f.write(str(yilan_uzunlugu-1))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: oyun_bitti = True; oyun_kapandi = False
                    if event.key == pygame.K_c: oyun_dongusu()

        keys = pygame.key.get_pressed()
        dash = keys[pygame.K_SPACE] and enerji > 5
        for event in pygame.event.get():
            if event.type == pygame.QUIT: oyun_bitti = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_d == 0: x1_d = -yilan_bloku; y1_d = 0
                elif event.key == pygame.K_RIGHT and x1_d == 0: x1_d = yilan_bloku; y1_d = 0
                elif event.key == pygame.K_UP and y1_d == 0: y1_d = -yilan_bloku; x1_d = 0
                elif event.key == pygame.K_DOWN and y1_d == 0: y1_d = yilan_bloku; x1_d = 0

        simdi = time.time()
        hayalet_aktif = simdi - hayalet_v < 5
        if simdi - miknatis_v < 5 and abs(x1 - yemek[0]) < 100 and abs(y1 - yemek[1]) < 100: yemek = [x1, y1]

        if x1_d != 0 or y1_d != 0: enerji -= 0.4 if dash else 0.15
        if enerji <= 0:
            patlama_animasyonu(yilan_listesi) # BURADA ÇAĞIRILIYOR
            oyun_kapandi = True

        x1 += x1_d; y1 += y1_d
        if x1 >= genislik: x1 = 0
        elif x1 < 0: x1 = genislik - yilan_bloku
        if y1 >= yukseklik: y1 = 60
        elif y1 < 60: y1 = yukseklik - yilan_bloku

        ekran.fill(siyah)
        if random.randint(1, 100) == 1 and hayalet_item[0] == -100: hayalet_item = rastgele_konum()
        if random.randint(1, 100) == 1 and miknatis_item[0] == -100: miknatis_item = rastgele_konum()
        
        pygame.draw.rect(ekran, kirmizi, [yemek[0], yemek[1], yilan_bloku, yilan_bloku])
        if hayalet_item[0] != -100: pygame.draw.rect(ekran, mor, [hayalet_item[0], hayalet_item[1], yilan_bloku, yilan_bloku])
        if miknatis_item[0] != -100: pygame.draw.rect(ekran, mavi, [miknatis_item[0], miknatis_item[1], yilan_bloku, yilan_bloku])
        for en in engeller: pygame.draw.rect(ekran, gri, [en[0], en[1], yilan_bloku, yilan_bloku])

        yilan_basi = [x1, y1]
        if not hayalet_aktif and (yilan_basi in engeller or yilan_basi in yilan_listesi[:-1]):
            patlama_animasyonu(yilan_listesi) # BURADA DA ÇAĞIRILIYOR
            oyun_kapandi = True

        yilan_listesi.append(yilan_basi)
        if len(yilan_listesi) > yilan_uzunlugu: del yilan_listesi[0]

        if x1 == yemek[0] and y1 == yemek[1]:
            ses_cal("yemek"); enerji = min(100, enerji + 18); yilan_uzunlugu += 1; yemek = rastgele_konum()
            if (yilan_uzunlugu - 1) % 5 == 0: mevcut_hiz += 1; engeller.append(rastgele_konum())

        if x1 == hayalet_item[0] and y1 == hayalet_item[1]:
            ses_cal("powerup"); hayalet_v = simdi; hayalet_item = [-100, -100]
        if x1 == miknatis_item[0] and y1 == miknatis_item[1]:
            ses_cal("powerup"); miknatis_v = simdi; miknatis_item = [-100, -100]

        yilan_ciz(yilan_listesi, hayalet_aktif)
        arayuz_ciz(yilan_uzunlugu - 1, rekor, mevcut_hiz, enerji, miknatis_v, hayalet_v, dash)
        pygame.display.update()
        saat.tick(mevcut_hiz * 2 if dash else mevcut_hiz)

    pygame.quit(); quit()

oyun_dongusu()