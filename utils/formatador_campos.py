class FormatadorCampos:

    @staticmethod
    def masp(masp_cru: str) -> str:
        if not masp_cru or len(masp_cru) < 2:
            return masp_cru
        digits = masp_cru.replace("-", "").strip()
        return f"{digits[:-1]}-{digits[-1]}"

    @staticmethod
    def arredondar_moeda(valor_cru) -> float:
        """Arredonda para 2 casas decimais se houver um número presente."""
        if valor_cru is None:
            return valor_cru
        return round(valor_cru, 2)
    
    @staticmethod
    def brl(valor: float) -> str:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

