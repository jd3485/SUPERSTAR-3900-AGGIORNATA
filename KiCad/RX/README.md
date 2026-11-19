# Primo filtro RX candidato

Passa-alto LC di quinto ordine nel master MAIN tra RX_FILTER_IN e RX_FILTER_OUT. Con iniezione inferiore e IF candidata a 10,695 MHz l'immagine di 25,615–28,305 MHz cade a 4,225–6,915 MHz. Il filtro tratta questa immagine; la selettività sopra banda richiede lo stadio accordato successivo. Topologia e impedenze da confermare con commutatore antenna e ingresso dello stadio RF.

C110/C112 270 pF, C111 82 pF, induttanze in derivazione L101/L102 240 nH. Per il modello assumiamo condensatori C0G, elementi ideali ±5%, generatore e carico a 50 Ω. Il calcolo riproducibile in risposta_filtro.py copre 270 punti a passi di 10 kHz per intervallo e 32 combinazioni agli estremi di tolleranza. Perdita di inserzione calcolata 0,036–0,719 dB in banda e attenuazione 43,566–69,159 dB nella banda immagine. Non include Q finito, frequenze di autorisonanza, tolleranze intermedie, parassiti, accoppiamento tra bobine e disadattamento del mixer.

KiCad 9.0.2: esportata la netlist del master e verificati entrambi i nodi a tre terminali, porte e ritorno comune alle bobine. Due nuovi errori ERC corrispondono alle porte RX ancora prive di endpoint. Il collegamento del ritorno RF al riferimento fisico richiede progetto del percorso di massa. Selezionare componenti THT OEM attivi con dati di Q e autorisonanza e verificare la risposta con impedenze reali prima del layout.

## Variante con Coilcraft 132-13L

Per L101 e L102 si valuta la 132-13L, bobina a filo da 246 nH ±5%. L'OEM riporta Q minimo 70 a 25 MHz e SRF minima 440 MHz. Nel modello esplorativo si assume ESR costante ricavata da quel Q e capacità parallela dalla SRF. Le perdite calcolate ai vertici sono 0,193–0,894 dB in banda e 43,116–68,665 dB nella banda immagine. La dipendenza reale del Q dalla frequenza, il montaggio, l'accoppiamento tra bobine e i disadattamenti restano da verificare. Il valore schematico resta 240 nH fino alla selezione definitiva. Confermare produzione corrente e qualificare impronta e passo prima di congelare la BOM.

[Pagina OEM](https://www.coilcraft.com/en-us/products/rf/air-core-inductors/maxi-spring/132/132-13/) · [Datasheet](https://www.coilcraft.com/getmedia/22e0981d-b6cb-4c11-a3ec-5cac433ee01c/132.pdf)

## Prima conversione candidata

U110 SBL-1+ è un mixer passivo bilanciato plug-in A06. Il segnale dal filtro entra sul pin RF 1. LO entra sul pin 8; i pin IF 3 e 4 sono uniti esternamente. I pin di massa 2, 5, 6 e 7 condividono RX_RF_RETURN. Tutti gli otto collegamenti sono verificati nella netlist esportata. Il driver LO resta da integrare. La porta IF alimenta la rete di terminazione descritta sotto. La sola unione dei due pin IF non costituisce un carico IF. Il mixer lavora con LO nominale +7 dBm (circa 0,50 V RMS su 50 Ω) nel piano candidato 14,920–17,610 MHz. Le specifiche OEM indicano perdita di conversione tipica 5,6 dB; il valore effettivo e il contributo al rumore richiedono verifica sul punto di lavoro. L'amplificazione RF precedente e la selettività sopra banda restano da decidere secondo il budget del ricevitore. Non è dimostrata una terminazione puramente resistiva da 50 Ω a ogni frequenza.

Confermare produzione attuale, compatibilità del modulo con il vincolo costruttivo THT, impronta, adattamento delle tre porte e isolamento dal trasmettitore prima di congelare il circuito. [Datasheet Mini-Circuits](https://www.minicircuits.com/pdfs/SBL-1%2B.pdf).

## Terminazione IF candidata

La porta IF alimenta due rami. L103 (390 nH) porta il segnale a R110 (49,9 Ω) e al nodo RX_IF_LOWPASS, destinato a uno stadio ad alta impedenza. C113 (160 pF) scarica la componente ad alta frequenza su R111 (49,9 Ω). Entrambi i ritorni vanno al riferimento RF del mixer. La relazione L/C prossima a R² consente ai rami complementari di presentare un carico vicino a 50 Ω. Il filtro di selettività di canale verrà dopo un buffer o uno stadio di adattamento.

A 10,695 MHz il modello lineare con L e C ±5% e R ±1%, ai 16 vertici, fornisce perdita di trasduzione in R110 di 0,985–1,198 dB e return loss minimo di 31,67 dB con ingresso successivo ideale aperto. Nell'ipotesi di 2 kΩ in parallelo a 10 pF la perdita diventa 1,057–1,264 dB e il return loss minimo 27,73 dB. Il modello non include perdite e parassiti della bobina, né il comportamento non lineare del mixer. L'induttanza THT e le impedenze reali restano da qualificare. Schema e controlli delle reti coprono i due pin IF del mixer, i due rami e i ritorni. Calcolo ripetibile con terminazione_if.py.

## Selettività AM a 10,695 MHz

FL101 e FL102 rappresentano le due sezioni di un solo filtro candidato KRYSTALY MCF 10.695-7.5B, specifica 92 189, quattro poli, due contenitori HC-49U a tre terminali. Contare un set per radio. Il disegno OEM pone i terminali marcati ai lati esterni, i due interni uniti e gli involucri a massa. C115 fornisce 11 pF complessivi sul nodo di accoppiamento. DOT/INNER/CASE sono identificatori funzionali da mappare su pad fisici con la conferma del disegno meccanico.

Il fabbricante specifica almeno 7,5 kHz complessivi a −3 dB, perdita ≤2,5 dB e attenuazione ≥40 dB a ±14 kHz nelle condizioni di misura prescritte. Questi valori guidano la scelta per AM. Prestazioni ai canali adiacenti a ±10 kHz, risposta del circuito reale e idoneità agli altri modi restano aperte.

La porta di ingresso richiede 1800 Ω in parallelo a 5 pF. Per un futuro buffer con sorgente da 50 Ω, L104 in serie da 4,4 µH e C114 totale da 54 pF trasformano l'ammettenza secondo Y = 1/(50+jωL) + jωC. A centro banda il calcolo ideale dà 1798,46 Ω in parallelo a 5,07 pF. All'uscita R112 e C116 prevedono 1800 Ω e 5 pF complessivi incluso il carico del successivo stadio. Nel dimensionamento fisico sottrarre capacità di pin, piste e stadio ricevente dai valori totali. Con capacità parassita già superiore al bersaglio sarà necessario cambiare adattamento. Verificare Q/SRF e tolleranze di L104. Il segnale RX_IF_LOWPASS resta da collegare tramite buffer e selezione di modo; l'ingresso a 50 Ω è un'ipotesi di interfaccia.

Verificate le reti KiCad del nodo centrale, dei terminali marcati e degli involucri. Restano da confermare produzione OEM attuale, impronte e risposta con modello del filtro o misure autorizzate. La prova citata è relativa al circuito del produttore. [Specifica OEM](https://www.krystaly.cz/en/wp-content/uploads/2023/06/TSP_10695-075-B.pdf)

## Buffer tra diplexer e filtro AM

Q101, candidato onsemi 2N3904BU in TO-92, opera a collettore comune. C119 preleva la IF da RX_IF_LOWPASS, R114/R115 e R116 stabiliscono la polarizzazione. C120 e R117 pilotano l'adattamento di FL101. R113 e C117/C118 disaccoppiano l'alimentazione del ramo analogico. Il ritorno RX_RF_RETURN richiede ancora un percorso fisico definito verso la sorgente DC. La rete resta collegata anche in altri modi: rivalutare il carico complessivo con i rami SSB/FM/CW.

Il calcolo a 10,695 MHz usa un modello parametrico ibrido-pi, sorgente mixer da 50 Ω, carico nominale da 50 Ω, resistenze nominali e disaccoppiamento ideale. Gli intervalli di beta, fT, VBE, capacità e alimentazione nello script sono ipotesi di sensibilità. Nei casi calcolati Ie = 1,93–2,67 mA e Zout presenta parte reale 48,50–52,30 Ω e immaginaria −1,21…−0,23 Ω. Il modulo di Zin del buffer varia da 664 a 1894 Ω. Sulla rete del mixer con L e C nominali questo produce perdita in R110 di 1,08–1,12 dB e return loss 29,24–36,23 dB. Verificare modello OEM al punto di lavoro, stabilità, rumore, dinamica e adattamento del filtro con parassiti e tolleranze. Rimangono aperte la qualifica OEM definitiva e quella meccanica. [Datasheet OEM](https://www.onsemi.com/pdf/datasheet/pzt3904-d.pdf).
