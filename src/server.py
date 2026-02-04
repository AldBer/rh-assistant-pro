# server.py - VERSÃO COMPLETA E CORRIGIDA
import http.server
import socketserver
import urllib.parse
import json
import os
from pathlib import Path
from assistant import RHAssistantPro
from triagem import EMOJIS
from config import Config

class RHRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.config = Config()
        self.assistant = RHAssistantPro()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Manipula requisições GET"""
        if not self.config.is_licensed():
            self.send_license_required()
            return
        if self.path == '/':
            self.serve_index()
        elif self.path == '/empresas':
            self.serve_empresas()
        elif self.path.startswith('/static/'):
            super().do_GET()
        else:
            self.send_error(404, "Página não encontrada")
    
    def do_POST(self):
        """Manipula requisições POST"""
        if self.path == '/consultar':
            self.handle_consulta()
        else:
            self.send_error(404, "Endpoint não encontrado")
    
    def serve_index(self):
        """Serve a página inicial"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        empresas = list(self.assistant.politica_manager.politicas.keys())
        metricas = self.assistant.get_metricas()
        
        html = self.generate_html(empresas, metricas)
        self.wfile.write(html.encode('utf-8'))
    
    def serve_empresas(self):
        """Retorna lista de empresas em JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        empresas = list(self.assistant.politica_manager.politicas.keys())
        response = {'empresas': empresas}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_consulta(self):
        """Processa uma consulta"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            post_data = post_data_bytes.decode('utf-8')
            
            # Parse JSON ou form data
            if post_data.startswith('{'):
                params = json.loads(post_data)
            else:
                params = self.parse_form_data(post_data)
            
            empresa = params.get('empresa', '').strip()
            pergunta = params.get('pergunta', '').strip()
            
            if not empresa or not pergunta:
                self.send_json_response({
                    'error': True,
                    'message': 'Por favor, selecione uma empresa e faça uma pergunta.'
                })
                return
            
            # Processa a consulta
            resposta, acao, urgencia = self.assistant.consultar(pergunta, empresa)
            
            # Busca contatos da empresa
            contato_info = self.assistant.politica_manager.get_contato_empresa(empresa)
            
            self.send_json_response({
                'success': True,
                'resposta': resposta,
                'acao': acao,
                'urgencia': urgencia,
                'empresa': empresa,
                'pergunta': pergunta,
                'contato': contato_info,
                'metricas': self.assistant.get_metricas()
            })
            
        except Exception as e:
            print(f"❌ Erro no POST: {e}")
            self.send_json_response({
                'error': True,
                'message': f'Erro interno: {str(e)[:100]}'
            }, status=500)
    
    def parse_form_data(self, post_data: str) -> dict:
        """Decodifica dados do formulário"""
        params = {}
        if not post_data:
            return params
        
        try:
            post_data_decoded = urllib.parse.unquote(post_data, encoding='utf-8')
            for param in post_data_decoded.split('&'):
                if param and '=' in param:
                    key, value = param.split('=', 1)
                    params[key.strip()] = value.strip().replace('+', ' ')
        except Exception as e:
            print(f"❌ Erro ao decodificar: {e}")
        
        return params
    
    def send_json_response(self, data, status=200):
        """Envia resposta JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def generate_html(self, empresas, metricas):
        """Gera HTML da interface - CORRIGIDO para evitar problemas com f-strings"""
        # Gera opções de empresas
        empresas_options = ""
        for empresa in empresas:
            empresas_options += f'<option value="{empresa}">{empresa}</option>'
        
        # Exemplos de perguntas (CORRIGIDO: usando dicionário normal)
        exemplos = [
            {"texto": "🏠 Home Office", "pergunta": "Posso trabalhar home office?"},
            {"texto": "🌴 Dias de Férias", "pergunta": "Quantos dias de férias eu tenho?"},
            {"texto": "📡 Reembolso Internet", "pergunta": "Como funciona o reembolso de internet?"},
            {"texto": "📊 Benefícios", "pergunta": "Quais são meus benefícios?"},
            {"texto": "👔 Uniforme", "pergunta": "Preciso de uniforme novo"}
        ]
        
        # Gera HTML dos exemplos (CORRIGIDO: usando string normal)
        exemplos_html = ""
        for exemplo in exemplos:
            # Escape aspas para JavaScript
            pergunta_esc = exemplo['pergunta'].replace('"', '&quot;').replace("'", "\\'")
            exemplos_html += f'''
            <button type="button" class="exemplo-btn" onclick="usarExemplo(\'{pergunta_esc}\')">
                {exemplo['texto']}
            </button>
            '''
        
        # HTML principal (CORRIGIDO: removendo f-strings problemáticas)
        html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 RH Assistant Pro</title>
    <style>
        /* [MESMOS ESTILOS DA VERSÃO ANTERIOR - mantidos] */
        :root {{
            --primary: #4a6ee0;
            --primary-dark: #3a5ad0;
            --secondary: #764ba2;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --light: #f8f9fa;
            --dark: #333;
            --gray: #666;
            --border: #e1e5e9;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            padding: 30px;
        }}
        
        @media (max-width: 768px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 2rem;
            }}
        }}
        
        .main-panel {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}
        
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
        }}
        
        .card h2, .card h3, .card h4 {{
            color: var(--dark);
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .card h2 {{
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
            font-size: 0.95rem;
        }}
        
        select, textarea, input {{
            width: 100%;
            padding: 14px;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.2s;
            background: white;
        }}
        
        select:focus, textarea:focus, input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 110, 224, 0.1);
        }}
        
        textarea {{
            min-height: 120px;
            resize: vertical;
        }}
        
        .btn {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 16px 32px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.2s;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(74, 110, 224, 0.2);
        }}
        
        .btn:active {{
            transform: translateY(0);
        }}
        
        .exemplos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        
        .exemplo-btn {{
            background: white;
            border: 2px solid var(--border);
            padding: 12px 15px;
            border-radius: 8px;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
            font-size: 14px;
            font-weight: 500;
            color: var(--dark);
        }}
        
        .exemplo-btn:hover {{
            border-color: var(--primary);
            background: var(--light);
            transform: translateY(-1px);
        }}
        
        .resposta-container {{
            display: none;
        }}
        
        .resposta {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-left: 4px solid var(--primary);
        }}
        
        .resposta-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border);
        }}
        
        .resposta-titulo {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--dark);
        }}
        
        .badge {{
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .badge-auto {{ background: #d1fae5; color: #065f46; }}
        .badge-encaminhado {{ background: #fee2e2; color: #991b1b; }}
        .badge-info {{ background: #fef3c7; color: #92400e; }}
        
        .resposta-content {{
            font-size: 1rem;
            line-height: 1.6;
            color: var(--dark);
            white-space: pre-line;
            margin-bottom: 20px;
        }}
        
        .resposta-footer {{
            padding-top: 20px;
            border-top: 1px solid var(--border);
            font-size: 0.9rem;
            color: var(--gray);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .metricas-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        
        .metrica-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-top: 4px solid var(--primary);
        }}
        
        .metrica-valor {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 5px;
        }}
        
        .metrica-label {{
            font-size: 0.9rem;
            color: var(--gray);
            font-weight: 500;
        }}
        
        .tags-grid {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .tag {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .tag-json {{ background: #e0f2fe; color: #075985; }}
        .tag-pdf {{ background: #f0f9ff; color: #0c4a6e; }}
        .tag-rh {{ background: #fef2f2; color: #7f1d1d; }}
        
        .contato-card {{
            background: linear-gradient(135deg, #e8f4fd 0%, #f0f4ff 100%);
            border-left: 4px solid var(--primary);
        }}
        
        .contato-info {{
            margin-top: 15px;
        }}
        
        .contato-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }}
        
        .loading {{
            display: none;
            text-align: center;
            padding: 40px;
        }}
        
        .loading-spinner {{
            border: 3px solid #f3f3f3;
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 RH Assistant Pro</h1>
            <p>Sistema inteligente de consulta de políticas com triagem automática</p>
        </div>
        
        <div class="content">
            <div class="main-panel">
                <div class="card">
                    <h2>💬 Consulta de Políticas</h2>
                    
                    <form id="consultaForm">
                        <div class="form-group">
                            <label for="empresa">🏢 Empresa:</label>
                            <select id="empresa" name="empresa" required>
                                <option value="">Selecione uma empresa...</option>
                                {empresas_options}
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="pergunta">💭 Sua pergunta:</label>
                            <textarea 
                                id="pergunta" 
                                name="pergunta" 
                                rows="4" 
                                placeholder="Ex: Como funciona o reembolso de internet? Posso trabalhar home office? Quantos dias de férias?" 
                                required
                            ></textarea>
                        </div>
                        
                        <button type="submit" class="btn">
                            🔍 Consultar Políticas
                        </button>
                    </form>
                    
                    <div id="loading" class="loading">
                        <div class="loading-spinner"></div>
                        <p>Processando sua consulta...</p>
                    </div>
                    
                    <div id="respostaContainer" class="resposta-container">
                        <!-- Resposta será inserida aqui pelo JavaScript -->
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="card">
                    <h3>🎯 Exemplos Rápidos</h3>
                    <div class="exemplos-grid">
                        {exemplos_html}
                    </div>
                </div>
                
                <div class="card">
                    <h3>📈 Estatísticas do Sistema</h3>
                    <div class="metricas-grid">
                        <div class="metrica-card">
                            <div class="metrica-valor" id="totalConsultas">{metricas['total_consultas']}</div>
                            <div class="metrica-label">Consultas</div>
                        </div>
                        <div class="metrica-card">
                            <div class="metrica-valor" id="taxaSucesso">{metricas['taxa_sucesso']}</div>
                            <div class="metrica-label">Auto Resolução</div>
                        </div>
                        <div class="metrica-card">
                            <div class="metrica-valor" id="economiaTempo">{metricas['economia_tempo']}</div>
                            <div class="metrica-label">Tempo Economizado</div>
                        </div>
                        <div class="metrica-card">
                            <div class="metrica-valor" id="empresasAtivas">{metricas['empresas_ativas']}</div>
                            <div class="metrica-label">Empresas</div>
                        </div>
                    </div>
                    
                    <div class="tags-grid">
                        <span class="tag tag-json" id="consultasJson">📄 {metricas['consultas_json']} JSON</span>
                        <span class="tag tag-pdf" id="consultasPdf">📋 {metricas['consultas_pdf']} PDF</span>
                        <span class="tag tag-rh" id="encaminhadasRh">🎫 {metricas['encaminhadas_rh']} RH</span>
                    </div>
                </div>
                
                <div class="card contato-card">
                    <h4>📞 Suporte</h4>
                    <div id="contatoInfo">
                        <p>Selecione uma empresa para ver informações de contato específicas.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Função para usar exemplo
        function usarExemplo(pergunta) {{
            document.getElementById('pergunta').value = pergunta;
            document.getElementById('pergunta').focus();
        }}
        
        // Atualiza contato quando empresa é selecionada
        document.getElementById('empresa').addEventListener('change', function() {{
            const empresa = this.value;
            const contatoInfo = document.getElementById('contatoInfo');
            
            if (!empresa) {{
                contatoInfo.innerHTML = '<p>Selecione uma empresa para ver informações de contato específicas.</p>';
                return;
            }}
            
            // Email formatado (simples, sem template string problemática)
            const emailEmpresa = 'rh@' + empresa.toLowerCase().replace(/ /g, '_') + '.com';
            
            contatoInfo.innerHTML = `
                <div class="contato-info">
                    <div class="contato-item">
                        📧 <strong>Email:</strong> ${{emailEmpresa}}
                    </div>
                    <div class="contato-item">
                        📞 <strong>Telefone:</strong> (11) 3339-5000
                    </div>
                    <div class="contato-item">
                        👤 <strong>Responsável:</strong> Departamento de RH
                    </div>
                    <div class="contato-item">
                        ⏰ <strong>Horário:</strong> Seg-Sex, 9h às 18h
                    </div>
                </div>
            `;
        }});
        
        // Envio do formulário via AJAX
        document.getElementById('consultaForm').addEventListener('submit', async function(e) {{
            e.preventDefault();
            
            const empresa = document.getElementById('empresa').value;
            const pergunta = document.getElementById('pergunta').value.trim();
            
            if (!empresa) {{
                alert('Por favor, selecione uma empresa.');
                document.getElementById('empresa').focus();
                return;
            }}
            
            if (!pergunta) {{
                alert('Por favor, digite sua pergunta.');
                document.getElementById('pergunta').focus();
                return;
            }}
            
            // Mostra loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('respostaContainer').style.display = 'none';
            
            try {{
                const response = await fetch('/consultar', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        empresa: empresa,
                        pergunta: pergunta
                    }})
                }});
                
                const data = await response.json();
                
                if (data.error) {{
                    throw new Error(data.message);
                }}
                
                // Atualiza métricas
                document.getElementById('totalConsultas').textContent = data.metricas.total_consultas;
                document.getElementById('taxaSucesso').textContent = data.metricas.taxa_sucesso;
                document.getElementById('economiaTempo').textContent = data.metricas.economia_tempo;
                document.getElementById('empresasAtivas').textContent = data.metricas.empresas_ativas;
                document.getElementById('consultasJson').textContent = '📄 ' + data.metricas.consultas_json + ' JSON';
                document.getElementById('consultasPdf').textContent = '📋 ' + data.metricas.consultas_pdf + ' PDF';
                document.getElementById('encaminhadasRh').textContent = '🎫 ' + data.metricas.encaminhadas_rh + ' RH';
                
                // Atualiza informações de contato
                const contatoInfo = document.getElementById('contatoInfo');
                contatoInfo.innerHTML = `
                    <div class="contato-info">
                        <div class="contato-item">
                            📧 <strong>Email:</strong> ${{data.contato.contato}}
                        </div>
                        <div class="contato-item">
                            📞 <strong>Telefone:</strong> ${{data.contato.telefone}}
                        </div>
                        <div class="contato-item">
                            👤 <strong>Responsável:</strong> ${{data.contato.responsavel}}
                        </div>
                        <div class="contato-item">
                            ⏰ <strong>Horário:</strong> Segunda a Sexta, 9h às 18h
                        </div>
                    </div>
                `;
                
                // Mostra resposta
                mostrarResposta(data);
                
            }} catch (error) {{
                alert('Erro: ' + error.message);
            }} finally {{
                document.getElementById('loading').style.display = 'none';
            }}
        }});
        
        function mostrarResposta(data) {{
            const container = document.getElementById('respostaContainer');
            
            // Determina classe do badge baseado na ação
            let badgeClass = 'badge-auto';
            let badgeText = '✅ Auto-resolvido';
            
            if (data.acao === 'ENCAMINHAR_RH') {{
                badgeClass = 'badge-encaminhado';
                badgeText = '🎫 Encaminhado';
            }} else if (data.acao === 'PEDIR_INFO') {{
                badgeClass = 'badge-info';
                badgeText = '🤔 Precisa de mais info';
            }}
            
            container.innerHTML = `
                <div class="resposta">
                    <div class="resposta-header">
                        <div class="resposta-titulo">${{badgeText}}</div>
                        <span class="badge ${{badgeClass}}">${{data.urgencia}}</span>
                    </div>
                    <div class="resposta-content">
                        ${{data.resposta}}
                    </div>
                    <div class="resposta-footer">
                        <div>
                            <strong>Empresa:</strong> ${{data.empresa}} | 
                            <strong>Ação:</strong> ${{data.acao}}
                        </div>
                        <div>
                            <strong>Consulta #${{data.metricas.total_consultas}}</strong>
                        </div>
                    </div>
                </div>
            `;
            
            container.style.display = 'block';
            
            // Scroll para resposta
            container.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
        
        // Foco automático no campo de pergunta
        document.getElementById('empresa').addEventListener('change', function() {{
            if (this.value) {{
                document.getElementById('pergunta').focus();
            }}
        }});
    </script>
</body>
</html>'''
        
        return html_content

def run_server(port=8000):
    """Executa o servidor com configurações aprimoradas"""
    # Cria diretório static se não existir
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Configura o handler
    handler = RHRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Servidor rodando em http://localhost:{port}")
        print(f"📁 Dados: {os.path.abspath('data')}")
        print(f"🖥️  Interface: Moderna e responsiva")
        print(f"⚡ Sistema: Triagem inteligente ativa")
        print(f"💰 Modelo: Pronto para venda (Starter: R$ 297/mês)")
        print(f"\n📢 Pressione Ctrl+C para encerrar")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n👋 Servidor encerrado!")
            
def send_license_required(self):
        """Envia página de licença expirada"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Licença Requerida - RH Assistant Pro</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; }
                .alert { background: #fee2e2; border: 1px solid #ef4444; padding: 30px; border-radius: 10px; }
                .btn { background: #4a6ee0; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="alert">
                    <h1>⛔ Licença Expirada</h1>
                    <p>Seu período de teste de 15 dias terminou.</p>
                    <p>Para continuar usando o RH Assistant Pro, adquira uma licença.</p>
                    
                    <div style="margin: 30px 0;">
                        <h3>Planos Disponíveis:</h3>
                        <p><strong>Starter:</strong> R$ 297/mês - Consultas ilimitadas</p>
                        <p><strong>Growth:</strong> R$ 597/mês + Conversor PDF</p>
                        <p><strong>Enterprise:</strong> R$ 997/mês + API</p>
                    </div>
                    
                    <a href="https://aldber.github.io/rh-assistant-landing/" class="btn" target="_blank">
                        🛒 Comprar Licença
                    </a>
                    
                    <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                        Ou entre em contato: aldo.bernardi@gmail.com
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.send_response(402)  # Payment Required
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))