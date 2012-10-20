==================================================
sphinx.recentpages:  Sphinx Recent Pages Extension
==================================================

This sphinx extension provides a new directive which displays recent updated files list.

.. contents::
   :depth: 2


Introduction
============

This sphinx extension provides a new directive which displays recent updated files list.
If you want to get all page list ordered by mtime, just put recentpages directive as follows:

::

  .. recentpages::


If you want to display recent 3 files only, add num option to the directive:
  
::

  .. recentpages::
      :num: 3

  

Install
=======

Put recentpages.py to your sphinx project and add 'recentpages' to extension list.
For example, if you put the file into source/_exts directory, add the following two lines into source/conf.py.

::

  sys.path.append(os.path.abspath('_exts'))
  extensions += ['recentpages']


Please note that recent updated pages list is not updated if you run 'make html' to build pages and you don't update the page which has the directive.
To update the list everytime, please use 'recentpageshtml' instead of 'html'.

::

  $ /usr/local/bin/sphinx-build -b recentpageshtml -d build/doctrees source build/recentpageshtml

If you want to run 'make recentpageshtml', please add the following lines to Makefile:
  
::

  recentpageshtml:
         $(SPHINXBUILD) -b recentpageshtml $(ALLSPHINXOPTS) $(BUILDDIR)/recentpageshtml
         @echo
         @echo "Build finished. The HTML page is in $(BUILDDIR)/recentpageshtml."

