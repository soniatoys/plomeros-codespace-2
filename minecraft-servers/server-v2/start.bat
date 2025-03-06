@ECHO OFF
SET BINDIR=%~dp0
CD /D "%BINDIR%"
"C:\Program Files\Java\jdk-17\bin\java.exe" -Xmx3G -Xms3G -jar server.jar
PAUSE