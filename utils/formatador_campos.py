class FormatadorCampos:

    @staticmethod
    def moeda_com_simbolo(valor: float) -> str:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def moeda_sem_simbolo(valor: float) -> str:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def masp(masp_cru: str) -> str:
        if not masp_cru or len(masp_cru) < 2:
            return masp_cru
        digits = masp_cru.replace("-", "").strip()
        return f"{digits[:-1]}-{digits[-1]}"

    @staticmethod
    def arredondar_moeda(valor_cru) -> float:
        """Converte para float e arredonda para 2 casas decimais."""
        try:
            return round(float(valor_cru), 2)
        except (ValueError, TypeError):
            return 0.0