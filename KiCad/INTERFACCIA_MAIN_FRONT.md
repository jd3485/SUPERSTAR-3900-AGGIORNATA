# Interfaccia cablata MAIN–FRONT candidata

MAIN ospita i circuiti RF/IF, alimentazione, modulazione e protezioni. FRONT ospita pannello, comandi e visualizzazione. Questa ripartizione e il pinout sono proposte di integrazione, da verificare prima della scelta del connettore e del layout.

| Pin J101 / J201 | Rete | Funzione candidata |
|---|---|---|
| 1 | FRONT_SUPPLY | Alimentazione da MAIN a FRONT |
| 2 | FRONT_RETURN | Ritorno di alimentazione |
| 3 | CONTROL_TO_MAIN | Comandi FRONT → MAIN |
| 4 | CONTROL_TO_FRONT | Stato di sintonia e dati per visualizzare SWR, potenza RF e modulazione MAIN → FRONT |
| 5 | CONTROL_RETURN | Riferimento dei segnali da definire con topologia delle masse |
| 6 | PTT_SENSE | Linea analogica supervisionata FRONT → MAIN, subordinata agli interblocchi MAIN |

Tensione, protocollo, corrente, sequenza di accensione, budget EMC, collegamento dei ritorni, interfacce audio, schermatura e connettori fisici restano aperti. I terminali non ancora integrati terminano al connettore. Il collegamento è rappresentato dalle due mappe pin equivalenti; nessun livello elettrico o abilitazione TX è implementato. Nessuna impronta è assegnata fino alla qualifica.

## Evidenza

KiCad CLI 9.0.2 ha aperto entrambi i master ed esportato due netlist XML con corrispondenza identica delle sei coppie pin/rete. ERC nativo eseguito. Dopo il collegamento del comando restano sei errori di etichetta su rete a singolo terminale su MAIN e quattro su FRONT, da risolvere integrando gli endpoint reali. Nessun DRC eseguibile senza PCB. Nessuna prova fisica.

## Richiesta PTT supervisionata candidata

Su MAIN, R101 da 10 kΩ polarizza PTT_SENSE dalla futura alimentazione logica. Su FRONT, R201 da 10 kΩ termina la linea verso CONTROL_RETURN. Premendo SW201 si aggiunge R202 da 2,2 kΩ in parallelo a R201. I tre resistori sono candidati THT con tolleranza funzionale 1%, da qualificare nella distinta definitiva.

| Condizione | PTT_SENSE / MAIN_LOGIC_SUPPLY |
|---|---:|
| Corto franco al ritorno sul lato MAIN | 0 ideale |
| PTT premuto | 0,150–0,163 |
| PTT rilasciato | 0,495–0,508 |
| Cavo aperto | 1 ideale |

Intervalli calcolati ai vertici delle tolleranze ±1% e con resistenza serie totale di 0–100 Ω come analisi di sensibilità. Modello statico, senza carico del ricevitore, transitori o corrente di perdita. La finestra indicativa di richiesta 0,08–0,25 della tensione logica resta da qualificare includendo soglie, perdite, rumore, corto non ideale, ESD, alimentazioni parziali e accensione. Un guasto resistivo interno alla finestra può imitare il comando: serve un interblocco separato e uno stato inattivo al reset, anche se il livello analogico sembra valido. Il circuito di ricezione e il comando TX restano da progettare. Le netlist native verificano contatto, terminazione, resistenza serie e pull-up; ERC invariato a 6 errori MAIN e 4 FRONT sulle reti ancora aperte.
