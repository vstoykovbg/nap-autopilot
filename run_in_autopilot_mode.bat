@echo off

REM Check if python3 is available
python3 --version >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_COMMAND=python3
) else (

    REM Search for python.exe in user's directory (AppData)
    for /f "delims=" %%i in ('dir /b /s "%APPDATA%\Python\Python*" ^| findstr /i /r "python[.]exe$"') do (
        set PYTHON_COMMAND=%%i
        goto :found_python
    )

    REM Search for python.exe in Program Files directory
    for /f "delims=" %%i in ('dir /b /s "C:\Program Files\Python*" ^| findstr /i /r "python[.]exe$"') do (
        set PYTHON_COMMAND=%%i
        goto :found_python
    )

    REM Search for python.exe in local programs directory (AppData)
    for /f "delims=" %%i in ('dir /b /s "%LOCALAPPDATA%\Programs\Python\Python*" ^| findstr /i /r "python[.]exe$"') do (
        set PYTHON_COMMAND=%%i
        goto :found_python
    )

    REM If Python is not found, display error message and exit
    echo Error: Python interpreter not found.
    echo Please install Python and make sure it is added to the system PATH.
    echo.
    echo After your confirmation the script will stop and the console may be closed.
    pause
    exit /b 1
)

REM Label to jump to when Python is found
:found_python

REM If Python interpreter is found, continue with script execution
if defined PYTHON_COMMAND (
    REM Execute the main Python script
    %PYTHON_COMMAND% autopilot.py
)

REM Display message and wait for user input to close the console
echo.
echo After your confirmation the script will stop and the console may be closed.
pause

