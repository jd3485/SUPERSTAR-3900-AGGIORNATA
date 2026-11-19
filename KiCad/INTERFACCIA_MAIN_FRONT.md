# Interfaccia cablata MAIN–FRONT candidata

MAIN ospita i circuiti RF/IF, alimentazione, modulazione e protezioni. FRONT ospita pannello, comandi e visualizzazione. Questa ripartizione e il pinout sono proposte di integrazione, da verificare prima della scelta del connettore e del layout.

| Pin J101 / J201 | Rete | Funzione candidata |
|---|---|---|
| 1 | FRONT_SUPPLY | Alimentazione da MAIN a FRONT |
| 2 | FRONT_RETURN | Ritorno di alimentazione |
| 3 | CONTROL_TO_MAIN | Comandi FRONT → MAIN |
| 4 | CONTROL_TO_FRONT | Stato e misure MAIN → FRONT |
| 5 | CONTROL_RETURN | Riferimento dei segnali da definire con topologia delle masse |
| 6 | TX_REQUEST | Richiesta logica FRONT → MAIN, subordinata agli interblocchi MAIN; stato sicuro con FRONT assente da progettare |

Tensione, protocollo, corrente, sequenza di accensione, budget EMC, collegamento dei ritorni, interfacce audio, schermatura e connettori fisici restano aperti. Le sei reti per scheda terminano al connettore perché i sottosistemi interni devono ancora essere collegati. Il collegamento è rappresentato dalle due mappe pin equivalenti; nessun livello elettrico o abilitazione TX è implementato. Nessuna impronta è assegnata fino alla qualifica.

## Evidenza

KiCad CLI 9.0.2 ha aperto entrambi i master ed esportato due netlist XML con corrispondenza identica delle sei coppie pin/rete. ERC nativo eseguito. Rimangono sei errori di etichetta su rete a singolo terminale per ciascun master, da risolvere integrando gli endpoint reali. Nessun DRC eseguibile senza PCB. Nessuna prova fisica.
