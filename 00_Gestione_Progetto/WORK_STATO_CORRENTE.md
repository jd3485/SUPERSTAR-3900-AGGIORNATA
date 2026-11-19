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

## Prossimo lavoro

Qualificare L104/L105, compensare le perdite e dimensionare commutazione e ramo SSB stretto.

Definire architettura delle sorgenti, ritorni e distribuzione di potenza, separando il ramo logico dal carico RF. Qualificare le bobine THT e definire lo stadio RF a valle con le sue impedenze. Integrare i percorsi di ritorno RF e di alimentazione. Progettare protezione di linea e interblocco con qualificazione all’avvio. Dimensionare alimentazione e ritorni del FRONT, scegliere interfaccia dati in funzione di EMC e topologia, poi collegare gli endpoint reali. Completare il riscontro storico delle posizioni extra e degli scostamenti di modo.

## Autorizzazioni

NO FAB, NO GERBER DI PRODUZIONE, NO ORDINI PCB, NO TX, NO BATTERIA, NO VEICOLO.
