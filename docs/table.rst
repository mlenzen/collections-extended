Table
=====

Goals
-----

Create a collection that has a simple, intuitive, pythonic interface.
Performance is a concern, but not the primary focus.

* Manipulating and building the data in the table must be easy to do and not require intermediate data structures.
* Importing and exporting to different formats should be dead simple.
* Aggregating column values should be as simple as `table.cols[2].sum()`
* Output to HTML, csv easily
* Be able to access rows using a primary key

Existing options
----------------

tablib
******

This is the closest match to what we're looking for. Eventually would like to reach feature parity.

What is tablib missing?
	- keys
		Want to access data rows via a column or set of columns that are the primary key. Tags exist, but they don't enforce uniqueness and aren't part of the data.
	- Row objects
		Want iterate over an object that can be accessed by both index and col name as a key. Currently have to zip both

pandas DataFrame
****************

Why not?
	- Complicated API
	- Would rather not depend on numpy.

sqllite in memory db
********************

Want a pythonic interface. Maybe use it as a backend?

pyTables_
*********

???


Similar questions
-----------------

https://stackoverflow.com/questions/1038160/data-structure-for-maintaining-tabular-data-in-memory


.. _pyTables: http://www.pytables.org/
