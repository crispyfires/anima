# Changelog

## [0.3] - 2026-05-04

### Aggiunto
- Character's Note (Screen2d_note) con slider profondità 1-10 (extensions.depth_prompt)
- Single-instance lock per impedire istanze multiple dell'app

### Corretto
- Bug critico "PNG modificato ma ST mostra dati vecchi": rimozione chunk ccv3 obsoleti in scrittura PNG + invalidazione mirata della cache `_cache/characters` di ST
- World preservation durante Modifica personaggio
- Selezione listbox (curselection) in Screen2f e Screen3
- Propagazione image_path quando si salta Screen1b
- Refresh automatico dashboard dopo creazione personaggio
- Altezze finestre wizard ottimizzate per scaling 1.3
- ScreenComplete: bottone "Ho capito, chiudi" ora sempre visibile

### Modificato
- Titolo app aggiornato a "ANIMA - ST Character Manager"

### Note
- Sito ufficiale online: https://threadripper.io
- Le cartelle di backup create in `data/` di SillyTavern devono avere prefisso `_` per non confondere la rilevazione utente

## [0.1] - 2026-04-30

### Aggiunto
- Wizard creazione personaggio (10 schermate)
- Dashboard Master/Detail con CustomTkinter
- Sistema Quick Reply + Author's Note + variabili di scena
- Lorebook statico e dinamico
- Screen4 — Inietta le note dell'autore
- Modifica personaggio
- Funzioni Resetta
- ScreenInfoGenerali con link GitHub cliccabile

### Note
- Documentazione completa in italiano in docs/it/
- Caso studio Anita in docs/it/case-study/
