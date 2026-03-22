from custom_errors import FileSuffixError, ExpectedFileError
from custom_typing import DictKey, DictValue
from typing_extensions import Any, Iterator
from pathlib import Path
import json 








class JDataStore:
    def __init__(self, file_path: str | Path, data_struct: dict[Any, Any] | None = None, init_load: bool = True) -> None:
        self._data_struct: dict[Any, Any] | None = data_struct
        self.file_path   : Path                  = Path(file_path)
        self._data       : dict[Any, Any]        = {}
        self._loaded     : bool                  = False

        self._check_file_path()

        if init_load:
            self._load(False)
    

    def _check_file_path(self, file_path: str | Path | None = None):
        if file_path is str:
            file_path = Path(file_path)

        if file_path is None:
            file_path = self.file_path

        assert file_path is Path, f"_check_file_path(): Expected 'file_path' to be a Path, but found {type(file_path)}"
        
        if file_path.suffix != "json":
            raise FileSuffixError(f"Expected {self.file_path.parent}\\{self.file_path.stem}.json, but found {self.file_path}")
        

        if not file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True)


        if not file_path.exists():
            with open(self.file_path, "x"):
                pass


        if file_path.is_dir():
            raise ExpectedFileError(f"Expected {self.file_path} to be a file, but found a directory")

        

    def _load(self, check_before_load: bool = True) -> None:
        if check_before_load:
            self._check_file_path()
        
        if self._data_struct is None:
            with open(self.file_path, "r") as f:
                self._data = json.load(f)
            return
        
        assert False, "TODO: _data_struct compatibility"
    
    # ------- Dict Wrappers -------
    def keys(self) -> list[DictKey]:
        return list(self._data.keys())
    
    def values(self) -> list[DictValue]:
        return list(self._data.values())
    
    def items(self) -> list[tuple[DictKey, DictValue]]:
        return list(self._data.items())

    def __getitem__(self, key: DictKey, /) -> DictValue:
        return self._data[key]
    
    def __setitem__(self, key: Any, value: Any, /) -> None:
        self._data[key] = value
    
    def __delitem__(self, key: DictKey, /) -> None:
        self._data.__delitem__(key)

    def __iter__(self) -> Iterator[DictKey]:
        return self._data.__iter__()
    
    