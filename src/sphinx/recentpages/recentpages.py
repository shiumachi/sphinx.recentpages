#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sphinx.recentpages.recentpages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""

from sphinx.recentpages.util.file import File
import sys
import os
import datetime
import stat

class RecentPages(object):

    @classmethod
    def generate(self, target_dir):
        rst = ""
        rst += self._getHeader()
        fileList = self.getFileListOrderedByMtime(target_dir)
        rst += self._getRstFileLists(fileList, target_dir)
        return rst

    @classmethod
    def _getHeader(self):
        header = """.. _recentPages:

============
Recent Pages
============

"""
        return header

    @classmethod
    def _getRstFileLists(self, fileList, target_dir):
        res = ""
        for file in fileList:
            s = "* :doc:`%s`: %s\n" % (file.getRelativePathRoot(target_dir), datetime.datetime.fromtimestamp(file.getMtime()))
            res += s

        return res
            

    @classmethod
    def getFileListOrderedByMtime(self, target_dir):
        """get sorted file lists in specified directory.

        Args:
        target_dir: target directory to get all file lists.

        Returns:
        list of files ordered by mtime.
        """
        
        res = []
        
        fileList = self._walk(target_dir)        
        for f in fileList:
            res.append(File(f))
            
        res.sort(cmp=lambda x,y: cmp(x.getMtime(), y.getMtime()), reverse=True)
        return res

    @classmethod
    def _walk(self, dir):
        res = []
        if dir == "": return res
        for w in os.walk(dir):
            rel_path, dir_list, file_list = w
            for f in file_list:
                if os.path.splitext(f)[1] != ".rst": continue
                if f == "recentpages.rst": continue
                res.append(rel_path + "/" + f)
            for d in dir_list:
                res += self._walk(d)
        return res        
            
    @classmethod
    def main(self,argv=None):        
        """main method
        """
        if argv is None:
            print "ERROR: directory must be specified"
        dir = argv[1]
        mode = os.stat(dir).st_mode
        if not stat.S_ISDIR(mode):
            print "ERROR: the argument is not a directory"            
        print self.generate(dir)


if __name__=='__main__':
    RecentPages.main(sys.argv)
