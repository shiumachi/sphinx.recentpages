# -*- coding: utf-8 -*-
"""
    sphinx.recentpages
    ~~~~~~~~~~~~~~~~~~

    Build recent update pages list.

    :copyright: Copyright 2012 by Sho Shimauchi.
    :license: BSD, see LICENSE for details.
"""

from sphinx.util.compat import Directive
from sphinx.builders.html import StandaloneHTMLBuilder
from docutils import nodes

from os import path
import os
import datetime
import re

try:
    from hashlib import md5
except ImportError:
    # 2.4 compatibility
    from md5 import md5


def visit_html_recentpages(self, node):
    env = self.builder.env
    file_list = get_file_list_ordered_by_mtime(env)
    for docname, mtime in file_list:
        self.body.append('<a href="%s.html">' % docname)
        self.body.append('%s' % (docname,))
        self.body.append('</a>: %s<br />' % (mtime,))
    raise nodes.SkipNode

def depart_recentpages(self, node):
    pass

def setup(app):
    app.add_node(recentpages,
                 html=(visit_html_recentpages, depart_recentpages))

    app.add_directive('recentpages', RecentpagesDirective)
    # app.connect('doctree-resolved', process_recentpages_nodes)

    # app.add_builder(RecentpagesHTMLBuilder)


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
        num = self.options.get('num', -1)
        res = recentpages('')
        res['num'] = num
        return [res]


def process_recentpages_nodes(app, doctree, docname):
    env = app.builder.env

    para = nodes.paragraph()
    file_list = get_file_list_ordered_by_mtime(env)

    for node in doctree.traverse(recentpages):
        num = node['num']
        content = generate_content(file_list, num)
        node.replace_self(content)


def generate_content(file_list, num=-1):
    content = []
    n = len(file_list) if num < 0 else num

    for docname, mtime in file_list:
        line = "%s: %s" % (docname, mtime)
        content.append(nodes.Text(line, line))
        content.append(nodes.paragraph())
        n -= 1
        if n <= 0:
            break

    return content


def get_file_list_ordered_by_mtime(env):
    res = []

    for docname in env.found_docs:
        abspath = env.doc2path(docname)
        mtime = os.path.getmtime(abspath)
        res.append((docname, mtime))

    res = list(set(res))
    res.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)

    # convert to readable date format
    res = map(lambda x: (x[0], datetime.datetime.fromtimestamp(x[1])), res)

    return res


class RecentpagesHTMLBuilder(StandaloneHTMLBuilder):
    """
    HTMLBuilder for recentpages extension.
    This is almost same to StandaloneHTMLBuilder.
    All pages which contains recentpages directive
    are always marked as outdated.
    This is required because recent pages list always
    should be updated even if the page is not updated.
    """
    name = 'recentpageshtml'

    def get_outdated_docs(self):
        cfgdict = dict((name, self.config[name])
                       for (name, desc) in self.config.values.iteritems()
                       if desc[1] == 'recentpageshtml')
        self.config_hash = md5(unicode(cfgdict).encode('utf-8')).hexdigest()
        self.tags_hash = md5(unicode(
            sorted(self.tags)).encode('utf-8')).hexdigest()
        old_config_hash = old_tags_hash = ''
        try:
            fp = open(path.join(self.outdir, '.buildinfo'))
            try:
                version = fp.readline()
                if version.rstrip() != '# Sphinx build info version 1':
                    raise ValueError
                fp.readline()  # skip commentary
                cfg, old_config_hash = fp.readline().strip().split(': ')
                if cfg != 'config':
                    raise ValueError
                tag, old_tags_hash = fp.readline().strip().split(': ')
                if tag != 'tags':
                    raise ValueError
            finally:
                fp.close()
        except ValueError:
            self.warn('unsupported build info format in %r, building all' %
                      path.join(self.outdir, '.buildinfo'))
        except Exception as e:
            self.warn('Exception was thrown: %s', (e,))

        if (old_config_hash != self.config_hash
                or old_tags_hash != self.tags_hash):
            for docname in self.env.found_docs:
                yield docname
            return

        if self.templates:
            template_mtime = self.templates.newest_template_mtime()
        else:
            template_mtime = 0
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.get_outfilename(docname)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = max(path.getmtime(self.env.doc2path(docname)),
                               template_mtime)
                # this is the only part which is different
                # from StandaloneHTMLBuilder.
                if srcmtime > targetmtime or self.has_recentpages(docname):
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    recentpages_directive_pattern = re.compile(r'\.\. recentpages::')

    def has_recentpages(self, docname):
        docpath = self.env.doc2path(docname)
        with open(docpath) as files:
            for line in files:
                if self.recentpages_directive_pattern.match(line):
                    return True

        return False
