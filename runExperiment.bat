@ECHO OFF

set /p pid="Please enter participants number: "

start "" https://rit.az1.qualtrics.com/jfe/form/SV_e4nSsaQNBIgMn54?PID=%pid%

PAUSE

python rcTask.py %pid%

PAUSE

start "" https://rit.az1.qualtrics.com/jfe/form/SV_0pnY9uBdhTs34YS?PID=%pid%

