# config.py
import os
import json
from licensing import LicensingSystem

class Config:
    def __init__(self):
        self.licensing = LicensingSystem()
        self.license_status = self.licensing.check_license()
        
    def is_licensed(self):
        """Verifica se o sistema está licenciado"""
        return self.license_status['valid']
    
    def get_license_info(self):
        """Retorna informações da licença"""
        return self.license_status
    
    def show_license_screen(self):
        """Exibe tela de licenciamento"""
        if self.license_status['type'] == 'trial' and self.license_status['valid']:
            days_left = self.license_status['days_left']
            print(f"\n{'='*60}")
            print(f"🧪 MODO TESTE - {days_left} dias restantes")
            print(f"{'='*60}")
            print(f"Após {days_left} dias, será necessário adquirir uma licença.")
            print(f"Visite: https://aldber.github.io/rh-assistant-landing/ para escolher seu plano.")
            print(f"{'='*60}\n")
            return True
        
        elif not self.license_status['valid']:
            print(f"\n{'='*60}")
            print(f"⛔ LICENÇA EXPIRADA")
            print(f"{'='*60}")
            print(f"Seu período de teste de 15 dias terminou.")
            print(f"Para continuar usando o RH Assistant Pro:")
            print(f"1. Acesse: https://aldber.github.io/rh-assistant-landing/ para escolher seu plano.")
            print(f"2. Escolha seu plano (Starter: R$ 297/mês)")
            print(f"3. Ative sua licença no menu 'Ativar Licença'")
            print(f"{'='*60}\n")
            return False
        
        return True
    
    def create_activation_server(self):
        """Cria servidor para ativação de licença"""
        import http.server
        import socketserver
        import urllib.parse
        
        class ActivationHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, config=None, **kwargs):
                self.config = config
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/activate':
                    self.send_activation_page()
                elif self.path == '/check':
                    self.send_license_status()
                else:
                    self.send_error(404)
            
            def do_POST(self):
                if self.path == '/activate':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    params = urllib.parse.parse_qs(post_data)
                    
                    license_key = params.get('license_key', [''])[0]
                    plan = params.get('plan', ['starter'])[0]
                    
                    result = self.config.licensing.activate_license(license_key, plan)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
            
            def send_activation_page(self):
                pricing = self.config.licensing.get_pricing_info()
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Ativar Licença - RH Assistant Pro</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; }}
                        .plan {{ border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }}
                        .plan.recommended {{ border-color: #4a6ee0; background: #f0f4ff; }}
                        button {{ background: #4a6ee0; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Ativar Licença - RH Assistant Pro</h1>
                        
                        <form method="POST" action="/activate">
                            <label>Chave de Licença:</label><br>
                            <input type="text" name="license_key" size="40" placeholder="RHA-S-XXXXXXXXXXXXXX"><br><br>
                            
                            <label>Plano:</label><br>
                            <select name="plan">
                                <option value="starter">Starter - R$ 297/mês</option>
                                <option value="growth">Growth - R$ 597/mês</option>
                                <option value="enterprise">Enterprise - R$ 997/mês</option>
                            </select><br><br>
                            
                            <button type="submit">Ativar Licença</button>
                        </form>
                    </div>
                </body>
                </html>
                """
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            
            def send_license_status(self):
                status = self.config.get_license_info()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(status).encode('utf-8'))
        
        return ActivationHandler