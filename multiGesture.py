#!/usr/bin/env python

import yaml
import sys
import re

from Maestor import maestor
from math import pi

robot = maestor()

def isJoint(tag): # tag is a String or list of Strings
    validTags= re.compile("[LR][SH][RPY]|[LR][KE]P|[LR]A[RP]|[LR]W[PY]|[LR][F][1-5]|WST|NKY|NK[12]")
    joint = filter(validTags.match, tag)
    return joint

def main():
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        doc = yaml.load(f)

    convertFac = 1
    for names in doc:
        if names == 'units' and doc[names] == 'deg':
            convertFac = pi / 180

    for names in doc['run']:
        jointArray = isJoint(doc[names])
        joints = ' '.join(jointArray)
        positions = [(doc[names][tag] * convertFac) for tag in jointArray]
        strPositions = ' '.join([str(tag) for tag in positions])
        robot.setProperties(joints, ' '.join(len(jointArray) * ['position']), strPositions)

if __name__ == '__main__':
    main()
