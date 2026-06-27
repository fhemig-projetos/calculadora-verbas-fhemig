from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ResultadoCalculo:
    valor: float
    memoria_calculo: list[str]

class CalculadoraVerba(ABC):
    @property
    @abstractmethod
    def descricao_formula(self) -> str:
        """Texto explicativo da fórmula que aparecerá na tela do Streamlit."""
        pass
    
    @property
    @abstractmethod
    def campos_necessarios(self) -> list[str]:
        pass

    @abstractmethod
    def calcular(self, **kwargs) -> ResultadoCalculo:
        """Recebe os parâmetros dinâmicos e retorna o valor e a memória."""
        pass