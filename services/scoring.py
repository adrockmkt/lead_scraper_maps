from typing import Dict
from config import (
    SCORE_REGRAS,
    SCORE_MINIMO_APROVACAO,
    BAIRROS_CURITIBA
)

# ======================================================
# SCORING ENGINE
# ======================================================

class LeadScorer:
    def __init__(self):
        pass

    # --------------------------------------------------
    # DETECTA BAIRRO VALORIZADO
    # --------------------------------------------------
    def _is_regiao_valorizada(self, endereco: str) -> bool:
        if not endereco:
            return False

        endereco_lower = endereco.lower()

        for bairro in BAIRROS_CURITIBA:
            if bairro.lower() in endereco_lower:
                return True

        return False

    # --------------------------------------------------
    # CALCULA SCORE TOTAL
    # --------------------------------------------------
    def calcular_score(self, lead: Dict) -> Dict:
        score = 0
        motivos = []

        # 1. Tem site próprio
        if lead.get("site"):
            score += SCORE_REGRAS["tem_site"]
            motivos.append("tem_site")

        # 2. Nicho alto ticket
        if lead.get("nicho"):
            score += SCORE_REGRAS["nicho_alto_ticket"]
            motivos.append("nicho_alto_ticket")

        # 3. Concorrência alta
        concorrencia = lead.get("concorrencia", 0)
        if concorrencia >= 10:
            score += SCORE_REGRAS["concorrencia_alta"]
            motivos.append("concorrencia_alta")

        # 4. Email corporativo válido
        if lead.get("email_corporativo"):
            score += SCORE_REGRAS["email_corporativo"]
            motivos.append("email_corporativo")

        # 5. Região valorizada
        if self._is_regiao_valorizada(lead.get("endereco", "")):
            score += SCORE_REGRAS["regiao_valorizada"]
            motivos.append("regiao_valorizada")

        # normalizar score
        score = min(score, 100)

        # classificação final
        if score >= SCORE_MINIMO_APROVACAO:
            status = "qualificado"
        elif lead.get("site") and not lead.get("email_corporativo"):
            status = "sem_email"
        else:
            status = "descartado"

        lead.update({
            "score_valor": score,
            "score_motivos": ",".join(motivos),
            "status": status
        })

        return lead