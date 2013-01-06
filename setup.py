from distutils.core import setup
import py2exe, sys, os
from glob import glob

DLL_PATH = r'%s\\MS_DLLs' % os.environ['USERPROFILE']
PYTHON_PATH = 'C:\\Programme\\Python27\\Lib\\site-packages'
sys.path.append(DLL_PATH)
data_files = [("icons", glob(r'icons\\*.png')+[('icons\\python.ico')]),
              ("xls", glob(r'xls\\*.xls')),
              # ('', [('versions.ini')]),
              ("Microsoft.VC90.CRT", glob(r'%s\\*.*'%DLL_PATH))]
packages = [
    "sqlalchemy.dialects.sqlite",
    "sqlalchemy.dialects.postgresql",
    "psycopg2",
    "sip",
    # "PyQt4._qt",
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
setup(#data_files=data_files,
      windows=[{'script': 'teilnehmerbogen.py', 
                'icon_resources': [(1, 'icons/python.ico')]
                }],
      options={'py2exe': {'packages': packages}}
      )
