#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    sp_path = os.path.join(os.path.dirname(sys.executable), 'Lib/site-packages')
    plugins_path = os.path.join(sp_path, 'PyQt4/plugins')
    # following line only for PyQt with Qt5
    # include_files.append((os.path.join(plugins_path, 'platforms/qwindows.dll'), 'platforms/qwindows.dll'))
    include_files.append((os.path.join(plugins_path, 'imageformats/qico4.dll'), 'imageformats/qico4.dll'))
    savRW_path = os.path.join(sp_path, 'savReaderWriter')
    savRW_lib_dir = r'spssio/win32'
    savRW_lib_files = [os.path.join(savRW_lib_dir, libfile) for libfile in os.listdir(os.path.join(savRW_path, savRW_lib_dir))]
    savRW_lib_files.append('VERSION')
    include_files += [(os.path.join(savRW_path, f), os.path.join('savReaderWriter', f)) for f in savRW_lib_files]

setup(
        name = "RPK-Teilnehmerdatenerfassung",
        version = "0.1",
        description = "Beispielanwendung yur Teilnehmerdatenerfassung...",
        # options = {'build_exe': {'include_files': include_files, 'zip_includes': zip_includes, "create_shared_zip": False}},
        # options = {'build_exe': {'includes': includes, 'include_files': include_files, 'zip_includes': zip_includes}},
        options = {'build_exe': {'includes': includes, 'include_files': include_files}},
        executables = [Executable("teilnehmerbogen.py", base = base, icon = 'icons/python.ico')])
