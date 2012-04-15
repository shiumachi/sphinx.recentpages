# -*- coding: utf-8 -*-
from sphinx.recentpages import RecentPages
from test.sphinx.Constants import Constants
from nose.tools import *
import unittest
import sys
import os


class TestRecentPages(unittest.TestCase):
    target_dir = Constants.TEST_ROOT_DIR

    def testGetSortedFileListWithMtime(self):
        expected = [
            (self.target_dir + "/test001", int(os.stat(self.target_dir + "/test001").st_mtime)),
            (self.target_dir + "/test002", int(os.stat(self.target_dir + "/test002").st_mtime)),
            (self.target_dir + "/test003", int(os.stat(self.target_dir + "/test003").st_mtime)),
            (self.target_dir + "/dir01/test004", int(os.stat(self.target_dir + "/dir01/test004").st_mtime)),
            (self.target_dir + "/dir02/dir03/test005", int(os.stat(self.target_dir + "/dir02/dir03/test005").st_mtime)),
            (self.target_dir + "/test006", int(os.stat(self.target_dir + "/test006").st_mtime)),
            ]
        assert expected == RecentPages.getSortedFileListWithMtime(self.target_dir)

    def testMain(self):
        RecentPages.main()
        assert 1 == 1 

