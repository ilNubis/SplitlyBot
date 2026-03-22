from custom_errors import MissingDirectoryError
from custom_typing import DictKey, DictValue
from typing_extensions import Any, Iterator
from utils import JDataStore
from pathlib import Path




class LanguageManager:
    def __init__(self, base_path: str | Path, supported_lang: list[str] | None = None) -> None:
        self.base_path         : Path                  = Path(base_path)
        supported_language     : list[Path]            = []
        self.language_data     : dict[str, JDataStore] = {}

        if not self.base_path.exists():
            raise MissingDirectoryError(f"base_path['{self.base_path}'] does not exist")

        if supported_lang is None:
            supported_language = [file for file in base_path.iterdir() if self.is_allowed_file(file)]
        else:
            for file in supported_lang:
                file = Path(file)

                if self._is_allowed_file(file):
                    supported_language.append(file)
        
        for lang in supported_language:
            self.language_data[lang.stem] = JDataStore(lang)
        


    def _is_allowed_file(self, file: Path):
        return file.exists() and file.is_file() and file.suffix == ".join"
    
    # ------- Dict Wrappers -------
    def keys(self, lang: str) -> list[DictKey]:
        return list(self.language_data[lang].keys())
    
    def values(self, lang: str) -> list[DictValue]:
        return list(self.language_data[lang].values())
    
    def items(self, lang: str) -> list[tuple[DictKey, DictValue]]:
        return list(self.language_data[lang].items())

    def __getitem__(self, lang: str, key: DictKey, /) -> DictValue:
        return self.language_data[lang][key]
    
    # def __setitem__(self, lang: str, key: Any, value: Any, /) -> None:
    #     self.language_data[lang][key] = value
    
    def get_iter(self, lang: str) -> Iterator[DictKey]:
        return self.language_data[lang].__iter__()