cd logs
for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)
cd ..
python scripts/setup.py %1 %2 %3 %4 %5 %6 %7 %8 %9
docker-compose build