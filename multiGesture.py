#!/usr/bin/env python

import yaml

import sys

from Maestor import maestor

from math import pi

robot = maestor()

fname = sys.argv[1]
with open(fname, 'r') as f:
    doc = yaml.load(f)

convertFac = 1
for names in doc:
    if names == 'units':
        if doc[names] == 'deg':
            convertFac = pi / 180

for names in doc['run']:
    joints = ' '.join(doc[names])
    positions = [(doc[names][i] * convertFac) for i in doc[names]]
    strPositions = ' '.join([str(i) for i in positions])
    robot.setProperties(joints, ' '.join(len(doc[names]) * ['position']), strPositions)
