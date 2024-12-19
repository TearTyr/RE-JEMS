@echo off
setlocal

REM --- Configuration ---
set ADDON_NAME=REJEMS-Alter
set ADDON_DIR=REJEMS-Alter
set OUTPUT_DIR=output
set ZIP_NAME=%ADDON_NAME%.zip

REM --- Create output directory if it doesn't exist ---
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM --- Clean up previous zip file ---
if exist "%OUTPUT_DIR%\%ZIP_NAME%" del "%OUTPUT_DIR%\%ZIP_NAME%"

REM --- Zip the add-on, make sure 7z.exe is in your PATH environment variable ---
"c:\Program Files\7-Zip\7z.exe" a -tzip "%OUTPUT_DIR%\%ZIP_NAME%" "%ADDON_DIR%\*" -xr!.git -xr!.gitignore -xr!.gitattributes -x!__pycache__

echo Add-on zipped to: %OUTPUT_DIR%\%ZIP_NAME%
pause
endlocal