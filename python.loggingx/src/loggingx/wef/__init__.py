"""
This module implements a logging formatter for emitting event records as
OASIS WEF (WSDM Event Format) Events. The log handlers and filters remain 
the same, this simply formats each log record as a WEF.
"""

import logging
import os
import platform
import sys
import time
import traceback
import uuid
from xml.sax.saxutils import XMLGenerator

_type_map = {type(1): 'xsd:int',
             type(1.0): 'xsd:float',
             type(1L): 'xsd:long',
             type(''): 'xsd:string',
             type(u''): 'xsd:string',
             type(True): 'xsd:boolean'}

_severity_map = {logging.FATAL: 6,
                 logging.ERROR: 4,
                 logging.WARNING: 2,
                 logging.INFO: 1,
                 logging.DEBUG: 1,
                 logging.NOTSET: 0}

_component_map = {}

VERSION_WEF_1 = '1.1'

REPORTER_ID = 'urn:uuid:e0b7f6ae-bc80-11db-990f-0014a4dafba5'

class WEFFormatter(logging.Formatter):
    """
    This class implements the standard logging Formatter class and
    provides a formatting of messages according to the OASIS WEF Event 
    Format. 
    """
    def __init__(self, version=VERSION_WEF_1):
        """ 
        Initializes the formatter, note that it is not possible to reset
        the format string as in the base class, to format a WEF the shape
        must be conformed to.
        """
        logging.Formatter.__init__(self, '')
        self.version = version

    def _extendedElement(self, doc, name, value, children={}):
        """ 
        Add extended data elements. 
        """
        doc.startElement('extendedDataElements',
                         {'name': name,
                          'type': _type_map[type(value)]})
        doc.startElement('values', {})
        doc.characters(str(value))
        doc.endElement('values')
        for _name, _value in children.items():
            doc.startElement('children',
                             {'name': _name,
                              'type': _type_map[type(value)]})
            doc.startElement('values', {})
            doc.characters(str(_value))
            doc.endElement('values')
            doc.endElement('children')
        doc.endElement('extendedDataElements')

    def _exception(self, doc, exc_info):
        """ 
        Format an exception record, this adds extended data elements. 
        """
        if isinstance(exc_info[0], type('')):
            tbl = exc_info[2]
            exc_name = exc_info[0]
            exc_msg = exc_info[1]
        else:
            tbl = traceback.extract_tb(exc_info[2])
            exc_name = exc_info[0].__name__
            exc_msg = str(exc_info[1].message)
        for tb in tbl:
            tbs = 'File: %s, Line: %d' % (tb[0], tb[1]) 
        self._extendedElement(doc, 
                              'Exception', exc_msg, 
                              {'Type': exc_name,
                               'Traceback': tbs})

    def format(self, record):
        """ 
        Format a log record as a WEF and return as a string.
        """
        # Note that the standard formatTime() only gives us time zones as 
        # text names, we need the TZ value as a +- hours.
        record.asctime = self.formatTime(record, '%Y-%m-%dT%H:%M:%SZ')
        record.asctime = record.asctime + '%+03d00' % (time.timezone / 3600)
        import StringIO
        stream = StringIO.StringIO()
        doc = XMLGenerator(stream)
        # We don't do this because this way we can stream one event after 
        # another, the inclusion of processing elements stops this.
        #doc.startDocument()
        doc.startElement('ManagementEvent', 
                         {'ReportTime': str(record.asctime),
                          'xmlns': 'http://docs.oasis-open.org/wsdm/muws1-2.xsd',
                          'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'})
        doc.startPrefixMapping('', 'http://docs.oasis-open.org/wsdm/muws1-2.xsd')
        doc.startPrefixMapping('xsd', 'http://www.w3.org/2001/XMLSchema')
        doc.startElement('EventId', {})
        doc.characters('urn:uuid:' + str(uuid.uuid1()))
        doc.endElement('EventId')
        doc.startElement('SourceComponent',
                         {'application': sys.executable, 
                          'component': record.module, 
                          'componentIdType': 'Module', 
                          'location': record.pathname, 
                          'locationType': 'path',
                          'componentType': 'Module',
                          'processId': str(record.process),
                          'threadId': str(record.thread)})
        doc.endElement('SourceComponent')
        doc.startElement('ReporterComponent', 
                         {'component': 'logging',
                          'componentIdType': 'Module',
                          'location': platform.node(),
                          'executionEnvironment': sys.platform,
                          'locationType': 'Hostname',
                          'subComponent': 'WEFFormatter',
                          'componentType': 'Module'})
        doc.endElement('ReporterComponent')
        doc.startElement('Situation', {})
        doc.startElement('SituationCategory', {})
        doc.startElement('ReportSituation', {})
        doc.startElement('Log', {})
        doc.endElement('Log')
        doc.endElement('ReportSituation')
        doc.endElement('SituationCategory')
        doc.startElement('SituationTime', {})
        doc.characters(str(record.asctime))
        doc.endElement('SituationTime')
        doc.startElement('Priority', {})
        doc.characters(str(50))
        doc.endElement('Priority')
        doc.startElement('Severity', {})
        doc.characters(str(_severity_map[record.levelno]))
        doc.endElement('Severity')
        doc.startElement('Message', {})
        doc.characters(record.getMessage())
        doc.endElement('Message')
        doc.endElement('Situation')
        doc.startElement('extendedContent', {})
        self._extendedElement(doc, 'Line', record.lineno)
        if record.exc_info:
            self._exception(doc, record.exc_info)
        doc.endElement('extendedContent')
        doc.endPrefixMapping('')
        doc.endPrefixMapping('xsd')
        doc.endElement('ManagementEvent')
        doc.endDocument()
        xml = stream.getvalue()
        stream.close()
        return xml
        
    def formatException(self, exc_info):
        """ 
        We ignore this. 
        """
        pass
