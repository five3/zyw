@echo off
set d=D:\mzproject\zyw\
D:
cd %d%
call D:\mzproject\Scripts\activate.bat
start /b python %d%manage.py runserver 8001 > %d%log.txt