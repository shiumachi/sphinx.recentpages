# -*- coding: utf-8 -*-
from sphinx.recentpages import RecentPages
from test.sphinx.Constants import Constants
from nose.tools import *
import unittest
import sys
import os


class TestRecentPages(unittest.TestCase):
    target_dir = Constants.TEST_ROOT_DIR

    def testGetFileListOrderedByMtime(self):
        expected = [
            (self.target_dir + "/test001", int(os.stat(self.target_dir + "/test001").st_mtime)),
            (self.target_dir + "/test002", int(os.stat(self.target_dir + "/test002").st_mtime)),
            (self.target_dir + "/test003", int(os.stat(self.target_dir + "/test003").st_mtime)),
            (self.target_dir + "/dir01/test004", int(os.stat(self.target_dir + "/dir01/test004").st_mtime)),
            (self.target_dir + "/dir02/dir03/test005", int(os.stat(self.target_dir + "/dir02/dir03/test005").st_mtime)),
            (self.target_dir + "/test006", int(os.stat(self.target_dir + "/test006").st_mtime)),
            ]
        res = RecentPages.getFileListOrderedByMtime(self.target_dir)
        l = len(res)
        for i in xrange(0, l):
            assert expected[i][0] == res[i].getAbsolutePath()
            assert expected[i][1] == res[i].getMtime()

    def testGenerate(self):
        expected = ".. _recentPages:\n============\nRecent Pages\n============\n\n* :doc:`test001`: 2012-04-15 20:43:48\n* :doc:`test002`: 2012-04-15 20:43:53\n* :doc:`test003`: 2012-04-15 20:45:37\n* :doc:`dir01/test004`: 2012-04-15 21:36:15\n* :doc:`dir02/dir03/test005`: 2012-04-15 21:36:24\n* :doc:`test006`: 2012-04-15 21:36:30\n"
        res = RecentPages.generate(self.target_dir)
        assert expected == res


    def testMain(self):
        RecentPages.main(['', self.target_dir])
        assert 1 == 1 

