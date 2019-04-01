for /f "tokens=*" %%a in ('where python') do set py=%%a
for /f "tokens=3" %%a in ('wmic process call create "%py% monitor.py"^,"%~dp0"^|find "ProcessId"') do set pid=%%a
echo %pid:~0,-1% > pid.txt