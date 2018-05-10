#!/usr/bin/env python

import yaml

from Maestor import maestor

robot = maestor()

import yaml
//Rename test.yaml to your YAML file
with open('test.yaml', 'r') as f:
    doc = yaml.load(f)

for names in doc['run']:
    joints = ' '.join(doc[names])
    positions = [doc[names][i] for i in doc[names]]
    strPositions = ' '.join([str(i) for i in positions])
    robot.setProperties(joints, ' '.join(len(doc[names]) * ['position']), strPositions)
