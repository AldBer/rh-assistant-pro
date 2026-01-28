@echo off
echo ================================
echo EMPACOTADOR SIMPLES - RH ASSISTANT
echo ================================

echo.
echo 1. Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo 2. Empacotando...
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
if exist dist\RH_Assistant_Pro.exe (
    echo SUCESSO! Executavel criado em: dist\RH_Assistant_Pro.exe
) else (
    echo FALHA! Verifique os erros acima.
)

pause