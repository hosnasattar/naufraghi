#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sys.path.append("../")

from bplnn import *

def load_data(filename):
    trace("Loading '%s'" % filename)
    data = []
    for line in open(filename).readlines():
        row = map(int, line.split(","))
        stroke, number = row[:-1], row[-1]
        # normalize inputs
        inputs = [float(i)/100 for i in stroke]
        # digitalize outputs
        targets = [int(i == number) for i in range(10)]
        data.append([inputs, targets])
    print stats(data)
    print "-"*70
    return data

def run():
    trace("PenDigits dataset", "#")
    patterns = load_data("pendigits.tra")
    n_in = len(patterns[0][0])
    n_out = len(patterns[0][1])
    net = DeepNetwork([n_in, (n_in+n_out)/2, n_out], auto_mode="step")
    for i in range(10):
        net.prepare(patterns, 1000, 0.05)
    #print net.dump()
    print net
    test_patterns = load_data("pendigits.tes")
    net.test(test_patterns)



if __name__=="__main__":
    run()
