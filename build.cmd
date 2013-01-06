del /S /Q build > NUL
del /S /Q dist > NUL
create_dbase.py
python setup.py py2exe
@PAUSE