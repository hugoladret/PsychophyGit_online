# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 14:52:15 2021

@author: Rémi Sanchez
"""
import numpy as np
import itertools
import random


## monitor parameters
monDistance = 70
monWidth = 53
monres1 = 1920
monres2 = 1080
win_color = [128, 128, 128]

# display
fixation_size = 0.4 # size of the fixation cross
gabor_size = 2  # size of the gabor circle
size_instruc = 0.4
instr_time = 0.1
police = 'Consolas'  # monospaced font
t_fb = 0.40

# staircase
trainLoop = 30
nLoopT = 50
trainingVals = [0.030, 0.025]
startVals = [0.025, 0.0165]
trainTrials = 30
nTrials= 50
nUp=1
nDown=3
nReversals = 6
stepSizes=0.00165
ftresh = 0.725


# gabor
gabor_sf = [2, 0]
noise_contrast = 0.35
noise_opacity = 0.32
noise_point = 0.01
noise_size = (1.8,1.8)
gab_cue_radius = 1
pilot_contrast = 0.025
training_pilot_contrast = 0.2

# prime display
prime_duration = 0.016
prime_SOA = 0.08
mask_duration = 0.2
mask_IT = 2

# primes and masks coordinates
losange_xy = [(0, 0.88), (-0.88, 0), (0, -0.88), (0.88,0)] # Sens anti horaire
square_xy = [(-0.66, 0.66), (-0.66, -0.66), (0.66, -0.66), (0.66, 0.66)]
concave_xy = [(-0.66, 0.66), (-0.66, -0.66), (0, -0.33), (0.66, -0.66), (0.66, 0.66), (0, 0.33)]

# masks
mask_a_xy = [(-0.66, 0.66), (0, -0.66), (0.66, 0.66)] #inverse triangle
mask_b_xy = [(-0.66, 0.66), (-0.66, 0.33), (0.66, 0.33), (0.66, 0.66)] # upper rectangle
mask_c_xy = [(-0.66, -0.33), (-0.66, -0.66), (0.66, -0.66), (0.66, -.33)] # lower rectangle
mask_d_xy = [(-0.66, 0.66), (-0.33, -0), (-0.66, -0.66), (0.66, -0.66), (0.33, 0), (0.66, 0.66)] #inverse concave
mask_e_xy = [(0, 0.88), (-0.88, 0), (0, -0.88), (0.88,0)]# big losange

mask_f_xy = [(0.33, 0.88), (-0.88, 0.33), (-0.33, -0.88), (0.88,-0.33)]# lets finish the star
mask_g_xy = [(-0.33, 0.88), (-0.88, -0.33), (0.33, -0.88), (0.88,0.33)]# lets finish the star
#mask_h_xy = [(-0.66,0),(0.66,0)]
mask_h_xy = [(0,0)]

mask_i_xy = [(-0.33,-0.66),(-0.33,0.66)]  # vertical lines to balance
mask_j_xy = [(0.33,-0.66),(0.33,0.66)]
#mask_k_xy = [(0,-0.66),(0,0.66)]
mask_k_xy = [(0,0)]


# experimental parameters
stairDL = 1.5
cue_deadline = 0.80
gab_deadline = 0.80
ITIarray = [0.9,1,1.1]
ITIarray_learning = [0.6,0.7,0.8]
SOA = 0.7
cue_duration = .2
white_cross_time = 0.4
gabor_duration = 2 # in frames
neutral_color = 'white'
training_trials = 32

# confidence display
conf_circle_color = [0.5, 0.5, 0.5]
conf_lineColor=[-1, -1, -1]
conf_circle_radius = 0.6
conf_text_height = 0.8
pos_errorconf = [(-0.8,-3.5),(0.8,-3.5),(0.8,-4.60),(-0.8,-4.60)]

# position
absposA = 1.8
absposB = 1
pos1 = [-absposA, -absposB]
pos2 = [-absposA, absposB]
pos3 = [absposA, absposB]
pos4 = [absposA, -absposB]
pos5 = [0,-2.65]

# response keys
LH = 'x'
RH = 'n'
LF = 'z'
RF = 'i'
detection_key1 = 'x'
detection_key2 = 'n'
NH = 'space'

# experimental trials
n_trial_break = 25

## ## *  Trials
## parameters
prime_array = np.array([1, 2])
cue_array = np.array([1, 2])  # color: 1=left, 2=right
ori_array = np.array([1, 2])  # orientation: 1=horizontal, 2=vertical, 0=none
possible_stim = [[prime, ori] for prime in prime_array for ori in ori_array] # 6 gabor conditions with primes
n_bloc = 18  ## number of blocks
n_trial = 16  ## number of trials/block
# 288 trials in 18 blocs de 16 trials
#TEST TO DELETE
#n_block = 1  ## number of blocks
#n_trial = 8  ## number of trials/block

primeratio = (1/2)  # proportion of gabor trials
total_trials = int(n_bloc * n_trial)  # total number of trials
gabor_trials = int(primeratio * total_trials)
no_gab_array = [(1, 0), (2, 0)]
no_gab_array = np.tile(no_gab_array, 1).reshape(-1, 2)  # possible stims for no_gabor

#  whole sequence
seq = np.empty((0, 2))
bloc = (0,2)
for i in range(9):
    gab_bloc = np.tile(possible_stim, int(4)).reshape(-1, 2)
    np.random.shuffle(gab_bloc)
    nogab_bloc = np.tile(no_gab_array, int(8)).reshape(-1, 2)
    np.random.shuffle(nogab_bloc)
    if random.randint(0,1) == 0:
        seq = np.append(seq, gab_bloc[0:8]).reshape(-1,2)  # first add 8 gabor trials to the empty bloc sequence (2*4)
        seq = np.append(seq, nogab_bloc[0:8]).reshape(-1, 2)
        seq = np.append(seq, gab_bloc[8:16]).reshape(-1, 2)  # first add 8 gabor trials to the empty bloc sequence (2*4)
        seq = np.append(seq, nogab_bloc[8:16]).reshape(-1, 2)
    else:
        seq = np.append(seq, nogab_bloc[0:8]).reshape(-1, 2)
        seq = np.append(seq, gab_bloc[0:8]).reshape(-1, 2)
        seq = np.append(seq, nogab_bloc[8:16]).reshape(-1, 2)
        seq = np.append(seq, gab_bloc[8:16]).reshape(-1, 2)

# confidence scale counterbalance
conf_seq = np.zeros(shape=(int(gabor_trials),4)) # gabor_trials + 12 because [132 gabor % 24 permutations = 12] unfortunately
#conf_seq = np.zeros(shape=(int(50),4)) less trials for testing
for i in range(0,int(gabor_trials),24):
    conf_seq[i:i+24] = list(itertools.permutations([1, 2, 3, 4]))  # all possible combinations (24)
    np.random.shuffle(conf_seq[i:i+24]) # shuffle within each 24 permutation set
    # (to check number of occurences: np.count_nonzero(conf_seq[:,x] == x))


# motor learning sequence
# parameters
cue_array_learning = [1,2]
possible_stim_learning = np.tile(cue_array_learning, 1).reshape(-1, 2)  # possible stims for cues
n_bloc_learning = 8  # number of blocks
n_trial_learning = 20  # number of trials/block
total_trials_learning = int(n_bloc_learning * n_trial_learning)  # total number of trials

#  whole sequence
seq_learning = np.empty((0, 1))
for i in range(n_bloc_learning):  # 8 blocks with 20 cue trials shuffled
    bloc = np.tile(possible_stim_learning, int(10)).reshape(-1, 1)  # add 25 trials to a bloc
    np.random.shuffle(bloc)  # shuffle it
    seq_learning = np.append(bloc, seq_learning).reshape(-1, 1)  # append bloc sequences for a whole exp sequence


# subliminal detection sequence
prime_array_detection = [1,2] # 1 = left prime, 2 = right prime
n_bloc_detection = 6
n_trial_detection = 20

total_trials_detection = int(n_bloc_detection * n_trial_detection)  # total number of trials

# sequence
seq_detection = np.empty((0, 1))
for i in range(n_bloc_detection):  # 5 blocks of 20 (10 of each prime shuffled)
    bloc_detection = np.tile(prime_array_detection, int(10)).reshape(-1, 1)  # first add 18 'same' trials to the empty bloc sequence (3*6)
    np.random.shuffle(bloc_detection)  # shuffle it
    seq_detection = np.append(bloc_detection, seq_detection).reshape(-1, 1)  # append bloc sequences for a whole exp sequence

seq_detection_gabor = np.empty((0,1))
for i in range((60)):
    gabor_vertical = 0
    gabor_horizontal = 90
    seq_detection_gabor = np.append(gabor_vertical, seq_detection_gabor).reshape(-1,1)
    seq_detection_gabor = np.append(gabor_horizontal, seq_detection_gabor).reshape(-1,1)
np.random.shuffle(seq_detection_gabor)

# STAIRCASE GABOR sequence
# parameters
# gabor test
seq_stair_gab = np.zeros((3,30))
seq_stair_prime = np.zeros((3,30))

for g in range(0,30):
    if g <= 7:
        seq_stair_gab[:,g] = 1
        seq_stair_prime[:,g] = 1
    elif 8 <= g <= 14:
        seq_stair_gab[:, g] = 2
        seq_stair_prime[:, g] = 2
    elif 15 <= g <= 21:
        seq_stair_gab[:, g] = 1
        seq_stair_prime[:, g] = 2
    elif 22 <= g <= 29:
        seq_stair_gab[:, g] = 2
        seq_stair_prime[:, g] = 1

#first
np.random.shuffle(seq_stair_gab[0,0:14])
np.random.shuffle(seq_stair_gab[1,0:14])
np.random.shuffle(seq_stair_gab[2,0:14])

np.random.shuffle(seq_stair_gab[0,14:29])
np.random.shuffle(seq_stair_gab[1,14:29])
np.random.shuffle(seq_stair_gab[2,14:29])

np.random.shuffle(seq_stair_prime[0,0:14])
np.random.shuffle(seq_stair_prime[1,0:14])
np.random.shuffle(seq_stair_prime[2,0:14])

np.random.shuffle(seq_stair_prime[0,14:29])
np.random.shuffle(seq_stair_prime[1,14:29])
np.random.shuffle(seq_stair_prime[2,14:29])

#second
np.random.shuffle(seq_stair_gab[0,0:14])
np.random.shuffle(seq_stair_gab[1,0:14])
np.random.shuffle(seq_stair_gab[2,0:14])

np.random.shuffle(seq_stair_gab[0,14:29])
np.random.shuffle(seq_stair_gab[1,14:29])
np.random.shuffle(seq_stair_gab[2,14:29])

np.random.shuffle(seq_stair_prime[0,0:14])
np.random.shuffle(seq_stair_prime[1,0:14])
np.random.shuffle(seq_stair_prime[2,0:14])

np.random.shuffle(seq_stair_prime[0,14:29])
np.random.shuffle(seq_stair_prime[1,14:29])
np.random.shuffle(seq_stair_prime[2,14:29])

# counting lists :
# from collections import Counter
# Counter(seq_detection[i,i])