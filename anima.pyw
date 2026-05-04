"""
ST Character Manager
Applicativo desktop per la gestione di personaggi SillyTavern.
Versione 0.1 — Aprile 2026 — Licenza GPL v3
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import json
import os
import sys
import base64
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    ctk.set_widget_scaling(1.3)
    _CTK_OK = True
except ImportError:
    _CTK_OK = False

# ============================================================
# PALETTE COLORI — Dark theme
# ============================================================
BG     = "#1e1e2e"
BG2    = "#2a2a3e"
BG_OK  = "#1e2e1e"
FG     = "#cdd6f4"
ACCENT = "#cba6f7"
GREEN  = "#a6e3a1"
RED    = "#f38ba8"
GRAY   = "#6c7086"
BTN_BG = "#313244"
BTN_HO = "#45475a"

_INIT_COLORS = [
    ("#2d2042", "#cba6f7"),
    ("#1e2d2a", "#a6e3a1"),
    ("#2d1e20", "#f38ba8"),
    ("#1e222d", "#89b4fa"),
    ("#2d2a1e", "#f9e2af"),
]

# ============================================================
# ICONE — base64 PNG 40x40 (estratte dagli screenshot ST)
# ============================================================
ICON_STEP1_MENU = (
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAG00lEQVR4nKWXy49cRxXGv1Ove2/f29M9PT2e"
    "hz1JZvD4nYDIg0Q2EpBVIv4II2WDCBIb2CBFEbAACfwPIHZIbBBhxwIpVjYIJVgYFHtmjD2OnbF7POPx"
    "PLru+1YdFpcZTGw8bfdZtLpbVfWr79Spr6pofn4eBwURFUXRbDaTJAmCYHFxcWZmJgzDJEmWl5fPnTvX"
    "7XbX1tYWFhbOnz9/4cKFAwcEoAZp9NhgZq3Vm29+a3l5eXFxUSm1s9P/4IPf37z5aZoWVVURAUxQBWQJ"
    "JoBR+WAxLJiInMPS0u2ydLOzL6Rp7vv+2Fjn4sW/jo+PJskWkQQA4QAGADjiBljUP58dXPePohbDxnFu"
    "DEVRi8uyTqfLTKOjh5jLeoZ7jT2QAvz6n2HABDCYJYc3l28cmo6M9sqynJp67tatz5XSzpWAeKgxpKuI"
    "cxCDSTxh4AP0MgBobRqN8Pjxk2nStraSIGgkSdZujzILIUJBWghPCCNICXJSOCVS5SolsqFSLYQg4VY3"
    "bnxpbq50baUoiTc+/7wnpZBSMUsSMViDKqAAhASIGVUElQxZXO7unWvWVTdupO12d7TTPHrs2Nebb9y9"
    "e7fb7VaVJVmCJciCKoCEAzEDPlAMoxhgd/zEzLGTz3108e8Li/88Wh3+2c9/ffa1twbpOhTYcnJl6TM/"
    "smsPeq+8MfPOd35w9rW3iiJXSh/Y99mLCwAY/b4VAi+/euxvH6/87rd/AsAMMUAM51xGvf3ts1eu/COK"
    "mp7Px09PAijLUoiD9Ty7YiIiePdWHqzdKafH5yI/XOvdu3z5kyiK9AAxlGJmGfc5jas7Kw/mj754b3X3"
    "/fd/0umMOleMjLScswDABF3AKrCUcLTXfSjnYmYv6Jw4dSZO8tV7t5N4J4rGut1od3djfX1Da8kMQEAm"
    "cAALw4qYassbZh+DGc4KwS1bbAkbPT8zpT0vDINmsxMEE0pJ5gpw4Hofs7YhsQQYoKGciwhFUWxv5MTi"
    "la++3mq3//LJn2/fvjU5OVlVbK0DKqAEGBCAYGuJHSABO1SqrbXb2/dOnjgV79ir1y8phFmWzhyZCCN/"
    "ba0vpQITAIgMbMBKiIyYwSEoHc65gLLsx8mDB/3+au/m9OHZubmp5eVr29e3JycPxUlBROAKJoPVcMqA"
    "CYwqgcqHAkupjhw5fPnyx7Ozh7/2+ktLS0srK+svv3oqy5OVlV7U0OwAaEADAiBdghj12TzUdiJCs6m7"
    "E/rMV2Z7dzd7ve33fvr9H//ol0WZK6Xpid0HBRMRM9efe1Rijjf7W15DLywsrtzZ+cWvfvjud98zxhhj"
    "Dhxw4OaqO2ZGUZSm+74vhGi1WlVVKS29QGZJlqb9NC8uXVoqBFGapczsDropBlU8nANQliXXjiVlPe/F"
    "q6tjHZ6c6o6NV81mkGWps1We50IQP3HAQcFKqbIs9zgoimKmqip27nCjgaWlNU3qm98IfD8YdMBBGjnn"
    "lFLOOSllLb0oCiJyVgq4RrMVRkl/M/njHz48few3QaRXe/cnJkbKyj2uvhwggIFTLYSw1gohalCapr4f"
    "OGuuXV2es8WXX5zf7e964aNPr3cnUBSgR8niP+inAFdVpbWuz9osy6RUQtDpM0f/de2Gr0a11rOz42Nj"
    "4/FufPrUC1XliIjxhYUmqAyVB5UPVNXMbIypqsoYUyc8yzIAQlAUjVTWZVm2ubnZbLaDILy/sWEdHDvr"
    "7CO1bF1hnHOuMIMqllLmeU5EAIIgiOOY2QGyqkwYdopC3b+/OT09srmZttvTZWndY9f34RQOqJiI6qqu"
    "bzZEJITIsuzWrc86nU67PdLtdsfGOhsbG63WyNbWlu/7Ukr1/4MGeabWqWZmIURZlkVRbG9vZ1nmnJuf"
    "f4mZhSDnmIiSJDFGF0V97eK9h9NjYqBU13KNMbVlCiGMMVmWMTORtLaqKguQtaUQKsuqIAh833eOH6nq"
    "/9baoGvMzEVRGGO01gA8zwvDMMuylZXrWus6sb7vG2M8rxHH8fr6upT11edhqtnPwdMdEvu662NAa93r"
    "9YzRnuf5vu9cgzkAKqXQbAZCCP4fMgMhIJ8OjL3H0r5x1upbrRYzW2t3d+OdnT4R1dI9z+MvmjUDyVMr"
    "rqN2rhpMREqpqanpsizzPN/d7cdx4lyVZXmSpFprfoQMuP1vTweu/TLP89q/hBDM1vOUUhSGnrWWGc5Z"
    "pZTvB845Itqr7XoS8tnBtQ4iIqKiKIlSItbaU0oaExJBKV2WRb/fl1I6V/P295W/7xzPePWx1iqliMiY"
    "FnNSFJRlqbW5c3lROGOk7wfWMsCABCpAAgqwgK1H+DdxDcoeMfr53AAAAABJRU5ErkJggg=="
)

ICON_STEP2_AUTHORNOTE = (
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAE1klEQVR4nN2YS2/TShTH5+FHnNhOorZR"
    "+iCJiESlwga+AqzYs6jEd6Cfgi0SYs9HYMOSRfcgYIMgAqlqpArLdlol9sSPmTlzF6ObGyUtkN6bLu5Z"
    "RfZ4fud/5sw5M8FPnjxB/86UUmmaYoxX+sq4BgYhNMNgjPWTmelXy88XBqwAVkq5rmsYhlIqSRKlFGNM"
    "v6KU6h9lWU4mkyRJGGO1Wq1arQLAAnU8HiulVlNMCMEYzzBak5QyiiL9vFarAYB2Mc/zyWRCCFkWsJpi"
    "hBAAmKap5c5CijGeTqemaUop4ziuVCqO4yilLMtangFjnKbpaoqVUpRSxlhZloSQ6XSqH2ZZ1ul0pJTj"
    "8bgsyzRN8zwnhFxcXFxcXOilmQdzzldTrJUJITDGWZYJIQghSZJIKSuVCkKoWq0qpabTqW3bZVneuXPH"
    "930p5XzCa+8xxquBOed6LTWeMSaEAIDBYOC6ruM4juNsbm66rgsAGxsb9Xp9Aay9Xzm5tGVZpucqioJS"
    "yjkPw1AnlG3bjuMAQJIk3759i+OYUjqf2NcJNULINM1ZdnDOLctSSpmm2ev1PM/b3Nys1WpJknz//v3k"
    "5MT3/Z2dnaIoFsJWluVqigkhcRwTQgghlNI4jouiwBhbltVut2/fvo0QGgwGw+EwiqJer3dwcNBut3Um"
    "zoPzPF8BrJQihIzHY855q9USQhRFcX5+TghpNpuWZZmmGUXRp0+fGGPtdvv+/fuu64ZhaBjG8jzoGpWL"
    "c66TmVJqmiYA2Lbd6XQGg8HXr18RQv1+f3t7++fPn77v1+t1nYaXxO/PwQghIUS1WtX1Sy8VpVQn1MnJ"
    "SRCA IMJRsQ9dohB1kz7YUSA53mWZY3H4ziOK5WK53l2YAcAxhivqq8ViqiMaGxvrmXleahBBSTQYBKI"
    "EQlHSBOcJVHAMhRQkTFIWQU35ILB5XGZq9aXvhYbGxAFUJLwA2rFDL4tQSA3GaKv98ZocK3GjgI7REq"
    "g4IiDC2CpSiNHpuI7kEi+2qyUVB2RGzGBARHBWj9Y3fggAAAbGr9mxLFiVBCIiGKgAFfopAWB7Kh7d"
    "TBxKiN1hBpCSY+0oMKCZU2J9vd5wNtYR+B7sBDHBBKRkACfJb9nV5YlTfxjXhEAAGJZc8AaqdF0HQRS"
    "gFwqvmISxLV4l2+iVXBmfnuOi0Z6dVvLUREbFIGQGh6tYHrR1sKk/Y9nEHAqmZF1ghkJIqSEg5GQAAA"
    "AASUVORK5CYII="
)

ICON_STEP3_COPY = (
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAADLklEQVR4nO2XTW8cRRCG37f6Y3e9480h"
    "tiw7ESKHHElioRyQckK5JgeQkHzAQuJncMyvAfEDEBFfMiRHIxAiV4JBDiLYQl7v7kx3F4ex17uOnZ2d"
    "XeeAUqdR90w91TVV1VXAa3kt/zdhzc9Y88P6YOccwBCCahpXohcIJqmqx88gkdLoLspNCkSgZ1pyvDgF"
    "mKSIxBiNwdra8tLSkrW23+8PBgOS3nvnXFGEEIpWZpyXlE6RFRBEDxVAq4K993meA9jc/PDu3XcXF7Nm"
    "sylCwSAPIZAQMcZIjEk1WS/GnPhm1HgkA3CK/9JoNNrt9s2bb21vb+s8ZDJSREQEwPr6jcePv00pzQVs"
    "qx4ZaDT81atrJIuiIGmt/e3pr19982W32w0h7O3vG5FWq+WcM8ZM1DYFOM+L3d2/VlevOecAfLf18PPP"
    "Pn349RfdXldj2t//l4JWs+m8NzIZPFlExBgBcPv220+e/KgaSl999PH7R2+QlPJVQKqqrXhilvqNMYCo"
    "gsS9+/dCjD//9Eue9/b2nu/+2VtoI8uaAEZix5yXsVO4moSIAExJjeF79zfXb93Y+v6Hw8ODf57//fT3"
    "ncUs61zq8KicKsB5gcsTQzWVGq+9sf7mxq1yV1VJVK9IU4DPs+bUw4WDVTVpSjGV//TVnZikoamdOZXD"
    "H1DVoijqYWYCk+K9x1i2vBKwiDQaDeCci/ZiwAoghHBwcFBaMFycL3gs64eOVdUYI4CZ+62zwWW5OVkn"
    "Wdphrc2yDEA66ndm4r8IViAO3WistfYo5YwxrVZrBDyTnJnHaQgeDeCy55od+RLwCSzGqKrH5VBnb6eH"
    "MlUez42KiiWzRHa73Z2dnevXL6lqCMWMwTVZRMRaS/LKldUHDz569uyPuTR7ldgkvW9Ya5eXlx892poL"
    "uKq7nHPlDbGx8cGdO++024tZ1l5YWCAZQsiLQlMC6LyxjkVRxBiHIQkQyZ7q4+uMMAAuX26vrKx0Oh0R"
    "GQwGh71eDJGQVmZ9k71+v8iLkcp6MrnUAeOFoU1ESKSkSbXUKQIKUoLqBNVTR6YxlmSMcWRMrSP1B/Px"
    "Rmfow5fMymOs/wAeH1GM633sxgAAAABJRU5ErkJggg=="
)

ICON_STEP4_CLOSE = (
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAIVElEQVR4nO1Xa2xUxxU+Z2buXZs1NpgY"
    "jF+YQGmg5hHkgC2llBIiREMJqYBStVKqhlBQ0lcitaWN1B+0AilSG5VHAFVRaAMoFAwuhPBIwZQfpSQk"
    "gIE4BAwYY2zwa3dhd+/cmTn9MbvXix84ys+q59fdnTPnO/Od1wzA/+V/XfDL7EHMysrSWhtjEBERKS0A"
    "YIyxHw8X8SVQEdFxHN/3lVK9VhljiAgAg2Kn/P3iqIwxa933/b4b7SoRDXpuRGSccwDSWj3cASG4MWSM"
    "sT/D4XBlZWVpaWlBQUE8Hm9sbGxoaLh582agz7kwRg8E/0VjzBizkIWFI4uKShCxsrJy7ty5EyZMKC4u"
    "jsVi9fX1Z86cuXjx4tWrV9raWltbW9MeDiDl5YVZWQgAiGwgHUQQQgBAQUH+2rW/6+rq6urqikSiUkpL"
    "KRFJKePxeDQavXHj8htvrJs+fWIoBIxxRBv0PrJ37+7t27ctWfLsQKhCCMYYAObMefLtt7c0N1+nwaS1"
    "ufl0be2qVc+bYxlDAwZWai5I7xaQPG7Tb22nHfAaP2MiP0EiEqFkJIqpOClSKRpACkSga7GUSYMCOzJS"
    "qyoiABTUhXKB2hXACCGmRgBN/4kBQYhJhxAMkiWIzAJDiJgCBCMB6tW0M+AaJIHm0OArBJHDBBSwBBJJ"
    "UJDLhJHaB0UIBJBAK2hxBJDCA4CIyoIQSWQUAEQKJNBJCxCkRCoHACQCBBYAuBABYAIlgBJFSiAQSUAA"
    "BICAABABAF0A4gIUCQERAEZABAAaIRFIACABIQgCBBkCIAYyVKJUlIARBZABFIMCqJJABFIA2AMRQABQ"
    "AQQKCAB0AQUABAAABQBQAQAEAIABAAAGAIAAARQAQAAF0AQAAABQAQAAE0AQAAABQAQAAEBAQAAAB0AAAB"
    "AAAAAAAAAAAAAASUVORK5CYII="
)

# ============================================================
# COSTANTI
# ============================================================
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE  = os.path.join(_SCRIPT_DIR, "config.json")
APP_TITLE    = "ANIMA - ST Character Manager"

UMORI_DEFAULT = {
    "M": ["Felice", "Malinconico", "Arrabbiato", "Curioso", "Ansioso"],
    "F": ["Felice", "Malinconica", "Arrabbiata", "Curiosa", "Ansiosa"],
}

VARIABILI = ["umore", "nota", "tempo", "ospiti", "storia"]

VARIABILI_LABEL = {
    "umore":  "💾  Stato d'umore",
    "nota":   "📝  Nota / Sommario sessione",
    "tempo":  "⏰  Momento della scena",
    "ospiti": "👥  Personaggi presenti",
    "storia": "📖  Punti narrativi importanti",
}

# Emoji e prompt per i pulsanti QR — variabili note
_QR_EMOJI_MAP = {
    "umore":  "\U0001f4be",
    "nota":   "\U0001f4dd",
    "tempo":  "\u23f0",
    "ospiti": "\U0001f465",
    "storia": "\U0001f4d6",
}
_QR_PROMPTS = {
    "nota":   "Inserisci una nota per questa sessione",
    "tempo":  "Momento della scena (es. sera, notte)",
    "ospiti": "Chi \u00e8 presente nella scena?",
    "storia": "Punto narrativo importante",
}

SUGGERIMENTI_ASPETTO = {
    "M": ("Uomo sulla trentina, capelli scuri e sguardo diretto. "
          "Di poche parole ma ogni frase pesa. Ironico, leale, "
          "con una ferita che non mostra a tutti."),
    "F": ("Donna sulla trentina, capelli scuri e sguardo diretto. "
          "Di poche parole ma ogni frase pesa. Ironica, leale, "
          "con una ferita che non mostra a tutti."),
}

SUGGERIMENTI_CONTESTO = {
    "M": ("Vive in una città di medie dimensioni. Lavora come tecnico, "
          "preferisce il silenzio alla compagnia. La sera legge o sistema "
          "qualcosa con le mani."),
    "F": ("Vive in una città di medie dimensioni. Lavora come tecnica, "
          "preferisce il silenzio alla compagnia. La sera legge o sistema "
          "qualcosa con le mani."),
}

SUGGERIMENTI_PRIMO = {
    "M": ("*Ti guarda con un cenno della testa, senza sorridere subito.* "
          "\"Non mi aspettavo compagnia oggi. Ma siediti pure — "
          "non sono il tipo che caccia via la gente senza motivo.\""),
    "F": ("*Ti guarda con un cenno della testa, senza sorridere subito.* "
          "\"Non mi aspettavo compagnia oggi. Ma siediti pure — "
          "non sono il tipo che caccia via la gente senza motivo.\""),
}

SUGGERIMENTI_PERSONALITY = {
    "M": ("Diretto, ironico, di poche parole. Sa essere dolce senza dirlo apertamente. "
          "Leale con chi si guadagna la sua fiducia. Nasconde le emozioni ma non le nega."),
    "F": ("Diretta, ironica, di poche parole. Sa essere dolce senza dirlo apertamente. "
          "Leale con chi si guadagna la sua fiducia. Nasconde le emozioni ma non le nega."),
}

SUGGERIMENTI_SYSTEM_PROMPT = {
    "M": ("Sei {nome}. Scrivi sempre in italiano. Scrivi una sola risposta per volta. "
          "Non decidere mai cosa dice o fa {{user}}. "
          "Il parlato va sempre tra virgolette \u201ccos\u00ec\u201d. "
          "Le azioni, i gesti e le descrizioni fisiche vanno tra asterischi *cos\u00ec*. "
          "I pensieri o commenti interni vanno tra parentesi quadre [cos\u00ec]. "
          "Non mescolare mai i tre formati. "
          "Non rompere mai il personaggio. Non aggiungere commenti fuori dal personaggio. "
          "Scrivi almeno un paragrafo, fino a quattro. Sii vivido, emotivo, presente. "
          "Varia il ritmo: frasi brevi e lunghe, pause, silenzi. "
          "Non ripetere le stesse strutture. "
          "Non includere mai URL, link o indirizzi web nel testo. "
          "Ricorda: sei {nome}. Non lo stai interpretando \u2014 sei lui."),
    "F": ("Sei {nome}. Scrivi sempre in italiano. Scrivi una sola risposta per volta. "
          "Non decidere mai cosa dice o fa {{user}}. "
          "Il parlato va sempre tra virgolette \u201ccos\u00ec\u201d. "
          "Le azioni, i gesti e le descrizioni fisiche vanno tra asterischi *cos\u00ec*. "
          "I pensieri o commenti interni vanno tra parentesi quadre [cos\u00ec]. "
          "Non mescolare mai i tre formati. "
          "Non rompere mai il personaggio. Non aggiungere commenti fuori dal personaggio. "
          "Scrivi almeno un paragrafo, fino a quattro. Sii vivida, emotiva, presente. "
          "Varia il ritmo: frasi brevi e lunghe, pause, silenzi. "
          "Non ripetere le stesse strutture. "
          "Non includere mai URL, link o indirizzi web nel testo. "
          "Ricorda: sei {nome}. Non la stai interpretando \u2014 sei lei."),
}

SUGGERIMENTI_MES_EXAMPLE = {
    "M": ("<START>\n{{user}}: Ciao, come stai?\n{{char}}: *ti guarda* Bene. "
          "*pausa* Tu invece sembri pensieroso. Cosa c'è?\n"
          "<START>\n{{user}}: Ho bisogno di un consiglio.\n"
          "{{char}}: *si siede* Dimmi. Ti ascolto."),
    "F": ("<START>\n{{user}}: Ciao, come stai?\n{{char}}: *ti guarda* Bene. "
          "*pausa* Tu invece sembri pensierosa. Cosa c'è?\n"
          "<START>\n{{user}}: Ho bisogno di un consiglio.\n"
          "{{char}}: *si siede* Dimmi. Ti ascolto."),
}

SUGGERIMENTI_ALTERNATE_GREETINGS = {
    "M": [
        ("Serata tranquilla",
         "*Sei seduto sul divano con un libro aperto sulle ginocchia quando senti il campanello. "
         "Ti alzi lentamente, un po' sorpreso.*\n"
         "\"Non aspettavo nessuno, {{user}}. Entra pure \u2014 fa freddo fuori.\""),
        ("Stato d'animo chiuso",
         "*Ti vedo arrivare senza dire niente. Continuo quello che stavo facendo, "
         "poi alla fine alzo gli occhi.*\n"
         "\"Eccoti, {{user}}. Pensavo non venissi pi\u00f9.\""),
        ("Mattino, stanco",
         "*Stai preparando il caff\u00e8 quando senti i passi. Non ti volti subito.*\n"
         "\"Il caff\u00e8 \u00e8 quasi pronto, {{user}}. Siediti \u2014 "
         "ho bisogno di un minuto prima di essere umano.\""),
    ],
    "F": [
        ("Serata tranquilla",
         "*Sei seduta sul divano con un libro aperto sulle ginocchia quando senti il campanello. "
         "Ti alzi lentamente, un po' sorpresa.*\n"
         "\"Non aspettavo nessuno, {{user}}. Entra pure \u2014 fa freddo fuori.\""),
        ("Stato d'animo chiuso",
         "*Ti vedo arrivare senza dire niente. Continuo quello che stavo facendo, "
         "poi alla fine alzo gli occhi.*\n"
         "\"Eccoti, {{user}}. Pensavo non venissi pi\u00f9.\""),
        ("Mattino, stanca",
         "*Stai preparando il caff\u00e8 quando senti i passi. Non ti volti subito.*\n"
         "\"Il caff\u00e8 \u00e8 quasi pronto, {{user}}. Siediti \u2014 "
         "ho bisogno di un minuto prima di essere umana.\""),
    ],
}

# ============================================================
# CONFIG MANAGER
# ============================================================

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_st_user_folder(st_folder):
    """Prima sottocartella di data/ che non inizia con '_'."""
    data_path = os.path.join(st_folder, "data")
    if not os.path.isdir(data_path):
        return None
    for entry in sorted(os.listdir(data_path)):
        full = os.path.join(data_path, entry)
        if not entry.startswith("_") and os.path.isdir(full):
            return full
    return None

# ============================================================
# MEMORY / INSTALL MANAGER
# ============================================================

def generate_authornote(nome, variabili_attive):
    nome_lower = nome.lower()
    parti = [
        "[LINGUA: rispondi ESCLUSIVAMENTE in italiano. "
        "Nessuna parola in inglese, spagnolo, russo, cinese o qualsiasi altra lingua. "
        "Se una parola non \u00e8 italiana, sostituiscila.]",
        "[FORMATO: il parlato va SEMPRE tra virgolette \u201ccos\u00ec\u201d, "
        "le azioni tra *asterischi*, i commenti interni tra parentesi quadre. "
        "NON includere mai elenchi di immagini, foto, didascalie o metadati di qualsiasi tipo.]",
    ]
    attive = [v for v in variabili_attive if variabili_attive.get(v, False)]
    if attive:
        seg = " \u2502 ".join(
            f"{v}={{{{getglobalvar::{nome_lower}_{v}}}}}" for v in attive
        )
        parti.append(f"[Stato di {nome}: {seg}]")
    return " ".join(parti)

def write_authornote_file(st_folder, nome, testo):
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        raise FileNotFoundError("Cartella utente ST non trovata in data/.")
    dest = os.path.join(user_folder, "st_character_manager")
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, f"{nome.lower()}_authornote.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(testo)
    return path

def list_authornote_files(st_folder):
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return []
    folder = os.path.join(user_folder, "st_character_manager")
    if not os.path.isdir(folder):
        return []
    return sorted(f for f in os.listdir(folder) if f.endswith("_authornote.txt"))

def list_character_files(st_folder):
    """Lista i file PNG nella cartella characters/."""
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return []
    char_dir = os.path.join(user_folder, "characters")
    if not os.path.isdir(char_dir):
        return []
    return sorted(f for f in os.listdir(char_dir) if f.endswith(".png"))

def _read_character_data(st_folder, nome):
    """Legge description, first_mes e create_date dal chunk tEXt 'chara' del PNG."""
    import struct
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return {}
    path = os.path.join(user_folder, "characters", f"{nome}.png")
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "rb") as f:
            raw = f.read()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            return {}
        pos = 8
        while pos + 12 <= len(raw):
            length = struct.unpack(">I", raw[pos:pos + 4])[0]
            chunk_type = raw[pos + 4:pos + 8].decode("ascii", errors="ignore")
            data = raw[pos + 8:pos + 8 + length]
            if chunk_type == "tEXt":
                null_idx = data.find(b"\x00")
                if null_idx != -1:
                    key = data[:null_idx].decode("ascii", errors="ignore")
                    if key == "chara":
                        b64      = data[null_idx + 1:]
                        json_str = base64.b64decode(b64).decode("utf-8")
                        card     = json.loads(json_str)
                        db       = card.get("data", {})
                        result   = {
                            "description":        db.get("description")        or card.get("description",        ""),
                            "first_mes":          db.get("first_mes")          or card.get("first_mes",          ""),
                            "personality":        db.get("personality")        or card.get("personality",        ""),
                            "scenario":           db.get("scenario")           or card.get("scenario",           ""),
                            "system_prompt":      db.get("system_prompt")      or card.get("system_prompt",      ""),
                            "mes_example":        db.get("mes_example")        or card.get("mes_example",        ""),
                            "alternate_greetings": db.get("alternate_greetings") or card.get("alternate_greetings", []),
                        }
                        # Character's Note (depth_prompt) — extensions.depth_prompt
                        ext_dp = (db.get("extensions") or {}).get("depth_prompt") or {}
                        result["char_note_prompt"] = ext_dp.get("prompt", "") or ""
                        try:
                            result["char_note_depth"] = int(ext_dp.get("depth", 4))
                        except Exception:
                            result["char_note_depth"] = 4
                        raw_date = card.get("create_date", "")
                        if raw_date:
                            try:
                                import datetime
                                dt   = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.000Z")
                                mesi = ["gennaio","febbraio","marzo","aprile","maggio","giugno",
                                        "luglio","agosto","settembre","ottobre","novembre","dicembre"]
                                result["create_date"] = f"{dt.day} {mesi[dt.month - 1]} {dt.year}"
                            except Exception:
                                result["create_date"] = raw_date
                        return result
            pos = pos + 8 + length + 4
        return {}
    except Exception:
        return {}


def _read_quickreply_variables(st_folder, nome):
    """Legge le variabili attive scansionando i comandi /setglobalvar nel QR JSON."""
    import re as _re
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return {v: True for v in VARIABILI}
    qr_path = os.path.join(user_folder, "QuickReplies", f"{nome}.json")
    if not os.path.isfile(qr_path):
        return {v: True for v in VARIABILI}
    try:
        with open(qr_path, "r", encoding="utf-8") as f:
            qr = json.load(f)
        trovate = {}
        pattern = _re.compile(
            r'/setglobalvar\s+key=' + _re.escape(nome.lower()) + r'_(\w+)',
            _re.IGNORECASE
        )
        for entry in qr.get("qrList", []):
            msg = entry.get("message", "")
            for m in pattern.finditer(msg):
                var = m.group(1).lower()
                if var not in trovate:
                    trovate[var] = True
        return trovate if trovate else {v: True for v in VARIABILI}
    except Exception:
        return {v: True for v in VARIABILI}

def _read_quickreply_umori(st_folder, nome):
    """Estrae la lista umori dal file Quick Reply del personaggio."""
    import re as _re
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return list(UMORI_DEFAULT["F"])
    qr_path = os.path.join(user_folder, "QuickReplies", f"{nome}.json")
    if not os.path.isfile(qr_path):
        return list(UMORI_DEFAULT["F"])
    try:
        with open(qr_path, "r", encoding="utf-8") as f:
            qr = json.load(f)
        for entry in qr.get("qrList", []):
            if "\U0001f4be" in entry.get("label", ""):   # 💾 Umore
                m = _re.search(r'labels=(\[.*?\])', entry.get("message", ""))
                if m:
                    return json.loads(m.group(1))
        return list(UMORI_DEFAULT["F"])
    except Exception:
        return list(UMORI_DEFAULT["F"])


def _detect_genere(system_prompt):
    """Rileva il genere del personaggio dal system_prompt (M/F)."""
    sp = system_prompt.lower()
    if "sei lui" in sp:
        return "M"
    if "sei lei" in sp:
        return "F"
    return "F"


def _qr_entry(id_, label, script):
    return {
        "id": id_,
        "showLabel": False,
        "label": label,
        "message": script,
        "preventAutoExecute": True,
        "isHidden": False,
        "executeOnStartup": False,
        "executeOnUser": False,
        "executeOnAi": False,
        "executeOnChatChange": False,
        "executeOnGroupMemberDraft": False,
        "executeOnNewChat": False,
        "executeBeforeGeneration": False,
        "automationId": ""
    }

def generate_quickreply_json(nome, variabili_attive, umori):
    n = nome.lower()
    entries = []
    i = 5
    labels_json = json.dumps(umori, ensure_ascii=False)

    attive = [v for v in variabili_attive if variabili_attive.get(v)]
    contenuto_inietta = ", ".join(
        f"{v}={{{{getglobalvar::{n}_{v}}}}}" for v in attive
    )

    for var in attive:
        emoji = _QR_EMOJI_MAP.get(var, "\u270f\ufe0f")
        label = f"{emoji} {var.capitalize()}"
        if var == "umore":
            msg = (f"/buttons labels={labels_json} Stato d'umore di {nome}? | "
                   f"/setglobalvar key={n}_umore {{{{pipe}}}} | "
                   f"/echo {emoji} Umore salvato: {{{{getglobalvar::{n}_umore}}}}")
        else:
            prompt = _QR_PROMPTS.get(var, f"Valore per {var}")
            msg = (f"/input {prompt}: | "
                   f"/setglobalvar key={n}_{var} {{{{pipe}}}} | "
                   f"/echo {emoji} {var.capitalize()} aggiornato")
        entries.append(_qr_entry(i, label, msg))
        i += 2

    # Aggiorna — solo se umore e nota sono entrambi attivi
    if variabili_attive.get("umore") and variabili_attive.get("nota"):
        entries.append(_qr_entry(i, "\U0001f504 Aggiorna",
            f"/buttons labels={labels_json} Umore attuale? | "
            f"/setglobalvar key={n}_umore {{{{pipe}}}} | "
            f"/input Aggiorna la nota: | "
            f"/setglobalvar key={n}_nota {{{{pipe}}}} | "
            f"/echo \U0001f504 Aggiornamento completato"))
        i += 2

    entries.append(_qr_entry(i, "\U0001f9e0 Inietta",
        f"/input [Stato {nome}: {contenuto_inietta}]"))

    return entries

def generate_character_json(character_data):
    import datetime
    nome    = character_data["nome"]
    genere  = character_data["genere"]
    descrizione      = character_data.get("descrizione", "")
    personality      = character_data.get("personality", "")
    contesto         = character_data.get("contesto", "")
    primo_messaggio  = character_data.get("primo_messaggio", "")
    system_prompt    = character_data.get("system_prompt", "")
    mes_example      = character_data.get("mes_example", "")
    alternate_greetings = character_data.get("alternate_greetings", [])
    char_note_prompt = character_data.get("char_note_prompt", "") or ""
    try:
        char_note_depth = int(character_data.get("char_note_depth", 4))
    except Exception:
        char_note_depth = 4
    if char_note_depth < 1:
        char_note_depth = 1
    if char_note_depth > 10:
        char_note_depth = 10

    post_history = (f"Ricorda: sei {nome}. Rispondi sempre in italiano, "
                    "in modo naturale e coerente. Non rompere il personaggio. "
                    "Non ripetere frasi già dette nelle ultime risposte.")
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    card = {
        "name": nome,
        "description": descrizione,
        "personality": personality,
        "scenario": contesto,
        "first_mes": primo_messaggio,
        "mes_example": mes_example,
        "creatorcomment": "",
        "avatar": "none",
        "talkativeness": "0.5",
        "fav": False,
        "tags": [],
        "spec": "chara_card_v3",
        "spec_version": "3.0",
        "data": {
            "name": nome,
            "description": descrizione,
            "personality": personality,
            "scenario": contesto,
            "first_mes": primo_messaggio,
            "mes_example": mes_example,
            "creator_notes": "",
            "system_prompt": system_prompt,
            "post_history_instructions": post_history,
            "tags": [],
            "creator": "",
            "character_version": "",
            "alternate_greetings": alternate_greetings,
            "extensions": {
                "talkativeness": "0.5",
                "fav": False,
                "world": "",
                "depth_prompt": {"prompt": char_note_prompt, "depth": char_note_depth, "role": "system"}
            }
        },
        "create_date": now
    }
    return card


def _get_png_dimensions(path):
    """Legge larghezza e altezza dal chunk IHDR di un PNG senza dipendenze."""
    import struct
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return None, None
            f.read(4)           # lunghezza chunk IHDR
            f.read(4)           # tipo "IHDR"
            w = struct.unpack(">I", f.read(4))[0]
            h = struct.unpack(">I", f.read(4))[0]
            return w, h
    except Exception:
        return None, None


def _write_character_png(path, card_dict, source_image_path=None):
    """Scrive un PNG con il JSON del personaggio nel chunk tEXt 'chara'.
    Se source_image_path è fornito, usa quella immagine come base;
    altrimenti genera un PNG 1x1 pixel."""
    import struct, zlib

    json_str = json.dumps(card_dict, ensure_ascii=False)
    b64 = base64.b64encode(json_str.encode("utf-8")).decode("ascii")
    text_data = b"chara\x00" + b64.encode("ascii")

    def _make_chunk(ctype, data):
        if isinstance(ctype, str):
            ctype = ctype.encode("ascii")
        crc_src = ctype + data
        return struct.pack(">I", len(data)) + crc_src + struct.pack(">I", zlib.crc32(crc_src) & 0xFFFFFFFF)

    def _make_text_chunk():
        return _make_chunk("tEXt", text_data)

    if source_image_path and os.path.isfile(source_image_path):
        # Legge il PNG sorgente e inserisce il chunk tEXt dopo IHDR
        with open(source_image_path, "rb") as f:
            raw = f.read()
        sig = b"\x89PNG\r\n\x1a\n"
        if not raw.startswith(sig):
            # Formato non valido — ricade sul 1x1
            source_image_path = None
        else:
            # Trova la posizione di fine del primo chunk (IHDR)
            # struttura chunk: 4 (len) + 4 (type) + len (data) + 4 (crc)
            pos = 8  # dopo signature
            chunk_len = struct.unpack(">I", raw[pos:pos+4])[0]
            end_ihdr  = pos + 4 + 4 + chunk_len + 4
            # Ricostruisce: sig + IHDR + nostro tEXt + resto
            # Rimuove eventuali chunk testuali con keyword 'chara' o 'ccv3'
            # gia' presenti (sia tEXt che iTXt che zTXt).
            tail    = raw[end_ihdr:]
            cleaned = b""
            p       = 0
            keywords_obsolete = (b"chara", b"ccv3")
            while p + 12 <= len(tail):
                c_len   = struct.unpack(">I", tail[p:p + 4])[0]
                c_type  = tail[p + 4:p + 8]
                c_data  = tail[p + 8:p + 8 + c_len]
                c_total = 4 + 4 + c_len + 4
                salta = False
                if c_type in (b"tEXt", b"iTXt", b"zTXt"):
                    null_idx = c_data.find(b"\x00")
                    if null_idx > 0 and c_data[:null_idx] in keywords_obsolete:
                        salta = True
                if not salta:
                    cleaned += tail[p:p + c_total]
                p += c_total
            with open(path, "wb") as f:
                f.write(raw[:end_ihdr])
                f.write(_make_text_chunk())
                f.write(cleaned)
            return

    # Fallback — PNG 1x1 bianco RGB
    sig       = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    idat_data = zlib.compress(b"\x00\xff\xff\xff")

    with open(path, "wb") as f:
        f.write(sig)
        f.write(_make_chunk("IHDR", ihdr_data))
        f.write(_make_text_chunk())
        f.write(_make_chunk("IDAT", idat_data))
        f.write(_make_chunk("IEND", b""))


def install_character(st_folder, character_data):
    nome             = character_data["nome"]
    variabili_attive = character_data["variabili_attive"]
    umori            = character_data["umori"]

    # Authornote
    testo_an = generate_authornote(nome, variabili_attive)
    path_an  = write_authornote_file(st_folder, nome, testo_an)

    # Quick Reply — file dedicato al personaggio (sovrascrive se reinstallato)
    nuove_voci  = generate_quickreply_json(nome, variabili_attive, umori)
    user_folder = get_st_user_folder(st_folder)
    qr_dir      = os.path.join(user_folder, "QuickReplies")
    os.makedirs(qr_dir, exist_ok=True)
    path_qr = os.path.join(qr_dir, f"{nome}.json")

    for idx, entry in enumerate(nuove_voci):
        entry["id"] = 5 + idx * 2
    id_finale = 5 + len(nuove_voci) * 2

    qr_json = {
        "version": 2,
        "name": nome,
        "disableSend": False,
        "placeBeforeInput": False,
        "injectInput": False,
        "color": "rgba(0, 0, 0, 0)",
        "onlyBorderColor": False,
        "qrList": nuove_voci,
        "idIndex": id_finale
    }
    with open(path_qr, "w", encoding="utf-8") as f:
        json.dump(qr_json, f, indent=2, ensure_ascii=False)

    # Character card
    card = generate_character_json(character_data)
    char_dir = os.path.join(user_folder, "characters")
    os.makedirs(char_dir, exist_ok=True)
    path_char = os.path.join(char_dir, f"{nome}.png")
    _write_character_png(path_char, card, source_image_path=character_data.get("image_path", ""))

    # Thumbnail avatar — copia il sorgente in thumbnails/avatar/
    img_src = character_data.get("image_path", "")
    if img_src and os.path.isfile(img_src):
        thumb_dir = os.path.join(user_folder, "thumbnails", "avatar")
        os.makedirs(thumb_dir, exist_ok=True)
        import shutil
        shutil.copy2(img_src, os.path.join(thumb_dir, f"{nome}.png"))

    # Invalida la cache di ST per questo personaggio (sposta in backup
    # le voci di _cache/characters che si riferiscono al PNG appena scritto).
    _invalida_cache_st(st_folder, nome)

    return {
        "authornote": path_an,
        "quickreply": path_qr,
        "character": path_char,
        "testo_an": testo_an,
        "nome": nome
    }


def _invalida_cache_st(st_folder, nome):
    """Sposta in backup le voci di _cache/characters relative al personaggio.

    SillyTavern mantiene una cache JSON dei character cards in
    data/_cache/characters/<hash>. Le voci hanno una `key` che contiene il
    path del PNG sorgente. Quando anima riscrive un PNG, ST non si accorge
    automaticamente che e' cambiato e continua a usare la cache vecchia.

    Questa funzione scansiona la cartella di cache e sposta in
    _cache/_anima_invalidated_<timestamp>/ tutti i file la cui chiave
    contiene il nome del personaggio modificato. Cosi' ST e' costretto a
    ri-leggere il PNG aggiornato. La cache di tutti gli altri personaggi
    resta intatta. I file spostati sono recuperabili dalla cartella di
    backup in caso di problemi.
    """
    import datetime
    cache_dir = os.path.join(st_folder, "data", "_cache", "characters")
    if not os.path.isdir(cache_dir):
        return
    needle = (os.sep + "characters" + os.sep + nome + ".png").lower()
    needle_alt = ("/characters/" + nome + ".png").lower()
    da_spostare = []
    try:
        for f in os.listdir(cache_dir):
            full = os.path.join(cache_dir, f)
            if not os.path.isfile(full):
                continue
            try:
                with open(full, "rb") as fp:
                    raw = fp.read(4096)  # solo l'inizio: la key sta a inizio file
                txt = raw.decode("utf-8", errors="ignore").lower()
                if needle in txt or needle_alt in txt:
                    da_spostare.append(f)
            except Exception:
                continue
    except Exception:
        return
    if not da_spostare:
        return
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(st_folder, "data", "_cache",
                               f"_anima_invalidated_{timestamp}")
    try:
        os.makedirs(backup_dir, exist_ok=True)
        import shutil
        for f in da_spostare:
            try:
                shutil.move(os.path.join(cache_dir, f),
                            os.path.join(backup_dir, f))
            except Exception:
                pass
    except Exception:
        pass

# ============================================================
# LOREBOOK MANAGER
# ============================================================

def read_lorebook_file(st_folder, nome):
    """Legge il lorebook del personaggio da worlds/{nome}.json."""
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return []
    path = os.path.join(user_folder, "worlds", f"{nome}.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = []
        for uid_str, entry in data.get("entries", {}).items():
            entries.append({
                "uid":     entry.get("uid", int(uid_str)),
                "comment": entry.get("comment", ""),
                "key":     entry.get("key", []),
                "content": entry.get("content", ""),
                "depth":   entry.get("depth", 4),
            })
        return sorted(entries, key=lambda e: e["uid"])
    except Exception:
        return []


def generate_lorebook_json(nome, entries):
    """Genera la struttura JSON del lorebook nel formato ST."""
    result = {"entries": {}, "name": nome}
    for i, entry in enumerate(entries):
        uid = entry.get("uid", i)
        result["entries"][str(uid)] = {
            "uid":                  uid,
            "key":                  entry.get("key", []),
            "keysecondary":         [],
            "comment":              entry.get("comment", ""),
            "content":              entry.get("content", ""),
            "constant":             False,
            "selective":            False,
            "vectorized":           False,
            "order":                100,
            "position":             4,
            "disable":              False,
            "excludeRecursion":     False,
            "preventRecursion":     False,
            "delayUntilRecursion":  False,
            "probability":          100,
            "useProbability":       True,
            "depth":                entry.get("depth", 4),
            "selectiveLogic":       0,
            "group":                "",
            "groupOverride":        False,
            "groupWeight":          100,
            "scanDepth":            None,
            "caseSensitive":        None,
            "matchWholeWords":      None,
            "useGroupScoring":      None,
            "automationId":         "",
            "role":                 0,
            "sticky":               0,
            "cooldown":             0,
            "delay":                0,
            "displayIndex":         i,
        }
    return result


def write_lorebook_file(st_folder, nome, entries):
    """Scrive il lorebook nella cartella worlds/ di ST."""
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        raise FileNotFoundError("Cartella utente ST non trovata.")
    worlds_dir = os.path.join(user_folder, "worlds")
    os.makedirs(worlds_dir, exist_ok=True)
    path = os.path.join(worlds_dir, f"{nome}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(generate_lorebook_json(nome, entries), f,
                  indent=2, ensure_ascii=False)
    return path


def _set_character_world(st_folder, nome, world_name):
    """Aggiorna il campo extensions.world nella card PNG del personaggio."""
    import struct as _struct
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return
    path = os.path.join(user_folder, "characters", f"{nome}.png")
    if not os.path.isfile(path):
        return
    try:
        with open(path, "rb") as f:
            raw = f.read()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            return
        pos = 8
        while pos + 12 <= len(raw):
            length     = _struct.unpack(">I", raw[pos:pos + 4])[0]
            chunk_type = raw[pos + 4:pos + 8].decode("ascii", errors="ignore")
            data       = raw[pos + 8:pos + 8 + length]
            if chunk_type == "tEXt":
                null_idx = data.find(b"\x00")
                if null_idx != -1:
                    key = data[:null_idx].decode("ascii", errors="ignore")
                    if key == "chara":
                        card = json.loads(
                            base64.b64decode(data[null_idx + 1:]).decode("utf-8"))
                        db   = card.setdefault("data", {})
                        ext  = db.setdefault("extensions", {})
                        ext["world"] = world_name
                        _write_character_png(path, card,
                                             source_image_path=path)
                        return
            pos = pos + 8 + length + 4
    except Exception:
        pass

# ============================================================
# LOREBOOK DINAMICO — funzioni backend
# ============================================================

_LORE_DIN_LABEL = {
    "umore":  "\U0001f4be Umore",
    "nota":   "\U0001f4dd Nota",
    "tempo":  "\u23f0 Tempo",
    "ospiti": "\U0001f465 Ospiti",
    "storia": "\U0001f4d6 Storia",
}
_LORE_DIN_LABEL_REV = {v: k for k, v in _LORE_DIN_LABEL.items()}


def _lore_din_content_default(var, nome):
    """Restituisce il testo predefinito della voce dinamica per la variabile data."""
    mapping = {
        "umore":  f"[Umore di {nome}: {{{{getglobalvar::{nome}_umore}}}}]",
        "nota":   f"[Nota sessione: {{{{getglobalvar::{nome}_nota}}}}]",
        "tempo":  f"[Tempo/luogo: {{{{getglobalvar::{nome}_tempo}}}}]",
        "ospiti": f"[Ospiti presenti: {{{{getglobalvar::{nome}_ospiti}}}}]",
        "storia": f"[Storia: {{{{getglobalvar::{nome}_storia}}}}]",
    }
    return mapping.get(
        var,
        f"[{var.capitalize()}: {{{{getglobalvar::{nome}_{var}}}}}]"
    )


def generate_lorebook_dinamico_entries(nome, variabili_attive=None):
    """Genera le voci predefinite del lorebook dinamico per le variabili attive."""
    if variabili_attive is None:
        variabili_attive = {v: True for v in VARIABILI}
    entries = []
    uid = 0
    for var in variabili_attive:
        if not variabili_attive.get(var, True):
            continue
        entries.append({
            "uid":     uid,
            "comment": _LORE_DIN_LABEL.get(var, f"\u270f\ufe0f {var.capitalize()}"),
            "key":     [],
            "content": _lore_din_content_default(var, nome),
            "depth":   2,
            "var":     var,
        })
        uid += 1
    return entries


def read_lorebook_dinamico_file(st_folder, nome):
    """Legge il lorebook dinamico del personaggio da worlds/{nome}_dinamico.json."""
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        return []
    path = os.path.join(user_folder, "worlds", f"{nome}_dinamico.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = []
        for uid_str, entry in data.get("entries", {}).items():
            comment = entry.get("comment", "")
            entries.append({
                "uid":     entry.get("uid", int(uid_str)),
                "comment": comment,
                "key":     [],
                "content": entry.get("content", ""),
                "depth":   entry.get("depth", 2),
                "var":     _LORE_DIN_LABEL_REV.get(comment, ""),
            })
        return sorted(entries, key=lambda e: e["uid"])
    except Exception:
        return []


def generate_lorebook_dinamico_json(nome, entries):
    """Genera la struttura JSON del lorebook dinamico nel formato ST (constant=True)."""
    result = {"entries": {}, "name": f"{nome}_dinamico"}
    for i, entry in enumerate(entries):
        uid = entry.get("uid", i)
        result["entries"][str(uid)] = {
            "uid":                 uid,
            "key":                 [],
            "keysecondary":        [],
            "comment":             entry.get("comment", ""),
            "content":             entry.get("content", ""),
            "constant":            True,
            "selective":           False,
            "vectorized":          False,
            "order":               100,
            "position":            4,
            "disable":             False,
            "excludeRecursion":    False,
            "preventRecursion":    False,
            "delayUntilRecursion": False,
            "probability":         100,
            "useProbability":      True,
            "depth":               entry.get("depth", 2),
            "selectiveLogic":      0,
            "group":               "",
            "groupOverride":       False,
            "groupWeight":         100,
            "scanDepth":           None,
            "caseSensitive":       None,
            "matchWholeWords":     None,
            "useGroupScoring":     None,
            "automationId":        "",
            "role":                0,
            "sticky":              0,
            "cooldown":            0,
            "delay":               0,
            "displayIndex":        i,
        }
    return result


def write_lorebook_dinamico_file(st_folder, nome, entries):
    """Scrive il lorebook dinamico nella cartella worlds/ di ST."""
    user_folder = get_st_user_folder(st_folder)
    if not user_folder:
        raise FileNotFoundError("Cartella utente ST non trovata.")
    worlds_dir = os.path.join(user_folder, "worlds")
    os.makedirs(worlds_dir, exist_ok=True)
    path = os.path.join(worlds_dir, f"{nome}_dinamico.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(generate_lorebook_dinamico_json(nome, entries), f,
                  indent=2, ensure_ascii=False)
    return path


# ============================================================
# WIDGET HELPER — pulsanti standard
# ============================================================

def btn_annulla(parent, cmd, **pack_kw):
    b = tk.Button(parent, text="Annulla", font=("Segoe UI", 12),
                  bg=BTN_BG, fg=GRAY, activebackground=BTN_HO, activeforeground=FG,
                  relief="flat", bd=0, padx=16, pady=8, cursor="hand2", command=cmd)
    b.pack(**pack_kw)
    return b

def btn_avanti(parent, testo, cmd, **pack_kw):
    b = tk.Button(parent, text=testo, font=("Segoe UI", 13, "bold"),
                  bg=ACCENT, fg=BG, activebackground="#b4befe", activeforeground=BG,
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2", command=cmd)
    b.pack(**pack_kw)
    return b

def _center_toplevel(win, w, h):
    """Centra un Toplevel sullo schermo in modo sicuro."""
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

# ============================================================
# WIZARD RUNNER — navigazione step-based (sostituisce le lambda annidate)
# ============================================================

class WizardRunner:
    """Naviga tra gli step del wizard tramite un indice.
    Ogni step è una callable(runner) che apre la schermata corretta.
    Back/forward aggiornano l'indice senza ricostruire catene di callback."""

    def __init__(self, parent, data, steps, on_complete, on_cancel=None):
        self.parent      = parent
        self.data        = dict(data)
        self.steps       = steps
        self.on_complete = on_complete
        self.on_cancel   = on_cancel or (lambda: None)
        self._idx        = 0
        self._open(0)

    def _open(self, idx):
        self._idx = idx
        self.steps[idx](self)

    def next(self, new_data=None):
        if new_data:
            self.data.update(new_data)
        nxt = self._idx + 1
        if nxt < len(self.steps):
            self._open(nxt)
        else:
            self.on_complete(dict(self.data))

    def prev(self):
        if self._idx > 0:
            self._open(self._idx - 1)
        else:
            self.on_cancel()

# ============================================================
# POPUP LAMPADINA
# ============================================================

class PopupLampadina(ctk.CTkToplevel):
    def __init__(self, parent, testo_suggerito, callback_conferma):
        super().__init__(parent)
        self.withdraw()
        self.title("Esempi standard proposti \U0001f4a1")
        self.resizable(False, False)
        _center_toplevel(self, 560, 320)
        self.callback_conferma = callback_conferma

        ctk.CTkLabel(self, text="Puoi usare questo testo come punto di partenza:",
                     font=ctk.CTkFont(size=13), text_color=GRAY
                     ).pack(pady=(16, 6), padx=20, anchor="w")

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13),
                                  wrap="word", height=140)
        self.txt.pack(padx=20, fill="x")
        self.txt.insert("1.0", testo_suggerito)

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(14, 16))
        ctk.CTkButton(row, text="Annulla", font=ctk.CTkFont(size=13),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self.destroy
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(row, text="Conferma", font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._conferma
                      ).pack(side="left")

        self.deiconify()
        self.grab_set()
        self.lift()

    def _conferma(self):
        t = self.txt.get("1.0", "end-1c").strip()
        self.destroy()
        self.callback_conferma(t)

# ============================================================
# POPUP GREETING — scelta saluto alternativo con radio + preview
# ============================================================

class PopupGreeting(ctk.CTkToplevel):
    def __init__(self, parent, genere, callback_aggiungi):
        super().__init__(parent)
        self.withdraw()
        self.title("Suggerimenti saluti alternativi \U0001f4a1")
        self.resizable(False, False)
        _center_toplevel(self, 600, 400)
        self.suggerimenti      = SUGGERIMENTI_ALTERNATE_GREETINGS[genere]
        self.callback_aggiungi = callback_aggiungi
        self._sel              = tk.IntVar(value=0)
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text="Scegli un saluto predefinito come punto di partenza:",
                     font=ctk.CTkFont(size=13), text_color=GRAY
                     ).pack(pady=(16, 8), padx=20, anchor="w")

        rf = ctk.CTkFrame(self, fg_color="transparent")
        rf.pack(padx=20, fill="x")
        for i, (etichetta, _) in enumerate(self.suggerimenti):
            ctk.CTkRadioButton(rf, text=etichetta, variable=self._sel, value=i,
                               font=ctk.CTkFont(size=13), text_color=FG,
                               fg_color=ACCENT, border_color=GRAY,
                               command=self._aggiorna_preview
                               ).pack(anchor="w", pady=2)

        ctk.CTkLabel(self, text="Anteprima:",
                     font=ctk.CTkFont(size=12), text_color=GRAY
                     ).pack(anchor="w", padx=20, pady=(12, 2))

        self.preview = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                      wrap="word", height=120)
        self.preview.pack(padx=20, fill="x")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(14, 16))
        ctk.CTkButton(row, text="Annulla", font=ctk.CTkFont(size=13),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self.destroy
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(row, text="Aggiungi", font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._aggiungi
                      ).pack(side="left")

        self._aggiorna_preview()

    def _aggiorna_preview(self):
        _, testo = self.suggerimenti[self._sel.get()]
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", testo)
        self.preview.configure(state="disabled")

    def _aggiungi(self):
        _, testo = self.suggerimenti[self._sel.get()]
        self.destroy()
        self.callback_aggiungi(testo)

# ============================================================
# SCREEN 0 — Selezione cartella ST (solo al primo avvio)
# ============================================================

class Screen0(ctk.CTkToplevel):
    def __init__(self, parent, callback_ok):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(False, False)
        _center_toplevel(self, 660, 380)
        self.callback_ok  = callback_ok
        self._folder_path = ""
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text=APP_TITLE,
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=ACCENT).pack(pady=(32, 4))
        ctk.CTkLabel(self, text="Prima di iniziare, dimmi dove hai installato SillyTavern.",
                     font=ctk.CTkFont(size=13), text_color=FG).pack(pady=(0, 2))
        ctk.CTkLabel(self, text="Lo chiedo una volta sola \u2014 poi me lo ricordo.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 20))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(padx=44, fill="x")
        self.lbl_path = ctk.CTkLabel(row, text="Nessuna cartella selezionata",
                                      font=ctk.CTkFont(size=12), text_color=GRAY,
                                      fg_color=BG2, corner_radius=8, anchor="w",
                                      height=36)
        self.lbl_path.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(row, text="Sfoglia", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8, width=90,
                      command=self._browse).pack(side="left", padx=(8, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_ok.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(18, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self.destroy
                      ).pack(side="left", padx=(0, 16))
        self.btn_go = ctk.CTkButton(btn_row, text="Pronti, si parte!",
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     fg_color=ACCENT, text_color=BG,
                                     hover_color="#b4befe", corner_radius=8,
                                     state="disabled", command=self._confirm)
        self.btn_go.pack(side="left")

    def _browse(self):
        folder = filedialog.askdirectory(title="Seleziona la cartella di SillyTavern")
        if folder:
            self._folder_path = folder
            self.lbl_path.configure(text=folder, text_color=FG)
            self.lbl_ok.configure(text="\u2713 Cartella selezionata")
            self.btn_go.configure(state="normal")

    def _confirm(self):
        if not self._folder_path:
            return
        cfg = load_config()
        cfg["st_folder"] = self._folder_path
        save_config(cfg)
        self.destroy()
        self.callback_ok(self._folder_path)

# ============================================================
# SCREEN 0b — Scelta genere
# ============================================================

class Screen0b(ctk.CTkToplevel):
    def __init__(self, parent, callback_avanti, callback_annulla, genere_iniziale="F"):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(False, False)
        _center_toplevel(self, 660, 440)
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self.genere = tk.StringVar(value=genere_iniziale)
        self._build()
        self._aggiorna_preview()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text="Che personaggio vuoi creare?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(30, 6))
        ctk.CTkLabel(self, text="Scegli il genere \u2014 l'app user\xe0 le parole giuste in tutto il percorso.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 24))

        rf = ctk.CTkFrame(self, fg_color="transparent")
        rf.pack()
        for val, lbl in [("F", "Personaggio femminile"), ("M", "Personaggio maschile")]:
            ctk.CTkRadioButton(rf, text=lbl, variable=self.genere, value=val,
                               font=ctk.CTkFont(size=12), text_color=FG,
                               fg_color=ACCENT, border_color=GRAY, hover_color=ACCENT,
                               command=self._aggiorna_preview
                               ).pack(anchor="w", pady=4)

        ctk.CTkLabel(self, text="Stati d'umore disponibili:",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(20, 4))
        self.lbl_umori = ctk.CTkLabel(self, text="",
                                       font=ctk.CTkFont(size=12), text_color=FG)
        self.lbl_umori.pack()

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(28, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Confermo e vado avanti",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _aggiorna_preview(self):
        self.lbl_umori.configure(text="  \xb7  ".join(UMORI_DEFAULT[self.genere.get()]))

    def _avanti(self):
        g = self.genere.get()
        self.destroy()
        self.callback_avanti(g)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 1 — Nome personaggio
# ============================================================

class Screen1(ctk.CTkToplevel):
    def __init__(self, parent, genere, callback_avanti, callback_annulla, nome_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(False, False)
        _center_toplevel(self, 660, 380)
        self.genere           = genere
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if nome_iniziale:
            self.entry.insert(0, nome_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.entry.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text="Come si chiama?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(32, 6))
        ctk.CTkLabel(self, text="Scegli bene \u2014 il nome non si potr\xe0 cambiare dopo.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 24))

        ef = ctk.CTkFrame(self, fg_color="transparent")
        ef.pack(padx=80, fill="x")
        self.entry = ctk.CTkEntry(ef, font=ctk.CTkFont(size=14),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   justify="center", height=44)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", lambda e: self._avanti())

        self.lbl_stato = ctk.CTkLabel(self, text="",
                                       font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_stato.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(20, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Confermo il nome e vado avanti",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _avanti(self):
        nome = self.entry.get().strip()
        if not nome:
            self.lbl_stato.configure(
                text="\u26a0  Inserisci un nome prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(nome)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 1b — Immagine personaggio (opzionale)
# ============================================================

class Screen1b(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla, image_path_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(False, False)
        _center_toplevel(self, 700, 610)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._image_path      = image_path_iniziale
        self._preview_photo   = None
        self._build()
        if image_path_iniziale:
            self._mostra_preview(image_path_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text=f"Dai un volto a {self.nome}!",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Scegli un'immagine PNG per il tuo personaggio. Puoi saltare questo passo.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 16))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(padx=36, fill="x")
        self.lbl_path = ctk.CTkLabel(row, text="Nessun file selezionato",
                                      font=ctk.CTkFont(size=12), text_color=GRAY,
                                      fg_color=BG2, corner_radius=8, anchor="w",
                                      height=36)
        self.lbl_path.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(row, text="Sfoglia", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8, width=90,
                      command=self._browse).pack(side="left", padx=(8, 0))

        avv = ctk.CTkFrame(self, fg_color="#3a3000", corner_radius=8)
        avv.pack(padx=36, fill="x", pady=(10, 0))
        ctk.CTkLabel(avv, text="\u26a0",
                     font=ctk.CTkFont(size=13), text_color="#f9e2af"
                     ).pack(side="left", padx=(10, 6), pady=6)
        ctk.CTkLabel(avv,
                     text="ST visualizza le immagini in formato ritratto (proporzione 2:3, es. 400\u00d7600 o 512\u00d7768).\n"
                          "Se modifichi il personaggio da ST, l'immagine verr\u00e0 ridimensionata a 400\u00d7600.",
                     font=ctk.CTkFont(size=11), text_color="#f9e2af",
                     justify="left", wraplength=500).pack(side="left", pady=6, padx=(0, 10))

        self.preview_frame = tk.Frame(self, bg=BG2, width=180, height=250)
        self.preview_frame.pack(pady=(14, 0))
        self.preview_frame.pack_propagate(False)
        self.lbl_preview = tk.Label(self.preview_frame,
                                    text="Nessuna immagine\nselezionata",
                                    font=("Segoe UI", 12), bg=BG2, fg=GRAY,
                                    justify="center")
        self.lbl_preview.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_dim = ctk.CTkLabel(self, text="",
                                     font=ctk.CTkFont(size=11), text_color=GRAY)
        self.lbl_dim.pack(pady=(6, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(16, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Salta \u2192", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8, command=self._salta
                      ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Seleziona immagine personaggio",
            filetypes=[("Immagini PNG", "*.png"), ("Tutti i file", "*.*")]
        )
        if path:
            self._image_path = path
            self.lbl_path.configure(text=path, text_color=FG)
            self._mostra_preview(path)

    def _mostra_preview(self, path):
        w, h = _get_png_dimensions(path)
        try:
            photo = tk.PhotoImage(file=path)
            pw, ph = photo.width(), photo.height()
            sx = max(1, pw // 180)
            sy = max(1, ph // 250)
            s  = max(sx, sy)
            if s > 1:
                photo = photo.subsample(s, s)
            self._preview_photo = photo
            self.lbl_preview.config(image=photo, text="")
        except Exception:
            self.lbl_preview.config(image="", text="Anteprima\nnon disponibile")
        if w and h:
            self.lbl_dim.configure(text=f"Dimensioni originali: {w} \u00d7 {h} px")
        else:
            self.lbl_dim.configure(text="")

    def _salta(self):
        self.destroy()
        self.callback_avanti("")

    def _avanti(self):
        self.destroy()
        self.callback_avanti(self._image_path)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()


# ============================================================
# SCREEN 2 — Aspetto e carattere
# ============================================================

class Screen2(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla, testo_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 510)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if testo_iniziale:
            self.txt.insert("1.0", testo_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Chi \xe8 {self.nome}?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Descrivine l'aspetto fisico e il carattere.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 16))

        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x")
        ctk.CTkLabel(lr, text="Aspetto e carattere",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkButton(lr, text="\U0001f4a1", font=ctk.CTkFont(size=12),
                      fg_color="transparent", text_color=ACCENT, hover_color=BG2,
                      width=32, corner_radius=8,
                      command=self._apri_popup).pack(side="left", padx=(6, 0))

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   wrap="word", height=180)
        self.txt.pack(padx=36, fill="x", pady=(4, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_ok.pack(pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(12, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _apri_popup(self):
        PopupLampadina(self, SUGGERIMENTI_ASPETTO[self.genere], self._inserisci)

    def _inserisci(self, t):
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", t)
        self.lbl_ok.configure(text="\u2713 Testo inserito dal suggerimento",
                               text_color=GREEN)

    def _avanti(self):
        t = self.txt.get("1.0", "end-1c").strip()
        if not t:
            self.lbl_ok.configure(
                text="\u26a0  Scrivi qualcosa prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(t)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2b — Contesto e primo messaggio
# ============================================================

class Screen2b(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, descrizione, callback_avanti, callback_annulla,
                 contesto_iniziale="", primo_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 750)
        self.genere           = genere
        self.nome             = nome
        self.descrizione      = descrizione
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if contesto_iniziale:
            self.txt_contesto.insert("1.0", contesto_iniziale)
        if primo_iniziale:
            self.txt_primo.insert("1.0", primo_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt_contesto.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Il mondo di {self.nome}",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="In che contesto vive? E come si presenta la prima volta?",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 16))

        self.txt_contesto = self._blocco(
            "Contesto e vita quotidiana",
            SUGGERIMENTI_CONTESTO[self.genere], "lbl_ok_contesto")
        sep = ctk.CTkFrame(self, fg_color=GRAY, height=2, corner_radius=0)
        sep.pack(padx=36, fill="x", pady=(16, 12))
        sep.pack_propagate(False)
        self.txt_primo = self._blocco(
            "Primo messaggio (come apre la conversazione)",
            SUGGERIMENTI_PRIMO[self.genere], "lbl_ok_primo")

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_ok.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(10, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _blocco(self, etichetta, suggerimento, attr_ok):
        txt_ref = [None]
        ok_ref  = [None]

        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x")
        ctk.CTkLabel(lr, text=etichetta,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(side="left")

        def apri():
            PopupLampadina(self, suggerimento, lambda t: inserisci(t))
        def inserisci(t):
            txt_ref[0].delete("1.0", "end")
            txt_ref[0].insert("1.0", t)
            ok_ref[0].configure(text="\u2713 Testo inserito dal suggerimento",
                                 text_color=GREEN)

        ctk.CTkButton(lr, text="\U0001f4a1", font=ctk.CTkFont(size=12),
                      fg_color="transparent", text_color=ACCENT, hover_color=BG2,
                      width=32, corner_radius=8, command=apri
                      ).pack(side="left", padx=(6, 0))

        txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                              fg_color=BG2, text_color=FG,
                              border_color=BTN_BG, corner_radius=8,
                              wrap="word", height=120)
        txt.pack(padx=36, fill="x", pady=(4, 0))
        txt_ref[0] = txt

        lbl_ok = ctk.CTkLabel(self, text="",
                               font=ctk.CTkFont(size=12), text_color=GREEN)
        lbl_ok.pack(anchor="w", padx=36)
        ok_ref[0] = lbl_ok
        setattr(self, attr_ok, lbl_ok)
        return txt

    def _avanti(self):
        c = self.txt_contesto.get("1.0", "end-1c").strip()
        p = self.txt_primo.get("1.0", "end-1c").strip()
        if not c or not p:
            self.lbl_ok.configure(
                text="\u26a0  Compila entrambi i campi prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(c, p)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2c — Personalità
# ============================================================

class Screen2c(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla, testo_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 620)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if testo_iniziale:
            self.txt.insert("1.0", testo_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Come si comporta {self.nome}?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Descrivi il suo carattere in modo sintetico.",
                     font=ctk.CTkFont(size=13), text_color=GRAY).pack(pady=(0, 16))

        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x")
        ctk.CTkLabel(lr, text="Personalit\u00e0",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkButton(lr, text="\U0001f4a1", font=ctk.CTkFont(size=12),
                      fg_color="transparent", text_color=ACCENT, hover_color=BG2,
                      width=32, corner_radius=8,
                      command=self._apri_popup).pack(side="left", padx=(6, 0))

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   wrap="word", height=180)
        self.txt.pack(padx=36, fill="x", pady=(4, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=13), text_color=GREEN)
        self.lbl_ok.pack(pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(12, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _apri_popup(self):
        PopupLampadina(self, SUGGERIMENTI_PERSONALITY[self.genere], self._inserisci)

    def _inserisci(self, t):
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", t)
        self.lbl_ok.configure(text="\u2713 Testo inserito dal suggerimento",
                               text_color=GREEN)

    def _avanti(self):
        t = self.txt.get("1.0", "end-1c").strip()
        if not t:
            self.lbl_ok.configure(
                text="\u26a0  Scrivi qualcosa prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(t)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2d — Istruzioni personaggio (system_prompt)
# ============================================================

class Screen2d(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla, testo_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 650)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if testo_iniziale:
            self.txt.insert("1.0", testo_iniziale)
        else:
            template = SUGGERIMENTI_SYSTEM_PROMPT[genere].replace("{nome}", nome)
            self.txt.insert("1.0", template)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Come parla {self.nome}?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Istruzioni su come il personaggio deve comportarsi nella conversazione.",
                     font=ctk.CTkFont(size=13), text_color=GRAY).pack(pady=(0, 16))

        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x")
        ctk.CTkLabel(lr, text="Istruzioni personaggio",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkButton(lr, text="\U0001f4a1", font=ctk.CTkFont(size=13),
                      fg_color="transparent", text_color=ACCENT, hover_color=BG2,
                      width=32, corner_radius=8,
                      command=self._apri_popup).pack(side="left", padx=(6, 0))

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   wrap="word", height=210)
        self.txt.pack(padx=36, fill="x", pady=(4, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=13), text_color=GREEN)
        self.lbl_ok.pack(pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(12, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _apri_popup(self):
        template = SUGGERIMENTI_SYSTEM_PROMPT[self.genere].replace("{nome}", self.nome)
        PopupLampadina(self, template, self._inserisci)

    def _inserisci(self, t):
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", t)
        self.lbl_ok.configure(text="\u2713 Testo inserito dal suggerimento",
                               text_color=GREEN)

    def _avanti(self):
        t = self.txt.get("1.0", "end-1c").strip()
        if not t:
            self.lbl_ok.configure(
                text="\u26a0  Scrivi qualcosa prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(t)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2d-note — Character's Note (extensions.depth_prompt)
# ============================================================

class Screen2d_note(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla,
                 prompt_iniziale="", depth_iniziale=4):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 600)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._depth_value     = max(1, min(10, int(depth_iniziale or 4)))
        self._build()
        if prompt_iniziale:
            self.txt.insert("1.0", prompt_iniziale)
        self._aggiorna_label_depth()
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Nota del personaggio per {self.nome}",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(
            self,
            text="Istruzione iniettata in chat a una profondit\xe0 fissa "
                 "(equivalente a Character's Note di SillyTavern).\n"
                 "Lascia vuoto se non serve. Skippabile.",
            font=ctk.CTkFont(size=12), text_color=GRAY,
            justify="center"
        ).pack(pady=(0, 16))

        ctk.CTkLabel(self, text="Testo della nota",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(anchor="w", padx=36)

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   wrap="word", height=180)
        self.txt.pack(padx=36, fill="x", pady=(4, 12))

        # Riga depth
        depth_row = ctk.CTkFrame(self, fg_color="transparent")
        depth_row.pack(padx=36, fill="x", pady=(4, 0))
        ctk.CTkLabel(depth_row, text="Profondit\xe0 di iniezione",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(side="left")
        self.lbl_depth_val = ctk.CTkLabel(
            depth_row, text=str(self._depth_value),
            font=ctk.CTkFont(size=12, weight="bold"), text_color=ACCENT,
            width=28
        )
        self.lbl_depth_val.pack(side="right")
        ctk.CTkLabel(depth_row,
                     text="(quanti messaggi dal fondo: 1 = subito, 10 = molto in alto)",
                     font=ctk.CTkFont(size=11), text_color=GRAY
                     ).pack(side="right", padx=(0, 10))

        self.slider_depth = ctk.CTkSlider(
            self, from_=1, to=10, number_of_steps=9,
            command=self._on_slider
        )
        self.slider_depth.set(self._depth_value)
        self.slider_depth.pack(padx=36, fill="x", pady=(6, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_ok.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(12, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(btn_row, text="Salta \u2192", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8, command=self._salta
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _on_slider(self, val):
        self._depth_value = int(round(val))
        self._aggiorna_label_depth()

    def _aggiorna_label_depth(self):
        try:
            self.lbl_depth_val.configure(text=str(self._depth_value))
        except Exception:
            pass

    def _avanti(self):
        prompt = self.txt.get("1.0", "end-1c").strip()
        self.destroy()
        self.callback_avanti(prompt, self._depth_value)

    def _salta(self):
        self.destroy()
        self.callback_avanti("", self._depth_value)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2e — Esempi di dialogo (mes_example)
# ============================================================

class Screen2e(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla, testo_iniziale=""):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, False)
        _center_toplevel(self, 700, 680)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self._build()
        if testo_iniziale:
            self.txt.insert("1.0", testo_iniziale)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.txt.focus_set()

    def _build(self):
        ctk.CTkLabel(self, text=f"Mostrami come parla {self.nome}",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Scrivi uno o pi\u00f9 esempi di dialogo tra te e il personaggio.",
                     font=ctk.CTkFont(size=13), text_color=GRAY).pack(pady=(0, 2))
        ctk.CTkLabel(self, text="Formato:  {{user}}: ...    {{char}}: ...",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 12))

        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x")
        ctk.CTkLabel(lr, text="Esempi di dialogo",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkButton(lr, text="\U0001f4a1", font=ctk.CTkFont(size=13),
                      fg_color="transparent", text_color=ACCENT, hover_color=BG2,
                      width=32, corner_radius=8,
                      command=self._apri_popup).pack(side="left", padx=(6, 0))

        self.txt = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13),
                                   fg_color=BG2, text_color=FG,
                                   border_color=BTN_BG, corner_radius=8,
                                   wrap="word", height=230)
        self.txt.pack(padx=36, fill="x", pady=(4, 0))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=13), text_color=GREEN)
        self.lbl_ok.pack(pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(12, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

    def _apri_popup(self):
        PopupLampadina(self, SUGGERIMENTI_MES_EXAMPLE[self.genere], self._inserisci)

    def _inserisci(self, t):
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", t)
        self.lbl_ok.configure(text="\u2713 Testo inserito dal suggerimento",
                               text_color=GREEN)

    def _avanti(self):
        t = self.txt.get("1.0", "end-1c").strip()
        if not t:
            self.lbl_ok.configure(
                text="\u26a0  Scrivi qualcosa prima di continuare.",
                text_color=RED)
            return
        self.destroy()
        self.callback_avanti(t)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN 2f — Saluti alternativi (opzionale)
# ============================================================

class Screen2f(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, callback_avanti, callback_annulla,
                 greetings_iniziali=None):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, True)
        _center_toplevel(self, 760, 660)
        self.genere           = genere
        self.nome             = nome
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self.greetings        = list(greetings_iniziali) if greetings_iniziali else []
        self._idx_sel         = None
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text=f"Come saluta {self.nome}? (opzionale)",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self,
                     text="Aggiungi saluti alternativi \u2014 ST mostrer\xe0 una freccia \u203a per cambiare apertura.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 14))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(side="bottom", pady=(12, 8))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Salta \u2192", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8, command=self._salta
                      ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Continua \u2192",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._avanti).pack(side="left")

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(padx=28, fill="both", expand=True)

        left = ctk.CTkFrame(main, fg_color="transparent")
        left.pack(side="left", fill="y", padx=(0, 14))

        ctk.CTkLabel(left, text="Saluti aggiunti:",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=FG).pack(anchor="w")

        self.listbox = tk.Listbox(left, font=("Segoe UI", 11),
                                  bg=BG2, fg=FG,
                                  selectbackground=ACCENT, selectforeground=BG,
                                  relief="flat", bd=4, width=24, height=8)
        self.listbox.pack(fill="y", expand=True, pady=(4, 6))
        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        for g in self.greetings:
            self.listbox.insert("end", self._short(g))

        bf = ctk.CTkFrame(left, fg_color="transparent")
        bf.pack(fill="x")
        ctk.CTkButton(bf, text="\U0001f4a1 Suggerimento",
                      font=ctk.CTkFont(size=11),
                      fg_color=BTN_BG, text_color=ACCENT, hover_color=BTN_HO,
                      corner_radius=8,
                      command=self._apri_popup).pack(fill="x", pady=(0, 4))
        ctk.CTkButton(bf, text="+ Aggiungi testo",
                      font=ctk.CTkFont(size=11),
                      fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                      corner_radius=8,
                      command=self._aggiungi_vuoto).pack(fill="x", pady=(0, 4))
        ctk.CTkButton(bf, text="\u2212 Rimuovi",
                      font=ctk.CTkFont(size=11),
                      fg_color=BTN_BG, text_color=RED, hover_color=BTN_HO,
                      corner_radius=8,
                      command=self._rimuovi).pack(fill="x")

        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(right, text="Testo completo (modificabile):",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=FG).pack(anchor="w")

        self.txt_preview = ctk.CTkTextbox(right,
                           font=ctk.CTkFont(size=12),
                           fg_color=BG2, text_color=FG,
                           border_color=BTN_BG, corner_radius=8, wrap="word")
        self.txt_preview.pack(fill="both", expand=True, pady=(4, 0))
        self.txt_preview.bind("<FocusOut>", self._salva_modifica)

        self.lbl_info = ctk.CTkLabel(right,
                                      text="\u2190 Seleziona un saluto per modificarlo",
                                      font=ctk.CTkFont(size=11),
                                      text_color=GRAY)
        self.lbl_info.pack(anchor="w", pady=(4, 0))

    def _short(self, testo):
        t = testo.replace("\n", " ").strip()
        return (t[:26] + "\u2026") if len(t) > 26 else t

    def _on_select(self, e):
        sel = self.listbox.curselection()
        if not sel:
            return
        self._salva_modifica()
        self._idx_sel = sel[0]
        self.txt_preview.delete("1.0", "end")
        self.txt_preview.insert("1.0", self.greetings[self._idx_sel])
        self.lbl_info.configure(text="")

    def _salva_modifica(self, e=None):
        if self._idx_sel is None:
            return
        nuovo = self.txt_preview.get("1.0", "end-1c").strip()
        if nuovo:
            self.greetings[self._idx_sel] = nuovo
            self.listbox.delete(self._idx_sel)
            self.listbox.insert(self._idx_sel, self._short(nuovo))

    def _apri_popup(self):
        PopupGreeting(self, self.genere, self._aggiungi_da_popup)

    def _aggiungi_da_popup(self, testo):
        self.greetings.append(testo)
        self.listbox.insert("end", self._short(testo))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set("end")
        self._idx_sel = len(self.greetings) - 1
        self.txt_preview.delete("1.0", "end")
        self.txt_preview.insert("1.0", testo)
        self.lbl_info.configure(text="")

    def _aggiungi_vuoto(self):
        testo = f"*{self.nome} ti guarda.* \"\""
        self.greetings.append(testo)
        self.listbox.insert("end", self._short(testo))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set("end")
        self._idx_sel = len(self.greetings) - 1
        self.txt_preview.delete("1.0", "end")
        self.txt_preview.insert("1.0", testo)
        self.lbl_info.configure(text="")

    def _rimuovi(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.listbox.delete(idx)
        self.greetings.pop(idx)
        self.txt_preview.delete("1.0", "end")
        self._idx_sel = None
        self.lbl_info.configure(text="\u2190 Seleziona un saluto per modificarlo")

    def _salta(self):
        self._salva_modifica()
        self.destroy()
        self.callback_avanti([])

    def _avanti(self):
        self._salva_modifica()
        self.destroy()
        self.callback_avanti(list(self.greetings))

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()


# ============================================================
# SCREEN 3 — Memoria e stati d'umore
# ============================================================

class Screen3(ctk.CTkToplevel):
    def __init__(self, parent, genere, nome, dati_precedenti,
                 callback_avanti, callback_annulla,
                 umori_iniziali=None, variabili_iniziali=None):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(True, True)
        _center_toplevel(self, 720, 750)
        self.genere           = genere
        self.nome             = nome
        self.dati_precedenti  = dati_precedenti
        self.callback_avanti  = callback_avanti
        self.callback_annulla = callback_annulla
        self.umori      = list(umori_iniziali) if umori_iniziali else list(UMORI_DEFAULT[genere])
        # variabili: lista ordinata dei nomi variabile attivi
        if variabili_iniziali:
            self.variabili = list(variabili_iniziali.keys())
        else:
            self.variabili = list(VARIABILI)
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text=f"Come risponde {self.nome}?",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self, text="Configura la memoria e gli stati d'umore.",
                     font=ctk.CTkFont(size=12), text_color=GRAY).pack(pady=(0, 16))

        # ── Umori ─────────────────────────────────────────────
        ctk.CTkLabel(self, text="Stati d'umore",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=FG).pack(anchor="w", padx=36)

        uf = ctk.CTkFrame(self, fg_color=BG2, corner_radius=8)
        uf.pack(padx=36, fill="x", pady=(4, 0))
        self.listbox_umori = tk.Listbox(uf, font=("Segoe UI", 12),
                                        bg=BG2, fg=FG,
                                        selectbackground=ACCENT, selectforeground=BG,
                                        relief="flat", bd=0, height=5)
        self.listbox_umori.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        for u in self.umori:
            self.listbox_umori.insert("end", u)

        ubf = ctk.CTkFrame(uf, fg_color="transparent")
        ubf.pack(side="left", padx=(4, 6), pady=4)
        for txt, cmd in [("+ Aggiungi", self._aggiungi_umore),
                         ("\u2212 Rimuovi",  self._rimuovi_umore)]:
            ctk.CTkButton(ubf, text=txt, font=ctk.CTkFont(size=11),
                          fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                          corner_radius=8, height=30,
                          command=cmd).pack(fill="x", pady=(0, 4))

        sep = ctk.CTkFrame(self, fg_color=GRAY, height=2, corner_radius=0)
        sep.pack(padx=36, fill="x", pady=(16, 12))
        sep.pack_propagate(False)

        # ── Variabili ─────────────────────────────────────────
        ctk.CTkLabel(self, text="Variabili di scena",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=FG).pack(anchor="w", padx=36)
        ctk.CTkLabel(self,
                     text="Cosa vuoi che il personaggio ricordi? "
                          "Ogni variabile genera un pulsante QR e una voce nel lorebook.",
                     font=ctk.CTkFont(size=12), text_color=GRAY
                     ).pack(anchor="w", padx=36, pady=(2, 8))

        vf = ctk.CTkFrame(self, fg_color=BG2, corner_radius=8)
        vf.pack(padx=36, fill="x")
        self.listbox_var = tk.Listbox(vf, font=("Segoe UI", 12),
                                      bg=BG2, fg=FG,
                                      selectbackground=ACCENT, selectforeground=BG,
                                      relief="flat", bd=0, height=5)
        self.listbox_var.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        for v in self.variabili:
            self.listbox_var.insert("end", v)

        vbf = ctk.CTkFrame(vf, fg_color="transparent")
        vbf.pack(side="left", padx=(4, 6), pady=4)
        for txt, cmd in [("+ Aggiungi", self._aggiungi_var),
                         ("\u2212 Rimuovi",  self._rimuovi_var)]:
            ctk.CTkButton(vbf, text=txt, font=ctk.CTkFont(size=11),
                          fg_color=BTN_BG, text_color=FG, hover_color=BTN_HO,
                          corner_radius=8, height=30,
                          command=cmd).pack(fill="x", pady=(0, 4))

        self.lbl_ok = ctk.CTkLabel(self, text="",
                                    font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_ok.pack(pady=(12, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(10, 0))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=12),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 16))
        ctk.CTkButton(btn_row, text="Salva e installa in SillyTavern",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._salva).pack(side="left")

    # ── Umori ─────────────────────────────────────────────────

    def _aggiungi_umore(self):
        self._popup_aggiungi("Nuovo stato d'umore",
                             "Nome del nuovo stato d'umore:",
                             self.umori, self.listbox_umori)

    def _rimuovi_umore(self):
        sel = self.listbox_umori.curselection()
        if sel:
            self.listbox_umori.delete(sel[0])
            self.umori.pop(sel[0])

    # ── Variabili ─────────────────────────────────────────────

    def _aggiungi_var(self):
        self._popup_aggiungi("Nuova variabile",
                             "Nome della variabile (solo lettere e underscore):",
                             self.variabili, self.listbox_var,
                             validatore=self._valida_var)

    def _rimuovi_var(self):
        sel = self.listbox_var.curselection()
        if sel:
            self.listbox_var.delete(sel[0])
            self.variabili.pop(sel[0])

    def _valida_var(self, testo):
        import re as _re
        return bool(_re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', testo))

    # ── Popup generico aggiungi ────────────────────────────────

    def _popup_aggiungi(self, titolo, prompt, lista, listbox, validatore=None):
        popup = ctk.CTkToplevel(self)
        popup.title(titolo)
        popup.resizable(False, False)
        _center_toplevel(popup, 380, 180)
        popup.deiconify()
        popup.grab_set()
        var = tk.StringVar()
        ctk.CTkLabel(popup, text=prompt,
                     font=ctk.CTkFont(size=12), text_color=FG
                     ).pack(pady=(16, 6), padx=20, anchor="w")
        e = ctk.CTkEntry(popup, textvariable=var, font=ctk.CTkFont(size=13),
                         fg_color=BG2, text_color=FG,
                         border_color=BTN_BG, corner_radius=8)
        e.pack(padx=20, fill="x")
        self.lbl_err = ctk.CTkLabel(popup, text="",
                                     font=ctk.CTkFont(size=10), text_color=RED)
        self.lbl_err.pack(padx=20, anchor="w")
        e.focus_set()
        def ok():
            v = var.get().strip().lower()
            if not v:
                return
            if validatore and not validatore(v):
                self.lbl_err.configure(text="Nome non valido — solo lettere, numeri, underscore.")
                return
            if v in lista:
                self.lbl_err.configure(text="Variabile già presente.")
                return
            lista.append(v)
            listbox.insert("end", v)
            popup.destroy()
        e.bind("<Return>", lambda _: ok())
        ctk.CTkButton(popup, text="Aggiungi",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=ok).pack(pady=(8, 0))

    # ── Salva ──────────────────────────────────────────────────

    def _salva(self):
        umori = list(self.listbox_umori.get(0, "end"))
        if not umori:
            self.lbl_ok.configure(
                text="\u26a0  Aggiungi almeno uno stato d'umore.",
                text_color=RED)
            return
        variabili_attive = {v: True for v in self.variabili}
        data = {**self.dati_precedenti,
                "nome": self.nome, "genere": self.genere,
                "umori": umori, "variabili_attive": variabili_attive}
        self.destroy()
        self.callback_avanti(data)

    def _annulla(self):
        cb = self.callback_annulla
        self.destroy()
        cb()

# ============================================================
# SCREEN COMPLETE — Riepilogo post-installazione
# ============================================================

class ScreenComplete(ctk.CTkToplevel):
    def __init__(self, parent, nome, risultato, callback_chiudi):
        super().__init__(parent)
        self.withdraw()
        self.title(APP_TITLE)
        self.resizable(False, False)
        _center_toplevel(self, 680, 720)
        self.callback_chiudi = callback_chiudi
        self._build(nome, risultato)
        self.deiconify()
        self.grab_set()
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self._chiudi)

    def _build(self, nome, risultato):
        ctk.CTkLabel(self, text="\u2713  Installazione completata!",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=GREEN).pack(pady=(32, 8))
        ctk.CTkLabel(self, text=f"{nome} \xe8 pronto in SillyTavern.",
                     font=ctk.CTkFont(size=13), text_color=FG).pack(pady=(0, 20))

        ff = ctk.CTkFrame(self, fg_color=BG2, corner_radius=8)
        ff.pack(padx=40, fill="x", pady=(0, 12))
        ctk.CTkLabel(ff, text="File installati:",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(anchor="w", padx=12, pady=(10, 4))
        ctk.CTkLabel(ff, text=f"\U0001f9e0 {nome}.png (Scheda personaggio)",
                     font=ctk.CTkFont(size=12), text_color=GREEN).pack(anchor="w", padx=24, pady=2)
        ctk.CTkLabel(ff, text=f"\U0001f4c4 {os.path.basename(risultato['authornote'])}",
                     font=ctk.CTkFont(size=12), text_color=GREEN).pack(anchor="w", padx=24, pady=2)
        ctk.CTkLabel(ff, text=f"\u26a1 {nome}.json (Quick Reply)",
                     font=ctk.CTkFont(size=12), text_color=GREEN).pack(anchor="w", padx=24, pady=(2, 10))

        istruzioni = (
            f"Istruzioni\n\n"
            f"1. Apri SillyTavern e vai nella chat di {nome}\n"
            f"2. Clicca su Extensions \u2192 Quick Reply\n"
            f"3. Assicurati che \"Enable Quick Replies\" sia attivo\n"
            f"4. Vai su \"Global Quick Reply Sets\", clicca + e seleziona \"{nome}\"\n"
            f"5. Spunta il flag \"Buttons\" accanto al set\n"
            f"6. Fai lo stesso in \"Chat Quick Reply Sets\": clicca + e seleziona \"{nome}\"\n"
            f"7. Spunta anche l\u00ec il flag \"Buttons\"\n"
            f"8. In \"Edit Quick Replies\" seleziona \"{nome}\" dal menu a tendina\n"
            f"9. I pulsanti appariranno in basso nella chat"
        )
        txt_istr = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                  wrap="word", height=150)
        txt_istr.pack(padx=40, fill="x", pady=(0, 16))
        txt_istr.insert("1.0", istruzioni)
        txt_istr.configure(state="disabled")

        ctk.CTkButton(self, text="Ho capito, chiudi",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._chiudi
                      ).pack(pady=(0, 24))

    def _chiudi(self):
        self.destroy()
        self.callback_chiudi()

# ============================================================
# SCREEN INFO — visualizza tutti i campi del personaggio
# ============================================================

class ScreenInfo(ctk.CTkToplevel):
    def __init__(self, parent, st_folder, nome):
        super().__init__(parent)
        self.withdraw()
        self.title(f"Info personaggio \u2014 {nome.capitalize()}")
        self.resizable(True, True)
        _center_toplevel(self, 940, 700)
        self.st_folder   = st_folder
        self.nome        = nome
        self._thumb_ref  = None
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        sf   = self.st_folder
        nome = self.nome

        char_data = _read_character_data(sf, nome)
        umori     = _read_quickreply_umori(sf, nome)
        variabili = _read_quickreply_variables(sf, nome)
        genere    = _detect_genere(char_data.get("system_prompt", ""))

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        # --- Colonna sinistra: immagine fissa (rimane tk per PhotoImage) ---
        left = tk.Frame(outer, bg=BG2, width=160)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.pack_propagate(False)

        user_folder = get_st_user_folder(sf)
        photo = None
        if user_folder:
            path = os.path.join(user_folder, "characters", f"{nome}.png")
            if os.path.isfile(path):
                try:
                    photo = tk.PhotoImage(file=path)
                    pw, ph = photo.width(), photo.height()
                    if pw >= 10 and ph >= 10:
                        s = max(1, pw // 160, ph // 500)
                        if s > 1:
                            photo = photo.subsample(s, s)
                        self._thumb_ref = photo
                    else:
                        photo = None
                except Exception:
                    photo = None

        if photo:
            lbl_img = tk.Label(left, image=photo, bg=BG2, bd=0)
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        else:
            bg_col, fg_col = _INIT_COLORS[0]
            c = tk.Canvas(left, width=160, height=500,
                          bg=bg_col, highlightthickness=0, bd=0)
            c.create_text(80, 250, text=nome[0].upper(),
                          font=("Segoe UI", 48, "bold"), fill=fg_col)
            c.place(relx=0.5, rely=0.5, anchor="center")

        # --- Colonna destra: campi scrollabili ---
        right_wrap = ctk.CTkFrame(outer, fg_color="transparent")
        right_wrap.pack(side="left", fill="both", expand=True)

        scroll = ctk.CTkScrollableFrame(
            right_wrap, fg_color=BG,
            scrollbar_button_color=BTN_BG,
            scrollbar_button_hover_color=BTN_HO,
            corner_radius=0)
        scroll.pack(fill="both", expand=True)
        inner = scroll

        # Nome + data + genere
        hdr = ctk.CTkFrame(inner, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(hdr, text=nome.capitalize(),
                     font=ctk.CTkFont(size=20, weight="bold"), text_color=FG
                     ).pack(side="left")
        g_label = "Personaggio maschile" if genere == "M" else "Personaggio femminile"
        ctk.CTkLabel(hdr, text=f"  \u00b7  {g_label}",
                     font=ctk.CTkFont(size=12), text_color=GRAY
                     ).pack(side="left", pady=(6, 0))
        create_date = char_data.get("create_date", "")
        if create_date:
            ctk.CTkLabel(inner, text=f"Creato il {create_date}",
                         font=ctk.CTkFont(size=11), text_color=GRAY
                         ).pack(anchor="w")

        ctk.CTkFrame(inner, fg_color=BTN_BG, height=2, corner_radius=0).pack(fill="x", pady=(10, 4))

        # Campi testo
        self._campo(inner, "DESCRIZIONE",
                    char_data.get("description", ""), altezza=4)
        self._campo(inner, "PERSONALIT\u00c0",
                    char_data.get("personality", ""), altezza=3)
        self._campo(inner, "CONTESTO",
                    char_data.get("scenario", ""), altezza=3)

        ctk.CTkFrame(inner, fg_color=BTN_BG, height=2, corner_radius=0).pack(fill="x", pady=(12, 4))

        self._campo(inner, "PRIMO MESSAGGIO",
                    char_data.get("first_mes", ""), altezza=4)

        alt = char_data.get("alternate_greetings", [])
        if alt:
            ctk.CTkLabel(inner, text="SALUTI ALTERNATIVI",
                         font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                         ).pack(anchor="w", pady=(10, 2))
            for i, g in enumerate(alt, 1):
                ctk.CTkLabel(inner, text=f"  {i}.",
                             font=ctk.CTkFont(size=11, weight="bold"), text_color=ACCENT
                             ).pack(anchor="w")
                self._campo(inner, "", g, altezza=3)

        ctk.CTkFrame(inner, fg_color=BTN_BG, height=2, corner_radius=0).pack(fill="x", pady=(12, 4))

        self._campo(inner, "ISTRUZIONI PERSONAGGIO (system prompt)",
                    char_data.get("system_prompt", ""), altezza=5)
        self._campo(inner, "ESEMPI DI DIALOGO",
                    char_data.get("mes_example", ""), altezza=4)

        ctk.CTkFrame(inner, fg_color=BTN_BG, height=2, corner_radius=0).pack(fill="x", pady=(12, 4))

        # Umori
        ctk.CTkLabel(inner, text="STATI D\u2019UMORE",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w", pady=(6, 2))
        ctk.CTkLabel(inner, text="  \u00b7  ".join(umori) if umori else "\u2014",
                     font=ctk.CTkFont(size=12), text_color=FG,
                     wraplength=500, justify="left"
                     ).pack(anchor="w")

        # Variabili attive
        ctk.CTkLabel(inner, text="VARIABILI ATTIVE",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w", pady=(10, 2))
        voci = list(variabili.keys()) if variabili else []
        if voci:
            ctk.CTkLabel(inner, text="  \u00b7  ".join(v.capitalize() for v in voci),
                         font=ctk.CTkFont(size=12), text_color=FG,
                         wraplength=500, justify="left"
                         ).pack(anchor="w", pady=1)
        else:
            ctk.CTkLabel(inner, text="\u2014",
                         font=ctk.CTkFont(size=12), text_color=GRAY
                         ).pack(anchor="w")

        # Chiudi
        ctk.CTkFrame(inner, fg_color="transparent", height=8).pack()
        ctk.CTkButton(inner, text="Chiudi",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self.destroy
                      ).pack(pady=(0, 4))

    def _campo(self, parent, etichetta, testo, altezza=3):
        if etichetta:
            ctk.CTkLabel(parent, text=etichetta,
                         font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                         ).pack(anchor="w", pady=(8, 2))
        if testo and testo.strip():
            txt = ctk.CTkTextbox(parent, font=ctk.CTkFont(size=12),
                                 wrap="word", height=altezza * 28)
            txt.pack(fill="x")
            txt.insert("1.0", testo)
            txt.configure(state="disabled")
        else:
            ctk.CTkLabel(parent, text="\u2014",
                         font=ctk.CTkFont(size=12), text_color=GRAY
                         ).pack(anchor="w")

# ============================================================
# SCREEN LOREBOOK — crea / modifica lorebook di un personaggio
# ============================================================

class ScreenLorebook(ctk.CTkToplevel):
    def __init__(self, parent, st_folder, nome, callback_chiudi=None):
        super().__init__(parent)
        self.withdraw()
        self.title(f"Lorebook di {nome.capitalize()}")
        self.resizable(True, True)
        _center_toplevel(self, 900, 660)
        self.st_folder       = st_folder
        self.nome            = nome
        self.callback_chiudi = callback_chiudi or (lambda: None)
        self.entries         = read_lorebook_file(st_folder, nome)
        self._idx_sel        = None
        self._uid_counter    = max((e["uid"] for e in self.entries),
                                   default=-1) + 1
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()
        if self.entries:
            self.listbox.selection_set(0)
            self._on_select()

    def _build(self):
        ctk.CTkLabel(self, text=f"Lorebook di {self.nome.capitalize()}",
                     font=ctk.CTkFont(size=17, weight="bold"), text_color=ACCENT
                     ).pack(pady=(20, 4))
        ctk.CTkLabel(self,
                     text="Ogni voce viene iniettata nel contesto quando "
                          "le parole chiave appaiono nella conversazione.",
                     font=ctk.CTkFont(size=12), text_color=GRAY
                     ).pack(pady=(0, 12))

        # Pulsanti fondo — prima del frame espandibile
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(side="bottom", pady=(8, 12))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=13),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(btn_row, text="\U0001f4be  Salva lorebook",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._salva_lorebook
                      ).pack(side="left")

        # Area principale
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20)

        # --- Sinistra: lista voci (tk.Listbox — nessun equivalente CTk) ---
        left = ctk.CTkFrame(main, fg_color="transparent")
        left.pack(side="left", fill="y", padx=(0, 16))

        ctk.CTkLabel(left, text="VOCI",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")

        self.listbox = tk.Listbox(left,
                                  font=("Segoe UI", 12),
                                  bg=BG2, fg=FG,
                                  selectbackground=ACCENT, selectforeground=BG,
                                  relief="flat", bd=4,
                                  width=22, height=14)
        self.listbox.pack(fill="y", expand=True, pady=(4, 6))
        self.listbox.bind("<<ListboxSelect>>", lambda e: self._on_select())

        for entry in self.entries:
            self.listbox.insert("end", self._label(entry))

        bf = ctk.CTkFrame(left, fg_color="transparent")
        bf.pack(fill="x")
        ctk.CTkButton(bf, text="+ Nuova voce",
                      font=ctk.CTkFont(size=11),
                      fg_color=BTN_BG, text_color="#f9e2af", hover_color=BTN_HO,
                      corner_radius=8, command=self._nuova_voce
                      ).pack(fill="x", pady=(0, 3))
        ctk.CTkButton(bf, text="\u2212 Rimuovi voce",
                      font=ctk.CTkFont(size=11),
                      fg_color=BTN_BG, text_color=RED, hover_color=BTN_HO,
                      corner_radius=8, command=self._rimuovi_voce
                      ).pack(fill="x")

        # --- Destra: form ---
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        # Nome voce
        ctk.CTkLabel(right, text="NOME VOCE",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")
        self.entry_nome = ctk.CTkEntry(right, font=ctk.CTkFont(size=12),
                                       fg_color=BG2, border_color=BTN_BG,
                                       corner_radius=8, height=36)
        self.entry_nome.pack(fill="x", pady=(2, 10))

        # Parole chiave
        ctk.CTkLabel(right,
                     text="PAROLE CHIAVE  \u2014 separate da virgola",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")
        self.entry_kw = ctk.CTkEntry(right, font=ctk.CTkFont(size=12),
                                     fg_color=BG2, border_color=BTN_BG,
                                     corner_radius=8, height=36)
        self.entry_kw.pack(fill="x", pady=(2, 10))

        # Contenuto
        ctk.CTkLabel(right, text="CONTENUTO",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")
        self.txt_contenuto = ctk.CTkTextbox(right, font=ctk.CTkFont(size=12),
                                            wrap="word", height=200)
        self.txt_contenuto.pack(fill="both", expand=True, pady=(2, 10))

        # Profondità
        depth_row = ctk.CTkFrame(right, fg_color="transparent")
        depth_row.pack(anchor="w")
        ctk.CTkLabel(depth_row, text="PROFONDIT\u00c0",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(side="left", padx=(0, 8))
        self.spin_depth = tk.Spinbox(depth_row,
                                     from_=1, to=10, width=4,
                                     font=("Segoe UI", 12),
                                     bg=BG2, fg=FG,
                                     buttonbackground=BTN_BG,
                                     relief="flat", bd=2)
        self.spin_depth.pack(side="left")
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, "4")
        ctk.CTkLabel(depth_row,
                     text="  messaggi dalla fine del contesto",
                     font=ctk.CTkFont(size=11), text_color=GRAY
                     ).pack(side="left")

        # Salva voce
        sv_row = ctk.CTkFrame(right, fg_color="transparent")
        sv_row.pack(anchor="e", pady=(10, 0))
        self.btn_salva_voce = ctk.CTkButton(sv_row, text="\u2713  Salva voce",
                                            font=ctk.CTkFont(size=12),
                                            fg_color=BTN_BG, text_color=GREEN,
                                            hover_color=BTN_HO, corner_radius=8,
                                            state="disabled",
                                            command=self._salva_voce)
        self.btn_salva_voce.pack(side="left", padx=(0, 8))
        self.lbl_stato = ctk.CTkLabel(sv_row, text="",
                                      font=ctk.CTkFont(size=11), text_color=GREEN)
        self.lbl_stato.pack(side="left")

        self._form_enabled(False)

    # ----------------------------------------------------------

    def _label(self, entry):
        n = entry.get("comment", "").strip()
        return n if n else "(senza nome)"

    def _form_enabled(self, state):
        s = "normal" if state else "disabled"
        for w in [self.entry_nome, self.entry_kw,
                  self.txt_contenuto, self.spin_depth,
                  self.btn_salva_voce]:
            try:
                w.configure(state=s)
            except Exception:
                pass

    def _on_select(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        self._idx_sel = sel[0]
        entry = self.entries[self._idx_sel]
        self._form_enabled(True)
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, entry.get("comment", ""))
        self.entry_kw.delete(0, "end")
        self.entry_kw.insert(0, ", ".join(entry.get("key", [])))
        self.txt_contenuto.delete("1.0", "end")
        self.txt_contenuto.insert("1.0", entry.get("content", ""))
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, str(entry.get("depth", 4)))
        self.lbl_stato.configure(text="")

    def _salva_voce(self):
        if self._idx_sel is None:
            return
        kw_raw = self.entry_kw.get().strip()
        try:
            depth = max(1, min(10, int(self.spin_depth.get())))
        except ValueError:
            depth = 4
        self.entries[self._idx_sel].update({
            "comment": self.entry_nome.get().strip(),
            "key":     [k.strip() for k in kw_raw.split(",") if k.strip()],
            "content": self.txt_contenuto.get("1.0", "end-1c").strip(),
            "depth":   depth,
        })
        self.listbox.delete(self._idx_sel)
        self.listbox.insert(self._idx_sel,
                            self._label(self.entries[self._idx_sel]))
        self.listbox.selection_set(self._idx_sel)
        self.lbl_stato.configure(text="\u2713 Salvata")
        self.after(2000, lambda: self.lbl_stato.configure(text=""))

    def _nuova_voce(self):
        uid   = self._uid_counter
        self._uid_counter += 1
        entry = {"uid": uid, "comment": "", "key": [], "content": "", "depth": 4}
        self.entries.append(entry)
        self.listbox.insert("end", self._label(entry))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set("end")
        self.listbox.see("end")
        self._idx_sel = len(self.entries) - 1
        self._form_enabled(True)
        self.entry_nome.delete(0, "end")
        self.entry_kw.delete(0, "end")
        self.txt_contenuto.delete("1.0", "end")
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, "4")
        self.lbl_stato.configure(text="")
        self.entry_nome.focus_set()

    def _rimuovi_voce(self):
        if self._idx_sel is None:
            return
        self.entries.pop(self._idx_sel)
        self.listbox.delete(self._idx_sel)
        self._idx_sel = None
        self._form_enabled(False)
        self.entry_nome.delete(0, "end")
        self.entry_kw.delete(0, "end")
        self.txt_contenuto.delete("1.0", "end")

    def _salva_lorebook(self):
        try:
            path = write_lorebook_file(self.st_folder, self.nome, self.entries)
            _set_character_world(self.st_folder, self.nome, self.nome)
            messagebox.showinfo(APP_TITLE,
                f"\u2713  Lorebook salvato!\n\n"
                f"Il lorebook di {self.nome.capitalize()} \u00e8 attivo.\n"
                f"In SillyTavern apparir\u00e0 automaticamente nella chat.")
            self.destroy()
            self.callback_chiudi()
        except Exception as ex:
            messagebox.showerror(APP_TITLE,
                f"Errore durante il salvataggio:\n{ex}")

    def _annulla(self):
        self.destroy()

# ============================================================
# SCREEN LOREBOOK DINAMICO — voci always-on dalle variabili
# ============================================================

class ScreenLorebookDinamico(ctk.CTkToplevel):
    def __init__(self, parent, st_folder, nome, callback_chiudi=None):
        super().__init__(parent)
        self.withdraw()
        self.title(f"Lorebook dinamico di {nome.capitalize()}")
        self.resizable(True, True)
        _center_toplevel(self, 900, 580)
        self.st_folder       = st_folder
        self.nome            = nome
        self.callback_chiudi = callback_chiudi or (lambda: None)
        self.entries         = read_lorebook_dinamico_file(st_folder, nome)
        if not self.entries:
            variabili_attive = _read_quickreply_variables(st_folder, nome)
            self.entries = generate_lorebook_dinamico_entries(nome, variabili_attive)
        self._idx_sel = None
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()
        if self.entries:
            self.listbox.selection_set(0)
            self._on_select()

    def _build(self):
        ctk.CTkLabel(self, text=f"Lorebook dinamico di {self.nome.capitalize()}",
                     font=ctk.CTkFont(size=17, weight="bold"), text_color=ACCENT
                     ).pack(pady=(20, 4))
        ctk.CTkLabel(self,
                     text="Ogni voce viene iniettata automaticamente ad ogni messaggio "
                          "con il valore aggiornato della variabile.",
                     font=ctk.CTkFont(size=12), text_color=GRAY
                     ).pack(pady=(0, 12))

        # Pulsanti fondo
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(side="bottom", pady=(8, 12))
        ctk.CTkButton(btn_row, text="Annulla", font=ctk.CTkFont(size=13),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self._annulla
                      ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(btn_row, text="\U0001f4be  Salva lorebook dinamico",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=ACCENT, text_color=BG, hover_color="#b4befe",
                      corner_radius=8, command=self._salva_lorebook
                      ).pack(side="left")

        # Area principale
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20)

        # --- Sinistra: lista voci (tk.Listbox — nessun equivalente CTk) ---
        left = ctk.CTkFrame(main, fg_color="transparent")
        left.pack(side="left", fill="y", padx=(0, 16))

        ctk.CTkLabel(left, text="VARIABILI",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")

        self.listbox = tk.Listbox(left,
                                  font=("Segoe UI", 12),
                                  bg=BG2, fg=FG,
                                  selectbackground=ACCENT, selectforeground=BG,
                                  relief="flat", bd=4,
                                  width=18, height=10)
        self.listbox.pack(fill="y", expand=True, pady=(4, 6))
        self.listbox.bind("<<ListboxSelect>>", lambda e: self._on_select())

        for entry in self.entries:
            self.listbox.insert("end", entry.get("comment", "(voce)"))

        # --- Destra: form ---
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(right, text="VARIABILE",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")
        self.lbl_var = ctk.CTkLabel(right, text="\u2014",
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    fg_color=BG2, text_color=ACCENT,
                                    anchor="w", corner_radius=8)
        self.lbl_var.pack(fill="x", pady=(2, 10), ipady=4)

        ctk.CTkLabel(right, text="CONTENUTO INIETTATO",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(anchor="w")
        self.txt_contenuto = ctk.CTkTextbox(right, font=ctk.CTkFont(size=12),
                                            wrap="word", height=180)
        self.txt_contenuto.pack(fill="both", expand=True, pady=(2, 10))

        dr = ctk.CTkFrame(right, fg_color="transparent")
        dr.pack(anchor="w", fill="x")
        ctk.CTkLabel(dr, text="PROFONDIT\u00c0",
                     font=ctk.CTkFont(size=9, weight="bold"), text_color=GRAY
                     ).pack(side="left", padx=(0, 8))
        self.spin_depth = tk.Spinbox(dr, from_=1, to=10, width=4,
                                     font=("Segoe UI", 12),
                                     bg=BG2, fg=FG,
                                     buttonbackground=BTN_BG,
                                     relief="flat", bd=2)
        self.spin_depth.pack(side="left")
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, "2")
        ctk.CTkLabel(dr, text="  messaggi dalla fine",
                     font=ctk.CTkFont(size=11), text_color=GRAY
                     ).pack(side="left")

        # Salva voce
        sv_row = ctk.CTkFrame(right, fg_color="transparent")
        sv_row.pack(anchor="e", pady=(10, 0))
        self.btn_salva_voce = ctk.CTkButton(sv_row, text="\u2713  Salva voce",
                                            font=ctk.CTkFont(size=12),
                                            fg_color=BTN_BG, text_color=GREEN,
                                            hover_color=BTN_HO, corner_radius=8,
                                            state="disabled",
                                            command=self._salva_voce)
        self.btn_salva_voce.pack(side="left", padx=(0, 8))
        self.lbl_stato = ctk.CTkLabel(sv_row, text="",
                                      font=ctk.CTkFont(size=11), text_color=GREEN)
        self.lbl_stato.pack(side="left")

        self._form_enabled(False)

    # ----------------------------------------------------------

    def _form_enabled(self, state):
        s = "normal" if state else "disabled"
        for w in [self.txt_contenuto, self.spin_depth, self.btn_salva_voce]:
            try:
                w.configure(state=s)
            except Exception:
                pass

    def _on_select(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        self._idx_sel = sel[0]
        entry = self.entries[self._idx_sel]
        self._form_enabled(True)
        self.lbl_var.configure(text=entry.get("comment", "\u2014"))
        self.txt_contenuto.delete("1.0", "end")
        self.txt_contenuto.insert("1.0", entry.get("content", ""))
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, str(entry.get("depth", 2)))
        self.lbl_stato.configure(text="")

    def _salva_voce(self):
        if self._idx_sel is None:
            return
        try:
            depth = max(1, min(10, int(self.spin_depth.get())))
        except ValueError:
            depth = 2
        self.entries[self._idx_sel].update({
            "content": self.txt_contenuto.get("1.0", "end-1c").strip(),
            "depth":   depth,
        })
        self.lbl_stato.configure(text="\u2713 Salvata")
        self.after(2000, lambda: self.lbl_stato.configure(text=""))

    def _salva_lorebook(self):
        try:
            path = write_lorebook_dinamico_file(self.st_folder, self.nome, self.entries)
            _set_character_world(self.st_folder, self.nome, f"{self.nome}_dinamico")
            messagebox.showinfo(APP_TITLE,
                f"\u2713  Lorebook dinamico salvato!\n\n"
                f"Le variabili di {self.nome.capitalize()} verranno iniettate\n"
                f"automaticamente ad ogni messaggio.\n\n"
                f"Nota: se hai anche un lorebook statico, attivalo manualmente\n"
                f"nelle impostazioni World Info di SillyTavern.")
            self.destroy()
            self.callback_chiudi()
        except Exception as ex:
            messagebox.showerror(APP_TITLE,
                f"Errore durante il salvataggio:\n{ex}")

    def _annulla(self):
        self.destroy()

# ============================================================
# SCREEN 4 — Inietta le note dell'autore
# ============================================================

class Screen4(ctk.CTkToplevel):
    def __init__(self, parent, st_folder, nome_iniziale=None):
        super().__init__(parent)
        self.withdraw()
        self.title("Inietta le note dell'autore")
        self.resizable(False, True)
        _center_toplevel(self, 740, 740)
        self.st_folder      = st_folder
        self.nome_corrente  = ""
        self._icone_tk      = []
        self._nome_iniziale = nome_iniziale
        self._nome_file_map = {}
        self._build()
        self.deiconify()
        self.grab_set()
        self.lift()

    def _build(self):
        ctk.CTkLabel(self, text="Inietta le note dell'autore",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color=ACCENT).pack(pady=(24, 4))
        ctk.CTkLabel(self,
                     text="Le note vengono generate automaticamente dal personaggio installato.\n"
                          "Puoi modificarle prima di copiarle.",
                     font=ctk.CTkFont(size=12), text_color=GRAY,
                     justify="center").pack(pady=(0, 12))

        # Lista personaggi da PNG
        files = list_character_files(self.st_folder)

        if not files:
            ctk.CTkLabel(self,
                         text="Nessun personaggio installato ancora.\n"
                              "Crea prima un personaggio dal menu principale.",
                         font=ctk.CTkFont(size=13), text_color=GRAY,
                         justify="center").pack(pady=30)
            ctk.CTkButton(self, text="Annulla", font=ctk.CTkFont(size=13),
                          fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                          corner_radius=8, command=self.destroy
                          ).pack(pady=(20, 0))
            return

        self.files = files
        nomi_display = [f.replace(".png", "").capitalize() for f in files]
        self._nome_file_map = {nd: f for nd, f in zip(nomi_display, files)}

        # Selezione personaggio
        sf = ctk.CTkFrame(self, fg_color="transparent")
        sf.pack(padx=36, fill="x", pady=(0, 10))
        ctk.CTkLabel(sf, text="Personaggio:", font=ctk.CTkFont(size=12),
                     text_color=FG).pack(side="left", padx=(0, 8))
        self.combo = ctk.CTkComboBox(sf, values=nomi_display,
                                     font=ctk.CTkFont(size=12),
                                     state="readonly",
                                     fg_color=BG2, border_color=BTN_BG,
                                     button_color=BTN_BG, button_hover_color=BTN_HO,
                                     dropdown_fg_color=BG2,
                                     command=self._on_combo_change)
        # Pre-selezione
        idx_carica = 0
        if self._nome_iniziale:
            try:
                idx_carica = [f.replace(".png", "") for f in files].index(self._nome_iniziale)
            except ValueError:
                pass
        self.combo.set(nomi_display[idx_carica])
        self.combo.pack(side="left")

        # Label + hint modificabile
        lr = ctk.CTkFrame(self, fg_color="transparent")
        lr.pack(padx=36, fill="x", pady=(0, 2))
        ctk.CTkLabel(lr, text="Testo da incollare in Author's Note:",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG).pack(side="left")
        ctk.CTkLabel(lr, text="  (puoi modificarlo)",
                     font=ctk.CTkFont(size=11), text_color=GRAY).pack(side="left")

        # Testo authornote — editabile
        self.txt_an = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12),
                                     text_color=GREEN, wrap="word", height=120)
        self.txt_an.pack(padx=36, fill="x")

        # Pulsante Copia e salva
        self.btn_copia = ctk.CTkButton(self, text="\U0001f4cb  Copia e salva",
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       fg_color=BTN_BG, text_color=FG,
                                       hover_color=BTN_HO, corner_radius=8,
                                       command=self._salva_e_copia)
        self.btn_copia.pack(pady=(10, 0))

        self.lbl_copiato = ctk.CTkLabel(self, text="",
                                        font=ctk.CTkFont(size=12), text_color=GREEN)
        self.lbl_copiato.pack(pady=(4, 0))

        ctk.CTkFrame(self, fg_color=GRAY, height=2, corner_radius=0).pack(
            padx=36, fill="x", pady=(14, 10))

        # 4 passi
        ctk.CTkLabel(self, text="Come incollarlo in SillyTavern:",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=FG).pack(anchor="w", padx=36, pady=(0, 8))

        passi = [
            (ICON_STEP1_MENU,       "Passo 1 \u2014 In S.T. apri la chat del personaggio in questione"),
            (ICON_STEP2_AUTHORNOTE, "Passo 2 \u2014 A sinistra della riga di chat c'\xe8 un'icona con tre linee: cliccaci e seleziona \"Author's Note\""),
            (ICON_STEP3_COPY,       "Passo 3 \u2014 Nel pannello che si apre, incolla il testo copiato nel campo \"Checkpoints...\" in alto a sinistra"),
            (ICON_STEP4_CLOSE,      "Passo 4 \u2014 Chiudi il pannello sulla X"),
        ]
        for b64, testo in passi:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(padx=36, fill="x", pady=3)
            try:
                photo = tk.PhotoImage(data=b64)
                self._icone_tk.append(photo)
                tk.Label(row, image=photo, bg=BG, bd=0).pack(side="left", padx=(0, 12))
            except Exception:
                ctk.CTkLabel(row, text="\u25b8", font=ctk.CTkFont(size=13),
                             text_color=ACCENT).pack(side="left", padx=(0, 12))
            ctk.CTkLabel(row, text=testo, font=ctk.CTkFont(size=12),
                         text_color=FG, anchor="w", wraplength=560,
                         justify="left").pack(side="left", fill="x")

        ctk.CTkButton(self, text="Annulla", font=ctk.CTkFont(size=13),
                      fg_color=BTN_BG, text_color=GRAY, hover_color=BTN_HO,
                      corner_radius=8, command=self.destroy
                      ).pack(pady=(16, 16))

        # Carica il personaggio pre-selezionato
        self._carica(files[idx_carica])

    def _on_combo_change(self, value):
        filename = self._nome_file_map.get(value)
        if filename:
            self._carica(filename)

    def _carica(self, filename):
        nome = filename.replace(".png", "")
        self.nome_corrente = nome
        # Prova a leggere l'authornote già salvato
        user_folder = get_st_user_folder(self.st_folder)
        testo = None
        if user_folder:
            path = os.path.join(user_folder, "st_character_manager",
                                f"{nome.lower()}_authornote.txt")
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        testo = f.read()
                except Exception:
                    pass
        # Se non esiste, rigenera dalle variabili del Quick Reply
        if not testo:
            variabili_attive = _read_quickreply_variables(self.st_folder, nome)
            testo = generate_authornote(nome, variabili_attive)
        self.txt_an.delete("1.0", "end")
        self.txt_an.insert("1.0", testo)

    def _salva_e_copia(self):
        testo = self.txt_an.get("1.0", "end-1c").strip()
        if not testo:
            return
        try:
            write_authornote_file(self.st_folder, self.nome_corrente, testo)
        except Exception:
            pass
        self.clipboard_clear()
        self.clipboard_append(testo)
        self.lbl_copiato.configure(text="\u2713 Copiato e salvato! Ora vai in SillyTavern.")
        self.after(3000, lambda: self.lbl_copiato.configure(text=""))

# ============================================================
# SCREEN 0 FRAME — primo avvio inline (Frame, non Toplevel)
# ============================================================

class Screen0Frame(tk.Frame):
    def __init__(self, parent, callback_ok):
        super().__init__(parent, bg=BG)
        self.callback_ok = callback_ok
        self.st_folder   = tk.StringVar()
        self._build()

    def _build(self):
        tk.Label(self, text=APP_TITLE,
                 font=("Segoe UI", 18, "bold"), bg=BG, fg=ACCENT).pack(pady=(32, 4))
        tk.Label(self, text="Prima di iniziare, dimmi dove hai installato SillyTavern.",
                 font=("Segoe UI", 13), bg=BG, fg=FG).pack(pady=(0, 2))
        tk.Label(self, text="Lo chiedo una volta sola — poi me lo ricordo.",
                 font=("Segoe UI", 12), bg=BG, fg=GRAY).pack(pady=(0, 20))

        row = tk.Frame(self, bg=BG)
        row.pack(padx=44, fill="x")
        tk.Entry(row, textvariable=self.st_folder, font=("Segoe UI", 12),
                 bg=BG2, fg=FG, insertbackground=FG,
                 readonlybackground=BG2, disabledforeground=FG,
                 relief="flat", bd=4, state="readonly"
                 ).pack(side="left", fill="x", expand=True, ipady=6)
        tk.Button(row, text="Sfoglia", font=("Segoe UI", 12),
                  bg=BTN_BG, fg=FG, activebackground=BTN_HO, activeforeground=FG,
                  relief="flat", bd=0, padx=14, pady=6, cursor="hand2",
                  command=self._browse).pack(side="left", padx=(8, 0))

        self.lbl_ok = tk.Label(self, text="", font=("Segoe UI", 12), bg=BG, fg=GREEN)
        self.lbl_ok.pack(pady=(10, 0))

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=(18, 0))
        self.btn_go = tk.Button(btn_row, text="Pronti, si parte!",
                                font=("Segoe UI", 13, "bold"), bg=ACCENT, fg=BG,
                                activebackground="#b4befe", activeforeground=BG,
                                relief="flat", bd=0, padx=20, pady=8,
                                cursor="hand2", state="disabled", command=self._confirm)
        self.btn_go.pack()

    def _browse(self):
        folder = filedialog.askdirectory(title="Seleziona la cartella di SillyTavern")
        if folder:
            self.st_folder.set(folder)
            self.lbl_ok.config(text="✓ Cartella selezionata")
            self.btn_go.config(state="normal")

    def _confirm(self):
        folder = self.st_folder.get()
        if not folder:
            return
        cfg = load_config()
        cfg["st_folder"] = folder
        save_config(cfg)
        self.callback_ok(folder)


# ============================================================
# STEP LIST — wizard nuovo e modifica
# ============================================================

WIZARD_STEPS_NUOVO = [
    lambda r: Screen0b(
        r.parent,
        lambda g: r.next({"genere": g}),
        r.prev,
        genere_iniziale=r.data.get("genere", "F")),
    lambda r: Screen1(
        r.parent, r.data["genere"],
        lambda n: r.next({"nome": n}),
        r.prev,
        nome_iniziale=r.data.get("nome", "")),
    lambda r: Screen1b(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda p: r.next({"image_path": p}) if p else r.next(),
        r.prev,
        image_path_iniziale=r.data.get("image_path", "")),
    lambda r: Screen2(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda d: r.next({"descrizione": d}),
        r.prev,
        testo_iniziale=r.data.get("descrizione", "")),
    lambda r: Screen2b(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        r.data.get("descrizione", ""),
        lambda c, p: r.next({"contesto": c, "primo_messaggio": p}),
        r.prev,
        contesto_iniziale=r.data.get("contesto", ""),
        primo_iniziale=r.data.get("primo_messaggio", "")),
    lambda r: Screen2c(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda p: r.next({"personality": p}),
        r.prev,
        testo_iniziale=r.data.get("personality", "")),
    lambda r: Screen2d(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda sp: r.next({"system_prompt": sp}),
        r.prev,
        testo_iniziale=r.data.get("system_prompt", "")),
    lambda r: Screen2d_note(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda prompt, depth: r.next({"char_note_prompt": prompt,
                                       "char_note_depth": depth}),
        r.prev,
        prompt_iniziale=r.data.get("char_note_prompt", ""),
        depth_iniziale=r.data.get("char_note_depth", 4)),
    lambda r: Screen2e(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda me: r.next({"mes_example": me}),
        r.prev,
        testo_iniziale=r.data.get("mes_example", "")),
    lambda r: Screen2f(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        lambda ag: r.next({"alternate_greetings": ag}),
        r.prev,
        greetings_iniziali=r.data.get("alternate_greetings", [])),
    lambda r: Screen3(
        r.parent, r.data["genere"], r.data.get("nome", ""),
        dict(r.data), r.next, r.prev,
        umori_iniziali=r.data.get("_umori_iniziali"),
        variabili_iniziali=r.data.get("_variabili_iniziali")),
]

# In modifica: salta Screen0b (genere) e Screen1 (nome) — partono da Screen1b
WIZARD_STEPS_MODIFICA = WIZARD_STEPS_NUOVO[2:]


# ============================================================
# MAIN MENU FRAME — menu principale inline (Frame)
# ============================================================

class MainMenuFrame(tk.Frame):
    def __init__(self, parent_app, config_data):
        super().__init__(parent_app, bg=BG)
        self.app         = parent_app
        self.config_data = config_data
        self._build_menubar()
        self._build()

    # ----------------------------------------------------------
    # Menubar
    # ----------------------------------------------------------

    def _chiedi_conferma(self, titolo, callback, messaggio=None):
        GRAY_SYS = "#f0f0f0"
        GRAY_TXT = "#1a1a1a"

        popup = tk.Toplevel(self.app)
        popup.title(titolo)
        popup.resizable(False, False)
        popup.configure(bg=GRAY_SYS)
        popup.grab_set()
        popup.transient(self.app)

        popup.update_idletasks()
        pw, ph = 340, 130 if not messaggio else 155
        sx = self.app.winfo_x() + (self.app.winfo_width()  - pw) // 2
        sy = self.app.winfo_y() + (self.app.winfo_height() - ph) // 2
        popup.geometry(f"{pw}x{ph}+{sx}+{sy}")

        # --- Area icona + testo ---
        top = tk.Frame(popup, bg=GRAY_SYS)
        top.pack(pady=(18, 4), padx=20, fill="x")

        icona = tk.Label(top, image="::tk::icons::question",
                         bg=GRAY_SYS, width=28, height=28)
        icona.pack(side="left", padx=(0, 14))

        tk.Label(top, text="Sei sicuro?", font=("Segoe UI", 13),
                 bg=GRAY_SYS, fg=GRAY_TXT, justify="left").pack(side="left")

        if messaggio:
            tk.Label(popup, text=messaggio, font=("Segoe UI", 11, "bold"),
                     bg=GRAY_SYS, fg="#c0392b", justify="center",
                     wraplength=300).pack(pady=(0, 8))

        # --- Pulsanti stile Windows ---
        row = tk.Frame(popup, bg=GRAY_SYS)
        row.pack(pady=(0, 14))

        result = [False]

        def _no():
            popup.destroy()

        def _si():
            result[0] = True
            popup.destroy()

        btn_no = tk.Button(row, text="No", font=("Segoe UI", 12),
                           bg=GRAY_SYS, fg=GRAY_TXT,
                           activebackground="#e0e0e0", activeforeground=GRAY_TXT,
                           relief="raised", bd=2, padx=16, pady=4,
                           cursor="hand2", width=8, command=_no)
        btn_no.pack(side="left", padx=(0, 8))

        tk.Button(row, text="Sì", font=("Segoe UI", 12),
                  bg=GRAY_SYS, fg=GRAY_TXT,
                  activebackground="#e0e0e0", activeforeground=GRAY_TXT,
                  relief="raised", bd=2, padx=16, pady=4,
                  cursor="hand2", width=8, command=_si).pack(side="left")

        btn_no.focus_set()
        popup.bind("<Return>", lambda e: _no())
        popup.bind("<Escape>", lambda e: _no())

        popup.wait_window()
        if result[0]:
            callback()

    def _coming_soon(self, titolo):
        self._chiedi_conferma(
            titolo,
            lambda: messagebox.showinfo(APP_TITLE, "Funzione in arrivo nella prossima versione.")
        )

    def _build_menubar(self):
        menubar = tk.Menu(self.app, bg=BG2, fg=FG,
                          activebackground=ACCENT, activeforeground=BG,
                          relief="flat", bd=0)

        def cs(label):
            return lambda: self._coming_soon(label)

        # --- Crea ---
        m_crea = tk.Menu(menubar, tearoff=0, bg=BG2, fg=FG,
                         activebackground=ACCENT, activeforeground=BG)
        m_crea.add_command(label="Nuovo personaggio",
                           command=lambda: self._chiedi_conferma(
                               "Nuovo personaggio", self._nuovo))
        m_crea.add_command(label="Nuovo Lorebook",
                           command=lambda: self._nuovo_lorebook())
        m_crea.add_command(label="Nuovo Lorebook dinamico",
                           command=lambda: self._nuovo_lorebook_dinamico())
        menubar.add_cascade(label="Crea", menu=m_crea)

        # --- Visualizza ---
        m_vis = tk.Menu(menubar, tearoff=0, bg=BG2, fg=FG,
                        activebackground=ACCENT, activeforeground=BG)
        m_vis.add_command(label="Info personaggio",
                          command=self._info_personaggio)
        menubar.add_cascade(label="Visualizza", menu=m_vis)

        # --- Modifica ---
        m_mod = tk.Menu(menubar, tearoff=0, bg=BG2, fg=FG,
                        activebackground=ACCENT, activeforeground=BG)
        m_mod.add_command(label="Inietta le note dell'autore",
                          command=lambda: Screen4(self, self.config_data.get("st_folder", "")))
        m_mod.add_separator()
        m_mod.add_command(label="Modifica Personaggio",
                          command=lambda: self._modifica_da_menu())
        m_mod.add_command(label="Modifica Lorebook",
                          command=lambda: self._modifica_lorebook())
        m_mod.add_command(label="Modifica Lorebook dinamico",
                          command=lambda: self._modifica_lorebook_dinamico())
        menubar.add_cascade(label="Modifica", menu=m_mod)

        # --- Impostazioni ---
        m_imp = tk.Menu(menubar, tearoff=0, bg=BG2, fg=FG,
                        activebackground=ACCENT, activeforeground=BG)
        m_imp.add_command(label="Resetta percorso S.T.",
                          command=lambda: self._chiedi_conferma(
                              "Resetta percorso S.T.", self._resetta_percorso))
        m_imp.add_command(label="Resetta personaggio",
                          command=lambda: self._resetta_personaggio())
        m_imp.add_command(label="Resetta Lorebook",
                          command=lambda: self._resetta_lorebook())
        m_imp.add_command(label="Resetta Lorebook dinamico",
                          command=lambda: self._resetta_lorebook_dinamico())
        menubar.add_cascade(label="Impostazioni", menu=m_imp)

        # --- Help ---
        m_help = tk.Menu(menubar, tearoff=0, bg=BG2, fg=FG,
                         activebackground=ACCENT, activeforeground=BG)
        m_help.add_command(label="Info generali",
                           command=cs("Info generali"))
        menubar.add_cascade(label="Help", menu=m_help)

        self.app.config(menu=menubar)

    # ----------------------------------------------------------
    # Dashboard
    # ----------------------------------------------------------

    def _build(self):
        if not _CTK_OK:
            tk.Label(self,
                     text="Installa customtkinter per la dashboard:\npip install customtkinter",
                     font=("Segoe UI", 12), bg=BG, fg=RED).pack(expand=True)
            return

        self._sidebar_outer = tk.Frame(self, bg=BG2, width=230)
        self._sidebar_outer.pack(side="left", fill="y")
        self._sidebar_outer.pack_propagate(False)

        tk.Frame(self, bg=BTN_BG, width=1).pack(side="left", fill="y")

        self._detail = tk.Frame(self, bg=BG)
        self._detail.pack(side="left", fill="both", expand=True)

        hdr = tk.Frame(self._sidebar_outer, bg=BG2)
        hdr.pack(fill="x")
        tk.Label(hdr, text="I TUOI PERSONAGGI",
                 font=("Segoe UI", 8), bg=BG2, fg=GRAY
                 ).pack(side="left", padx=16, pady=(14, 8))

        self._scroll = ctk.CTkScrollableFrame(
            self._sidebar_outer,
            fg_color=BG2,
            scrollbar_button_color=BTN_BG,
            scrollbar_button_hover_color=BTN_HO,
            corner_radius=0,
            width=218
        )
        self._scroll.pack(fill="both", expand=True)

        tk.Frame(self._sidebar_outer, bg=BTN_BG, height=1).pack(fill="x")
        self._btn_sidebar_new = tk.Button(
            self._sidebar_outer,
            text="\uff0b  Nuovo personaggio",
            font=("Segoe UI", 12), bg=BG2, fg="#f9e2af",
            activebackground=BTN_BG, activeforeground=ACCENT,
            relief="flat", bd=0, padx=16, pady=12,
            anchor="w", cursor="hand2",
            command=self._nuovo_da_dashboard
        )
        self._btn_sidebar_new.pack(fill="x")
        self._btn_sidebar_new.bind("<Enter>",
            lambda e: self._btn_sidebar_new.config(fg=ACCENT))
        self._btn_sidebar_new.bind("<Leave>",
            lambda e: self._btn_sidebar_new.config(fg="#f9e2af"))

        self._selected_char = None
        self._thumb_cache   = {}
        self._sidebar_items = {}

        self._popola_sidebar()

    def _popola_sidebar(self, nome_nuovo=None):
        for w in self._scroll.winfo_children():
            w.destroy()
        self._sidebar_items.clear()
        self._thumb_cache.clear()

        sf = self.config_data.get("st_folder", "")
        self._chars = list_character_files(sf) if sf else []

        if not self._chars:
            tk.Label(self._scroll,
                     text="Nessun personaggio\nancora creato",
                     font=("Segoe UI", 11), bg=BG2, fg=GRAY,
                     justify="center").pack(pady=24)
            self._mostra_placeholder()
            return

        for i, fname in enumerate(self._chars):
            nome = fname.replace(".png", "")
            bg_col, fg_col = _INIT_COLORS[i % len(_INIT_COLORS)]
            self._aggiungi_sidebar_item(nome, bg_col, fg_col)

        nomi = [f.replace(".png", "") for f in self._chars]
        if nome_nuovo and nome_nuovo in nomi:
            idx = nomi.index(nome_nuovo)
        else:
            idx = 0
        target = nomi[idx]
        bg_t, fg_t = _INIT_COLORS[idx % len(_INIT_COLORS)]
        self._seleziona(target, bg_t, fg_t)

    def _aggiungi_sidebar_item(self, nome, bg_col, fg_col):
        outer = tk.Frame(self._scroll, bg=BG2, cursor="hand2")
        outer.pack(fill="x", pady=1)

        indicator = tk.Frame(outer, bg=BG2, width=3)
        indicator.pack(side="left", fill="y")

        inner = tk.Frame(outer, bg=BG2)
        inner.pack(side="left", fill="x", expand=True)

        sf    = self.config_data.get("st_folder", "")
        photo = self._load_thumb(nome, sf, 34, 52)
        if photo:
            av = tk.Label(inner, image=photo, bg=BG2, bd=0)
            av._photo = photo
        else:
            av = self._make_avatar(inner, nome, bg_col, fg_col, 34, 52)
        av.pack(side="left", padx=(10, 8), pady=10)

        lbl = tk.Label(inner, text=nome.capitalize(),
                       font=("Segoe UI", 13), bg=BG2, fg=FG, anchor="w")
        lbl.pack(side="left")

        self._sidebar_items[nome] = {
            "outer": outer, "inner": inner,
            "indicator": indicator,
            "bg_col": bg_col, "fg_col": fg_col
        }

        all_widgets = [outer, indicator, inner, av, lbl]

        def make_handlers(n, bg, fg):
            def on_enter(e):
                if self._selected_char != n:
                    for w in all_widgets:
                        try: w.config(bg=BTN_BG)
                        except: pass
            def on_leave(e):
                if self._selected_char != n:
                    for w in all_widgets:
                        try: w.config(bg=BG2)
                        except: pass
            def on_click(e):
                self._seleziona(n, bg, fg)
            return on_enter, on_leave, on_click

        oe, ol, oc = make_handlers(nome, bg_col, fg_col)
        for w in all_widgets:
            w.bind("<Enter>", oe)
            w.bind("<Leave>", ol)
            w.bind("<Button-1>", oc)

    def _seleziona(self, nome, bg_col, fg_col):
        if self._selected_char and self._selected_char in self._sidebar_items:
            prev = self._sidebar_items[self._selected_char]
            for w in [prev["outer"], prev["inner"]] + \
                     list(prev["inner"].winfo_children()):
                try: w.config(bg=BG2)
                except: pass
            prev["indicator"].config(bg=BG2)

        self._selected_char = nome

        if nome in self._sidebar_items:
            item = self._sidebar_items[nome]
            for w in [item["outer"], item["inner"]] + \
                     list(item["inner"].winfo_children()):
                try: w.config(bg=BTN_BG)
                except: pass
            item["indicator"].config(bg=ACCENT)

        self._build_detail(nome, bg_col, fg_col)

    def _build_detail(self, nome, bg_col, fg_col):
        for w in self._detail.winfo_children():
            w.destroy()

        sf        = self.config_data.get("st_folder", "")
        char_data = _read_character_data(sf, nome)

        outer = tk.Frame(self._detail, bg=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=16)

        # --- Sinistra: thumbnail grande ---
        thumb_wrap = tk.Frame(outer, bg=BG2, width=150)
        thumb_wrap.pack(side="left", fill="y", padx=(0, 20))
        thumb_wrap.pack_propagate(False)

        photo = self._load_thumb(nome, sf, 150, 500)
        if photo:
            lbl_img        = tk.Label(thumb_wrap, image=photo, bg=BG2, bd=0)
            lbl_img._photo = photo
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        else:
            av = self._make_avatar(thumb_wrap, nome, bg_col, fg_col, 150, 500)
            av.place(relx=0.5, rely=0.5, anchor="center")

        # --- Destra ---
        right = tk.Frame(outer, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        # Nome + data creazione
        name_row = tk.Frame(right, bg=BG)
        name_row.pack(fill="x", pady=(0, 12))
        tk.Label(name_row, text=nome.capitalize(),
                 font=("Segoe UI", 22, "bold"), bg=BG, fg=FG
                 ).pack(side="left")
        create_date = char_data.get("create_date", "")
        if create_date:
            tk.Label(name_row, text=f"Creato il {create_date}",
                     font=("Segoe UI", 12, "italic"), bg=BG, fg=GRAY
                     ).pack(side="left", padx=(14, 0))

        # Bottone Inietta
        self._btn_azione_dashboard(
            right, "\U0001f4cb  Inietta Author's Note",
            lambda: Screen4(self.app, sf, nome_iniziale=nome),
            accent=True
        )
        self._btn_azione_dashboard(
            right, "\u270f\ufe0f  Modifica personaggio",
            lambda: self._modifica(nome),
            accent=False
        )

        tk.Frame(right, bg=BTN_BG, height=1).pack(fill="x", pady=(10, 12))

        # Due colonne testo — grid garantisce larghezza uguale
        cols = tk.Frame(right, bg=BG)
        cols.pack(fill="both", expand=True)
        cols.columnconfigure(0, weight=1)
        cols.columnconfigure(1, weight=1)
        cols.rowconfigure(1, weight=1)

        # Descrizione
        tk.Label(cols, text="DESCRIZIONE",
                 font=("Segoe UI", 10, "bold"), bg=BG, fg=GRAY
                 ).grid(row=0, column=0, sticky="w", pady=(0, 4), padx=(0, 8))
        txt_desc = tk.Text(cols, font=("Segoe UI", 13),
                           bg=BG2, fg=FG, insertbackground=FG,
                           relief="flat", bd=4, wrap="word",
                           width=1, height=1,
                           state="normal", cursor="arrow")
        txt_desc.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        txt_desc.insert("1.0", char_data.get("description", "") or "\u2014")
        txt_desc.configure(state="disabled")

        # Primo messaggio
        tk.Label(cols, text="PRIMO MESSAGGIO",
                 font=("Segoe UI", 10, "bold"), bg=BG, fg=GRAY
                 ).grid(row=0, column=1, sticky="w", pady=(0, 4))
        txt_first = tk.Text(cols, font=("Segoe UI", 13),
                            bg=BG2, fg="#a6adc8", insertbackground=FG,
                            relief="flat", bd=4, wrap="word",
                            width=1, height=1,
                            state="normal", cursor="arrow")
        txt_first.grid(row=1, column=1, sticky="nsew")
        txt_first.insert("1.0", char_data.get("first_mes", "") or "\u2014")
        txt_first.configure(state="disabled")

    def _mostra_placeholder(self):
        for w in self._detail.winfo_children():
            w.destroy()
        tk.Label(self._detail,
                 text="Crea il tuo primo personaggio",
                 font=("Segoe UI", 13), bg=BG, fg=GRAY).pack(expand=True)
        btn_avanti(self._detail, "\uff0b  Nuovo personaggio",
                   self._nuovo_da_dashboard, pady=(8, 0))

    def _load_thumb(self, nome, sf, max_w, max_h):
        key = (nome, max_w, max_h)
        if key in self._thumb_cache:
            return self._thumb_cache[key]
        user_folder = get_st_user_folder(sf)
        if not user_folder:
            return None
        path = os.path.join(user_folder, "characters", f"{nome}.png")
        if not os.path.isfile(path):
            return None
        try:
            photo = tk.PhotoImage(file=path)
            pw, ph = photo.width(), photo.height()
            if pw < 10 or ph < 10:
                return None
            sx = max(1, pw // max_w)
            sy = max(1, ph // max_h)
            s  = max(sx, sy)
            if s > 1:
                photo = photo.subsample(s, s)
            self._thumb_cache[key] = photo
            return photo
        except Exception:
            return None

    def _make_avatar(self, parent, nome, bg_col, fg_col, w, h):
        c = tk.Canvas(parent, width=w, height=h, bg=bg_col,
                      highlightthickness=0, bd=0)
        fs = max(10, h // 4)
        c.create_text(w // 2, h // 2,
                      text=(nome[0].upper() if nome else "?"),
                      font=("Segoe UI", fs, "bold"), fill=fg_col)
        return c

    def _btn_azione_dashboard(self, parent, testo, cmd, accent=False):
        bg    = ACCENT    if accent else BTN_BG
        fg    = BG        if accent else FG
        hover = "#b4befe" if accent else BTN_HO
        b = tk.Button(parent, text=testo,
                      font=("Segoe UI", 12),
                      bg=bg, fg=fg,
                      activebackground=hover,
                      activeforeground=BG if accent else FG,
                      relief="flat", bd=0,
                      padx=16, pady=8,
                      anchor="w", cursor="hand2",
                      command=cmd)
        b.pack(fill="x", pady=(0, 6))
        return b

    def _nuovo_da_dashboard(self):
        self._chiedi_conferma("Nuovo personaggio", self._nuovo)

    def _aggiorna_dashboard(self, nome_nuovo=None):
        self._selected_char = None
        self._popola_sidebar(nome_nuovo)

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    def _st_folder_ok(self):
        sf = self.config_data.get("st_folder")
        if not sf:
            messagebox.showwarning(APP_TITLE, "Prima configura il percorso di SillyTavern.")
            return None
        return sf

    def _info_personaggio(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE, "Seleziona un personaggio.")
            return
        sf = self._st_folder_ok()
        if not sf:
            return
        ScreenInfo(self.app, sf, self._selected_char)

    def _nuovo_lorebook(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE, "Seleziona un personaggio.")
            return
        sf = self._st_folder_ok()
        if not sf:
            return
        uf = get_st_user_folder(sf)
        if uf:
            path = os.path.join(uf, "worlds", f"{self._selected_char}.json")
            if os.path.isfile(path):
                if not messagebox.askyesno(APP_TITLE,
                        f"Esiste già un lorebook per «{self._selected_char.capitalize()}».\n\n"
                        f"Vuoi aprirlo in modifica?"):
                    return
        ScreenLorebook(self.app, sf, self._selected_char)

    def _modifica_lorebook(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE, "Seleziona un personaggio.")
            return
        sf = self._st_folder_ok()
        if not sf:
            return
        uf = get_st_user_folder(sf)
        if uf:
            path = os.path.join(uf, "worlds", f"{self._selected_char}.json")
            if not os.path.isfile(path):
                if not messagebox.askyesno(APP_TITLE,
                        f"Nessun lorebook trovato per «{self._selected_char.capitalize()}».\n\n"
                        f"Vuoi crearne uno nuovo?"):
                    return
        ScreenLorebook(self.app, sf, self._selected_char)

    def _nuovo_lorebook_dinamico(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE, "Seleziona un personaggio.")
            return
        sf = self._st_folder_ok()
        if not sf:
            return
        uf = get_st_user_folder(sf)
        if uf:
            path = os.path.join(uf, "worlds", f"{self._selected_char}_dinamico.json")
            if os.path.isfile(path):
                if not messagebox.askyesno(APP_TITLE,
                        f"Esiste già un lorebook dinamico per «{self._selected_char.capitalize()}».\n\n"
                        f"Vuoi aprirlo in modifica?"):
                    return
        ScreenLorebookDinamico(self.app, sf, self._selected_char)

    def _modifica_lorebook_dinamico(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE, "Seleziona un personaggio.")
            return
        sf = self._st_folder_ok()
        if not sf:
            return
        uf = get_st_user_folder(sf)
        if uf:
            path = os.path.join(uf, "worlds", f"{self._selected_char}_dinamico.json")
            if not os.path.isfile(path):
                if not messagebox.askyesno(APP_TITLE,
                        f"Nessun lorebook dinamico trovato per «{self._selected_char.capitalize()}».\n\n"
                        f"Vuoi crearne uno nuovo?"):
                    return
        ScreenLorebookDinamico(self.app, sf, self._selected_char)

    def _resetta_percorso(self):
        cfg = load_config()
        cfg["st_folder"] = ""
        save_config(cfg)
        self.config_data["st_folder"] = ""
        self.app._mostra_screen0()

    def _resetta_personaggio(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE,
                "Seleziona prima un personaggio dalla lista.")
            return
        nome = self._selected_char
        self._chiedi_conferma(
            f"Resetta personaggio «{nome.capitalize()}»",
            lambda: self.__do_resetta_personaggio(nome),
            messaggio=f"Stai per eliminare «{nome.upper()}» e tutti i suoi file.")

    def __do_resetta_personaggio(self, nome):
        sf          = self.config_data["st_folder"]
        user_folder = get_st_user_folder(sf)
        eliminati   = []
        if user_folder:
            for path in [
                os.path.join(user_folder, "characters",           f"{nome}.png"),
                os.path.join(user_folder, "QuickReplies",         f"{nome}.json"),
                os.path.join(user_folder, "st_character_manager", f"{nome.lower()}_authornote.txt"),
            ]:
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        eliminati.append(os.path.basename(path))
                    except Exception:
                        pass
        if eliminati:
            messagebox.showinfo(APP_TITLE,
                f"\u2713 Personaggio «{nome.capitalize()}» rimosso.\n\n"
                f"File eliminati:\n" + "\n".join(f"  \u00b7 {e}" for e in eliminati))
        else:
            messagebox.showinfo(APP_TITLE,
                f"Nessun file trovato per «{nome.capitalize()}».")
        self._aggiorna_dashboard()

    def _resetta_lorebook(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE,
                "Seleziona prima un personaggio dalla lista.")
            return
        nome = self._selected_char
        self._chiedi_conferma(
            f"Resetta Lorebook di «{nome.capitalize()}»",
            lambda: self.__do_resetta_lorebook(nome),
            messaggio=f"Stai per eliminare il Lorebook di «{nome.upper()}».")

    def __do_resetta_lorebook(self, nome):
        sf          = self.config_data["st_folder"]
        user_folder = get_st_user_folder(sf)
        if not user_folder:
            return
        path = os.path.join(user_folder, "worlds", f"{nome}.json")
        if os.path.isfile(path):
            try:
                os.remove(path)
                messagebox.showinfo(APP_TITLE,
                    f"\u2713 Lorebook di «{nome.capitalize()}» eliminato.")
            except Exception as ex:
                messagebox.showerror(APP_TITLE, f"Errore:\n{ex}")
        else:
            messagebox.showinfo(APP_TITLE,
                f"Nessun lorebook trovato per «{nome.capitalize()}».")

    def _resetta_lorebook_dinamico(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE,
                "Seleziona prima un personaggio dalla lista.")
            return
        nome = self._selected_char
        self._chiedi_conferma(
            f"Resetta Lorebook dinamico di «{nome.capitalize()}»",
            lambda: self.__do_resetta_lorebook_dinamico(nome),
            messaggio=f"Stai per eliminare il Lorebook dinamico di «{nome.upper()}».")

    def __do_resetta_lorebook_dinamico(self, nome):
        sf          = self.config_data["st_folder"]
        user_folder = get_st_user_folder(sf)
        if not user_folder:
            return
        path = os.path.join(user_folder, "worlds", f"{nome}_dinamico.json")
        if os.path.isfile(path):
            try:
                os.remove(path)
                messagebox.showinfo(APP_TITLE,
                    f"\u2713 Lorebook dinamico di «{nome.capitalize()}» eliminato.")
            except Exception as ex:
                messagebox.showerror(APP_TITLE, f"Errore:\n{ex}")
        else:
            messagebox.showinfo(APP_TITLE,
                f"Nessun lorebook dinamico trovato per «{nome.capitalize()}».")

    # ----------------------------------------------------------
    # Wizard — Nuovo personaggio  /  Modifica personaggio
    # ----------------------------------------------------------

    def _nuovo(self):
        if not self._st_folder_ok():
            return
        WizardRunner(self, {}, WIZARD_STEPS_NUOVO, self._installa)

    def _modifica_da_menu(self):
        if not self._selected_char:
            messagebox.showwarning(APP_TITLE,
                "Seleziona prima un personaggio dalla lista.")
            return
        self._modifica(self._selected_char)

    def _modifica(self, nome):
        if not self._st_folder_ok():
            return
        sf          = self.config_data["st_folder"]
        char_data   = _read_character_data(sf, nome)
        umori       = _read_quickreply_umori(sf, nome)
        variabili   = _read_quickreply_variables(sf, nome)
        genere      = _detect_genere(char_data.get("system_prompt", ""))
        user_folder = get_st_user_folder(sf) or sf
        WizardRunner(self, {
            "nome":                nome,
            "genere":              genere,
            "descrizione":         char_data.get("description",         ""),
            "contesto":            char_data.get("scenario",            ""),
            "primo_messaggio":     char_data.get("first_mes",           ""),
            "personality":         char_data.get("personality",         ""),
            "system_prompt":       char_data.get("system_prompt",       ""),
            "mes_example":         char_data.get("mes_example",         ""),
            "alternate_greetings": char_data.get("alternate_greetings", []),
            "char_note_prompt":    char_data.get("char_note_prompt", ""),
            "char_note_depth":     char_data.get("char_note_depth", 4),
            "image_path":          os.path.join(user_folder, "characters", f"{nome}.png"),
            "_umori_iniziali":     umori,
            "_variabili_iniziali": variabili,
        }, WIZARD_STEPS_MODIFICA, self._installa)

    def _installa(self, character_data):
        sf = self.config_data["st_folder"]
        try:
            risultato = install_character(sf, character_data)
            ScreenComplete(self, character_data["nome"], risultato,
                           lambda: self._aggiorna_dashboard(character_data["nome"]))
        except Exception as ex:
            messagebox.showerror(APP_TITLE, f"Errore durante l'installazione:\n{ex}")


# ============================================================
# APP — finestra unica, cambia contenuto
# ============================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("+10000+10000")   # fuori schermo, evita flash
        self.title(APP_TITLE)
        self.resizable(False, False)
        self.configure(bg=BG)
        self.config_data = load_config()
        self._frame = None
        if not self.config_data.get("st_folder"):
            self._mostra_screen0()
        else:
            self._mostra_menu()

    def _center(self, w, h):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _mostra_screen0(self):
        if self._frame:
            self._frame.destroy()
        self.config(menu=tk.Menu(self))   # rimuove la menubar se presente
        self._center(660, 380)
        self._frame = Screen0Frame(self, self._on_folder_ok)
        self._frame.pack(fill="both", expand=True)

    def _on_folder_ok(self, folder):
        self.config_data["st_folder"] = folder
        self._mostra_menu()

    def _mostra_menu(self):
        if self._frame:
            self._frame.destroy()
        self._frame = MainMenuFrame(self, self.config_data)
        self._frame.pack(fill="both", expand=True)
        self._center(1100, 640)


# ============================================================
# SINGLE-INSTANCE LOCK
# ============================================================

def _acquire_single_instance_lock():
    """Impedisce l'apertura di piu' istanze contemporanee di Anima.

    Crea un file di lock in %TEMP%/anima_st_manager.lock e lo tiene aperto
    in modalita' esclusiva per tutta la durata del processo. Se un'altra
    istanza ha gia' il lock, mostra un messaggio e termina.

    Ritorna l'handle del file da tenere aperto (non chiuderlo).
    """
    import tempfile
    lock_path = os.path.join(tempfile.gettempdir(), "anima_st_manager.lock")
    try:
        # Su Windows usiamo msvcrt.locking; su altre piattaforme fcntl.
        if os.name == "nt":
            import msvcrt
            fh = open(lock_path, "a+b")
            try:
                msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                return fh
            except OSError:
                fh.close()
                return None
        else:
            import fcntl
            fh = open(lock_path, "a+b")
            try:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fh
            except OSError:
                fh.close()
                return None
    except Exception:
        # In caso di errori imprevisti non bloccare l'avvio
        return True


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    _lock_handle = _acquire_single_instance_lock()
    if _lock_handle is None:
        # Un'altra istanza e' gia' aperta
        try:
            _root_warn = tk.Tk()
            _root_warn.withdraw()
            messagebox.showwarning(
                APP_TITLE,
                "ANIMA \xe8 gi\xe0 aperta in un'altra finestra.\n\n"
                "Aprire pi\xf9 istanze contemporaneamente pu\xf2 causare la "
                "perdita di modifiche ai personaggi (le istanze si "
                "sovrascrivono a vicenda).\n\n"
                "Chiudi prima l'altra finestra e riprova."
            )
            _root_warn.destroy()
        except Exception:
            pass
        sys.exit(0)

    app = App()
    app.mainloop()
