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
