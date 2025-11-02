@echo off
echo ===================================
echo   Instalando dependencias...
echo ===================================
pip install pyinstaller
pip install pygame

echo ===================================
echo   Compilando Clue MINECRAFT .exe
echo   Esto puede tardar unos minutos...
echo ===================================

REM Asumiendo que tu script se llama Clue_minecraft_gui.py
SET SCRIPT_NAME="Clue_minecraft_gui.py"

REM Asumiendo que tus assets estan en la carpeta "assets"
SET ASSET_FOLDER="assets"

REM --- CAMBIO PRINCIPAL ---
REM Llamamos a pyinstaller usando "python -m" para asegurar que se encuentre
python -m PyInstaller --onefile --noconsole --add-data "%ASSET_FOLDER%;%ASSET_FOLDER%" %SCRIPT_NAME%

@echo on
echo.
echo ===================================
echo   ¡Compilacion Terminada!
echo ===================================
echo Tu archivo .exe se encuentra en la carpeta 'dist'.
echo.
pause