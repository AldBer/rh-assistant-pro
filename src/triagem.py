# triagem.py
from datetime import datetime

# ==================== EMOJIS ====================
EMOJIS = {
    'check': '✅', 'palm_tree': '🌴', 'house': '🏠', 'chart': '📊',
    'shirt': '👔', 'hospital': '🏥', 'computer': '💻', 'target': '🎯',
    'robot': '🤖', 'office': '🏢', 'thought': '💭', 'mag_glass': '🔍',
    'satellite': '📡', 'benefits': '📊', 'home': '🏠', 'phone': '📞',
    'statistics': '📈', 'support': '📞', 'file': '📄', 'answer': '📝',
    'exclamation': '❌', 'thinking': '🤔', 'warning': '⚠️', 'stop': '⏹️',
    'wave': '👋', 'folder': '📁', 'ticket': '🎫', 'money': '💰',
    'clock': '⏰', 'star': '⭐', 'rocket': '🚀', 'crown': '👑'
}

def classificar_pergunta(pergunta):
    """Classificação SIMPLES e EFETIVA"""
    pergunta_lower = pergunta.lower().strip()
    
    # AUTO_RESOLVER: Perguntas claras sobre políticas
    if any(kw in pergunta_lower for kw in [
        'como funciona', 'posso', 'quanto', 'quantos dias',
        'qual é', 'tem direito', 'benefício', 'reembolso',
        'home office', 'férias', 'uniforme', 'plano de saúde',
        'vr ', 'vt ', 'internet', 'curso', 'equipamento',
        'dias de férias', 'vale', 'alimentação', 'transporte',
        'saúde', 'odontológico', 'treinamento', 'horário',
        'salário', 'admissão', 'demissão', 'rescisão'
    ]):
        return "AUTO_RESOLVER", "BAIXA"
    
    # ENCAMINHAR_RH: Pedidos complexos
    if any(kw in pergunta_lower for kw in [
        'aprovação', 'exceção', 'liberação', 'autorização',
        'abrir chamado', 'abrir ticket', 'protocolo',
        'reclamação', 'denúncia', 'conflito', 'problema com',
        'não estou conseguindo', 'urgente', 'emergência'
    ]):
        urgencia = "ALTA" if 'urgente' in pergunta_lower or 'emergência' in pergunta_lower else "MEDIA"
        return "ENCAMINHAR_RH", urgencia
    
    # PEDIR_INFO: Perguntas vagas
    return "PEDIR_INFO", "BAIXA"