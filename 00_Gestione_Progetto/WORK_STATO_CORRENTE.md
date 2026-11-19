# Stato operativo

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

## Prossimo lavoro

Selezionare il dispositivo RF THT e confrontare guadagno/rumore con blocco e intermodulazione prima di fissare la topologia d’ingresso.

Qualificare L104/L105, compensare le perdite e dimensionare commutazione e ramo SSB stretto.

Definire architettura delle sorgenti, ritorni e distribuzione di potenza, separando il ramo logico dal carico RF. Qualificare le bobine THT e definire lo stadio RF a valle con le sue impedenze. Integrare i percorsi di ritorno RF e di alimentazione. Progettare protezione di linea e interblocco con qualificazione all’avvio. Dimensionare alimentazione e ritorni del FRONT, scegliere interfaccia dati in funzione di EMC e topologia, poi collegare gli endpoint reali. Completare il riscontro storico delle posizioni extra e degli scostamenti di modo.

## Autorizzazioni

NO FAB, NO GERBER DI PRODUZIONE, NO ORDINI PCB, NO TX, NO BATTERIA, NO VEICOLO.
