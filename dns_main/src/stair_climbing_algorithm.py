#!/usr/bin/env python2
import time
from math import radians
from service_router import *
from locomotion     import *
from math import asin, pi, atan2
from kinematics import Kinematics
from math_calc import vector_length

K = Kinematics()

def terminate():
    ee_xyz, servopos = K.doFkine(readPos())
    if abs(ee_xyz[2]-ee_xyz[5]) < 50:
        if abs(ee_xyz[8]-ee_xyz[11]) < 50:
            if abs(ee_xyz[8]-ee_xyz[2]) < riser/2:
                print("yeay im on top of stairs")
                return True
    else:
        return False

def standUpForStairs():
    standup_pos = [2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296,
                   2048, 2048, 1296, 2048, 2048, 1296]

    front_standup = list_combine(leg[1] + leg[2], standup_pos)
    rear_standup = list_combine(leg[5] + leg[6], standup_pos)
    middle_standup = list_combine(leg[3] + leg[4], standup_pos)
    positionN(front_standup)
    time.sleep(1)
    positionN(rear_standup)
    time.sleep(1)
    positionN(middle_standup)
    time.sleep(1)

def correctMiddleLegs(z):
    Up          =   [0, 0,  z]
    LiftUp      =   calc_motion(Up)

    pos = list()
    pos.extend(LiftUp[12:18])
    pos.extend(LiftUp[18:24])
    positionN(pos)
    leg_case = [3,4]
    check_position_error_legs(80, 20, pos, leg_case)
    ServoCentering=[7,2048,10,2048]
    positionN(ServoCentering)
    time.sleep(1)

    Down          =   [0, 0, -z]
    LiftDown      =   calc_motion(Down)

    pos1 = list()
    pos1.extend(LiftDown[12:18])
    pos1.extend(LiftDown[18:24])
    positionN(pos1)
    leg_case = [3,4]
    check_position_error_legs(80, 20, pos1, leg_case)

def initialDistance(distance):
    all_pos = readPos()
    ee_xyz, servopos = K.doFkine(all_pos)
    dist2FirstStep_1 = distance 
    dist2FirstStep_2 = distance
    dist2FirstStep_3 = distance + ee_xyz[1] - ee_xyz[7]
    dist2FirstStep_4 = distance + ee_xyz[1] - ee_xyz[10]
    dist2FirstStep_5 = distance + ee_xyz[1] - ee_xyz[13]
    dist2FirstStep_6 = distance + ee_xyz[1] - ee_xyz[16]
    dist2FirstStep = dist2FirstStep_1, dist2FirstStep_2, dist2FirstStep_3, dist2FirstStep_4, dist2FirstStep_5, dist2FirstStep_6
    print dist2FirstStep
    return dist2FirstStep

def initConfig_legs(depth):
    maxy = 344.74638441867046
    r = 392.55798277243395 - 141.33 #maximumy - y_offset of leg one
    miny = 181.0804846109524
    phai = asin((depth-miny)/r) * 2048/pi # change of coxa in steps
    #print(int(phai))
    if depth < maxy:
        standup_pos = [ 1536 + int(phai), 2048, 1296, 2560 - int(phai), 2048, 1296,
                        2048            , 2048, 1296, 2048       , 2048, 1296,
                        2560 - int(phai), 2048, 1296, 1536 + int(phai), 2048, 1296]
        # lift_up = [2048, 2448,1296,2048,2448,1296,
        #            2048, 2448,1296,2048,2448,1296,
        #            2048, 2448,1296,2048,2448,1296]
        #print(standup_pos)
        # front_liftup = list_combine(leg[2] + leg[5],lift_up)
        # positionN(front_liftup)
        # time.sleep(2)
        front_standup = list_combine(leg[1] + leg[2], standup_pos)
        positionN(front_standup)
        time.sleep(1)
        # rear_liftup = list_combine(leg[1] + leg[6],lift_up)
        # positionN(rear_liftup)
        # time.sleep(1)
        rear_standup = list_combine(leg[3] + leg[4], standup_pos)
        positionN(rear_standup)
        time.sleep(1)
        rear_standup = list_combine(leg[5] + leg[6], standup_pos)
        positionN(rear_standup)
        time.sleep(1)
        ee_xyz, servopos = K.doFkine(readPos())
        return maxy - ee_xyz[1] 

def correctRotation(depth, riser):
    slope = atan2(riser,depth)*180/pi
    gamma, beta = K.get_orientation([1,5,6])
    new_gamma = slope - gamma
    parallelGait(0,0,int(new_gamma-3),0,0,0) #-3 should be 0  but seems to help to keep the robot parallel
    time.sleep(3)
    print("Slope is:", new_gamma)

def moveForward(x, y, z, alpha, beta, gamma, distance):
    

    Forward =   [x, y, z]
    Up      =   [0, 0, z]
    Down    =   [x, y, 0]
    Push    =   [0, 0, 0]

    HalfForward =   [0.5*x, 0.5*y, z]
    HalfUp      =   [    0,     0, z]
    HalfDown    =   [0.5*x, 0.5*y, 0]


    PushBackwards = calc_motion(Push)
    LiftUp        = calc_motion(Up)
    LiftDown      = calc_motion(Down)
    PutForward    = calc_motion(Forward)

  
    HalfLiftUp        = calc_motion(HalfUp)
    HalfLiftDown      = calc_motion(HalfDown)
    HalfPutForward    = calc_motion(HalfForward)

    
    while distance > 0.75 * stepSize:
        if distance > 1.5 * stepSize:
            pos = list()
            pos.extend(LiftUp[6:12])
            pos.extend(LiftUp[12:18])
            pos.extend(LiftUp[30:36])
            positionN(pos)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos, leg_case)

            pos1 = list()
            pos1.extend(PutForward[6:12])
            pos1.extend(PutForward[12:18])
            pos1.extend(PutForward[30:36])
            positionN(pos1)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos1, leg_case)

            pos2 = list()
            pos2.extend(LiftDown[6:12])
            pos2.extend(LiftDown[12:18])
            pos2.extend(LiftDown[30:36])
            positionN(pos2)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos2, leg_case)

            pos3 = list()
            pos3.extend(LiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(LiftUp[18:24])
            pos3.extend(LiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(40, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            positionN(pos4)
            leg_case = [1,4,5]
            check_position_error_legs(20, 30, pos4, leg_case)
            distance = distance -  stepSize
        else:
            pos = list()
            pos.extend(HalfLiftUp[6:12])
            pos.extend(HalfLiftUp[12:18])
            pos.extend(HalfLiftUp[30:36])
            positionN(pos)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos, leg_case)

            pos1 = list()
            pos1.extend(HalfPutForward[6:12])
            pos1.extend(HalfPutForward[12:18])
            pos1.extend(HalfPutForward[30:36])
            positionN(pos1)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos1, leg_case)

            pos2 = list()
            pos2.extend(HalfLiftDown[6:12])
            pos2.extend(HalfLiftDown[12:18])
            pos2.extend(HalfLiftDown[30:36])
            positionN(pos2)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos2, leg_case)

            pos3 = list()
            pos3.extend(HalfLiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(HalfLiftUp[18:24])
            pos3.extend(HalfLiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(80, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            positionN(pos4)
            leg_case = [1,4,5]
            check_position_error_legs(20, 30, pos4, leg_case)
            distance = distance -  (0.5 *stepSize)
    time.sleep(0.5)
    return distance   

def walkUp(distanceToStair, x, stepSize, threshold, riser, alpha, beta, gamma):
    orientation = [alpha,beta,gamma]

                
    Forward =   [x, stepSize, threshold]
    Up      =   [0,        0, threshold]
    Down    =   [x, stepSize,         0]
    Push    =   [0, 0, 0]

    UpForward       =  [x, stepSize, threshold+riser]
    StepUp          =  [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)

    pos = []

  
    ##Lift_Up_First_Leg_group
    for i in range(len(distanceToStair)):
        if i == 0 or i == 3 or i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6]) 
    positionN(pos)
    leg_case = [1,4,5]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    ##Put_Forward_First_Leg_group
    for i in range(len(distanceToStair)):
        if i == 0 or i == 3 or i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpForward[i*6 : i*6+6])
            else:
                pos.extend(PutForward[i*6 : i*6+6]) 
    positionN(pos)
    leg_case = [1,4,5]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    ##Step_Down_First_leg_group
    for i in range(len(distanceToStair)):
        if i == 0 or i == 3 or i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownFirst[i*6 : i*6+6])
            else:
                pos.extend(LiftDown[i*6 : i*6+6]) 
    positionN(pos)
    leg_case = [1,4,5]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    check_contact()
    #########################################################################################################
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    UpPushBackwards     = [0, -stepSize, 0]
    StepUpPushBackwards = calc_motion(UpPushBackwards)
    ##Lift_Up_Second_Leg_group
    for i in range(len(distanceToStair)):
        if i == 1 or i == 2 or i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpUp[i*6 : i*6+6])
            else:
                pos.extend(LiftUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [2,3,6]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    ##Put_Forward_Second_Leg_group
    for i in range(len(distanceToStair)):
        if i == 0 or i == 3 or i == 4:
            if distanceToStair[i] < stepSize:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6])
            else:
                pos.extend(StepUpPushBackwards[i*6 : i*6+6]) 
    positionN(pos)
    leg_case = [1,4,5]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    ##Step_Down_Second_leg_group
    for i in range(len(distanceToStair)):
        if i == 1 or i == 2 or i == 5:
            if distanceToStair[i] < stepSize:
                pos.extend(StepDownDownSecond[i*6 : i*6+6])
            else:
                pos.extend(PushBackwards[i*6 : i*6+6])
    positionN(pos)
    leg_case = [2,3,6]
    check_position_error_legs(120, 30, pos, leg_case)
    pos = []
    check_contact()
    distanceToStair = [i - stepSize for i in distanceToStair]

def updateDistance(distanceToStair, stepSize):
    distanceToStair = [i - stepSize for i in distanceToStair]
    for i in range(len(distanceToStair)):
        if distanceToStair[i] < 0:
            distanceToStair[i] = distanceToStair[i] + thread
    print distanceToStair
    return distanceToStair

def rotateAndTranslate(riser,climbed_stairs_front, climbed_stairs_rear):
    gamma, beta = K.get_orientation([1, 5, 6])
    parallelGait(0, -beta, -gamma, 0, 0, 0)
    time.sleep(2)
    a = K.calc_translationStairs(riser,climbed_stairs_front, climbed_stairs_rear)
    parallelGait(0, 0, 0, 0, a[1], a[0])
    time.sleep(2)
    return beta , gamma

def moveForwardOnStair(x, y, z, alpha, beta, gamma, distance):
    initialDistance = distance
    orientation = [alpha, beta, gamma]    

    Forward =   [x, y, z]
    Up      =   [0, 0, z]
    Down    =   [x, y, 0]
    Push    =   [0, 0, 0]

    HalfForward =   [0.5*x, 0.5*y, z]
    HalfUp      =   [0, 0, z]
    HalfDown    =   [0.5*x, 0.5*y, 0]


    PushBackwards = calc_motion(Push, orientation)
    LiftUp        = calc_motion(Up, orientation)
    LiftDown      = calc_motion(Down, orientation)
    PutForward    = calc_motion(Forward, orientation)

  
    HalfLiftUp        = calc_motion(HalfUp, orientation)
    HalfLiftDown      = calc_motion(HalfDown, orientation)
    HalfPutForward    = calc_motion(HalfForward, orientation)

    print (distance)

    while distance > 0.75 * stepSize:
        if distance > 1.5 * stepSize:
            pos = list()
            pos.extend(LiftUp[6:12])
            pos.extend(LiftUp[12:18])
            pos.extend(LiftUp[30:36])
            positionN(pos)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos, leg_case)

            pos1 = list()
            pos1.extend(PutForward[6:12])
            pos1.extend(PutForward[12:18])
            pos1.extend(PutForward[30:36])
            positionN(pos1)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos1, leg_case)

            pos2 = list()
            pos2.extend(LiftDown[6:12])
            pos2.extend(LiftDown[12:18])
            pos2.extend(LiftDown[30:36])
            positionN(pos2)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos2, leg_case)

            pos3 = list()
            pos3.extend(LiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(LiftUp[18:24])
            pos3.extend(LiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(20, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            positionN(pos4)
            leg_case = [1,4,5]
            check_position_error_legs(20, 30, pos4, leg_case)
            distance = distance -  stepSize
        else:
            pos = list()
            pos.extend(HalfLiftUp[6:12])
            pos.extend(HalfLiftUp[12:18])
            pos.extend(HalfLiftUp[30:36])
            positionN(pos)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos, leg_case)

            pos1 = list()
            pos1.extend(HalfPutForward[6:12])
            pos1.extend(HalfPutForward[12:18])
            pos1.extend(HalfPutForward[30:36])
            positionN(pos1)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos1, leg_case)

            pos2 = list()
            pos2.extend(HalfLiftDown[6:12])
            pos2.extend(HalfLiftDown[12:18])
            pos2.extend(HalfLiftDown[30:36])
            positionN(pos2)
            leg_case = [2,3,6]
            check_position_error_legs(20, 30, pos2, leg_case)

            pos3 = list()
            pos3.extend(HalfLiftUp[0:6])
            pos3.extend(PushBackwards[6:12])
            pos3.extend(PushBackwards[12:18])
            pos3.extend(HalfLiftUp[18:24])
            pos3.extend(HalfLiftUp[24:30])
            pos3.extend(PushBackwards[30:36])
            positionN(pos3)
            check_position_error(20, 50, pos3)

            pos4 = list()
            pos4.extend(PushBackwards[0:6])
            pos4.extend(PushBackwards[18:24])
            pos4.extend(PushBackwards[24:30])
            positionN(pos4)
            leg_case = [1,4,5]
            check_position_error_legs(20, 30, pos4, leg_case)
            distance = distance -  (0.5 *stepSize)
    time.sleep(0.5)
    return distance

def walkUpAllLegs(distanceToStair, x, stepSize, threshold, riser, alpha, beta, gamma):
    orientation = [alpha,beta,gamma]

                
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)

    pos = []

  
    ##Lift_Up_Fifth_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Fifth_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Fifth_leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Sixth_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Sixth_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Sixth_leg
    for i in range(len(distanceToStair)):
        if i ==5:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    distanceToStair = [i - stepSize for i in distanceToStair]
    parallelGait(0,0,0,0,0,riser/2)
    time.sleep(2)
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)
    ###########################################################################
    ##Lift_Up_Third_Leg
    for i in range(len(distanceToStair)):
        if i == 2:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [3]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Third_Leg
    for i in range(len(distanceToStair)):
        if i == 2:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [3]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Third_leg
    for i in range(len(distanceToStair)):
        if i == 2:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [3]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Forth_Leg
    for i in range(len(distanceToStair)):
        if i == 3:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [4]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Forth_Leg
    for i in range(len(distanceToStair)):
        if i == 3:
            pos.extend(StepUpForward[i*6 : i*6+6])
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    positionN(pos)
    leg_case = [4]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Forth_leg
    for i in range(len(distanceToStair)):
        if i ==3:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [4]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    distanceToStair = [i - stepSize for i in distanceToStair]
    parallelGait(0,0,0,0,0,riser/2)
    time.sleep(2)
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)
    


        ###########################################################################
        ##Lift_Up_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [1]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_First_Leg
    for i in range(len(distanceToStair)):
        if i == 0:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [1]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_First_leg
    for i in range(len(distanceToStair)):
        if i == 0:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])

    positionN(pos)
    leg_case = [1]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [2]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Second_Leg
    for i in range(len(distanceToStair)):
        if i == 1:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [2]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Second_leg
    for i in range(len(distanceToStair)):
        if i ==1:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [2]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    distanceToStair = [i - stepSize for i in distanceToStair]
    timeToTerminate = terminate()
    if timeToTerminate == True: 
        timeToContinue = True
        return timeToContinue

def moveUpOnlyLastLegs(distanceToStair, x, stepSize, threshold, riser, alpha, beta, gamma):
    orientation = [alpha,beta,gamma]

                
    Forward =   [x, stepSize, threshold]
    Up      =   [0, 0, threshold]
    Down    =   [x, stepSize, 0]
    Push    =   [0, 0, 0]

    UpForward       =   [x, stepSize, threshold+riser]
    StepUp          =   [0, 0, threshold+riser]
    StepDownFirst   =  [x, stepSize, threshold/2+riser]
    StepDownSecond  =  [x, 0, threshold/2+riser]

    PushBackwards = calc_motion(Push,orientation)
    LiftUp        = calc_motion(Up,orientation)
    LiftDown      = calc_motion(Down,orientation)
    PutForward    = calc_motion(Forward,orientation)

  
    StepUpForward        = calc_motion(UpForward,orientation)
    StepUpUp             = calc_motion(StepUp,orientation)
    StepDownDownFirst    = calc_motion(StepDownFirst,orientation)
    StepDownDownSecond   = calc_motion(StepDownSecond,orientation)

    pos = []

  
    ##Lift_Up_Fifth_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Fifth_Leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Fifth_leg
    for i in range(len(distanceToStair)):
        if i == 4:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [5]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    UpNothing           = [0, 0, 0]
    UpUpNothing         = calc_motion(UpNothing)
    #########################################################################################################
    ##Lift_Up_Sixth_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            pos.extend(StepUpUp[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Put_Forward_Sixth_Leg
    for i in range(len(distanceToStair)):
        if i == 5:
            pos.extend(StepUpForward[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    ##Step_Down_Sixth_leg
    for i in range(len(distanceToStair)):
        if i ==5:
            pos.extend(StepDownDownFirst[i*6 : i*6+6])
    positionN(pos)
    leg_case = [6]
    check_position_error_legs(120, 20, pos, leg_case)
    pos = []
    check_contact()
    distanceToStair = [i - stepSize for i in distanceToStair]
    parallelGait(0,0,0,0,0,riser/2)
    time.sleep(2)

def translateAboveRiser():
    ee_xyz, servopos = K.doFkine(readPos())
    legZPlancement = abs(ee_xyz[8]+ee_xyz[11])/2
    print("first leg placement in z is" , legZPlancement)
    if legZPlancement-riser < 70: 
        translationZ = riser + 70 - legZPlancement
        parallelGait(0,0,0,0,0,translationZ)
        time.sleep(3)

#####################STAIR CLIMBING ALGORITHM STARTS HERE#########################

torque(0)
pwm_list = [800]*18         #Setting PWM to "high" max is 885
pwmAll(pwm_list)
scaler_acc = [20] * 18      #Setting Acceleration to "low"
scaler_vel = [20] * 18      #Setting Velocity to "low"
velocityAll(scaler_vel)
accelerationAll(scaler_acc)
torque(1)
threshold = 50              # Set z threshold (step up)
stepSize = 50               # Set Step Size 
riser = 163                 # Enter your riser height or obtain by camera
thread = 284                # Enter your thread depth or obtain by camera

initConfig_legs(thread)     # Rotates the coxa servos to cause the displacement of a thread depth between the leg pairs
time.sleep(3)


## Move forward to the first step on the stair. 700 = mm. Assuming the robot is placed at this distance 
#distanceToStairInitial = initialDistance(moveForward(0, stepSize, threshold, 0, 0, 0, 550))
##For testing put the first legs next to the riser with the distance of approx 25mm
distance = 25
distanceToStairInitial = initialDistance(distance)  # Gets the y value of each legs with respect to the first leg

parallelGait(0,0,0,0,0,riser/2)                     # Translate the body by half of the riser
time.sleep(2)
walkUp(distanceToStairInitial,0, stepSize*2, threshold, riser, 0,0,0)   # Walks up with the leg within the step size (leg 1,2)of a riser by tripod
moveForwardOnStair(0, stepSize, threshold, 0, 0, 0, thread)             # Moves forward on the stairs by the riser depth
parallelGait(0,0,0,0,0,riser/2)                                 
time.sleep(2)
# Update distances by substracting the riser to 2nd and 3rd legpair
distanceToStairs = distanceToStairInitial[0], distanceToStairInitial[1], distanceToStairInitial[2]-thread, distanceToStairInitial[3]-thread, distanceToStairInitial[4]-thread,distanceToStairInitial[5]-thread   
walkUp(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0)          # Walks up with the leg within the step size (leg 1,2,3,4 )of a riser by tripod
translateAboveRiser()     # Body is translated above the riser, unless the body is already above

stairs = True   
# Update distances by substracting the riser to the 3rd legpair
distanceToStairs = distanceToStairs[0], distanceToStairs[1], distanceToStairs[2], distanceToStairs[3], distanceToStairs[4]-thread, distanceToStairs[5]-thread

while stairs is True:
    stepSize = 50
    correctRotation(thread,riser) # Correcting the rotation by the negative slope of the stairs to keep the body horizontal
    time.sleep(2)
    correctMiddleLegs(20)         # Corrects possible errors that tend to affect the coxa joint
    moveForwardOnStair(0, stepSize, threshold, 0, 0, 0, riser+stepSize)
    stability_margin, stability_bool = check_stabilty()   # Checking for stability
    if stability_margin > stepSize:
        checkForTermination = walkUpAllLegs(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0) #Walking up with all legs by wave gait and check if the robot is ontop of the stairs
        if checkForTermination == True:
            break    #If the robot is ontop then go out of while loop
        correctRotation(thread,riser)  
        time.sleep(1)
        parallelGait(0,0,0,0,50,0) #translate the body forward
        time.sleep(2)
        parallelGait(0,0,0,0,50,0)
        time.sleep(2)
        translateAboveRiser()
    else:
        stepSize = stability_margin
        checkForTermination = walkUpAllLegs(distanceToStair,0, stepSize*2, threshold, riser, 0,0,0
        if checkForTermination == True:
            break   
        correctRotation(thread,riser)  
        time.sleep(1)
        parallelGait(0,0,0,0,50,0) 
        time.sleep(2)
        parallelGait(0,0,0,0,50,0)
        time.sleep(2)
        translateAboveRiser()


# This part is executed if the algorithm is terminated by checking if the front legs dosnt change level when it tries to get to next level

time.sleep(2)
parallelGait(0,0,0,0,50,0)
time.sleep(2)
parallelGait(0,0,0,0,50,0)
time.sleep(2)
moveForwardOnStair(0, stepSize, threshold, 0, 0, 0, riser)
moveUpOnlyLastLegs(distanceToStair,0,stepSize,threshold,riser,0,0,0) # Only lifts the rear legs by wave gait above the last riser
moveForward(0, stepSize, threshold, 0, 0, 0, 550)  # Move forward 


