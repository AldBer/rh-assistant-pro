#!/usr/bin/env python3
"""
Verificador de Sintaxe - RH Assistant Pro
Executa antes do empacotamento para detectar erros.
"""

import sys
import os

def verificar_arquivo(caminho_arquivo):
    """Verifica se um arquivo Python tem erros de sintaxe"""
    print(f"🔍 Verificando: {caminho_arquivo}")
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Tenta compilar para verificar sintaxe
        compile(codigo, caminho_arquivo, 'exec')
        print(f"✅ {caminho_arquivo} - Sintaxe OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ ERRO DE SINTAXE em {caminho_arquivo}:")
        print(f"   Linha {e.lineno}: {e.msg}")
        print(f"   Texto: {e.text}")
        return False
    except Exception as e:
        print(f"⚠️  Erro ao verificar {caminho_arquivo}: {e}")
        return False

def main():
    arquivos_para_verificar = [
        "app_profissional.py"
    ]
    
    todos_ok = True
    
    for arquivo in arquivos_para_verificar:
        if os.path.exists(arquivo):
            if not verificar_arquivo(arquivo):
                todos_ok = False
        else:
            print(f"❌ Arquivo não encontrado: {arquivo}")
            todos_ok = False
    
    print("\n" + "="*50)
    if todos_ok:
        print("🎉 TODOS OS ARQUIVOS ESTÃO COM SINTAXE CORRETA!")
        print("🚀 Pode prosseguir com o empacotamento.")
    else:
        print("❌ CORRIJA OS ERROS ACIMA ANTES DE EMPACOTAR!")
    
    return todos_ok

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)