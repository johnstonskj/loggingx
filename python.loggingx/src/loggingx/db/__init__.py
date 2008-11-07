"""
This module implements a logging handler for emitting event records to
a database as individual records in a pre-defined table. The handler is
able to select different database providers although is pre-configured
to use the SQLite3 module (part of the 2.5 standard library).

Classes:
   DatabaseError - Exception raised on database errors.
   DatabaseHandler - The logging handler itself.
"""

import logging, os, os.path, traceback
import cPickle

# The default database identifier for SQLite3
DEF_DB = '/tmp'
try:
    DEF_DB = os.path.join(os.environ['TMP'], 'pylogging.db')
except KeyError:
    DEF_DB = os.path.join(os.environ.get('TEMP', '/temp'), 'pylogging.db')

# The default table name.
DEF_TABLE_NAME = 'python_logger'

# The default table structure.
DEF_TABLE_CREATE = """
create table %s (
    record_id integer not null primary key autoincrement,
    name varchar(30) not null,
    levelno int not null,
    created datetime not null,
    msecs integer not null,
    process integer not null,
    thread inteher not null,
    threadname varchar(120) null,
    levelname varchar(30) null,
    pathname varchar(120) null,
    filename varchar(120) null,
    module varchar(120) null,
    funcname varchar(120) null,
    lineno integer null,
    message text null,
    extended text null
)
""" % DEF_TABLE_NAME

# Standard keys for the event record.
STD_KEYS = ['name', 'levelno', 'created', 'msecs', 'process', 'thread', 'threadName',
            'levelname', 'pathname', 'filename', 'module', 'funcName', 'lineno',
            'msg', 'message', 'args']

class DatabaseError(Exception):
    """ This event is raised when exceptions occur during connection to, or
        configuration of the logging database.
    """
    pass

class DatabaseHandler(logging.Handler):
    """ A Database log-file handler, this will store log records in a table
        using the standard DBAPI. The table will be created during the construction
        of the handler instance - this has no effect if the table exists already.
        The use of the module-level lock is only used during this constructor to 
        create a connection, writes use the per-instance lock.
    """
    def __init__(self, level=logging.NOTSET, module='sqlite3', database=DEF_DB, **db_kwds):
        """ 
        Initialize the logger, including opening the database connection. 
        level - the event level to log
        module - the name of a database API module to load.
        database - the database name to provide to the connect() call.
        db_kwds - additional parameters for the connect() call.
        """
        logging.Handler.__init__(self, level)
        logging._acquireLock()
        try:
            dbapi = __import__(module)
            self.db_conn = dbapi.connect(database, **db_kwds)
            cursor = self.db_conn.cursor()
        except:
            raise DatabaseError, \
                  'Could not connect to database %s (module %s)' % \
                  (database, module)
        else:
            try:
                cursor.execute(DEF_TABLE_CREATE)
                self.db_conn.commit()
            except:
                pass # No report required, we assume the table already exists
            else:
                cursor.close()
        logging._releaseLock()
        
    def setFormatter(self, fmt):
        """ Note that this will ignore any formatters. """
        pass
    
    def emit(self, record):
        """ Write log record to the database. """
        cursor = self.db_conn.cursor()
        
        try:
            extended = {}
            for key in record.__dict__.keys():
                if key not in STD_KEYS:
                    if key == 'exc_info':
                        if record.exc_info:
                            extended[key] = (record.exc_info[0].__name__,
                                             record.exc_info[1].message,
                                             traceback.extract_tb(record.exc_info[2]))
                    else:
                        extended[key] = record.__dict__[key]
            extended_str = cPickle.dumps(extended, 0)
            cursor.execute('insert into %s values (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' % DEF_TABLE_NAME, 
                           (record.name,       record.levelno,   record.created,
                            record.msecs,      record.process,   record.thread, 
                            record.threadName, record.levelname, record.pathname,
                            record.filename,   record.module,    record.funcName,
                            record.lineno,     record.msg,       extended_str))
            self.db_conn.commit()
        except Exception:
            self.handleError(record)
        else:
            cursor.close()
            emitted = True

    def close(self):
        """ Close connection to the database. """
        logging.Handler.close(self)
        self.db_conn.close()
