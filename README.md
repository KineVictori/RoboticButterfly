# Mekanisk Sommerfugl styrt av Håndbevegelser

Dette prosjektet lar deg styre en mekanisk sommerfugl med håndbevegelser foran et kamera, ved hjelp av OpenCV, MediaPipe og en ESP32-basert motorstyring. Systemet tolker håndgester i sanntid og oversetter dem til både roterende og “flaksende” bevegelser på sommerfuglen.

## Funksjonalitet

- **Rotasjon:** Sommerfuglen roterer til høyre eller venstre basert på hvor du peker med hånden.
- **Vingeslag:** Når du lukker hånden (fører fingertuppen mot håndleddet), aktiveres solenoiden og sommerfuglen slår med vingene.
- **Responsiv styring:** Systemet bruker en PID-regulator for å gi jevne og stabile bevegelser, selv om håndsignalet varierer litt.
- **Sanntidsvisning:** Håndsporing og tilbakemelding vises direkte i et OpenCV-vindu.

## Maskinvare

- **ESP32-brett** med ferdiglaget PCB
- **DC-motor med enkoder** (for rotasjon)
- **Solenoid** (for vingeslag)
- **Webkamera**
- **PC** med Python 3.11

## Programvareavhengigheter

**Viktig:**  
> MediaPipe støtter per mai 2025 **ikke** Python 3.13, og det er rapportert problemer med Python 3.12 for enkelte brukere.  
> For å unngå installasjonsfeil og sikre at både MediaPipe og OpenCV fungerer som forventet, bør du bruke **Python 3.11**.

- Python 3.11
- [OpenCV](https://opencv.org/) (`pip install opencv-python`)
- [MediaPipe](https://developers.google.com/mediapipe) (`pip install mediapipe`)
- [pyserial](https://pythonhosted.org/pyserial/) (`pip install pyserial`)
- Numpy (`pip install numpy`)

## Filstruktur

- `hand_tracking.py`: Håndsporing og tolking av håndgester (generator som gir ut kommandoer).
- `main.py`: Hovedprogram som håndterer PID-regulering, setpunkter og kommunikasjon med ESP32.
- `serial_handler.py`: Klasse for seriell kommunikasjon mellom PC og ESP32.

## Bruk

1. **Koble til maskinvare:**  
   Koble ESP32, motor og solenoid i henhold til PCB-oppsett. Koble webkamera til PC (evt. bruk det innebygde om du har det).

2. **Installer avhengigheter:**  
```bash
pip install opencv-python mediapipe pyserial numpy
```


3. **Start programmet:**  
Sørg for at `main.py`, `hand_tracking.py` og `serial_handler.py` ligger i samme mappe.  
Kjør hovedprogrammet:
```bash
python main.py
```
Standard seriellport er satt til `COM3` – endre dette i `main.py` hvis nødvendig.

4. **Bruk:**  
- Beveg hånden foran kameraet.  
- Peker du tydelig mot høyre eller venstre, roterer sommerfuglen den veien.
- Lukker du hånden (fører fingertuppen mot håndleddet), slår sommerfuglen med vingene.
- Håndsporing vises i eget vindu. Trykk `q` for å avslutte.

## Tilpasning

- **Terskelverdier** for gester og PID-parametre kan justeres i koden for å tilpasse responsen til ditt oppsett.
- **Seriellport** kan endres i `main.py` (variabelen `com_port`).

## Feilsøking

- Sjekk at alle avhengigheter er installert.
- Pass på at riktig seriellport er valgt og at ESP32 er tilkoblet.
- Hvis kameraet ikke starter, prøv å endre kameraindeksen i `hand_tracking.py`.
- For best ytelse, sørg for god belysning og enkle bakgrunner.

## Kreditering

Basen for `hand_tracking.py` er inspirert av [trflorian/hand-tracker](https://github.com/trflorian/hand-tracker/blob/main/src/main.py).
