# JDataStore

## `JDataStore(file_path: str | Path, type_struct: dict[Any, Any] | None = None, init_load: bool = True)`

Inizializza un archivio dati basato su file JSON.

### file_path: str | Path
Percorso del file JSON dove i dati verranno salvati o caricati.
Può essere una stringa o un oggetto Path.
    
### type_struct: dict[Any, Any], **\<opzionale\>**
Struttura dati da usare durante il caricamento dei dati dal file.
Se None, i dati vengono caricati tutti secondo la libreria json.

Serve per evitare l'inserimento errato di un tipo di dato in una determinata chiave
Esempio: 
```python 
type_struct = {
    int: {
        "name": str,    
        "language": str,
        "groups": [int]
    }
}
```

L'esempio descrive che il valore di `type_struct[0]["name"]` deve essere `str`, se ad esempio in quel campo venisse inserito un `int` nel file json, con la presenza di una type_struct nel momento del caricamento verrebbe immediatamente scoperto il tipo errato.

È una funzione pensata esclusivamente per dare una struttura fissa all'archivio ed evitare ore di debug.

Da implementare: In più questa funzione permette al serializzazione in json anche di oggetti più complessi"

### init_load: bool, **\<opzionale\>**
Se **True**, tenta di caricare i dati dal file al momento
dell'inizializzazione. Se **False**, si disattiva il caricamento automatico per consentire il caricamento manuale in un secondo momento.

### Note

 - Questo metodo prepara l'oggetto per essere usato come "database".
 - `file_path` indica dove salvare e leggere i dati.
 - `type_struct` è la forma base dei dati.
 - `init_load` decide se partire dai dati del file o da quelli passati.


## `.load(check_before_load: bool = True) -> None:`

Carica il contenuto del file

### check_before_load: bool, **\<opzionale\>**
Se **True**, viene chiamato il metodo `_check_file_path()` che si occupa di controllare la vailidità del percorso. Se **False**, si disattiva il controllo per consentire più margine di manovra


## Note

Questo oggetto possiede quasi tutte le caratteristiche del `dict` per l'estrazione e l'inserimento dei dati