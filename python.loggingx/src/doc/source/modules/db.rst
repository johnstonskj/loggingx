:mod:`loggingx.db` -- Log to a database
=======================================

.. automodule:: loggingx.db


Constants
---------

.. data:: DEF_DB

   The default path and name to the database to log to.
   
.. data:: DEF_TABLE_NAME

   The default name of the SQL table to use in the database.
   
.. data:: DEF_TABLE_CREATE

   The default SQL CREATE TABLE statement to use to create the log table
   in the database.
   
Classes
-------

.. autoexception:: loggingx.db.DatabaseError

.. autoclass:: loggingx.db.DatabaseHandler
   :members:
