import os, os.path, sqlite3, unittest

from loggingx.db.extract import run_extract
from loggingx.wef import WEFFormatter

class TestDatabaseExtract(unittest.TestCase):
    """ Test the DB logging extraction.
    """
    
    def testExtract(self):
        db = os.path.join(os.environ['TEMP'], 'pylogging.db')
        connection = sqlite3.connect(db)
        run_extract(connection, 0, WEFFormatter())
            
if __name__ == '__main__':
    unittest.main()
