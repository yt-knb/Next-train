import pandas as pd
import numpy as np
import tkinter as tk
from time import *
from datetime import datetime
import jpholiday
import concurrent.futures

def get_h_m_s(td):
    Min, Sec = divmod(td.seconds, 60)
    Hour, Min = divmod(Min, 60)
    Hour = str(Hour)
    Min = str(Min)
    Sec = str(Sec)
    return Hour, Min, Sec

clock = tk.Tk()
clock.title('次の電車 β')

yoko = 1500 #ここを変更して大きさを変える
tate = yoko * 9 / 16
fontsize = int(tate / 18)
w = tk.Canvas(clock, width = yoko, height = tate, background = '#000000')
w.pack()

heijitu = pd.read_excel('上り時刻表.xlsx', '平日', header = None, index_col = None)
kyujitu = pd.read_excel('上り時刻表.xlsx', '休日', header = None, index_col = None)
heigo = pd.read_excel('上り時刻表.xlsx', '平日行先', header = None, index_col = None)
kyugo = pd.read_excel('上り時刻表.xlsx', '休日行先', header = None, index_col = None)
heiskp = pd.read_excel('上り時刻表.xlsx', '平日運行', header = None, index_col = None)
kyuskp = pd.read_excel('上り時刻表.xlsx', '休日運行', header = None, index_col = None)

heijitu2 = pd.read_excel('下り時刻表.xlsx', '平日', header = None, index_col = None)
kyujitu2 = pd.read_excel('下り時刻表.xlsx', '休日', header = None, index_col = None)
heigo2 = pd.read_excel('下り時刻表.xlsx', '平日行先', header = None, index_col = None)
kyugo2 = pd.read_excel('下り時刻表.xlsx', '休日行先', header = None, index_col = None)

hei_time = heijitu.values
hei_go = heigo.values
hei_skp = heiskp.values

kyu_time = kyujitu.values
kyu_go = kyugo.values
kyu_skp = kyuskp.values

hei_time2 = heijitu2.values
hei_go2 = heigo2.values

kyu_time2 = kyujitu2.values
kyu_go2 = kyugo2.values


def nobori(now):
    holiday = jpholiday.is_holiday(datetime.now().date())
    if holiday == True or now.weekday() == 5 or now.weekday() == 6:
        tr_time = kyu_time
        tr_go = kyu_go
        tr_skp = kyu_skp
    else:
        tr_time = hei_time
        tr_go = hei_go
        tr_skp = hei_skp
        
    h = int(now.hour)
    m = 0
    day = now.day
    m_max = tr_time.shape[1]
    
    while True:
        if np.isnan(tr_time[h, m]) == True:
            h = h + 1
            m = 0
        else:
            break
            
    while True:
        if h == 24:
            h = 0
            day = day + 1
            while True:
                if np.isnan(tr_time[h, m]) == True:
                    h = h + 1
                    m = 0
                else:
                    break
        tr_next = datetime(int(now.year), int(now.month), day, h, int(tr_time[h, m]))
        
        if tr_next < now:
            m = m + 1
            if m == m_max + 1:
                h = h + 1
                m = 0
            if np.isnan(tr_time[h, m]) == True:
                h = h + 1
                m = 0
        else:
            break
    
    tr_lim = tr_next - now
    lim_h, lim_m, lim_s = get_h_m_s(tr_lim)
    
    color = '#fff'
    
    if tr_skp[h, m] == '各駅停車' :
        iro = '#fff'
    else:
        iro = '#f00'
    
    w.create_text(yoko / 2, tate / 10, text = now.strftime('%Y/%m/%d %H:%M:%S'), font = ("", fontsize), tag="Y", fill = color)
    w.create_text(yoko / 8, tate * 3 / 10, text = '次の電車', font = ("", fontsize), tag="Y", fill = color)
    w.create_text(yoko * 2 / 8, tate * 4 / 10, text = tr_go[h, m], font = ("", fontsize), tag="Y", fill = color)
    w.create_text(yoko / 4, tate * 5 / 10, text = tr_next.strftime('%H : %M'), font = ("", int(fontsize*1.2)), tag="Y", fill = color)
    w.create_text(yoko * 3 / 8, tate * 3 / 10, text = tr_skp[h, m], font = ("", fontsize), tag="Y", fill = iro)
    w.create_text(yoko / 4, tate * 7 / 10, text = lim_h.zfill(2) + ' : ' + lim_m.zfill(2) + ' : ' + lim_s.zfill(2), font = ("", int(fontsize*1.3)), tag="Y", fill = color)
    


def kudari(now):
    holiday = jpholiday.is_holiday(datetime.now().date())
    if holiday == True or now.weekday() == 5 or now.weekday() == 6:
        tr_time2 = kyu_time2
        tr_go2 = kyu_go2
    else:
        tr_time2 = hei_time2
        tr_go2 = hei_go2
        
    h = int(now.hour)
    m = 0
    day = now.day
    m_max = tr_time2.shape[1]
    
    while True:
        if np.isnan(tr_time2[h, m]) == True:
            h = h + 1
            m = 0
        else:
            break
            
    while True:
        if h == 24:
            h = 0
            day = day + 1
            while True:
                if np.isnan(tr_time2[h, m]) == True:
                    h = h + 1
                    m = 0
                else:
                    break
        tr_next2 = datetime(int(now.year), int(now.month), day, h, int(tr_time2[h, m]))
        
        if tr_next2 < now:
            m = m + 1
            if m == m_max + 1:
                h = h + 1
                m = 0
            if np.isnan(tr_time2[h, m]) == True:
                h = h + 1
                m = 0
        else:
            break
    
    tr_lim2 = tr_next2 - now
    lim_h2, lim_m2, lim_s2 = get_h_m_s(tr_lim2)
    
    color = '#fff'
    

    w.create_text(yoko * 5 / 8, tate * 3 / 10, text = '次の電車', font = ("", fontsize), tag="X", fill = color)
    w.create_text(yoko * 6 / 8, tate * 4 / 10, text = tr_go2[h, m], font = ("", fontsize), tag="X", fill = color)
    w.create_text(yoko * 6 / 8, tate * 5 / 10, text = tr_next2.strftime('%H : %M'), font = ("", int(fontsize*1.2)), tag="X", fill = color)
    w.create_text(yoko * 7 / 8, tate * 3 / 10, text = '各駅停車', font = ("", fontsize), tag="Y", fill = color)
    w.create_text(yoko * 3 / 4, tate * 7 / 10, text = lim_h2.zfill(2) + ' : ' + lim_m2.zfill(2) + ' : ' + lim_s2.zfill(2), font = ("", int(fontsize*1.3)), tag="X", fill = color)
    

if __name__ == "__main__":
    while True:
        #start = time()
        
        now = datetime.now()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
            e.submit(nobori(now))
            e.submit(kudari(now))
        #nobori(now)
        #kudari(now)
        w.update()
        w.delete("Y")
        w.delete("X")
        
        #end = time()
        #print("process pool = %.3f sec" % (end-start))
        sleep(0.1)  #0.1秒毎に描画
