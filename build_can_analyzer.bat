@echo off
setlocal

pushd "%~dp0can_analyser"
if errorlevel 1 goto :missing_project

where py >nul 2>&1
if errorlevel 1 goto :missing_python

py -m PyInstaller --version >nul 2>&1
if errorlevel 1 goto :missing_pyinstaller

echo Building a single-file, windowed CAN Analyzer executable...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name CAN_Analyzer main.py
if errorlevel 1 goto :build_failed

if not exist "dist\CAN_Analyzer.exe" goto :missing_output

echo.
echo Build succeeded:
echo %CD%\dist\CAN_Analyzer.exe
popd
pause
exit /b 0

:missing_project
echo ERROR: Could not find the can_analyser project folder next to this script.
pause
exit /b 1

:missing_python
echo ERROR: The Python launcher "py" was not found on PATH.
echo Install Python and enable the Python launcher, then try again.
goto :failed

:missing_pyinstaller
echo ERROR: PyInstaller is not installed for the Python selected by "py".
echo Install it with: py -m pip install pyinstaller
goto :failed

:build_failed
set "BUILD_ERROR=%ERRORLEVEL%"
echo.
echo ERROR: PyInstaller build failed with exit code %BUILD_ERROR%.
popd
pause
exit /b %BUILD_ERROR%

:missing_output
echo ERROR: PyInstaller finished but dist\CAN_Analyzer.exe was not created.
goto :failed

:failed
popd
pause
exit /b 1
