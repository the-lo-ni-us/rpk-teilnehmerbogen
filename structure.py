#!/usr/bin/env python
# coding=utf-8
import datetime
from fieldname_list import FieldnameList
from settings import *

structure = FieldnameList([
  {
    'title': u"Name",
    'fieldname': u"name",
    'allowance': '',
    'typ': 'str',
    'default': '',
    'disabled': False,
    'appears': ('capture', 'documentation')
  },
  {
    'title': u"geboren",
    'fieldname': u"birthdate",
    'disabled': True,
    'default': datetime.date(1970,1,1)
  },
  {
    'title': u"1 - Einrichtungs-Code Nr.: (Postleitzahl)",
    'fieldname': CONFIG_ZIP_NAME,
    'allowance': '',
    'typ': 'str',
    'default': '',
    'appears': ('tabulation',)
  },
  {
    'title': u"Medizinisch/Teilhabe planmässig/vorzeitig",
    'fieldname': u"mtpv",
    'typ': 'dropdown',
    'default': 4,
    'allowance': [
      u"Medizinisch-planmässig",
      u"Medizinisch-vorzeitig",
      u"Teilhabe-planmässig",
      u"Teilhabe-vorzeitig",
      u""
    ],
    'appears': ('capture', 'documentation')
  }, 
  {
    'title': u"Teilnahme abgeschlossen",
    'fieldname': 'jahr',
    'allowance': [
      ('',u'ungewiss'),
      ('2014','2014'),
      ('2013','2013'),
      ('2012','2012'),
      ('2011','2011'),
      ('2010','2010')
    ],
    'typ': 'enum',
    'default': '',
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"Teilnahme abgeschlossen",
    'fieldname': 'jahr2',
    'default': None,
    'typ': 'date',
    'disabled': True,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"2 - Gesamtverweildauer in der RPK-Maßnahme: (Kalendertage medizinische, ggf. plus berufliche Reha)",
    'fieldname': u"f2",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"2a - davon Kalendertage vorausgegangene medizinische Reha",
    'fieldname': u"f2a",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"3 - Anzahl der in diesem Summenbogen erfassten Rehabilitanden",
    'fieldname': u"count_participants",
    'typ': 'int',
    'default': -1,
    'appears': ('tabulation',),
  }, 
  {
    'title': u"Soziodemografische Merkmale der Rehabilitanden (bei Aufnahme in eine RPK)",
    'fieldname': u"f4",
    'typ': 'heading',
    'allowance': None,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"5 - Geschlecht ",
    'fieldname': u"f5",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [
      u"00 - keine Angabe / nicht bekannt",
      u"01 - männlich",
      u"02 - weiblich"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"6 - Alter bei Aufnahme (in Jahren)",
    'fieldname': u"f6",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"7 - Familienstand",
    'fieldname': u"f7",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ledig",
      u"02 - verheiratet",
      u"03 - getrennt lebend",
      u"04 - geschieden",
      u"05 - verwitwet"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"8 - Lebensverhältnisse (in den letzten 4 Wochen vor der Aufnahme)",
    'fieldname': u"f8",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - lebe allein",
      u"02 - mit Ehe-(Partner)",
      u"03 - bei den Eltern / Elternteil",
      u"04 - bei Verwandten / Bekannten",
      u"05 - betreutes Wohnen",
      u"06 - Leben innerhalb einer Einrichtung",
      u"07 - alleinerziehend"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"9 - Zahl der Kinder",
    'fieldname': u"f9",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - keine Kinder",
      u"02 - ein Kind",
      u"03 - zwei Kinder",
      u"04 - drei Kinder und mehr"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"10 - Wohnsituation (z.B.: Betreutes Einzelwohnen = 01) ",
    'fieldname': u"f10",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - eigene Wohnung",
      u"02 - Wohnung im elterlichen Haus",
      u"03 - Zimmer in elterlichen Wohnung/elterliches Haus",
      u"04 - Wohngemeinschaft",
      u"05 - Leben in einer Einrichtung",
      u"06 - ohne festen Wohnsitz"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"11 - Überwiegender Lebensunterhalt (in den letzten 4 Wochen    vor der Aufnahme)",
    'fieldname': u"f11",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - eigenenes Arbeitseinkommen",
      u"02 - finanzielle Unterstützung durch Angehörige",
      u"03 - Krankengeld",
      u"04 - Übergangsgeld",
      u"05 - Arbeitslosengeld I",
      u"06 - Arbeitslosengeld II",
      u"07 - Sozialhilfe / Grundsicherung",
      u"08 - Ausbildungsbeihilfe",
      u"09 - BU/EU/Unfall-/Erwerbsminderungsrente",
      u"10 - sonstiges Einkommen / Vermögen"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"12 - Höchster Schulabschluss",
    'fieldname': u"f12",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ohne Schulabschluss",
      u"02 - Sonderschulabschluss",
      u"03 - Hauptschulabschluss",
      u"04 - Mittlere Reife oder vergleichbarer Abschluss",
      u"05 - (Fach-) Abitur",
      u"06 - noch Schüler"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"13 - Höchster beruflicher Abschluss (z.B. noch Schüler=1)",
    'fieldname': u"f13",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ohne Ausbildung / Anlernverhältnis",
      u"02 - Lehre oder vergleichbare Ausbildung",
      u"03 - Fachschule oder vergleichbares",
      u"04 - Fachhoch- Hochschule",
      u"05 - zurzeit noch Student",
      u"06 - zurzeit noch in beruflicher Ausbildung"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"15 - Dauer der letzten sozialversicherungspflichtigen beruflichen Tätigkeit",
    'fieldname': u"f15",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - bis zu 1 Monat",
      u"02 - bis zu 6 Monaten",
      u"03 - bis zu 1 Jahr",
      u"04 - bis zu 3 Jahren",
      u"05 - bis zu 5 Jahren",
      u"06 - länger als 5 Jahre",
      u"07 - noch nie berufstätig gewesen",
      u"08 - noch Schüler/Student/Auszubildender"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"15.1 - Gesamtdauer aller sozialversicherungspflichtigen beruflichen Tätigkeiten (in Jahren): (auch Ausbildungszeiten; Versicherungsverlauf eventuell beim Rentenvers. klären)", 
    'fieldname': u"f15_1",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"16 - Zeitraum zwischen letzter beruflicher Tätigkeit und    Aufnahme  ",
    'fieldname': u"f16",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - bis direkt vor der Aufnahme gearbeitet",
      u"02 - bis 6 Monate vor der Aufnahme gearbeitet",
      u"03 - bis 1 Jahr vor der Aufnahme gearbeitet",
      u"04 - bis 3 Jahre vor der Aufnahme gearbeitet",
      u"05 - bis 5 Jahre vor der Aufnahme gearbeitet",
      u"06 - länger als 5 Jahre vor der Aufnahme nicht gearbeitet",
      u"07 - noch nie gearbeitet",
      u"08 - noch Schüler/Student/Auszubildender"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"17 - Erwerbs- und Ausbildungssituation   (Status zum Zeitpunkt der   Aufnahme) ",
    'fieldname': u"f17",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - allgemeiner Arbeitsmarkt - Vollzeit",
      u"02 - allgemeiner Arbeitsmarkt - Teilzeit",
      u"03 - Selbsthilfe/Integrationsbetrieb - Vollzeit",
      u"04 - Selbsthilfe/Integrationsbetrieb - Teilzeit",
      u"05 - WfbM Arbeitsbereich",
      u"06 - Hinzuverdienst / Gelegenheitsarbeiten",
      u"07 - Schüler",
      u"08 - Ausbildung (betrieblich)",
      u"09 - Ausbildung (BBW)",
      u"10 - Umschulung (betrieblich)",
      u"11 - Umschulung (BFW)",
      u"12 - Studium",
      u"13 - sonst. berufsfördernde Maßnahme (z.B. BvB)",
      u"14 - WfbM Berufsbildungsbereich",
      u"16 - Erwerbsfähig und ohne Beschäftigung",
      u"17 - Teilhabebeeinträchtigung und ohne Beschäftigung",
      u"18 - Hausfrau/Hausmann"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"19 - Rente / Rentenantrag",
    'fieldname': u"f19",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - derzeit bereits Rentenbezug",
      u"02 - Rentenantrag gestellt/ volle Erwerbsminderungsrente",
      u"03 - Rentenantrag nicht gestellt",
      u"04 - Rentenantrag gestellt / Teilerwerbsminderungsrente",
      u"05 - Rentenbezug Teilerwerbsminderungsrente"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"20 - Schwerbehindertenausweis",
    'fieldname': u"f20",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ja ( 50% und mehr GdB)",
      u"02 - beantragt",
      u"03 - nein"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"21 - Gesetzliche Betreuung",
    'fieldname': u"f21",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ja",
      u"02 - beantragt",
      u"03 - nein"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"22 - Entfernung vom Wohnort zur RPK (zu Beginn der Reha-Maßnahme,      laut Routenplaner)           ",
    'fieldname': u"f22",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - bis 20 km Umkreis",
      u"02 - bis 50 km Umkreis",
      u"03 - bis 100 km Umkreis",
      u"04 - über 100 km Umkreis"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'typ': 'pagebreak',
    'allowance': None,
    'appears': ('documentation')
  },                                                       
  {
    'title': u"Krankheitsmerkmale der Rehabilitanden",
    'typ': 'heading',
    'allowance': None,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"23.1 - 1. Diagnose (nach ICD 10 GM)",
    'fieldname': u"f23_1",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / keine Diagnose",
      u"F0",
      u"F10",
      u"F20",
      u"F30",
      u"F40",
      u"F50",
      u"F60",
      u"F70",
      u"F80",
      u"F90",
      u"F99"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"23.2 - 2. Diagnose",
    'fieldname': u"f23_2",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / keine Diagnose",
      u"F0",
      u"F10",
      u"F20",
      u"F30",
      u"F40",
      u"F50",
      u"F60",
      u"F70",
      u"F80",
      u"F90",
      u"F99"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"24 - Alter beim ersten professionellen Kontakt (in Jahren):",
    'fieldname': u"f24",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"25 - Alter bei der ersten Klinikaufnahme (in Jahren):",
    'fieldname': u"f25",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"26 - Anzahl der psychiatrischen Klinikaufenthalte:",
    'fieldname': u"f26",
    'typ': 'int',
    'default': -1,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"27 - Dauer der Klinikaufenthalte insgesamt (Stationär / Teilstationär)      ",
    'fieldname': u"f27",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ohne Aufenthalte",
      u"02 - bis zu 3 Monaten",
      u"03 - bis zu 6 Monaten",
      u"04 - bis zu 12 Monaten",
      u"05 - bis zu 3 Jahren",
      u"06 - bis zu 5 Jahren",
      u"07 - länger als 5 Jahre"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"28 - Zeitraum zwischen letzter Klinikentlassung und RPK-Aufnahme ",
    'fieldname': u"f28",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - bis zu 1 Woche",
      u"02 - bis zu 4 Wochen",
      u"03 - bis zu 6 Monaten",
      u"04 - bis zu 12 Monaten",
      u"05 - bis 2 Jahren",
      u"06 - bis zu 3 Jahren",
      u"07 - länger als 3 Jahre",
      u"08 - vorher nicht stationär/teilstationär behandelt"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"29 - Behandlung/Betreuung vor der Aufnahme (Mehrfachnennungen möglich) (in den letzten 4 Wochen vor der Aufnahme)",
    'fieldname': u"f29",
    'typ': 'multi_bool',
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - stationäre psychiatrische Behandlung",
      u"02 - teilstationäre Behandlung (Tagesklinik)",
      u"03 - Psychiatrische Ambulanz/Poliklinik",
      u"04 - niedergelassener Facharzt für Psychiatrie",
      u"05 - Hausarzt",
      u"06 - niedergelassener Psychotherapeut",
      u"07 - Sozialpsychiatrischer Dienst",
      u"08 - Psychosozialer Dienst / Berufsbegleitender Dienst / IFD",
      u"09 - Tagesstätte / ambulante Ergotherapie",
      u"10 - Beratungsstelle",
      u"11 - Selbsthilfegruppe",
      u"12 - keine",
      u"13 - Sonstiges"
    ],
    'default': False,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  # {
  #   'typ': 'pagebreak',
  #   'allowance': None,
  #   'appears': ('documentation')
  # },                                                       
  {
    'title': u"Rehabilitationsverlauf und Behandlungsergebnis",
    'typ': 'heading',
    'allowance': None,
    'appears': ('capture', 'tabulation', 'documentation')
  },                                                       
  {
    'title': u"30 - Durch wen wurde vorrangig der Kontakt zur RPK vermittelt?  ",
    'fieldname': u"f30",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - Psychiatrische Klinik / Tagesklinik",
      u"02 - niedergelassener Facharzt für Psychiatrie",
      u"03 - niedergelassener Psychotherapeut",
      u"04 - Beratungsstelle (BBD, SpDi, IFD u.a.)",
      u"05 - Reha-Träger (GKV, GRV, BA, u.a.)",
      u"06 - Psychiatrisches Heim, therapeutische WG",
      u"07 - WfbM",
      u"08 - gesetzlicher Betreuer",
      u"09 - Selbsthilfegruppe, Laienhelfer, u.a.",
      u"10 - Angehörige, Bekannte, Kollegen",
      u"11 - Eigeninitiative",
      u"12 - Psychiatrische Institutsambulanz",
      u"13 - Tagesstrukturierende Maßnahmen"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"31 - Leistungsträger der medizinischen Reha-Phase   (Abgerechnete Tage auf der Basis einer 7 Tage Woche,  ohne Unterbrechungen)",
    'fieldname': u"f31",
    'typ': 'multi_int',
    'allowance': [
      u"01 - AOK",
      u"02 - BKK",
      u"03 - IKK",
      u"04 - Ersatzkassen (BEK, DAK, TKK, u.a.)",
      u"05 - DRV Knappschaft / Bahn / See",
      u"06 - Sonderkassen (Landwirte u.a.)",
      u"07 - DRV Regional",
      u"08 - DRV Bund",
      u"09 - Berufsgenossenschaft",
      u"10 - Sozialhilfe",
      u"11 - Privatversicherung, Beihilfe, Selbstzahler",
      u"12 - Jugendhilfe",
      u"13 - Sonstiges"
    ],
    'default': 0,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"32 - Leistungsträger der beruflichen Reha-Phase  (Abgerechnete Tage auf der Basis einer 7 Tage Woche,  ohne Unterbrechungen)",
    'fieldname': u"f32",
    'typ': 'multi_int',
    'allowance': [
      u"01 - DRV Regional",
      u"02 - DRV Bund",
      u"03 - DRV Knappschaft / Bahn / See", 
      u"04 - Sonderkassen (Landwirte u.a.)", 
      u"05 - Agentur für Arbeit", 
      u"06 - Berufsgenossenschaft", 
      u"08 - Privatversicherung, Beihilfe, Selbstzahler", 
      u"11 - Sonstiges"
    ],
    'default': 0,
    'appears': ('capture', 'tabulation', 'documentation')
  },      
  {
    'title': u"32.1 - Art der beruflichen Reha-Maßnahme ",
    'fieldname': u"f32_1",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - berufliche Reha innerhalb der RPK",
      u"04 - berufliche Reha extern / WfbM",
      u"05 - berufliche Reha extern / Sonstiges"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"33 - Durchführung der Reha-Maßnahme  ",
    'fieldname': u"f33",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - nur stationär",
      u"02 - nur ganztägig Ambulant",
      u"03 - Wechsel: stationär nach ganztägig Ambulant",
      u"04 - Wechsel: ganztägig ambulant nach stationär"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"34 - Beendigung der RPK- Maßnahme gemäß fortgeschriebenen Reha-Plan    (Nicht gemäß Kostenzusage!)  ",
    'fieldname': u"f34",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - planmäßig gemäß Reha-Plan beendet"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"35 - Erreichtes Reha-Ziel gemäß Reha-Plan   (qualitative Einschätzung am Ende  der Maßnahme im Abgleich zum fortgeschriebenen Reha-Plan)   ",
    'fieldname': u"f35",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - Reha-Ziel erreicht",
      u"02 - Reha-Ziel bedingt erreicht",
      u"03 - Reha-Ziel nicht erreicht"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"36 - Schwerbehindertenausweis (zum Zeitpunkt der Entlassung) ",
    'fieldname': u"f36",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ja ( 50% und mehr GdB)",
      u"02 - beantragt",
      u"03 - nein"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"37 - Rente / Rentenantrag (zum Zeitpunkt der Entlassung) ",
    'fieldname': u"f37",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - derzeit bereits Rentenbezug",
      # u"02 - Rentenantrag gestellt/Empfehlung volle Erwerbsminderungsrente",
      # u"03 - Rentenantrag nicht gestellt",
      # u"04 - Rentenantrag gestellt/Empfehlung Teilerwerbsminderungsrente",
      u"02 - Rentenantrag gest./Empf. volle Erwerbsminderungsrente",
      u"03 - Rentenantrag nicht gestellt",
      u"04 - Rentenantrag gest./Empf. Teilerwerbsminderungsrente",
      u"05 - Rentenbezug Teilerwerbsminderungsrente"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"38 - Gesetzliche Betreuung (zum Zeitpunkt der Entlassung) ",
    'fieldname': u"f38",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - ja",
      u"02 - beantragt",
      u"03 - nein"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"39 - Entfernung vom Wohnort zur RPK (zum Zeitpunkt der Entlassung) (laut Routenplaner) ",
    'fieldname': u"f39",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - bis 20 km Umkreis",
      u"02 - bis 50 km Umkreis",
      u"03 - bis 100 km Umkreis",
      u"04 - über 100 km Umkreis"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'typ': 'pagebreak',
    'allowance': None,
    'appears': ('documentation')
  },                                                       
  {
    'title': u"Einschätzung /Empfehlung nach Beendigung der RPK-Maßnahme",
    'typ': 'heading',
    'allowance': None,
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"40 - Behandlung/Betreuung nach der RPK-Maßnahme   (Mehrfachnennungen möglich)  ",
    'fieldname': u"f40",
    'typ': 'multi_bool',
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - stationäre psychiatrische Behandlung",
      u"02 - teilstationäre Behandlung (Tagesklinik)",
      u"03 - Psychiatrische Ambulanz/Poliklinik",
      u"04 - niedergelassener Facharzt für Psychiatrie",
      u"05 - Hausarzt",
      u"06 - niedergelassener Psychotherapeut",
      u"07 - Sozialpsychiatrischer Dienst",
      u"08 - Psychosozialer Dienst / Berufsbegleitender Dienst / IFD",
      u"09 - Tagesstätte / ambulante Ergotherapie",
      u"10 - Beratungsstelle",
      u"11 - Selbsthilfegruppe",
      u"12 - keine",
      u"13 - Sonstiges"
    ],
    'default': False,
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"41 - Erwerbs- und Ausbildungssituation   (Situation nach Beendigung  der RPK-Maßnahme)      ",
    'fieldname': u"f41",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - allgemeiner Arbeitsmarkt - Vollzeit",
      u"02 - allgemeiner Arbeitsmarkt - Teilzeit",
      u"03 - Selbsthilfe/Integrationsbetrieb - Vollzeit",
      u"04 - Selbsthilfe/Integrationsbetrieb - Teilzeit",
      u"05 - WfbM Arbeitsbereich",
      u"06 - Hinzuverdienst / Gelegenheitsarbeiten",
      u"07 - Schüler",
      u"08 - Ausbildung (betrieblich)",
      u"09 - Ausbildung (BBW)",
      u"10 - Umschulung (betrieblich)",
      u"11 - Umschulung (BFW)",
      u"12 - Studium",
      u"13 - sonst. berufsfördernde Maßnahme (z.B. BvB)",
      u"14 - WfbM Berufsbildungsbereich",
      u"16 - Erwerbsfähig und ohne Beschäftigung",
      u"17 - Erwerbsgemindert und ohne Beschäftigung",
      u"18 - Hausfrau/Hausmann"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"41.1 - Erwerbsfähigkeit nach Rentenrecht   (Situation nach Beendigung der RPK-Maßnahme)     ",
    'fieldname': u"f41_1",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - unter drei Stunden",
      u"02 - bis 6 Stunden",
      u"03 - vollschichtig",
      u"04 - vollschichtig 2. Arbeitsmarkt (z.B. WfbM)"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"43 - Lebensverhältnisse (Einschätzung nach Beendigung der RPK-Maßnahme) ",
    'fieldname': u"f43",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - lebt allein",
      u"02 - mit Ehe-(Partner)",
      u"03 - bei den Eltern / Elternteil",
      u"04 - bei Verwandten / Bekannten",
      u"05 - betreutes Wohnen",
      u"06 - Leben innerhalb einer Einrichtung",
      u"07 - alleinerziehend"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"44 - Wohnsituation (Einschätzung nach Beendigung   der RPK-Maßnahme) ",
    'fieldname': u"f44",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - Eigene Wohnung",
      u"02 - Wohnung im elterlichen Haus",
      u"03 - Zimmer in elterlichen Wohnung/elterliches Haus",
      u"04 - Wohngemeinschaft",
      u"05 - Leben in einer Einrichtung",
      u"06 - ohne festen Wohnsitz"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  }, 
  {
    'title': u"45 - Überwiegender Lebensunterhalt (Einschätzung nach Beendigung der RPK-Maßnahme) ",
    'fieldname': u"f45",
    'typ': 'dropdown',
    'default': 0,
    'allowance': [ 
      u"00 - keine Angabe / nicht bekannt",
      u"01 - eigenenes Arbeitseinkommen",
      u"02 - finanzielle Unterstützung durch Angehörige",
      u"03 - Krankengeld",
      u"04 - Übergangsgeld",
      u"05 - Arbeitslosengeld I",
      u"06 - Arbeitslosengeld II",
      u"07 - Sozialhilfe / Grundsicherung",
      u"08 - Ausbildungsbeihilfe",
      u"09 - BU/EU/Unfall/Erwerbsminderungsrente",
      u"10 - sonstiges Einkommen / Vermögen"
    ],
    'appears': ('capture', 'tabulation', 'documentation')
  },
  {
    'title': u"Datum und Name für die Endkontrolle:",
    'fieldname': CONFIG_SIGNER_NAME,
    'allowance': '',
    'typ': 'str',
    'default': '',
    'appears': ('tabulation',)
  }
])

if __name__ == '__main__':
    types = {}
    for field in structure:
        if not field['typ'] in types:
            types[field['typ']] = 0
        types[field['typ']] += 1
        if not 'typ' in field:
            print repr(field)
    print repr(types)
