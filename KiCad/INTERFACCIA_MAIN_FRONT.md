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

Intervalli calcolati ai vertici delle tolleranze ±1% e con resistenza serie totale di 0–100 Ω come analisi di sensibilità. Modello statico, senza carico del ricevitore, transitori o corrente di perdita. La finestra indicativa di richiesta 0,08–0,25 della tensione logica resta da qualificare includendo soglie, perdite, rumore, corto non ideale, ESD, alimentazioni parziali e accensione. Un guasto resistivo interno alla finestra può imitare il comando: serve un interblocco separato e uno stato inattivo al reset, anche se il livello analogico sembra valido. Il ricevitore candidato è ora nello schema MAIN. L'interblocco e il comando TX restano da progettare. Le netlist native verificano contatto, terminazione, resistenza serie e pull-up; ERC invariato a 6 errori MAIN e 4 FRONT sulle reti ancora aperte.

## Ricevitore candidato su MAIN

U101 Texas Instruments LM2903P, PDIP-8, stato OEM ACTIVE. Due uscite open collector unite con pull-up R107 generano PTT_WINDOW_VALID. La prima scarica l'uscita sotto la soglia bassa, la seconda sopra la soglia alta. I due ingressi di misura vedono PTT_SCALED tramite R102/R103 e C101. La scala circa 1:2 tiene la linea aperta sotto il limite di modo comune con una rail candidata nominale da 5 V. Il partitore delle soglie e il pull-up condividono la futura rail logica MAIN.

Calcolo statico normalizzato a MAIN_LOGIC_SUPPLY, resistori ±1%, resistenza serie totale 0–100 Ω, senza bias, offset e transitori: short 0–0, pressed 0.07379–0.08142, idle 0.23905–0.24999, open 0.4712–0.48118, low 0.03981–0.04136, high 0.12369–0.12809. Verificati la separazione statica delle finestre e gli otto pin U101 nella netlist KiCad, inclusa l'unione delle due uscite. La validazione strumentale, l'immunità EMC, i guasti resistivi, l'offset e il bias ai limiti termici, le protezioni di linea e il comportamento ad alimentazione parziale restano aperti. Un breve attraversamento della finestra durante guasti o accensione è possibile. Il segnale è solo un ingresso al futuro interblocco, che deve partire inattivo, qualificare la durata e richiedere uno stato di riposo valido prima di accettare una pressione. Nessun collegamento al TX.

ERC nativo: MAIN ha quattro reti ancora aperte e due pin di alimentazione U101 senza sorgente definita. FRONT conserva quattro reti aperte. Nessun DRC o prova hardware. Fonte OEM: https://www.ti.com/product/LM2903/part-details/LM2903P
