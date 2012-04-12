# -*- coding: utf-8 -*-
from sphinx.recentpages import RecentPages
from nose.tools import *
import unittest
import sys

class TestRecentPages(unittest.TestCase):

    def testMain(self):
        RecentPages.main()
        assert 1 == 1 

