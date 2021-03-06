@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation on Windows

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build
set SPHINXPROJ=Test

if "%1" == "" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    echo.
    echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
    echo.installed, then set the SPHINXBUILD environment variable to point
    echo.to the full path of the 'sphinx-build' executable. Alternatively you
    echo.may add the Sphinx directory to PATH.
    echo.
    echo.If you don't have Sphinx installed, grab it from
    echo.http://sphinx-doc.org/
    exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%


:htmlview
if NOT "%2" EQU "" (
    echo.Can't specify filenames to build with htmlview target, ignoring.
)
cmd /C %this% html

if EXIST %BUILDDIR%\html\index.html (
    echo.Opening %BUILDDIR%\html\index.html in the default web browser...
    start %BUILDDIR%\html\index.html
)


if "%1" == "pdf" (
   %SPHINXBUILD% -b pdf %ALLSPHINXOPTS% %BUILDDIR%/pdf
   if errorlevel 1 exit /b 1
   echo.
   echo.Build finished. The pdf files are in %BUILDDIR%/pdf.
   goto end
)


:end
popd