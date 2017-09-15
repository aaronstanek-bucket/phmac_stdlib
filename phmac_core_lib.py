from phmac_compiler import py_html_macro_node as node
from phmac_compiler import my_custom
from phmac_compiler import load as file_to_tree
import copy

def raw(inp):
    inp.ty = "t"
    inp.text = ""
    for x in inp.subs:
        x.ty = "t"
    return inp

my_custom.add("raw",raw)

def addString(b,s):
    w = s.encode("utf8")
    for x in w:
        b.append(x)

my_macros = dict()

def macro_recur(n,subs):
    if n.ty == "u":
        if n.tag=="inside":
            n.ty = "t"
            n.text = ""
            n.subs = subs
            return
    for x in n.subs:
        macro_recur(x,subs)

def macro_handler(inp):
    ou = node()
    ou.ty = "t"
    ou.text = ""
    ou.subs.append(copy.deepcopy(my_macros[inp.tag]))
    macro_recur(ou,inp.subs)
    return ou

def macro(inp):
    ou = node()
    ou.ty = "t"
    ou.text = ""
    my_macros[inp.subs[0].text] = copy.deepcopy(inp.subs[1])
    my_custom.add(inp.subs[0].text,macro_handler)
    return ou

my_custom.add("macro",macro)

def Import(inp):
    ou = node()
    ou.ty= "t"
    ou.text = ""
    for x in inp.subs:
        if x.text[-3:]==".js":
            p = node()
            p.ty = "b"
            p.tag = "script"
            p.args = "src=\""+x.text+"\""
            ou.subs.append(p)
        elif x.text[-4:]==".css":
            p = node()
            p.ty = "b"
            p.tag = "link"
            p.args = "rel=\"stylesheet\" type=\"text/css\" href=\""+x.text+"\""
            ou.subs.append(p)
        elif x.text[-6:]==".phmac":
            m = file_to_tree(inp.subs[0].text)
            ou.subs = m.subs
        elif x.text[-5:]==".html":
            infile = open(x.text,"r")
            ou.text = infile.read()
            infile.close()
        else:
            raise Exception("Import file, extension not recognized (.js .css .phmac .html  only): "+x.text)
    return ou

my_custom.add("import",Import)

def meta(inp):
    ou = node()
    ou.ty = "t"
    ou.text = ""
    p = node()
    p.ty = "b"
    p.tag = "meta"
    p.args = "charset=\"UTF-8\""
    ou.subs.append(p)
    try:
        for x in inp.subs:
            p = node()
            p.ty = "b"
            p.tag = "meta"
            p.args = "name=\""+x.text+"\" content=\""+x.subs[0].text+"\""
            ou.subs.append(p)
    except:
        raise Exception("Syntax error in custom meta tag.")
    return ou

my_custom.add("meta",meta)

def a_link(inp):
    ou = node()
    ou.ty = "b"
    ou.tag = "a"
    ou.args = "href=\""+inp.subs[1].text+"\""
    if inp.args!="":
        ou.args = inp.args+" "+ou.args
    ou.subs.append(inp.subs[0])
    return ou

my_custom.add("a",a_link)

def space(inp):
    inp.ty = "t"
    inp.text = " "
    return inp

my_custom.add("space",space)

def nothing(inp):
    inp.ty = "t"
    inp.text = ""
    return inp

my_custom.add("null",nothing)

def par(inp):
    sp_node = node()
    sp_node.ty = "t"
    sp_node.text = " "
    ou = node()
    ou.ty = "b"
    if inp.tag!="s":
        ou.tag = inp.tag
    else:
        ou.tag = "span"
    ou.args = inp.args
    for x in inp.subs:
        if (x.tag=="br") and (x.ty=="b"):
            ou.subs.append(x)
        elif x.tag=="s" and (x.ty=="u"):
            ou.subs.append(par(x))
        elif x.tag=="b" and (x.ty=="b"):
            ou.subs.append(par(x))
        elif x.tag=="<i" and (x.ty=="b"):
            ou.subs.append(par(x))
        else:
            ou.subs.append(x)
            ou.subs.append(sp_node)
    return ou

my_custom.add("p",par)
