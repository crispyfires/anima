# ST Character Manager
## Specifica e Documentazione — v6

Applicativo desktop Python/CustomTkinter per la gestione di personaggi SillyTavern

**Versione 0.1 — Aprile 2026 — Licenza GPL v3**

---

# Parte 1 — Visione e filosofia

## Perché esiste questo applicativo

SillyTavern è uno strumento potente e flessibile per la gestione di personaggi AI in locale. Tuttavia, la sua esperienza di primo accesso rappresenta un muro per chi non ha background tecnico: setup manuale, sintassi esposta, documentazione frammentata e parziale.

ST Character Manager nasce per abbassare la soglia di ingresso — non semplificando lo strumento, ma eliminando la barriera tra l'utente e le sue funzionalità. Chi vuole capire il dettaglio può farlo; chi vuole solo usarlo ha un percorso guidato.

> *Motto del progetto: la tecnologia deve essere amica dell'utente, non nemica. La differenza tra uno strumento che usano i tecnici e uno che usano tutti non sta nella potenza — sta nell'esperienza di primo accesso.*

## A chi serve

- Utenti che vogliono creare e configurare personaggi ST senza conoscere la sintassi STScript
- Utenti che vogliono gestire la memoria persistente del personaggio senza entrare nel dettaglio tecnico
- Chiunque voglia replicare una configurazione su una nuova installazione ST in pochi click

Il target presuppone: SillyTavern installato, Node.js, Git, e la capacità di eseguire `pip install customtkinter`.

## Principi di design

- **Semplicità prima di tutto** — ogni funzione deve essere accessibile in un click o meno
- **Nessuna conoscenza tecnica richiesta** — l'utente non vede mai percorsi, variabili o sintassi
- **Blocchi indipendenti** — ogni sezione è modificabile ed esportabile separatamente
- **Esportazione diretta** — i file vanno automaticamente dove devono andare in ST
- **Mai usare la parola "modello"** nell'interfaccia utente — sempre "personaggio"

---

# Parte 2 — Architettura dell'applicativo

## Decisione architetturale fondamentale

> *L'app è un singolo file: `st_character_manager.pyw` — tutti i moduli (icone, schermate, memory manager, orchestratore) sono contenuti in un unico file. L'utente installa una dipendenza una sola volta, poi fa doppio click sul file, fine.*

## Stack tecnologico

| Componente | Tecnologia e motivazione |
|---|---|
| Linguaggio | Python 3.x — già installato nell'ecosistema ST, cross-platform |
| Interfaccia grafica | CustomTkinter (ctk) — dark theme nativo, widget moderni |
| Tkinter (tk) | Ancora usato per: `App(tk.Tk)`, `Screen0Frame`, `MainMenuFrame`, `tk.Listbox`, `tk.Spinbox`, `tk.PhotoImage`, popup conferma |
| Formato dati | JSON — formato nativo ST per card, lorebook e Quick Reply |
| Configurazione app | `config.json` locale — salva percorso ST e preferenze utente |
| File distribuzione | `st_character_manager.pyw` — file unico, doppio click su Windows |
| Licenza | GPL v3 |
| Dipendenza esterna | `customtkinter` — `pip install customtkinter` |

## Dimensioni del file

**~4043 righe** — file unico.

## DPI Awareness

All'avvio, prima di qualsiasi import grafico, viene richiesto `SetProcessDpiAwareness(2)` (o fallback `SetProcessDPIAware()`) tramite `ctypes.windll` per garantire nitidezza su monitor ad alta risoluzione su Windows.

## Inizializzazione CTk

```python
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.3)   # leggibilità testi
```

Se `customtkinter` non è installato, `_CTK_OK = False` e la dashboard mostra un messaggio di installazione al posto del contenuto.

## Palette colori — Dark theme

| Costante | Valore | Uso |
|---|---|---|
| `BG` | `#1e1e2e` | Sfondo principale |
| `BG2` | `#2a2a3e` | Sfondo secondario / sidebar |
| `BG_OK` | `#1e2e1e` | Feedback campo compilato (non più usato attivamente) |
| `FG` | `#cdd6f4` | Testo principale |
| `ACCENT` | `#cba6f7` | Viola — pulsanti avanzamento, highlight |
| `GREEN` | `#a6e3a1` | Feedback positivo |
| `RED` | `#f38ba8` | Errori, avvisi |
| `GRAY` | `#6c7086` | Testo secondario, separatori |
| `BTN_BG` | `#313244` | Sfondo pulsanti |
| `BTN_HO` | `#45475a` | Hover pulsanti |

`_INIT_COLORS` — 5 coppie (bg, fg) per gli avatar iniziale nella sidebar.

## Architettura avvio — Decisione definitiva

**Una sola finestra `tk.Tk()` che cambia contenuto tramite Frame.**

- `App(tk.Tk)` è l'unica finestra principale — sempre visibile, mai nascosta
- Al primo avvio (nessun `st_folder` in `config.json`) carica `Screen0Frame` inline
- Dopo conferma percorso, distrugge il frame e carica `MainMenuFrame`
- Dalle volte successive carica direttamente `MainMenuFrame`
- Le schermate wizard e di utilità sono `ctk.CTkToplevel` figli di `App`
- Dimensione finestra principale: 660×380 (primo avvio) → 1100×640 (menu)

## Flusso applicativo

**Primo avvio:**
```
App → Screen0Frame (inline) → save config.json → MainMenuFrame
```

**Wizard Nuovo personaggio:**
```
Screen0b → Screen1 → Screen1b → Screen2 → Screen2b → Screen2c →
Screen2d → Screen2e → Screen2f → Screen3 → ScreenComplete
```

**Wizard Modifica personaggio:**
```
Screen1b → Screen2 → Screen2b → Screen2c → Screen2d → Screen2e → Screen2f → Screen3 → ScreenComplete
```
(salta Screen0b e Screen1 — genere e nome già noti dalla card esistente)

---

# Parte 3 — Struttura interna del file

```
st_character_manager.pyw
├── Palette colori (dark theme) + _INIT_COLORS (5 coppie per avatar iniziali)
├── Icone base64 (ICON_STEP1_MENU, ICON_STEP2_AUTHORNOTE, ICON_STEP3_COPY, ICON_STEP4_CLOSE)
├── Costanti
│   ├── VARIABILI = ["umore", "nota", "tempo", "ospiti", "storia"]
│   ├── VARIABILI_LABEL                             ← per retrocompatibilità
│   ├── _QR_EMOJI_MAP                               ← emoji per Quick Reply
│   ├── _QR_PROMPTS                                 ← prompt /input per QR
│   ├── SUGGERIMENTI_ASPETTO / CONTESTO / PRIMO / PERSONALITY
│   ├── SUGGERIMENTI_SYSTEM_PROMPT
│   ├── SUGGERIMENTI_MES_EXAMPLE
│   └── SUGGERIMENTI_ALTERNATE_GREETINGS            ← 3 saluti M/F con {{user}}
├── Config manager
│   ├── load_config()
│   ├── save_config(data)
│   └── get_st_user_folder(st_folder)
├── Memory / Install manager
│   ├── generate_authornote()
│   ├── write_authornote_file()
│   ├── list_authornote_files()
│   ├── list_character_files()
│   ├── _read_character_data()
│   ├── _read_quickreply_variables()     ← regex /setglobalvar key=, supporta custom
│   ├── _read_quickreply_umori()
│   ├── _detect_genere()
│   ├── _qr_entry()
│   ├── generate_quickreply_json()       ← generico, gestisce variabili custom
│   ├── generate_character_json()
│   ├── _get_png_dimensions()
│   ├── _write_character_png()
│   └── install_character()
├── Lorebook manager (statico)
│   ├── read_lorebook_file()
│   ├── generate_lorebook_json()
│   ├── write_lorebook_file()
│   └── _set_character_world()
├── Lorebook dinamico manager
│   ├── _LORE_DIN_LABEL + _LORE_DIN_LABEL_REV
│   ├── _lore_din_content_default()
│   ├── generate_lorebook_dinamico_entries()
│   ├── read_lorebook_dinamico_file()
│   ├── generate_lorebook_dinamico_json()
│   └── write_lorebook_dinamico_file()
├── Widget helpers tk (btn_annulla, btn_avanti, _center_toplevel)
│   └── Ancora usati da ScreenLorebook, ScreenLorebookDinamico, Screen4
├── WizardRunner
├── PopupLampadina    — ctk.CTkToplevel
├── PopupGreeting     — ctk.CTkToplevel
│
├── ── SCHERMATE WIZARD — tutte ctk.CTkToplevel ─────────────────
├── Screen0b   — scelta genere M/F
├── Screen1    — nome personaggio
├── Screen1b   — immagine (preview frame tk per PhotoImage)
├── Screen2    — aspetto e carattere
├── Screen2b   — contesto e primo messaggio
├── Screen2c   — personalità
├── Screen2d   — istruzioni / system_prompt
├── Screen2e   — esempi di dialogo
├── Screen2f   — saluti alternativi (listbox tk + CTkTextbox)
├── Screen3    — memoria e stati d'umore
│   └── _popup_aggiungi: ctk.CTkToplevel con CTkEntry
│
├── ── SCHERMATE UTILITÀ — tutte ctk.CTkToplevel ────────────────
├── ScreenComplete          — riepilogo post-installazione
├── ScreenInfo              — info personaggio selezionato
├── ScreenInfoGenerali      — Info → Info generali (link GitHub cliccabile)
├── ScreenLorebook          — crea/modifica lorebook statico
├── ScreenLorebookDinamico  — crea/modifica lorebook dinamico
├── Screen4                 — inietta Author's Note
│
├── ── ECCEZIONI ARCHITETTURALI (nessun equivalente CTk) ────────
│   · tk.Listbox      — Screen2f, Screen3, ScreenLorebook, ScreenLorebookDinamico
│   · tk.Spinbox      — ScreenLorebook, ScreenLorebookDinamico
│   · tk.PhotoImage + tk.Label — Screen1b, ScreenInfo, Screen4
│
├── Screen0Frame   — primo avvio inline (tk.Frame dentro App)
├── WIZARD_STEPS_NUOVO / WIZARD_STEPS_MODIFICA
├── MainMenuFrame  — menubar nativa + dashboard CTk (tk.Frame)
└── App(tk.Tk) + Entry point
```

---

# Parte 4 — Menu principale

## Struttura menubar

| Voce | Sottovoci |
|---|---|
| **Crea** | Nuovo personaggio · Nuovo Lorebook · Nuovo Lorebook dinamico |
| **Visualizza** | Info personaggio |
| **Modifica** | Inietta le note dell'autore · *(separatore)* · Modifica Personaggio · Modifica Lorebook · Modifica Lorebook dinamico |
| **Impostazioni** | Resetta percorso S.T. · Resetta personaggio · Resetta Lorebook · Resetta Lorebook dinamico |
| **Info** | Info generali ✅ (ScreenInfoGenerali — versione, autore, licenze, link GitHub cliccabile) |

Tutte le azioni distruttive (Resetta, Nuovo personaggio) passano per `_chiedi_conferma`.

## Dashboard — Master/Detail

Layout a due colonne (1100×640):

- **Sidebar sinistra** (230px, `CTkScrollableFrame`): lista personaggi installati. Ogni voce mostra avatar (iniziale colorata 34×52px o thumbnail PNG) + nome. Header fisso "I TUOI PERSONAGGI".
- **Pannello dettaglio destra**: quando si seleziona un personaggio, mostra thumbnail, nome + data installazione, pulsanti azione in due colonne.

## Popup conferma (`_chiedi_conferma`)

Toplevel tk nativo con sfondo grigio sistema (stile OS). Accetta parametro opzionale `messaggio=` che mostra il nome del personaggio in **rosso grassetto MAIUSCOLO**. Focus automatico su "No", Enter/Escape = No.

---

# Parte 5 — Specifica delle schermate

## Screen0Frame — Selezione cartella ST *(primo avvio, inline)*

Appare solo al primo avvio come frame inline nell'`App`. Chiede dove ha installato SillyTavern con `filedialog.askdirectory`. Salva il percorso in `config.json`. Non appare mai più. Dimensione finestra: 660×380.

## Screen0b — Scelta genere

`ctk.CTkToplevel`. Radio button M/F (`CTkRadioButton`). Mostra preview degli stati d'umore declinati in tempo reale al cambio selezione. Annulla torna al menu principale.

## Screen1 — Nome personaggio

`ctk.CTkToplevel`. Campo `CTkEntry` altezza 44px, centrato. Invio da tastiera equivale al click sul pulsante. Nome obbligatorio — errore se vuoto. Confermato il nome, non è modificabile senza creare un nuovo personaggio.

## Screen1b — Immagine personaggio

`ctk.CTkToplevel`. Permette di selezionare un file PNG come immagine del personaggio. Preview tramite `tk.PhotoImage` + `tk.Label` (eccezione architetturale mantenuta). Campo opzionale — si può procedere senza immagine.

## Screen2 — Aspetto e carattere

`ctk.CTkToplevel`. `CTkTextbox` ridimensionabile. Icona lampadina 💡 apre `PopupLampadina` con testo suggerito declinato per genere. Conferma inserisce il testo e mostra label `lbl_ok` di feedback.

## Screen2b — Contesto e primo messaggio

`ctk.CTkToplevel`. Due `CTkTextbox` nella stessa schermata: contesto di vita e primo messaggio. Ogni blocco ha la propria lampadina 💡. Validazione su entrambi i campi prima di procedere.

## Screen2c — Personalità

`ctk.CTkToplevel`. `CTkTextbox`. Lampadina 💡 con suggerimento `SUGGERIMENTI_PERSONALITY`.

## Screen2d — Istruzioni / System prompt

`ctk.CTkToplevel`. `CTkTextbox`. Lampadina 💡 con `SUGGERIMENTI_SYSTEM_PROMPT` (sintassi parlato/azioni/pensieri).

**Template definitivo:**
```
Il parlato va sempre tra virgolette "così".
Le azioni, i gesti e le descrizioni fisiche vanno tra asterischi *così*.
I pensieri o commenti interni vanno tra parentesi quadre [così].
Non mescolare mai i tre formati.
```

## Screen2e — Esempi di dialogo

`ctk.CTkToplevel`. `CTkTextbox`. Lampadina 💡 con `SUGGERIMENTI_MES_EXAMPLE`.

## Screen2f — Saluti alternativi

`ctk.CTkToplevel`. `tk.Listbox` (eccezione architetturale) per la lista dei saluti + `CTkTextbox` per l'editor. Lampadina 💡 con `SUGGERIMENTI_ALTERNATE_GREETINGS` (3 varianti M/F con `{{user}}`). Pulsanti Aggiungi / Rimuovi / Modifica.

## Screen3 — Memoria e stati d'umore

`ctk.CTkToplevel`. Due sezioni:

- **Stati d'umore**: `tk.Listbox` modificabile (Aggiungi via `_popup_aggiungi` CTkToplevel / Rimuovi). Default declinati per genere: Felice, Malinconico/a, Arrabbiato/a, Curioso/a, Ansioso/a.
- **Variabili attive**: checkbox (`CTkCheckBox`) per umore, nota, tempo, ospiti, storia. Supporta variabili custom aggiunte dall'utente.

Al click su **[ Salva e installa in SillyTavern ]** genera e installa: character PNG, Quick Reply JSON, Author's Note, e opzionalmente Lorebook/Lorebook dinamico.

## ScreenComplete — Riepilogo post-installazione

`ctk.CTkToplevel`. Mostra i file installati. `CTkTextbox` con istruzioni per abilitare il set Quick Reply in ST. Pulsante "Ho capito, chiudi".

## ScreenInfo — Info personaggio

`ctk.CTkToplevel`. Mostra i dati della character card selezionata: thumbnail (`tk.PhotoImage`), nome, descrizione, contesto, system prompt, variabili Quick Reply attive.

## ScreenInfoGenerali — Info generali

`ctk.CTkToplevel`. Accessibile da menu Info → Info generali. Mostra: nome progetto (Anima), sottotitolo, versione v0.1, autore Threadripper, licenza codice (GPL v3), licenza documentazione (CC BY-SA 4.0), Python richiesto, link GitHub cliccabile (sottolineato, colore accent, cursore a mano, apre il browser su `https://github.com/Threadripper2/anima`).

## ScreenLorebook — Lorebook statico

`ctk.CTkToplevel`. Gestione voci lorebook: `tk.Listbox` per la lista voci, `tk.Spinbox` per position/order/depth, `CTkTextbox` per contenuto. Crea/Modifica/Elimina voci. Salva in `worlds/{nome}.json`.

## ScreenLorebookDinamico — Lorebook dinamico

`ctk.CTkToplevel`. Struttura analoga a ScreenLorebook. Gestisce voci con `constant: True` e `keys: []` che iniettano le variabili di scena ad ogni messaggio senza trigger. Salva in `worlds/{nome}_dinamico.json`.

## Screen4 — Inietta le note dell'autore

`ctk.CTkToplevel`. Voce autonoma del menu Modifica, richiamabile in qualsiasi momento. Legge il file authornote installato. Se ci sono più personaggi, mostra `CTkComboBox` per selezionare quale caricare. Ricostruisce le variabili attive dal JSON Quick Reply. Auto-genera l'Author's Note se non ne esiste una salvata. Permette la modifica del testo prima della copia. Salva il file e copia negli appunti.

Guida in 4 passi con icone base64 estratte da ST:
1. Apri il menu principale (icona ≡ in basso a sinistra)
2. Clicca su Author's Note
3. Incolla il testo copiato nel campo
4. Chiudi il pannello con ✕

---

# Parte 6 — Blocchi funzionali

## Blocco 1 — Scheda Personaggio (character PNG)

Genera il file PNG con JSON incorporato nel formato nativo ST (`_write_character_png`).

**Campi della card:**

| Campo | Provenienza |
|---|---|
| `name` | Screen1 |
| `description` | Screen2 |
| `scenario` | Screen2b (contesto) |
| `first_mes` | Screen2b (primo messaggio) |
| `personality` | Screen2c |
| `system_prompt` | Screen2d |
| `mes_example` | Screen2e |
| `alternate_greetings` | Screen2f |
| Immagine thumbnail | Screen1b (opzionale) |

**Percorso installazione:**
`{st_folder}/characters/{nome}.png`

## Blocco 2 — Lorebook statico

Voci classiche con `keys` e `content`. Ogni voce viene associata alla character card tramite `extensions.world`.

**Percorso:** `{st_folder}/data/{utente}/worlds/{nome}.json`

## Blocco 3 — Lorebook dinamico

Voci con `constant: True` e `keys: []` — iniettate ad ogni messaggio senza trigger. Il contenuto usa `{{getglobalvar::{nome}_{var}}}` per leggere le variabili scritte dai Quick Reply.

**Percorso:** `{st_folder}/data/{utente}/worlds/{nome}_dinamico.json`

## Blocco 4 — Sistema Memoria (Quick Reply)

Un file JSON dedicato per personaggio nel formato nativo ST. Un file per personaggio — non un Default.json condiviso — per evitare che in ST appaiano i pulsanti di tutti i personaggi in ogni chat.

**Ordine bottoni:**
⏰ Tempo → 👥 Ospiti → 💾 Umore → 📝 Nota → 📖 Storia → 🔄 Aggiorna → 🧠 Inietta

| Label | Variabile | Quando usarlo |
|---|---|---|
| ⏰ Tempo | `{nome}_tempo` | Inizio scena |
| 👥 Ospiti | `{nome}_ospiti` | Quando entra qualcuno |
| 💾 Umore | `{nome}_umore` | Fine sessione |
| 📝 Nota | `{nome}_nota` | Fine sessione |
| 📖 Storia | `{nome}_storia` | Dopo momento importante |
| 🔄 Aggiorna | `{nome}_umore` + `{nome}_nota` | Ogni 10-15 scambi |
| 🧠 Inietta | — (input bar) | Inizio sessione |

`disableSend` impostato a `False` direttamente nel JSON generato.

**Percorso:** `{st_folder}/data/{utente}/QuickReplies/{nome}.json`

**Variabili custom:** Screen3 permette di aggiungere/rimuovere variabili oltre alle 5 default. `_read_quickreply_variables` scansiona con regex `/setglobalvar key={nome}_(\w+)`.

## Blocco 5 — Author's Note

Testo generato automaticamente in base alle variabili attive.

**Template definitivo:**
```
[LINGUA: rispondi ESCLUSIVAMENTE in italiano. ...]
[FORMATO: il parlato va SEMPRE tra virgolette "così", le azioni tra *asterischi*, ...]
[Stato di {nome}: umore={{getglobalvar::{nome}_umore}} | tempo={{getglobalvar::{nome}_tempo}} | ...]
```

**Percorso:** `{st_folder}/data/{utente}/st_character_manager/{nome}_authornote.txt`

La cartella utente viene rilevata automaticamente: prima sottocartella di `data/` che non inizia con `_`.

---

# Parte 7 — Decisioni UI/UX

| Elemento | Decisione |
|---|---|
| Linguaggio | Nessun termine tecnico. Parole di tutti i giorni. Mai "modello" — sempre "personaggio". |
| Genere | Screen0b chiede M/F. Tutta l'app si adatta: testi, umori, etichette, suggerimenti. |
| Nome bloccato | Confermato in Screen1, non modificabile nel wizard. Per cambiarlo: Modifica personaggio. |
| Feedback campo | Label `lbl_ok` verde su compilazione completata. |
| Textarea | Tutti i campi testo lungo sono `CTkTextbox` wrap="word". |
| Lampadina 💡 | Click apre `PopupLampadina` con testo precompilato declinato per genere. Conferma / Annulla. |
| Umori default | Felice, Malinconico/a, Arrabbiato/a, Curioso/a, Ansioso/a — declinati al genere. |
| Back nel wizard | Dati preservati su tutta la catena. Funziona sia in Nuovo che in Modifica. |
| File distribuzione | `st_character_manager.pyw` — doppio click su Windows, no terminale. |
| Quick Reply | Un file JSON per personaggio, non un Default condiviso. |
| Popup conferma | `tk.Toplevel` sfondo grigio sistema, icona ?, No a sinistra con focus, Enter/Escape = No. |
| Widget scaling | `ctk.set_widget_scaling(1.3)` per leggibilità ottimale. |
| Saluti alternativi | `PopupGreeting` (`ctk.CTkToplevel`) con 3 varianti M/F precompilate con `{{user}}`. |

---

# Parte 8 — Pattern tecnici consolidati

## Pattern navigazione wizard (CTkToplevel)

```python
def _avanti(self):
    self.destroy()
    self.callback_avanti(dati)

def _annulla(self):
    cb = self.callback_annulla
    self.destroy()
    cb()
```

`destroy()` **sempre prima** del callback. Mai usare `after()` per la navigazione tra finestre — causa perdita del focus su Windows quando `grab_set()` è attivo.

## Migrazione Tkinter → CustomTkinter

| Vecchio | Nuovo |
|---|---|
| `tk.Toplevel` | `ctk.CTkToplevel` |
| `tk.Label(…, bg=BG, fg=COLOR)` | `ctk.CTkLabel(…, text_color=COLOR)` |
| `tk.Frame(…, bg=BG)` | `ctk.CTkFrame(fg_color="transparent")` |
| `tk.Frame(…, bg=BG2)` | `ctk.CTkFrame(fg_color=BG2, corner_radius=8)` |
| Separatore `tk.Frame(h=1)` | `ctk.CTkFrame(height=2, corner_radius=0)` + `pack_propagate(False)` |
| `tk.Entry` | `ctk.CTkEntry(fg_color=BG2, border_color=BTN_BG, corner_radius=8)` |
| Entry readonly | `ctk.CTkLabel(fg_color=BG2, anchor="w", height=36)` |
| `scrolledtext.ScrolledText` | `ctk.CTkTextbox(wrap="word", height=N)` |
| `tk.Button` | `ctk.CTkButton(fg_color=BTN_BG, hover_color=BTN_HO, corner_radius=8)` |
| `tk.Radiobutton` | `ctk.CTkRadioButton(fg_color=ACCENT, border_color=GRAY)` |
| `ttk.Combobox` | `ctk.CTkComboBox(…, command=callback)` |
| `font=("Segoe UI", N)` | `font=ctk.CTkFont(size=N)` |
| `font=("Segoe UI", N, "bold")` | `font=ctk.CTkFont(size=N, weight="bold")` |

## Eccezioni mantenute in tk (nessun equivalente CTk)

- `tk.Listbox` — Screen2f, Screen3, ScreenLorebook, ScreenLorebookDinamico
- `tk.Spinbox` — ScreenLorebook, ScreenLorebookDinamico
- `tk.PhotoImage` + `tk.Label` — Screen1b, ScreenInfo, Screen4 (icone/preview)
- `Screen0Frame` — `tk.Frame` inline nell'`App` (non Toplevel, rimane tk by design)
- Popup conferma `_chiedi_conferma` — `tk.Toplevel` nativo (stile OS)

---

# Parte 9 — Roadmap

## Stato attuale — 30 Aprile 2026

| Attività | Stato |
|---|---|
| Visione e filosofia del progetto | ✅ |
| Architettura file unico (.pyw) | ✅ |
| Struttura menu applicativo | ✅ |
| Wizard completo (10 schermate) | ✅ |
| Modifica personaggio | ✅ |
| Screen4 Author's Note | ✅ |
| Dashboard CTk Master/Detail | ✅ |
| Lorebook statico | ✅ |
| Lorebook dinamico | ✅ |
| Variabili di scena custom | ✅ |
| Funzioni Resetta (personaggio / lorebook / lorebook din.) | ✅ |
| Migrazione completa a CustomTkinter | ✅ sessione 29 Aprile notte |
| `ctk.set_widget_scaling(1.3)` | ✅ |
| Fix curselection Screen2f / Screen3 | ✅ 30 Aprile |
| Fix altezze finestre wizard (scaling 1.3) | ✅ 30 Aprile |
| Fix image_path propagation in Screen1b `_salta` | ✅ 30 Aprile |
| Fix world preservation in Modifica (`extensions.world`) | ✅ 30 Aprile |
| Info generali (ScreenInfoGenerali + link GitHub cliccabile) | ✅ 30 Aprile |
| Menu "Help" rinominato in "Info" | ✅ 30 Aprile |

## Da fare

Nessun known issue aperto. Prossimo obiettivo: preparazione repository GitHub per pubblicazione Anima v0.1.

*Documento in evoluzione — aggiornato al 30 Aprile 2026*
