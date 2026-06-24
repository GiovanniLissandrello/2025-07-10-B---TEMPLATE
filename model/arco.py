from dataclasses import dataclass
from model.prodotto import Prodotto

@dataclass
class Arco:
    u : Prodotto
    v : Prodotto
    peso : int
