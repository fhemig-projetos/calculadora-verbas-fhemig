class FormatadorCampos:
    
    @staticmethod
    def moeda_com_simbolo(valor: float) -> str:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def moeda_sem_simbolo(valor: float) -> str:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
    @staticmethod
    def masp(masp_cru: str) -> str:
        # Se tiver menos de 2 caracteres, não formata
        if not masp_cru or len(masp_cru) < 2:
            return masp_cru
        
        # Isola o último dígito e adiciona um traço (ex: 1234567-8)
        return f"{masp_cru[:-1]}-{masp_cru[-1]}"