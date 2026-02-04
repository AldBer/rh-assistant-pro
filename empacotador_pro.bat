@echo off
chcp 65001 >nul
echo ========================================
echo  🚀 EMPACOTADOR RH ASSISTANT PRO v2.1
echo ========================================
echo.

REM Verifica estrutura
if not exist "src\main.py" (
    echo ❌ Erro: Estrutura incorreta!
    echo Execute primeiro os comandos de organizacao
    pause
    exit /b 1
)

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Instale Python 3.8+ em: https://python.org
    pause
    exit /b 1
)

echo 📦 Instalando dependencias...
pip install -r requirements.txt >nul 2>&1
pip install --upgrade pyinstaller >nul 2>&1

echo.
echo 🛠️  Criando executável profissional...
echo.

REM Remove arquivos .spec antigos se existirem
if exist "build_spec.spec" del "build_spec.spec"

REM Cria especificação CORRIGIDA (faltava vírgula na linha 16)
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo import sys
echo import os
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['src/main.py'],
echo     pathex=['src'],
echo     binaries=[],
echo     datas=[
echo         ('src/data/*.json', 'data'),
echo         ('src/static/*', 'static'),
echo         ('src/config.json', '.'),
echo         ('src/license.json', '.')
echo     ],
echo     hiddenimports=[],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False
echo )
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.datas,
echo     [],
echo     name='RH_Assistant_Pro',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=True,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None
echo )
) > RH_Assistant_Pro.spec

REM Limpa builds anteriores
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Executa PyInstaller SEM --onefile quando tem .spec
echo ⚙️  Compilando...
pyinstaller --clean --noconfirm RH_Assistant_Pro.spec

if errorlevel 1 (
    echo ❌ Erro ao criar executável!
    echo Verifique se todos os arquivos Python estão em src/
    pause
    exit /b 1
)

echo.
echo ✅ Executável criado: dist\RH_Assistant_Pro\RH_Assistant_Pro.exe
echo.

REM Move para formato onefile manualmente
echo 📁 Convertendo para formato portable...
copy "dist\RH_Assistant_Pro\RH_Assistant_Pro.exe" "dist\RH_Assistant_Pro.exe" >nul

REM Cria estrutura para instalador
echo 📁 Preparando instalador...
if exist "installers\windows" rmdir /s /q "installers\windows"
mkdir "installers\windows"
mkdir "installers\windows\data"
mkdir "installers\windows\static"

REM Copia arquivos necessários
copy "dist\RH_Assistant_Pro.exe" "installers\windows\" >nul
xcopy "src\data\*.json" "installers\windows\data\" /Y >nul
xcopy "src\static\*" "installers\windows\static\" /Y >nul
copy "src\config.json" "installers\windows\" >nul
copy "src\license.json" "installers\windows\" >nul
copy "README_Cliente.md" "installers\windows\" >nul

REM Cria arquivo ZIP para download
echo 📦 Criando pacote para download...
cd "installers\windows"
powershell -Command "Compress-Archive -Path * -DestinationPath ..\RH_Assistant_Pro_Installer.zip -Force"
cd ..\..

echo.
echo 🎉 EMPACOTAMENTO CONCLUÍDO!
echo.
echo 📂 ARQUIVOS GERADOS:
echo   1. dist\RH_Assistant_Pro.exe (Executável portable)
echo   2. installers\RH_Assistant_Pro_Installer.zip (Pacote completo)
echo   3. installers\windows\installer.bat (Instalador)
echo.
echo 📢 PRÓXIMOS PASSOS:
echo   1. Teste o instalador
echo   2. Faça upload do ZIP para Google Drive
echo   3. Atualize o link na landing page
echo.
echo Pressione qualquer tecla para testar o executável...
pause >nul

REM Testa o executável rapidamente
echo.
echo 🧪 Testando execução rápida...
start dist\RH_Assistant_Pro.exe