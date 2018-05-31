#!/usr/bin/env python

import yaml
import sys
import re

from Maestor import maestor
from math import pi

robot = maestor()

class Gesture(object):
    def __init__(self, name=None, joints=None, positions=None, waits=None, conversion=1):
        self.NAME = name
        self.JOINTS = joints
        self.POSTIONS = positions
        self.WAITS = waits
        self.CONVERSION = conversion

    def getString(self):
        self.SETPROPSTR = "robot.setProperties(" \
        + ' '.join(joints) + ',' + ' '.join(len(joints) *  ['position']) + ',' \
        + ' '.join(str(i * self.CONVERSION) for i in self.POSTIONS) + ")"
        return self.SETPROPSTR

    def execute(self, robot):
        robot.setProperties(' '.join(self.JOINTS), ' '.join(len(self.JOINTS) * ['position']), ' '.join(str(i * self.CONVERSION) for i in self.POSTIONS))
        if self.WAITS != None:
            for joints in self.WAITS:
                robot.waitForJoint(joints)

def isJoint(tag):
    validTags = re.compile("[LR][SH][RPY]|[LR][KE]P|[LR]A[RP]|[LR]W[PY]|[LR][F][1-5]|WST|NKY|NK[12]")
    return filter(validTags.match, tag)

   # Add more functions in future
   # def isFunc(tag):
   #    vaildFunc = "waitFor|setVelocities"
   #    matchFunc = re.compile(validFunc)
   #    function = filter(validFunc.match, tag)
   #    return function

   # otherTags = !(validTags | validFunc)

def isWait(tag):
    matchWait = re.compile('waitFor')
    result = filter(matchWait.match, tag)
    if result != []:
        return tag['waitFor'].split(" ")
    else:
        return None

def parseYAML(dictionary):
    gestures = []
    for tags in dictionary:
        if tags == 'units' and dictionary[tags] == 'deg':
            conversion = pi / 180
        else:
            conversion = 1
    for names in dictionary['run']:
        name = names
        for tags in dictionary[name]:
            joints = isJoint(dictionary[name])
            positions = [dictionary[name][position] for position in joints]
            waits = isWait(dictionary[name])
        gestures.append(Gesture(name, joints, positions, waits, conversion))
    return gestures

def main():

    fname = sys.argv[1]
    with open(fname, 'r') as f:
        doc = yaml.load(f)

    for g in parseYAML(doc):
        g.execute(robot)

if __name__ == '__main__':
    main()
