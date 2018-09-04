#!/usr/bin/env python

import yaml
import sys
import re

from Maestor import maestor
from math import pi

robot = maestor()


class Gesture(object):
    def __init__(self, name=None, joints=None, positions=None, waits=None, conversion=1, velset=1):
        self.NAME = name
        self.JOINTS = joints
        self.POSTIONS = positions
        self.WAITS = waits
        self.CONVERSION = conversion
        self.VELSET = velset

    def getString(self):
        self.SETPROPSTR = "robot.setProperties(" \
                          + ' '.join(joints) + ',' + ' '.join(len(joints) * ['position']) + ',' \
                          + ' '.join(str(i * self.CONVERSION) for i in self.POSTIONS) + ")"
        return self.SETPROPSTR

    def execute(self, robot):
        currentPositions = self.getPositions(robot)
        finalPositions = map(float, self.POSTIONS)
        changeInPositions = [final - initial for final, initial in zip(finalPositions, currentPositions)]


        largest = -1
        for i in range(len(changeInPositions)):
            if abs(changeInPositions[i]) > largest:
                largest = abs(changeInPositions[i])

        for i in range(len(changeInPositions)):
            changeInPositions[i] /= largest
        print(largest)

        '''
        Set velocities so everything ends at the same time

        '''
        robot.setProperties(' '.join(self.JOINTS), ' '.join(len(self.JOINTS) * ['velocity']),
                            ' '.join(str(changeInPositions * self.VELSET)))
        #print(robot.setProperties( ' '.join(self.JOINTS), ' '.join(len(self.JOINTS) * ['velocity']),
        #                          ' '.join(str(changeInPositions))))
        robot.setProperties(' '.join(self.JOINTS), ' '.join(len(self.JOINTS) * ['position']),
                            ' '.join(str(i * self.CONVERSION) for i in self.POSTIONS))

        # print(self.WAITS)
        if self.WAITS != None:
            for joints in self.WAITS: \
            robot.waitForJoint(joints)

    def getPositions(self, robot):
        return [float(robot.getProperties(joints, "position")) for joints in self.JOINTS]


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
        return isJoint(tag['waitFor'].split(" "))
    else:
        return None


def parseYAML(dictionary):
    gestures = []
    for tags in dictionary:
        if tags == 'units' and dictionary[tags] == 'deg':
            conversion = pi / 180
        else:
            conversion = 1
        if tags == 'vel':
            velset = float(dictionary[tags])
        else:
            velset = 1
    for names in dictionary['run']:
        name = names
        for tags in dictionary[name]:
            joints = isJoint(dictionary[name])
            positions = [dictionary[name][position] for position in joints]
            waits = isWait(dictionary[name])
        gestures.append(Gesture(name, joints, positions, waits, conversion, velset))
    return gestures

def main():

    fname = sys.argv[1]
    with open(fname, 'r') as f:
        doc = yaml.load(f)

    for g in parseYAML(doc):
        g.execute(robot)

if __name__ == '__main__':
    main()
