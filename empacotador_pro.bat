@echo off
echo ========================================
echo 🚀 EMPACOTADOR RH ASSISTANT PRO - FINAL
echo ========================================

echo.
echo 📍 Localização atual: %cd%
echo.

echo 1. Verificando arquivos necessários...
if not exist "app_profissional.py" (
    echo ❌ ERRO: app_profissional.py não encontrado!
    echo 💡 Certifique-se de estar na pasta do projeto.
    pause
    exit /b 1
)

if not exist "data\" (
    echo ⚠️  AVISO: Pasta 'data' não encontrada. Criando...
    mkdir data
    echo ✅ Pasta 'data' criada com sucesso.
)

if not exist "assets\" (
    echo ⚠️  AVISO: Pasta 'assets' não encontrada. Criando...
    mkdir assets
    echo ✅ Pasta 'assets' criada com sucesso.
)

echo.
echo 2. Limpando compilações anteriores...
if exist "build\" (
    echo 🗑️  Removendo pasta 'build'...
    rmdir /s /q "build"
    echo ✅ Pasta 'build' removida.
)

if exist "dist\" (
    echo 🗑️  Removendo pasta 'dist'...
    rmdir /s /q "dist"
    echo ✅ Pasta 'dist' removida.
)

if exist "RH_Assistant_Pro.spec" (
    echo 🗑️  Removendo arquivo .spec antigo...
    del "RH_Assistant_Pro.spec"
    echo ✅ Arquivo .spec removido.
)

echo.
echo 3. Verificando PyInstaller...
python -m pip list | findstr PyInstaller >nul
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller --quiet
    echo ✅ PyInstaller instalado.
) else (
    echo ✅ PyInstaller já instalado.
)

echo.
echo 4. Empacotando aplicação...
echo 📦 Este processo pode levar alguns minutos...

pyinstaller --onefile ^
            --name "RH_Assistant_Pro" ^
            --add-data "data;data" ^
            --hidden-import=json ^
            --hidden-import=os ^
            --hidden-import=http.server ^
            --hidden-import=socketserver ^
            --hidden-import=webbrowser ^
            --hidden-import=threading ^
            --hidden-import=datetime ^
            --hidden-import=urllib.parse ^
            --noconsole ^
            app_profissional.py

echo.
echo 5. Verificando resultado...
if exist "dist\RH_Assistant_Pro.exe" (
    echo.
    echo 🎉🎉🎉 EMPACOTAMENTO CONCLUÍDO COM SUCESSO! 🎉🎉🎉
    echo ================================================
    echo.
    echo 📁 Executável gerado em: %cd%\dist\RH_Assistant_Pro.exe
    echo 📏 Tamanho do arquivo:
    for %%F in (dist\RH_Assistant_Pro.exe) do echo        %%~zF bytes
    echo.
    echo 🧪 PARA TESTAR:
    echo   1. Navegue até: cd dist
    echo   2. Execute: RH_Assistant_Pro.exe
    echo   3. Acesse: http://localhost:8000
    echo.
    echo 📦 PARA ENTREGAR AO CLIENTE:
    echo   - Envie a pasta "dist" inteira
    echo   - Ou apenas o arquivo "RH_Assistant_Pro.exe"
    echo.
    echo ⚠️  IMPORTANTE: O cliente precisa da pasta "data" junto!
) else (
    echo.
    echo ❌❌❌ FALHA NO EMPACOTAMENTO! ❌❌❌
    echo Verifique os erros acima.
)

echo.
pause