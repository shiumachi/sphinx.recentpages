# -*- coding: utf-8 -*-
"""
    sphinx.recentpages
    ~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""

import os

class RecentPages(object):

    @classmethod
    def getSortedFileListWithMtime(self, target_dir):
        """get sorted file lists in specified directory.

        Args:
        target_dir: target directory to get all file lists.

        Returns:
        list of files ordered by mtime.
        """
        
        res = []
        
        fileList = self._walk(target_dir)        
        for file in fileList:
            res.append((file, int(os.stat(file).st_mtime)))
                       
        res.sort(cmp=lambda x,y: cmp(x[1],y[1]))
        return res

    @classmethod
    def _walk(self, dir):
        res = []
        if dir == "": return res
        for w in os.walk(dir):
            rel_path, dir_list, file_list = w
            for f in file_list:
                res.append(rel_path + "/" + f)
            for d in dir_list:
                res += self._walk(d)
        return res
            

        
        
    
    @classmethod
    def main(self):
        """main method
        """
        print "test"


if __name__=='__main__':
    RecentPages.main()
