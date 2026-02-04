# politicas_manager.py
import json
import os
from triagem import EMOJIS

class PoliticaManager:
    def __init__(self):
        self.politicas = {}
        self.empresas_data = {}
        self.carregar_politicas()
    
    def carregar_politicas(self):
        """Carrega APENAS JSONs - SIMPLES e CONFIAVEL"""
        data_dir = "data"
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            self.criar_politicas_exemplo()
        
        for arquivo in os.listdir(data_dir):
            if arquivo.endswith('.json'):
                try:
                    caminho = os.path.join(data_dir, arquivo)
                    with open(caminho, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    empresa_nome = dados['empresa']
                    self.empresas_data[empresa_nome] = dados
                    
                    # Formato UNIFICADO e SIMPLES
                    if isinstance(dados.get('politicas'), dict):
                        politicas_formatadas = []
                        for chave, valor in dados['politicas'].items():
                            politicas_formatadas.append({
                                'titulo': chave.replace('_', ' ').title(),
                                'conteudo': valor,
                                'tags': chave.split('_') + [empresa_nome.lower()]
                            })
                        self.politicas[empresa_nome] = politicas_formatadas
                    else:
                        self.politicas[empresa_nome] = dados.get('politicas', [])
                    
                    print(f"{EMOJIS['check']} {empresa_nome}: {len(self.politicas[empresa_nome])} políticas")
                    
                except Exception as e:
                    print(f"{EMOJIS['exclamation']} Erro em {arquivo}: {e}")
    
    def buscar_politica(self, empresa, consulta):
        """Busca INTELIGENTE e PRECISA"""
        if empresa not in self.politicas:
            return []
        
        consulta_lower = consulta.lower()
        palavras = [p for p in consulta_lower.split() if len(p) > 3]
        
        resultados = []
        
        for politica in self.politicas[empresa]:
            score = 0
            titulo_lower = politica['titulo'].lower()
            conteudo_lower = politica['conteudo'].lower()
            
            # Busca EXATA no título (maior peso)
            if consulta_lower in titulo_lower:
                score += 20
            
            # Busca por palavras no título
            for palavra in palavras:
                if palavra in titulo_lower:
                    score += 10
            
            # Busca no conteúdo
            if consulta_lower in conteudo_lower:
                score += 8
            
            for palavra in palavras:
                if palavra in conteudo_lower:
                    score += 5
            
            # Busca em tags
            for tag in politica.get('tags', []):
                if tag.lower() in consulta_lower:
                    score += 7
            
            if score > 0:
                resultados.append({
                    'score': score,
                    'titulo': politica['titulo'],
                    'conteudo': politica['conteudo'],
                    'empresa': empresa
                })
        
        # Ordena por relevância
        resultados.sort(key=lambda x: x['score'], reverse=True)
        return resultados
    
    def get_contato_empresa(self, empresa_nome):
        """Retorna contatos do RH"""
        if empresa_nome in self.empresas_data:
            dados = self.empresas_data[empresa_nome]
            return {
                'contato': dados.get('contato', 'rh@empresa.com'),
                'telefone': dados.get('telefone', '(11) 3339-5000'),
                'responsavel': dados.get('responsavel', 'Departamento de RH')
            }
        return {
            'contato': 'rh@empresa.com',
            'telefone': '(11) 3339-5000',
            'responsavel': 'RH Central'
        }
    
    def criar_politicas_exemplo(self):
        """Exemplo PROFISSIONAL para demonstração"""
        exemplo = {
            "empresa": "Bernardi Logistics",
            "contato": "rh@bernardilogistics.com.br",
            "telefone": "(11) 3339-5000",
            "responsavel": "Carla Silva - Gerente de RH",
            "politicas": {
                "home_office": f"""{EMOJIS['house']} **POLÍTICA DE HOME OFFICE**
• **Frequência:** Máximo de 3 dias por semana
• **Requisitos:** Ambiente adequado e internet estável
• **Aprovação:** Necessária do gestor imediato
• **Equipamento:** Fornecido pela empresa
• **Reembolso internet:** R$ 200/mês (com comprovante)""",
                
                "ferias": f"""{EMOJIS['palm_tree']} **POLÍTICA DE FÉRIAS**
• **Período aquisitivo:** 12 meses de trabalho
• **Dias de direito:** 30 dias corridos
• **Aviso prévio:** 30 dias de antecedência
• **Não acumulação:** Máximo 2 períodos
• **Abono pecuniário:** 1/3 do salário (opcional)""",
                
                "reembolso_internet": f"""{EMOJIS['money']} **REEMBOLSO DE INTERNET**
• **Valor:** Até R$ 200,00 mensais
• **Comprovação:** Nota fiscal obrigatória
• **Prazo:** Solicitar até 5º dia útil
• **Forma:** Crédito na folha seguinte
• **Vigência:** Enquanto em regime home office""",
                
                "beneficios": f"""{EMOJIS['chart']} **PACOTE DE BENEFÍCIOS**
• **VR (Vale Refeição):** R$ 30,00 por dia útil
• **VT (Vale Transporte):** Passe livre ou estacionamento
• **Plano de Saúde:** Unimed (cobertura nacional)
• **Odontológico:** Odontoprev
• **Gympass:** Acesso a academias parceiras
• **Seguro de Vida:** 24x o último salário""",
                
                "uniforme": f"""{EMOJIS['shirt']} **UNIFORME CORPORATIVO**
• **Quantidade:** 2 conjuntos por ano
• **Solicitação:** RH (com 30 dias de antecedência)
• **Troca:** Por desgaste normal (com avaliação)
• **Uso obrigatório:** Áreas operacionais
• **Lavagem:** Por conta do funcionário"""
            }
        }
        
        os.makedirs("data", exist_ok=True)
        with open("data/politicas_bernardi_logistics.json", 'w', encoding='utf-8') as f:
            json.dump(exemplo, f, indent=2, ensure_ascii=False)
        
        print(f"{EMOJIS['file']} Exemplo criado: politicas_bernardi_logistics.json")