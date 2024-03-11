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

REM Define the location of the requirements.txt file
set REQUIREMENTS_FILE=requirements.txt

REM Check if pip is available
%PYTHON_COMMAND% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed.
    echo Please install pip to continue.
    echo.
    echo After your confirmation the script will stop and the console may be closed.
    pause
    exit /b 1
)

REM Install requirements from requirements.txt
%PYTHON_COMMAND% -m pip install -r %REQUIREMENTS_FILE%
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements using pip.
    echo Please check the requirements.txt file and try again.
    echo.
    echo After your confirmation the script will stop and the console may be closed.
    pause
    exit /b 1
)

REM Display message and wait for user input to close the console
echo.
echo After your confirmation the script will stop and the console may be closed.
pause

