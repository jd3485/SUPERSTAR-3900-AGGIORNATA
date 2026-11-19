# Requisiti del progetto

| ID | Requisito approvato | Verifica prevista |
|---|---|---|
| REQ-01 | Replica funzionale del Connex 3900 export, sei bande e 271 canali, AM/FM/USB/LSB/CW | Confronto con documentazione storica e verifica della mappa |
| REQ-02 | Su uno o più LCD devono essere leggibili numero di canale, frequenza, SWR (ROS), potenza RF e modulazione. Numero e formato dei display da scegliere in fase di progettazione. | Confronto di canale e frequenza con la mappa di sintonia e delle letture SWR, potenza e modulazione con strumenti di riferimento durante prove autorizzate |
| REQ-03 | Accordatore manuale e misuratore di modulazione e potenza | Prova strumentale autorizzata |
| REQ-04 | Alimentazione sia AC sia DC | Prova elettrica autorizzata per ogni ingresso |
| REQ-05 | Eco, Roger beep e PA | Verifica audio e comportamento della commutazione |
| REQ-06 | Potenza regolabile, 10 W AM/FM e 20 W SSB/CW | Prova strumentale autorizzata per modo |
| REQ-07 | Componenti finali 100% THT in produzione presso l’OEM | Qualifica di MPN, package e ciclo di vita |
| REQ-08 | Due PCB KiCad complete, MAIN e FRONT | Schemi, netlist, interfacce, layout, ERC, DRC e revisione indipendente |
| REQ-09 | NO FAB, NO GERBER DI PRODUZIONE, NO ORDINI PCB, NO TX, NO BATTERIA, NO VEICOLO | Controllo delle autorizzazioni prima di ogni azione applicabile |

Fonte requisiti: richieste del committente e direttiva in ../AGENTS.md. I criteri di misura RF per modo sono candidati da formalizzare, compresi portante per AM/FM, PEP per SSB e potenza a tasto premuto per CW. Anche tensioni nominali AC/DC, limite termico, margine RF, punti esatti della mappa aggiuntiva e implementazione interna del display sono da definire o verificare. Per l'LCD vale il vincolo THT, senza eccezioni approvate.

## Comandi originali e filtraggio

**REQ-10.** Conservare tutti i comandi fisici e le funzioni operative del Connex Superstar 3900 export a 271 canali. Le dotazioni REQ-02–06 si aggiungono alla dotazione originale. Prima di congelare FRONT e cablaggio, associare ogni comando a una fonte della variante corretta, una posizione sul pannello, un circuito o ingresso di controllo e una verifica del suo effetto in RX/TX/PA secondo applicabilità.

| Provenienza | Comandi e funzioni da tracciare |
|---|---|
| Connex 3900 export documentato in Italia | Selezione dei canali e modi, tasto +10 kHz, doppio clarifier con azione RX/TX da riconciliare per comando, rosmetro incorporato. |
| Manuale Superstar 3900 MK1, da riscontrare sulla versione Connex | Accensione/volume, squelch, MIC GAIN, RF GAIN, calibrazione SWR, selettore S-RF/SWR/CAL, selettori modo/canale/banda, HI/LOW, richiamo CH9, NB/ANL, clarifier coarse/fine, PTT, ingresso tasto CW e Roger beep. Verificare anche indicazioni e prese associate. |

La fonte Connex descrive separazione RX/TX; il manuale MK1 assegna coarse a RX/TX e fine a RX. Conservare questa differenza aperta fino a una fonte specifica della versione export. Completare l'inventario con materiale originale del modello prima della chiusura meccanica. [Connex, CQ Elettronica gennaio 1988](https://www.worldradiohistory.com/INTERNATIONAL/CQ-Elettronica/CQ-Elettronica-1988-01.pdf) · [Superstar MK1, sez. III](https://www.rigpix.com/cbfreeband/superstar_3900mk1_manual.pdf)

**REQ-11.** Progettare e verificare il filtraggio dell'intera radio nelle condizioni operative richieste.

| Percorso | Criterio da dimensionare e verificare |
|---|---|
| Antenna e RF RX | Perdita utile sulle sei bande, attenuazione immagine e segnali fuori banda, impedenze reali e comportamento con segnali forti. |
| IF e audio | Selettività di canale e banda passante per modo, soppressione banda laterale indesiderata in SSB, intelligibilità e risposta ai disturbi impulsivi. Tracciare separatamente le funzioni NB/ANL. |
| TX | Filtraggio audio e di modulazione per modo; attenuazione di armoniche e spurie all'uscita RF, tenendo conto di potenza, temperatura e accordatore. |
| Alimentazioni e interfacce | Ripple e rumore condotto, accoppiamento di clock LCD/logica nei percorsi RF/IF/audio, ritorni di corrente e cablaggio MAIN–FRONT. |

Fissare obiettivi numerici tracciabili per ciascun percorso prima del congelamento. Conservare risposta calcolata o simulata e condizioni di carico; qualificare poi con misure autorizzate. Il passa-alto RX e la rete IF presenti sono stadi candidati.

## Sensibilità RX e qualità della modulazione

**REQ-12 – Alta sensibilità in ricezione.** Rilevare segnali deboli con audio intelligibile su tutte le sei bande, mantenendo la selettività e la capacità di ricevere in presenza di segnali forti vicini. Prima di congelare il front-end, costruire un bilancio di rumore e guadagno dall'antenna al demodulatore, includendo perdite di commutazione, filtro RF, conversione e IF. Usarlo per decidere guadagno e posizione del primo stadio attivo. Verificare anche il rumore introdotto da alimentazione, display e comandi.

Per il collaudo autorizzato registrare il livello RF minimo all'ingresso a 50 Ω e le condizioni: frequenza, modo, larghezza di banda, impostazioni, segnale di prova e criterio audio. In AM e FM specificare rispettivamente profondità e deviazione del segnale di prova e SINAD richiesto. In USB/LSB e CW specificare rapporto segnale/rumore audio, tono e banda di misura. Confrontare a parità di condizioni centro ed estremi delle bande. Misurare separatamente blocco e reiezione del canale adiacente.

**REQ-13 – Buona modulazione.** Riprodurre la voce con intelligibilità, basso rumore e bassa distorsione nell'intervallo utile di MIC GAIN e RF POWER. Verificare risposta microfono–RF e margine prima del clipping con eco e Roger beep inizialmente esclusi, poi controllare l'effetto del loro inserimento.

| Modo | Grandezze da misurare in collaudo autorizzato |
|---|---|
| AM | Profondità sui picchi positivi e negativi, distorsione dell'inviluppo e sovramodulazione |
| FM | Deviazione di picco, risposta audio demodulata, distorsione e banda occupata |
| USB/LSB | Intermodulazione a due toni, compressione, soppressione di portante e banda laterale indesiderata alla PEP prevista |
| CW | Tempi di salita e discesa dell'inviluppo, transitori di manipolazione e stabilità della portante |

Fissare soglie numeriche e condizioni ripetibili prima del congelamento dei blocchi interessati. Il requisito qualitativo è approvato; prestazioni raggiunte e margini saranno documentati con evidenze della fase applicabile.

## Fabbricazione e montaggio

**REQ-14 – PCB nude e saldatura manuale.** MAIN e FRONT sono destinate alla fabbricazione da PCBWay come circuiti stampati nudi. L’utente installerà e salderà personalmente i componenti THT. Per ogni impronta verificare il foro finito rispetto alla sezione massima del terminale, la piazzola e l’accesso del saldatore nella sequenza di montaggio. Indicare sulla serigrafia riferimenti, polarità, pin 1 e orientamento dei connettori. Verificare fori e distanze rispetto alle capacità del processo PCBWay scelto prima del rilascio. Ordini e file di produzione restano subordinati ad autorizzazione separata.
