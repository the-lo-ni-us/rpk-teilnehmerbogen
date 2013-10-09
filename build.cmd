del /S /Q build > NUL
del /S /Q dist > NUL

@echo %PROCESSOR_ARCHITECTURE% > ARCH
create_dbase.py
setup_cx_freeze.py build
@PAUSE