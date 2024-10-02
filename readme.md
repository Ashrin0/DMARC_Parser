# DMARC Parser

v0.1 - Initial build.  Parses an XML file from DMARC updates and reports all elements.
v0.2 - Added support for .gz and .zip compressed XMLs.  Default is now to show only reject elements.

## TODO
- Confirm all xml elements are being parsed
- Save elements to an sql database.  Maybe mySql, probably SQLite
- Confirm parsed xml files are not already in the db
- Grab new xml files via IMAP from the email