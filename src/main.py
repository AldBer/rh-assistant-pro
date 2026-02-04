# src/main.py - Ajuste para nova estrutura
import os
import sys
import webbrowser
import threading

# Ajusta o path para incluir a pasta src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from server import run_server
from triagem import EMOJIS

def main():
    # Verifica licença
    config = Config()
    
    if not config.show_license_screen():
        print("⏳ Aguardando ativação da licença...")
        print("🌐 Acesse: http://localhost:8001 para ativar")
        
        # Inicia servidor de ativação
        import http.server
        import socketserver
        
        handler = config.create_activation_server()
        activation_server = socketserver.TCPServer(("", 8001), lambda *args, **kwargs: handler(*args, config=config, **kwargs))
        
        # Abre navegador para ativação
        threading.Timer(1, lambda: webbrowser.open("http://localhost:8001/activate")).start()
        
        print(f"🔑 Servidor de ativação: http://localhost:8001")
        print(f"🔄 Verificando licença a cada 30 segundos...")
        
        try:
            # Mantém servidor de ativação rodando enquanto verifica licença
            import time
            while True:
                activation_server.handle_request()  # Processa uma requisição
                
                # Verifica se licença foi ativada
                config.license_status = config.licensing.check_license()
                if config.license_status['valid']:
                    print(f"\n✅ Licença ativada com sucesso!")
                    print(f"📋 Plano: {config.license_status.get('plan', 'starter').upper()}")
                    break
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n👋 Ativação cancelada.")
            sys.exit(0)
    
    # Se licença válida, inicia servidor principal
    PORT = 8000
    
    print(f"\n{'='*60}")
    print(f"🚀 RH ASSISTANT PRO - VERSÃO COMERCIAL v1.0")
    print(f"{'='*60}")
    
    license_info = config.get_license_info()
    if license_info['type'] == 'trial':
        print(f"{EMOJIS['clock']} **Modo Teste:** {license_info['days_left']} dias restantes")
    else:
        print(f"{EMOJIS['crown']} **Licença Ativa:** Plano {license_info.get('plan', 'starter').upper()}")
    
    print(f"{EMOJIS['rocket']} Sistema 100% funcional")
    print(f"{EMOJIS['star']} Triagem inteligente")
    print(f"{EMOJIS['money']} Pronto para produção")
    print(f"{'='*60}")
    
    # Cria diretórios necessários
    os.makedirs('data', exist_ok=True)
    
    print(f"\n🌐 **ACESSO CLIENTE:** http://localhost:{PORT}")
    print(f"📁 **Dados:** {os.path.abspath('data')}")
    
    if license_info['type'] == 'trial':
        print(f"⏰ **{license_info['days_left']} DIAS GRÁTIS** - Depois R$ 297/mês")
    else:
        print(f"✅ **LICENÇA ATIVA** - Plano {license_info.get('plan', 'starter').upper()}")
    
    print(f"{EMOJIS['stop']} Ctrl+C para encerrar")
    print(f"{'='*60}")
    
    try:
        # Abre no navegador
        threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    except:
        pass
    
    try:
        run_server(PORT)
    except KeyboardInterrupt:
        print(f"\n{EMOJIS['wave']} Sistema encerrado!")
        
        # Mostra estatísticas de uso
        from assistant import RHAssistantPro
        assistant = RHAssistantPro()
        metricas = assistant.get_metricas()
        
        print(f"\n{EMOJIS['chart']} **RELATÓRIO DA SESSÃO:**")
        print(f"   • Consultas realizadas: {metricas['total_consultas']}")
        print(f"   • Auto-resolução: {metricas['taxa_sucesso']}")
        print(f"   • Tempo economizado: {metricas['economia_tempo']}")
        print(f"   • Chamados abertos: {metricas['encaminhadas_rh']}")
        print(f"\n{EMOJIS['rocket']} **Pronto para vender para clientes!**")

if __name__ == "__main__":
    main()