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

    def testMain(self):
        RecentPages.main()
        assert 1 == 1 

