# Primo filtro RX candidato

Passa-alto LC di quinto ordine nel master MAIN tra RX_FILTER_IN e RX_FILTER_OUT. Con iniezione inferiore e IF candidata a 10,695 MHz l'immagine di 25,615–28,305 MHz cade a 4,225–6,915 MHz. Il filtro tratta questa immagine; la selettività sopra banda richiede lo stadio accordato successivo. Topologia e impedenze da confermare con commutatore antenna e ingresso dello stadio RF.

C110/C112 270 pF, C111 82 pF, induttanze in derivazione L101/L102 240 nH. Per il modello assumiamo condensatori C0G, elementi ideali ±5%, generatore e carico a 50 Ω. Il calcolo riproducibile in risposta_filtro.py copre 270 punti a passi di 10 kHz per intervallo e 32 combinazioni agli estremi di tolleranza. Perdita di inserzione calcolata 0,036–0,719 dB in banda e attenuazione 43,566–69,159 dB nella banda immagine. Non include Q finito, frequenze di autorisonanza, tolleranze intermedie, parassiti, accoppiamento tra bobine e disadattamento del mixer.

KiCad 9.0.2: esportata la netlist del master e verificati entrambi i nodi a tre terminali, porte e ritorno comune alle bobine. Due nuovi errori ERC corrispondono alle porte RX ancora prive di endpoint. Il collegamento del ritorno RF al riferimento fisico richiede progetto del percorso di massa. Selezionare componenti THT OEM attivi con dati di Q e autorisonanza e verificare la risposta con impedenze reali prima del layout.
