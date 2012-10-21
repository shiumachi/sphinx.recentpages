# -*- coding: utf-8 -*-
"""
    sphinxcontrib.recentpages
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Build recent update pages list.

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""

from sphinx.util.compat import Directive
from docutils import nodes

import os
import datetime
import re


def visit_html_recentpages(self, node):
    env = self.builder.env
    file_list = get_file_list_ordered_by_mtime(env)

    num = node['num']
    n = len(file_list) if num < 0 else num

    for docname, mtime, title in file_list:
        self.body.append('<a href="%s.html">' % docname)
        self.body.append('%s' % (title,))
        self.body.append('</a>: %s<br />' % (mtime,))
        n -= 1
        if n <= 0:
            break
    raise nodes.SkipNode


def depart_recentpages(self, node):
    pass


def setup(app):
    app.add_node(recentpages,
                 html=(visit_html_recentpages, depart_recentpages))

    app.add_directive('recentpages', RecentpagesDirective)


class recentpages(nodes.General, nodes.Element):
    """Node for recentpages extention.
    """
    pass


class RecentpagesDirective(Directive):
    """
    Directive to display recent update pages list.
    """

    has_content = True
    option_spec = {
        'num': int
    }

    def run(self):
        env = self.state.document.settings.env
        env.note_reread()

        num = self.options.get('num', -1)
        res = recentpages('')
        res['num'] = num
        return [res]


explicit_title_re = re.compile(r'^<(.*?)>(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)


def get_file_list_ordered_by_mtime(env):
    res = []

    for docname in env.found_docs:
        abspath = env.doc2path(docname)
        mtime = os.path.getmtime(abspath)
        title = env.titles[docname]
        m = explicit_title_re.match(unicode(title))
        if m:
            title = m.group(2)
        else:
            title = None
        res.append((docname, mtime, title))

    res = list(set(res))
    res.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)

    # convert to readable date format
    res = map(lambda x: (x[0], datetime.datetime.fromtimestamp(x[1]), x[2]),
              res)

    return res


