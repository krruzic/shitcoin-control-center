set pwd=%cd%
SET XMRSTAK_NOWAIT=1
REM change the args below to whatever you'd like. 
start "MINING %3" "%pwd%\xmr-stak" --noUAC %~1 %~2 --config %~3
