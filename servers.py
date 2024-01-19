# 1: Bugajski (414889), Adamek (414896), Basiura (414817)
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from typing import Optional
from abc import ABC, abstractmethod
from typing import TypeVar
import re

class Product:

    def __init__(self, name: str, price: float):
        if not self.is_name_correct(name):
            raise ValueError("Nieprawidłowa nazwa produktu")
        self.name = name
        self.price = price

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.name == other.name and self.price == other.price
        return False

    def __hash__(self):
        return hash((self.name, self.price))

    @staticmethod
    def is_name_correct(name: str) -> bool:
        return re.fullmatch('^[a-zA-Z]+\\d+$', name)

class ServerError(Exception):
    pass

class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania
 
class Server(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    n_max_returned_entries: int = 3

    @abstractmethod
    def _get_all_products(self, n_letters: int = 1):
        raise NotImplementedError
    
    def get_entries(self, n_letters: int = 1):
        string = '^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'.format(n_letters=n_letters)
        products = [elem for elem in self._get_all_products(n_letters) if re.match(string, elem.name)]
        if len(products) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(products, key = lambda x: x.price)
ServerType = TypeVar('ServerType', bound=Server)

class ListServer(Server):

    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__products = products
    
    def _get_all_products(self, n_letters: int = 1):
        return self.__products

class MapServer(Server):

    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__products = {elem.name: elem for elem in products}
    
    def _get_all_products(self, n_letters: int = 1):
        return list(self.__products.values())
    
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: ServerType) -> None:
        self.server: ServerType = server
        pass
 
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            if n_letters is  None:
                entries = self.server.get_entries()
            else:
                entries = self.server.get_entries(n_letters)
            if not entries:
                return None
            else:
                return sum([entry.price for entry in entries])
        except TooManyProductsFoundError:
            return None
        try:
            if n_letters is  None:
                entries = self.server.get_entries()
            else:
                entries = self.server.get_entries(n_letters)
            if not entries:
                return None
            else:
                return sum([entry.price for entry in entries])
        except TooManyProductsFoundError:
            return None
    # 1: Bugajski (414889), Adamek (414896), Basiura (414817)
