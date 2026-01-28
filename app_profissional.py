import json
import os
import http.server
import socketserver
import webbrowser
import threading
import urllib.parse
from datetime import datetime

# ==================== EMOJIS DEFINIDOS COMO CONSTANTES ====================
EMOJIS = {
    'check': '✅',
    'palm_tree': '🌴',
    'house': '🏠',
    'chart': '📊',
    'shirt': '👔',
    'hospital': '🏥',
    'computer': '💻',
    'target': '🎯',
    'robot': '🤖',
    'office': '🏢',
    'thought': '💭',
    'mag_glass': '🔍',
    'satellite': '📡',
    'benefits': '📊',
    'home': '🏠',
    'phone': '📞',
    'statistics': '📈',
    'support': '📞',
    'file': '📄',
    'answer': '📝',
    'exclamation': '❌',
    'thinking': '🤔',
    'warning': '⚠️',
    'stop': '⏹️',
    'wave': '👋',
    'folder': '📁'
}

class PoliticaManager:
    def __init__(self):
        self.politicas = {}
        self.carregar_politicas()
    
    def carregar_politicas(self):
        """Carrega políticas de arquivos JSON"""
        data_dir = "data"
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            self.criar_politicas_exemplo()
        
        for arquivo in os.listdir(data_dir):
            if arquivo.endswith('.json'):
                try:
                    with open(os.path.join(data_dir, arquivo), 'r', encoding='utf-8') as f:
                        empresa_data = json.load(f)
                        self.politicas[empresa_data['empresa']] = empresa_data
                        print(f"{EMOJIS['check']} Carregadas políticas: {empresa_data['empresa']}")
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")
    
    def criar_politicas_exemplo(self):
        """Cria políticas de exemplo"""
        exemplos = {
            "Bernardi Logistics": {
                "empresa": "Bernardi Logistics",
                "contato": "rh@bernardi.com",
                "telefone": "(11) 3333-3333",
                "politicas": {
                    "reembolso_internet": f"{EMOJIS['check']} Até R$ 200/mês para home office (comprovante obrigatório)",
                    "reembolso_cursos": f"{EMOJIS['check']} Até R$ 500/ano para cursos relacionados à função",
                    "ferias": f"{EMOJIS['palm_tree']} 30 dias após 12 meses de trabalho + não acumular mais de 2 períodos",
                    "home_office": f"{EMOJIS['house']} Máximo 3 dias/semana - requer ambiente adequado e internet estável",
                    "beneficios": f"{EMOJIS['chart']} VR: R$ 30/dia, VT: passe livre, Saúde: Unimed, Odonto: Odontoprev",
                    "uniforme": f"{EMOJIS['shirt']} 2 uniformes por ano - solicitar no RH",
                    "plano_saude": f"{EMOJIS['hospital']} Unimed - 30 dias de carência"
                }
            },
            "TechStart BR": {
                "empresa": "TechStart BR", 
                "contato": "rh@techstart.com",
                "telefone": "(11) 4444-4444",
                "politicas": {
                    "reembolso_internet": f"{EMOJIS['check']} R$ 150/mês para todos os funcionários",
                    "reembolso_cursos": f"{EMOJIS['check']} Até R$ 1.000/ano para qualquer curso de tecnologia",
                    "ferias": f"{EMOJIS['palm_tree']} 30 dias + 10 abono pecuniário opcional",
                    "home_office": f"{EMOJIS['house']} 100% remoto opcional - fornecemos notebook e monitor",
                    "beneficios": f"{EMOJIS['chart']} VR: R$ 40/dia, Gympass, Plano Dental, Auxílio creche",
                    "equipamento": f"{EMOJIS['computer']} Notebook + monitor fornecidos",
                    "bonus": f"{EMOJIS['target']} Bônus por performance: até 2 salários/ano"
                }
            }
        }
        
        for empresa, dados in exemplos.items():
            nome_arquivo = f"politicas_{empresa.lower().replace(' ', '_')}.json"
            with open(f"data/{nome_arquivo}", 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print(f"Criado exemplo: {nome_arquivo}")

class RHAssistantPro:
    def __init__(self):
        self.politica_manager = PoliticaManager()
        self.historico = []
    
    def consultar(self, pergunta, empresa):
        """Consulta inteligente nas políticas"""
        pergunta_limpa = pergunta.lower().strip()
        
        # Mapeamento de palavras-chave para políticas
        mapeamento_politicas = {
            'internet': ['reembolso_internet', 'reembolso'],
            'curso': ['reembolso_cursos', 'reembolso'],
            'férias': ['ferias'],
            'ferias': ['ferias'],
            'home office': ['home_office', 'homeoffice'],
            'remoto': ['home_office'],
            'benefício': ['beneficios', 'benefício'],
            'beneficios': ['beneficios'],
            'vr': ['beneficios'],
            'vt': ['beneficios'],
            'uniforme': ['uniforme'],
            'saúde': ['plano_saude', 'beneficios'],
            'plano': ['plano_saude', 'beneficios'],
            'equipamento': ['equipamento'],
            'notebook': ['equipamento'],
            'computador': ['equipamento'],
            'bônus': ['bonus'],
            'performance': ['bonus']
        }
        
        if empresa in self.politica_manager.politicas:
            politicas = self.politica_manager.politicas[empresa]['politicas']
            
            # 1. Busca direta por palavras na pergunta
            palavras_pergunta = set(pergunta_limpa.split())
            
            for palavra in palavras_pergunta:
                if len(palavra) >= 4:
                    for chave_politica, valor_politica in politicas.items():
                        if palavra in chave_politica or palavra in valor_politica.lower():
                            self.registrar_consulta(pergunta, empresa, "AUTO_RESOLVER")
                            return valor_politica, "AUTO_RESOLVER", "BAIXA"
            
            # 2. Busca por mapeamento de sinônimos
            for palavra_chave, politicas_relacionadas in mapeamento_politicas.items():
                if palavra_chave in pergunta_limpa:
                    for politica_alvo in politicas_relacionadas:
                        if politica_alvo in politicas:
                            self.registrar_consulta(pergunta, empresa, "AUTO_RESOLVER")
                            return politicas[politica_alvo], "AUTO_RESOLVER", "BAIXA"
            
            # 3. Busca por termos específicos comuns
            termos_especificos = {
                'quantos dias': 'ferias',
                'quanto tempo': 'ferias', 
                'tirar férias': 'ferias',
                'trabalhar de casa': 'home_office',
                'trabalho remoto': 'home_office',
                'reembolsar': 'reembolso_internet',
                'vale refeição': 'beneficios',
                'vale transporte': 'beneficios',
                'plano médico': 'plano_saude',
                'plano de saúde': 'plano_saude'
            }
            
            for termo, politica_alvo in termos_especificos.items():
                if termo in pergunta_limpa and politica_alvo in politicas:
                    self.registrar_consulta(pergunta, empresa, "AUTO_RESOLVER")
                    return politicas[politica_alvo], "AUTO_RESOLVER", "BAIXA"
        
        # Se não encontrou
        self.registrar_consulta(pergunta, empresa, "PEDIR_INFO")
        return f"{EMOJIS['thinking']} Para ajudar melhor, poderia especificar se é sobre: reembolsos, férias, benefícios, home office ou equipamentos?", "PEDIR_INFO", "MEDIA"
    
    def registrar_consulta(self, pergunta, empresa, acao):
        """Registra consulta no histórico"""
        self.historico.append({
            'timestamp': datetime.now().isoformat(),
            'empresa': empresa,
            'pergunta': pergunta,
            'acao': acao
        })
    
    def get_metricas(self):
        """Retorna métricas do sistema"""
        total = len(self.historico)
        auto_resolver = len([h for h in self.historico if h['acao'] == 'AUTO_RESOLVER'])
        
        return {
            'total_consultas': total,
            'auto_resolver': auto_resolver,
            'taxa_sucesso': f"{(auto_resolver/total*100) if total > 0 else 0:.1f}%",
            'economia_tempo': f"{(total * 0.2):.1f}h",
            'empresas_ativas': len(self.politica_manager.politicas)
        }

class RHRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.assistant = RHAssistantPro()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            empresas = list(self.assistant.politica_manager.politicas.keys())
            metricas = self.assistant.get_metricas()
            
            html = self.generate_html(empresas, metricas)
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data_bytes = self.rfile.read(content_length)
                post_data = post_data_bytes.decode('utf-8')
                
                # DECODIFICAÇÃO CORRETA dos dados do formulário
                params = self._parse_form_data(post_data)
                
                empresa = params.get('empresa', '').strip()
                pergunta = params.get('pergunta', '').strip()
                
                if empresa and pergunta:
                    resposta, acao, urgencia = self.assistant.consultar(pergunta, empresa)
                else:
                    resposta = f"{EMOJIS['exclamation']} Por favor, selecione uma empresa e faça uma pergunta."
                    acao, urgencia = "ERRO", "ALTA"
                
                self._send_html_response(empresa, pergunta, resposta, acao, urgencia)
                
            except Exception as e:
                print(f"Erro no processamento POST: {e}")
                self.send_error(500, "Erro interno do servidor")
    
    def _parse_form_data(self, post_data: str) -> dict:
        """Decodifica corretamente os dados do formulário"""
        params = {}
        
        if not post_data:
            return params
            
        try:
            # Primeiro unquote para decodificar %xx
            post_data_decoded = urllib.parse.unquote(post_data, encoding='utf-8')
            
            # Depois processa os pares chave=valor
            for param in post_data_decoded.split('&'):
                if param and '=' in param:
                    key, value = param.split('=', 1)
                    
                    # Substitui '+' por espaço e remove espaços extras
                    key = key.strip()
                    value = value.strip().replace('+', ' ')
                    
                    params[key] = value
                    
        except Exception as e:
            print(f"Erro ao decodificar dados do formulário: {e}")
        
        return params
    
    def _send_html_response(self, empresa, pergunta, resposta, acao, urgencia):
        """Envia resposta HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        empresas = list(self.assistant.politica_manager.politicas.keys())
        metricas = self.assistant.get_metricas()
        
        html = self.generate_html(empresas, metricas, empresa, pergunta, resposta, acao, urgencia)
        self.wfile.write(html.encode('utf-8'))
    
        def generate_html(self, empresas, metricas, empresa_selecionada="", pergunta="", resposta="", acao="", urgencia=""):
            """Gera HTML da interface - VERSÃO CORRIGIDA"""
            empresas_options = ""
            for empresa in empresas:
                selected = "selected" if empresa == empresa_selecionada else ""
                empresas_options += f'<option value="{empresa}" {selected}>{empresa}</option>'
        
            # Parte da resposta - CORRIGIDA
            resposta_html = ""
            if resposta:
                resposta_html = f'''
                <div class="resposta">
                    <h3>📝 Resposta:</h3>
                    <p>{resposta}</p>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e1e5e9;">
                        <small>
                            <strong>Ação:</strong> <span class="urgencia-{urgencia.lower()}">{acao}</span> | 
                            <strong>Urgência:</strong> <span class="urgencia-{urgencia.lower()}">{urgencia}</span> |
                            <strong>Empresa:</strong> {empresa_selecionada}
                        </small>
                    </div>
                </div>
                '''
            
            # HTML completo
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>🤖 RH Assistant Pro</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 40px;
                        text-align: center;
                    }}
                    .content {{
                        display: flex;
                        gap: 30px;
                        padding: 30px;
                    }}
                    .main-panel {{
                        flex: 2;
                    }}
                    .sidebar {{
                        flex: 1;
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 10px;
                    }}
                    .form-group {{
                        margin-bottom: 20px;
                    }}
                    label {{
                        display: block;
                        margin-bottom: 8px;
                        font-weight: 600;
                        color: #333;
                    }}
                    select, textarea {{
                        width: 100%;
                        padding: 12px;
                        border: 2px solid #e1e5e9;
                        border-radius: 8px;
                        font-size: 16px;
                        transition: border-color 0.3s;
                    }}
                    select:focus, textarea:focus {{
                        outline: none;
                        border-color: #667eea;
                    }}
                    .btn {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 15px 30px;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 16px;
                        font-weight: 600;
                        transition: transform 0.2s;
                    }}
                    .btn:hover {{
                        transform: translateY(-2px);
                    }}
                    .resposta {{
                        background: #f8f9fa;
                        padding: 25px;
                        border-radius: 10px;
                        margin: 25px 0;
                        border-left: 5px solid #667eea;
                    }}
                    .metricas {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 15px;
                        margin: 20px 0;
                    }}
                    .metrica {{
                        background: white;
                        padding: 15px;
                        border-radius: 8px;
                        text-align: center;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    .exemplo-btn {{
                        display: block;
                        width: 100%;
                        background: white;
                        border: 2px solid #e1e5e9;
                        padding: 10px;
                        margin: 5px 0;
                        border-radius: 6px;
                        cursor: pointer;
                        text-align: left;
                        transition: all 0.2s;
                    }}
                    .exemplo-btn:hover {{
                        border-color: #667eea;
                        background: #f0f4ff;
                    }}
                    .urgencia-baixa {{ color: #10b981; }}
                    .urgencia-media {{ color: #f59e0b; }}
                    .urgencia-alta {{ color: #ef4444; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 RH Assistant Pro</h1>
                        <p>Sistema inteligente de consulta de políticas de RH</p>
                    </div>
                    
                    <div class="content">
                        <div class="main-panel">
                            <h2>💬 Consulta de Políticas</h2>
                            
                            <form method="POST" id="consultaForm">
                                <div class="form-group">
                                    <label for="empresa">🏢 Empresa:</label>
                                    <select id="empresa" name="empresa" required>
                                        <option value="">Selecione uma empresa...</option>
                                        {empresas_options}
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label for="pergunta">💭 Sua pergunta:</label>
                                    <textarea id="pergunta" name="pergunta" placeholder="Ex: Como funciona o reembolso de internet? Quais são meus benefícios? Quando posso tirar férias?" required>{pergunta}</textarea>
                                </div>
                                
                                <button type="submit" class="btn">🔍 Consultar Políticas</button>
                            </form>
                            
                            {resposta_html}
                        </div>
                        
                        <div class="sidebar">
                            <h3>🎯 Exemplos Rápidos</h3>
                            <button type="button" class="exemplo-btn" data-pergunta="Como funciona o reembolso de internet?">📡 Reembolso de Internet</button>
                            <button type="button" class="exemplo-btn" data-pergunta="Quantos dias de férias eu tenho?">🌴 Dias de Férias</button>
                            <button type="button" class="exemplo-btn" data-pergunta="Quais são meus benefícios?">📊 Benefícios</button>
                            <button type="button" class="exemplo-btn" data-pergunta="Posso trabalhar home office?">🏠 Home Office</button>
                            <button type="button" class="exemplo-btn" data-pergunta="Preciso de uniforme novo">👔 Uniforme</button>
                            
                            <div style="margin-top: 30px;">
                                <h3>📈 Estatísticas</h3>
                                <div class="metricas">
                                    <div class="metrica">
                                        <div style="font-size: 24px; font-weight: bold; color: #667eea;">{metricas['total_consultas']}</div>
                                        <div>Consultas</div>
                                    </div>
                                    <div class="metrica">
                                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">{metricas['taxa_sucesso']}</div>
                                        <div>Auto Resolução</div>
                                    </div>
                                    <div class="metrica">
                                        <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">{metricas['economia_tempo']}</div>
                                        <div>Tempo Economizado</div>
                                    </div>
                                    <div class="metrica">
                                        <div style="font-size: 24px; font-weight: bold; color: #764ba2;">{metricas['empresas_ativas']}</div>
                                        <div>Empresas</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div style="margin-top: 30px; padding: 15px; background: #e8f4fd; border-radius: 8px;">
                                <h4>📞 Suporte</h4>
                                <p>Dúvidas? Entre em contato com o RH da sua empresa.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    // Configura botões de exemplo
                    document.querySelectorAll('.exemplo-btn').forEach(btn => {{
                        btn.addEventListener('click', function() {{
                            const pergunta = this.getAttribute('data-pergunta');
                            document.getElementById('pergunta').value = pergunta;
                            document.getElementById('empresa').focus();
                            document.querySelector('.main-panel').scrollIntoView({{
                                behavior: 'smooth',
                                block: 'start'
                            }});
                        }});
                    }});
                    
                    // Validação do formulário
                    document.getElementById('consultaForm').addEventListener('submit', function(e) {{
                        const empresa = document.getElementById('empresa').value;
                        const pergunta = document.getElementById('pergunta').value.trim();
                        
                        if (!empresa) {{
                            e.preventDefault();
                            alert('Por favor, selecione uma empresa.');
                            document.getElementById('empresa').focus();
                        }} else if (!pergunta) {{
                            e.preventDefault();
                            alert('Por favor, digite sua pergunta.');
                            document.getElementById('pergunta').focus();
                        }}
                    }});
                </script>
            </body>
            </html>
            '''
            
            return html_content

def main():
    PORT = 8000
    
    # Verificar se a pasta data existe
    if not os.path.exists('data'):
        os.makedirs('data')
        print(f"{EMOJIS.get('folder', '')} Pasta 'data' criada")
    
    with socketserver.TCPServer(("", PORT), RHRequestHandler) as httpd:
        print(f"🚀 RH Assistant Pro iniciado!")
        print(f"🌐 Acesse: http://localhost:{PORT}")
        print(f"{EMOJIS.get('folder', '')} Políticas carregadas automaticamente da pasta 'data/'")
        print(f"{EMOJIS.get('stop', '')} Pressione Ctrl+C para parar")
        
        # Abrir navegador automaticamente
        try:
            threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
        except:
            print(f"{EMOJIS.get('warning', '')} Não foi possível abrir o navegador automaticamente")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n{EMOJIS.get('wave', '')} Servidor encerrado!")

if __name__ == "__main__":
    main()