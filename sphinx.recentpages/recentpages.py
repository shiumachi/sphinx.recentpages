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
    out_list = generate_file_list('source')

    for node in doctree.traverse(recentpages):
        num = node['num']
        content = generate_content(out_list, num)
        node.replace_self(content)

def generate_file_list(target_dir):
    res = []    
    file_list = get_file_list_ordered_by_mtime(target_dir)    

    for path_and_mtime in file_list:
        res.append("%s: %s" % path_and_mtime)
    
    return res

def generate_content(out_list, num=-1):
    content = []
    n = len(out_list) if num < 0 else num

    for line in out_list:
        content.append(nodes.Text(line, line))
        content.append(nodes.paragraph())
        n -= 1
        if n <= 0: break        

    return content
            
def get_file_list_ordered_by_mtime(target_dir):
    """get sorted file lists in specified directory.

    Args:
    target_dir: target directory to get all file lists.

    Returns:
    list of files ordered by mtime.
    """
    
    res = []
    
    fileList = walk(target_dir)        
    for abspath in fileList:
        mtime = os.stat(abspath).st_mtime
        res.append((abspath,mtime))

    res = list(set(res))
    res.sort(cmp=lambda x,y: cmp(x[1], y[1]), reverse=True)

    # convert to readable date format
    res = map(lambda x: (x[0], datetime.datetime.fromtimestamp(x[1])), res)
    
    return res
    
def walk(dir):
    res = []
    if dir == "": return res
    for w in os.walk(dir):
        rel_path, dir_list, file_list = w
        for f in file_list:
            if os.path.splitext(f)[1] != ".rst": continue
            res.append(os.path.normpath(rel_path + "/" + f))
        for d in dir_list:
            res += walk(d)
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
            

        
