==================================================
sphinx.recentpages:  Sphinx Recent Pages Generator
==================================================

This script generates 'Recent Pages' rst page for Sphinx sources.

.. contents::
   :depth: 2


Introduction
============

This script generates 'Recent Pages' rst page for Sphinx sources.
For example, if you modified file1.rst, file2.rst, and file3.rst in this order and then run this script, you'll get 'Recent Pages' file like this:

::

  .. _recentPages:

  ============
  Recent Pages
  ============

  * :doc:`file3`: 2012-04-15 21:36:30
  * :doc:`file2`: 2012-04-15 21:36:24
  * :doc:`file1`: 2012-04-15 21:36:15


Install
=======

You can choose the following two way to install sphinx.recentpages.

::

  $ pip install sphinx.recentpages-0.1.tar.gz

::

  $ easy_install sphinx.recentpages



Usage
=====
  
It's pretty easy to use this script.
Please just run ::

  $ recentpages [sphinx source directory] > recentpages.rst


Tips
====

How to update 'Recent Pages' page automatically?
------------------------------------------------

Put templates/OMakefile into the root directory of your sphinx project and then run the following command in background: ::

  $ omake -P --verbose  

How to put link to 'Recent Pages' on the top bar of generated html document?
----------------------------------------------------------------------------

Put templates/layout.html into source/_templates directory.
  


