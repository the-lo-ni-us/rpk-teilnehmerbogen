
import sys, os

from cx_Freeze import setup, Executable

includes = [
    "sqlalchemy.dialects.sqlite",
    "sqlalchemy.dialects.postgresql",
    "psycopg2",
    "sip",
    "savReaderWriter",
    "reportlab.pdfbase._can_cmap_data",
    "reportlab.pdfbase._cidfontdata",
    "reportlab.pdfbase._fontdata",
    "reportlab.pdfbase._fontdata_enc_macexpert",
    "reportlab.pdfbase._fontdata_enc_macroman",
    "reportlab.pdfbase._fontdata_enc_pdfdoc",
    "reportlab.pdfbase._fontdata_enc_standard",
    "reportlab.pdfbase._fontdata_enc_symbol",
    "reportlab.pdfbase._fontdata_enc_winansi",
    "reportlab.pdfbase._fontdata_enc_zapfdingbats",
    "reportlab.pdfbase._fontdata_widths_courier",
    "reportlab.pdfbase._fontdata_widths_courierbold",
    "reportlab.pdfbase._fontdata_widths_courierboldoblique",
    "reportlab.pdfbase._fontdata_widths_courieroblique",
    "reportlab.pdfbase._fontdata_widths_helvetica",
    "reportlab.pdfbase._fontdata_widths_helveticabold",
    "reportlab.pdfbase._fontdata_widths_helveticaboldoblique",
    "reportlab.pdfbase._fontdata_widths_helveticaoblique",
    "reportlab.pdfbase._fontdata_widths_symbol",
    "reportlab.pdfbase._fontdata_widths_timesbold",
    "reportlab.pdfbase._fontdata_widths_timesbolditalic",
    "reportlab.pdfbase._fontdata_widths_timesitalic",
    "reportlab.pdfbase._fontdata_widths_timesroman",
    "reportlab.pdfbase._fontdata_widths_zapfdingbats"
]

include_files = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    plugins_path = 'Lib/site-packages/PyQt4/plugins'
    savRW_path = r'C:\Programme\Python27\Lib\site-packages\savReaderWriter'
    # following line only for PyQt with Qt5
    # include_files.append((os.path.join(os.path.dirname(sys.executable), plugins_path, 'platforms/qwindows.dll'), 'platforms/qwindows.dll'))
    include_files.append((os.path.join(os.path.dirname(sys.executable), plugins_path, 'imageformats/qico4.dll'), 'imageformats/qico4.dll'))
    include_files.append((os.path.join(savRW_path, r'VERSION'), r'savReaderWriter\VERSION'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\icudt48.dll'),'savReaderWriter\spssio\win32\icudt48.dll'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\icuin48.dll'),'savReaderWriter\spssio\win32\icuin48.dll'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\icuuc48.dll'),'savReaderWriter\spssio\win32\icuuc48.dll'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\spssio32.dll'),'savReaderWriter\spssio\win32\spssio32.dll'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\spssjdio.dll'),'savReaderWriter\spssio\win32\spssjdio.dll'))
    include_files.append((os.path.join(savRW_path, r'spssio\win32\zlib123spss.dll'),'savReaderWriter\spssio\win32\zlib123spss.dll'))
    # zip_includes = [(r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\VERSION', r'savReaderWriter\VERSION')]
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\icudt48.dll','savReaderWriter\spssio\win32\icudt48.dll'))
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\icuin48.dll','savReaderWriter\spssio\win32\icuin48.dll'))
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\icuuc48.dll','savReaderWriter\spssio\win32\icuuc48.dll'))
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\spssio32.dll','savReaderWriter\spssio\win32\spssio32.dll'))
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\spssjdio.dll','savReaderWriter\spssio\win32\spssjdio.dll'))
    # zip_includes.append((r'C:\Programme\Python27\Lib\site-packages\savReaderWriter\spssio\win32\zlib123spss.dll','savReaderWriter\spssio\win32\zlib123spss.dll'))

setup(
        name = "RPK-Teilnehmerdatenerfassung",
        version = "0.1",
        description = "Beispielanwendung yur Teilnehmerdatenerfassung...",
        # options = {'build_exe': {'include_files': include_files, 'zip_includes': zip_includes, "create_shared_zip": False}},
        # options = {'build_exe': {'includes': includes, 'include_files': include_files, 'zip_includes': zip_includes}},
        options = {'build_exe': {'includes': includes, 'include_files': include_files}},
        executables = [Executable("teilnehmerbogen.py", base = base, icon = 'icons/python.ico')])
