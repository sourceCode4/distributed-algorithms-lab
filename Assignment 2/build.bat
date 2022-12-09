cd logs
for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)
cd ..
if "%1"=="" (python src/setup.py) else (python src/setup.py -n "%1")
docker-compose build