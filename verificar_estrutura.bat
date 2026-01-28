@echo off
echo 🔍 VERIFICANDO ESTRUTURA DO PROJETO
echo ==================================

echo.
echo 📍 Pasta atual: %cd%
echo.

echo 📁 Estrutura encontrada:
dir /b

echo.
echo 📋 Verificando arquivos essenciais...
set "erro=0"

if not exist "app_profissional.py" (
    echo ❌ app_profissional.py - NÃO ENCONTRADO
    set "erro=1"
) else (
    echo ✅ app_profissional.py - OK
)

if not exist "data\" (
    echo ⚠️  data\ - NÃO ENCONTRADA (será criada automaticamente)
) else (
    echo ✅ data\ - OK
    echo    Conteúdo:
    dir /b data\
)

if not exist "assets\" (
    echo ⚠️  assets\ - NÃO ENCONTRADA (será criada automaticamente)
) else (
    echo ✅ assets\ - OK
)

echo.
if %erro%==1 (
    echo ❌ CORRIJA OS ERROS ACIMA ANTES DE EMPACOTAR!
) else (
    echo ✅ ESTRUTURA PRONTA PARA EMPACOTAMENTO!
    echo.
    echo 🚀 Execute: empacotar_final.bat
)

pause