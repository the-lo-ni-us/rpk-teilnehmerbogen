del /S /Q build > NUL
del /S /Q dist > NUL

rem @echo %PROCESSOR_ARCHITECTURE% > ARCH
rem python -c 'import sys; print(sys.maxsize > 2**32)' > x64
create_dbase.py
setup_cx_freeze.py build
@PAUSE