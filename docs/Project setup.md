# Project Setup

## Premessa

Attenzione, prima di proseguire avrete bisogno di installare la versione 3.14 di python

Vi consiglio di scaricarlo dal [sito ufficiale](https://www.python.org/downloads/)

Se avete altre versioni di python, per non complicarvi la vita con disistallazioni o setup ulteriori, vi consiglio di creare un file e chiamarlo "py.bat".

Copiate e incollate questo codice dentro quel file

```Batch

@echo off


set "EXE_PATH=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
set "BASE=%~dp0"
set "NOMEFILE=python.exe"


for /d %%D in ("%BASE%*") do (
    if exist "%%D\Scripts\%NOMEFILE%" (
        set "EXE_PATH=%%D\Scripts\%NOMEFILE%"
    )
)

echo EXE_PATH: %EXE_PATH%
"%EXE_PATH%" %*

@echo on

```

## Primo passo (Ottenere il token del bot di sviluppo)

### Il primo passo può essere saltato se avete già un TOKEN

Andate su telegram e create un bot con [@BotFather](t.me/BotFather).
Una volta creato il bot vi sarà dato un TOKEN(NON DOVETE DARLO A NESSUNO ALTRIMENTI SIETE FREGATI)

## Secondo passo (Creare .env)

- Copiate `.template-env`
- Sostiuite `{YOUR_TOKEN}` con il token del bot
- Rimonominate il nome della copia di `.template-env` in `.env`

## Terzo passo (Creare e sistemare la venv)

Create un virtual environment con python con il comando

```shell
py -m venv venv
```

### Per avviare il virtual environment

Se siete da cmd:

```shell
.\venv\Scripts\activate.bat
```

Se siete da PowerShell:

```shell
.\venv\Scripts\activate.ps1
```

## Quarto passo (Integrazione di requirements.txt)

_**Prima di procedere per questo passo controllate di aver attivato il virtual environment.**_

### Integrare requirements.txt

Questo comando avvierà l'installazione di tutte le librerie necessarie per lo sviluppo

```shell
pip install -r requirements.txt
```

### Estrarre requirements.txt

Questo comando estrarrà tutte le librerie scaricate per dare la possibilità ad altri sviluppatori di lavorare sul progetto

#### Indicazioni d'uso

**Il comando che vi sto per indicare va usato solo e soltato dopo l'installazione e l'ufficializzazione di una libreria all'interno del progetto**

```shell
pip freeze > requirements.txt 
```
