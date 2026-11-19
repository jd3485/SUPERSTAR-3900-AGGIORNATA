# Interfaccia cablata MAIN–FRONT candidata

MAIN ospita i circuiti RF/IF, alimentazione, modulazione e protezioni. FRONT ospita pannello, comandi e visualizzazione. Questa ripartizione e il pinout sono proposte di integrazione, da verificare prima della scelta del connettore e del layout.

| Pin J101 / J201 | Rete | Funzione candidata |
|---|---|---|
| 1 | FRONT_SUPPLY | Alimentazione da MAIN a FRONT |
| 2 | FRONT_RETURN | Ritorno di alimentazione |
| 3 | CONTROL_TO_MAIN | Comandi FRONT → MAIN |
| 4 | CONTROL_TO_FRONT | Stato e misure MAIN → FRONT |
| 5 | CONTROL_RETURN | Riferimento dei segnali da definire con topologia delle masse |
| 6 | TX_REQUEST_N | Richiesta logica FRONT → MAIN, subordinata agli interblocchi MAIN; stato sicuro con FRONT assente da progettare |

Tensione, protocollo, corrente, sequenza di accensione, budget EMC, collegamento dei ritorni, interfacce audio, schermatura e connettori fisici restano aperti. I terminali non ancora integrati terminano al connettore. Il collegamento è rappresentato dalle due mappe pin equivalenti; nessun livello elettrico o abilitazione TX è implementato. Nessuna impronta è assegnata fino alla qualifica.

## Evidenza

KiCad CLI 9.0.2 ha aperto entrambi i master ed esportato due netlist XML con corrispondenza identica delle sei coppie pin/rete. ERC nativo eseguito. Dopo il collegamento del comando restano sei errori di etichetta su rete a singolo terminale su MAIN e quattro su FRONT, da risolvere integrando gli endpoint reali. Nessun DRC eseguibile senza PCB. Nessuna prova fisica.

## Richiesta PTT candidata

SW201 è un contatto normalmente aperto su FRONT che porta il pin 6 al ritorno sul pin 5. R101 da 10 kΩ su MAIN propone il livello inattivo a cavo aperto, quando la futura alimentazione logica è presente. Valore, soglie, protezioni, supervisione del cavo e stato all'accensione da qualificare. Un cortocircuito verso il ritorno può simulare una pressione: l'ingresso non deve abilitare direttamente RF. Manca il ricevitore/interblocco su MAIN. Le netlist native confermano connessioni del contatto e della resistenza.
