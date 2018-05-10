#!/usr/bin/env python

import yaml

from Maestor import maestor

robot = maestor()

//Rename test.yaml to your YAML file
with open('test.yaml', 'r') as f:
    doc = yaml.load(f)

joints = ' '.join(doc['gesture'])
positions = [doc['gesture'][i] for i in doc['gesture']]
strPositions = ' '.join([str(i) for i in positions])

robot.setProperties(joints, ' '.join(len(doc['gesture']) * ['position']), strPositions)
