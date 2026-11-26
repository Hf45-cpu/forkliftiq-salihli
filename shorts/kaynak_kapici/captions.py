import json, numpy as np
from scipy.io import wavfile
VO="/tmp/claude-0/-home-user-forkliftiq-salihli/2dc5a21c-e011-5b01-b859-14ffbfbdb788/scratchpad/vo2"
CH=[["BİR ZAMANLAR","HER APARTMANIN","BİR *KRALI* VARDI...","*KAPICI!*"],
["SABAHIN YEDİSİNDE","*EKMEK, GAZETE, SÜT...*","ÜST KATTAN İPLE","*SEPET* SARKITILIR,","KAPICI DA *SICAK EKMEĞİ*","İÇİNE KOYARDI."],
["KIŞIN *KÖMÜR KAMYONU* GELİNCE,","BÜTÜN GÜN","*KÜREK* SALLARDI.","KALORİFER YANMADIYSA...","*SUÇLU BELLİYDİ!*"],
["KİM TAŞINDI,","KİM EVLENDİ,","KİME MİSAFİR GELDİ...","APARTMANIN","*CANLI ARŞİVİYDİ.*"],
["PEKİ *NE OLDU?*","*DOĞALGAZ* GELDİ,","KÖMÜR GİTTİ.","*MARKET* KAPIYA GELDİ.","YENİ BİNALARIN ÇOĞUNDA","ARTIK *KAPICI DAİRESİ*","BİLE YOK."],
["YERİNE *SİTE YÖNETİMİ,*","*KAMERALAR*","VE *AKILLI KİLİTLER* ALDI.","AMA HİÇBİRİ,","BAYRAMDA KAPINI ÇALIP","*\"BAYRAMINIZ MÜBAREK OLSUN\"*","DEMEDİ."],
["SENİN APARTMANININ","*KAPICISININ ADI* NEYDİ?","*YORUMLARA YAZ.*"],
["KAYBOLAN MESLEKLER","SERİSİNİ KAÇIRMAMAK İÇİN...","*HEMEN ABONE OL!*"]]
import numpy as _np
from scipy.io import wavfile as _wf
_d=[len(_wf.read(f"{VO}/l{i}.wav")[1])/44100 for i in range(8)]
_g=[0.6,0.6,0.6,0.6,0.6,0.9,0.5]; _s=[0.9]
for i in range(7): _s.append(_s[-1]+_d[i]+_g[i])
tl={"starts":_s}
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
