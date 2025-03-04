@echo off
setlocal enabledelayedexpansion

:: Ask user for the file path
echo Please enter the file path that will be used for both scripts:
set /p file_path=Enter the file path: 

:: Ensure the file path is wrapped in quotes in case there are spaces
set "file_path=%file_path%"
set "secondfile=%CD%\labIPs.csv"

:MENU
echo 1. Run identical IPs with file "%file_path%"
echo 2. Run same name many IPs with file "%file_path%"
echo 3. Check mismatch between csv files and lab IPs
echo 4. Change file path
echo 5. Exit


:: Prompt for user input
set /p user_input=Enter 1, 2, 3, 4 or 5: 

if "%user_input%"=="1" (
    echo Running Script 1 with file "%file_path%"...
    if exist "%file_path%" (
        python check_identical_ips.py "%file_path%"
    ) else (
        echo The file path you entered does not exist. Please check and try again.
    )
    goto MENU
) else if "%user_input%"=="2" (
    echo Running Script 2 with file "%file_path%"...
    if exist "%file_path%" (
        echo format hours hh:mm
        set /p start_hour=Enter the starting hour: 
        set /p end_hour=Enter the ending hour: 
        python check_manyIps_sameName.py "%file_path%" "%start_hour%" "%end_hour%"
    ) else (
        echo The file path you entered does not exist. Please check and try again.
    )
    goto MENU
) else if "%user_input%"=="3" (
    echo Second file is: %secondfile%
    echo Running Script 3 with file "%file_path%"...
    if exist "%file_path%" (
        echo Current directory: %CD%
        echo The first file is: %file_path%
        python checkForLabIPs.py "%file_path%" "%secondfile%"
    ) else (
        echo The file path you entered does not exist. Please check and try again.
    )
    goto MENU
) else if "%user_input%"=="4" (
    echo Changing the file path...
    echo Please enter a new file path:
    set /p file_path=Enter the new file path: 
    set "file_path=%file_path%"
    goto MENU
) else if "%user_input%"=="5" (
    echo Exiting the program.
    exit
) else (
    echo Invalid input. Please enter 1, 2, 3, 4 or 5.
    goto MENU
)

pause
