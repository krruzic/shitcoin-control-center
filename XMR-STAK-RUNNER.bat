set pwd=%cd%
SET XMRSTAK_NOWAIT=1
start "MINING %1" "%pwd%\xmr-stak" --noUAC --noNVIDIA --noCPU --config %1
