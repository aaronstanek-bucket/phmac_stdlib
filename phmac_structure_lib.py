from phmac_compiler import py_html_macro_node as node
from phmac_compiler import my_custom

def table(inp):
    centering = False
    args = dict()
    ou = node()
    ou.ty = "b"
    ou.tag = "table"
    ou.args = inp.args
    for row in inp.subs:
        if row.text=="args":
            for elem in row.subs:
                args[elem.text] = elem.subs[0].text
        elif row.text=="stop-args":
            for elem in row.subs:
                if elem.text=="all":
                    args = dict()
                elif elem.text in args:
                    del(args[elem.text])
        elif row.text=="centered":
            centering = True
        elif row.text=="stop-centered":
            centering = False
        else:
            p = node()
            p.ty = "b"
            p.tag = "tr"
            ou.subs.append(p)
            col_num = 0
            for elem in row.subs:
                q = node()
                q.ty = "b"
                q.tag = "td"
                s_col_num = str(col_num)
                if s_col_num in args:
                    q.args = args[s_col_num]
                p.subs.append(q)
                if centering:
                    r = node()
                    r.ty= "b"
                    r.tag = "center"
                    q.subs.append(r)
                    r.subs.append(elem)
                    del(r)
                else:
                    q.subs.append(elem)
                col_num = col_num+1
    return ou

my_custom.add("table",table)

def hmenu(inp):
    w = "width="+str(int(float(100)/float(len(inp.subs))))+"%"
    ou = node()
    ou.ty = "b"
    ou.tag = "table"
    ou.args = inp.args
    tr = node()
    tr.ty = "b"
    tr.tag = "tr"
    ou.subs.append(tr)
    for i in range(len(inp.subs)):
        td = node()
        td.ty = "b"
        td.tag = "td"
        td.args = w
        tr.subs.append(td)
        # p_node = node()
        # p_node.ty = "b"
        # p_node.tag = "p"
        # td.subs.append(p_node)
        a_node = node()
        a_node.ty = "b"
        a_node.tag = "a"
        a_node.args = "href=\""+inp.subs[i].subs[0].text+"\""
        td.subs.append(a_node)
        words = node()
        words.ty = "t"
        words.text = inp.subs[i].text
        a_node.subs.append(words)
    return ou

my_custom.add("hmenu",hmenu)
