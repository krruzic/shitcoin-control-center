set pwd=%cd%
SET XMRSTAK_NOWAIT=1
REM change the args below to whatever you'd like. 
start "MINING %1" "%pwd%\xmr-stak" --noUAC --noNVIDIA --noCPU --config %1
