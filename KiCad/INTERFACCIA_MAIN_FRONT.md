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

U101 Texas Instruments LM2903P, PDIP-8, stato OEM ACTIVE. Due uscite open collector unite con pull-up R107 generano PTT_WINDOW_VALID. La prima scarica l'uscita sotto la soglia bassa, la seconda sopra la soglia alta. I due ingressi di misura vedono PTT_SCALED tramite R102/R103 e C101. La scala circa 1:2 tiene la linea aperta sotto il limite di modo comune con la rail candidata nominale da 5 V generata da U102. Il partitore delle soglie e il pull-up condividono la rail logica MAIN.

Calcolo statico normalizzato a MAIN_LOGIC_SUPPLY, resistori ±1%, resistenza serie totale 0–100 Ω, senza bias, offset e transitori: short 0–0, pressed 0.07379–0.08142, idle 0.23905–0.24999, open 0.4712–0.48118, low 0.03981–0.04136, high 0.12369–0.12809. Verificati la separazione statica delle finestre e gli otto pin U101 nella netlist KiCad, inclusa l'unione delle due uscite. La validazione strumentale, l'immunità EMC, i guasti resistivi, l'offset e il bias ai limiti termici, le protezioni di linea e il comportamento ad alimentazione parziale restano aperti. Un breve attraversamento della finestra durante guasti o accensione è possibile. Il segnale è solo un ingresso al futuro interblocco, che deve partire inattivo, qualificare la durata e richiedere uno stato di riposo valido prima di accettare una pressione. Nessun collegamento al TX.

ERC nativo: MAIN ha quattro reti ancora aperte. L'ingresso di U102 e il ritorno comune attendono la sorgente a monte; U101 pin 8 è ora pilotato da U102 pin 3. FRONT conserva quattro reti aperte. Nessun DRC o prova hardware. Fonte OEM: https://www.ti.com/product/LM2903/part-details/LM2903P

## Alimentazione logica candidata

U102 è il TI LM7805CT/NOPB in TO-220 a tre terminali, in produzione secondo il datasheet OEM. C103 da 220 nF e C104 da 100 nF sono i condensatori locali di ingresso e uscita. C102 resta il disaccoppiamento di U101. MAIN_PROTECTED_DC è l'uscita della selezione locale a diodi per il ramo logico. CONTROL_RETURN è il ritorno locale di questo blocco; la relazione con il ritorno di potenza e FRONT_RETURN resta da definire al punto di distribuzione.

Verificati nella netlist pin 1 ingresso, pin 2 ritorno, pin 3 uscita, le due capacità e il collegamento a U101, oltre al riferimento di impronta TO-220. Impronta candidata, con montaggio e dissipazione da verificare. La verifica termica richiede tensione massima, corrente effettiva, bias interno e condizioni di montaggio: P ≈ (Vin − 5 V) × Iout + Vin × Iq. Perdita di regolazione, scarica inversa, sequenza di accensione e compatibilità con il filtro/protezioni a monte restano aperte. Fonte OEM: https://www.ti.com/lit/ds/symlink/lm340.pdf

### Selezione locale delle sorgenti

D101 e D102 combinano le due sorgenti DC del ramo logico con catodi comuni su MAIN_PROTECTED_DC. L'anodo D101 riceve esclusivamente la bassa tensione DC di una futura sorgente AC/DC isolata. L'anodo D102 riceve la DC esterna dopo le protezioni a monte. C105, 1 µF candidato, è il serbatoio locale sul nodo comune. La tensione effettiva è determinata dalla sorgente che prevale dopo la caduta sul rispettivo diodo. Non è prevista una priorità garantita e la corrente inversa di perdita non è nulla.

D101/D102 sono candidati onsemi 1N5819RLG, assiali, 40 V, 1 A nominale secondo OEM. L'impronta candidata DO-41 ha pad passanti 1 (catodo) e 2 (anodo). La netlist verifica polarità, nodo comune e collegamento al regolatore e ai condensatori. Da qualificare ciclo produttivo del codice ordinabile, caduta diretta e perdita a temperatura, margine di dropout, corrente e dissipazione. L'OR a diodi riguarda esclusivamente il ramo logico e non costituisce la distribuzione di potenza RF. Il collegamento dei ritorni, i limiti di sorgente, le protezioni esterne e le condizioni di commutazione richiedono il progetto a monte.

ERC MAIN: sei reti aperte, di cui due relative alle sorgenti candidate, e due errori di alimentazione all'ingresso U102 e al ritorno. Nessun collegamento fittizio per sopprimerli. Fonte OEM: https://www.onsemi.com/download/data-sheet/pdf/1n5817-d.pdf

## Trasferimento del collegamento PTT sulle PCB candidate

Le PCB includono ora J101 e J201 con impronte candidate JST XH verticali a sei poli, identiche per il cablaggio pin a pin. I pin 5 (CONTROL_RETURN) e 6 (PTT_SENSE) raggiungono il circuito PTT su entrambe le schede. I pin 1–4 attendono gli endpoint interni. Su MAIN sono posizionati e collegati anche C101 (10 nF, filtro del segnale) e C102 (100 nF, disaccoppiamento U101). Le due impronte radiali da 2,50 mm e i connettori richiedono qualifica meccanica e di produzione. Prima di fissare il cablaggio verificare corrente FRONT, sezione fili, contatti, verso del pin 1 alle due estremità e spazio di estrazione. SW201 e il consenso TX restano aperti.

Confronto delle due netlist esportate: corrispondenza dei sei pin e connessioni elettriche invariate. Verificati tutti i pad presenti contro le netlist. MAIN ha 11 impronte e FRONT 3. DRC con parità: zero pad scollegati fra quelli presenti, assenti entrambi i contorni, mancanti 34 impronte MAIN e 1 FRONT. ERC nativo: 10 errori MAIN, 4 FRONT. Nessun ordine o prova fisica.

## Collegamento del microfono al rilevatore PTT

J202 porta il contatto normalmente aperto del microfono alla FRONT tramite un cablaggio interno candidato. Pin 1 CONTROL_RETURN, pin 2 MIC_PTT_KEY. Il pulsante fisico si trova nel microfono. J202 è un connettore interno a due vie e la presa esterna multipolare rimane da definire. R202 (2,2 kΩ) è in serie fra PTT_SENSE e MIC_PTT_KEY. R201 (10 kΩ) rimane fra PTT_SENSE e CONTROL_RETURN. La posizione di R202 sul lato segnale permette la chiusura verso il comune del microfono. Conservare il riferimento di controllo durante il progetto dell'audio e verificare le correnti di schermo prima di raccordare i ritorni.

A 5 V nominali, con il carico di 200 kΩ del partitore MAIN, il modello resistivo dà 1,220 V a PTT_SCALED a contatto aperto e 0,379 V a contatto chiuso. Un corto fra i fili di J202 equivale al tasto premuto, mentre un corto diretto PTT_SENSE–CONTROL_RETURN sul fascio interscheda dà 0 V. Il rilevamento a finestra da solo non può discriminare il primo guasto. Gestire tale caso e la richiesta già presente all'accensione nella progettazione dell'interblocco TX.

Il manuale [Super Star 3900 Mk1](https://www.rigpix.com/cbfreeband/superstar_3900mk1_manual.pdf) documenta una presa microfonica a quattro poli. Verificare variante export, orientamento e pin della presa reale prima di congelare il cablaggio. Audio e commutazione RX restano da integrare.

## Finestra di rilascio PTT su MAIN

Il comparatore doppio U103 legge PTT_SCALED e confronta il segnale con due soglie indipendenti dalla finestra di pressione U101. I collettori aperti dei pin 1 e 7 condividono il pull-up R123. PTT_RELEASE_VALID è alto entro la finestra di rilascio a regime. R120–R122 formano il partitore da 6,81 / 1,40 / 1,80 kΩ. C121 disaccoppia l’alimentazione. Per LM2903P Texas Instruments indica PDIP attivo. [Dati OEM](https://www.ti.com/product/LM2903/part-details/LM2903P).

A 5 V, sulle 256 combinazioni degli estremi ±1% di R101–R103, R201–R202 e R120–R122, il modello resistivo ideale fornisce 1,195–1,244 V a riposo, 0,369–0,390 V premuto, 2,356–2,406 V a FRONT scollegata e 0 V con corto diretto sul fascio. Soglia inferiore 0,884–0,914 V, superiore 1,576–1,621 V. Metodo: Vscaled/Vcc = [R103/(R102+R103)] / [1+R101·(Gfront+1/(R102+R103))], con Gfront=1/R201 a riposo e 1/R201+1/R202 premuto. Il minimo margine resistivo del rilascio supera 0,28 V. Il calcolo non include offset, correnti di polarizzazione dei quattro ingressi sul nodo scalato, tolleranza della sorgente, temperatura, RF o transitori.

La futura memoria di armamento dovrà osservare alimentazione valida e rilascio stabile prima di accettare una nuova pressione, con inibizione durante reset e brownout. PTT_RELEASE_VALID e PTT_WINDOW_VALID non pilotano la catena TX. Un corto ai capi del tasto avvenuto dopo l’armamento è ancora indistinguibile da una pressione. Verificare filtraggio temporale, tempi di salita e guasti prima di qualificare l’interblocco.

## Alimentazione locale della logica sulla PCB MAIN

Su MAIN sono posizionati e collegati D101/D102, U102, C103/C104/C105 e R124. Il nodo a catodi comuni arriva al pin 1 del regolatore. Le capacità di bypass tornano al pin 2, il pin 3 alimenta la logica PTT. Nel confronto con la netlist precedente l’unica aggiunta elettrica è R124 in parallelo all’uscita. Verificati pad passanti e corrispondenza elettrica di tutte le impronte presenti.

R124 è un precarico candidato, 910 Ω ±1%, assiale da 0,25 W. La tabella 6.6 TI per LM340/LM7805 caratterizza la regolazione da 5 mA di carico. Fra 4,75 e 5,25 V la sola R124 assorbe 5,17–5,83 mA (V/R agli estremi), dissipando al massimo 30,6 mW. Questo evita di dipendere dal consumo degli altri circuiti per raggiungere il limite inferiore della prova OEM. Nel bilancio termico di U102 includere il precarico, gli altri carichi e la corrente propria. Verificare il minimo di 7,5 V al pin 1 nelle condizioni della tabella, dopo diodo, ondulazione e cablaggio. Tensione e corrente delle sorgenti, dissipatore, protezioni a monte, comportamento all’avvio e allo spegnimento restano da qualificare. I 5 V riguardano il ramo logico. Le impronte dei condensatori sono candidate in attesa di MPN e riscontro meccanico. [Texas Instruments, tabella 6.6 e note](https://www.ti.com/lit/ds/symlink/lm340.pdf).
