rpk-teilnehmerbogen
===================
Für die Erfassung der Daten zur jährlichen Meldung wie in [Summenbögen BAG-RPK 2011.xls](http://www.bagrpk.de/fileadmin/webseite/Downloads/Formulare/Summenb%F6gen%20BAG-RPK%202011.xls)

Status: Erst in Teilen funktionstüchtig. Struktur der Daten bis auf weiteres ungeklärt. Generierte Dokumentation zur Struktur und diesbezüglicher Möglichkeiten in [Tech-Dok.pdf](https://raw.github.com/the-lo-ni-us/rpk-teilnehmerbogen/develop/Doku/Tech-Dok.pdf)

Voraussetzungen:

* Python 2.7
* PyQt4 >= 4.8
* sqlalchemy >= 0.7.9
* savReaderWriter >= 3.2.1
* reportlab >= 2.6
* ggf. psycopg2

Speichert die Daten in einer Sqlite-Datenbank oder auf einem Postgresql-Server.