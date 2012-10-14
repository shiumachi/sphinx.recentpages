# -*- coding: utf-8 -*-

from sphinx.util.compat import Directive
from sphinx.builders.html import StandaloneHTMLBuilder
from docutils import nodes

from os import path
import sys, os, datetime, stat, re

try:
    from hashlib import md5
except ImportError:
    # 2.4 compatibility
    from md5 import md5

def setup(app):
    app.add_node(recentpages)

    app.add_directive('recentpages', RecentpagesDirective)
    app.connect('doctree-resolved', process_recentpages_nodes)

    app.add_builder(RecentpagesHTMLBuilder)

class recentpages(nodes.General, nodes.Element):
    pass

class RecentpagesDirective(Directive):
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
        content = generate_content2(file_list, num)
        node.replace_self(content)

def generate_content2(file_list, num=-1):
    content = []
    n = len(file_list) if num < 0 else num

    for docname, mtime in file_list:
        line = "%s: %s" % (docname, mtime)
        content.append(nodes.Text(line, line))
        content.append(nodes.paragraph())
        n -= 1
        if n <= 0: break        

    return content
            
            
def get_file_list_ordered_by_mtime(env):
    """get sorted file lists in specified directory.

    Args:
    env: app.env

    Returns:
    list of files ordered by mtime.
    """
    
    res = []
    
    for docname in env.found_docs:
        abspath = env.doc2path(docname)
        mtime = os.path.getmtime(abspath)
        res.append((docname,mtime))

    res = list(set(res))
    res.sort(cmp=lambda x,y: cmp(x[1], y[1]), reverse=True)

    # convert to readable date format
    res = map(lambda x: (x[0], datetime.datetime.fromtimestamp(x[1])), res)
    
    return res

class RecentpagesHTMLBuilder(StandaloneHTMLBuilder):
    """
    """
    name = 'recentpageshtml'

    def get_outdated_docs(self):
        cfgdict = dict((name, self.config[name])
                       for (name, desc) in self.config.values.iteritems()
                       if desc[1] == 'recentpageshtml')
        self.config_hash = md5(unicode(cfgdict).encode('utf-8')).hexdigest()
        self.tags_hash = md5(unicode(sorted(self.tags)).encode('utf-8')) \
                .hexdigest()
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
            pass

        if old_config_hash != self.config_hash or \
               old_tags_hash != self.tags_hash:
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
                if srcmtime > targetmtime or self.has_recentpages(docname):
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    recentpages_directive_pattern = re.compile('\.\. recentpages::')
            
    def has_recentpages(self, docname):
        path = self.env.doc2path(docname)
        file = open(path)
        for line in file:
            if self.recentpages_directive_pattern.match(line):
                return True

        return False
            

        
