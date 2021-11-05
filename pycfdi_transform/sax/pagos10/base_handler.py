from __future__ import annotations
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self, empty_char = '', safe_numerics = False) -> BaseHandler:
        super().__init__()
        self._config = {
            'empty_char': empty_char,
            'safe_numerics': safe_numerics
        }
        self._data = {
            'pago': [],
            'version': empty_char
        }
    
    @abstractmethod
    def transform_from_string(self, xml_str:str) -> dict:
        raise NotImplementedError