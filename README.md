# hubo-yaml
hubo-yaml is a lightweight python script for creating Hubo scripts using a YAML format.


## Installation
There are several ways to install hubo-yaml:
  - [Download the latest version](https://github.com/jhs88/hubo-yaml/archive/master.zip)
  - Install with git

## Usage
Gestures are created in YAML files. File name does not matter.

To create a gesture name the tag and specify the joints and their positions:
  ```YAML
  my-gesture:
    RSY: 1
    RSP: -1
  ```
Multiple Gestures can be run in sequence using the `run` tag:
  ```YAML
  hello:
    RSY: 1
    RSP: -1

  good-bye:
    LKP: 1

  run:
    - hello
    - good-bye
  ```
This tag is required to run a YAML script.
Gestures will be run in the order of the list.
They can also be repeated.

To specify units use the `units` tag:
  ```YAML
  units: deg

    hello:
      RSY: 45
      RSP: 30
  ```
The `deg` tag is used for degrees and `rad` tag for radians.
The script will default to radians if the `units` tag is not specified.

The `waitFor` tag can be used to specify which joints the robot should
wait to move before going on to another process. This creates more natural-like movements.
  ```YAMl
  hello:
    RSY: 45
    RSP: 30
    waitFor: RSY RSP
  ```

## Example YAML
A finished YAML script should like this:
  ```YAML
  units: rad

  gesture1:
      RSY: 1
      LSY: 2
      waitFor: RSY LSY

  gesture2:
      RSY: -1
      RSR: 1

  run:
      - gesture1
      - gesture2
  ```

## Options

### Functions

Function | Sub Tag | Description
:------: | :-----------: | -------------
`units` | `deg` `rad` | specifies units
`waitFor` |`"list of joints"` | waits for joints to move to position
(More Functions coming soon)


### Joint List
Hubo has six joints on each side: Shoulder, Hip, Knee, Elbow, Ankle, Wrist, Finger.
Joints are defined by standard three letter tags. For most of them the first letter
specifies which side the joint is on (Left or Right). The second letter specifies the
joint location. And the third specifies roll, pitch, and yaw.

Hubo also has joints that don't follow the standard: Waist, Neck, Finger.
Hubo's Neck and Fingers have multiple joints and his Waist only has one. These joint tags
are still only three characters.

This table shows the valid joint exceptions:

Tag | Description
:-------: | :-----:
`WST` | Waist joint
`NKY` | Neck yaw
`NK[1-2]` | Neck joint (1 or 2)
`[L-R]F[1-5]` | Finger (Left or Right hand has 5 fingers)

This diagram shows all the valid joint declarations:

<img src="/img/joints.svg"/>




## Build
  - Clone the repository: `https://github.com/jhs88/hubo-yaml.git`
  - Change in the project directory: `cd hubo-yaml`
  - Create YAML script in directory
  - Run hubo-yaml.py in Hubo: `python hubo-yaml.py [YAML script]`
