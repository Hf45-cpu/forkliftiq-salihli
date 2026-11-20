import json, numpy as np
from scipy.io import wavfile
VO="/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/vo"
tl=json.load(open("timeline.json"))
CH=[["DUR!","KAYDIRMA...","BU VİDEO SENİ","*DOKSANLARA* GERİ GÖTÜRECEK!"],
["KASET Mİ KOPTU?","HEMEN BİR","*KURŞUN KALEM* BULUNURDU.","VE O BANT,","SABIRLA,","TEK TEK *SARILIRDI.*"],
["TÜPLÜ TELEVİZYONDA","*KARINCALAR* ÇIKINCA...","EVDE BİRİ HEP","*ANTENİN* BAŞINDA BEKLERDİ.","TAMAM! TAMAM!","*ORADA DUR!*"],
["*TELEFON KARTI!*","KONTÖR BİTMESİN DİYE,","BÜTÜN HAYATINI","*ÜÇ DAKİKAYA* SIĞDIRIRDIN."],
["BİR BUÇUK MEGABAYTLIK","*DİSKET...*","O ZAMAN BU,","KOCA BİR *HAZİNEYDİ.*"],
["CEP OYUNCAĞINDAKİ","*SANAL BEBEK* ACIKINCA,","BÜTÜN SINIF","*ALARMA* GEÇERDİ!"],
["VE SOKAK LAMBALARI","*YANDIĞINDA...*","*HERKES EVE!*"],
["PEKİ SEN DOKSANLARDAN","EN ÇOK *NEYİ ÖZLEDİN?*","*YORUMLARA YAZ.*","DOKSANLAR ÇOCUKLARI,","*BURADA MISINIZ?*"]]
out=[]
for i,chunks in enumerate(CH):
    sr,d=wavfile.read(f"{VO}/l{i}.wav"); d=d.astype(float)/32768
    hop=int(sr*0.01); e=np.array([np.sqrt(np.mean(d[k:k+hop]**2)) for k in range(0,len(d)-hop,hop)])
    thr=max(e.max()*0.06,1e-3); sil=e<thr
    # silence runs >= 9 frames
    runs=[];k=0
    while k<len(sil):
        if sil[k]:
            j=k
            while j<len(sil) and sil[j]: j+=1
            if j-k>=9 and k>0 and j<len(sil): runs.append(((k+j)/2*0.01,(j-k)*0.01))
            k=j
        else: k+=1
    # speech start/end
    sp=np.where(~sil)[0]; a,b=sp[0]*0.01,sp[-1]*0.01
    w=[len(c.replace('*',''))+4 for c in chunks]; cum=np.cumsum(w)/sum(w)
    bounds=[a]
    used=set()
    for c in cum[:-1]:
        est=a+(b-a)*c
        cand=[(abs(m-est),idx,m) for idx,(m,l) in enumerate(runs) if idx not in used and abs(m-est)<0.45]
        if cand:
            _,idx,m=min(cand); used.add(idx); est=m
        bounds.append(max(est,bounds[-1]+0.25))
    bounds.append(b+0.25)
    for j,c in enumerate(chunks):
        out.append({"t0":round(tl["starts"][i]+bounds[j],3),"t1":round(tl["starts"][i]+bounds[j+1],3),"text":c,"line":i})
    print(i,[round(x,2) for x in bounds],[round(m,2) for m,_ in runs])
json.dump(out,open("captions.json","w"),ensure_ascii=False,indent=0)
