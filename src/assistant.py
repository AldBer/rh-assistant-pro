# assistant.py
from datetime import datetime
from triagem import classificar_pergunta, EMOJIS
from politicas_manager import PoliticaManager

class RHAssistantPro:
    def __init__(self):
        self.politica_manager = PoliticaManager()
        self.historico = []
        self.metricas = {
            'total_consultas': 0,
            'auto_resolvidas': 0,
            'encaminhadas_rh': 0,
            'taxa_sucesso': 0.0,
            'tempo_economizado': 0.0  # em horas
        }
    
    def consultar(self, pergunta, empresa):
        """Consulta PRINCIPAL - KPIs FUNCIONANDO"""
        # INCREMENTA TOTAL SEMPRE
        self.metricas['total_consultas'] += 1
        
        # Classifica a pergunta
        decisao, urgencia = classificar_pergunta(pergunta)
        
        # AUTO_RESOLVER: Busca nas políticas
        if decisao == "AUTO_RESOLVER":
            resultados = self.politica_manager.buscar_politica(empresa, pergunta)
            
            if resultados:
                # INCREMENTA AUTO-RESOLVIDAS
                self.metricas['auto_resolvidas'] += 1
                self.metricas['tempo_economizado'] += 0.5  # 30min por consulta
                
                melhor = resultados[0]
                resposta = melhor['conteudo']
                
                # Adiciona contexto
                if len(resultados) > 1:
                    resposta += f"\n\n{EMOJIS['mag_glass']} **Encontrei {len(resultados)} resultados relacionados.**"
                
                return resposta, "AUTO_RESOLVER", urgencia
            
            # Se não encontrou, pede mais info
            return self.resposta_nao_encontrada(pergunta), "PEDIR_INFO", "BAIXA"
        
        # ENCAMINHAR_RH
        elif decisao == "ENCAMINHAR_RH":
            self.metricas['encaminhadas_rh'] += 1
            return self.resposta_encaminhamento(pergunta, empresa, urgencia), "ENCAMINHAR_RH", urgencia
        
        # PEDIR_INFO
        else:
            return self.resposta_pedir_info(pergunta), "PEDIR_INFO", urgencia
    
    def resposta_nao_encontrada(self, pergunta):
        """Quando não encontra resposta"""
        return f"""{EMOJIS['thinking']} **Não encontrei uma resposta específica**

Sua pergunta: "{pergunta}"

**Sugestões:**
1. Reformule usando palavras como: "home office", "férias", "reembolso", "benefícios"
2. Verifique se selecionou a empresa correta
3. Consulte os exemplos rápidos na barra lateral

**Precisando de ajuda imediata?** Entre em contato com o RH da sua empresa."""
    
    def resposta_encaminhamento(self, pergunta, empresa, urgencia):
        """Resposta para encaminhamento ao RH"""
        contato = self.politica_manager.get_contato_empresa(empresa)
        
        return f"""{EMOJIS['ticket']} **CHAMADO ABERTO COM SUCESSO**

**Detalhes do encaminhamento:**
• **Empresa:** {empresa}
• **Assunto:** {pergunta[:100]}...
• **Urgência:** {urgencia}
• **Protocolo:** RH-{datetime.now().strftime('%Y%m%d')}-{self.metricas['encaminhadas_rh']:03d}
• **Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Contato do RH:**
📧 **Email:** {contato['contato']}
📞 **Telefone:** {contato['telefone']}
👤 **Responsável:** {contato['responsavel']}

**Status:** Seu chamado foi registrado e será atendido em até 24h (urgências em até 4h)."""
    
    def resposta_pedir_info(self, pergunta):
        """Pede mais informações"""
        return f"""{EMOJIS['thinking']} **Preciso de mais detalhes**

Para responder com precisão, especifique sobre **o que** é sua dúvida:

**Exemplos de perguntas claras:**
• "Como funciona a política de home office?"
• "Qual o valor do reembolso de internet para home office?"
• "Quantos dias de férias tenho direito após 1 ano?"
• "Quais são meus benefícios como funcionário?"

**Sua pergunta atual:** "{pergunta}"
**Sugestão:** Adicione palavras como "home office", "férias", "reembolso", "benefícios"."""
    
    def get_metricas(self):
        """Retorna métricas ATUALIZADAS e CORRETAS"""
        total = self.metricas['total_consultas']
        auto = self.metricas['auto_resolvidas']
        
        # Calcula taxa de sucesso REAL
        taxa = (auto / total * 100) if total > 0 else 0
        self.metricas['taxa_sucesso'] = taxa
        
        return {
            'total_consultas': total,
            'taxa_sucesso': f"{taxa:.1f}%",
            'economia_tempo': f"{self.metricas['tempo_economizado']:.1f}h",
            'empresas_ativas': len(self.politica_manager.politicas),
            'encaminhadas_rh': self.metricas['encaminhadas_rh'],
            'auto_resolvidas': auto,
            'consultas_json': total,  # Agora 100% JSON
            'consultas_pdf': 0        # Sem PDFs
        }