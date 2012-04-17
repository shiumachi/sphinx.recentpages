# -*- coding: utf-8 -*-
"""
    sphinx.recentpages.util.file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""

import os

class File(object):

    def __init__(self,abspath):
        self.absolutePath = abspath
        self.statResult = os.stat(abspath)

    def getAbsolutePath(self):
        return self.absolutePath

    def getMtime(self):
        return self.statResult.st_mtime

    def getRelativePath(self, start_dir):
        return os.path.relpath(self.absolutePath, start_dir)

    def getRelativePathRoot(self, start_dir):
        return os.path.splitext(os.path.relpath(self.absolutePath, start_dir))[0]