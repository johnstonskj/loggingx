"""
This module provides a simple function to extract records from a database
log created by the loggingx.db.DatabaseHandler and format them for reporting.
The function uses an already open database connection, an ID to start the
query from and standard Formatter and File objects.

Functions:
   run_extract - extract records from a database log and format.
"""

import cPickle, sys
from logging import makeLogRecord

def run_extract(connection, last_id, formatter, stream=sys.stdout):
    """ Extract records from a database log, from the given event ID
        and write them to a provided stream using the provided event
        formatter. This allows flexible reporting of the event log
        in the database.
        connect - a DBAPI connection object
        last_id - an integer id to select records from
        formatter - a logging Formatter object
        stream - a file-like object to write formatted records to
    """
    cursor = connection.cursor()
    cursor.execute('select * from python_logger where record_id > ?', (last_id,))
    stream.write('<ManagementEvents>')
    for row in cursor:
        record = {'name': row[1],       'levelno': row[2],   'created': row[3],
                  'msecs': row[4],      'process': row[5],   'thread': row[6],
                  'threadName': row[7], 'levelname': row[8], 'pathname': row[9],
                  'filename': row[10],  'module': row[11],   'funcName': row[12],
                  'lineno': row[13],    'msg': row[14],
                  }
        if row[15]:
            try:
                extra = cPickle.loads(str(row[15]))
                record.update(extra)
            except Exception, msg:
                print 'Exception: %s (in %s)' % (msg, row[15])
        stream.write(formatter.format(makeLogRecord(record)))
    stream.write('</ManagementEvents>')
    cursor.close()
    