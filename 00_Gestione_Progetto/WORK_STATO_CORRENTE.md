# Stato operativo

## Preamplificatore in banda base I/Q · PR #1

Le porte IF dei due SBL-1+ conservano le terminazioni da 49,9 Ω e raggiungono le due sezioni di U115. Il doppio OPA2134PA THT è accoppiato in continua: nessuno zero di trasmissione a 0 Hz, per conservare anche la portante centrata. R158/R161 da 100 Ω e C149/C151 da 4,7 nF filtrano l’ingresso. Il guadagno non invertente è fissato da 2 kΩ e 100 Ω per canale, con 10 nF in parallelo ai resistori di retroazione. Specificare 1% per i resistori e 5% per i condensatori di segnale, verificare l’accoppiamento fra canali. U115 usa il pinout standard del doppio operazionale in DIP-8. TI indica lo specifico OPA2134PA come ACTIVE. [Pagina OEM](https://www.ti.com/product/OPA2134/part-details/OPA2134PA) · [Datasheet](https://www.ti.com/lit/ds/symlink/opa2134.pdf)

Il modello KiCad/RX/preamplificatore_iq.py usa 25 Ω di sorgente equivalente e amplificatore ideale a banda base. Guadagno nominale 21 V/V in continua e 18,77 V/V a 4 kHz. Ai vertici delle tolleranze la differenza fra canali può raggiungere 0,47 dB e 2,74° a 4 kHz. Il modello bianco approssima 10,51 µV RMS in uscita fra 0 e 4 kHz, con rumore tipico dell’operazionale e contributi termici. Esclusi rumore 1/f, spurie, offset dei mixer e interferenze delle alimentazioni. Ai livelli precedentemente stimati (2,29–9,48 µV RMS dai mixer) il segnale vicino alla continua diventa 48–199 µV RMS. Un offset di ingresso di 3,5 mV produce invece 73,5 mV DC in uscita: qualificare azzeramento e dinamica prima del guadagno successivo. Il guadagno asintotico della rete di retroazione tende a uno: resta necessario il filtro anti-alias. Con i mixer pompati verificare anche il carico IF alle frequenze di fuga e l’eventuale rettificazione all’ingresso di U115.

R164 alimenta il ramo positivo da AM_LO_5V. C153 e C154 chiudono localmente i due bypass sul ritorno RF. Il ramo AM_BB_NEG deve ancora ricevere una sorgente negativa filtrata: le uscite AM_I_PRE e AM_Q_PRE sono bipolari. Verificare margine di modo comune, swing, offset, avviamento con una sola rail presente e banda di rumore. Il budget di U114 ora considera come scenario altri 10 mA sul ramo positivo: 1,412 W a 16 V con driver 75 mA e XO 30 mA; la generazione del ramo negativo e gli eventuali carichi in uscita andranno aggiunti. Nessuna prova fisica.

MAIN candidata con 145 impronte THT, tutti i pin precedenti conservati e pin/pad/net confrontati. ERC MAIN 15 errori, inclusi i due pin di alimentazione di U115, FRONT 4. DRC con parità su entrambe: contorno assente, zero pad scollegati e zero discrepanze schema/PCB. Prossimo blocco: chiudere il ramo negativo di U115 con un generatore compatibile con il rumore richiesto, poi dimensionare offset, guadagno successivo e anti-alias.

## Generatore del clock AM a 10,695 MHz · PR #1

Y101, R156/R157 e C147/C148 sono ora nello schema e nella PCB MAIN candidata (131 impronte THT). La configurazione richiesta alla famiglia Abracon ACH è 10,695 MHz, 5 V, opzione R ±25 ppm, uscita HCMOS, abilitazione attiva alta e carico opzionale 50 pF. Nessun codice di ordinazione specifico a questa frequenza è stato verificato in produzione. Il componente resta candidato, con conferma OEM della combinazione, qualifica del foro, dimensioni massime, tolleranze e BOM aperte. Impronta DIP-8 a quattro terminali su griglia 7,62 × 7,62 mm: 1 enable collegato a VDD, 4 massa/case, 5 uscita, 8 alimentazione. L’oscillatore pilota direttamente il driver del solo rivelatore AM tramite R156 da 33 Ω in serie. L’uscita resta separata dal LO del primo mixer della radio.

R157 da 3,3 Ω e i bypass locali 10/100 nF disaccoppiano l’alimentazione del clock da quella del driver. Con carico XO di 30 mA, R157 +1% e rail minimo 4,75 V si ottengono 4,650 V prima delle perdite su rame (minimo OEM 4,5 V). Verificare avviamento, transitori, distorsione del duty, capacità d’ingresso del driver (12 pF effettivi indicati da Microchip), rumore di fase e accoppiamento diretto sul filtro IF. Il modello termico aggiornato per il caso 75 mA driver + 30 mA XO stima 1,311 W su U114 a 16 V e richiede almeno 8,066 V sul bus prima delle perdite di distribuzione. Verificare la corrente massima con l’opzione di carico selezionata. [Oscillatore ACH](https://abracon.com/Oscillators/ACH.pdf) · [Driver Microchip](https://ww1.microchip.com/downloads/en/DeviceDoc/20001423J.pdf)

La tolleranza candidata di ±25 ppm pesa ±267,375 Hz (iniziale e temperatura). Nella finestra simulata del recupero digitale, ±750 Hz, rimangono 482,625 Hz per gli altri errori concordi, compresi sintonia del primo LO, scostamento della stazione e invecchiamento. Il rivelatore I/Q ideale in recupero_portante_am.py è stato esercitato con scarti ±267,375 e ±700 Hz, C/N 0 dB, modulazioni 50/100%, semi 0–2. Nei 24 casi zero salti nella finestra di conteggio e massimo errore RMS 5,47°. Non è una misura di sensibilità né una verifica dell’intera catena analogica.

Netlist precedente preservata sui pin esistenti, pin-pad-net verificati. ERC 13 errori MAIN (il nuovo è Vcc di Y101 dopo il resistore di filtro), 4 FRONT. DRC con parità per entrambe: unico errore contorno assente, zero pad scollegati e zero discrepanze. Prossima attività CAD: dimensionare e integrare il primo stadio di banda base I/Q considerando rumore, componente continua, guadagno e saturazione. La conferma OEM dell’oscillatore e la qualifica termica rimangono aperte.

## Alimentazione del driver LO AM · PR #1

MAIN candidata: 126 impronte THT. U114 genera i 5 V del TC4427AEPA dal bus MAIN_PROTECTED_DC a valle dei due diodi. R153 (4,7 Ω ±1%, obiettivo ≥0,25 W) disaccoppia il ramo con C146 (1 µF THT, non polarizzato, obiettivo ≥35 V) presso il regolatore. C144/C145 restano sul ramo locale. R155 (910 Ω ±1%) assicura almeno 5,16 mA a 4,75 V anche a clock fermo. U114 non carica l’uscita del regolatore logico U102. L’andata passa sul rame anteriore e il ritorno sul posteriore. R154 è il ponticello assiale da 0 Ω fra RX_RF_RETURN e CONTROL_RETURN presso il condensatore di distribuzione C105. Chiude la corrente DC dei circuiti RX alimentati e fissa il riferimento fra i domini. I fronti del driver devono richiudersi anzitutto su C144 e C145. Qualificare la corrente totale del ponticello, i percorsi comuni e l’impedenza del ritorno anche per le sezioni IF. Il tab metallico del TO-220 riferito a massa va considerato nella scelta del fissaggio per evitare un secondo percorso verso il telaio.

Il bilancio in KiCad/RX/alimentazione_lo_am.py usa le condizioni TI (5–1000 mA, 7,5–20 V per 4,75–5,25 V) e 8,5 mA di corrente propria. I casi 9/13,8/16 V sono tensioni ipotetiche sul bus dopo i diodi, senza ripple. A 75 mA di driver, il bus richiede almeno 7,924 V oltre alle cadute su rame e ponticello. A 16 V il regolatore dissipa fino a 1,002 W negli scenari, R153 fino a 38 mW. Il carico reale a 10,695 MHz, la temperatura nel contenitore, gli ingombri termici e il margine in dropout al minimo della forma d’onda devono essere qualificati. R153 non dimensiona la protezione dai corti: sul ramo prima del regolatore servono limitazione e coordinamento energia/tempo delle sorgenti. Restano da verificare spegnimento con capacità cariche, stabilità e accoppiamento del clock nel ricevitore. Il datasheet TI indica il codice LM7805CT/NOPB Active/Production, TO-220 NDE. [Datasheet TI](https://www.ti.com/lit/ds/symlink/lm340.pdf)

Netlist precedente conservata per tutti i pin preesistenti e confronto pin/pad/net sulla MAIN candidata. ERC MAIN 12 errori: la porta VDD del driver ora ha un regolatore reale; rimangono fra gli altri la sorgente a monte del nuovo regolatore e il riferimento elettrico a monte. ERC FRONT 4 errori. Il DRC con parità di entrambe le schede segnala il contorno assente, zero pad scollegati e zero discrepanze schema/PCB. Prossimo blocco: generazione del clock a 10,695 MHz coerente con il piano IF e verifica della sua precisione/deriva rispetto alla banda base.

## Driver LO AM, stato candidato della PR #1

MAIN comprende ora U113, R150–R152 e C144–C145, collegati nello schema e posizionati e instradati sulla PCB (121 impronte THT). Il TC4427AEPA in PDIP-8 converte il futuro clock logico a 10,695 MHz in un’onda rettangolare. R150 da 60,4 Ω in serie e R151 da 196 Ω in derivazione precedono il blocco DC C143 e fissano livello e impedenza. R152 da 10 kΩ porta a zero l’ingresso in assenza di clock. Il canale B ha ingresso a massa e uscita lasciata aperta. I pin 1 e 8 sono NC secondo il datasheet. C144 da 100 nF e C145 da 1 µF chiudono il bypass del ramo locale AM_LO_5V sul ritorno RX_RF_RETURN. Restano da progettare la sorgente del clock, la distribuzione dei 5 V a basso rumore e il ritorno verso il regolatore.

Il modello KiCad/RX/driver_lo_am.py usa il filtro e l’ibrido già in netlist. Ipotesi nominali: 5 V, resistenza di uscita simmetrica 7 Ω, duty cycle 50%, fronti lineari da 8 ns. Risultato: 50,15 Ω, fondamentale a vuoto 4,68 Vpp, potenze I/Q +7,82/+7,21 dBm. Con 4,75–5,25 V, resistenza 4–15 Ω, fronti 4–20 ns e duty 45–55%, gli scenari campionati con passivi nominali danno I +6,12…+8,55 dBm, Q +5,51…+7,94 dBm. Questi intervalli sono ipotesi di sensibilità, non limiti garantiti. Da combinare con tolleranze dei passivi, carichi reali dei mixer e parassiti. Qualificare consumo dinamico, dissipazione, distorsione del duty, emissioni del clock e iniezione nel ricevitore prima del congelamento.

Microchip indica la famiglia TC4427A in produzione e documenta il suffisso EPA, PDIP 8 a passo 2,54 mm, file da 7,62 mm. Pin/pad verificati, stato commerciale del codice specifico da riconfermare alla chiusura BOM. [Pagina OEM](https://www.microchip.com/en-us/product/tc4427a) · [Datasheet e codici d’ordine](https://ww1.microchip.com/downloads/en/DeviceDoc/20001423J.pdf)

Verifica KiCad locale: nessun pad scollegato o errore di parità su entrambe le schede, DRC ancora aperto per entrambi i contorni assenti. ERC MAIN 12 errori, inclusi i due pin di alimentazione del driver, FRONT 4 errori. Prossimo blocco: valutare la generazione del clock dal piano di frequenza e la chiusura del percorso di alimentazione RF. Nessuna prova fisica.

## Filtro e dimensionamento del pilotaggio LO · PR #1

MAIN candidata: 115 impronte THT. C143 interrompe la continua del driver; L110/C141/L111/C142/L112 costituiscono un passa-basso del quinto ordine davanti all’ibrido I/Q. Le induttanze successive sono montate su assi ortogonali. La sorgente attiva a monte di C143 resta aperta. Pin, pad e net precedenti conservati. DRC con parità su MAIN e FRONT: solo contorno mancante, zero pad scollegati; ERC rispettivamente 11 e 4 errori. Il nuovo errore identifica la sorgente LO da integrare.

Il modello nodale in KiCad/RX/pilotaggio_lo_am.py include filtro, anello e terminazioni. Ipotesi: sorgente di Thévenin e mixer da 50 Ω, L ±10%, C di filtro e ibrido ±2%, blocco DC ±5%, terminazione ±1%, Q comune 30/60. Ai 65 536 vertici analizzati, +11,49 dBm disponibili alla fondamentale minimizzano la massima deviazione da +7 dBm sui due mixer; sono 4,75 Vpp sinusoidali a vuoto oppure 2,37 Vpp su carico adattato. Ai mixer si stimano +4,68…+9,32 dBm. Le curve tipiche OEM a +4/+7/+10 dBm sono un riferimento per il confronto; non specificano la prestazione del rivelatore a IF quasi nulla né un massimo assoluto applicabile. [SBL-1+, dati originali](https://www.minicircuits.com/pdfs/SBL-1%2B.pdf)

La scelta dei passivi è candidata. Verificare produzione OEM, Q/SRF, parassiti e accoppiamento fisico. Alle armoniche il modello ideale serve solo a confrontare topologie, perché ignora accoppiamenti diretti, autorisonanze, Q dipendente dalla frequenza e impedenza dei mixer pompati. Prossimo passo: selezionare la sorgente a 10,695 MHz e uno stadio THT compatibile con il livello calcolato, l’alimentazione disponibile, lo spettro e i limiti in corrente, prima del routing attivo.

## Stato precedente · distribuzione LO della ricezione AM

Base canonica verificata `c14cfea15ceb180db34efb6fb73f0257736559a8`. La PR #1 contiene il CAD candidato. MAIN ha 109 impronte THT. L106–L109, C137–C140 e R149 formano un ibrido a elementi concentrati fra AM_LO_DRIVE e gli ingressi LO dei mixer U111/U112. Il quarto ramo termina su 49,9 Ω. Il driver a monte manca ancora. Netlist e PCB preservano le connessioni preesistenti. Il DRC con parità rileva zero pad scollegati e il solo errore di contorno assente. L’ERC MAIN mantiene dieci errori.

Il modello riproducibile in KiCad/RX/ibrido_lo_am.py assume porte resistive da 50 Ω e Q delle induttanze pari a 45. A 10,695 MHz stima −90,12° Q/I e perdite di 3,16 e 3,77 dB. L’ingresso necessario per +7 dBm sul ramo debole è +10,77 dBm. Con L ±10%, C ±2%, R ±1% e Q comune 30 o 60, i 1024 vertici simulati danno da −101,63° a −77,43° e fino a +12,80 dBm richiesti. Il ramo più forte riceve più potenza. Restano da determinare il massimo pilotaggio ammissibile e lo sbilanciamento accettabile, inclusi i carichi reali non lineari, le capacità parassite, l’accoppiamento magnetico e i ritorni sul layout. Valutare selezione o taratura dei passivi prima del congelamento. Famiglia assiale candidata [Fastron MICC](https://fastrongroup.com/product-category/leaded-inductors-fixed-choke-coils/micc/). Produzione OEM del codice definitivo, Q alla frequenza di lavoro e geometria di montaggio ancora da qualificare.

Prossimo blocco RX: dimensionare sorgente e driver a 10,695 MHz e verificare la finestra di pilotaggio di entrambi i mixer.

## Ultima integrazione su main al momento della proposta

Bootstrap operativo a commit 34d1c309c6b1b58e1b32f2193e49a19d2ce8a4c5. Nessuna run Actions per quel commit.

## Modifica candidata

I master nativi MAIN e FRONT contengono i connettori candidati J101/J201 e sei reti locali corrispondenti. Netlist XML esportate da KiCad CLI 9.0.2 e confrontate. Integrata la terminazione resistiva PTT su FRONT e rinominata PTT_SENSE in entrambi i master. Distinti staticamente i livelli di riposo, pressione, corto franco e cavo aperto. ERC eseguito con sei errori a singolo terminale su MAIN e quattro su FRONT. Netlist del ramo PTT verificate. Nessuna impronta, PCB, BOM definitiva, DRC o prova fisica.

La mappa candidata delle 240 frequenze base e del LO nominale è in [KiCad/Sintonia](../KiCad/Sintonia/README.md). Numerazione del Connex ed estensioni ancora da confermare.

Requisito LCD approvato: visualizzare numero di canale, frequenza, SWR, potenza RF e modulazione. Uno o più moduli ammessi, sempre nel rispetto del vincolo THT.

Il ricevitore a finestra PTT è integrato nello schema MAIN candidato con LM2903P. Verificati il pinout nella netlist e le fasce statiche. MAIN conserva 4 reti aperte e 2 errori ERC di alimentazione; FRONT conserva 4 reti aperte. Interblocco e protezione di linea aperti.

Aggiunto U102 con condensatori locali. La rail 5 V candidata pilota il ricevitore PTT. Netlist e associazione dell’impronta U102 verificate. ERC MAIN: quattro reti aperte e due errori a monte sul ramo di alimentazione (ingresso U102 e ritorno). FRONT invariata.

Integrato OR a diodi candidato per le due sorgenti DC del ramo logico. Verificati polarità, connessioni e pad THT; ERC MAIN aggiornato a 8 errori (sei reti aperte, due alimentazioni). Stato FRONT invariato: 4 errori.

MAIN include il primo filtro di ricezione verso il mixer. Netlist verificata per C110–C112 e L101–L102. Risposta ideale e limiti in KiCad/RX. ERC aggiornato a 10 errori MAIN (due nuove porte RX aperte), 4 FRONT nell’ultima verifica. Nessun layout RF o collaudo.

Report ERC e netlist XML dei master al commit 8e668b1a52254d7f210e857b498fed2bcf52372d archiviati in Verifiche/KiCad (KiCad 9.0.2, percorsi sorgente resi relativi). MAIN 10 errori, FRONT 4 errori. Analizzata la bobina candidata 132-13L a 246 nH nel filtro RX; modello e limiti in KiCad/RX. Il CAD rimane al valore preliminare da 240 nH.

Prima conversione RX candidata integrata nel master MAIN. Filtro collegato a U110, SBL-1+ plug-in. Pin RF, LO, IF e ritorni controllati in netlist; aggiornati report ERC e XML MAIN. Dieci errori su MAIN, zero warning. FRONT conserva quattro errori. Porte LO e IF da completare. BOM e impronta del mixer aperte.

MAIN include la terminazione IF a due rami su U110. Reti verificate, XML ed ERC aggiornati, 10 errori MAIN e 4 FRONT nell’ultima verifica. Il pilotaggio LO, il buffer IF e il filtro di canale restano aperti. Risultati dei 16 vertici in KiCad/RX.

REQ-10 e REQ-11 vincolano FRONT e MAIN alla conservazione di tutti i comandi originali e al filtraggio completo. Inventario iniziale e criteri per percorso in REQUISITI.md. Chiudere le differenze di variante prima di congelare pannello e cablaggio.

Filtro IF AM candidato aggiunto al master MAIN, ancora isolato dal mixer. Due sezioni HC-49U, rete di accoppiamento e terminazioni verificate in netlist. MAIN 11 errori ERC, FRONT 4 nell’ultima verifica. Produzione, piedinatura meccanica e risposta reale aperte.

Il ramo candidato AM è collegato al mixer tramite Q101 e la rete di adattamento. Netlist verificata sui sei nodi di segnale e alimentazione del buffer. Modello e risultati in KiCad/RX/buffer_am.py. Report ERC MAIN aggiornato: 10 errori; FRONT 4 nell’ultima verifica. Ritorno RX, selezione dei modi, componenti e comportamento RF reale restano aperti.

Uscita AM trasformata tramite L105/C116/R112 su AM_IF_TERMINATED. Netlist e report MAIN aggiornati, ERC 10 errori. Il modello mostra la sensibilità dell’adattamento alle tolleranze e al Q. La scelta del commutatore di modo e la taratura restano aperte.

REQ-12 e REQ-13 introducono alta sensibilità RX e buona modulazione. Priorità: quantificare perdite e rumore prima del mixer e definire il margine microfono–modulatore per ciascun modo prima del congelamento.

REQ-12: bilancio di rumore preliminare e analisi di sensibilità in KiCad/RX. Nello scenario nominale il percorso passivo dà 14,09 dB di NF, un front-end candidato da 12 dB di guadagno e 2 dB di NF dà 5,70 dB. Ipotesi senza misure. CAD invariato in questo ciclo.

Il vincolo REQ-14 stabilisce la destinazione PCBWay delle due schede nude e il montaggio THT manuale a cura dell'utente.

REQ-12, limite dovuto al solo mixer. Assumendo 1,394 dB di perdite prima del preamplificatore e +1 dBm di compressione tipica all'ingresso SBL-1+, la potenza equivalente all'antenna per un singolo tono in banda è +2,39 dBm in passivo, −3,61 dBm con 6 dB di guadagno e −9,61 dBm con 12 dB. Calcolo: Pantenna = Pmixer + perdite − guadagno. La compressione propria del preamplificatore e il blocco IF possono anticipare il limite. Il J310 InterFET in TO-92 è candidato da caratterizzare per polarizzazione, adattamento, rumore e IIP3. Aperta la conferma OEM di produzione del codice ordinabile. Nessuna modifica al master in base a queste sole stime.

Fonti: [SBL-1+](https://www.minicircuits.com/pdfs/SBL-1+.pdf), [catalogo InterFET](https://interfet.com/oscillators/).

## PCB candidate — prima integrazione del PTT

MAIN contiene U101 e R101–R107, FRONT contiene R201 e R202. I due file nativi derivano da pin e reti delle netlist esportate. Le impronte assiali DIN0207 da 7,62 mm sono candidate per il montaggio manuale, da qualificare sugli MPN definitivi. I 40 segmenti MAIN e il segmento FRONT collegano i pad attualmente presenti. Restano fuori PCB i componenti di filtro e disaccoppiamento, connettori e pulsante. La catena PTT completa e il consenso TX restano aperti.

ERC nativo: MAIN 10 errori, FRONT 4. Netlist: connettività pin/rete invariata. DRC con parità: nessun collegamento aperto tra i pad presenti, contorno assente su entrambe, 37 impronte mancanti MAIN e 2 FRONT. I rapporti KiCad sono in Verifiche/KiCad. Assenti prova fisica e qualifica di fabbricazione.

## Connettori e filtro PTT su PCB candidate

Le PCB includono ora J101 e J201 con impronte candidate JST XH verticali a sei poli, identiche per il cablaggio pin a pin. I pin 5 (CONTROL_RETURN) e 6 (PTT_SENSE) raggiungono il circuito PTT su entrambe le schede. I pin 1–4 attendono gli endpoint interni. Su MAIN sono posizionati e collegati anche C101 (10 nF, filtro del segnale) e C102 (100 nF, disaccoppiamento U101). Le due impronte radiali da 2,50 mm e i connettori richiedono qualifica meccanica e di produzione. Prima di fissare il cablaggio verificare corrente FRONT, sezione fili, contatti, verso del pin 1 alle due estremità e spazio di estrazione. SW201 e il consenso TX restano aperti.

Confronto delle due netlist esportate: corrispondenza dei sei pin e connessioni elettriche invariate. Verificati tutti i pad presenti contro le netlist. MAIN ha 11 impronte e FRONT 3. DRC con parità: zero pad scollegati fra quelli presenti, assenti entrambi i contorni, mancanti 34 impronte MAIN e 1 FRONT. ERC nativo: 10 errori MAIN, 4 FRONT. Nessun ordine o prova fisica.

## Ingresso PTT dal microfono

SW201 è stato sostituito in FRONT da J202 per il contatto esterno. R202 passa sul lato segnale. I quattro componenti del master FRONT attuale sono posizionati e collegati. DRC con parità: zero pad scollegati, zero difformità, contorno assente. ERC: quattro reti di alimentazione/dati aperte. Dettagli su tensioni, corto nel microfono e limiti del collegamento in KiCad/INTERFACCIA_MAIN_FRONT.md. Prossima integrazione: interfaccia microfonica audio e gestione della richiesta PTT all'avvio.

## Rilevamento del rilascio PTT su MAIN

Aggiunti e collegati nello schema e sulla PCB U103, R120–R123 e C121. MAIN ospita 17 impronte. Confrontata la netlist precedente e verificati pin/pad/reti. Calcolo statico del rilascio e dei guasti in KiCad/INTERFACCIA_MAIN_FRONT.md. ERC MAIN: 10 errori. DRC con parità: zero pad scollegati tra le impronte presenti, manca il contorno e restano 34 impronte del master da trasferire. La memoria di armamento al rilascio e il reset per alimentazione insufficiente restano da progettare.

## Alimentazione locale della logica su PCB MAIN

Sette impronte aggiunte e collegate: selezione a diodi delle sorgenti DC del ramo logico, regolatore e capacità locali, precarico R124. MAIN ha 24 impronte THT. ERC: 10 errori. DRC con parità: nessun pad scollegato tra quelli presenti, contorno assente e 28 impronte mancanti rispetto allo schema. Dimensionamento e limiti del precarico in KiCad/INTERFACCIA_MAIN_FRONT.md. Restano aperti distribuzione e protezioni a monte, verifica termica e supervisore di reset con memoria di armamento.

## Supervisione del rail logico su MAIN

U104, C122 e R125 integrati e sbrogliati. Il simbolo di progetto di U104 segue la piedinatura MCP102 indicata nella tabella OEM. Controllati pad/reti e preservate tutte le connessioni precedenti. MAIN ha 27 impronte; ERC 10 errori, DRC con parità: contorno assente, zero pad scollegati e 28 impronte mancanti. Prossimo passo dell’interblocco: usare LOGIC_RESET_N per azzerare la memoria e consentire l’armamento solo dopo un rilascio stabile successivo. Vedere KiCad/INTERFACCIA_MAIN_FRONT.md per limiti di qualifica.

## Memoria di rilascio dopo il reset

U105, R126, C123, C124 e R127 integrati su schema e PCB MAIN. 32 impronte THT presenti. Nessun pad scollegato tra quelli presenti; contorno e 28 impronte del master mancanti. ERC MAIN: 10 errori. Il modello nominale basato sulla netlist verifica accensione con tasto premuto, rilascio, mantenimento e reset. Prossimo passo: verificare rimbalzi ripetuti e casi di guasto prima di progettare la qualificazione finale della richiesta. PTT_ARMED non pilota il trasmettitore.

## Correzione del filtro di rilascio PTT

Rilevato armamento spurio nel modello con impulsi ripetuti; integrati e sbrogliati D103 e R128 sulla MAIN candidata. Lo scenario di regressione è riprodotto e respinto dopo la modifica su 64 combinazioni. MAIN ha 34 impronte. ERC: 10 errori; DRC con parità: zero pad scollegati fra quelli presenti, contorno assente e 28 impronte mancanti. L’interblocco resta candidato. Proseguire con il percorso RF/IF del ricevitore mentre rimangono aperte qualifica fisica e gestione dei guasti PTT.

## Buffer della media frequenza AM su PCB MAIN

Trasferiti e collegati Q101, R113–R117 e C117–C120. L’emettitore pilota C120 e R117 verso la rete di adattamento del filtro. R113 alimenta il collettore tramite la rete locale di disaccoppiamento. Confermati corrispondenza pin/pad/net e montaggio passante di tutte le 44 impronte presenti. La netlist del master conserva tutte le connessioni precedenti. Per il candidato 2N3904BU è stato usato il TO-92 in linea, con emettitore, base e collettore ai pad 1, 2 e 3. Restano da confermare produzione OEM del codice e dimensioni definitive dei passivi. [Datasheet onsemi](https://www.onsemi.com/download/data-sheet/pdf/pzt3904-d.pdf).

Il modello già presente in KiCad/RX/buffer_am.py, rieseguito a 10,695 MHz, restituisce Re(Zout) 48,50–52,30 Ω nelle condizioni esaminate, con ritorno RF ideale. Il rame non comprende ancora la terminazione IF a monte né L104 a valle. RX_RF_RETURN collega i componenti locali; resta da progettare il percorso DC di ritorno alla sorgente e da controllare l’impedenza RF del ritorno reale. Il buffer non è alimentabile nello stato attuale. ERC MAIN: 10 errori. DRC con parità: zero pad scollegati fra quelli presenti, contorno assente e 18 impronte del master mancanti. Prossimo blocco: terminazione del mixer e collegamento a C119, con scelta dell’induttore e verifica di Q e autorisonanza alla IF.

## Terminazione IF del mixer sulla MAIN candidata

L103, C113, R110 e R111 sono posizionati e collegati a C119 e al ritorno RF locale. L103 alimenta il ramo utile e C113/R111 terminano il ramo complementare. La PCB ha 48 impronte THT. Verificati pad e net delle impronte presenti e identità di tutte le connessioni schematiche rispetto alla revisione precedente. ERC MAIN: 10 errori. DRC con parità: contorno assente, zero pad scollegati tra quelli presenti, 14 impronte dello schema mancanti. U110 è ancora solo nello schema.

Per L103 il candidato Fastron SMCC-R39K-02 ha valore 390 nH ±10%, Q minimo 45 a 25,2 MHz, SRF minima 230 MHz e DCR massima 0,13 Ω. Impronta assiale candidata specifica della serie a passo 12,70 mm. Confermare lo stato di produzione del codice completo, le pieghe dei reofori, il Q a 10,695 MHz e i parassiti del montaggio. [Scheda OEM Fastron SMCC](https://www.fastrongroup.com/uploads/datasheets/Series/Complete-DataSheet/SMCC.pdf).

Lo script KiCad/RX/terminazione_if.py considera L ±10%, C ±5%, resistenze ±1%, Q ipotetici 10/25/45 alla IF e due casi di capacità parassita. Con il carico di prova 2 kΩ in parallelo a 10 pF e sorgente 50 Ω stima 1,094–1,569 dB di perdita verso R110 e return loss minimo 26,13 dB. Sono risultati del modello a una frequenza; restano da misurare risposta in banda e comportamento con il mixer reale. Prossimo passo: verificare la vista del lato piedini e il disegno meccanico A06 di U110 prima del trasferimento su rame. [Datasheet Mini-Circuits SBL-1+](https://www.minicircuits.com/pdfs/SBL-1%2B.pdf).

## Mixer RX sulla PCB MAIN candidata

U110 SBL-1+ ha un’impronta locale A06 a otto fori metallizzati. Vista lato componenti, pin 1 all’origine, pin 2 a y = −5,08 mm, pin 3 a x = +5,08 mm. La vista inferiore OEM è stata ribaltata rispetto all’asse orizzontale. Inviluppo massimo 20,32 × 10,16 mm, terminali nominali Ø0,79 mm. Foro finito candidato Ø1,10 mm e piazzola 1,90 mm da qualificare con tolleranze e processo. [Disegno del fabbricante e piedinatura](https://www.minicircuits.com/WebStore/dashboardPdf?model=SBL-1%2B).

Pin 3 e 4 uniti sul rame al diplexer, pin 2/5/6/7 collegati al ritorno RX. Pin 1 RF e pin 8 LO attendono i rispettivi stadi. La netlist logica è invariata e i pad THT presenti corrispondono alla netlist. MAIN contiene 49 impronte. ERC 10 segnalazioni, DRC un errore di contorno, zero pad scollegati fra le impronte presenti e 13 impronte mancanti. Restano da verificare ritorni RF distribuiti, disponibilità OEM e montaggio. Prossimo blocco: preselettore RX verso il pin 1, previa verifica delle bobine e delle relative impronte.

## Preselettore RX sulla MAIN candidata

C110 (270 pF), C111 (82 pF) e C112 (270 pF) hanno impronte radiali THT candidate a passo 2,50 mm. I loro nodi in serie e l’uscita verso U110.1 sono instradati. Specifica candidata per i tre condensatori: C0G/NP0, ±5%, almeno 50 V. Restano aperti i codici OEM finali, l'ingresso a monte e i due rami induttivi verso RX_RF_RETURN.

La scheda Coilcraft della 132-13L riporta 246 nH ±5%, Q minimo 70 a 25 MHz e autorisonanza minima 440 MHz. Il modello a terminazioni ideali da 50 Ω restituisce 0,193–0,894 dB nella banda RX analizzata. Nella sezione di processo il fabbricante specifica la sola saldatura a onda. Per L101/L102 rimane quindi aperta la scelta di una bobina compatibile con il montaggio manuale. Il valore schematico resta preliminare a 240 nH. [Scheda OEM e processo di saldatura](https://www.coilcraft.com/en-us/products/rf/air-core-inductors/maxi-spring/132/132-13/).

Verifiche KiCad sulla candidata: stessa connettività logica, corrispondenza pin/pad/rete per le 52 impronte presenti, ERC MAIN 10 segnalazioni. DRC con parità: contorno assente, 10 impronte mancanti e zero pad scollegati tra quelli presenti. Prossimo lavoro: selezionare una bobina con processo manuale documentato e verificare perdita e reiezione prima di fissarne l'impronta.

## Due rami induttivi del preselettore collegati

Sul ramo candidato L101 e L102 passano a 270 nH. L’impronta assiale di libreria da 7 × 3,3 mm con passo 10,16 mm ospita il corpo Token TCAL0307 (massimo 7 × 3 mm, terminali Ø0,50 ±0,05 mm). Il nome Fastron dell'impronta indica la geometria di libreria. I due assi sono ortogonali per limitare l’accoppiamento. I due rami dal percorso capacitivo tornano al ritorno RX del mixer. Resta aperta la sorgente a monte di C110. Codice candidato della famiglia TCAL con formatura U; prima della BOM finale confermare codice d’ordine completo, passo e produzione OEM attiva. Il produttore documenta la saldatura a mano dei suoi induttori con terminali. [Geometrie](https://token.com.tw/inductor/inductor-fixed1.htm) · [Dati RF](https://token.com.tw/pdf/inductor/inductor-fixed1.pdf) · [Processo](https://token.com.tw/inductor-precautions-usage.htm).

Il modello a 50 Ω confronta 220 e 270 nH, tolleranza bobine ±20%, condensatori ±5%, Q minimo 30 a 25,2 MHz, frequenza di autorisonanza minima 380 e 360 MHz rispettivamente. Nella scansione storica da 25,615 a 28,305 MHz a passi da 10 kHz, sui 32 vertici di tolleranza, la massima perdita calcolata scende da 3,071 a 1,525 dB scegliendo 270 nH; l’attenuazione minima nella corrispondente banda immagine scende da 42,679 a 38,514 dB. La scelta candidata privilegia la sensibilità. Il modello a ESR costante esclude piste, accoppiamento residuo, dispersioni di montaggio e impedenze reali. La qualifica richiede misure di perdita e reiezione e verifica con il mixer reale.

MAIN ora ha 54 impronte THT. Netlist invariata nelle connessioni, pad e reti verificati. ERC 10 segnalazioni, DRC con parità un errore di contorno, otto impronte mancanti e zero pad scollegati tra quelli presenti. Prossima attività: chiudere la rete di adattamento IF dei filtri AM verificando terminazioni e fattori di merito.

## Rete IF AM candidata a 10,695 MHz

Sulla MAIN L104 e L105 da 4,7 µH, C114 e C116 da 47 pF, C115 da 9,1 pF e R112 da 56,2 Ω sono presenti nello schema e sulla PCB. Collegati il driver R117, i rami di adattamento disponibili e il ritorno RX. Per i condensatori si ipotizzano C0G ±5% e 1–3 pF di capacità esterna di montaggio; 9,1 pF più circa 2 pF concorrono agli 11 pF richiesti tra le sezioni. Le due sezioni FL101/FL102 restano da posizionare, con verifica della marcatura e della piedinatura.

Confronto a centro banda nel modello carico_filtro_am.py. La scheda Krystaly prescrive 1800 Ω in parallelo a 5 pF a entrambe le porte. Il candidato assiale Token TCAL0307-4R7K ha tolleranza ±10%, Q minimo 45 a 7,96 MHz e SRF minima 50 MHz. Simulati ESR costante estratta dal Q, due estremi di capacità propria e parassiti di montaggio ipotetici. Usando il modello di impedenza complessa del buffer si ottengono 1463–2470 Ω e −5,11…12,44 pF all’ingresso; con carico futuro aperto o 2 kΩ in parallelo a 10 pF si ottengono 1376–2232 Ω e −4,88…12,67 pF all’uscita. Un valore negativo indica suscettanza netta induttiva. La dispersione richiede selezione o regolazione delle reti e verifica con il filtro reale. La banda passante e l’attenuazione fuori banda del circuito montato restano da dimostrare. Confermare MPN completo, produzione, parassiti, processo e impronte prima di congelare il circuito. [Filtro OEM](https://www.krystaly.cz/en/wp-content/uploads/2023/06/TSP_10695-075-B.pdf) · [Induttori OEM](https://token.com.tw/pdf/inductor/inductor-fixed1.pdf).

MAIN candidata: 60 impronte THT; netlist logica conservata e pad verificati. ERC 10 segnalazioni. DRC con parità: errore di contorno, zero pad scollegati tra quelli presenti e due impronte mancanti nel master attuale. Il master rappresenta una radio parziale. Prossimo lavoro: predisporre la taratura alle due porte e verificare impronta e orientamento delle sezioni a quarzi.

## Taratura predisposta sui due terminali esterni del filtro AM

C114 e C116 diventano 33 pF. Accanto a ciascuno è instradato un secondo condensatore THT C0G da selezionare al montaggio: C125 all’ingresso, C126 all’uscita, inizialmente 15 pF ciascuno. Il circuito consente di regolare la parte reale mediante selezione di R117/R112 e quella reattiva mediante C125/C126. La rete tra le due sezioni mantiene C115. Verificati i quattro nuovi pin e la conservazione delle reti precedenti.

Il calcolo riproducibile in KiCad/RX/taratura_am.py seleziona per ciascun caso valori discreti, assunti misurati. A 10,695 MHz si punta a 1800 Ω in parallelo a 5 pF. Nel dominio campionato del modello, R117 va da 27 a 62 Ω e C125 da 6,2 a 24 pF; R112 da 43 a 75 Ω e C126 da 6,8 a 24 pF. Dopo la selezione, ingresso 1742–1866 Ω e 4,01–6,00 pF, uscita 1734–1860 Ω e 4,04–5,98 pF. La compensazione è individuale per caso. Un unico valore fisso non assicura questi risultati. Restano aperte le verifiche di perdita e ondulazione sull’intera banda, il carico effettivo dello stadio successivo e la validazione con componenti reali.

Il disegno Krystaly indica due sezioni HC-49U a tre terminali. Rimane da verificare il passo e il legame tra il punto colorato, il terminale esterno e il pad del contenitore sul disegno meccanico originale prima di trasferire FL101 e FL102. [Specifica del produttore](https://www.krystaly.cz/en/wp-content/uploads/2023/06/TSP_10695-075-B.pdf).

MAIN candidata: 62 impronte THT, zero pad scollegati tra quelli presenti. ERC 10 segnalazioni, DRC un errore di contorno e due impronte mancanti rispetto allo schema parziale. Nessun collaudo fisico.

## Filtro AM a quattro poli trasferito sulla MAIN candidata

Il disegno 61 9573, specifica Krystaly 92 189, mostra le due sezioni HC-49U/3 pin, l’interasse esterno 5,08 ±0,3 mm e i punti colorati rivolti verso le porte esterne. La nuova impronta locale usa 5,08 mm tra DOT e INNER. Il pad centrale CASE è collocato a metà interasse per simmetria del disegno. Foro finito candidato 0,95 mm per terminali nominali da 0,43 mm; ingombro massimo in pianta 11,2 × 4,7 mm, altezza massima 11,3 mm. Rimangono da qualificare il centraggio del terminale centrale non quotato separatamente, le tolleranze di assemblaggio e la distanza del fondo metallico dal rame. Il punto serigrafico identifica il lato DOT. [Disegno quotato e circuito di misura OEM, pagina 1](https://www.krystaly.cz/wp-content/uploads/2023/05/TSP_10695-075-B.pdf).

FL101.DOT va all’ingresso dal driver, FL102.DOT all’uscita terminata, entrambi gli INNER al nodo di accoppiamento con C115. Entrambi i CASE raggiungono RX_RF_RETURN. La rete verso il demodulatore a valle resta da sviluppare. La risposta in banda, l’attenuazione fuori banda e i parassiti effettivi non sono misurati. Confermare anche lo stato di produzione OEM della coppia prima di congelare la BOM.

MAIN: 64 impronte THT sullo schema parziale corrente, corrispondenza pin/pad/rete verificata. Netlist logica conservata. DRC con parità: zero pad scollegati e zero discrepanze di impronta; permane un errore di contorno. ERC: 10 errori aperti. Prossimo blocco: dimensionare guadagno e carico dello stadio IF a valle di FL102, includendo il comportamento ai segnali deboli e la dinamica richiesta dal rivelatore AM.

## Primo amplificatore IF AM dopo FL102

Q102, candidato onsemi 2N3904BU in TO-92 E/B/C, riceve il segnale dal nodo terminato attraverso C127. R129/C129 filtrano localmente la linea logica candidata, R130/R131 polarizzano la base, R132 è il carico di collettore e R133/R134 con C128 fissano la degenerazione di emettitore. Le dieci impronte THT e i relativi collegamenti sono presenti sulla MAIN. L’uscita AM_IF1_COLLECTOR porta anche la polarizzazione continua: prevedere accoppiamento e carico del prossimo stadio. Il ritorno RF alla sorgente e l’alimentazione complessiva restano aperti. [Scheda OEM](https://www.onsemi.com/download/data-sheet/pdf/2n3904-d.pdf).

Il modello riproducibile KiCad/RX/guadagno_if_am.py (Python con NumPy) risolve polarizzazione e piccolo segnale a 10,695 MHz. A 4,75–5,25 V, nei casi campionati di transistor e con carico futuro solo AC da 2–10 kΩ in parallelo a 5–15 pF, restituisce Ie 0,97–1,77 mA, Vce 2,44–3,24 V e guadagno di tensione dal nodo AM_IF_TERMINATED al collettore 15,0–21,2 dB. L’impedenza d’ingresso in modulo è 229–714 Ω; il modello include la capacità base-collettore. Con questo carico complesso il calcolo della selezione di R112/C126 restituisce 43–82 Ω e 6,8–24 pF, equivalenti nei casi valutati a 1732–1874 Ω e 4,00–5,99 pF alla porta del quarzo. Sono scenari con componenti ideali esterni, senza parassiti del layout, rumore, compressione o modello OEM completo. Restano da verificare stabilità in frequenza, tolleranze, impedenza della distribuzione, guadagno complessivo e dinamica di rivelazione. Produzione OEM corrente da confermare prima del congelamento.

Verifiche MAIN: conservate le connessioni precedenti e verificata nella netlist la mappa dei nuovi pin. 74 impronte THT. ERC 10 errori preesistenti; DRC con parità zero pad scollegati, zero discrepanze di impronte, contorno ancora assente. Prossimo lavoro: determinare il guadagno ancora necessario prima del rivelatore AM e il punto di intervento del controllo di guadagno, con il carico effettivo di uscita.

## Secondo amplificatore IF AM e bilancio verso il rivelatore

Q103 è accoppiato in alternata al collettore di Q102 mediante C130. R135/C132 disaccoppiano l’alimentazione locale. R136/R137 polarizzano la base, R138 carica il collettore e R139/R140/C131 impostano la degenerazione di emettitore. Dieci componenti instradati sulla MAIN, uscita AM_IF2_COLLECTOR polarizzata in continua. Il modello e il CAD usano la medesima topologia di Q102. [Transistor candidato onsemi](https://www.onsemi.com/pdf/datasheet/pzt3904-d.pdf).

Il modello riproducibile in KiCad/RX/cascata_if_am.py risolve prima Q103, poi applica la sua impedenza complessa d’ingresso al collettore di Q102. Nei casi analizzati a 10,695 MHz il guadagno di Q102 caricato è 6,55–14,82 dB. Il guadagno totale dal nodo AM_IF_TERMINATED al collettore di Q103 è 24,37–33,91 dB. Con 1 µV RMS di portante a quel nodo si ottengono 16,5–49,6 µV RMS in uscita. La tensione al connettore antenna è distinta da quella al nodo IF. Per un esempio di 100 mV di inviluppo di picco con modulazione 100% servirebbero altri 57,06–66,60 dB con tale ingresso. Con i soli due stadi la stessa ampiezza sarebbe raggiunta per 0,713–2,138 mV RMS al nodo IF. La soglia è uno scenario per confrontare i rivelatori: guadagno finale e punto di intervento AGC dipendono dal rivelatore e dalla dinamica effettiva. Mancano verifica di rumore, compressione, stabilità, parassiti e tensione RF al filtro. Scelta successiva: confrontare rivelazione sincrona e d’inviluppo con livelli deboli e modulazione profonda prima di aumentare ancora il guadagno fisso.

MAIN candidata a 84 impronte THT, zero pad scollegati e zero discrepanze rispetto allo schema parziale. Verificate le reti precedenti, la topologia duplicata del nuovo stadio e la separazione delle sue reti interne. ERC 10 errori aperti, DRC un errore per contorno assente. PCB e BOM ancora da qualificare.

## Ramo di misura dell’inviluppo AM e confronto dei rivelatori

C133 disaccoppia il collettore Q103 in continua. R141 (6,8 kΩ) assicura il ritorno di ingresso, D104 (candidato BAT85S-TAP, DO-35) carica C134 (120 pF) e R142 (47 kΩ) scarica il nodo AM_ENV_RAW. Costante nominale a diodo interdetto 5,64 µs. I cinque componenti THT sono cablati nello schema e sulla PCB. Nodo disponibile per la futura misura di livello; impedenza dell’eventuale buffer, filtraggio lento AGC, attuatore e stabilità di anello da dimensionare. Il ramo non chiude un anello AGC. [Diodo Vishay](https://www.vishay.com/docs/85513/bat85s.pdf).

KiCad/RX/rivelatore_am.cpp confronta un rivelatore passivo con una demodulazione coerente ideale normalizzata. Sorgente di Thévenin da 1 kΩ, 10,695 MHz modulati all’80% a 1 kHz. I due scenari di Shockley (Is 10 o 100 nA, nVT 30 mV, Cj costante 8 pF) sono ipotesi di sensibilità: mancano parametri OEM a bassissima corrente, rumore, temperatura e capacità del cablaggio. Il modello risolve la corrente attraverso C133 e le due tensioni ai terminali del diodo. Con 30 µV RMS a vuoto e 192 passi per ciclo la fondamentale audio passiva è circa 0,20–1,76 nV di picco, rapporto combinato di seconda e terza armonica circa 20%. A 100 mV RMS risulta 8,95–25,69 mV di picco, con 22–40% di armoniche seconde/terze nei casi esaminati. Il raddoppio da 96 a 192 passi cambia le ampiezze fino a circa 2,1%. Sono stime deterministiche, non una misura della sensibilità né della distorsione reale. Il riferimento coerente ideale con portante perfettamente allineata produce 33,94 µV di picco a 30 µV RMS a vuoto: non include caricamento, perdita di conversione, rumore o perdita di aggancio.

Il ramo a diodo resta candidato come indicatore di livelli maggiori. Per il percorso audio debole si privilegia lo studio della rivelazione sincrona: prossimo blocco è il recupero di portante e la verifica di aggancio con scarto IF, modulazione profonda e rumore, prima di fissare il demodulatore e le soglie AGC. Verificare anche il carico non lineare visto da Q103 e la dinamica complessiva.

MAIN candidata: 89 impronte THT. Il confronto netlist conserva tutte le precedenti connessioni e verifica orientamento di D104 e ritorni. ERC 10 errori preesistenti; DRC con parità zero pad scollegati, zero discrepanze, contorno assente. Qualifica OEM e collaudo fisico restano aperti.

## Separazione del segnale IF e studio del recupero di portante

Q104, candidato 2N3904BU, riceve direttamente la polarizzazione del collettore Q103. R143/C135 disaccoppiano il collettore e R144 fissa la corrente di emettitore. C133 preleva ora il segnale dall’emettitore AM_IF_BUFFER_OUT, condivisibile con il futuro ramo coerente. Il modello separatore_if_am.py include il caricamento del rivelatore linearizzato a portante prossima a zero. Nei casi campionati: Ie 2,16–3,05 mA, Vce 1,68–2,89 V, modulo dell’impedenza di ingresso 2,53–5,69 kΩ. Con 1 µV RMS al nodo AM_IF_TERMINATED restituisce 21,7–53,8 µV RMS all’emettitore. Ipotesi: ritorno e distribuzione ideali, resistenza di Thévenin DC approssimata, parametri ibrido-pi e capacità del diodo di scenario. Il precedente esempio a sorgente da 1 kΩ del rivelatore non rappresenta l’impedenza di uscita del nuovo separatore. Da verificare rumore, trasferimento su inviluppi grandi e dissipazione del regolatore. [Transistor OEM](https://www.onsemi.com/pdf/datasheet/pzt3904-d.pdf).

In recupero_portante_am.py si prova un’acquisizione spettrale di 32 ms seguita da un anello di fase di secondo ordine in banda base complessa ideale a 16 kcampioni/s. Scarti −480/0/+480 Hz, modulazione al 50/100% a 1 kHz e tre realizzazioni di rumore per combinazione. Il C/N è potenza di portante divisa per potenza totale del rumore complesso campionato. Nell’ultimo quarto di secondo a −12 dB si osservano zero casi con salti su 18 e un errore RMS massimo di 23,8°; a −18 dB compaiono salti in 12 casi su 18. Questi punti non costituiscono una soglia garantita. Nessun convertitore I/Q, ADC, firmware o PLL fisico è integrato. Prossimo confronto concreto: dimensionare rumore riferito all’ingresso, guadagno e dinamica di un convertitore I/Q THT compatibile con decine di microvolt e verificare cattura anche con modulanti basse, interferenze e deriva. Verificare separatamente l’alternativa analogica e la disponibilità dei componenti.

MAIN candidata: 93 impronte THT, zero pad scollegati, zero discrepanze. ERC 10 errori aperti; DRC errore per contorno assente. Verificato lo spostamento di C133 e mantenuti i collegamenti preesistenti estranei al ramo. Nessuna prova hardware.

## Convertitore I/Q candidato sulla MAIN

U111/U112 sono due mixer passivi SBL-1+ con impronte THT A06. C136 da 10 nF blocca la continua di Q104; R145/R146 da 49,9 Ω alimentano i due ingressi RF, e R147/R148 terminano le uscite in banda base su RX_RF_RETURN. Ogni coppia di pin IF 3–4 è unita localmente. Entrambi i ritorni sono instradati. Le due porte LO attendono ancora i driver a 10,695 MHz sfasati di 90°; il livello nominale richiesto è +7 dBm per porta (circa 0,50 V RMS su 50 Ω). In mancanza dei LO il percorso non effettua la conversione prevista. [Scheda Mini-Circuits](https://www.minicircuits.com/pdfs/SBL-1%2B.pdf).

Il modello conversione_iq_am.py include entrambe le porte pompate assunte a 50 Ω, il disaccoppiamento in alternata e il ramo del diodo linearizzato. Per 1 µV RMS al nodo AM_IF_TERMINATED dà 11,5–36,1 µV RMS all’emettitore e 5,75–18,07 µV RMS all’ingresso di ciascun mixer. Per un tono leggermente scostato dal LO, assumendo 5,6–8 dB di perdita, risultano 2,29–9,48 µV RMS per uscita. La perdita al piccolo scarto, l’offset DC, il rumore 1/f, la fuga del LO verso Q104, l’isolamento tra canali e lo sbilanciamento di fase devono essere verificati. La stima di interdizione dell’emettitore con i rami nominali e senza carico del diodo è 103–145 mV di picco, da riesaminare a grande segnale. Il rumore a vuoto della sola terminazione da 49,9 Ω è circa 0,057 µV RMS su 4 kHz a 290 K. Per arrivare a 100 mV RMS (scenario ADC) al livello IF ipotizzato, il guadagno successivo richiesto è circa 10 550–43 670 V/V. Un guadagno fisso di tale entità avrebbe dinamica limitata. Confrontare un primo stadio baseband THT a basso rumore con conversione a basso IF e guadagno distribuito/regolabile; dimensionare separatamente i driver LO e il filtraggio anti-alias.

MAIN candidata: 100 impronte THT. Pin/pad/net confrontati, nessun pad scollegato tra le impronte presenti e zero discrepanze di parità. DRC aperto per contorno assente. ERC 12 errori: i due nuovi sono le porte LO a singolo terminale. Nessuna qualifica di produzione o misura hardware implicita. Nessuna variazione della FRONT.

## Prossimo lavoro

Selezionare il dispositivo RF THT e confrontare guadagno/rumore con blocco e intermodulazione prima di fissare la topologia d’ingresso.

Qualificare L104/L105, compensare le perdite e dimensionare commutazione e ramo SSB stretto.

Definire architettura delle sorgenti, ritorni e distribuzione di potenza, separando il ramo logico dal carico RF. Qualificare le bobine THT e definire lo stadio RF a valle con le sue impedenze. Integrare i percorsi di ritorno RF e di alimentazione. Progettare protezione di linea e interblocco con qualificazione all’avvio. Dimensionare alimentazione e ritorni del FRONT, scegliere interfaccia dati in funzione di EMC e topologia, poi collegare gli endpoint reali. Completare il riscontro storico delle posizioni extra e degli scostamenti di modo.

## Autorizzazioni

NO FAB, NO GERBER DI PRODUZIONE, NO ORDINI PCB, NO TX, NO BATTERIA, NO VEICOLO.
