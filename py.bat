@echo off


set "EXE_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
set "BASE=%~dp0"
set "NOMEFILE=python.exe"


for /d %%D in ("%BASE%*") do (
    if exist "%%D\Scripts\%NOMEFILE%" (
        set "EXE_PATH=%%D\Scripts\%NOMEFILE%"
    )
)

echo EXE_PATH: %EXE_PATH%
"%EXE_PATH%" %*
