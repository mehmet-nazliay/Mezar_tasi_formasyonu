import sqlite3
#verileri aktarma
baglanti=sqlite3.connect("ciktilar1.db")
isaretci=baglanti.cursor()
isaretci.execute("create table if not exists results (side TEXT,date  TEXT, high6th NUMERIC, low6thlow NUMERIC, after10high NUMERIC, after10low NUMERIC, target NUMERIC, losess NUMERIC, oncelik TEXT, before5max NUMERIC,before5min NUMERIC)")
baglanti.commit()
#********************************************
con=sqlite3.connect("veriyeni.db")

db=con.cursor()

cek=db.execute("SELECT * from yen")

listetarih=[]
listeopen=[]
listehigh=[]
listelow=[]
listeclose=[]


for i in cek:
    listetarih.append(i[4])
    listeopen.append(i[0])
    listeclose.append(i[1])
    listehigh.append(i[2])
    listelow.append(i[3])
  
a=len(listetarih)
b=a-5
for i in range(0,b):
    vr=(max(listehigh[0+i:4+i])-min(listelow[0+i:4+i]))
    vr5=vr
    vr32=(vr*3)/2
    sonbarboyu=listehigh[i+5]-listelow[i+5]
    
    if (sonbarboyu>vr5):
            #Artış
        altg3=3*(listeclose[i+4]-listelow[i+5])
        ustg=listehigh[i+5]-listeclose[i+4]
        maximum=max(listehigh[0+i:4+i])
        minimumartı=(min(listelow[0+i:4+i])+vr32)
        if(altg3<ustg)  and listeclose[i+4]>listelow[i+5] and listehigh[i+5]>maximum and listeclose[i+5]>minimumartı:
            if (i+15)>b:
                continue
            
            bar10yuksek=max(listehigh[i+6:i+15])
            bar10dusuk=min(listelow[i+6:i+15])
            bartarih=listetarih[i+5]
            bar6low=listelow[i+5]
            bar6close=listeclose[i+5]
            bar6high=listehigh[i+5]
            target=bar6close-bar10dusuk
            losess=bar10yuksek-bar6close
            before5max=max(listehigh[0+i:4+i])
            before5min=min(listehigh[0+i:4+i])
            yon="Artis"
            listeoncelik1=[]
            listeoncelik2=[]            
            for j in range(6,15):
                listeoncelik1.append(listelow[i+j])
                listeoncelik2.append(listehigh[i+j])
            o1=listeoncelik1.index(min(listeoncelik1))
            o2=listeoncelik2.index(max(listeoncelik2))
            if o1>o2:
                oncelik="1.losess"
            elif o2>o1:
                oncelik="1.target"
                insert_stmt=(
    """INSERT INTO results (side, date, high6th, low6thlow, after10high, after10low, target, losess, oncelik, before5max, before5min) 
    Select ?,?,?,?,?,?,?,?,?,?,?
    WHERE NOT EXISTS (SELECT 1 FROM results WHERE side=? and date=? and high6th=? and low6thlow=? and after10high=? and after10low=? and target=? and losess=? and oncelik=? and before5max=? and before5min=?)""")    
                isaretci.execute(insert_stmt,(yon,bartarih,bar6high,bar6low,bar10yuksek,bar10dusuk,target,losess,oncelik,before5max,before5min)*2)
                baglanti.commit()                
                print(oncelik)
        
        #azalış
        altg3=3*(listehigh[i+5]-listeclose[i+4])
        ustg=listeclose[i+4]-listelow[i+5] 
        
        minimum=min(listelow[0+i:4+i])
        maximumartı=(max(listehigh[0+i:4+i])-(vr*1.5))

        if (altg3<ustg) and listeclose[i+4]<listehigh[i+5] and listelow[i+5]<minimum and listeclose[i+5]<maximumartı:
            if (i+15)>b:
                continue
            bar10yuksek=max(listehigh[i+6:i+15])
            bar10dusuk=min(listelow[i+6:i+15])
            bartarih=listetarih[i+5]
            bar6close=listeclose[i+5]
            bar6low=listelow[i+5]
            bar6high=listehigh[i+5]
            target=bar10yuksek-bar6close
            losess=bar6close -bar10dusuk 
            before5max=max(listehigh[0+i:4+i])
            before5min=min(listehigh[0+i:4+i])
            yon="Azalis"
            listeoncelik1=[]
            listeoncelik2=[]            
            for j in range(6,15):
                listeoncelik1.append(listelow[i+j])
                listeoncelik2.append(listehigh[i+j])
            o1=listeoncelik1.index(min(listeoncelik1))
            o2=listeoncelik2.index(max(listeoncelik2))
            if o2<o1:
                oncelik="1.target"
            elif o2>o1:
                oncelik="1.losess"
                insert_stmt=(
    """INSERT INTO results (side, date, high6th, low6thlow, after10high, after10low, target, losess, oncelik, before5max, before5min) 
    Select ?,?,?,?,?,?,?,?,?,?,?
    WHERE NOT EXISTS (SELECT 1 FROM results WHERE side=? and date=? and high6th=? and low6thlow=? and after10high=? and after10low=? and target=? and losess=? and oncelik=? and before5max=? and before5min=?)""")    
                isaretci.execute(insert_stmt,(yon,bartarih,bar6high,bar6low,bar10yuksek,bar10dusuk,target,losess,oncelik,before5max,before5min)*2)
                baglanti.commit()
                print(oncelik)
db.close()
baglanti.close() 
   
   
   
   
   