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
    ou = node()
    ou.ty = "t"
    ou.text = ""
    tab = node()
    ou.subs.append(tab)
    tab.ty = "u"
    tab.tag = "table"
    tab.args = inp.args
    tab.subs.append(node())
    tab.subs[0].ty = "t"
    tab.subs[0].text = "centered"
    tab.subs.append(node())
    tab.subs[1].ty = "t"
    tab.subs[1].text = "args"
    w = str(int(float(100)/float(len(inp.subs))))+"%"
    rep = node()
    rep.ty = "t"
    rep.text = "width=\""+w+"\""
    for i in range(len(inp.subs)):
        j_node = node()
        j_node.ty = "t"
        j_node.text = str(i)
        j_node.subs.append(rep)
        tab.subs[1].subs.append(j_node)
        del(j_node)
    del(rep)
    del(w)
    tab.subs.append(node())
    tab.subs[2].ty = "t"
    tab.subs[2].text = "row0"
    for i in range(len(inp.subs)):
        a_node = node()
        a_node.ty = "u"
        a_node.tag = "a"
        a_node.subs.append(inp.subs[i])
        a_node.subs.append(inp.subs[i].subs[0])
        a_node.subs[0].subs = []
        a_node.subs[1].subs = []
        tab.subs[2].subs.append(a_node)
        del(a_node)
    return ou

my_custom.add("hmenu",hmenu)
