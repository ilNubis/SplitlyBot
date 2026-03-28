# Project Docs

## Label `users_data`

Questa "label" users_data ha come key-value l'id dell'utente

Struttura `users_data` in json:

```json
{
    "<user-id | int-value>": {
        "name": <str-value>,
        "language": <str-value>,
        "groups": [<id-group | int-value>]
    }
}
```

Struttura `users_data` in python:

```python
users_data_struct = {
    int: {
        "name": str,
        "language": str,
        "groups": [int]
    }
}
```

Un database che ha come key-value l'id dei gruppi con un dizionario con le informazioni per utente

Struttura per `<id-group>`:

```json
{
    <id-group | int-value>: {
        "name": <str-value>,
        "total-cost": <int-value>,
        "total-users": <int-value>

        "events": [<event-cost>]
    }
}

```

Struttura `<event-cost>`:

```json
{
    "title": <str-value>,
    "date": <int-value>,
    "reason": <str-value>,
    "request-from": <user-id | int-value>,
    "cost": <int-value>
}

```

## Comando \start

### Interazione in privato

Il bot risponde con

```
Benvenuto {USERNAME}\n\n\n Se preferisci un'altra lingua puoi impostarla cliccando il pulsante *Lingua🌍*, altrimenti clicca *Continua*
```

### Quando viene cliccato il pulsante Lingua

```
Seleziona la lingua attraverso i pulsanti qui sotto \\/
```

La generazione dei pulsanti deve essere fatta da codice e ogni bottone deve avere per nome il testo nella lingua con codice "name-lang"

La distribuzione dei pulsanti deve essere verticale

Esempio per estrarre i nomi di tutte le lingue:

```python

from utils import LanguageManager

for lang in LanguageManager.language_data.values():
    print(lang["name-lang"])

```

Esempio:

```python
@dp.message()
async def handle_all_msg(message: types.Message):
    language_pack: JDataStore = lang_manager[message.from_user.language_code] # Selezioni la lingua corrispondente per l'utente
    message.reply(language_pack["start-priv"])

```

### Interazione nel gruppo
