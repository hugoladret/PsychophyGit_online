#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02.03.2020

@author: remi sanchez

PILOT EXPERIMENT : STAIRCASE
"""
## *  libraries
from __future__ import print_function
import numpy as np
import os
from psychopy import core, data, visual, gui, monitors, logging, event
from psychopy.visual import ShapeStim
from datetime import datetime
import time
from builtins import next
from builtins import range
from numpy.random import shuffle
import copy
import settings
import pandas as pd

clock = core.Clock()

## * Functions
def ask(text='', color='white'):
    """
    Display instruction.
    key = space
    """
    while True:
        theseKeys = event.getKeys()
        if 'escape' in theseKeys:
            win.close()
            core.quit()
        if len(theseKeys):
            break

        instr = visual.TextStim(win, autoLog=False,
                                ori=0,
                                height=size_instruc,
                                font=police,
                                wrapWidth=35,
                                )
        instr.color = color
        instr.text = text
        instr.draw()
        win.flip()
    core.wait(instr_time)


def current_milli_time():
    return round(time.time() * 1000)

## * informations & files

## participant and expe info infos
expInfo = {'participant': '', 'prime': ['1', '2']}
expName = 'Sub_motor_learning'
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if not dlg.OK:
    core.quit()  # user pressed cancel

condition = expInfo['prime']
if expInfo['prime'] == '1':
    left_prime = 'square'
    print('left square')
    right_prime = 'losange'
    print('right losange')
elif expInfo['prime'] == '2':
    left_prime = 'losange'
    print('left losange')
    right_prime = 'square'
    print('right square')


_thisDir = os.path.abspath(os.getcwd())
data_dir = _thisDir + os.sep + 'data' + os.sep + expInfo['participant']
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

subject_id = expInfo['participant']

# create files
filename = data_dir + os.sep + 'motor_learning_' + '%s_%s' % (expInfo['participant'], expInfo['date']) + '_' + condition
filename_short = data_dir + os.sep + 'motor_learning_' + expInfo['participant'] + '_' + condition
output = "subject_id,trial,bloc,cue,pressed_cue,expected_cue,rt_cue,accuracy_cue,trial_start_time_rel2exp,bloc_start_time_rel2exp,exp_start_date\n"
running_filename = filename_short + '_TEMP.txt'
f_handle = open(running_filename, 'a')
f_handle.write(output)
f_handle.close()

logFile = logging.LogFile(filename + '.log', level=logging.DEBUG, filemode='a')

# experiment settings
# monitor parameters
monDistance = settings.monDistance
monWidth = settings.monWidth
monres1 = settings.monres1
monres2 = settings.monres2
win_color = settings.win_color

# display
fixation_size = settings.fixation_size
size_instruc = settings.size_instruc
instr_time = settings.instr_time
police = settings.police
t_fb = settings.t_fb

# primes
losange_xy = settings.losange_xy
square_xy = settings.square_xy
concave_xy = settings.concave_xy

# experimental parameters
cue_deadline = settings.cue_deadline
ITIarray_learning = settings.ITIarray_learning
SOA = settings.SOA
cue_duration = settings.cue_duration
white_cross_time = settings.white_cross_time
neutral_color = settings.neutral_color
# gabor_SOA = settings.gabor_SOA

# keys
LH = settings.LH
RH = settings.RH

# experimental trials handling
n_trial_break = settings.n_trial_break
seq_learning = settings.seq_learning
init_seq_learning = seq_learning
n_trial_learning = settings.n_trial_learning
n_bloc_learning = settings.n_bloc_learning

# * Hardware
# Monitor definition
mon1 = monitors.Monitor('testMonitor')
mon1.setDistance(monDistance)  # cm
mon1.setWidth(monWidth)  # cm
mon1.setSizePix([monres1, monres2])
mon1.saveMon()

# keyboard

# * Stimuli & texts
# create a window to draw in
win = visual.Window(size=[monres1, monres2], monitor=mon1, allowGUI=False, units='deg', fullscr=False, color=win_color,
                    colorSpace='rgb255')
win.setMouseVisible(False)  # hide the mouse cursor


# stimuli
whiteCross = visual.GratingStim(win=win, autoLog = False,
                                mask='cross', size=fixation_size,
                                pos=[0, 0], sf=0, color = neutral_color)

shape = ShapeStim(win, autoLog = False, vertices=losange_xy, lineColor = 'white') # initialize shape

## * textes
police = 'Consolas'  # monospaced font
size_instruc = 0.4
instr_time = 0.1

# instr_1 = "Bienvenue ! \n\n\
# Placez l'index de vos deux mains sur les touches \n\n\
# x et n \n\n\n"
#
# instr_2 = "A chaque essai vous verrez une flèche blanche \n\n\
# suivie d'un stimulus orienté verticalement ou horizontalement"
#
# instr_3 = "Après la présentation de ce stimulus, vous devrez indiquer\n\n\
# son orientation"
#
# instr_31B = "Pour répondre, appuyez sur la touche: \n\n\
# \t - de gauche (x) si le stimulus est orienté verticalement | \n\n\
# \t - de droite (n) si le stimulus est orienté horizontalement — \n\n"
#
# instr_31A = "Pour répondre, appuyez sur la touche: \n\n\
# \t - de gauche (x) si le stimulus est orienté horizontalement — \n\n\
# \t - de droite (n) si le stimulus est orienté verticalement | \n\n"
#
# instr_5 = "Attention! \n\n\n\
# Attendez que le stimulus disparaisse avant de répondre !"

instr_repos = "Prenez un petit temps de pause, reposez-vous les yeux...\n\n\
puis appuyez sur n'importe quelle touche pour continuer."

instr_fin = "Bravo, et merci! \n\n\n\
Vous avez fini l'expérience. \n\n\n\
Merci d'attendre les instructions de l'expérimentateur"


def get_keypress():
    keys = event.waitKeys(maxWait=cue_deadline,keyList = [LH,RH,'escape'], timeStamped = clock, clearEvents = True)
    if keys:
        pressed_key = keys[0][0]  # name
        rt_key = keys[0][1]  # rt
        if 'escape' in pressed_key:
            core.quit()
    else:
        too_late.draw()
        print("too late !")
        logging.exp('too late !')
        win.flip()
        core.wait(t_fb)
        win.flip()
        pressed_key = None
        rt_key = None
    return pressed_key, rt_key


too_late = visual.TextStim(win, ori=0, autoLog = False,
                           height=size_instruc,
                           font=police,
                           color='black',
                           text="Trop lent!")

correct_disp = visual.TextStim(win, ori=0, autoLog = False,
                               height=size_instruc,
                               font=police,
                               color='green',
                               text="Correct")

incorrect_disp = visual.TextStim(win, ori=0, autoLog = False,
                                 height=size_instruc,
                                 font=police,
                                 color='red',
                                 text="Incorrect")

if left_prime == 'square':
    ask(text='square = touche x')
elif left_prime == 'losange':
    ask(text='losange = touche x')

if right_prime == 'square':
    ask(text='square = touche n')
elif right_prime == 'losange':
    ask(text='losange = touche n')

## * Experiment

# get time framework
now_date = datetime.now().time()
exp_start_date = now_date.strftime("%H:%M:%S.%f")
exp_start_ms_abs = current_milli_time()

## ** Instructions
core.wait(t_fb)
# ask(text=instr_1)
# ask(text=instr_2)
# ask(text=instr_5)

## ** Trials
# main loop
# get bloc start time
now = current_milli_time()
bloc_start_ms_abs = now
bloc_start_time_rel2exp = now - exp_start_ms_abs

## Initialisation
currentblock_trial = 0  # current within block trial
i = 0
trial = 0
bloc = 1
toolate = 0
score = 0
lst_toolate = np.zeros((n_bloc_learning, 1))
data_container = []
pressed_cue = -1
rt_cue = -1
accuracy_cue = -1
FBdisp = True

while i < len(seq_learning):  # main loop through all trials #
    ## initialize
    pressed_cue = -1
    expected_cue = -1
    rt_cue = -1
    accuracy_cue = -1
    Not_answered = False

    # get trial timestamp
    now = current_milli_time()
    trial_start_time_rel2exp = now - bloc_start_ms_abs

    # update trial
    trial += 1
    logging.exp(f'start of trial {trial}')

    c_i = seq_learning[i][0]

    if c_i == 1:
        cue_i = left_prime
    elif c_i == 2:
        cue_i = right_prime

    # define shape
    if cue_i == 'losange':
        shape_i = losange_xy
    elif cue_i == 'square':
        shape_i = square_xy

    shape.vertices = shape_i

    # expected responses
    if cue_i == left_prime:
        expected_cue = LH
    elif cue_i == right_prime:
        expected_cue = RH

    # draw white fixation
    whiteCross.draw()
    win.flip()
    core.wait(white_cross_time)
    win.flip()
    core.wait(SOA)

    # draw cue
    shape.draw()
    win.flip()
    core.wait(cue_duration)
    win.flip()

    # Response

    clock.reset()
    pressed_cue, rt_cue = get_keypress()
    if pressed_cue is None:
        # update sequence
        retry = seq_learning[i]  # get current conditions for retry
        seq_learning = np.delete(seq_learning, i, 0)  # remove current row from seq
        seq_learning = np.insert(seq_learning, ((bloc * n_trial_learning) - 1), retry, axis=0)  # add it to the end of the current block
        trial -= 1  # restart trial
        toolate += 1
        continue  # restart trial

    if expected_cue == pressed_cue:
        accuracy_cue = 1
        accdisp = 1
        score += 1
        correct_disp.draw()
        win.flip()
        core.wait(t_fb)
    else:
        accuracy_cue = 0
        accdisp = 0
        incorrect_disp.draw()
        win.flip()
        core.wait(t_fb)

    # Condition specification for the dataframe
    cue = cue_i

    print(
        (
            f"{bloc} trial {trial}, accuracy={accdisp} ({pressed_cue}), stim: {cue_i}, score = {score}/{trial}" + '(%0.2f' % (
                    score / trial) + ')'))

    logging.exp(f'stim {cue}')
    logging.exp(f'end of trial {trial}')
    i = i + 1

    # write
    data_array = [subject_id,
                  trial,
                  bloc,
                  cue,
                  pressed_cue,
                  expected_cue,
                  rt_cue,
                  accuracy_cue,
                  trial_start_time_rel2exp,
                  bloc_start_time_rel2exp,
                  exp_start_date,
                  ]

    data_container.append(data_array)
    output = str(data_array[0]) + ',' + str(data_array[1]) + ',' + str(data_array[2]) + ',' + str(
        data_array[3]) + ',' + str(data_array[4]) + ',' + str(data_array[5]) + ',' + str(data_array[6]) + ',' + str(
        data_array[7]) + ',' + str(data_array[8]) + ',' + str(data_array[9]) + ',' + str(data_array[10]) + ',' + '\n'

    f_handle = open(running_filename, 'a')
    f_handle.write(output)
    f_handle.close()

    logging.flush()

    if trial % n_trial_learning == 0:
        bloc += 1
        print(f"End of block {bloc - 1}. Number of toolate trials: {toolate}")
        toolate = 0
        core.wait(t_fb)
        ask(f"end of bloc {bloc - 1} / {n_bloc_learning}")
        ask(instr_repos)
        # get current time
        now = current_milli_time()
        bloc_start_time = now - exp_start_ms_abs

    win.flip()  # clean screen
    ITI = np.random.choice(ITIarray_learning)
    core.wait(ITI)

## Fin des essais
core.wait(0.5)
ask(text="fin de cette partie de l'expérience")
win.flip()

## save & cleanup
data_container = np.array(data_container, dtype="object")
np.save(filename, data_container)
np.savetxt(filename + '.csv', data_container, delimiter=',', fmt='%s')
np.savetxt(filename_short + '.csv', data_container, delimiter=',', fmt='%s')

df_toolate = pd.DataFrame(lst_toolate)  # too late info table
df_toolate.index = range(1, (n_bloc_learning + 1))
df_init_seq = pd.DataFrame(init_seq_learning)  # initial sequence info table

df_toolate.to_csv(data_dir + os.sep + 'motor_learning_toolate_info_S' + expInfo['participant'] + '.csv', header=False,
                  index=True)
df_init_seq.to_csv(data_dir + os.sep + 'motor_learning_initial_seq_info_S' + expInfo['participant'] + '.csv', header=False,
                   index=False)


# Shutting down
core.quit()
win.close()


