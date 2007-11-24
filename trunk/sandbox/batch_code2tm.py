#!/usr/bin/python -O

import os, sys, tmcolorizer, re, glob

frag_re = re.compile("(?:--|#)start \*(?P<frag>[^\*]+)\*(.*)(?:--|#)end \*(?P=frag)\*", re.S)

def get_frags_from_file(srcfile):
    code = file(srcfile, "r").read()
    return get_frags_from_txt(code)   
    
def get_frags_from_txt(code):
    frags, insides = [], []
    all = frag_re.findall(code) + [("",""),]
    if all:
        frags, insides = zip(*all)
    for icode in [i for i in insides if i != ""]:
        tmpfrags = get_frags_from_txt(icode)
        for ifrag in [i for i in tmpfrags if i != ""]:
            frags = frags + tmpfrags
#    frags = frags.append("")
    return frags

EXCLUDE_LIST = ["perceptron/pyml_perceptron.py",]
perceptron = [i for i in glob.glob("perceptron/*.py") if i not in EXCLUDE_LIST]

alberi = glob.glob("alberi/*.py")

filelist = glob.glob("*.py")

for srcfile in filelist:
    sys.stdout.write("Processing %s... " % srcfile)
    sys.stdout.flush()
    for frag in get_frags_from_file(srcfile):
        if frag:
            outname = srcfile + "." + frag.replace(" ","") + ".tm"
        else:
            outname = srcfile + ".tm"            
        try:
            if outname not in ["perceptron/perceptron.py.tm","perceptron/svg_paths.py.tm"]:
                tmsource = tmcolorizer.get_tmsource(srcfile, frag)
                tmfile = file("./tm/%s" % outname, "w+")
                tmfile.write(tmsource)
                tmfile.close()
            if __debug__:
                sys.stdout.write(".. %s\n" % frag)
                sys.stdout.flush()
        except tmcolorizer.EmptyFragmentError:
            pass
    sys.stdout.write("*** Done! ***\n")    
