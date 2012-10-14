# -*- coding: utf-8 -*-

from sphinx.util.compat import Directive
from docutils import nodes
import sys, os, datetime, stat

def setup(app):
    app.add_node(recentpages)

    app.add_directive('recentpages', RecentpagesDirective)
    app.connect('doctree-resolved', process_recentpages_nodes)
    app.connect('env-purge-doc', purge_recentpages)

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

def process_recentpages_nodes(app, doctree, fromdocname):
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

def purge_recentpages(app, env, docname):
    if not hasattr(env, 'recentpages_nodes'):
        return
    env.recentpages_nodes = [recentpages for recentpages in env.recentpages_nodes
                          if recentpages['docname'] != docname]
    pass

