del /S /Q build > NUL
del /S /Q dist > NUL

@echo %PROCESSOR_ARCHITECTURE% > ARCH
create_dbase.py
setup.py py2exe
@PAUSE