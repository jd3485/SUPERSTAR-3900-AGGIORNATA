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

## Prossimo lavoro

Selezionare il dispositivo RF THT e confrontare guadagno/rumore con blocco e intermodulazione prima di fissare la topologia d’ingresso.

Qualificare L104/L105, compensare le perdite e dimensionare commutazione e ramo SSB stretto.

Definire architettura delle sorgenti, ritorni e distribuzione di potenza, separando il ramo logico dal carico RF. Qualificare le bobine THT e definire lo stadio RF a valle con le sue impedenze. Integrare i percorsi di ritorno RF e di alimentazione. Progettare protezione di linea e interblocco con qualificazione all’avvio. Dimensionare alimentazione e ritorni del FRONT, scegliere interfaccia dati in funzione di EMC e topologia, poi collegare gli endpoint reali. Completare il riscontro storico delle posizioni extra e degli scostamenti di modo.

## Autorizzazioni

NO FAB, NO GERBER DI PRODUZIONE, NO ORDINI PCB, NO TX, NO BATTERIA, NO VEICOLO.
