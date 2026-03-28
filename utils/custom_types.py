from typing_extensions import Any, Iterator
from .custom_typing import DictKey, DictValue
from types import NoneType

class AdvType:
    def __init__(self) -> None:
        self._supported_value_type: list[Any] = [
            NoneType, int, str, float, dict, list, StaticDict, PatternList
        ]
    
    def _force_type(self, value: Any, new_type: Any) -> Any:
        # Conversione a rischio e pericolo dello sviluppatore:
        #    Nessun errore viene trattato all'interno di questo metodo

        primitive_types: list[type] = [int, float, str]
        if new_type not in self._supported_value_type:
            raise TypeError(f"Unsuported conversion from {type(value)} to {new_type}")

        if isinstance(value, new_type):
            return value

        if new_type in primitive_types:
            return new_type(value) 
        
        if new_type == dict:
            if isinstance(value, *primitive_types):
                return {value: None}
            
            if isinstance(value, StaticDict):
                return value.to_dict()
            
            if isinstance(value, PatternList):
                temp = value.to_list()

                if len(temp)%2 != 0:
                    print("Warning: The None data has been added to make the conversion to dict possible!")
                    temp.append(None)
                
                return {temp[i]: temp[i+1] for i in range(0, len(temp), 2)}
        
        
        if new_type == list:
            if isinstance(value, *primitive_types):
                return [value]
            
            if isinstance(value, StaticDict):
                return list(value.to_dict().items())
            
            if isinstance(value, PatternList):
                return value.to_list()
        

        raise TypeError(f"Could not force conversion from {type(value)} to {new_type}")


class PatternList(AdvType):
    def __init__(self, pattern: list[Any], init_data: list[Any] | None = None, force_cohesion: bool = False) -> None:
        super().__init__()
        self._pattern_struct      : list[Any] = self.init_pattern(pattern)
        self._data                : list[Any] = []
        

        if not init_data is None:
            self.eval_data(init_data, force_cohesion)
    

    def init_pattern(self, pattern: list[Any]) -> list[Any]:
        if len(pattern) == 0:
            raise ValueError("Cannot initialize the object without a pattern")
        
        new_pattern: list[Any] = list()

        for value in pattern:
            if isinstance(value, dict):
                value = StaticDict(value)
            
            elif isinstance(value, list):
                value = PatternList(value)
            
            new_pattern.append(value)
        
        if len(new_pattern) == 1:
            new_pattern.append(new_pattern[0])
        
        return new_pattern
    
    def eval_data(self, data: list[Any], force_cohesion: bool = False) -> PatternList:
        for (index, value) in enumerate(data):
            value_type = self._pattern_struct[(index+len(self._data))%len(self._pattern_struct)]

            if type(value) == type:
                raise TypeError(f"Unsupported raw object-type '{value}' as value")
            
            if isinstance(value, dict):
                if isinstance(value_type, StaticDict):
                    value = value_type.struct_copy().eval_data(value, force_cohesion)
                else: raise TypeError(f"Expected value-type '{value_type}', but found '{dict}'")
            
            if isinstance(value, list):
                if isinstance(value_type, PatternList):
                    value = value_type.pattern_copy().eval_data(value, force_cohesion)
                else: raise TypeError(f"Expected value-type '{value_type}', but found '{list}'")


            if force_cohesion and not isinstance(value, (StaticDict, PatternList, dict, list)):
                value = self._force_type(value, value_type)
                data[index] = value


            if (isinstance(value_type, StaticDict) and isinstance(value, StaticDict)) or \
               (isinstance(value_type, PatternList) and isinstance(value, PatternList)):
                if not value.struct_eq(value_type):
                    raise ValueError(f"Expected {value_type.struct_repr()}, but found {value.struct_repr()}")
                continue


            if not isinstance(value, value_type):
                raise ValueError(f"Expected {value_type} type, but found {type(value)}")
        
        self._data.extend(data)
        return self
    
    def pattern_copy(self) -> PatternList:
        return PatternList(self._pattern_struct)
    
    def append(self, item: Any) -> None:
        # Non è proprio il modo ottimale di implementare questo metodo però siamo accorto di tempo
        self.eval_data([item])

    def extend(self, items: list[Any]) -> None:
        self.eval_data(items)
    
    def to_list(self) -> list[Any]:
        buffer: list[Any] = []
        for value in self._data:
            if isinstance(value, StaticDict):
                value = value.to_dict()
            
            if isinstance(value, PatternList):
                value = value.to_list()

            buffer.append(value)
        
        return buffer

    def struct_eq(self, object: PatternList):
        return object._pattern_struct == self._pattern_struct

    def struct_repr(self) -> str:
        return self._pattern_struct.__repr__()
    
    def __delitem__(self, key: DictKey, /) -> None:
        self._data.__delitem__(key)
    
    def __contains__(self, item: Any) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[DictKey]:
        return self._data.__iter__()
    
    def __eq__(self, value: object) -> bool:
        return self._data.__eq__(value)

    def __repr__(self) -> str:
        return f"<PatternList {self._data.__repr__()}>"
    
    def __str__(self) -> str:
        return self._data.__str__()



class StaticDict(AdvType):
    def __init__(self, type_struct: dict[Any, Any], init_data: dict[Any, Any] | None = None, force_cohesion: bool = False):
        super().__init__()
        
        self._data                : dict[Any, Any] = {}
        self._type_struct         : dict[Any, Any] = self.init_struct(type_struct)
        
        
        if not init_data is None:
            self.eval_data(init_data, force_cohesion)
    
    
    def is_supported_type(self, value: Any) -> bool:
        type_value = type(value)
        if type_value == type:
            return value in self._supported_value_type
        return type_value in self._supported_value_type


    def init_struct(self, type_struct: dict[Any, Any]) -> dict[Any, Any]:
        new_struct: dict[Any, Any] = {}

        for key, value in type_struct.items():
            if isinstance(value, dict):
                value = StaticDict(value)
            
            if isinstance(value, list):
                value = PatternList(value)

            if not self.is_supported_type(key):
                raise TypeError(f"Unsupported '{key}' type of key")
            
            if not self.is_supported_type(value):
                raise TypeError(f"Unsupported '{value}' type of value")

            new_struct[key] = value

        return new_struct
    

    def eval_data(self, data: dict[Any, Any], force_cohesion: bool = False) -> StaticDict:
        key_type_list: list[Any] = list(self._type_struct.keys())

        for index, (key, value) in enumerate(list(data.items())):
            if not (key_type := type(key)) in self._supported_value_type:
                raise TypeError(f"Unsupported key-type '{key_type}'")
            
            if force_cohesion and index < len(key_type_list):
                if type(key_type_list[index]) == type:
                    key = self._force_type(key, key_type_list[index])
                    key_type = type(key)

            if key_type not in key_type_list and key not in key_type_list:
                raise TypeError(f"Expected one of those key-types '{key_type_list}', but found '{key_type}'")       

            if key_type not in key_type_list:
                key_type = key
            

            if isinstance(value, dict):
                if isinstance(self._type_struct[key_type], StaticDict):
                    value = self._type_struct[key_type].struct_copy().eval_data(value, force_cohesion)
                else: raise TypeError(f"Expected value-type '{self._type_struct[key_type]}', but found '{dict}'")
            
            if isinstance(value, list):
                if isinstance(self._type_struct[key_type], PatternList):
                    value = self._type_struct[key_type].pattern_copy().eval_data(value, force_cohesion)
                else: raise TypeError(f"Expected value-type '{self._type_struct[key_type]}', but found '{list}'")

            if force_cohesion and not isinstance(value, (StaticDict, PatternList, dict, list)):
                value = self._force_type(value, self._type_struct[key_type])
            
            self[key] = value
        
        return self
    

    def struct_copy(self) -> StaticDict:
        return StaticDict(self._type_struct)
    
    def struct_eq(self, value: StaticDict) -> bool:
        return value._type_struct == self._type_struct
    
    def data_eq(self, value: StaticDict) -> bool:
        return value._data == self._data
    
    def to_dict(self, json_rule: bool = False) -> dict[Any, Any]:
        buffer: dict[Any, Any] = {}
        for key, value in self._data.items():
            if isinstance(value, StaticDict):
                value = value.to_dict(json_rule)
            
            if isinstance(value, PatternList):
                value = value.to_list()

            if json_rule:
                key = self._force_type(key, str)
            
            buffer[key] = value
        
        return buffer

    def keys(self) -> list[DictKey]:
        return list(self._data.keys())
    
    def values(self) -> list[DictValue]:
        return list(self._data.values())
    
    def items(self) -> list[tuple[DictKey, DictValue]]:
        return list(self._data.items())

    def __getitem__(self, key: DictKey) -> DictValue:
        key_type = type(key)
        key_type_list = list(self._type_struct.keys())

        if key_type == type:
            raise TypeError(f"Unsupported '{type}' as key")

        if key_type not in key_type_list and key not in key_type_list:
            raise TypeError(f"Expected one of those key-types '{key_type_list}', but found '{key}'")
        
        if key_type not in key_type_list:
            key_type = key

        if key not in self and isinstance(self._type_struct[key_type], StaticDict):
            self[key] = self._type_struct[key_type].struct_copy()
        
        if key not in self._data and key_type in self._type_struct:
            self._data[key] = None

        return self._data[key]
    
    def __setitem__(self, key: Any, value: Any) -> None:
        value_type = type(value) # type: ignore     
        key_type = type(key)     # type: ignore 

        key_type_list = list(self._type_struct.keys())

        if key_type == type:
            raise TypeError(f"Unsupported '{type}' as key")

        if value_type not in self._supported_value_type:
            raise TypeError(f"Unsupported value-type '{value_type}'")
        
        if key_type not in key_type_list and key not in key_type_list:
            raise TypeError(f"Expected one of those key-types '{key_type_list}', but found '{key}'")

        if key_type not in key_type_list:
            key_type = key
        
        if isinstance(value, dict):
            if isinstance(self._type_struct[key_type], StaticDict):
                value = self._type_struct[key_type].struct_copy().eval_data(value)
                value_type = StaticDict
            else: raise TypeError(f"Expected value-type '{self._type_struct[key_type]}', but found '{value}'")
            
        if isinstance(value, list):
            if isinstance(self._type_struct[key_type], PatternList):
                value = self._type_struct[key_type].pattern_copy().eval_data(value)
                value_type = PatternList
            else: raise TypeError(f"Expected value-type '{self._type_struct[key_type]}', but found '{value}'")
        
        if not (value_type == self._type_struct[key_type] or value_type in [NoneType, StaticDict, PatternList]):
            raise TypeError(f"Expected value-type '{self._type_struct[key_type]}', but found '{value_type}'")
        
        
        
        self._data[key] = value
        
    def __delitem__(self, key: DictKey, /) -> None:
        self._data.__delitem__(key)
    
    def __contains__(self, item: Any) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[DictKey]:
        return self._data.__iter__()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, StaticDict):
            return self.struct_eq(value) and self.data_eq(value)
        
        if isinstance(value, dict):
            return value == self._data
        return False
    
    def struct_repr(self) -> str:
        return f"<StaticDict {self._type_struct.__repr__()}>"

    def __repr__(self) -> str:
        return f"<StaticDict {self._data.__repr__()}>"
    
    def __str__(self) -> str:
        return self._data.__str__()