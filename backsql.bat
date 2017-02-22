@echo off
SET a=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
mysqldump -u root -pchangeit! mzproject > D:\mzproject\zyw\mysqldata\mzproject_%a%.sql    