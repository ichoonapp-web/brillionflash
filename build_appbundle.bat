@echo off
echo ================================================================
echo  BRILLIONFLASH GLOBAL #1 - AUTOMATIC APP BUILDER & LAUNCHER
echo ================================================================
echo.
echo [1/3] Navigating to Brillionflash Mobile Project...
cd "C:\Users\home\StudioProjects\brillion flash.1"

echo [2/3] Setting Java Home Environment...
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr

echo [3/3] Building Release Android App Bundle (.aab)...
call gradlew.bat bundleRelease --no-daemon

echo.
echo ================================================================
echo  SUCCESS! App Bundle generated. Opening output directory...
echo ================================================================
explorer "C:\Users\home\StudioProjects\brillion flash.1\app\build\outputs\bundle\release"
pause
