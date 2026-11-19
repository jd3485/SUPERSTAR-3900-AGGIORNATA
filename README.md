# SUPERSTAR 3900 CON AGGIORNAMENTI

**Progetto radio Connex / Superstar 3900 aggiornato · due PCB THT MAIN + FRONT · KiCad · montaggio manuale PCBWay**

> **STATO 19 novembre 2026 — CAD CANDIDATO, NON FABBRICABILE.** La home `main` contiene documentazione e indici. Schemi e PCB effettivi si trovano nella [PR #1 in bozza](https://github.com/jd3485/SUPERSTAR-3900-AGGIORNATA/pull/1), ramo `cad/avvio-main-front`. **Non ancora integrati su main.**

## Cruscotto avanzamento

| Area | Stato verificato | Percorso |
|---|---|---|
| Mandato / regole | Documentazione integrata su `main` | [AGENTS.md](AGENTS.md) |
| Specifiche funzionali | REQ-01–14 **candidate sul ramo PR** | [Indice specifiche](01_Specifiche/README.md) |
| PCB MAIN | Schema e PCB candidate; **44 impronte THT presenti**, 18 ancora mancanti nel checkpoint | [Indice KiCad](KiCad/README.md) |
| PCB FRONT | Schema e PCB candidate; **4 componenti** posizionati e collegati | [Indice KiCad](KiCad/README.md) |
| Filtri RX / conversione / IF AM | Primi stadi progettati, modelli e netlist preliminari; non validati al banco | [Percorso RX candidato](https://github.com/jd3485/SUPERSTAR-3900-AGGIORNATA/tree/cad/avvio-main-front/KiCad/RX) |
| Sintonia | Mappa candidata di 240 canali base; estensioni a 271 da verificare | [Sintonia candidata](https://github.com/jd3485/SUPERSTAR-3900-AGGIORNATA/tree/cad/avvio-main-front/KiCad/Sintonia) |
| Verifiche CAD | **ERC MAIN 10 errori; FRONT 4**; DRC diagnostici, non finali | [Indice verifiche](Verifiche/README.md) |
| PCBWay / prototipo | **NON AUTORIZZATO**; nessuna PCB produttiva pronta | [Sicurezza](AGENTS.md#sicurezza) |

I numeri della MAIN/FRONT riportano l'**ultimo checkpoint del ramo candidato**, non la versione approvata di `main`. Un pad collegato nel layout parziale non equivale a scheda completa o validata.

## Versioni / milestone

| Milestone | Descrizione | Stato |
|---|---|---|
| **V0.0 — Bootstrap** | Direttiva, checkpoint, ingresso di ripresa | **Su `main`** |
| **V0.1 — MAIN/FRONT WIP** | Requisiti, primi schemi, prime PCB, PTT, alimentazione logica, RX/IF | **PR #1 DRAFT, NON MERGED** |
| **V0.2 — Integrazione tecnica** | Completamento dei percorsi e delle interfacce, qualifiche e regressioni | **Da realizzare** |
| **V1.0 — CAD pronto alla revisione di fabbricazione** | Schemi e PCB complete, ERC/DRC applicabili, BOM OEM, verifica indipendente | **Non raggiunta** |

Queste sigle sono **milestone organizzative** e non indicano versioni CAD rilasciate. La storia tecnica resta nei commit, nella PR e nel checkpoint.

## Navigazione repository

- [00_Gestione_Progetto — stato canonico e direttive](00_Gestione_Progetto/WORK_STATO_CORRENTE.md)
- [01_Specifiche — requisiti e decisioni](01_Specifiche/README.md)
- [KiCad — MAIN / FRONT / RX / Sintonia](KiCad/README.md)
- [Verifiche — ERC, netlist, DRC, modelli](Verifiche/README.md)
- [AGENTS.md — mandato, controlli e autorizzazioni](AGENTS.md)
- [PR #1 — lavoro CAD in corso](https://github.com/jd3485/SUPERSTAR-3900-AGGIORNATA/pull/1)

## Prossimi passi

Completare la catena RF/IF e la scelta del dispositivo RF THT secondo rumore, blocco e intermodulazione; chiudere alimentazioni, PTT e connessioni tra schede; trasferire sul PCB le impronte mancanti; qualificare componenti OEM attivi; correggere gli ERC, completare le PCB e verificare i DRC. Integrare la PR solo rispettando i gate e le autorizzazioni previsti.

**Vincoli permanenti:** NO FAB · NO GERBER DI PRODUZIONE · NO ORDINI PCB · NO TX · NO BATTERIA · NO VEICOLO, finché non espressamente autorizzati dopo le verifiche.

### Ripresa da una nuova chat

«Riprendi `jd3485/SUPERSTAR-3900-AGGIORNATA` da `main`, leggi `AGENTS.md`, `00_Gestione_Progetto/WORK_STATO_CORRENTE.md` e la PR aperta, verifica lo SHA reale e procedi».
