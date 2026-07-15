import json
import os
from typing import Optional
import streamlit as st

class ProvedorDadosFhemig:

    @staticmethod
    @st.cache_data
    def _carregar_dados_globais() -> dict:
        """Carrega o arquivo JSON de tabelas uma única vez e mantém em cache.
        
        Este método é privado (começa com _) porque serve apenas para uso interno 
        da própria classe.
        """
        caminho_atual = os.path.dirname(__file__)
        caminho_json = os.path.join(caminho_atual, "tabelas.json")
        
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def buscar_cargo(cls, classe: str, nivel: str, grau: str, ch_semanal: str) -> Optional[dict]:
        """Retorna o registo de cargo ou None se não for encontrado."""
        dados = cls._carregar_dados_globais()
        for cargo in dados["tabela_cargos"]:
            if (cargo["classe"].upper() == classe.upper() and
                str(cargo["nivel"]) == str(nivel) and
                cargo["grau"].upper() == grau.upper() and
                cargo["ch_semanal"] == ch_semanal):
                return cargo
        return None

    @classmethod
    def obter_tabela_inss(cls, ano: int) -> list:
        """Retorna as faixas de INSS para o ano solicitado."""
        dados = cls._carregar_dados_globais()
        # Busca o ano mais recente se não encontrar tabela p/ o ano especificado
        return dados["tabela_inss"].get(str(ano), dados["tabela_inss"]["2026"])

    @classmethod
    def obter_verbas(cls) -> dict:
        """Retorna o dicionário com os metadados das verbas."""
        dados = cls._carregar_dados_globais()
        return dados["verbas"]
    
    @classmethod
    def obter_valor_grs(cls, nivel: str) -> float:
        """Retorna o valor da GRS conforme o nível de risco."""
        dados = cls._carregar_dados_globais()
        return dados["tabela_grs"][nivel]

    

