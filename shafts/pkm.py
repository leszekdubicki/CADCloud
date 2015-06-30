"""
plik zaw. funkcje i klasy pkm
funkcje zwracaj± s³owniki z danymi (np uszczelnienia wa³ów)
specjalne zadania (np rysowanie tego badziewia) bêdzie realizowane przez osobne funkcje 
które bêda rozró¿nia³y jakim obiektem (pseudoobiektem/s³ownikiem) jest dana zmienna (argument)
ka¿dy pseudoobiekt bêdzie zawiera³ dwa specjalne pola pozwalaj±ce je odró¿niæ
jedno z nazw± tego pseudoobiektu, drugie z list± (dos³ownie i w przeno¶ni) nazw pól

rysowaniem takich pseudoobiektów bêdzie zajmowa³a sie specjalna funkcja bo bezsensu ¿eby taka popierdu³ka by³a klas±
"""
#*************************************************************************************
#funkcje:

#global NAZWA_PLIKU_TEX
#0000000000000000000000000000000000000000000000000000000000000000000000000
#funkcja 0 - s³u¿y do testowania ró¿nych stuffów:
def tescik():
	a="wielka kupa"
	return a
#0000000000000000000000000000000000000000000000000000000000000000000000000


def kozeb_wyn(NAZ_PL):
    #funkcja odczytuje pliki wynikowe programu kozebw
    PLIK=open(NAZ_PL,'r')
    LINIE=PLIK.readlines()
    PLIK.close()

    #obróbka pliku:

    #1. usuniêcie pierwszych 4 linii:
    LINIE=LINIE[4:]
    #2. usuniêcie ostatnich 3 linii:
    LINIE=LINIE[0:len(LINIE)-3]
    WYNIK={}
    nr_mat=1
    for i in range(0,len(LINIE)):
        #3. usuniêcie pocz±tkowych (opisowych) elementów ka¿dej linii (pierwsze 44 kol.) i ostatnich znaków (ramki i \r i \n)
        LINIE[i]=LINIE[i][44:len(LINIE[i])-3]
        #4. rozdzielenie na wyrazy:
        WYRAZY=LINIE[i].split()
        if (len(WYRAZY)==0) or (len(WYRAZY)==1) or ('WALCOWYCH' in WYRAZY):
            continue
        #sprawdzenie, z jakimi wielko¶ciami mamy do czynienia:
        if len(WYRAZY)==2:
            WYNIK[WYRAZY[0]]=float(WYRAZY[1])
        elif (len(WYRAZY)==3) and (WYRAZY[0].count('1,2')!=0):
            KEY=WYRAZY[0][0:WYRAZY[0].index('1,2')]
            WYNIK[KEY+'1']=float(WYRAZY[1])
            WYNIK[KEY+'2']=float(WYRAZY[2])
        elif (WYRAZY[0]=='hartowana') and (nr_mat==1):
            WYNIK['mat1']=''
            for j in range(2,len(WYRAZY)):
                WYNIK['mat1']=WYNIK['mat1']+WYRAZY[j]
            nr_mat=nr_mat+1
        elif (WYRAZY[0]=='hartowana') and (nr_mat==2):
            WYNIK['mat2']=''
            for j in range(2,len(WYRAZY)):
                WYNIK['mat2']=WYNIK['mat2']+WYRAZY[j]
            nr_mat=nr_mat+1
        elif (len(WYRAZY)==3):
            WYNIK[WYRAZY[0]]=[float(WYRAZY[1]),float(WYRAZY[2])]
    WYNIK['beta']=WYNIK['\xe1']
    WYNIK['alpha']=WYNIK['\xe0n']
    WYNIK['alpha_t']=WYNIK['\xe0t']
    WYNIK['id']='kozebw'
    WYNIK['nr_kola']=1 #mówi konstruktorowi ob. wal które kolo brac pod uwage
    #obliczenie si³ obc. wa³y:
    from math import tan, cos, pi
    WYNIK['n2']=WYNIK['n1']*WYNIK['z1']/float(WYNIK['z2'])
    WYNIK['Ms1']=9550.0*WYNIK['N']/float(WYNIK['n1'])
    WYNIK['Fo1']=1000.0*2.0*WYNIK['Ms1']/WYNIK['d1']
    WYNIK['Fr1']=WYNIK['Fo1']*tan(WYNIK['alpha']*pi/180.0)/cos(WYNIK['beta']*pi/180.0)
    WYNIK['Fa1']=WYNIK['Fo1']*tan(WYNIK['beta']*pi/180.0)
    WYNIK['Ms2']=9550.0*WYNIK['N']/float(WYNIK['n2'])
    WYNIK['Fo2']=1000.0*2.0*WYNIK['Ms2']/WYNIK['d2']
    WYNIK['Fr2']=WYNIK['Fo2']*tan(WYNIK['alpha']*pi/180.0)/cos(WYNIK['beta']*pi/180.0)
    WYNIK['Fa2']=WYNIK['Fo2']*tan(WYNIK['beta']*pi/180.0)
    return(WYNIK)
#definicja klasy kolo_zebate:
class cos_na_wale:
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['cos_na_wale','cos']
        self.__name__='cos_na_wale'
    def ustaw_klucze(self):
        #sprawdzenie podstawowych kluczy i ew. ustawienie ich:
        #s³ownik zaw wymagane klucze i ich warto¶ci domy¶lne:
        WYM_KLUCZE={'l-':0.0,'l+':0.0,'b-':0.0,'b+':0.0}
        try:
            WYM_KLUCZE=self._klucze.update(WYM_KLUCZE)
        except:
            kupa='kupa'

        self._klucze=WYM_KLUCZE
        for KLUCZ in WYM_KLUCZE.keys():
            if not self._dane.has_key(KLUCZ):
                self._dane[KLUCZ]=WYM_KLUCZE[KLUCZ]
    def __getitem__(self,ITEM):
        return self._dane[ITEM]
    def __setitem__(self,ITEM,WARTOSC):
        self._dane[ITEM]=WARTOSC
    def typ(self):
        try:
            return self._ozn_typu[0]
        except:
            return ''
    def isa(self,OZN):
        if (OZN in self._ozn_typu) or (OZN==self.__name__):
            return 1
        else:
            return 0
    def l_c(self):
        #metoda zwraca ca³kowit± d³ugo¶æ elementu nie pokrywaj±c± siê z innymi elementami:
        #w sumie to d³ugo¶æ wa³u o ¶rednicy elementu
        return self['b']+self['b-']+self['b+']+self['l-']+self['l+']
    def l_obc(self,STR='-',WITH_B=0):
        #metoda zwraca d³ugo¶æ od krawêdzi do ¶rodka obci±¿enia elementu w stronê + lub - osi z:
        #WITH_B - czy braæ pod uwagê ca³e b mo¿e byæ równe 0,1,lub -1
        return self['b']/2.0+self['b'+STR]+self['l'+STR] + (self['b']/2.0*int(WITH_B))
    def L_p(self,STR=''):
        #zwraca d³ugo¶æ piasty
        if STR=='':
            return self['b']+self['b-']+self['b+']
        else:
            #to zwraca tylko po³owê piasty w STR
            return self['b']/2.0+self['b'+STR]
    def powieksz(self,l,STR=''):
        #metoda powiêksza odcinki przed i po elemencie tak, aby zachowane by³y proporcje miêdzy nimi
        #l to d³ugo¶æ jak± ma zajmowaæ ca³y element:
        #je¶li 'l+' lub 'l-' jest równe 0 to nie jest zmieniane
        #je¶li argument STR jest ró¿ny od '' to powiêksza stronê STR ('+' lub '-')
        l_w=l-self['b']-self['b-']-self['b+']
        if len(STR)==0:
            if (self['l+']==0) and (self['l-']==0):
                self['l-']=l_w/2.0; self['l+']=l_w/2.0
            elif self['l+']==0:
                self['l+']=l_w
            elif self['l-']==0:
                self['l-']=l_w
            else:
                STOSUNEK=self['l+']/float(self['l+']+self['l-'])
                self['l+']=l_w*STOSUNEK; self['l-']=l_w-self['l+']
        else:
            STR_PRZEC='+'*int(STR=='-')+'-'*int(STR=='+')
            self['l'+STR]=l_w-self[l+STR_PRZEC]
    def text_dan(self,KLUCZE):
        #funkcja zwraca tekst z danymi KLUCZE obiektu
        TEXT=''
        for i in range(0,len(KLUCZE)):
            TEXT=TEXT+\
            KLUCZE[i]+' = '+str(self[KLUCZE[i]])+'\n'
        return TEXT
class kolo_z(cos_na_wale):
    def __init__(self,dane,kier_obr='p',kier_lz='p',naped='c'):
        #dane to s³ownik z odpowiednimi polami
        #kier_obr - kierunek obrotów ('p'/'l')
        #kier_lz - kierunek pochylenia linii zêbów ('p'/'l')
        #naped - czy ko³o jest nepêdzane ( 'c'/'b' (czynne/bierne) )
        if not dane.has_key('kier_obr'):
            dane['kier_obr']=kier_obr
        if not dane.has_key('kier_lz'):
            dane['kier_lz']=kier_lz
        if not dane.has_key('naped'):
            dane['naped']=naped
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['kolo_z','kz','k_z']
        self.__name__='kolo_z'
    def obr_przec(self,obr=None):
        #metoda podaje przeciwne do obr obroty
        import types
        if isinstance(obr,types.NoneType):
            obr=self['kier_obr']
        if obr=='p':
            return 'l'
        elif obr=='l':
            return 'p'
    def kier_przec(self,obr=None):
        #metoda podaje przeciwne do obr obroty
        #jest kopi± poprzedniej ale chodzi o to aby by³a dziedziczone w niezmiennej postaci
        import types
        if isinstance(obr,types.NoneType):
            obr=self['kier_obr']
        if obr=='p':
            return 'l'
        elif obr=='l':
            return 'p'
    def kier_Fo(self):
        #metoda ustala kierunek dzia³ania si³y obwodowej
        #dla ko³a napêdzaj±cego jest on przeciwny do kierunku obr.
        #dla ko³a napêdzanego zgodny
        if (self['naped']=='c'):
            #to ko³o napêdzaj±ce, kierunek dzia³ania Fo przeciwny do kierunku obrotów:
            return self.obr_przec()
        elif self['naped']=='b':
            #to ko³o napêdzane, kierunek Fo zgodny z kierunkiem obr:
            return self['kier_obr']
    def kier_Fz(self):
        #metoda zwraca znak kierunku dzia³ania si³y Fz w zale¿no¶ci od kierunku obrotów
        #i napêdu ko³a
        #dodatni znaczy zgodny ze zwrotem osi z (osi wa³u)
        if (self['naped']=='c'):
            #to ko³o napêdzaj±ce, kierunek dzia³ania Fz dodatni dla kombinacji p-p i l-l, ujemny w przeciwnym wyp.:
            return 1*int(self['kier_obr']==self['kier_lz']) + (-1)*int(self['kier_obr']!=self['kier_lz'])
        elif self['naped']=='b':
            return (-1)*int(self['kier_obr']==self['kier_lz']) + 1*int(self['kier_obr']!=self['kier_lz'])
            #to ko³o napêdzane, kierunek dzia³ania Fz dodatni dla kombinacji p-l i l-p, ujemny w przeciwnym wyp.:
        
    def M_s(self):
        r=self['d']/2.0
        Fo=self['Fo']
        return r*Fo/1000.0
    def sily(self,PHI=0.0):
        #metoda zwraca si³y gdy punkt pracy jest na ¶rednicy podzia³owej pod k±tem PHI 
        #do przyjêtego uk³adu wspó³rzêdnych
        from math import *
        Fo=self['Fo']
        Fr=self['Fr']
        Fa=self['Fa']*self.kier_Fz()
        if self.kier_Fo()=='l':
            Fo=-1.0*Fo
        Fx=-1.0*(Fo*sin(PHI)-Fr*cos(PHI))
        Fy=-1.0*(-1.0*Fo*cos(PHI)-Fr*sin(PHI))
        Fz=Fa
        #teraz momenty:
        r=self['d']/2.0
        rx=self['d']/2.0*cos(PHI)
        ry=self['d']/2.0*sin(PHI)
        Mgx=Fz*rx/1000.0; Mgy=Fz*ry/1000.0; Ms=r*Fo/1000.0
        return {'Fx':Fx,'Fy':Fy,'Fz':Fz,'Mgx':Mgx,'Mgy':Mgy,'Ms':Ms}
    def dodaj_sily(self,SILY):
        #metoda dodaje si³y umieszczone w li¶cie w postaci s³owników odp. do klas walwp
        WYNIK={}
        KLUCZE_NIEDOD=['rx','ry']
        for i in range(0,len(SILY)):
            if i==0:
                WYNIK.update(SILY[i])
                break
            for K in SILY[i].keys():
                if not K in KLUCZE_NIEDOD:
                    WYNIK[K]=WYNIK[K]+SILY[i][K]
        return WYNIK
    def sily_w(self):
        if not self._dane.has_key('phi'):
            self['phi']=0.0
        if isinstance(self['phi'],float):
            return self.sily(self['phi'])
        elif isinstance(self['phi'],list):
            SILY=[]
            for i in range(0,len(self['phi'])):
                SILY.append(self.sily(self['phi'][i]))
            return self.dodaj_sily(SILY)
    def __str__(self):
        TEXT='KOLO ZEBATE:\n'+\
        self.text_dan(['z','d','b','Fo','Fr','Fa'])
        if self._dane.has_key('Dp'):
            TEXT=TEXT+\
            'Lp = '+str(self.L_p())+'\n'+\
            'Dp = '+str(self['Dp'])+'\n'
        return TEXT
    def fazka(self):
        import funkcje
        return funkcje.niceround(0.5*self['mn'],1)
    def rys(self,DANE_RYS,P0=[0.0,0.0]):
        #rysuje to pierdolone ko³o
        da=self['da']; df=self['df']; b=self['b']; d=self['d']; d_w=self['d_wal']; f=self.fazka()
        PIASTA=0
        if self._dane.has_key('Dp'):
            #to jest piasta:
            Dp=self['Dp']; Lp=self['b-']+b+self['b+']
            PIASTA=1
        else:
            Dp=d_w; Lp=b
        x0=P0[0]; y0=P0[1]
        import cad
        TEXT=';\r\n;rysunek ko³a zêbatego\r\n'+\
        cad.sly('g',DANE_RYS)+\
        cad.linia([[x0-b/2.0,y0+Dp/2.0],[x0-b/2.0,y0+da/2.0-f],[x0-b/2.0+f,y0+da/2.0],[x0+b/2.0-f,y0+da/2.0],[x0+b/2.0,y0+da/2.0-f],[x0+b/2.0,y0+Dp/2.0]])+\
        cad.linia([[x0-b/2.0,y0+df/2.0],[x0+b/2.0,y0+df/2.0]])+\
        cad.sly('o',DANE_RYS)+\
        cad.linia([[x0-b/2.0-5.0,y0+d/2.0],[x0+b/2.0+5.0,y0+d/2.0]])+\
        cad.sly('g',DANE_RYS)+\
        cad.linia([[x0-b/2.0,y0-Dp/2.0],[x0-b/2.0,y0-da/2.0+f],[x0-b/2.0+f,y0-da/2.0],[x0+b/2.0-f,y0-da/2.0],[x0+b/2.0,y0-da/2.0+f],[x0+b/2.0,y0-Dp/2.0]])+\
        cad.linia([[x0-b/2.0,y0-df/2.0],[x0+b/2.0,y0-df/2.0]])+\
        cad.sly('o',DANE_RYS)+\
        cad.linia([[x0-b/2.0-5.0,y0-d/2.0],[x0+b/2.0+5.0,y0-d/2.0]])
        if PIASTA:
            TEXT=TEXT+\
            cad.sly('g',DANE_RYS)+\
            cad.linia([[x0-b/2.0,y0+Dp/2.0],[x0-Lp/2.0,y0+Dp/2.0],[x0-Lp/2.0,y0+d_w/2.0],[x0+Lp/2.0,y0+d_w/2.0],[x0+Lp/2.0,y0+Dp/2.0],[x0+b/2.0,y0+Dp/2.0]])+\
            cad.linia([[x0-b/2.0,y0-Dp/2.0],[x0-Lp/2.0,y0-Dp/2.0],[x0-Lp/2.0,y0-d_w/2.0],[x0+Lp/2.0,y0-d_w/2.0],[x0+Lp/2.0,y0-Dp/2.0],[x0+b/2.0,y0-Dp/2.0]])
        return TEXT
    def piasta(self,wpust):
        #funkcja ustawia piastê ko³a na podst. wpustu:
        if not wpust._dane.has_key('d_wal'):
            wpust['d_wal']=self['d_wal']
        if not wpust._dane.has_key('Ms'):
            wpust['Ms']=self['Ms']
        d_b=wpust.l_min()-self['b']
        if d_b>0:
            self['b+']=self['b-']=d_b/2.0
            wpust.ust_l()
            if not self._dane.has_key('Dp'):
                self['Dp']=round(1.6*self['d_wal'])
        return wpust
        
        
#definicja klasy para kó³ zêbatych:
class para_z(kolo_z):
    def __init__(self,dane,kier_obr_1='p',kier_lz_1='p'):
        if isinstance(dane,str):
            DANE=kozeb_wyn(dane)
            self._plik_wyn=dane
            self.__init__(DANE,kier_obr_1,kier_lz_1)
        elif isinstance(dane,dict):
            import copy
            DANE=copy.deepcopy(dane)
            #stworzenie obiektów kó³:
            KLUCZE=DANE.keys()
            #wstêpne dane dla kó³:
            DANE_1={'kier_obr':kier_obr_1,'kier_lz':kier_lz_1,'naped':'c'}
            DANE_2={'kier_obr':self.kier_przec(kier_obr_1),'kier_lz':self.kier_przec(kier_lz_1),'naped':'c'}
            for i in range(0,len(KLUCZE)):
                K=KLUCZE[i]
                if K[len(K)-1]=='1':
                    DANE_1[K[0:len(K)-1]]=DANE[K]
                elif K[len(K)-1]=='2':
                    DANE_2[K[0:len(K)-1]]=DANE[K]
                else:
                    DANE_1[K]=DANE[K]
                    DANE_2[K]=DANE[K]
            #raw_input('co kurwa')        
            self._kola={1:kolo_z(DANE_1),2:kolo_z(DANE_2)}
            DANE['kier_obr_1']=kier_obr_1 #kierunek obrotów ko³a pierwszego
            DANE['kier_lz_1']=kier_lz_1 #kierunek poch linii zêbów ko³a pierwszego
            self._dane=DANE
            self.ustaw_klucze()
            self._kola[1]['b']=self._kola[1]['b']+2.0
            self._ozn_typu=['para_z','pz','p_z','para']
            self.__name__='para_z'
            #troche tu redundancji, ale spoko
    def obr_przec(self,KOLO=1,OBR=None):
        return self._kola[KOLO].obr_przec(OBR)
    def kier_Fo(self,KOLO=1):
        #metoda ustala kierunek dzia³ania si³y obwodowej
        #dla ko³a napêdzaj±cego jest on przeciwny do kierunku obr.
        #dla ko³a napêdzanego zgodny
        return self._kola[KOLO].kier_Fo
    def sily(self,KOLO=1,PHI=0.0):
        #metoda podaje warto¶æ si³ obci±zaj±cych wa³y dla punktu przy³o¿enia si³y pod k±tem 
        #PHI od osi x , przy czym o¶ z jest zgodna a uk³ad jest lewoskrêtny (k±t jest mierzony w lew± str - jak w acadzie)
        return self._kola[KOLO].sily(PHI)
    def pierwszy_wal(self,NR=1):
        #metoda ustawia pole _pierwszy_wal które mówi o kierunku osi
        self._pierwszy_wal=NR
    def sily_w(self,WAL=1,PIERWSZY_WAL=None):
        #metoda zwraca si³y dzia³aj±ce na wa³y w postaci wymaganej przez konstr. klasy wal2p i walwp
        #dla osi x biegn±cej od wa³u PIERWSZY_WAL do tego drugiego, osi y prostopad³ej do niej
        #WAL to dla którego wa³u zwróciæ si³y
        import types
        if isinstance(PIERWSZY_WAL,types.NoneType):
            PIERWSZY_WAL=self._pierwszy_wal
        import math
        if PIERWSZY_WAL==1:
            #to o¶ x biegnie od wa³u 1 do wa³u 2:
            PHI_1=0.0; PHI_2=math.pi
        elif PIERWSZY_WAL==2:
            #to o¶ x biegnie od wa³u 2 do wa³u 1:
            PHI_2=0.0; PHI_1=math.pi
        if WAL==1:
            SILY=self.sily(WAL,PHI_1)
        elif WAL==2:
            SILY=self.sily(WAL,PHI_2)
        return SILY
    def ustaw_phi(self,PIERWSZY_WAL=None):
        import types
        if isinstance(PIERWSZY_WAL,types.NoneType):
            PIERWSZY_WAL=self._pierwszy_wal
        else:
            self._pierwszy_wal=PIERWSZY_WAL
        import math
        if PIERWSZY_WAL==1:
            #to o¶ x biegnie od wa³u 1 do wa³u 2:
            PHI_1=0.0; PHI_2=math.pi
        elif PIERWSZY_WAL==2:
            #to o¶ x biegnie od wa³u 2 do wa³u 1:
            PHI_2=0.0; PHI_1=math.pi
        self._kola[1]['phi']=PHI_1
        self._kola[2]['phi']=PHI_2
    def __str__(self):
        TEXT='PARA KOL ZEBATYCH:\n'+\
        'KOLO 1:\n'+\
        self._kola[1].__str__()+\
        'KOLO 2:\n'+\
        self._kola[2].__str__()
        return TEXT
class trojka_z(para_z):
    #klasa trójka, sk³ada siê generalnia z dwuch par, ko³o drugie pary pierwszej = ko³o pierwsze pary drugiej
    def __init__(self,dane_1,dane_2,a_w,poz='g',kier_obr_1='p',kier_lz_1='p'):
        self._para_1=para_z(dane_1,kier_obr_1,kier_lz_1)
        self._para_2=para_z(dane_2,self.kier_przec(kier_obr_1),self.kier_przec(kier_lz_1))
        self._kola={1:self._para_1._kola[1],3:self._para_1._kola[2],2:self._para_2._kola[2]}
        self._kola[1]['b']=self._kola[1]['b']+2.0 #zwiekszenie szeroko¶ci wieñca pierwszego ko³a
        self._kola[3]['b']=self._kola[3]['b']+1.0 #zwiekszenie szeroko¶ci wieñca trzeciego ko³a
        #zwróæ uwagê, ¿e ko³o drugie jest tak naprawdê ostatnie (trzecie)
        self._a_w=a_w #odleg³o¶æ osi ko³a 1 i 3
        self._poz=poz #po³o¿enie drugiego kó³ka w stosunku do p³aszczyzny przech przez osie 1-3
        self._ozn_typu=['trojka_z','tz','t_z','trojka']
        self.__name__='trojka_z'
    def alpha(self,NR=0):
        #metoda oblicza k±ty pomiêdzy p³aszczyzn± ³±cz±c± osie 1 i 2 a p³aszczyzn± ³±cz±c± osie 1 i 3 (alpha_1) oraz 
        #pomiêdzy p³aszczyzn± ³±cz±c± osie 2 i 3 a p³aszczyzn± ³±cz±c± osie 1 i 3 (alpha_2)
        #NR to numer k±ta, je¶li 0 to zwraca sumê k±tów:
        r1=self._kola[1]['d']/2.0; r2=self._kola[3]['d']/2.0; r3=self._kola[2]['d']/2.0
        a_w=self._a_w
        a_1=-0.5*( ((r2+r3)**2 - (r1+r2)**2)/(a_w) - a_w )
        a_2=a_w-a_1
        import math
        ALPHA_1=math.acos(a_1/(r1+r2))
        ALPHA_2=math.acos(a_2/(r2+r3))
        if NR==0:
            return ALPHA_2+ALPHA_1
        elif NR==1:
            return ALPHA_1
        elif NR==2:
            return ALPHA_2
    def sily(self,KOLO=1,PHI=0.0):
        #metoda wyprowadza s³ownik zaw. si³y dzia³aj±ce na wa³ ko³a KOLO pod k±tem PHI do osi x w lewo
        if KOLO==3:
            ALPHA_1=self.alpha(1)
            ALPHA_2=self.alpha(2)
            if self._poz=='g':
                PHI_1=-1.0*PHI-ALPHA_1
                PHI_2=ALPHA_2+math.pi-PHI
            if self._poz=='d':
                PHI_1=-1.0*PHI+ALPHA_1
                PHI_2=-1.0*ALPHA_2+math.pi-PHI
            SILY_1=self._para_1._kola[2].sily(PHI_1)
            SILY_2=self._para_2._kola[1].sily(PHI_2)
            KLUCZE=SILY_2.keys()
            SILY={}
            for i in range(0,len(KLUCZE)):
                SILY=[KLUCZE[i]]=SILY_1[KLUCZE[i]]+SILY_2[KLUCZE[i]]
            return SILY
        else:
            return self._kola[KOLO].sily(PHI)
    def sily_w(self,WALY=[1,2],WAL=1):
        #metoda zwraca si³y dzia³aj±ce na wa³y w postaci wymaganej przez konstr. klasy wal2p i walwp
        #dla osi x biegn±cej od wa³u WALY[0] do WALY[1], osi y prostopad³ej do niej
        #WAL to dla którego wa³u zwróciæ si³y
        #
        import math
        if WALY==[1,2]:
            #to o¶ x biegnie od wa³u 1 do wa³u 2:
            PHI_1=0.0; PHI_2=math.pi; PHI_3=0.0
        elif WALY==[2,1]:
            #to o¶ x biegnie od wa³u 2 do wa³u 1:
            PHI_2=0.0; PHI_1=math.pi; PHI_3=math.pi

        if WAL==1:
            SILY=self.sily(WAL,PHI_1)
        elif WAL==3:
            SILY=self.sily(WAL,PHI_3)
        elif WAL==2:
            SILY=self.sily(WAL,PHI_2)
        return SILY
    def ustaw_phi(self,PIERWSZY_WAL=None):
        import types
        if isinstance(PIERWSZY_WAL,types.NoneType):
            PIERWSZY_WAL=self._pierwszy_wal
        else:
            self._pierwszy_wal=PIERWSZY_WAL
        import math
        ALPHA_1=self.alpha(1)
        ALPHA_2=self.alpha(2)
        if PIERWSZY_WAL==1:
            #to o¶ x biegnie od wa³u 1 do wa³u 2:
            PHI_1=0.0+ALPHA_1; PHI_2=math.pi-ALPHA_2; PHI_3=0.0
        elif PIERWSZY_WAL==2:
            #to o¶ x biegnie od wa³u 2 do wa³u 1:
            PHI_2=0.0+ALPHA_1; PHI_1=math.pi-ALPHA_2; PHI_3=math.pi
        #ustawienie wszystkich k±tów phi
        if self._poz=='g':
            PHI_3_1=-1.0*PHI_3-ALPHA_1
            PHI_3_2=ALPHA_2+math.pi-PHI_3
        if self._poz=='d':
            PHI_3_1=-1.0*PHI_3+ALPHA_1
            PHI_3_2=-1.0*ALPHA_2+math.pi-PHI_3
            PHI_1=-1.0*PHI_1
            PHI_2=-1.0*PHI_2
        PHI_3=[PHI_3_1,PHI_3_2]
        self._kola[1]['phi']=PHI_1
        self._kola[2]['phi']=PHI_2
        self._kola[3]['phi']=PHI_3
    def __str__(self):
        TEXT='TROJKA KOL ZEBATYCH:\n'+\
        'KOLO 1:\n'+\
        self._kola[1].__str__()+\
        'KOLO 2:\n'+\
        self._kola[2].__str__()
        'KOLO 3:\n'+\
        self._kola[3].__str__()
        return TEXT
        
        
#definicja klasy wal2p:
class wal2p:
    """
    klasa przechowyjaca informacje i metody pomocne przy obliczeniach walow
    """
    def __init__(self,OBC,L):
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        """
        metoda konstruujaca obiekt
        OBC - lista zaw. slowniki - dla obciazen, oraz napis 'podpora' - jesli ma to byc podpora
        OBC ma nast. postac:
        [{'Fx':FX,'Fy':FY,'Mgx':MX,'Mgy':MY,'Ms':MS}, ... ,'podpora', ... ,'podpora', ...]
        lub:
        [{'Fx':FX,'Fy':FY,'Fz':Fz,'rx':RX,'ry':RY,'Ms':MS}, ... ,'podpora', ... ,'podpora', ...]
            wtedy Mgx=Fz*rx i Mgy=Fz*ry;
        L - odleglosci pomiedzy poszcz. elementami z listy OBC
        """
        self._OBC=OBC; self._L=L
        #stworzenie macierzy zaw. obci±¿enia i wspó³rzêdne z
        Z=[]; Fx=[]; Fy=[]; Mgx=[]; Mgy=[]; Ms=[]; Fz=[]
        LL=[0]+L; PODP=[]; i_PODP=[]
        for i in range(0,len(LL)):
            Z.append(float(sum(LL[:i+1])))
            if (isinstance(OBC[i],dict)):
                #sprawdzenie, czy s³ownik ma wszystkie klucze:
                if not OBC[i].has_key('Fx'):
                    OBC[i]['Fx']=0.0
                if not OBC[i].has_key('Fy'):
                    OBC[i]['Fy']=0.0
                if not OBC[i].has_key('Fz'):
                    OBC[i]['Fz']=0.0
                if not OBC[i].has_key('Ms'):
                    OBC[i]['Ms']=0.0
                if (not OBC[i].has_key('rx')) and (not OBC[i].has_key('Mgx')):
                    OBC[i]['Mgx']=0.0
                    OBC[i]['rx']=0.0
                if (not OBC[i].has_key('ry')) and (not OBC[i].has_key('Mgy')):
                    OBC[i]['Mgy']=0.0
                    OBC[i]['ry']=0.0
                
                Fx.append(float(OBC[i]['Fx'])); Fy.append(float(OBC[i]['Fy'])); Ms.append(float(OBC[i]['Ms']))
                #momenty gn±ce:
                if (OBC[i].has_key('Mgx')):
                    Mgx.append(float(OBC[i]['Mgx']))
                else:
                    Mgx.append(float(OBC[i]['Fz'])*OBC[i]['rx']/1000.0)
                if (OBC[i].has_key('Mgy')):
                    Mgy.append(float(OBC[i]['Mgy']))
                else:
                    Mgy.append(float(OBC[i]['Fz'])*OBC[i]['ry']/1000.0)
                if OBC[i].has_key('Fz'):
                    Fz.append(OBC[i]['Fz'])
                else:
                    Fz.append(0.0)
                    
            elif isinstance(OBC[i],str):
                Fx.append(0.0); Fy.append(0.0); Ms.append(0.0); Mgx.append(0.0); Mgy.append(0.0); 
                Fz.append(0.0)
                PODP.append(Z[i])
                i_PODP.append(len(Z)-1)
       
        za=PODP[0]; zb=PODP[1]
        ia=Z.index(za); ib=Z.index(zb)
        #Zmiana wszystkiego na tablice array:
        Fx=array(Fx); Fy=array(Fy); Mgx=array(Mgx); Mgy=array(Mgy); Ms=array(Ms); Z=array(Z)
        
        #za³atwienie problemu momentu skrêcaj±cego
        #wyszed³em z za³o¿enia, ¿e EMs=0 na ca³ej d³ aw³u, wiêc je¶li ostatni odbiornik momentu nie zeruje ca³o¶ci
        #to jest podmieniany tak, ¿eby j± zerowa³
        #w przypadku wiêcej ni¿ dwóch elementów wtytwarzaj±cych m. trzeba bardzo dok³adnie wprowadzaæ
        #momenty ¿eby nie by³o nieporozumieñ
        if sum(Ms)!=0:
            Ms[len(Ms)-1]=-1.0*sum(Ms[0:len(Ms)-1])

        #obliczenie reakcji podpór:
        Rax=(-1.0*(sum(Fx*(Z-zb)/1000.0))+sum(Mgx))*1/(za-zb)*1000.0; Rbx=(-1.0*(sum(Fx*(Z-za)/1000.0))+sum(Mgx))*1/(zb-za)*1000.0  #przed momentami zmieniono znak na +: z niewiadomych przyczyn tak jest dobrze
        Ray=-1.0*sum(Fy*(Z-zb)/1000.0-Mgy)*1/(za-zb)*1000.0; Rby=-1.0*sum(Fy*(Z-za)/1000.0-Mgy)*1/(zb-za)*1000.0  #przed momentami zmieniono znak na - (analogicznie do poprzedniego równania - wynikato z jego innej konstrukcji): z niewiadomych przyczyn tak jest dobrze
        Ra=sqrt(Rax**2+Ray**2); Rb=sqrt(Rbx**2+Rby**2)
        R=[Ra,Rb]; Rx=[Rax,Rbx]; Ry=[Ray,Rby]
        #podstawienie Ra i Rb do wektorów Fx i Fy:
        Fx[ia]=Rax; Fx[ib]=Rbx
        Fy[ia]=Ray; Fy[ib]=Rby
        self._i_PODP=i_PODP
        self._Fx=Fx; self._Fy=Fy; self._Mgx=Mgx; self._Mgy=Mgy; self._Ms=Ms; self._PODP=PODP; self._Z=Z
        from copy import deepcopy
        self._Z0=deepcopy(Z)
        self._za=za; self._zb=zb
        self._z_podp=[self._za,self._zb]
        self._ia=ia; self._ib=ib
        self._Rax=Rax; self._Ray=Ray; self._Rbx=Rbx; self._Rby=Rby
        self._Ra=Ra; self._Rb=Rb; 
        self._R=R; self._Rx=Rx; self._Ry=Ry
        self._IS_SZTYWN=0
        self._Fz=Fz

    def moment(self,z,_os=""):
        """
        metoda oblicza moment gn±cy w podanej osi ("x", "y", "" - wypadkowy) w danym punkcie z (z mo¿e te¿ byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        if _os=="x":
            Mg=self._Mgx
            F=self._Fx
        elif _os=="y":
            Mg=self._Mgy
            F=self._Fy
        elif len(_os)==0:
            Mx=self.moment(z,'x')
            My=self.moment(z,'y')
            M=sqrt(Mx**2+My**2)
            return M
        #Z=concatenate([self._Z,array(self._Z[len(self._Z)-1])])
        Z=self._Z
        if (isinstance(z,float)) or (isinstance(z,int)):
            #to mamy do czynienia z pojedyncz± liczb±, to upraqszcza sprawê:
            M=(sum(F*0.001*(z-Z)*((z-Z)>=0))+sum(Mg*((z-Z)>=0))) #te 1000 na koñcu to zamiana z Nmm na Nm
        elif isinstance(z,ArrayType):
            #no tu sprawa jest nieco bardziej skomplikowana:
            try:
                M=zeros(size(z),type=Float64)
            except:
                M=zeros(size(z),typecode='f')
            for i in range(0,len(Z)):
                M=M+F[i]*(0.001*(z-Z[i])*(z>=Z[i]))+Mg[i]*(z>=Z[i])
        return M
    def moment_s(self,z):
        """
        metoda oblicza moment skrêcaj±cy w danym punkcie z (z mo¿e te¿ byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        Ms=self._Ms
        Z=self._Z
        if (isinstance(z,float)) or (isinstance(z,int)):
            #to mamy do czynienia z pojedyncz± liczb±, to upraqszcza sprawê:
            M=sum(Ms*((z-Z)>=0))
        elif isinstance(z,ArrayType):
            #no tu sprawa jest nieco bardziej skomplikowana:
            try:
                M=zeros(size(z),type=Float64)
            except:
                M=zeros(size(z),typecode='f')
            for i in range(0,len(Z)):
                M=M+Ms[i]*((z-Z[i])>=0)
        return M

    def moment_zred(self,z,ALPHA=0):
        """
        metoda oblicza moment zredukowany w danym punkcie z (z mo¿e te¿ byæ macierz±) dla dominuj±cego zginania
        ALPHA to wspó³czynnik (ALPHA=Zgo/2*Zso=~sqrt(3)/2 - dla zmiany kier. obr. wa³u, ALPHA=Zgo/2*Zsj=~sqrt(3)/4 - bez zmiany kier. obr. wa³u)
        je¶li ALPHA nie jest wprowadzany to metoda sprawdza, czy jest ustawiony atrybut obiektu _mat
        w którym s± przechowywane inf. o materiale
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        if (ALPHA==0):
            try:
                ZM_KIER=self._zmiana_kier
            except:
                print("uwaga: ustawiam atrybut _zmiana_kier na zero !!! ")
                ZM_KIER=0
                self._zmiana_kier=ZM_KIER
            try:
                MAT=self._mat
                if ZM_KIER==0:
                    ALPHA=MAT['Zgo']/(2*MAT['Zsj'])
                elif ZM_KIER==1:
                    ALPHA=MAT['Zgo']/(2*MAT['Zso'])
            except:
                print("uwaga: ustawiam ALPHA a priori odp. do atrybutu _zmiana_kier!!! ")
                ALPHA=(sqrt(3)/2.0)*(ZM_KIER==1)+(sqrt(3)/4.0)*(ZM_KIER==0)
                
        #obliczenie momentów wypadkowego i skrêcaj±cego dla zadanego z:
        Mg=self.moment(z); Ms=self.moment_s(z)
        M=sqrt(Mg**2+(ALPHA*Ms)**2)
        self._ALPHA=ALPHA
        return M
    def mat(self,MAT):
        if not MAT.has_key('xz'):
            MAT['xz']=3.0
        if not MAT.has_key('kgo'):
            MAT['kgo']=MAT['Zgo']/MAT['xz']
        self._mat=MAT
    def d_teor(self,z,ALPHA=0):
        """
        metoda oblicza srednice minimaln± z war. wytrzyma³o¶ciowego w danym punkcie z (z mo¿e te¿ byæ macierz±)
        drugi argument ALPHA wprowadza siê w celu obliczenia momentu zredukowanego - patrz opis w metodzie moment_zred()
        obliczona ¶rednica jest s³uszna tylko dla dominujacego zginania
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        try:
            MAT=self._mat
            kgo=MAT['kgo']
        except:
            print("blad: ¿eby obliczyæ d_teor musisz wprowadziæ atrybut MAT, a w nim kgo!!! ")
            return

        Mzr=self.moment_zred(z,ALPHA)
        d=((32.0*Mzr*1000.0)/(pi*kgo))**(1/3.0)
        return d
    def d_teor_M(self,M):
        """
        metoda oblicza srednice minimaln± z war. wytrzyma³o¶ciowego dla momentu M (M mo¿e te¿ byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        try:
            MAT=self._mat
            kgo=MAT['kgo']
        except:
            print("blad: ¿eby obliczyæ d_teor musisz wprowadziæ atrybut MAT, a w nim kgo!!! ")
            return

        Mzr=M
        d=((32.0*Mzr*1000.0)/(pi*kgo))**(1/3.0)
        return d
    def set_d(self,D,L,L0):
        """
        przy pomocy tej metody ustawia siê ¶rednice poszczególnych stopni wa³u
        D - lista (wektor) zaw. ¶rednice poszczególnych stopni
        L - lista (wektor) zaw. d³ugo¶ci poszczególnych stopni
        L0 - odleg³o¶æ czo³a wa³u od pierwszego punktu obci±¿enia
        """

        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
            
        self._IS_SZTYWN=1
        #wszystkie wielko¶ci charakterystyczne (wektory Z, M itd) bêd± zdefiniowane na nowo z 
        #indeksem _s (od sztywno¶æ)
        #wa³ ma teraz wiêcej punktów granicznych na których zmianiaj± siê przebiegi naprê¿eñ (odkszta³ceñ)
        #bo zmieniaj± siê one i w punktach ze zmian± obci±¿eñ i zmiany przekroju (¶rednicy)
        
        #ustawienie danych wej¶ciowych jako pól obiektu:
        self._D=D; self._L_s=L; self._L0=L0
        #za³adowanie starych pól obiektu do przekszta³ceñ:
        import copy
        Z=copy.deepcopy(self._Z); Mgx=copy.deepcopy(self._Mgx); Mgy=copy.deepcopy(self._Mgy); Ms=copy.deepcopy(self._Ms); Fx=copy.deepcopy(self._Fx); Fy=copy.deepcopy(self._Fy)
        self._Z=self._Z+L0
        ########################################################################################
        #dodanie L0 do dotychczasowego Z:
        Z=Z+L0
        L_s=concatenate([array([0]),cumsum(array(L))]); D__s=concatenate([array(D),array([D[len(D)-1]])])
        n=len(Z)
        Z_s=array([]); Mgx_s=array([]); Mgy_s=array([]); Ms_s=array([]); Fx_s=array([]); Fy_s=array([]); D_s=array([]); Ix_s=array([]); Iy_s=array([]); Io_s=array([])
        for i in range(0,n):
            while (len(L_s)>0) and (L_s[0]<Z[i]):
                Z_s=concatenate([Z_s,array([float(L_s[0])])])  #wektor wspó³rzêdnych pocz±tków przedzia³ów
                D_s=concatenate([D_s,array(float(D__s[0]))])   #wektor ¶rednic przedzia³ów 
                d_temp=float(D__s[0])
                Fx_s=concatenate([Fx_s,array([0.0])])     #wektor si³ x obci±¿aj±cych na pocz±tku przedz.
                Fy_s=concatenate([Fy_s,array([0.0])])     #wektor si³ y obci±¿aj±cych na pocz±tku przedz.
                Mgx_s=concatenate([Mgx_s,array([0.0])])   #wektor mom. x obci±¿aj±cych na pocz±tku przedz.
                Mgy_s=concatenate([Mgy_s,array([0.0])])   #wektor mom. x obci±¿aj±cych na pocz±tku przedz.
                Ms_s=concatenate([Ms_s,array([0.0])])     #wektor mom. skrêcaj±cych na pocz±tku przedz.
                if len(L_s)>1:
                    L_s=L_s[1:]
                    D__s=D__s[1:]
                else:
                    L_s=array([])
                    D__s=array([])
            Z_s=concatenate([Z_s,array([float(Z[i])])])        #wektor wspó³rzêdnych pocz±tków przedzia³ów
            Fx_s=concatenate([Fx_s,array([Fx[i]])])     #wektor si³ x obci±¿aj±cych na pocz±tku przedz.
            Fy_s=concatenate([Fy_s,array([Fy[i]])])     #wektor si³ y obci±¿aj±cych na pocz±tku przedz.
            Mgx_s=concatenate([Mgx_s,array([Mgx[i]])])  #wektor mom. x obci±¿aj±cych na pocz±tku przedz.
            Mgy_s=concatenate([Mgy_s,array([Mgy[i]])])  #wektor mom. x obci±¿aj±cych na pocz±tku przedz.
            Ms_s=concatenate([Ms_s,array([Ms[i]])])     #wektor mom. skrêcaj±cych na pocz±tku przedz.
            if (len(L_s)>0) and (L_s[0]==Z[i]):
                D_s=concatenate([D_s,array(float(D__s[0]))])  #wektor ¶rednic przedzia³ów 
            else:
                D_s=concatenate([D_s,array([d_temp])])  #wektor ¶rednic przedzia³ów 
                
        #dope³nienie Z_s ew. pozosta³o¶ci± z L_s
        if len(L_s)>1:
            Z_s=concatenate([Z_s,L_s[0:len(L_s)-1]])
        Ix_s=(pi*(D_s**4))/64
        Iy_s=(pi*(D_s**4))/64
        self._Z_s=Z_s; self._Fx_s=Fx_s; self._Fy_s=Fy_s; self._Mgx_s=Mgx_s; self._Mgy_s=Mgy_s; self._Ms_s=Ms_s
        self._D_s=D_s; self._Ix_s=Ix_s; self._Iy_s=Iy_s
        #obliczenie macierzy M i B (patrz str. 5-12 Z. II.)
        #oznaczone jako MM i BB ¿eby nie koja¿y³y siê z momentem
        MMx=+1.0*cumsum(Fx_s); MMy=+1.0*cumsum(Fy_s) #zmieni³em znak na +
        BBx=1000*cumsum(Mgx_s)-cumsum(Fx_s*Z_s); BBy=1000*cumsum(Mgy_s)-cumsum(Fy_s*Z_s) #zmieni³em znak przed drugimi sk³adnikami na minus
        self._MMx=MMx; self._MMy=MMy; self._BBx=BBx; self._BBy=BBy
        #obliczenie sta³ych ca³kowania z warunków brzegowych:
        n=len(Z_s) #ilo¶æ przedzia³ów

        try:
            E=self._mat['E']
        except:
            E=2.1*(10**5) #MPa
        Sx=1/Ix_s
        Sy=1/Iy_s
        #1. warunek zerowego ugiêcia w podporach - tablice AA1 i DD1 (Z II. str. 8):
        za=copy.deepcopy(self._za)+L0; ia=list(Z_s).index(za)
        zb=copy.deepcopy(self._zb)+L0; ib=list(Z_s).index(zb)
        self._ia_s=ia; self._ib_s=ib

        AA1x=zeros([2,2*n],typecode='f'); AA1x[0,2*ia]=za; AA1x[0,2*ia+1]=1.0; AA1x[1,2*ib]=zb; AA1x[1,2*ib+1]=1.0
        AA1y=zeros([2,2*n],typecode='f'); AA1y[0,2*ia]=za; AA1y[0,2*ia+1]=1.0; AA1y[1,2*ib]=zb; AA1y[1,2*ib+1]=1.0
        DD1x=array([[-1*(MMx[ia]/6.0*(Z_s[ia]**3)+BBx[ia]/2*(Z_s[ia]**2))],\
        [-1*(MMx[ib]/6.0*(Z_s[ib]**3)+BBx[ib]/2*(Z_s[ib]**2))]])
        DD1y=array([[-1*(MMy[ia]/6.0*(Z_s[ia]**3)+BBy[ia]/2*(Z_s[ia]**2))],\
        [-1*(MMy[ib]/6.0*(Z_s[ib]**3)+BBy[ib]/2*(Z_s[ib]**2))]])

        #2. warunek równo¶ci k±tów obrotu na granicach przedzia³ów (z II. str 9):
        AA2x=zeros([n-1,2*n],typecode='f'); DD2x=zeros([n-1,1],typecode='f')
        AA2y=zeros([n-1,2*n],typecode='f'); DD2y=zeros([n-1,1],typecode='f')
        for i in range(0,n-1):
            AA2x[i,2*i]=1.0/Ix_s[i]; AA2x[i,2*(i+1)]=-1.0/Ix_s[i+1]
            AA2y[i,2*i]=1.0/Iy_s[i]; AA2y[i,2*(i+1)]=-1.0/Iy_s[i+1]
            DD2x[i,0]=1/(Ix_s[i+1])*(MMx[i+1]/2.0*(Z_s[i+1]**2)+BBx[i+1]*Z_s[i+1])-1/(Ix_s[i])*(MMx[i]/2.0*(Z_s[i+1]**2)+BBx[i]*Z_s[i+1])
            DD2y[i,0]=1/(Iy_s[i+1])*(MMy[i+1]/2.0*(Z_s[i+1]**2)+BBy[i+1]*Z_s[i+1])-1/(Ix_s[i])*(MMy[i]/2.0*(Z_s[i+1]**2)+BBy[i]*Z_s[i+1])
            #print(MMx[i]/2.0*Z_s[i]**2+BBx[i]*Z_s[i])
        #3. warunek równo¶ci ugiêcia na granicach przedzia³ów (z II. str 9):
        AA3x=zeros([n-1,2*n],typecode='f'); DD3x=zeros([n-1,1],typecode='f')
        AA3y=zeros([n-1,2*n],typecode='f'); DD3y=zeros([n-1,1],typecode='f')
        for i in range(0,n-1):
            AA3x[i,2*i]=Z_s[i+1]/Ix_s[i]; AA3x[i,2*(i+1)]=-1.0*Z_s[i+1]/Ix_s[i+1]
            AA3x[i,2*i+1]=1.0/Ix_s[i]; AA3x[i,2*(i+1)+1]=-1.0/Ix_s[i+1]
            AA3y[i,2*i]=Z_s[i+1]/Iy_s[i]; AA3y[i,2*(i+1)]=-1.0*Z_s[i+1]/Iy_s[i+1]
            AA3y[i,2*i+1]=1.0/Iy_s[i]; AA3y[i,2*(i+1)+1]=-1.0/Iy_s[i+1]
            DD3x[i,0]=1/Ix_s[i+1]*(MMx[i+1]/6.0*(Z_s[i+1]**3)+BBx[i+1]/2.0*(Z_s[i+1]**2))-1/Ix_s[i]*(MMx[i]/6.0*(Z_s[i+1]**3)+BBx[i]/2.0*(Z_s[i+1]**2))
            DD3y[i,0]=1/Iy_s[i+1]*(MMy[i+1]/6.0*(Z_s[i+1]**3)+BBy[i+1]/2.0*(Z_s[i+1]**2))-1/Iy_s[i]*(MMy[i]/6.0*(Z_s[i+1]**3)+BBy[i]/2.0*(Z_s[i+1]**2))
        #obliczenie macierzy sta³ych ca³kowania:
        AAx=concatenate([AA1x,AA2x,AA3x])
        AAy=concatenate([AA1y,AA2y,AA3y])
        DDx=concatenate([DD1x,DD2x,DD3x])
        DDy=concatenate([DD1y,DD2y,DD3y])
        CCx=matrixmultiply(inverse(AAx),DDx)
        CCy=matrixmultiply(inverse(AAy),DDy)
        #rozdzielenie CCx i CCy na dwie macierze - sta³ych po pierwszym ca³kowaniu i po drugim ca³kowaniu:
        CC1x=CCx[range(0,2*n-1,2),0]; CC2x=CCx[range(1,2*n,2),0]
        CC1y=CCy[range(0,2*n-1,2),0]; CC2y=CCy[range(1,2*n,2),0]
        
        self._AA1x=AA1x; self._AA2x=AA2x; self._AA3x=AA3x; self._AAx=AAx
        self._AA1y=AA1y; self._AA2y=AA2y; self._AA3y=AA3y; self._AAy=AAy
        self._DD1x=DD1x; self._DD2x=DD2x; self._DD3x=DD3x; self._DDx=DDx
        self._DD1y=DD1y; self._DD2y=DD2y; self._DD3y=DD3y; self._DDy=DDy
        self._Cx=CCx; self._Cy=CCy
        self._C1x=CC1x; self._C2x=CC2x
        self._C1y=CC1y; self._C2y=CC2y
        ########################################################################################
    
    def ugiecie(self,z,_os=""):
        """
        metoda oblicza strza³kê ugiêcia w podanej osi ("x", "y", "" - wypadkowa) w danym punkcie z (z mo¿e te¿ byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        import copy
        if _os=="x":
            M=self._MMx
            B=self._BBx
            C1=self._C1x
            C2=self._C2x
            I=self._Ix_s
        elif _os=="y":
            M=self._MMy
            B=self._BBy
            C1=self._C1y
            C2=self._C2y
            I=self._Iy_s
        elif len(_os)==0:
            fx=self.ugiecie(z,'x')
            fy=self.ugiecie(z,'y')
            f=sqrt(fx**2+fy**2)
            return f
        Z=copy.deepcopy(self._Z_s)
        L=sum(self._L_s)+0.001    #te 0.001 to ¿eby mo¿na by³o obliczyæ na ca³ej dl. wa³u
        
        Z=concatenate([Z,array([L])])
        try:
            E=self._mat['E']
        except:
            E=2.1*(10**5) #MPa
        
        f=zeros(size(z),typecode='f')
        S=-1.0/(E*I)
        for i in range(0,len(Z)-1):
            f=f+(S[i]*(M[i]/6.0*(z**3)+B[i]/2.0*(z**2))+S[i]*(C1[i]*z+C2[i]))*(z>=Z[i])*(z<Z[i+1])
            #print(f)
        if (isinstance(z,float)) or (isinstance(z,int)):
            f=f[0]
        
        return f
    def f_max(self,os='',krok=0.1,ZAKRES=1):
        #zwróciæ max. ugiêcie wa³u
        #zakres to parametr okre¶laj±cy przedzia³ poszukiwania
        #   ZAKRES = 1 - tylko miêdzy skrajnymi obci±¿eniami
        #   ZAKRES = 2 - ca³a d³ugo¶æ wa³u
        import pylab
        if ZAKRES==1:
            z=pylab.arange(self._L0,sum(self._L)+self._L0,krok)
        elif ZAKRES==2:
            z=pylab.arange(0.0,sum(self._L_s),krok)
        f=pylab.absolute(self.ugiecie(z,os))
        return pylab.amax(f)
    def kat_max(self,os='',krok=0.1,ZAKRES=1):
        #zwróciæ max. kat_obr wa³u
        #zakres to parametr okre¶laj±cy przedzia³ poszukiwania
        #   ZAKRES = 1 - tylko miêdzy skrajnymi obci±¿eniami
        #   ZAKRES = 2 - ca³a d³ugo¶æ wa³u
        import pylab
        if ZAKRES==1:
            z=pylab.arange(self._L0,sum(self._L)+self._L0,krok)
        elif ZAKRES==2:
            z=pylab.arange(0.0,sum(self._L_s),krok)
        f=pylab.absolute(self.kat_obr(z,os))
        return pylab.amax(f)
    def kat_obr(self,z,_os=""):
        """
        metoda oblicza k±t obrotu w podanej osi ("x", "y", "" - wypadkowa) w danym punkcie z (z mo¿e te¿ byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        import copy
        if _os=="x":
            M=self._MMx
            B=self._BBx
            C1=self._C1x
            I=self._Ix_s
        elif _os=="y":
            M=self._MMy
            B=self._BBy
            C1=self._C1y
            I=self._Iy_s
        elif len(_os)==0:
            phix=self.kat_obr(z,'x')
            phiy=self.kat_obr(z,'y')
            phi=sqrt(phix**2+phiy**2)
            return phi
        Z=copy.deepcopy(self._Z_s)
        L=sum(self._L_s)+0.001    #te 0.001 to ¿eby mo¿na by³o obliczyæ na ca³ej dl. wa³u
        
        Z=concatenate([Z,array([L])])
        try:
            E=self._mat['E']
        except:
            E=2.1*(10**5) #MPa
        
        phi=zeros(size(z),typecode='f')
        S=-1.0/(E*I)
        for i in range(0,len(Z)-1):
            phi=phi+(S[i]*(M[i]/2.0*(z**2)+B[i]/1.0*(z**1))+S[i]*(C1[i]))*(z>=Z[i])*(z<Z[i+1])
        
        return phi
        if (isinstance(z,float)) or (isinstance(z,int)):
            phi=phi[0]
    def d(self,z):
        """
        metoda podaje srednice wa³u (rzeczywist±) dla podanego z (mo¿e byæ macierz±)
        """
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        D=self._D_s
        Z=self._Z_s
        d=zeros(size(z),typecode='f')
        for i in range(0,len(Z)-1):
            d=d+D*((z>=Z[i])*(z<Z[i+1]))
        if (isinstance(z,float)) or (isinstance(z,int)):
            d=d[0]
        return d
    def obc_loz(self):
        """
        funkcja zwraca s³ownik zaw. dane potrzebne do obl. ³o¿ysk:
        Ra, Rb, Fw, da, db
        """
        WYN={}
        WYN['Ra']=abs(self._Ra)
        WYN['Rb']=abs(self._Rb)
        za=self._za+self._L0
        zb=self._zb+self._L0
        WYN['da']=self._D_s[self._ia_s]
        WYN['db']=self._D_s[self._ib_s]
        #jeszcze tylko zsumowanie wszystkich si³ wzd³u¿nych:
        #warunek jest taki, ¿eby dane by³y dp. wprowadzone
        OBC=self._OBC
        Fw=0
        for i in range(0,len(OBC)):
            if (isinstance(OBC[i],dict)) and (OBC[i].has_key('Fz')):
                Fw=Fw+OBC[i]['Fz']
        WYN['Fw']=abs(Fw)
        return WYN
    def rozst_podp(self):
        return self._z_podp[len(self._z_podp)-1]-self._z_podp[0]
    def f_dop(self,WSPOLCZYNNIK=0.0003):
        #zwraca dopuszczaln± strza³kê ugiêcia równ± (0.0002-0.0003) * rozst_podp
        return WSPOLCZYNNIK*self.rozst_podp()
    def has_key(self,klucz):
        """
        funkcja sprawdza czy obiekt ma atrybut klucz
        """
        try:
            eval('self.'+klucz)
            return True
        except:
            return False
    #___________________________________________________________________________________________________
    #dalej bêd± metody plotuj±ce ³adne wykresy ró¿nych wielko¶ci wa³ów dla zadanego z
    def plot(self,CO,TYT='',SHOW=0,naz_pliku='',z=[],legenda=1,is_subplot=0,nr_rys=1,mono=0):
        """
        Metoda kre¶li wykresy wielko¶ci podanych w li¶cie CO w kolumnie
        """
        NAZ_PL=naz_pliku
        if isinstance(CO,str):
            CO=[CO]
        PLOT_PCHAR=1 #czy rysowaæ punkty charakterystyczne (obc. podp.)
        #ustawienie kolor"ow:
        if mono:
            KOLOR='k'; KOLOR_D='k'; LW_D=2.0
            KOLOR_PODP='^k'; KOLOR_OBC='vk'
        else:
            KOLOR='b'; KOLOR_D='k'; LW_D=2.0
            KOLOR_PODP='^g'; KOLOR_OBC='vr'
        #za³adowanie matplotliba:
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        KROK_z=0.1
        MIN_z=0.0
        if self._IS_SZTYWN==0:
            MAX_z=sum(self._L)
        else:
            MAX_z=sum(self._L_s)
        if len(z)==0:
            z=arrayrange(0,MAX_z,KROK_z)
            
        #ustalenie granic osi z:
        Z_MIN=MIN_z-0.07*(MAX_z-MIN_z)
        Z_MAX=MAX_z+0.07*(MAX_z-MIN_z)
        SKALA_RYS=1.0
        if (len(NAZ_PL)==0) and (SHOW==1):
            SKALA_RYS=1.0 #¿eby zmie¶ci³o siê na ekranie
            
        if (len(CO)==1) and (len(NAZ_PL)>0):
            #FIG=figure(figsize=(297.0/25.4*SKALA_RYS,210.0/25.4*SKALA_RYS))
            FIGSIZE=(297.0/25.4*SKALA_RYS,210.0/25.4*SKALA_RYS)
            ORIENT='portrait'
            #ORIENT='landscape'
        elif (len(NAZ_PL)>0):
            #FIG=figure(figsize=(210.0/25.4,297.0/25.4))
            FIGSIZE=(210.0/25.4*SKALA_RYS,297.0/25.4*SKALA_RYS)
            ORIENT='portrait'
            #ORIENT='landscape'
        else:
            FIG=None
        if (len(NAZ_PL)>0) and (not SHOW):
            gcf().set_figsize_inches(FIGSIZE[0],FIGSIZE[1])

        ##############################################################################
        #narysowanie poszczególnych subplotów:
        for i in range(0,len(CO)):
            if not is_subplot:
                subplot(100*len(CO)+10+(i+1))
            if i==0:
                title(TYT)
            LEG_H=[]; LEG_T=[]
            IS_KRECHY=1
            IS_D=0
            Y_LAB=''
            if CO[i] in ['Mgx','M_gx']:
                w=self.moment(z,'x')
                Y_LAB='$M_{gx}\\ [Nm]$'
            elif CO[i] in ['Mgy','M_gy']:
                w=self.moment(z,'y')
                Y_LAB='$M_{gy}\\ [Nm]$'
            elif CO[i] in ['M_g','Mg']:
                w=self.moment(z,'')
                Y_LAB='$M_{g}(wypadkowy)\\ [Nm]$'
            elif CO[i] in ['Ms','M_s']:
                w=self.moment_s(z)
                Y_LAB='$M_{s}\\ [Nm]$'
            elif CO[i] in ['Mgz','Mzred','M_zr']:
                w=self.moment_zred(z)
                Y_LAB='$M_{gzr}(zredukowany)\\ [Nm]$'
            elif CO[i] in ['dteor','d','d_teor']:
                w=self.d_teor(z)
                Y_LAB='$r\\ [mm]$'
                IS_D=1
            elif CO[i] in ['fx','x','ugiecie_x']:
                w=self.ugiecie(z,'x')
                Y_LAB='$f_{x}\\ [mm]$'
            elif CO[i] in ['fy','y','ugiecie_y']:
                w=self.ugiecie(z,'y')
                Y_LAB='$f_{y}\\ [mm]$'
            elif CO[i] in ['f','ugiecie']:
                w=self.ugiecie(z,'')
                Y_LAB='$f\\ [mm]$'
            elif CO[i] in ['phix','phi_x','kat_obr_x']:
                w=self.kat_obr(z,'x')*180.0/pi
                Y_LAB='$\\phi_{x}\\ [^o]$'
            elif CO[i] in ['phiy','phi_y','kat_obr_y']:
                w=self.kat_obr(z,'y')*180.0/pi
                Y_LAB='$\\phi_{y}\\ [^o]$'
            elif CO[i] in ['phi','phi','kat_obr']:
                w=self.kat_obr(z,'')*180.0/pi
                Y_LAB='$\\phi\\ [^o]$'

            if IS_D==0:
                plot(z,w,KOLOR)
            else:
                print(w)
                plot(z,w/2.0,KOLOR,z,-1.0*w/2.0,KOLOR)
                if self.has_key('_L_s'):
                    #wykre¶lenie obrysu rzeczywistego
                    Z_D=concatenate([array([0.0]),cumsum(self._L_s)])
                    _D1=concatenate([self._D,array([self._D[len(self._D)-1]])])
                    _D2=concatenate([array([self._D[0]]),self._D])
                    _D=amax(concatenate([[_D1],[_D2]]))
                    for j in range(0,len(_D)):
                        #if _D1[j]>
                        plot(array([Z_D[j],Z_D[j]]),array([-_D[j]/2.0,_D[j]/2.0]),KOLOR_D)
                    for j in range(1,len(_D)):
                        plot(array([Z_D[j-1],Z_D[j]]),array([self._D[j-1]/2.0,self._D[j-1]/2.0]),KOLOR_D)
                        plot(array([Z_D[j-1],Z_D[j]]),array([-1.0*self._D[j-1]/2.0,-1.0*self._D[j-1]/2.0]),KOLOR_D)
                    #jeszcze ustawienie proporcjonalnej skali (patrz ni¿ej)
                    
            
            grid(1)
            #dorysowanie kresek do wykresu:
            if IS_KRECHY==1:
                #narysowanie kresek:
                n_KR=30
                d_KR=len(z)/n_KR
                j_KR=0
                for j in range(0,n_KR):
                    if j_KR<len(z):
                        if IS_D==0:
                            plot([z[j_KR],z[j_KR]],[0,w[j_KR]],KOLOR)
                        else:
                            plot([z[j_KR],z[j_KR]],[-1.0*w[j_KR]/2.0,w[j_KR]/2.0],KOLOR)
                        j_KR=j_KR+d_KR
                if j_KR-d_KR!=len(z)-1:
                    j_KR=len(z)-1
                    #narysowanie kreski na ost. miejscu
                    if IS_D:
                        plot([z[j_KR],z[j_KR]],[-1.0*w[j_KR]/2.0,w[j_KR]/2.0],KOLOR)
                    else:
                        plot([z[j_KR],z[j_KR]],[0.0,w[j_KR]],KOLOR)
                    
            #ró¿ne dodatki:
            #1. linia ozn. o¶ z:
            plot(array([min(z),amax(z)]),array([0,0]),'k')
            #2. znaczki odp. odpowiednim punktom (podpora, obci±¿enie) na tej osi:
            PODP=[]; OBC=[]
            for j in range(0,len(self._OBC)):
                if j in self._i_PODP:
                    PODP.append(self._Z[j])
                else:
                    OBC.append(self._Z[j])
            if PLOT_PCHAR:
                H_OBC=plot(array(OBC),zeros(size(OBC)),KOLOR_OBC)
                H_PODP=plot(array(PODP),zeros(size(PODP)),KOLOR_PODP)
            #i legenda dla tych znaczków:
            LEG_H=LEG_H+[H_OBC,H_PODP] #identyfikatory legendy
            LEG_T=LEG_T+['obciazenia','podpory'] #texty legendy
            
            #wstawienie legendy
            if (i==0) and (legenda):
                legend(LEG_H,LEG_T,'upper right')
            #3. opisy osi:
            xlabel('z [mm]')
            ylabel(Y_LAB)
            
            #ustawienie granic wykresu
            xlim(Z_MIN,Z_MAX)
            if get(gca(),'ylim')[0]==0:
                #trzeba troszeczkê podnie¶æ ¿eby by³o widaæ trójk±ciki
                YLIM=get(gca(),'ylim')
                Y_MIN=YLIM[0]-0.08*(YLIM[1]-YLIM[0])
                Y_MAX=YLIM[1]
                ylim(Y_MIN,Y_MAX)
            if (IS_D) and (self._IS_SZTYWN):
                #ustawienie proporcjonalnej skali
                POS=get(gca(),'position')
                SIZE=get(gcf(),'size_inches')
                x_=SIZE[0]*POS[2]
                y_=SIZE[1]*POS[3]
                Z_LIM=Z_MAX-Z_MIN
                Y_LIM=Z_LIM*y_/x_
                Y_MIN=-Y_LIM/2.0; Y_MAX=Y_LIM/2.0
                ylim(Y_MIN,Y_MAX)
        ##############################################################################
        #koniec rysowanie poszcz. subplotów

        if SHOW==1:
            show()
        if len(NAZ_PL)>0:
            gcf().set_figsize_inches(FIGSIZE[0],FIGSIZE[1])
            savefig(NAZ_PL,orientation=ORIENT)
        #return FIG
    def rys(self,DANE_RYS,P0=[0,0]):
        """
        funkcja rys(self,P0) rysuje (wyprowadza skrypt acada) wa³ek
        P0 - punkt krañcowy (z=0) wa³ka - punkt wstawienia
        """
        import cad, copy
        x0=P0[0]; y0=P0[1]
        x=copy.deepcopy(x0)
        y=copy.deepcopy(y0)
        
        D=copy.deepcopy(self._D)
        L=copy.deepcopy(self._L_s)
        L0=self._L0
        
        ZAW_SKR=';\r\n;rysunek wa³ka:\r\n'+\
        cad.linia([[x,y-D[0]/2.0],[x,y+D[0]/2.0]])+\
        cad.sly('o',DANE_RYS)+\
        cad.linia([[x-10.0,y],[sum(L)+10.0,y]])+\
        cad.sly('g',DANE_RYS)

        x=x; yd=y-D[0]/2.0; yg=y+D[0]/2.0
        yd2=y-D[1]/2.0; yg2=y+D[1]/2.0
        for i in range(0,len(D)):
            if i<len(D)-1:
                yd2=y0-D[i+1]/2.0; yg2=y0+D[i+1]/2.0
            else:
                yd2=y0-D[i]/2.0; yg2=y0+D[i]/2.0
            yd=y0-D[i]/2.0; yg=y0+D[i]/2.0
            x=x+L[i]
            ZAW_SKR=ZAW_SKR+\
            cad.linia([[x-L[i],yd],[x,yd]])+\
            cad.linia([[x-L[i],yg],[x,yg]])+\
            cad.linia([[x,max([yg,yg2])],[x,min([yd,yd2])]])

        return ZAW_SKR
    def R(self,nr_podp,os=''):
        #zwraca reakcjê podpory nr nr_podp w osi os
        if os=='x':
            RR=[self._Rax,self._Rbx]
        elif os=='y':
            RR=[self._Ray,self._Rby]
        else:
            #to reakcja wypadkowa
            RR=[self._Ra,self._Rb]
        return RR[nr_podp-1]
    def __str__(self):
        #wy¶wietla niektóre informacje
        TEXT='WAL '+str(len(self._Rx))+' PODPOROWY\n'+\
        'REAKCJE PODPOR:\n'+\
        'os X: '
        for i in range(0,len(self._Rx)):
            TEXT=TEXT+' '+str(round(self.R(i+1,'x')))
        TEXT=TEXT+'\nos Y: ' 
        for i in range(0,len(self._Rx)):
            TEXT=TEXT+' '+str(round(self.R(i+1,'y')))
        TEXT=TEXT+'\nwypadkowe: ' 
        for i in range(0,len(self._Rx)):
            TEXT=TEXT+' '+str(round(self.R(i+1)))
        TEXT=TEXT+'\n\nmax. ugiecie: '+str(self.f_max())+' mm'
        TEXT=TEXT+'\ndop. ugiecie: '+str(self.f_dop())+' mm\n'
        return TEXT
    def n_podp(self):
        return len(self._R)
    def doc1(self):
        #generuje text latex pobrany z pliku plik_tex
        import funkcje; str2=funkcje.nicestr
        n_podp=self.n_podp(); Rx=self._Rx; Ry=self._Ry; R=self._R
        rozst=self.rozst_podp()
        OZN_PODP=['a','b','c','d','e','f','g','h','i','j']
        #NAZWA_PLIKU_TEX=plik_tex
        #execfile('/home/lex/programy/exttex.py')+\
        TEXT_R='&Max. strza"lka ugi"ecia: $f_{max}='+str2(self.f_max(),5)+'\\ mm$&\\\\\n'+\
        '&Reakcje podp"or:&\\\\\n &\\[\\begin{array}{lll}\n'
        for i in range(0,n_podp):
            TEXT_R=TEXT_R+\
            'R_{'+OZN_PODP[i]+'x}='+str2(Rx[i],0)+'&'+'R_{'+OZN_PODP[i]+'y}='+str2(Ry[i],0)+'&''R_{'+OZN_PODP[i]+'}='+str2(abs(R[i]),0)+'\\\\'
        TEXT_R=TEXT_R+'\\end{array}\\] &\\\\\n'
        
        #return ZAW_PL_
        return TEXT_R
        

#definicja klasy wal:
class walwp(wal2p):
    """
    klasa przechowyjaca informacje i metody pomocne przy obliczeniach walow wielopodp
    """
    def __init__(self,OBC,L,D,L_s,L0):
        try:
            from matplotlib.matlab import *
        except:
            from pylab import *
        #"""
        #metoda konstruujaca obiekt
        #__init__(self,OBC,L,D,L_D,L0):
        #OBC - lista zaw. slowniki - dla obciazen, oraz napis 'podpora' - jesli ma to byc podpora
        #OBC ma nast. postac:
        #[{'Fx':FX,'Fy':FY,'Mgx':MX,'Mgy':MY,'Ms':MS}, ... ,'podpora', ... ,'podpora', ...]
        #lub:
        #[{'Fx':FX,'Fy':FY,'Fz':Fz,'rx':RX,'ry':RY,'Ms':MS}, ... ,'podpora', ... ,'podpora', ...]
        #wtedy Mgx=Fz*rx i Mgy=Fz*ry;
        #L - odleglosci pomiedzy poszcz. elementami z listy OBC
        #D - ¶rednice kolejnych stopni wa³u
        #L_D - d³ugo¶ci poszcz. stopni wa³u
        #L0 - odl, czo³a wa³u od pierwszego punktu obci±¿enia
        #"""
        self._OBC=OBC; self._L=L; self._D=D; self._L_s=L_s; self._L0=L0
        #stworzenie macierzy zaw. obci±¿enia i wspó³rzêdne z
        Z=[]; Fx=[]; Fy=[]; Mgx=[]; Mgy=[]; Ms=[]; Fz=[]
        PODP=[]; i_PODP=[]
        PODP_s=[]; i_PODP_s=[]
        LL_f=[0]+L; LL_f=cumsum(array(LL_f))+L0
        LL_d=[0]+L_s; LL_d=cumsum(array(LL_d))
        D=D+[D[len(D)-1]]
        #od razu ustawie przedzialy dla obl. sztywn
        Z_s=[]; Fx_s=[]; Fy_s=[]; Mgx_s=[]; Mgy_s=[]; Ms_s=[]; Fz_s=[]; D_s=[]
        i_f=0
        i_d=0
        #ustawienie wielko¶ci:
        KONIEC=0
        #print(L)
        #print(LL_f)
        #print(L_s)
        #print(LL_d)
        while not KONIEC:
            #print(i_f)
            #print(i_d)
            #raw_input()
            #print('co kurwa')
            if (i_f<=len(LL_f)-1) and (i_d<=len(LL_d)-1) and (LL_f[i_f]<=LL_d[i_d]):
                Z.append(LL_f[i_f])
                Z_s.append(LL_f[i_f]); D_s.append(D[i_d-1])
                if (isinstance(OBC[i_f],dict)):
                    #sprawdzenie, czy s³ownik ma wszystkie klucze:
                    if not OBC[i_f].has_key('Fx'):
                        OBC[i_f]['Fx']=0.0
                    if not OBC[i_f].has_key('Fy'):
                        OBC[i_f]['Fy']=0.0
                    if not OBC[i_f].has_key('Fz'):
                        OBC[i_f]['Fz']=0.0
                    if not OBC[i_f].has_key('Ms'):
                        OBC[i_f]['Ms']=0.0
                    if (not OBC[i_f].has_key('rx')) and (not OBC[i_f].has_key('Mgx')):
                        OBC[i_f]['Mgx']=0.0
                        OBC[i_f]['rx']=0.0
                    if (not OBC[i_f].has_key('ry')) and (not OBC[i_f].has_key('Mgy')):
                        OBC[i_f]['Mgy']=0.0
                        OBC[i_f]['ry']=0.0
                    Fx.append(float(OBC[i_f]['Fx'])); Fy.append(float(OBC[i_f]['Fy']))
                    Ms.append(float(OBC[i_f]['Ms']))
                    #momenty gn±ce:
                    if (OBC[i_f].has_key('Mgx')):
                        Mgx.append(float(OBC[i_f]['Mgx']))
                    else:
                        Mgx.append(float(OBC[i_f]['Fz'])*OBC[i_f]['rx']/1000.0)
                    if (OBC[i_f].has_key('Mgy')):
                        Mgy.append(float(OBC[i_f]['Mgy']))
                    else:
                        Mgy.append(float(OBC[i_f]['Fz'])*OBC[i_f]['ry']/1000.0)
                    if OBC[i_f].has_key('Fz'):
                        Fz.append(OBC[i_f]['Fz'])
                    else:
                        Fz.append(0.0)
                elif (isinstance(OBC[i_f],str)):
                    Fx.append(0.0); Fy.append(0.0); Ms.append(0.0); Mgx.append(0.0); Mgy.append(0.0); 
                    Fz.append(0.0)
                    PODP.append(Z[i_f]); i_PODP.append(len(Z)-1)
                    i_PODP_s.append(len(Z_s)-1)
                Fx_s.append(Fx[i_f]); Fy_s.append(Fy[i_f]); Mgx_s.append(Mgx[i_f]); Mgy_s.append(Mgy[i_f])
                Ms_s.append(Ms[i_f])
                i_f=i_f+1
            elif (i_d<len(LL_d)-1):
                Z_s.append(LL_d[i_d])
                Fx_s.append(0.0); Fy_s.append(0.0); Fz_s.append(0.0); Mgx_s.append(0.0); Mgy_s.append(0.0)
                Ms_s.append(0.0)
                D_s.append(D[i_d])
                i_d=i_d+1
            elif (i_d>len(LL_d)-2) and (i_f>len(LL_f)-1):
                KONIEC=1
        #Z_s=Z_s[0:len(Z_s)-1]
        #print(Z)
        #print(Fx)
        #print(Mgx)
        #print(Fz)

        #print(Z_s)
        #print(Fx_s)
        #print(Mgx_s)
        #raw_input()
        #print(D_s)
        #Zmiana wszystkiego na tablice array:
        import copy
        PODP_s=copy.deepcopy(PODP)
        Fx=array(Fx); Fy=array(Fy); Mgx=array(Mgx); Mgy=array(Mgy); Ms=array(Ms); Z=array(Z)
        Fx_s=array(Fx_s); Fy_s=array(Fy_s); Mgx_s=array(Mgx_s); Mgy_s=array(Mgy_s); Ms_s=array(Ms_s); Z_s=array(Z_s)
        PODP=array(PODP); PODP_s=array(PODP_s); i_PODP=array(i_PODP); i_PODP_s=array(i_PODP_s)
        D_s=array(D_s)
        
        #za³atwienie problemu momentu skrêcaj±cego
        #wyszed³em z za³o¿enia, ¿e EMs=0 na ca³ej d³ wa³u, wiêc je¶li ostatni odbiornik momentu nie zeruje ca³o¶ci
        #to jest podmieniany tak, ¿eby j± zerowa³
        #w przypadku wiêcej ni¿ dwóch elementów wtytwarzaj±cych m. trzeba bardzo dok³adnie wprowadzaæ
        #momenty ¿eby nie by³o nieporozumieñ
        if sum(Ms)!=0:
            Ms[len(Ms)-1]=-1.0*sum(Ms[0:len(Ms)-1])

        self._Fx=Fx; self._Fy=Fy; self._Mgx=Mgx; self._Mgy=Mgy; self._Ms=Ms; self._PODP=PODP; self._z_podp=PODP
        self._Fx_s=Fx_s; self._Fy_s=Fy_s; self._Mgx_s=Mgx_s; self._Mgy_s=Mgy_s; self._Ms_s=Ms_s
        self._Fz_s=Fz_s
        self._i_PODP=i_PODP; self._Z=Z; self._Z_s=Z_s
        from copy import deepcopy
        self._Z0=deepcopy(Z)
        #self._za=za; self._zb=zb
        #self._ia=ia; self._ib=ib
        #self._Rax=Rax; self._Ray=Ray; self._Rbx=Rbx; self._Rby=Rby
        #self._Ra=Ra; self._Rb=Rb; 
        self._IS_SZTYWN=1
        self._Fz=Fz
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #teraz ¿mudny proces budowania macierzy potrzebnych do obliczenia reakcji i sta³ych ca³kowania:
        #macierz A (wspó³czynników) sk³ada siê z bloków odpowiadaj±cych ró¿nym równaniom w pionie i ró¿nym zmiennym 
        #(reakcjom i sta³ym ca³kowania) w poziomie, w sumie 5x2 bloków
        #~szczegó³y konstrukcji tych macierzy - Z. II. str. 17-25.
        
        n=2*len(Z_s)+len(PODP) #ilo¶æ równañ:
        n_prz=len(Z_s) #ilo¶æ przedzia³ów
        n1=2*len(Z_s); n2=len(PODP); np=n2; nc=n1

        #zbudowanie macierzy MMx, MMy, BBx, BBy:
        MMx=1.0*cumsum(Fx_s); MMy=1.0*cumsum(Fy_s) #zmieni³em znaki na +
        BBx=1000*cumsum(Mgx_s)-cumsum(Fx_s*Z_s); BBy=1000*cumsum(Mgy_s)-cumsum(Fy_s*Z_s) #zmieni³em znaki przed drugimi sk³adnikami na -
        #self._MMx=MMx; self._MMy=MMy; self._BBx=BBx; self._BBy=BBy
        #zbudowanie macierzy I (mom. bezw³.)
        I_s=(pi*(D_s**4))/64.0
        I=I_s
        self._Ix_s=I; self._Iy_s=I
        #for i in range(0,len(Z_s)):
            
        #________________________________________________
        #1. równania statyki:
        #dwa równania (EMA=0 i EMB=0)
        #macierze A_R1 i A_C1 oraz D1
        
        #1.1 p³aszczyzna x0z
        A_R1_x=zeros([2,np],typecode='f')
        A_C1_x=zeros([2,nc],typecode='f')
        D_1_x=zeros([2,1],typecode='f')
        for i in range(0,np):
            A_R1_x[0,i]=1.0*(PODP[i]-PODP[0])  #zmiana na plus w ramach experymentu z dnia 25.07.05r
            A_R1_x[1,i]=1.0*(PODP[i]-PODP[1])  #zmiana na plus w ramach experymentu z dnia 25.07.05r
        #for i in range(0,len())
        D_1_x[0][0]=1.0*sum(Fx*PODP[0])-sum(Fx*Z)+sum(Mgx)*1000.0 #wszystko w Nmm #przed momentami zmieniono znak na +: z niewiadomych przyczyn tak jest dobrze
        D_1_x[1][0]=1.0*sum(Fx*PODP[1])-sum(Fx*Z)+sum(Mgx)*1000.0  #przed momentami zmieniono znak na +: z niewiadomych przyczyn tak jest dobrze

        #1.2 p³aszczyzna y0z
        A_R1_y=zeros([2,np],typecode='f')
        A_C1_y=zeros([2,nc],typecode='f')
        D_1_y=zeros([2,1],typecode='f')
        for i in range(0,np):
            A_R1_y[0,i]=1.0*(PODP[i]-PODP[0])
            A_R1_y[1,i]=1.0*(PODP[i]-PODP[1])
        #for i in range(0,len())
        D_1_y[0][0]=1.0*sum(Fy*PODP[0])-sum(Fy*Z)+sum(Mgy)*1000.0 #przed momentami zmieniono znak na +: z niewiadomych przyczyn tak jest dobrze
        D_1_y[1][0]=1.0*sum(Fy*PODP[1])-sum(Fy*Z)+sum(Mgy)*1000.0  #przed momentami zmieniono znak na +: z niewiadomych przyczyn tak jest dobrze
        #print(A_R1_x)
        #print(D_1_x)
        #print(A_R1_y)
        #print(D_1_y)
        #________________________________________________

        #2.1 zerowe ugiêcia w podporach na pocz±tku przedzia³ów (podpora jest pierwszym punktem przedzia³u)
        
        #2.1.1 p³aszczyzna ZOX
        A_R21_x=zeros([np,np],typecode='f')
        A_C21_x=zeros([np,nc],typecode='f')
        D_21_x=zeros([np,1],typecode='f')
        
        for i in range(0,np):
            A_R21_x[i,:]=0.5*(PODP[i]**2)*(PODP[i]/3.0-PODP)*(PODP<=PODP[i]) #____zmiana znaku na pocz±tku na + 26.07.05r.
            A_C21_x[i,2*i_PODP_s[i]]=PODP[i]
            A_C21_x[i,2*i_PODP_s[i]+1]=1.0
            D_21_x[i,0]=-1.0*(MMx[i_PODP_s[i]]/6.0*(PODP[i]**3)+BBx[i_PODP_s[i]]/2.0*(PODP[i]**2))

        #2.1.2 p³aszczyzna ZOY
        A_R21_y=zeros([np,np],typecode='f')
        A_C21_y=zeros([np,nc],typecode='f')
        D_21_y=zeros([np,1],typecode='f')
        
        for i in range(0,np):
            A_R21_y[i,:]=0.5*(PODP[i]**2)*(PODP[i]/3.0-PODP)*(PODP<=PODP[i])  #____zmiana znaku na pocz±tku na + 26.07.05r.
            A_C21_y[i,2*i_PODP_s[i]]=PODP[i]
            A_C21_y[i,2*i_PODP_s[i]+1]=1.0
            D_21_y[i,0]=-1.0*(MMy[i_PODP_s[i]]/6.0*(PODP[i]**3)+BBy[i_PODP_s[i]]/2.0*(PODP[i]**2))
        #print('\n')
        #print(A_R21_x)
        #print(D_21_x)
        #print(A_R2_y)
        #print(D_2_y)
        
        #2.2 zerowe ugiêcia w podporach na koñcu przedzia³ów (podpora jest ostatnim punktem przedzia³u)
        
        #2.2.1 p³aszczyzna ZOX
        A_R22_x=zeros([np,np],typecode='f')
        A_C22_x=zeros([np,nc],typecode='f')
        D_22_x=zeros([np,1],typecode='f')
        
        for i in range(0,np):
            A_R22_x[i,:]=0.5*(PODP[i]**2)*(PODP[i]/3.0-PODP)*(PODP<PODP[i])  #____zmiana znaku na pocz±tku na + 26.07.05r.
            A_C22_x[i,2*(i_PODP_s[i]-1)]=PODP[i]
            A_C22_x[i,2*(i_PODP_s[i]-1)+1]=1.0
            D_22_x[i,0]=-1.0*(MMx[i_PODP_s[i]-1]/6.0*(PODP[i]**3)+BBx[i_PODP_s[i]-1]/2.0*(PODP[i]**2))
        
        #2.2.2 p³aszczyzna ZOY
        A_R22_y=zeros([np,np],typecode='f')
        A_C22_y=zeros([np,nc],typecode='f')
        D_22_y=zeros([np,1],typecode='f')
        
        for i in range(0,np):
            A_R22_y[i,:]=0.5*(PODP[i]**2)*(PODP[i]/3.0-PODP)*(PODP<PODP[i])  #____zmiana znaku na pocz±tku na + 26.07.05r.
            A_C22_y[i,2*(i_PODP_s[i]-1)]=PODP[i]
            A_C22_y[i,2*(i_PODP_s[i]-1)+1]=1.0
            D_22_y[i,0]=-1.0*(MMy[i_PODP_s[i]-1]/6.0*(PODP[i]**3)+BBy[i_PODP_s[i]-1]/2.0*(PODP[i]**2))
        
        #3. równo¶æ k±tów obrotu na granicach przedzia³ów:
        
        #3.1 p³aszczyzna ZOX
        A_R3_x=zeros([n_prz-1,np],typecode='f')
        A_C3_x=zeros([n_prz-1,nc],typecode='f')
        D_3_x=zeros([n_prz-1,1],typecode='f')
        
        for i in range(1,n_prz):
            if not i in i_PODP_s:
                A_R3_x[i-1,:]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP)*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>PODP)  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C3_x[i-1,2*(i-1)]=1.0/I[i-1]
                A_C3_x[i-1,2*i]=-1.0/I[i]
                D_3_x[i-1,0]=1.0/I[i]*(0.5*MMx[i]*Z_s[i]**2+BBx[i]*Z_s[i])-1.0/I[i-1]*(0.5*MMx[i-1]*Z_s[i]**2+BBx[i-1]*Z_s[i])
            else:
                for j in range(0,np):
                    if i_PODP_s[j]==i:
                        A_R3_x[i-1,j]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP[j])*(-1.0/I[i])*(Z_s[i]>=PODP[j])  #____zmiana znaku na pocz±tku na + 26.07.05r.
                    else:
                        A_R3_x[i-1,j]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP[j])*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>=PODP[j])  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C3_x[i-1,2*(i-1)]=1.0/I[i-1]
                A_C3_x[i-1,2*i]=-1.0/I[i]
                D_3_x[i-1,0]=1.0/I[i]*(0.5*MMx[i]*Z_s[i]**2+BBx[i]*Z_s[i])-1.0/I[i-1]*(0.5*MMx[i-1]*Z_s[i]**2+BBx[i-1]*Z_s[i])
        
        #3.2 p³aszczyzna ZOY
        A_R3_y=zeros([n_prz-1,np],typecode='f')
        A_C3_y=zeros([n_prz-1,nc],typecode='f')
        D_3_y=zeros([n_prz-1,1],typecode='f')
        
        for i in range(1,n_prz):
            if not i in i_PODP_s:
                A_R3_y[i-1,:]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP)*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>=PODP)  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C3_y[i-1,2*(i-1)]=1.0/I[i-1]
                A_C3_y[i-1,2*i]=-1.0/I[i]
                D_3_y[i-1,0]=1.0/I[i]*(0.5*MMy[i]*Z_s[i]**2+BBy[i]*Z_s[i])-1.0/I[i-1]*(0.5*MMy[i-1]*Z_s[i]**2+BBy[i-1]*Z_s[i])
            else:
                for j in range(0,np):
                    if i_PODP_s[j]==i:
                        A_R3_y[i-1,j]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP[j])*(-1.0/I[i])*(Z_s[i]>=PODP[j])  #____zmiana znaku na pocz±tku na + 26.07.05r.
                    else:
                        A_R3_y[i-1,j]=1.0*Z_s[i]*(0.5*Z_s[i]-PODP[j])*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>=PODP[j])  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C3_y[i-1,2*(i-1)]=1.0/I[i-1]
                A_C3_y[i-1,2*i]=-1.0/I[i]
                D_3_y[i-1,0]=1.0/I[i]*(0.5*MMy[i]*Z_s[i]**2+BBy[i]*Z_s[i])-1.0/I[i-1]*(0.5*MMy[i-1]*Z_s[i]**2+BBy[i-1]*Z_s[i])
        
        #4. równo¶æ ugiêæ na granicach przedzia³ów:
        
        #4.1 p³aszczyzna ZOX
        A_R4_x=zeros([n_prz-1-np,np],typecode='f')
        A_C4_x=zeros([n_prz-1-np,nc],typecode='f')
        D_4_x=zeros([n_prz-1-np,1],typecode='f')
        
        j=0
        for i in range(1,n_prz):
            if sum(i==i_PODP_s)==0:
                A_R4_x[j,:]=0.5*(Z_s[i]**2)*((1/3.0)*Z_s[i]-PODP)*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>PODP)  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C4_x[j,2*(i-1)]=1.0*Z_s[i]/I[i-1]
                A_C4_x[j,2*(i-1)+1]=1.0/I[i-1]
                A_C4_x[j,2*i]=-1.0*Z_s[i]/I[i]
                A_C4_x[j,2*i+1]=-1.0/I[i]
                D_4_x[j,0]=1.0/I[i]*((1.0/6.0)*MMx[i]*Z_s[i]**3+0.5*BBx[i]*Z_s[i]**2)-1.0/I[i-1]*((1.0/6.0)*MMx[i-1]*Z_s[i]**3+0.5*BBx[i-1]*Z_s[i]**2)
                j=j+1
        
        #4.1 p³aszczyzna ZOY
        A_R4_y=zeros([n_prz-1-np,np],typecode='f')
        A_C4_y=zeros([n_prz-1-np,nc],typecode='f')
        D_4_y=zeros([n_prz-1-np,1],typecode='f')
        
        j=0
        for i in range(1,n_prz):
            if sum(i==i_PODP_s)==0:
                A_R4_y[j,:]=0.5*(Z_s[i]**2)*((1/3.0)*Z_s[i]-PODP)*(1.0/I[i-1]-1.0/I[i])*(Z_s[i]>PODP)  #____zmiana znaku na pocz±tku na + 26.07.05r.
                A_C4_y[j,2*(i-1)]=Z_s[i]/I[i-1]
                A_C4_y[j,2*(i-1)+1]=1.0/I[i-1]
                A_C4_y[j,2*i]=-1.0*Z_s[i]/I[i]
                A_C4_y[j,2*i+1]=-1.0/I[i]
                D_4_y[j,0]=1.0/I[i]*((1.0/6.0)*MMy[i]*Z_s[i]**3+0.5*BBy[i]*Z_s[i]**2)-1.0/I[i-1]*((1.0/6.0)*MMy[i-1]*Z_s[i]**3+0.5*BBy[i-1]*Z_s[i]**2)
                j=j+1
                
        #po³±czenie tablic w jedn±:
        #p³. ZOX
        A_1_x=concatenate([A_R1_x,A_C1_x],1)
        A_21_x=concatenate([A_R21_x,A_C21_x],1)
        A_22_x=concatenate([A_R22_x,A_C22_x],1)
        A_3_x=concatenate([A_R3_x,A_C3_x],1)
        A_4_x=concatenate([A_R4_x,A_C4_x],1)
        AAx=concatenate([A_1_x,A_21_x,A_22_x,A_3_x,A_4_x],0)
        DDx=concatenate([D_1_x,D_21_x,D_22_x,D_3_x,D_4_x],0)
        #p³. ZOY
        A_1_y=concatenate([A_R1_y,A_C1_y],1)
        A_21_y=concatenate([A_R21_y,A_C21_y],1)
        A_22_y=concatenate([A_R22_y,A_C22_y],1)
        A_3_y=concatenate([A_R3_y,A_C3_y],1)
        A_4_y=concatenate([A_R4_y,A_C4_y],1)
        AAy=concatenate([A_1_y,A_21_y,A_22_y,A_3_y,A_4_y],0)
        DDy=concatenate([D_1_y,D_21_y,D_22_y,D_3_y,D_4_y],0)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        CRx=matrixmultiply(inverse(AAx),DDx)
        CRy=matrixmultiply(inverse(AAy),DDy)
        #rozdzielenie CR na CC i RR:
        RRx=CRx[0:np,0]; CCx=CRx[np:,0]
        RRy=CRy[0:np,0]; CCy=CRy[np:,0]
        #rozdzielenie CCx i CCy na dwie macierze - sta³ych po pierwszym ca³kowaniu i po drugim ca³kowaniu:
        #print(size(CCx,0))
        #print(size(CCx,1))
        #print(size(CCy,0))
        #print(size(CCy,1))
        
        CC1x=CCx[range(0,2*n_prz-1,2)]; CC2x=CCx[range(1,2*n_prz,2)]
        CC1y=CCy[range(0,2*n_prz-1,2)]; CC2y=CCy[range(1,2*n_prz,2)]

        #ustawienie wielko¶ci Fx_s i Fy_s i Fx i Fy (dodanie do nich wielko¶ci R)
        self._Fx[i_PODP]=RRx; self._Fy[i_PODP]=RRy
        self._Fx_s[i_PODP_s]=RRx; self._Fy_s[i_PODP_s]=RRy
        self._MMx=1.0*cumsum(self._Fx_s); self._MMy=1.0*cumsum(self._Fy_s)
        self._BBx=1000.0*cumsum(self._Mgx_s)-cumsum(self._Fx_s*Z_s)
        self._BBy=1000.0*cumsum(self._Mgy_s)-cumsum(self._Fy_s*Z_s)
        self._Rx=RRx; self._Ry=RRy #reakcje podpór
        self._R=(RRx**2 + RRy**2)**0.5
        #self._MMx=MMx; self._MMy=MMy; self._BBx=BBx; self._BBy=BBy
        #print('\n')
        #print(self._MMx)
        #print(self._BBx)
        #raw_input()
        
        #self._AA1x=AA1x; self._AA2x=AA2x; self._AA3x=AA3x; self._AAx=AAx
        #self._AA1y=AA1y; self._AA2y=AA2y; self._AA3y=AA3y; self._AAy=AAy
        #self._DD1x=DD1x; self._DD2x=DD2x; self._DD3x=DD3x; self._DDx=DDx
        #self._DD1y=DD1y; self._DD2y=DD2y; self._DD3y=DD3y; self._DDy=DDy
        self._Cx=CCx; self._Cy=CCy
        self._C1x=CC1x; self._C2x=CC2x
        self._C1y=CC1y; self._C2y=CC2y
    def R(self,nr_podp,os=''):
        #zwraca reakcjê podpory nr nr_podp w osi os
        if os=='x':
            return self._Rx[nr_podp-1]
        elif os=='y':
            return self._Ry[nr_podp-1]
        else:
            #to reakcja wypadkowa
            return (self.R(nr_podp,'x')**2 + self.R(nr_podp,'y')**2)**0.5


class lozysko(cos_na_wale):
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['lozysko','loz','podp']
        self.__name__='lozysko'
        if not self._dane.has_key('b'):
            self['b']=self['B']
    def sily_w(self):
        return 'podpora'
    def rys(self,DANE_RYS,P0=[0.0,0.0]):
        #rysuje ³o¿ysko w punkcie P0 (¶rodkowym)
        #ta metoda rysuje ³o¿ysko jako kwadracik ze skrzy¿owanymi liniami
        d=self['d_wal']; D=self['D']; B=self['B']
        x0=P0[0]; y0=P0[1]
        import cad
        TEXT=';\r\n;rys. lozyska:\r\n'+\
        cad.sly('g',DANE_RYS)+\
        cad.linia([[x0-B/2.0,y0+d/2.0],[x0-B/2.0,y0+D/2.0],[x0+B/2.0,y0+D/2.0],[x0+B/2.0,y0+d/2.0],[x0-B/2.0,y0+d/2.0]])+\
        cad.linia([[x0-B/2.0,y0-d/2.0],[x0-B/2.0,y0-D/2.0],[x0+B/2.0,y0-D/2.0],[x0+B/2.0,y0-d/2.0],[x0-B/2.0,y0-d/2.0]])+\
        cad.linia([[x0-B/2.0,y0+d/2.0],[x0+B/2.0,y0+D/2.0]])+\
        cad.linia([[x0+B/2.0,y0+d/2.0],[x0-B/2.0,y0+D/2.0]])+\
        cad.linia([[x0-B/2.0,y0-d/2.0],[x0+B/2.0,y0-D/2.0]])+\
        cad.linia([[x0+B/2.0,y0-d/2.0],[x0-B/2.0,y0-D/2.0]])
        return TEXT
    
class loz_kul(lozysko):
    #musi byc tez init:
    #hyba nie musi
    """
    def __init__(self,dane,Pp=0.0,fd=1.2,ft=1.0,V=1.0):
        #metoda dobiera odp. ³o¿ysko z bazy danych dla dane i Pp
        lozysko.__init__(dane)
        self._Pp=Pp
        self._p=3.0
        self._X=0.56 #wg Kurmaz
        self._fd=fd
        self._ft=ft
        self._V=V
    """
    #hyba jednak musi:
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['lozysko','loz','podp']
        self.__name__='lozysko'
        if not self._dane.has_key('b'):
            self['b']=self['B']
        self['p']=3.0
        self['X']=0.56
    def P_p(self):
        if self._dane.has_key('R'):
            return self['R']
        elif self._dane.has_key('Pp'):
            return self['Pp']
        else:
            return 0.0
    def P_w(self):
        return 0.0
    def P(self):
        return self['fd']*self['ft']*self.P_p()*self['V']
    def P_sr(self):
        return self.P()
    def L_n(self):
        return (self['C']/self.P_sr())**self['p']
    def L_h(self):
        return (1000000)*self.L_n() / (60.0*self['n'])
    def baza(self):
        #funkcja zwraca bazê danych dla danego typu lozyska i srednicy walu
        import normy
        d=self['d_wal']
        BAZA=normy.kz_db(d) #odczytanie bazy danych
        return BAZA
    def dob_z_bazy(self):
        #wyszukuje z bazy odp. lozysko
        BAZA=self.baza()
        if self.P_p()==0.0:
            self._dane.update(BAZA[0])
        else:
            for i in range(0,len(BAZA)):
                self._dane.update(BAZA[i])
                #self._C=BAZA[i]['C']
                Lh=self.L_h()
                if Lh>=self['Lh']:
                    #to odp. lozysko, opuszczam petle
                    break
    def not_good(self):
        #zwraca wartosc rozna od zera jesli lozysko nie spelnia wymogow trwalosciowych:
        if self.L_h()<self['Lh']:
            return 1
        else:
            return 0
    def __str__(self):
        TEXT='LOZYSKO KULKOWE ZWYKLE:\n'+\
        self.text_dan(['d','D','B','n','C','Lh'])+\
        'Lh_obl = '+str(self.L_h())+'\n'+\
        'Pp = '+str(self.P_p())+'\n'+\
        'Pw = '+str(self.P_w())+'\n'+\
        'P = '+str(self.P())+'\n'+\
        ('dobre'*int(self.not_good()==0))+('zle'*int(self.not_good()!=0))+'\n'
        return TEXT
    def skosne(self):
        if (isinstance(self,loz_ks)) or (isinstance(self,loz_st)):
            return 1
        else:
            return 0
    def doc(self,plik_tex):
        #Pp=self.P_p(); Pw=self.P_w(); P=self.P(); p=self['p']
        try:
            X=self['X']; Y=self['Y']
        except:
            X=1.0; Y=0.0
        C=self['C']; n=self['n']; Lh=self['Lh']; Lhobl=self.L_h(); Ln=self.L_n()
        fd=self['fd']; ft=self['ft']; V=self['V']
        OZN=self['ozn']; NORMA=self['norma']
        P=self.P(); Pp=self.P_p(); p=self['p']; Pw=self.P_w()
        if isinstance(self,loz_st):
            NAZWA_LOZ='"lo"rysko sto"rkowe'
        elif isinstance(self,loz_ks):
            NAZWA_LOZ='"lo"rysko kulkowe sko"sne'
        elif isinstance(self,loz_kul):
            NAZWA_LOZ='"lo"rysko kulkowe zwyk"le'
        else:
            NAZWA_LOZ=''
        NAZWA_PLIKU_TEX=plik_tex
        #execfile('/home/lex/programy/exttex.py',{'ZAW_PL_'})
        #__import__('exttex',globals())
        execfile('/home/lex/programy/exttex.py')
        import __main__
        #print(__main__.ZAW_PL_)
        #print(exttex.ZAW_PL)
        return __main__.ZAW_PL_
class loz_ks(loz_kul):
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['lozysko','loz','podp']
        self.__name__='lozysko'
        if not self._dane.has_key('b'):
            self['b']=self['B']
        self['p']=10.0/3.0
    def P_p(self):
        if self._dane.has_key('R'):
            return self['R']
        elif self._dane.has_key('Pp'):
            return self['Pp']
        else:
            return 0.0
        #try:
        #    return self['Pp']
        #except:
        #    return 0.0
    def P_w(self):
        try:
            return self['Pw']
        except:
            return 0.0
    def P(self):
        return self['fd']*self['ft'] * (self.P_p()*self['V']*self['X'] + self.P_w()*self['Y'])
    def baza(self):
        #funkcja zwraca bazê danych dla danego typu lozyska i srednicy walu
        import normy
        d=self['d_wal']
        BAZA=normy.ks_db(d) #odczytanie bazy danych
        return BAZA
    def __str__(self):
        TEXT='LOZYSKO KULKOWE SKOSNE:\n'+\
        self.text_dan(['d','D','B','n','C','Lh'])+\
        'Lh_obl = '+str(self.L_h())+'\n'+\
        'Pp = '+str(self.P_p())+'\n'+\
        'Fw = '+str(self['Fw'])+'\n'+\
        'Pw = '+str(self.P_w())+'\n'+\
        'P = '+str(self.P())+'\n'+\
        ('dobre'*int(self.not_good()==0))+('zle'*int(self.not_good()!=0))+'\n'
        return TEXT
class loz_st(loz_ks):
    def baza(self):
        #funkcja zwraca bazê danych dla danego typu lozyska i srednicy walu
        import normy
        d=self['d_wal']
        BAZA=normy.st_db(d) #odczytanie bazy danych
        return BAZA
    def __str__(self):
        TEXT='LOZYSKO STOZKOWE:\n'+\
        self.text_dan(['d','D','B','n','C','Lh'])+\
        'Lh_obl = '+str(self.L_h())+'\n'+\
        'Pp = '+str(self.P_p())+'\n'+\
        'Fw = '+str(self['Fw'])+'\n'+\
        'Pw = '+str(self.P_w())+'\n'+\
        'P = '+str(self.P())+'\n'+\
        ('dobre'*int(self.not_good()==0))+('zle'*int(self.not_good()!=0))+'\n'
        return TEXT

#funkcja obl. pare jednakowych ³o¿ysk:
def lozyska_2sj(DANE_a,DANE_b,obiekty=1,takie_same=1):
    """
    funkcja oblicza pare lozysk dla slowników DANE zaw. odp. dane
    """
    #1. wyci±gniêcie danych ze s³owników DANE:
    Fw=abs(DANE_a['Fw'])
    Ra=DANE_a['R']
    Rb=DANE_b['R']
    da=DANE_a['d_wal']
    db=DANE_b['d_wal']
    Lh=DANE_a['Lh']
    if not DANE_a.has_key('K'):
        DANE_a['K']=1
    if not DANE_a.has_key('uklad'):
        DANE_a['uklad']='X'
    if not DANE_a.has_key('n'):
        print('UWAGA!!! Nie podano prêdko¶ci obrotowej wa³u do obliczeñ ³o¿ysk')
        DANE_a['n']=1500
    if not DANE_a.has_key('rodz'):
        DANE_a['rodz']='auto'
    if not DANE_b.has_key('rodz'):
        DANE_b['rodz']='auto'
    if not DANE_a.has_key('fd'):
        DANE_a['fd']=1.2
    if not DANE_a.has_key('ft'):
        DANE_a['ft']=1.0
    if not DANE_a.has_key('V'):
        DANE_a['V']=1.0
    #if not DANE_a.has_key('jednakowe'):
    #    DANE_a['jednakowe']=1
    K=DANE_a['K']
    UKLAD=DANE_a['uklad']
    n=DANE_a['n']
    RODZ_a=DANE_a['rodz']#w tej funcji zawsze ten sam rodzaj - sko¶ne
    RODZ_b=DANE_b['rodz']# i zawsze jednakowe (a nie zawsze)
    fd=DANE_a['fd']
    ft=DANE_a['ft']
    V=DANE_a['V']
    #JEDNAKOWE=DANE_a['jednakowe']

    d=da
        
    #2. za³adowanie bazy danych ³o¿ysk o odp ¶rednicy:
    import normy
    BAZA_ks_a=normy.ks_db(da)
    BAZA_ks_b=normy.ks_db(db)
    BAZA_st_a=normy.st_db(da)
    BAZA_st_b=normy.st_db(db)

    #3. obliczenia - najpierw dla kulkowych sko¶nych, nastêpnie dla sto¿kowych
    WYN_a={}
    WYN_b={}
    import copy
    KONIEC=0
    for i in range(0,len(BAZA_ks_a)):
      if KONIEC:
        break
      for j2 in range(0,len(BAZA_ks_b)):
        if (takie_same) and (da==db):
            j=copy.deepcopy(i)
        else:
            j=copy.deepcopy(j2)
        e=1.14; p=3.0
        Sa=e*Ra; Sb=e*Rb
        Ppa=Ra; Ppb=Rb
        #ustalwnie obc. wzd³u¿nych:
        if (Sa>Sb) and (Fw>=0):
            Pwa=Sa; Pwb=Sa+Fw
        elif (Sa<Sb) and (Fw>=Sb-Sa):
            Pwa=Sa; Pwb=Sa+Fw
        elif (Sa<Sb) and (Fw<=Sb-Sa):
            Pwa=Sb-Fw; Pwb=Sb
        elif (Sa<Sb) and (Fw>=0):
            Pwa=Sb+Fw; Pwb=Sb
        elif (Sa>Sb) and (Fw>=Sa-Sb):
            Pwa=Sb+Fw; Pwb=Sb
        elif (Sa>Sb) and (Fw<=Sa-Sb):
            Pwa=Sa; Pwb=Sa-Fw
        #ustalenie warto¶ci wspó³czynników X i Y
        if Pwa/(V*Ppa)<=e:
            Xa=1.0; Ya=0.0
        else:
            Xa=0.35; Ya=0.57
        if Pwb/(V*Ppb)<=e:
            Xb=1.0; Yb=0.0
        else:
            Xb=0.35; Yb=0.57
        
        #obliczenie obci±¿enia zastêpczego:
        Pa=(Xa*V*Ppa+Ya*Pwa)*fd*ft
        Pb=(Xb*V*Ppb+Yb*Pwb)*fd*ft
        P=max([Pa,Pb])
        #obliczenie zastêpczego obc. ¶redniego:
        Pasr=(K**(1/p))*Pa
        Pbsr=(K**(1/p))*Pb
        #obliczenie trwa³o¶ci ³o¿yska:
        La=(BAZA_ks_a[i]['C']/Pasr)**p
        Lb=(BAZA_ks_b[j]['C']/Pbsr)**p
        Lahobl=(10**6)*La/(60.0*n)
        Lbhobl=(10**6)*Lb/(60.0*n)
        if min([Lahobl,Lbhobl])>=Lh:
            #to jest w³a¶ciwe ³o¿ysko
            WYN_a=BAZA_ks_a[i]
            WYN_b=BAZA_ks_b[j]
            WYN_a['id']='ks'
            WYN_b['id']='ks'
            WYN_a['R']=Ra
            WYN_b['R']=Rb
            WYN_a['Pp']=Ppa
            WYN_b['Pp']=Ppb
            WYN_a['Pw']=Pwa
            WYN_b['Pw']=Pwb
            WYN_a['P']=Pa
            WYN_b['P']=Pb
            WYN_a['X']=Xa
            WYN_a['Y']=Ya
            WYN_b['X']=Xb
            WYN_b['Y']=Yb
            WYN_a['e']=e
            WYN_b['e']=e
            WYN_a['Psr']=Pasr
            WYN_b['Psr']=Pbsr
            WYN_a['L']=La
            WYN_b['L']=Lb
            WYN_a['Lhobl']=Lahobl
            WYN_b['Lhobl']=Lbhobl
            WYN_a['n']=DANE_a['n']
            WYN_b['n']=DANE_b['n']
            WYN_a['p']=p
            WYN_b['p']=p
            WYN_a['d_wal']=WYN_a['d']
            WYN_b['d_wal']=WYN_b['d']
            WYN_a['Lh']=Lh
            WYN_b['Lh']=Lh
            WYN_a['fd']=fd
            WYN_b['fd']=fd
            WYN_a['ft']=ft
            WYN_b['ft']=ft
            WYN_a['V']=V
            WYN_b['V']=V
            WYN_a['K']=K
            WYN_b['K']=K
            WYN_a['l+']=DANE_a['l+']
            WYN_b['l+']=DANE_b['l+']
            WYN_a['l-']=DANE_a['l-']
            WYN_b['l-']=DANE_b['l-']
            WYN_a['Fw']=DANE_a['Fw']
            WYN_b['Fw']=DANE_b['Fw']
            KONIEC=1
            break
    if (len(WYN_a)==0) or (len(WYN_b)==0):
        KONIEC=0
        for i in range(0,len(BAZA_st_a)):
          if KONIEC:
            break
          for j2 in range(0,len(BAZA_st_b)):
            if (takie_same) and (da==db):
                j=copy.deepcopy(i)
            else:
                j=copy.deepcopy(j2)
            ea=BAZA_st_a[i]['e']
            eb=BAZA_st_b[j]['e']
            p=10.0/3.0
            Sa=ea*Ra; Sb=eb*Rb
            Ppa=Ra; Ppb=Rb
            #ustalwnie obc. wzd³u¿nych:
            if (Sa>Sb) and (Fw>=0):
                Pwa=Sa; Pwb=Sa+Fw
            elif (Sa<Sb) and (Fw>=Sb-Sa):
                Pwa=Sa; Pwb=Sa+Fw
            elif (Sa<Sb) and (Fw<=Sb-Sa):
                Pwa=Sb-Fw; Pwb=Sb
            elif (Sa<Sb) and (Fw>=0):
                Pwa=Sb+Fw; Pwb=Sb
            elif (Sa>Sb) and (Fw>=Sa-Sb):
                Pwa=Sb+Fw; Pwb=Sb
            elif (Sa>Sb) and (Fw<=Sa-Sb):
                Pwa=Sa; Pwb=Sa-Fw
            #ustalenie warto¶ci wspó³czynników X i Y
            if Pwa/(V*Ppa)<=ea:
                Xa=1.0; Ya=0.0
            else:
                Xa=0.4; Ya=BAZA_st_a[i]['Y']
            if Pwb/(V*Ppb)<=eb:
                Xb=1.0; Yb=0.0
            else:
                Xb=0.4; Yb=BAZA_st_b[j]['Y']
            
            #obliczenie obci±¿enia zastêpczego:
            Pa=(Xa*V*Ppa+Ya*Pwa)*fd*ft
            Pb=(Xb*V*Ppb+Yb*Pwb)*fd*ft
            P=max([Pa,Pb])
            #obliczenie zastêpczego obc. ¶redniego:
            Pasr=(K**(1/p))*Pa
            Pbsr=(K**(1/p))*Pb
            #obliczenie trwa³o¶ci ³o¿yska:
            La=(BAZA_st_a[i]['C']/Pasr)**p
            Lb=(BAZA_st_b[j]['C']/Pbsr)**p
            Lahobl=(10**6)*La/(60.0*n)
            Lbhobl=(10**6)*Lb/(60.0*n)
            if min([Lahobl,Lbhobl])>=Lh:
                #to jest w³a¶ciwe ³o¿ysko
                WYN_a=BAZA_st_a[i]
                WYN_b=BAZA_st_b[j]
                WYN_a['id']='st'
                WYN_b['id']='st'
                WYN_a['R']=Ra
                WYN_b['R']=Rb
                WYN_a['Pp']=Ppa
                WYN_b['Pp']=Ppb
                WYN_a['Pw']=Pwa
                WYN_b['Pw']=Pwb
                WYN_a['P']=Pa
                WYN_b['P']=Pb
                WYN_a['X']=Xa
                WYN_a['Y']=Ya
                WYN_b['X']=Xb
                WYN_b['Y']=Yb
                WYN_a['e']=ea
                WYN_b['e']=eb
                WYN_a['Psr']=Pasr
                WYN_b['Psr']=Pbsr
                WYN_a['L']=La
                WYN_b['L']=Lb
                WYN_a['Lhobl']=Lahobl
                WYN_b['Lhobl']=Lbhobl
                WYN_a['n']=DANE_a['n']
                WYN_b['n']=DANE_a['n']
                WYN_a['p']=p
                WYN_b['p']=p
                WYN_a['d_wal']=WYN_a['d']
                WYN_b['d_wal']=WYN_b['d']
                WYN_a['Lh']=Lh
                WYN_b['Lh']=Lh
                WYN_a['fd']=fd
                WYN_b['fd']=fd
                WYN_a['ft']=ft
                WYN_b['ft']=ft
                WYN_a['V']=V
                WYN_b['V']=V
                WYN_a['K']=K
                WYN_b['K']=K
                WYN_a['l+']=DANE_a['l+']
                WYN_b['l+']=DANE_b['l+']
                WYN_a['l-']=DANE_a['l-']
                WYN_b['l-']=DANE_b['l-']
                WYN_a['Fw']=DANE_a['Fw']
                WYN_b['Fw']=DANE_b['Fw']
                KONIEC=1
                break
    #ustalenie wiekszego lozyska:
    #WIEKSZE=int(Pbsr>Pasr)
    import copy
    #if (takie_same) and (WYN_a['d']==WYN_b['d']):
    #    #wyrównanie ³o¿ysk:
    #    if WIEKSZE==0:
    #        WYN_b['']
    #    else:
    #        WYN_a=copy.deepcopy(WYN_b)
    if not obiekty:
        return WYN_a, WYN_b
    else:
        #to zwraca obiekty obu ³o¿ysk:
        if WYN_a['id']=='ks':
            WYN_a=loz_ks(WYN_a)
        elif WYN_a['id']=='st':
            WYN_a=loz_st(WYN_a)
        if WYN_b['id']=='ks':
            WYN_b=loz_ks(WYN_b)
        elif WYN_b['id']=='st':
            WYN_b=loz_st(WYN_b)
        return WYN_a, WYN_b


class sprzeglo(lozysko):
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['sprzeglo']
        self.__name__='sprzeglo'
    def sily_w(self):
        if not self._dane.has_key('Ms'):
            self['Ms']=0.0
        return {'Ms':self['Ms']}
    def geom(self,z,dw,a,h=None,strona='+'):
        #metoda zapisuje informacje o geometrii sprzegla klowego
        #oznaczenia wg. rys. 4.26 str. 163 Z. Osiñski Sprzêg³a i hamulce PWN W-wa 1996 r.
        #z - liczba zêbów
        #h - wysoko¶æ k³a (wzd³ó¿ osi wa³u)
        #dw - ¶rednica wewnêtrzna
        #b - szeroko¶æ podstawy k³a na obwodzie (nie tu, obliczony przez self.b())
        #a - szeroko¶æ w kierunku promieniowym (szeroko¶æ wieñca)
        self._z=z; self._h=h; self._dw=dw; self._a=a
        #ustawienie l+ lub l-
        #self['l'+strona]=self._h+2.0
    def d_z(self):
        #obliczanie ¶rednicy zewnêtrznej
        return self._dw+2.0*self._a
    def d_sr(self):
        #obliczanie ¶rednicy ¶redniej
        return (self._dw+self.d_z())/2.0
    def b(self):
        #metoda oblicza szeroko¶æ podstawy k³a (w kier. obwodowym)
        import math, funkcje
        return funkcje.niceround(math.pi*self.d_sr()/(2.0*self._z),1)
    def mat(self,MAT):
        #metoda ustawia pole _mat obiektu, pole to powinno zawierac klucze (to s³ownik) 'pdop' i 'kg':
        self._mat=MAT
    def F_o(self):
        #obliczanie si³y obwodowej
        return 2.0*abs(self['Ms'])/(self.d_sr()/1000.0) #w N
    def F_op(self):
        #obliczanie si³y obwodowej na wale
        return 2.0*abs(self['Ms'])/(self['d_wal']/1000.0) #w N
    def p(self):
        #metoda oblicza naciski powierzchniowe:
        Fo=self.F_o(); z=self._z; A=self._a*self._h
        return Fo/float(z*A)
    def Sg(self):
        Fo=self.F_o(); z=self._z; h=self._h; b=self.b(); W=h*(b**2)/6.0
        return Fo*h/float(z*W)
    def not_good(self):
        #metoda zwraca 0 jesli sprzeglo spelnia warunki wytrzymalosciowe, 
        #zwraca 1 jesli nie spelnia warunku na naciski
        #zwraca 2 jesli nie spelnia warunku na zginanie
        #zwraca 3 jesli nie spelnia obu warunków
        if (self.p()>self._mat['pdop']) and (self.Sg()>self._mat['kg']):
            return 3
        elif self.p()>self._mat['pdop']:
            return 1
        elif self.Sg()>self._mat['kg']:
            return 2
        else:
            return 0
    def alpha_max(self,mi=0.1,mi_1=None):
        #metoda oblicza maxymalny k±t pochylenia ¶cianki k³a, przy którym sprzêg³o jest samohamowne
        import types
        if isinstance(mi_1,types.NoneType):
            mi_1=mi
        import math
        self._mi=mi
        self._mi_1=mi_1
        TG_AL=mi*(1+ mi_1*self.d_sr()/self['d_wal'] ) / (1-mi*mi_1*self.d_sr()/self['d_wal'])
        return math.atan(TG_AL)
    def ust_alpha(self,mi=0.1,mi_1=None,alpha_max=None):
        #metoda ustawia atrybut _alpha obiektu (na liczbê ca³kowit± w stopniach, ale atrybut jest w rad.)
        import types
        if isinstance(alpha_max,types.NoneType):
            alpha_max=self.alpha_max(mi,mi_1)
        alpha_max=min([alpha_max,self.alpha_max(mi,mi_1)])
        import math
        self._alpha=int(alpha_max*180.0/math.pi)*math.pi/180.0
    #zanim wywo³a siê metodê F_w trzeba nadaæ obiektowi atrybut _alpha
    def F_w(self,czynnosc='zal'):
        WSPOLCZYNNIK=1.0*int(czynnosc in ['zal','wlo','wl',1,1.0])-1.0*int(czynnosc in ['roz','wyl',-1,-1.0])
        import math
        RHO=math.atan(self._mi)
        return self.F_op()*self._mi_1+WSPOLCZYNNIK*self.F_o()*math.tan(self._alpha+WSPOLCZYNNIK*RHO)
    def h_min(self):
        h=self.F_o()/(self._z*self._a*self._mat['pdop'])
        return h
    def h_max(self):
        h=self._mat['kg']*self._a*self.b()**2*self._z/(self.F_o()*6.0)
        return h
    def obl_h(self,hmin_=4.0):
        #metoda oblicza h z warunków za naciski i zginanie dla podanych pozosta³ych danych
        h_min=self.h_min()
        h_max=self.h_max()
        if hmin_<=h_max:
            self._h=max([int(h_min)+1.0,hmin_])
        else:
            self._h=int(h_min)+1.0
    def __str__(self):
        TEXT='SPRZEGLO KLOWE:\n'+\
        'dw = '+str(self._dw)+'\n'+\
        'dz = '+str(self.d_z())+'\n'+\
        'b = '+str(self.b())+'\n'+\
        'h = '+str(self._h)+'\n'+\
        'z = '+str(self._z)+'\n'+\
        'Ms = '+str(self['Ms'])+'\n'+\
        'p = '+str(self.p())+'\n'+\
        'p_dop = '+str(self._mat['pdop'])+'\n'+\
        'Sg = '+str(self.Sg())+'\n'+\
        'kg = '+str(self._mat['kg'])+'\n'+\
        ('dobre'*int(self.not_good()==0))+('zle'*int(self.not_good()!=0))+'\n'
        return TEXT
    def doc(self,plik_tex):
        #generuje text latex pobrany z pliku plik_tex
        dw=self._dw; dz=self.d_z(); a=self._a; b=self.b(); z=self._z
        p=self.p(); pdop=self._mat['pdop']
        Sg=self.Sg(); kg=self._mat['kg']
        Ms=self['Ms']; d_wal=self['d_wal']; Fo=self.F_o(); Fop=self.F_op()
        d_sr=self.d_sr()
        hmin=self.h_min(); hmax=self.h_max(); h=self._h
        import math
        mi=self._mi;
        AL=self._alpha*180.0/math.pi; AL_MAX=self.alpha_max()*180.0/math.pi
        Fw1=self.F_w('zal'); Fw2=self.F_w('wyl')
        RHO=math.atan(self._mi)*180.0/math.pi
        NAZWA_PLIKU_TEX=plik_tex
        execfile('/home/lex/programy/exttex.py')
        import __main__
        return __main__.ZAW_PL_
        
class sprz_podw(sprzeglo):
    #klasa zachowuje informacje o sprzêgle z podwójnym wieñcem (na wale)
    #
    def geom(self,z1,dw1,a1,h1,z2,dw2,a2,h2):
        self.sprz_1=sprzeglo(self._dane)
        self.sprz_2=sprzeglo(self._dane)
        self['l-']=h1+2.0; self['l+']=h2+2.0
        self.sprz_1.geom(z1,dw1,a1,h1)
        self.sprz_2.geom(z2,dw2,a2,h2)
        
        
class czop(lozysko):
    def __init__(self,dane={}):
        self._dane=dane
        self.ustaw_klucze()
        self._ozn_typu=['czop']
        self.__name__='czop'
    def sily_w(self):
        if not self._dane.has_key('Ms'):
            self['Ms']=0.0
        return {'Ms':self['Ms']}
class wpust(sprzeglo):
    def __init__(self,dane={}):
        if isinstance(dane,wpust):
            self._dane=dane._dane
        else:
            self._dane=dane
        self._ozn_typu=['wpust']
        if not self._dane.has_key('odm'):
            self['odm']='A'
        if not self._dane.has_key('z'):
            self['z']=1
        self.__name__='wpust'
    def l_ef(self):
        #zwraca efektywn± d³ugo¶æ wpustu:
        if self._dane.has_key('l_ef'):
            return self['l_ef']
        else:
            return self['l'] - (self['b']*int(self['odm']=='A')) - (0.5*self['b']*int(self['odm']=='AB'))
    def A_p1(self):
        #zwraca pole przekroju bocznego osadzonego w wale (efektywne)
        return self['t1']*self.l_ef()
    def A_p2(self):
        #zwraca pole przekroju bocznego osadzonego w pia¶cie (efektywne)
        return (self['h']-self['t1'])*self.l_ef()
    def A_p(self):
        #zwraca pole przekroju bocznego (przybli¿one)
        return self['h']*self.l_ef()/2.0
    def A_t(self):
        #zwraca pole przekroju dla ¶cinania (efektywne)
        return self['b']*self.l_ef()
    def F(self):
        #zwraca si³ê obwodow±:
        return 2.0*abs(self['Ms'])/(self['d_wal']/1000.0)
    def p_1(self):
        return self.F()/self.A_p1()/self['z']
    def p_2(self):
        return self.F()/self.A_p2()/self['z']
    def p(self):
        return self.F()/self.A_p()/self['z']
    def S_t(self):
        return self.F()/self.A_t()/self['z']
    def mat(self,MAT_1,MAT_2=None):
        #metoda ustawia pole _mat obiektu, pole to powinno zawierac klucze (to s³ownik) 'pdop' i 'kg':
        import types, copy
        if isinstance(MAT_2,types.NoneType):
            MAT_2=copy.deepcopy(MAT_1)
        self._mat_1=MAT_1
        self._mat_2=MAT_2
    def not_good(self):
        #metoda zwraca 0 jesli sprzeglo spelnia warunki wytrzymalosciowe, 
        #zwraca 1 jesli nie spelnia warunku na naciski 1
        #zwraca 2 jesli nie spelnia warunku na ¶cinanie
        #zwraca 3 jesli nie spelnia obu warunków
        if (self.p()>self._mat_1['pdop']) and (self.S_t()>self._mat_1['kt']):
            return 3
        elif (self.p()>self._mat_1['pdop']):
            return 1
        elif self.S_t()>self._mat_1['kt']:
            return 2
        else:
            return 0
    def __str__(self):
        TEXT='WPUST_PRYZM.:\n'+\
        self.text_dan(['l','b','h','t1','t2','Ms','z'])+\
        'p = '+str(self.p())+'\n'+\
        'p_dop = '+str(self._mat_1['pdop'])+'\n'+\
        'St = '+str(self.S_t())+'\n'+\
        'kt = '+str(self._mat_1['kt'])+'\n'+\
        ('dobre'*int(self.not_good()==0))+('zle'*int(self.not_good()!=0))+'\n'
        return TEXT
    def rys(self,DANE_RYS,P0=[0.0,0.0]):
        #rysowanie:
        l=self['l']; l_ef=self.l_ef(); b=self['b']
        x0=P0[0]; y0=P0[1]
        import cad
        TEXT=';\r\n;rys. wpustu:\r\n'+\
        cad.sly('g',DANE_RYS)+\
        cad.linia([[x0-l_ef/2.0,y0+b/2.0],[x0+l_ef/2.0,y0+b/2.0]])+\
        cad.linia([[x0-l_ef/2.0,y0-b/2.0],[x0+l_ef/2.0,y0-b/2.0]])+\
        cad.luk([x0-l_ef/2.0,y0],[x0-l_ef/2.0,y0+b/2.0],[x0-l_ef/2.0,y0-b/2.0])+\
        cad.luk([x0+l_ef/2.0,y0],[x0+l_ef/2.0,y0-b/2.0],[x0+l_ef/2.0,y0+b/2.0])
        return TEXT
    def l_min(self):
        #zwraca minimaln± d³ugo¶æ wpustu (ca³kowit±, nie efektywn±)
        return float( int(2.0*self.F()/(self['z']*self['h']*self._mat_1['pdop'])) +1 )+self['b']
    def ust_l(self):
        self['l']=self.l_min()
    def doc(self,plik_tex):
        #generuje text latex pobrany z pliku plik_tex
        ODM=self['odm']; l=self['l']; l_ef=self.l_ef()
        b=self['b']; h=self['h']; p=self.p(); pdop=self._mat_1['pdop']
        Ms=self['Ms']; d_wal=self['d_wal']; Fo=self.F(); z=self['z']
        NORMA='PN-70/M-85005'
        NAZWA_PLIKU_TEX=plik_tex
        execfile('/home/lex/programy/exttex.py')
        import __main__
        return __main__.ZAW_PL_
        
#klasy bardziej z³o¿one:

##przekl_wp - (przek³adnia wieloprze³o¿eniowa): zestaw przek³adni skrzynki prêdko¶ci

##definicja rodzica wszystkich takich przek³adni:
class przekl_wp:
    def __init__(self):
        self._kupa='kupa'

#konkretne przypadki, oznaczenia klas maj± nastêpuj±ce znaczenie:
#przekl_wp_<n_p>_<n_w>_<typ>
#n_p - ilo¶æ prze³o¿eñ przednich
#n_w - ilo¶æ prze³o¿eñ wstecznych
#typ - typ przek³adni w którym zawieraj± siê jej wszystkie pozosta³e cechy

class przekl_wp_3_1_1(przekl_wp):
    #przek³adnia sk³ada siê z przek³adni zêbatej wstêpnie redukuj±cej, trzech par kó³ zêbatych
    #przek³adni przednich, jednej trójki przek³adni wstecznej
    #wa³ek 1 ma dwa ³o¿yska
    #wa³ek 2 ma 4 ³o¿yska, dwa skrajne sko¶ne w uk³adzie O
    #wa³ek 3 ma 4 ³o¿yska, dwa wewnêtrzne sko¶ne w uk³adzie X
    
    def odl(self,WAL,ELEM,MODE=[0,0]):
        #metoda oblicza odleg³o¶ci na wa³kach WALY
        #miêdzy elementami ELEM=[ELEMENTY_NA_WALE_1, ELEMENTY_NA_WALE_2]
        #zgodnie z MODE=[ ['0'/'-'/'+','0'/'-'/'+'], ['0'/'-'/'+','0'/'-'/'+'] ]
        #   '0' - wyrównanie do ¶rodka czê¶ci g³ównej elementu (o czeroko¶ci b)
        #   '-' - wyrównanie do skraju czê¶ci g³ównej elementu (o czeroko¶ci b) od str. ujemnej osi z
        #   '+' - wyrównanie do skraju czê¶ci g³ównej elementu (o czeroko¶ci b) od str. dodatniej osi z
        
        ##ustalenie d³ugo¶ci elementów na wale 1 i na wale 2:
        #wa³ 1:
        E1=self._elementy[WAL]
        #E2=self._elementy[WALY[1]]
        L_1=0.0#; L_2=0.0
        WITH_B_1={'-':1,'+':-1,'0':0,'+-':0,0:0,'s':0}
        WITH_B_2={'-':-1,'+':1,'0':0,'+-':0,0:0,'s':0}
        L_1_1=E1[ELEM[0]].l_obc('+',WITH_B_1[MODE[0]])
        L_1_2=E1[ELEM[1]].l_obc('-',WITH_B_2[MODE[1]])
        L_1=L_1+L_1_1+L_1_2
        if ELEM[1]-ELEM[0]>1:
            for i in range(ELEM[0]+1,ELEM[1]):
                L_1=L_1+E1[i].l_c()
        return L_1
    def wyr_dl(self,WALY,ELEM,MODE):
        #metoda wyrównuje odleg³o¶ci na wa³kach WALY
        #miêdzy elementami ELEM=[ELEMENTY_NA_WALE_1, ELEMENTY_NA_WALE_2]
        #zgodnie z MODE=[ ['0'/'-'/'+','0'/'-'/'+'], ['0'/'-'/'+','0'/'-'/'+'] ]
        #   '0' - wyrównanie do ¶rodka czê¶ci g³ównej elementu (o czeroko¶ci b)
        #   '-' - wyrównanie do skraju czê¶ci g³ównej elementu (o czeroko¶ci b) od str. ujemnej osi z
        #   '+' - wyrównanie do skraju czê¶ci g³ównej elementu (o czeroko¶ci b) od str. dodatniej osi z
        
        ##ustalenie d³ugo¶ci elementów na wale 1 i na wale 2:
        #wa³ 1:
        E1=self._elementy[WALY[0]]
        E2=self._elementy[WALY[1]]
        L_1=0.0; L_2=0.0
        WITH_B_1={'-':1,'+':-1,'0':0,'+-':0,0:0,'s':0}
        WITH_B_2={'-':-1,'+':1,'0':0,'+-':0,0:0,'s':0}
        L_1_1=E1[ELEM[0][0]].l_obc('+',WITH_B_1[MODE[0][0]])
        L_1_2=E1[ELEM[0][1]].l_obc('-',WITH_B_2[MODE[0][1]])
        L_1=L_1+L_1_1
        if ELEM[0][1]-ELEM[0][0]>1:
            for i in range(ELEM[0][0]+1,ELEM[0][1]):
                L_1=L_1+E1[i].l_c()
                
        L_2_1=E2[ELEM[1][0]].l_obc('+',WITH_B_1[MODE[1][0]])
        L_2_2=E2[ELEM[1][1]].l_obc('-',WITH_B_2[MODE[1][1]])
        L_2=L_2+L_2_1+L_2_2
        if ELEM[1][1]-ELEM[1][0]>1:
            for i in range(ELEM[1][0]+1,ELEM[1][1]):
                L_2=L_2+E2[i].l_c()
        
        ##porównanie tych d³ugo¶ci:
        if L_1>L_2:
            ##to trzeba doprowadziæ, ¿eby L_2 mia³o d³ugo¶æ L_1:
            ##ustalenie stosunków d³ugo¶ci poszczególnych stopni:
            STOSUNKI=[]
            STOSUNKI.append(L_2_1/L_2)
            if ELEM[1][1]-ELEM[1][0]>1:
                for i in range(ELEM[1][0]+1,ELEM[1][1]):
                    STOSUNKI.append(E2[i].l_c()/L_2)
            STOSUNKI.append(L_2_2/L_2)
            #powiêkszenie wszystkich stopni:
            for i in range(0,len(STOSUNKI)):
                if i==0:
                    l_=L_1*STOSUNKI[i]+E2[ELEM[1][0]+i].l_obc('-',WITH_B_1[MODE[1][0]]*-1)
                    E2[ELEM[1][0]+i].powieksz(l_,'+')
                elif i==len(STOSUNKI)-1:
                    l_=L_1*STOSUNKI[i]+E2[ELEM[1][0]+i].l_obc('+',WITH_B_2[MODE[1][0]]*-1)
                    E2[ELEM[1][0]+i].powieksz(l_,'-')
                else:
                    E2[ELEM[1][0]+i].powieksz(L_1*STOSUNKI[i],'')
                
        elif L_2>L_1:
            ##to trzeba doprowadziæ, ¿eby L_1 mia³o d³ugo¶æ L_2:
            ##ustalenie stosunków d³ugo¶ci poszczególnych stopni:
            STOSUNKI=[]
            STOSUNKI.append(L_1_1/L_1)
            if ELEM[0][1]-ELEM[0][0]>1:
                for i in range(ELEM[0][0]+1,ELEM[0][1]):
                    STOSUNKI.append(E1[i].l_c()/L_1)
            STOSUNKI.append(L_1_2/L_1)
            #powiêkszenie wszystkich stopni:
            for i in range(0,len(STOSUNKI)):
                if i==0:
                    E1[ELEM[0][0]+i].powieksz(L_2*STOSUNKI[i],'+')
                elif i==len(STOSUNKI)-1:
                    E1[ELEM[0][0]+i].powieksz(L_2*STOSUNKI[i],'-')
                else:
                    E1[ELEM[1][0]+i].powieksz(L_2*STOSUNKI[i],'')
                
            #ustawienie zmienionych pól:
            for i in range(ELEM[0][0],ELEM[0][1]+1):
                self._elementy[WALY[0]][i]=E1[i]
            for i in range(ELEM[1][0],ELEM[1][1]+1):
                self._elementy[WALY[1]][i]=E2[i]

    def __init__(self,PRZEKL_1_2,PRZEKL_2_3,ELEMENTY_1,ELEMENTY_2,ELEMENTY_3,ELEMENTY_4,MAT_WALOW,aw_1_3=2.0,Lh=9000.0):
        #funkcja konstruuje obiekt dla nast. danych:
        #PRZEKL_1_2 - przek³adnia zêbata miêdzy wa³kiem 1 i 2
        #PRZEKL_2_3 - przek³adnie zêbate miêdzy wa³kami 2 i 3 (lista)
        #ELEMENTY_[1-4] - elementy na wa³ach [1-4] (do nich trzeba bêdzie do³±czyæ ko³a zêbate na odp. pozycjach)
        #   w sk³ad ELEMENTY_[1-4] wchodz± takie rzeczy jak ³o¿yska, sprzêg³a, uszczelnienia itd.
        #aw_1_3 - odleg³o¶c czo³a wa³u 1 od czo³a wa³u 3
        
        ##walimy
        #
        #
        kupa='kupa'
        #znalezienie indeksu biegu wstecznego:
        import copy
        for i in range(0,len(PRZEKL_2_3)):
            if isinstance(PRZEKL_2_3[i],trojka_z):
                IND_WST=copy.deepcopy(i)
                break
        ##wpisanie kó³ zêbatych w listy(ELEMENTY_*):
        ELEMENTY=[ELEMENTY_1,ELEMENTY_2,\
        ELEMENTY_3,\
        ELEMENTY_4]
        KOLA_Z=[\
        [PRZEKL_1_2._kola[1]],\
        [PRZEKL_1_2._kola[2],PRZEKL_2_3[0]._kola[1],PRZEKL_2_3[1]._kola[1],PRZEKL_2_3[2]._kola[1],PRZEKL_2_3[3]._kola[1]],\
        [PRZEKL_2_3[0]._kola[2],PRZEKL_2_3[1]._kola[2],PRZEKL_2_3[2]._kola[2],PRZEKL_2_3[3]._kola[2]],\
        [PRZEKL_2_3[IND_WST]._kola[3]]\
        ]
        IND_KZ=[ [4], [2,4,6,9,11], [1,3,5,7], [2] ]
        WALY_MULTIOBC=[1,2] #wa³y, dla których rozpatruje siê wiele przypadków obci±¿enia
        ZMIANA_KIER=[0,0,1,0] #warto¶ci atrybytów _zmiana_kier do wa³ów
        for i in range(0,len(ELEMENTY)):
            for j in range(0,len(IND_KZ[i])):
                ELEMENTY[i].insert(IND_KZ[i][j],KOLA_Z[i][j])
        
        ELEMENTY_PIERWOTNE=copy.deepcopy(ELEMENTY)
        #_______________________________________________________________________________
        ##wyrównanie d³ugo¶ci miêdzy ko³ami zêbatymi i niektórymi ³o¿yskami:
        #nastêpuj±ce d³ugo¶ci musz± byæ równe (wszystkie potraktujê indywidualnie, bo nie wysz³o mi z metod± wyr_dl()):
        #1. wa³ek 1 i 2:
        L_1=ELEMENTY[0][2].l_obc('+',-1)+ELEMENTY[0][3].l_c()+ELEMENTY[0][4].l_obc('-',0) #od krawêdzi ³o¿yska do ¶rodka ko³a wa³ka 1
        L_2=ELEMENTY[1][1].l_obc('+',-1)+ELEMENTY[1][2].l_obc('-',0)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][2].L_p('-')
            ELEMENTY[1][1]['l+']=round(L_/2.0) #zwiêkszenie odcinka za ³o¿yskiem A
            ELEMENTY[1][2]['l-']=L_-ELEMENTY[1][1]['l+'] #zwiêkszenie odcinka przed ko³em 1
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[0][4].L_p('-')
            ELEMENTY[0][3]['l-']=L_/2.0 #zwiêkszenie lewej strony ko³nie¿a
            ELEMENTY[0][3]['l+']=L_/2.0 #zwiêkszenie prawej strony ko³nie¿a
        #2. wa³ek 1 i 2, ko³a zêbate do przerwy miêdzy wa³ami 1 i 3:
        L_1=ELEMENTY[0][4].l_obc('+',0)+ELEMENTY[0][5].l_c()+aw_1_3/2.0
        L_2=ELEMENTY[1][2].l_obc('+',0)+ELEMENTY[1][3].l_obc('-',0)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][2].L_p('+')-ELEMENTY[1][3].L_p('-')
            ELEMENTY[1][3]['l-']=L_ #zwiêkszenie odcinka przed ³o¿yskiem B
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[0][4].L_p('+')-ELEMENTY[0][5].l_c()-aw_1_3/2.0
            ELEMENTY[0][4]['l+']=L_
        #3. wa³ek 2 i 3, ko³a zêbate od przerwy miêdzy wa³ami 1 i 3:
        L_1=ELEMENTY[2][0].l_c()+ELEMENTY[2][1].l_obc('-',0)+aw_1_3/2.0
        L_2=ELEMENTY[1][3].l_obc('+',0)+ELEMENTY[1][4].l_obc('-',0)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][3].L_p('+')-ELEMENTY[1][4].L_p('-')-ELEMENTY[1][3]['l+']
            ELEMENTY[1][4]['l-']=L_
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[2][0].l_c()-ELEMENTY[2][1].L_p('-')-aw_1_3/2.0
            ELEMENTY[2][1]['l-']=L_
        #4. wa³ek 2 i 3, ko³a zêbate miêdzy którymi dzia³a pierwsze sprzêg³o:
        L_1=ELEMENTY[2][1].l_obc('+',0)+ELEMENTY[2][2].l_obc('-',0)+ELEMENTY[2][3].l_c()
        L_2=ELEMENTY[1][4].l_obc('+',0)+ELEMENTY[1][6].l_obc('-',0)+ELEMENTY[1][5].l_c()
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][4].L_p('+')-ELEMENTY[1][6].L_p('-')-ELEMENTY[1][5]['b']
            ELEMENTY[1][5]['l-']=L_/2.0
            ELEMENTY[1][5]['l+']=L_/2.0
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[2][1].L_p('+')-ELEMENTY[2][3].L_p('-')-ELEMENTY[2][2]['b']
            ELEMENTY[2][2]['l-']=L_/2.0
            ELEMENTY[2][3]['l-']=L_/2.0
        #5. wa³ek 2 i 3, ko³a zêbate 2 i 3 na wa³ku 3:
        L_1=ELEMENTY[2][3].l_obc('+',0)+ELEMENTY[2][5].l_obc('-',0)+ELEMENTY[2][4].l_c()
        L_2=ELEMENTY[1][6].l_obc('+',0)+ELEMENTY[1][9].l_obc('-',0)+ELEMENTY[1][7].l_c()+ELEMENTY[1][8].l_c()
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][6].L_p('+')-ELEMENTY[1][9].L_p('-')-ELEMENTY[1][8]['b']-ELEMENTY[1][7].l_c()
            ELEMENTY[1][8]['l-']=L_/2.0
            ELEMENTY[1][8]['l+']=L_/2.0
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[2][3].L_p('+')-ELEMENTY[2][5].L_p('-')
            ELEMENTY[2][4]['l-']=L_/2.0
            ELEMENTY[2][4]['l+']=L_/2.0
        #6. wa³ek 2 i 3, ko³a zêbate miêdzy którymi dzia³a drugie sprzêg³o:
        L_1=ELEMENTY[2][5].l_obc('+',0)+ELEMENTY[2][7].l_obc('-',0)+ELEMENTY[2][6].l_c()
        L_2=ELEMENTY[1][9].l_obc('+',0)+ELEMENTY[1][11].l_obc('-',0)+ELEMENTY[1][10].l_c()
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][9].L_p('+')-ELEMENTY[1][11].L_p('-')-ELEMENTY[1][10]['b']
            ELEMENTY[1][10]['l-']=L_/2.0
            ELEMENTY[1][10]['l+']=L_/2.0
        elif L_2>L_1:
            #to zwiêkszamy L_1: (tu wprowadzono poprawki)
            L_=L_2-ELEMENTY[2][5].L_p('+')-ELEMENTY[2][7].L_p('-')-ELEMENTY[2][6]['b']
            ELEMENTY[2][5]['l+']=L_/2.0
            ELEMENTY[2][6]['l+']=L_/2.0
        #7. wa³ek 2 i 3, ko³a zêbate skrajne i ³o¿yska skrajne:
        L_1=ELEMENTY[2][7].l_obc('+',0)+ELEMENTY[2][8].l_obc('-',1)
        L_2=ELEMENTY[1][11].l_obc('+',0)+ELEMENTY[1][12].l_obc('-',1)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[1][11].L_p('+')-ELEMENTY[1][12]['b']
            ELEMENTY[1][11]['l+']=L_
        elif L_2>L_1:
            #to zwiêkszamy L_1:
            L_=L_2-ELEMENTY[2][7].L_p('+')-ELEMENTY[2][8]['b']
            ELEMENTY[2][7]['l+']=L_
        #8. wa³ek 3 i 4, ko³a zêbate i ³o¿yska wewnêtrzne:
        L_1=ELEMENTY[2][6].l_obc('+',0)+ELEMENTY[2][7].l_obc('-',0)
        L_2=ELEMENTY[3][0].l_obc('+',0)+ELEMENTY[3][2].l_obc('-',0)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[3][0].L_p('+')-ELEMENTY[3][2].L_p('-')
            ELEMENTY[3][1]['l+']=L_/2.0; ELEMENTY[3][1]['l-']=L_/2.0
        #elif L_2>L_1:
        #    #to zwiêkszamy L_1 ale taki przypadek nie jest mo¿liwy:
        #    L_=L_2-ELEMENTY[2][6].L_p('+')-ELEMENTY[2][7].l_obc('-',0)
        #    ELEMENTY[2][6]['l+']=L_
        #8. wa³ek 3 i 4, ko³a zêbate i ³o¿yska zewnêtrzne:
        L_1=ELEMENTY[2][7].l_obc('+',0)+ELEMENTY[2][8].l_obc('-',1)
        L_2=ELEMENTY[3][2].l_obc('+',0)+ELEMENTY[3][3].l_obc('-',1)
        if L_1>L_2:
            #to zwiêkszamy L_2:
            L_=L_1-ELEMENTY[3][2].L_p('+')-ELEMENTY[3][3].l_obc('-',1)
            ELEMENTY[3][2]['l+']=L_
        #elif L_2>L_1:
        #    #to zwiêkszamy L_1 ale taki przypadek nie jest mo¿liwy:
        #    #L_=L_2-ELEMENTY[2][6].L_p('+')-ELEMENTY[2][7].l_obc('-',0)
        #    #ELEMENTY[2][6]['l+']=L_
        #kurwa ale to d³ugie
        #________________________________________________________________________________
        self._elementy=copy.deepcopy(ELEMENTY)
        self._Lh=Lh
        self._elementy_pierwotne=copy.deepcopy(ELEMENTY_PIERWOTNE)
        self._ind_wst=IND_WST
        
        #listy wspó³pracuj±cych kó³ zêbatych (indeksy odp. w tablicy ELEMENTY)
        EL_PRAC_WAL_1=[0,2,4,5]
        EL_PRAC_WAL_2=[\
        [1,2,3,4,5,8,12],\
        [1,2,3,5,6,8,12],\
        [1,2,3,8,9,10,12],\
        [1,2,3,8,10,11,12]\
        ]
        EL_PRAC_WAL_3=[\
        [0,1,2,6,8,10],\
        [0,2,3,6,8,10],\
        [0,2,5,6,8,10],\
        [0,2,6,7,8,10]\
        ]
        EL_PRAC_WAL_4=[0,2,3]
        EL_PRAC_WALOW=[EL_PRAC_WAL_1,EL_PRAC_WAL_2,EL_PRAC_WAL_3,EL_PRAC_WAL_4]
        
        #ustawienie momentów skrêcaj±cych wa³ów o pojedynczym przypadku:
        ##wa³ 1:
        #Ms_=self.get(1,1,'kolo_z','Ms')
        #self.set(1,1,'czop',{'Ms':Ms_})
        
        ELEMENTY=copy.deepcopy(self._elementy)
        #zbudowanie danych do utworzenia obiektów wa³ów:
        ##Obci±¿enia wa³ków i inne dane do konstruktora klasy walwp:
        OBC_WALOW=[]; L_OBC=[]; D_WALOW=[]; L_D_WALOW=[]; L_0_WALOW=[]
        #zmienne tymczasowe
        l_o=0.0; l_d=0.0
        DANE_DO_WALOW=[]
        SPRZEGLA=[]
        for i in range(0,len(ELEMENTY)):
            D=[]; L_D=[]; d=copy.deepcopy(ELEMENTY[i][0]['d_wal'])
            l_d=0.0
            for j in range(0,len(ELEMENTY[i])+1):
                ELEM=copy.deepcopy(ELEMENTY[i][min([j,len(ELEMENTY[i])-1])])
                #print('')
                if j==len(ELEMENTY[i]):
                    D.append(copy.deepcopy(d)); L_D.append(copy.deepcopy(l_d))
                    #print('if')
                elif ELEM['d_wal']==d:
                    l_d=l_d+ELEM.l_c()
                    #print('elif')
                else:
                    D.append(copy.deepcopy(d)); L_D.append(copy.deepcopy(l_d))
                    l_d=ELEM.l_c(); d=copy.deepcopy(ELEM['d_wal'])
                    #print('else')
                #print(j)
                #print(ELEM)
                #print(d)
                #print(l_d)
                #print(D)
                #print(L_D)
                #raw_input()
            #print(D)
            #print(L_D)
            #raw_input()
            D_WALOW.append(copy.deepcopy(D))
            L_D_WALOW.append(copy.deepcopy(L_D))
            
            #teraz obci±¿enia - tu trochê trudniej
            l_o=0.0; OBC=[]; L_OBC=[];
            #obliczenie l_0:
            if i==1:
                #to z nakrêtk± ³o¿yskow±:
                l_0=ELEMENTY[i][0].l_c()+ELEMENTY[i][1].l_obc('-')
            else:
                l_0=ELEMENTY[i][0].l_obc('-')
            if i in WALY_MULTIOBC:
                for j1 in range(0,len(EL_PRAC_WALOW[i])):
                    l_o=0.0
                    OBC_2=[]; L_OBC_2=[]
                    NR_KZ=0; Ms=0.0
                    for j2 in range(0,len(EL_PRAC_WALOW[i][j1])):
                        #ustawienie momentów skrêcaj±cych:
                        INDEX=EL_PRAC_WALOW[i][j1][j2]
                        #ustalenie numeru w kolejno¶ci ko³a zêbatego:
                        #if isinstance(ELEMENTY[i][INDEX],kolo_z):
                        #    NR_KZ_2=NR_KZ_2+1
                        SILY_W=ELEMENTY[i][INDEX].sily_w()
                        #ustawienie momentów skrêcaj±cych:
                        ##je¶li wa³ 2
                        if i+1==2:
                            NR_KZ=j1+2
                            NR_SPRZ=1*int(NR_KZ in [2,3])+2*int(NR_KZ in [4,5])
                            if j2>1:
                                Ms_=OBC_2[1]['Ms']
                            if (isinstance(ELEMENTY[i][INDEX],kolo_z)) and (INDEX>2):
                                SILY_W['Ms']=0.0
                            elif (INDEX+1==self.index(i+1,NR_SPRZ,'sprzeglo')):
                                SILY_W['Ms']=-1.0*Ms_
                                SPRZEGLA.append(copy.deepcopy(ELEMENTY[i][INDEX]))
                                SPRZEGLA[len(SPRZEGLA)-1]['Ms']=abs(Ms_)
                        elif i+1==3:
                            #je¶li wa³ 3
                            NR_KZ=j1+1
                            #NR_SPRZ=1*int(NR_KZ in [2,3])+2*int(NR_KZ in [4,5])
                            #Ms_=OBC_2[]
                            if (isinstance(ELEMENTY[i][INDEX],kolo_z)):
                                Ms_=SILY_W['Ms']
                            elif (isinstance(ELEMENTY[i][INDEX],czop)):
                                SILY_W['Ms']=-1.0*Ms_
                                
                        OBC_2.append(copy.deepcopy(SILY_W))
                        if j2>0:
                            #obliczenie odleg³o¶ci od poprzedniego elementu pracuj±cego:
                            l_o=self.odl(i,[EL_PRAC_WALOW[i][j1][j2-1],EL_PRAC_WALOW[i][j1][j2]])
                            L_OBC_2.append(l_o)
                        #else: #nie wiem po co to else
                        #IS_KZ=0
                        #if isinstance(ELEMENTY[i][EL_PRAC_WALOW[i][j1][j2]],kolo_z):
                        #    IS_KZ=1
                        #    NR_KZ=NR_KZ+1
                        #    if (NR_KZ==2) and (i==1):
                        #        #dla wa³u 2 (i=1) trzeba zamieniæ Ms na 0 w kole zêbatym i nadaæ sprzêg³u Ms
                        #        OBC_2[j2]['Ms']==0.0
                        #    elif (NR_KZ==1):
                        #        Ms=-1.0*OBC_2[j2]['Ms']
                    #dodanie list do list
                    OBC.append(OBC_2)
                    L_OBC.append(L_OBC_2)
            else:
                for j in range(0,len(EL_PRAC_WALOW[i])):
                    INDEX=EL_PRAC_WALOW[i][j]
                    SILY_W=ELEMENTY[i][EL_PRAC_WALOW[i][j]].sily_w()
                    #ustawienie momentów skrêcaj±cych:
                    NR_KZ=1
                    if i+1==1:
                        if isinstance(ELEMENTY[i][INDEX],kolo_z):
                            OBC[0]['Ms']=-1.0*SILY_W['Ms']
                    elif i+1==4:
                        if isinstance(ELEMENTY[i][INDEX],kolo_z):
                            SILY_W['Ms']=0.0
                    OBC.append(copy.deepcopy(SILY_W))
                    if j>0:
                        #obliczenie odleg³o¶ci od poprzedniego elementu pracuj±cego:
                        l_o=self.odl(i,[EL_PRAC_WALOW[i][j-1],EL_PRAC_WALOW[i][j]])
                        L_OBC.append(l_o)
            #dodanie wszystkich utworzonych danych wej¶ciowych do odp. list:
            DANE_DO_WALOW.append({'obc':OBC,'l_obc':L_OBC,'d':D,'l_d':L_D,'l_0':l_0})
        #print(DANE_DO_WALOW)
        #teraz obilczenie wszystkich wa³ów:
        print('\n')
        print('inicjacja obiektów wa³ów:')
        OBIEKTY_WALOW=[]
        for i in range(0,len(DANE_DO_WALOW)):
            print('')
            print('WAL '+str(i+1)+':')
            if i in WALY_MULTIOBC:
                OBIEKTY_WALOW_2=[]
                for j in range(0,len(DANE_DO_WALOW[i]['obc'])):
                    print('PARA '+str(j+1)+':')
                    DANE=DANE_DO_WALOW[i]
                    #print('')
                    #print(DANE['d'])
                    #print(DANE['l_d'])
                    #raw_input()
                    OBIEKTY_WALOW_2.append(walwp(DANE['obc'][j],DANE['l_obc'][j],DANE['d'],DANE['l_d'],DANE['l_0']))
                    OBIEKTY_WALOW_2[j].mat(MAT_WALOW[i])
                    OBIEKTY_WALOW_2[j]._zmiana_kier=ZMIANA_KIER[i]
                OBIEKTY_WALOW.append(OBIEKTY_WALOW_2)
            else:
                DANE=DANE_DO_WALOW[i]
                #print(DANE)
                #raw_input()
                OBIEKTY_WALOW.append(walwp(DANE['obc'],DANE['l_obc'],DANE['d'],DANE['l_d'],DANE['l_0']))
                OBIEKTY_WALOW[i].mat(MAT_WALOW[i])
                OBIEKTY_WALOW[i]._zmiana_kier=ZMIANA_KIER[i]
                #OBIEKTY_WALOW.append(wal2p(DANE['obc'],DANE['l_obc']))
                #OBIEKTY_WALOW[i].set_d(DANE['d'],DANE['l_d'],DANE['l_0'])
        #zapisanie pól obiektu:
        self._dane_do_walow=DANE_DO_WALOW
        self._waly=OBIEKTY_WALOW
        self._waly_multiobc=WALY_MULTIOBC
        self._przekl_1_2=PRZEKL_1_2
        self._przekl_2_3=PRZEKL_2_3
        self._sprzegla=SPRZEGLA
    def element(self,WAL,NR):
        #metoda zwraca element na wale WAL o numerze NR w kolejno¶ci
        #numery wa³ów s± od 1 (wa³ 1, 2, 3, 4 a nie 0 itd)
        #tak samo numery elementów
        return self._elementy[WAL-1][NR-1]
    def elementy_w(self,WAL):
        return self._elementy[WAL-1]
    def isa(self,WAL,NR,OZN_TYPU):
        #funkcja podaje, czy element numer NR na wale WAL jest typu OZN_TYPU:
        return self._elementy[WAL-1][NR-1].isa(OZN_TYPU)
    def index(self,WAL,NR_W_KOL,TYP):
        #metoda wyszukuje element typu TYP bêd±cy NR_W_KOL elementem tego typu na wale WAL
        #zwraca index ale licz±c od 1
        NR=0
        EL_WALU=self._elementy[WAL-1]
        #print(NR_W_KOL)
        for i in range(0,len(EL_WALU)):
            #print(EL_WALU[i])
            if EL_WALU[i].isa(TYP):
                NR=NR+1
            if NR_W_KOL==NR:
                return i+1
            elif i==len(EL_WALU)-1:
                print('UWAGA!! nie znaleziono elementu '+TYP+' na wale '+str(WAL)+'\nnaci¶nij dowolny klawisz')
                raw_input()
    #def set(self,WAL,NR_W_KOL,TYP,WARTOSCI):
    #    #metoda ustawie warto¶ci elementu TYP kolejno 
    #def sprzeglo()
    def set(self,WAL,NR,TYP,SLOWNIK):
        #metoda ustawia warto¶ci pola _dane elementu na WAL o numerze IND ze s³ownika SLOWNIK
        IND=self.index(WAL,NR,TYP)
        #for i in SLOWNIK.keys():
        if isinstance(SLOWNIK,dict):
            self._elementy[WAL-1][IND-1]._dane.update(SLOWNIK)
        else:
            import copy
            self._elementy[WAL-1][IND-1]=copy.deepcopy(SLOWNIK)
    def get(self,WAL,NR,TYP,KLUCZ):
        #metoda ustawia warto¶ci pola _dane elementu na WAL o numerze IND ze s³ownika SLOWNIK
        IND=self.index(WAL,NR,TYP)
        #for i in SLOWNIK.keys():
        return self._elementy[WAL-1][IND-1][KLUCZ]
    def get_obc(self,WAL,NR,TYP,KLUCZ):
        IND=self.index(WAL,NR,TYP)
        return self._elementy[WAL-1][IND-1].sily_w()[KLUCZ]
    def wal(self,WAL,PRZYP_OBC=1):
        #metoda zwraca obiekt wa³u na wale WAL dla przypadku obci±¿enia PRZYP_OBC
        #numeracja od 1
        if WAL-1 in self._waly_multiobc:
            return self._waly[WAL-1][PRZYP_OBC-1]
        else:
            return self._waly[WAL-1]
    def plot(self,WAL,PRZYP_OBC=1,wielkosci=['fx','fy','f'],tytul=None,show=1,filename='',nr_rys=1,mono=0):
        OB_WALU=self.wal(WAL,PRZYP_OBC)
        import types
        if isinstance(tytul,types.NoneType):
            tytul='wal '+str(WAL)+'('+str(PRZYP_OBC)+')'
        import pylab
        pylab.figure(nr_rys)
        OB_WALU.plot(wielkosci,tytul,show,filename,mono=mono)
    def plot2(self,WAL=2,WIELKOSC='fx',tytul='',show=0,filename='',nr_rys=1,mono=0):
        #metoda plotuje t± sam± wielko¶æ dla wszystkich przypadków obci±¿enia danego wa³u
        #niestety wszystkie kupy musz± byæ opisane od zera:
        #a wcale ¿e nie
        import pylab
        FIG=pylab.figure(nr_rys,figsize=[210.0/25.4,297.0/25.4])
        OBIEKTY_WALOW=self._waly[WAL-1]
        for i in range(0,len(OBIEKTY_WALOW)):
            if (i==0) and (len(tytul)>0):
                LEGENDA=1
            else:
                LEGENDA=0
            pylab.subplot(10*41+i+1)
            OBIEKTY_WALOW[i].plot(WIELKOSC,legenda=LEGENDA,is_subplot=1,mono=mono)
            if (i==0) and (len(tytul)>0):
                pylab.title(tytul)
        #zapisanie rysunku:
        if len(filename)>0:
            pylab.savefig(filename)
        #pokazanie rysunku:
        if show:
            pylab.show()
        return FIG
    def n(self,WAL,przyp_obc=1):
        #metoda zwraca prêdko¶æ obrotow± wa³u WAL dla przyp_obc
        if (WAL<=2) or (WAL==4):
            i=self.index(WAL,1,'kolo_z')
        elif WAL==3:
            i=self.index(WAL,przyp_obc,'kolo_z')
        return self.element(WAL,i)['n']
    def R(self,WAL,nr_loz,nr_obc=1):
        if WAL-1 in self._waly_multiobc:
            return self._waly[WAL-1][nr_obc-1].R(nr_loz)
        else:
            return self._waly[WAL-1].R(nr_loz)
    def F_w(self,WAL,nr_obc=1):
        #zwraca si³ê wzd³u¿n± obc. wa³ dla przyp_obc nr_obc
        if (WAL==1) or (WAL==4):
            #to tylko warto¶æ pojedynczej si³y wzd³u¿nej dla ko³a z 
            i=self.index(WAL,1,'kolo_z')
            KZ=self._elementy[WAL-1][i-1]
            return KZ['Fa']*KZ.kier_Fz()
        elif WAL==2:
            i1=self.index(WAL,1,'kolo_z')
            i2=self.index(WAL,nr_obc+1,'kolo_z')
            KZ1=self._elementy[WAL-1][i1-1]
            KZ2=self._elementy[WAL-1][i2-1]
            return KZ1['Fa']*KZ1.kier_Fz()+KZ2['Fa']*KZ2.kier_Fz()
        elif WAL==3:
            i=self.index(WAL,nr_obc,'kolo_z')
            KZ=self._elementy[WAL-1][i-1]
            return KZ['Fa']*KZ.kier_Fz()
    def M_s(self,WAL,nr_obc=1):
        #zwraca moment skrêcaj±cy wa³ WAL dla przypadku obc. nr_obc
        if (WAL==1) or (WAL==4):
            #to tylko warto¶æ pojedynczego momentu skrêcaj±cego dla czopa 
            i=self.index(WAL,1,'kolo_z')
            KZ=self._elementy[WAL-1][i-1]
            return abs(KZ.M_s())
        elif WAL==2:
            i=self.index(WAL,nr_obc+1,'kolo_z')
            KZ=self._elementy[WAL-1][i-1]
            return abs(KZ.M_s())
        elif WAL==3:
            i=self.index(WAL,nr_obc,'kolo_z')
            KZ=self._elementy[WAL-1][i-1]
            return abs(KZ.M_s())
    def M_smax(self,WAL):
        #zwraca max. moment dla danego wa³u (przydatne przy obl. wpustów)
        if not WAL-1 in self._waly_multiobc:
            return self.M_s(WAL)
        else:
            Ms=[]
            for i in range(1,5):
                Ms.append(self.M_s(WAL,i))
            return max(Ms)
    def obc_loz(self,WAL,nr_loz,fd=1.2,ft=1.0,V=1.0,K=1.0):
        #metoda zwraca reakcje lozyska oraz sily wzdluzne obc. to lozysko i n
        #je¶li wa³ jest z tych wieloobci±¿eniowych to zwraca listê odp. warto¶ci:
        DANE_LOZ_0=self._elementy_pierwotne[WAL-1][self.index(WAL,nr_loz,'lozysko')-1]
        if WAL-1 in self._waly_multiobc:
            DANE=[]
            for i in range(0,4):
                DANE.append({})
                DANE[i].update(DANE_LOZ_0._dane)
                #print(DANE[i])
                #raw_input()
                DANE[i]['R']=abs(self.R(WAL,nr_loz,i+1))
                if WAL==2:
                    DANE[i]['Fw']=abs(self.F_w(WAL,i+1)*int(nr_loz in [1,4]))
                else:
                    DANE[i]['Fw']=abs(self.F_w(WAL,i+1)*int(nr_loz in [2,3]))
                DANE[i]['n']=abs(self.n(WAL,i+1))
                DANE[i]['K']=K
                DANE[i]['fd']=fd
                DANE[i]['ft']=ft
                DANE[i]['V']=V
                DANE[i]['d']=DANE_LOZ_0['d_wal']
                DANE[i]['Lh']=self._Lh
        else:
            DANE={}
            DANE.update(DANE_LOZ_0._dane)
            DANE['R']=abs(self.R(WAL,nr_loz))
            DANE['Fw']=abs(self.F_w(WAL))
            DANE['n']=abs(self.n(WAL))
            DANE['K']=K
            DANE['fd']=fd
            DANE['ft']=ft
            DANE['V']=V
            DANE['Lh']=self._Lh
            DANE['d']=DANE_LOZ_0['d_wal']
        return DANE
    def nowe_loz(self,fd=1.2,ft=1.0,V=1.0,K=1.0):
        #metoda zwraca tablice nowych lozysk dla wszystkich walow
        print('\ngenerowanie lozysk:\n')
        CHECK2=0
        CHECK3=0
        import copy
        ##wa³ 1:
        DANE_a=self.obc_loz(1,1,fd,ft,V,K)
        DANE_b=self.obc_loz(1,2,fd,ft,V,K)
        LOZ_a,LOZ_b=lozyska_2sj(DANE_a,DANE_b)
        LOZYSKA_1=copy.deepcopy([LOZ_a,LOZ_b])
        ##wa³ 2
        DANE_a=self.obc_loz(2,1,fd,ft,V,K)
        DANE_b=self.obc_loz(2,2,fd,ft,V,K)
        DANE_c=self.obc_loz(2,3,fd,ft,V,K)
        DANE_d=self.obc_loz(2,4,fd,ft,V,K)
        for i in range(0,len(DANE_d)):
            LOZ_a_0,LOZ_d_0=lozyska_2sj(DANE_a[i],DANE_d[i])
            LOZ_b_0=loz_kul(DANE_b[i])
            LOZ_b_0.dob_z_bazy()
            LOZ_c_0=loz_kul(DANE_c[i])
            LOZ_c_0.dob_z_bazy()
            if CHECK2:
                #wy¶wietlenie informacji:
                print('\n\n')
                print('informacje o lozyskach na wale 2:\n')
                print('przypadek obc. :'+str(i+1))
                print('lozysko A:\n')
                print(LOZ_a_0)
                print('lozysko B:\n')
                print(LOZ_b_0)
                print('lozysko C:\n')
                print(LOZ_c_0)
                print('lozysko D:\n')
                print(LOZ_d_0)
                print('\n')
                raw_input()

            if i==0:
                LOZ_a=copy.deepcopy(LOZ_a_0)
                LOZ_b=copy.deepcopy(LOZ_b_0)
                LOZ_c=copy.deepcopy(LOZ_c_0)
                LOZ_d=copy.deepcopy(LOZ_d_0)
                continue
            if LOZ_a_0.P()>LOZ_a.P():
                LOZ_a=copy.deepcopy(LOZ_a_0)
            if LOZ_b_0.P()>LOZ_b.P():
                LOZ_b=copy.deepcopy(LOZ_b_0)
            if LOZ_c_0.P()>LOZ_c.P():
                LOZ_c=copy.deepcopy(LOZ_c_0)
            if LOZ_d_0.P()>LOZ_d.P():
                LOZ_d=copy.deepcopy(LOZ_d_0)
        LOZYSKA_2=copy.deepcopy([LOZ_a,LOZ_b,LOZ_c,LOZ_d])
        ##wa³ 3:
        DANE_a=self.obc_loz(3,1,fd,ft,V,K)
        DANE_b=self.obc_loz(3,2,fd,ft,V,K)
        DANE_c=self.obc_loz(3,3,fd,ft,V,K)
        DANE_d=self.obc_loz(3,4,fd,ft,V,K)
        for i in range(0,len(DANE_d)):
            LOZ_b_0,LOZ_c_0=lozyska_2sj(DANE_b[i],DANE_c[i])
            LOZ_a_0=loz_kul(DANE_a[i])
            LOZ_a_0.dob_z_bazy()
            LOZ_d_0=loz_kul(DANE_d[i])
            LOZ_d_0.dob_z_bazy()
            if CHECK3:
                #wy¶wietlenie informacji:
                print('\n\n')
                print('informacje o lozyskach na wale 2:\n')
                print('przypadek obc. :'+str(i+1))
                print('lozysko A:\n')
                print(LOZ_a_0)
                print('lozysko B:\n')
                print(LOZ_b_0)
                print('lozysko C:\n')
                print(LOZ_c_0)
                print('lozysko D:\n')
                print(LOZ_d_0)
                print('\n')
                raw_input()
            if i==0:
                LOZ_a=copy.deepcopy(LOZ_a_0)
                LOZ_b=copy.deepcopy(LOZ_b_0)
                LOZ_c=copy.deepcopy(LOZ_c_0)
                LOZ_d=copy.deepcopy(LOZ_d_0)
                continue
            if LOZ_a_0.P()>LOZ_a.P():
                LOZ_a=copy.deepcopy(LOZ_a_0)
            if LOZ_b_0.P()>LOZ_b.P():
                LOZ_b=copy.deepcopy(LOZ_b_0)
            if LOZ_c_0.P()>LOZ_c.P():
                LOZ_c=copy.deepcopy(LOZ_c_0)
            if LOZ_d_0.P()>LOZ_d.P():
                LOZ_d=copy.deepcopy(LOZ_d_0)
        LOZYSKA_3=copy.deepcopy([LOZ_a,LOZ_b,LOZ_c,LOZ_d])
        ##wa³ 4:
        DANE_a=self.obc_loz(4,1,fd,ft,V,K)
        DANE_b=self.obc_loz(4,2,fd,ft,V,K)
        LOZ_a,LOZ_b=lozyska_2sj(DANE_a,DANE_b)
        LOZYSKA_4=copy.deepcopy([LOZ_a,LOZ_b])
        self._lozyska=copy.deepcopy([LOZYSKA_1,LOZYSKA_2,LOZYSKA_3,LOZYSKA_4])
        #ustawienie ³o¿ysk w tablicy elementów:
        LOZYSKA_=[LOZYSKA_1,LOZYSKA_2,LOZYSKA_3,LOZYSKA_4]
        #for j in range(0,len(LOZYSKA)):
        #    for k in range(0,len(LOZYSKA[j])):
        #        self.set(j+1,k+1,'lozysko',LOZYSKA_[j][k])
        #        #ale to bêdzie trwa³o
        return LOZYSKA_1, LOZYSKA_2, LOZYSKA_3, LOZYSKA_4
    def nowe_sprz(self,z,a,mat):
        #metoda zwraca nowe sprzegla
        print('\ngenerowanie sprzegiel:\n')
        import copy
        STARE_SPRZ=[self._elementy_pierwotne[1][self.index(2,1,'sprzeglo')-1],\
        self._elementy_pierwotne[1][self.index(2,2,'sprzeglo')-1]]
        NOWE_SPRZ=copy.deepcopy(STARE_SPRZ)
        for j in range(0,len(NOWE_SPRZ)):
            NOWE_SPRZ[j].mat(mat)
        STARE_SPRZ_OBC=copy.deepcopy(self._sprzegla)
        for i in range(0,len(STARE_SPRZ_OBC)):
            j=0+1*int(i>1) #indeks w STARE_SPRZ
            dw=STARE_SPRZ[j]['d_wal']+5.0
            Ms=self.element(2,self.index(2,i+2,'kolo_z'))['Ms']
            STRONA='+'*int(i in [0,2]) + '-'*int(i in [1,3])
            STARE_SPRZ_OBC[i]['Ms']=copy.deepcopy(Ms)
            STARE_SPRZ_OBC[i].mat(mat)
            STARE_SPRZ_OBC[i].geom(z,dw,a,strona=STRONA)
            STARE_SPRZ_OBC[i].obl_h()
            STARE_SPRZ_OBC[i].ust_alpha()
            #zmodernizowanie nowych sprzêgie³:
            NOWE_SPRZ[j]['l'+STRONA]=2.0*STARE_SPRZ_OBC[i]._h+4.0
            #NOWE_SPRZ[j].geom(z,dw,a,STRONA)
        self._sprzegla=copy.deepcopy(STARE_SPRZ_OBC)
        return NOWE_SPRZ
    def wpust(self,DANE,NR_WAL,NR_EL,TYP_EL):
        #zwraca pojedynczy wpust na wale nr NR_WAL ustalaj±cy element nr NR_EL typu TYP_EL
        ELEMENT_USTALANY=self._elementy[NR_WAL][self.ind]
    def d_wal(self,WAL,NR_EL,TYP_EL):
        #zwraca ¶rednicê wa³u
        i=self.index(WAL,NR_EL,TYP_EL)
        return self.element(WAL,i)['d_wal']
    def l_wp(self,WAL,NR_EL,TYP_EL):
        #zwraca d³ugo¶æ wpustu
        i=self.index(WAL,NR_EL,TYP_EL)
        ELEMENT=self.element(WAL,i)
        if TYP_EL in ['kolo_z','sprzeglo']:
            return ELEMENT.L_p()
        else:
            return ELEMENT.L_p()-2.0
    def wpusty(self,DANE_WPUSTOW,MAT_WPUSTOW_SP,MAT_WPUSTOW_SUW):
        #funkcja ustawia wpusty na ko³ach zêbatych i sprzêg³ach:
        print('\ngenerowanie wpustów:\n')
        #DANE_WPUSTOW to lista z danymi wpustów dla wszystkich wa³ów (lista list)
        #MAT_WPUSTOW_SP i MAT_WPUSTOW_SUW to materia³ wpustów dla po³ spoczynkowych i suwliwych
        #funkcja ustawia Ms i d_wal dla wpustów
        WPUSTY=[] #lista obiektów wpustów
        ##wa³ 1:
        #dwa wpusty:
        #ustawienie brakuj±cych kluczy
        DANE_WPUSTOW[0][0]['Ms']=self.M_smax(1)
        DANE_WPUSTOW[0][0]['d_wal']=self.d_wal(1,1,'czop')
        DANE_WPUSTOW[0][0]['l']=self.l_wp(1,1,'czop')
        DANE_WPUSTOW[0][1]['Ms']=self.M_smax(1)
        DANE_WPUSTOW[0][1]['d_wal']=self.d_wal(1,1,'kolo_z')
        DANE_WPUSTOW[0][1]['l']=self.l_wp(1,1,'kolo_z')
        #stworzenie wpustów:
        WPUSTY.append([])
        WPUSTY[0].append(wpust(DANE_WPUSTOW[0][0]))
        WPUSTY[0][0].mat(MAT_WPUSTOW_SP)
        WPUSTY[0].append(wpust(DANE_WPUSTOW[0][1]))
        WPUSTY[0][1].mat(MAT_WPUSTOW_SUW)
        ##wa³ 2:
        #cztery wpusty:
        #ustawienie brakuj±cych kluczy
        DANE_WPUSTOW[1][0]['Ms']=self.M_smax(2)
        DANE_WPUSTOW[1][0]['d_wal']=self.d_wal(2,1,'kolo_z')
        DANE_WPUSTOW[1][0]['l']=self.l_wp(2,1,'kolo_z')
        for j in range(0,4):
            DANE_WPUSTOW[1][j+1]['Ms']=self.M_s(2,j+1)
            j2=1*int(j+2<=2) + 2*int(j+2>2) #numer sprzêg³a
            DANE_WPUSTOW[1][j+1]['d_wal']=self.d_wal(2,j2,'sprzeglo')
            DANE_WPUSTOW[1][j+1]['l']=self.l_wp(2,j2,'sprzeglo')
        #stworzenie wpustów:
        WPUSTY.append([])
        for j in range(0,len(DANE_WPUSTOW[1])):
            WPUSTY[1].append(wpust(DANE_WPUSTOW[1][j]))
            if j==0:
                WPUSTY[1][j].mat(MAT_WPUSTOW_SP)
            else:
                WPUSTY[1][j].mat(MAT_WPUSTOW_SUW)
        ##wa³ 3:
        #cztery wpusty:
        #ustawienie brakuj±cych kluczy
        for j in range(0,4):
            DANE_WPUSTOW[2][j]['Ms']=self.M_s(3,j+1)
            DANE_WPUSTOW[2][j]['d_wal']=self.d_wal(3,j+1,'kolo_z')
            DANE_WPUSTOW[2][j]['l']=self.l_wp(3,j+1,'kolo_z')
        DANE_WPUSTOW[2][4]['Ms']=self.M_smax(3)
        DANE_WPUSTOW[2][4]['d_wal']=self.d_wal(3,1,'czop')
        DANE_WPUSTOW[2][4]['l']=self.l_wp(3,1,'czop')
        #stworzenie wpustów:
        WPUSTY.append([])
        for j in range(0,len(DANE_WPUSTOW[2])):
            WPUSTY[2].append(wpust(DANE_WPUSTOW[2][j]))
            WPUSTY[2][j].mat(MAT_WPUSTOW_SP)
        ##wa³ 4:
        #jeden wpust:
        #ustawienie brakuj±cych kluczy
        DANE_WPUSTOW[3][0]['Ms']=self.M_smax(4)
        DANE_WPUSTOW[3][0]['d_wal']=self.d_wal(4,1,'kolo_z')
        DANE_WPUSTOW[3][0]['l']=self.l_wp(4,1,'kolo_z')
        #stworzenie wpustów:
        WPUSTY.append([])
        WPUSTY[3].append(wpust(DANE_WPUSTOW[3][0]))
        WPUSTY[3][0].mat(MAT_WPUSTOW_SP)
        self._wpusty=WPUSTY
    def wsp_el(self,WAL,NR_EL,TYP_EL):
        #zwraca wspó³rzêdne ¶rodka piasty elementu licz±c od czo³a wa³u
        i=self.index(WAL,NR_EL,TYP_EL)
        ODL_OD_POCZ=0.0
        for j in range(1,i):
            ODL_OD_POCZ=ODL_OD_POCZ+self.element(WAL,j).l_c()
        ODL_OD_POCZ=ODL_OD_POCZ+self.element(WAL,i).l_obc('-')
        return ODL_OD_POCZ
    def plik_txt(self,naz_pliku='output.txt'):
        #metoda drukuje do pliku dane elementów
        print('\ngenerowanie pliku tekstowego z wynikami:\n')
        ELEM_DO_PRINT=['kolo_z']
        LOZYSKA=self._lozyska
        SPRZEGLA=self._sprzegla
        WPUSTY=self._wpusty
        WALY=self._waly
        TEXT='ELEMENTY PRZEKLADNI:'+'\n'
        ##ko³a zêbate:
        for i in range(0,len(self._elementy)):
            TEXT=TEXT+\
            '\n'+\
            '--------------------------WAL '+str(i+1)+'------------------------------'
            '\n'
            TEXT=TEXT+'\n\nKOLA ZEBATE:\n'
            for j in range(0,len(self._elementy[i])):
                if self._elementy[i][j].__name__ in ELEM_DO_PRINT:
                    TEXT=TEXT+\
                    '\n'+\
                    self._elementy[i][j].__str__()
            ##³o¿yska:
            TEXT=TEXT+'\n\nLOZYSKA:\n'
            for j in range(0,len(LOZYSKA[i])):
                TEXT=TEXT+\
                '\n'+\
                LOZYSKA[i][j].__str__()
            ##sprzêg³a:
            if i==1:
                TEXT=TEXT+'\n\nSPRZEGLA:\n'
                for j in range(0,len(SPRZEGLA)):
                    TEXT=TEXT+\
                    '\n'+\
                    SPRZEGLA[j].__str__()
            ##wpusty:
            TEXT=TEXT+'\n\nWPUSTY:\n'
            for j in range(0,len(WPUSTY[i])):
                TEXT=TEXT+\
                '\n'+\
                WPUSTY[i][j].__str__()
            #WALY
            TEXT=TEXT+'\n\nPRZYPADKI OBC. WALOW:\n'
            if i in self._waly_multiobc:
                for j in range(0,len(WALY[i])):
                    TEXT=TEXT+'\nPRZYPADEK '+str(j+1)+'\n'+\
                    WALY[i][j].__str__()
            else:
                TEXT=TEXT+\
                WALY[i].__str__()
            
                
        
        PLIK=open(naz_pliku,'w')
        PLIK.write(TEXT)
        PLIK.close()
    def rys(self,nazwa_pliku='doc/skrypty/skrypt_zlo.scr'):
        #zapisuje skrypt acada rysuj±cy szkielet reduktora:
        print('\ngenerowanie skryptu autocada:\n')
        import cad
        DANE_RYS,TEXT=cad.rysinit()
        
        ##WA£ 1 - jego czo³o w punkcie 0,0:
        TEXT=TEXT+\
        self._waly[0].rys(DANE_RYS)
        #pierwszy wpust:
        x=self.wsp_el(1,1,'czop')
        y=0.0
        TEXT=TEXT+\
        self._wpusty[0][0].rys(DANE_RYS,[x,y])
        #drugi wpust i ko³o zêbate:
        x=self.wsp_el(1,1,'kolo_z')
        IND=self.index(1,1,'kolo_z')
        TEXT=TEXT+\
        self._wpusty[0][1].rys(DANE_RYS,[x,y])+\
        self._elementy[0][IND-1].rys(DANE_RYS,[x,y])
        #³o¿yska:
        for i in range(0,2):
            IND=self.index(1,i+1,'lozysko')
            x=self.wsp_el(1,i+1,'lozysko')
            TEXT=TEXT+\
            self._elementy[0][IND-1].rys(DANE_RYS,[x,y])
        
        ##WA£ 2
        #ustalenie wspó³rzêdnej czo³a:
        import copy #kurwa jak ja tego nie lubie
        y=copy.deepcopy(-1.0*self._przekl_1_2['aw'])
        x=self.wsp_el(1,1,'kolo_z')-self.wsp_el(2,1,'kolo_z')
        y_2=copy.deepcopy(y)
        x_2=copy.deepcopy(x)
        TEXT=TEXT+\
        self._waly[1][0].rys(DANE_RYS,[x_2,y_2])
        #³o¿yska:
        for i in range(0,4):
            IND=self.index(2,i+1,'lozysko')
            x=x_2+self.wsp_el(2,i+1,'lozysko')
            TEXT=TEXT+\
            self._elementy[1][IND-1].rys(DANE_RYS,[x,y])
        #ko³a zêbate:
        for i in range(0,5):
            IND=self.index(2,i+1,'kolo_z')
            x=x_2+self.wsp_el(2,i+1,'kolo_z')
            TEXT=TEXT+\
            self._elementy[1][IND-1].rys(DANE_RYS,[x,y])
            if i==0:
                #to rysuje wpust
                TEXT=TEXT+\
                self._wpusty[1][0].rys(DANE_RYS,[x,y])
        #wpusty (pod sprzêg³ami):
        x1=x_2+self.wsp_el(2,1,'sprzeglo')
        x2=x_2+self.wsp_el(2,2,'sprzeglo')
        TEXT=TEXT+\
        self._wpusty[1][1].rys(DANE_RYS,[x1,y])+\
        self._wpusty[1][3].rys(DANE_RYS,[x2,y])
        
        ##WA£ 3
        #ustalenie wspó³rzêdnej czo³a:
        y=copy.deepcopy(-1.0*self._przekl_1_2['aw']+self._przekl_2_3[0]['aw'])
        y_3=copy.deepcopy(y)
        x=self.wsp_el(1,1,'kolo_z')-self.wsp_el(2,1,'kolo_z')+self.wsp_el(2,2,'kolo_z')-self.wsp_el(3,1,'kolo_z')
        x_3=copy.deepcopy(x)
        TEXT=TEXT+\
        self._waly[2][0].rys(DANE_RYS,[x_3,y_3])
        #³o¿yska:
        for i in range(0,4):
            IND=self.index(3,i+1,'lozysko')
            x=x_3+self.wsp_el(3,i+1,'lozysko')
            TEXT=TEXT+\
            self._elementy[2][IND-1].rys(DANE_RYS,[x,y])
        #ko³a zêbate:
        for i in range(0,4):
            IND=self.index(3,i+1,'kolo_z')
            x=x_3+self.wsp_el(3,i+1,'kolo_z')
            TEXT=TEXT+\
            self._elementy[2][IND-1].rys(DANE_RYS,[x,y])+\
            self._wpusty[2][i].rys(DANE_RYS,[x,y])
        #wpust na czopie:
        x=x_3+self.wsp_el(3,1,'czop')
        TEXT=TEXT+\
        self._wpusty[2][4].rys(DANE_RYS,[x,y])

        ##WA£ 4: tu trochê problematic stuff
        import math
        y=y_2+self._przekl_2_3[self._ind_wst]._para_1['aw']*math.cos(self._przekl_2_3[self._ind_wst].alpha(1))
        x=x_3+self.wsp_el(3,self._ind_wst+1,'kolo_z')-self.wsp_el(4,1,'kolo_z')
        y_4=copy.deepcopy(y)
        x_4=copy.deepcopy(x)
        TEXT=TEXT+\
        self._waly[3].rys(DANE_RYS,[x_4,y_4])
        #³o¿yska:
        for i in range(0,2):
            IND=self.index(4,i+1,'lozysko')
            x=x_4+self.wsp_el(4,i+1,'lozysko')
            TEXT=TEXT+\
            self._elementy[3][IND-1].rys(DANE_RYS,[x,y])
        
        IND=self.index(4,1,'kolo_z')
        x=x_4+self.wsp_el(4,1,'kolo_z')
        TEXT=TEXT+\
        self._elementy[3][IND-1].rys(DANE_RYS,[x,y])
        PLIK=open(nazwa_pliku,'w')
        PLIK.write(TEXT)
        PLIK.close()
        return DANE_RYS
    def wsp_wpustow(self,NR_WALU):
        #podaje liste wspolrzednych wszystkich wpustów
        #tablica definiuj±ca pod którymi elementami s± wpusty
        TAB_EL_POD_WPUSTY=[\
        [{'elem':'czop','nr':1},{'elem':'kolo_z','nr':1}],\
        [{'elem':'kolo_z','nr':1},{'elem':'sprzeglo','nr':1},{'elem':'sprzeglo','nr':2}],\
        [{'elem':'kolo_z','nr':1},{'elem':'kolo_z','nr':2},{'elem':'kolo_z','nr':3},{'elem':'kolo_z','nr':4},{'elem':'czop','nr':1}]\
        ]
        TAB_ODP_DLA_WALU=TAB_EL_POD_WPUSTY[NR_WALU-1]
        WSPOLRZEDNE=[]
        for i in range(0,len(TAB_ODP_DLA_WALU)):
            WSPOLRZEDNE.append(self.wsp_el(NR_WALU,TAB_ODP_DLA_WALU[i]['nr'],TAB_ODP_DLA_WALU[i]['elem']))
        return WSPOLRZEDNE
    def rys_wal(self,NR,DANE_RYS={},nazwa_pliku='doc/skrypty/rys_wal.scr'):
        WAL=self._waly[NR-1]
        if NR-1 in self._waly_multiobc:
            WAL=WAL[0]
        import cad
        DANE_RYS,TEXT=cad.rysinit(DANE_RYS)
        TEXT=TEXT+WAL.rys(DANE_RYS)
        #narysowanie wpust"ow:
        WPUSTY=self._wpusty[NR-1]
        WSP_WPUSTOW=self.wsp_wpustow(NR)
        for i in range(0,len(WSP_WPUSTOW)):
            x=WSP_WPUSTOW[i]
            TEXT=TEXT+\
            WPUSTY[i].rys(DANE_RYS,[x,0.0])
        #return TEXT
        PLIK=open(nazwa_pliku,'w')
        PLIK.write(TEXT)
        PLIK.close()
        return DANE_RYS
    def rys_kz(self,NR_WAL,NR_KOL,DANE_RYS={},nazwa_pliku='doc/skrypty/rys_kola.scr'):
        #rysuje wskazane ko"lo z"ebate i umieszcza to w pliku ... ->
        KOLO=self.element(NR_WAL,self.index(NR_WAL,NR_KOL,'kolo_z'))
        import cad
        DANE_RYS,TEXT=cad.rysinit(DANE_RYS)
        TEXT=TEXT+KOLO.rys(DANE_RYS)
        PLIK=open(nazwa_pliku,'w')
        PLIK.write(TEXT)
        PLIK.close()
        return DANE_RYS
    def doc(self):
        #metoda zwraca tekst z kodem latex dla prowadzonych obliczeñ:
        print('\ngenerowanie dokumantacji TEX\n')
        import funkcje ; str2=funkcje.nicestr
        ##LOKALIZACJE PLIKOW ¿ród³owych:
        PLIK_LOZ_KUL='doc/loz_kul_1.tex'
        PLIK_LOZ_SK='doc/loz_skos_1.tex'
        PLIK_WPUST='doc/wpust.tex'
        PLIK_SPRZ_1='doc/sprzegla_1.tex'
        PLIK_SPRZ='doc/sprzegla.tex'
        WSTEP='doc/walki_wstep.tex'
        #numeracja rozdzia³ów:
        NR_ROZDZ=4
        #1. do"l"aczenie wst"epu:
        PLIK=open(WSTEP,'r')
        TEXT=PLIK.read()
        PLIK.close()

        #2. wyniki obliczeñ wa³ów:
        WALY_MULTIOBC=self._waly_multiobc
        WALY=self._waly
        import copy
        for i in range(0,len(WALY)):
            if i in WALY_MULTIOBC:
                MAT_WALO=copy.deepcopy(WALY[i][0]._mat)
            else:
                MAT_WALO=copy.deepcopy(WALY[i]._mat)
                
            TEXT=TEXT+\
            ' & & \\\\\n&\\rozdz{'+str(NR_ROZDZ)+'.'+str(i+1)+' Wa"l '+str(i+1)+'}&\\\\\n'+\
            ' & Materia"l wa"lu: & \\\\\n'+\
            ' & Stal '+MAT_WALO['znak']+' o nast. danych: & \\\\\n'+\
            ' & \\begin{itemize} \n'+\
            '\\item $k_{gj}='+str2(MAT_WALO['kgj'],0)+'\ MPa$ \n'+\
            '\\item $k_{go}='+str2(MAT_WALO['kgo'],0)+'\ MPa$ \n'+\
            '\\item $k_{sj}='+str2(MAT_WALO['ksj'],0)+'\ MPa$ \n'+\
            '\\item $k_{so}='+str2(MAT_WALO['kso'],0)+'\ MPa$ \n'+\
            '\\item $x_{z}='+str2(MAT_WALO['xz'],2)+' $ \n'+\
            '\\end{itemize}& \\\\\n'
            if i in WALY_MULTIOBC:
                TEXT=TEXT+'&Wyst"epuj"a cztery przypadki obci"a"renia:&\\\\\n'+\
                '&Rozstaw podp"or: $l_{podp}='+str(WALY[i][0].rozst_podp())+'\\ mm$&\\\\\n'+\
                '&Dopuszczalne ugi"ecie. : $f_{dop}=0.0003\\cdot l_{podp}='+str2(WALY[i][0].f_dop(),4)+' mm$&\\\\\n'
                for j in range(0,len(WALY[i])):
                    TEXT=TEXT+'&Przypadek '+str(j+1)+'&\\\\\n'+\
                    WALY[i][j].doc1()
            else:
                TEXT=TEXT+\
                '&Rozstaw podp"or: $l_{podp}='+str(WALY[i].rozst_podp())+'\\ mm$&\\\\\n'+\
                '&Dopuszczalne ugi"ecie. : $f_{dop}=0.0003\\cdot l_{podp}='+str2(WALY[i].f_dop(),4)+' mm$&\\\\\n'+\
                WALY[i].doc1()
        
        #3. wyniki obliczeñ ³o¿ysk:
        OZN_LOZ=['A','B','C','D','E','F']
        ILOSCI_LOZYSK=[2,4,4,2]
        ELEMENTY=self._elementy
        LOZYSKA=self._lozyska
        TEXT=TEXT+\
        ' & & \\\\\n'+\
        '&\\rozdz{'+str(NR_ROZDZ+1)+' Obliczenie "lo"rysk.'+'}&\\\\\n'
        for i in range(0,len(ELEMENTY)):
            TEXT=TEXT+\
            ' & & \\\\\n'+\
            '&\\rozdz{'+str(NR_ROZDZ+1)+'.'+str(i+1)+' "Lo"ryska na wale '+str(i+1)+'.'+'}&\\\\\n'
            for j in range(0,ILOSCI_LOZYSK[i]):
                #LOZYSKO=ELEMENTY[i][self.index(i+1,j+1,'lozysko')-1]
                LOZYSKO=LOZYSKA[i][j]
                if LOZYSKO.skosne():
                    TEXT=TEXT+\
                    '&Podpora '+OZN_LOZ[j]+':&\\\\\n'+\
                    LOZYSKO.doc(PLIK_LOZ_SK)
                else:
                    TEXT=TEXT+\
                    '&Podpora '+OZN_LOZ[j]+':&\\\\\n'+\
                    LOZYSKO.doc(PLIK_LOZ_KUL)
        
        #4. wyniki obliczeñ sprzêgie³:
        SPRZEGLA=self._sprzegla
        TEXT=TEXT+\
        ' & & \\\\\n'+\
        '&\\rozdz{'+str(NR_ROZDZ+2)+' Obliczenie sprz"egie"l.'+'}&\\\\\n'
        for i in range(0,len(SPRZEGLA)):
            TEXT=TEXT+\
            ' & & \\\\\n'+\
            '&\\rozdz{'+str(NR_ROZDZ+2)+'.'+str(i+1)+' Sprz"eg"lo '+str(i+1)+'.'+'}&\\\\\n'
            if i==0:
                TEXT=TEXT+SPRZEGLA[i].doc(PLIK_SPRZ_1)
            else:
                TEXT=TEXT+SPRZEGLA[i].doc(PLIK_SPRZ)
        
        #5. wyniki obliczeñ wpustów:
        WPUSTY=self._wpusty
        POD_CZYM=[\
        ['na czopie wej"sciowym','na kole z"ebatym'],\
        ['na kole z"ebatym 1','na sprz"egle 1','na sprz"egle 2','na sprz"egle 3','na sprz"egle 4'],\
        ['na kole z"ebatym 1','na kole z"ebatym 2','na kole z"ebatym 3','na kole z"ebatym 4','na czopie ko"ncowym'],\
        ]
        TEXT=TEXT+\
        ' & & \\\\\n'+\
        '&\\rozdz{'+str(NR_ROZDZ+3)+' Obliczenie wpust"ow.'+'}&\\\\\n'
        for i in range(0,len(WPUSTY)-1):
            TEXT=TEXT+\
            ' & & \\\\\n'+\
            '&\\rozdz{'+str(NR_ROZDZ+3)+'.'+str(i+1)+' Wpusty na wale '+str(i+1)+'.'+'}&\\\\\n'
            for j in range(0,len(WPUSTY[i])):
                TEXT=TEXT+'&Wpust '+POD_CZYM[i][j]+':&\\\\\n'+\
                WPUSTY[i][j].doc(PLIK_WPUST)
        return TEXT
        
#kurwa jak bêdzie dzia³aæ to bêdê w szoku

