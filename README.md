# testlink-csv-import
Simple Python script to import Testlink test suites from csv from Word doc exported from Testlink

This is a very crude python script written in a manner of hours. Following the problem it solves

You have a Word doc which was exported from Testlink. This Word doc file contains a list of test suites with test cases. You have nothing else and you want to restore this information on a different/new Testlink server.

To use this script, follow these steps:

1. Copy everything except the Table contents hyperlinks to a spreadsheet app like LibreOffice, Google Sheets or Microsoft Excel.
2. Export the contents in a csv file
3. Clone this repository or just download the file named 'testlinkconverter.py'
4. Make the file 'testlinkconverter.py' executable
5. Make sure Python 2.7.x is installed in your system
6. Install [lxml](http://lxml.de/)
7. Run the script giving path of csv file as first argument. For example:
python testlinkconverter.py /path/to/csv/file > output.xml
8. A file will be generated named 'output.xml'. This file can be used to import test suites in testlink


Statutory warning: This is a crude script. There might be obvious bugs.
