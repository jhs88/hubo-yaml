#!/usr/bin/env python

import yaml

import sys

from Maestor import maestor

from math import pi

robot = maestor()

fname = sys.argv[1]
with open(fname', 'r') as f:
    doc = yaml.load(f)

convertFac = 1
for names in doc:
    if names == 'units':
        if doc[names] == 'deg':
            convertFac = pi / 180

joints = ' '.join(doc['gesture'])
positions = [(doc['gesture'][i] * convertFac) for i in doc['gesture']]
strPositions = ' '.join([str(i) for i in positions])

robot.setProperties(joints, ' '.join(len(doc['gesture']) * ['position']), strPositions)
