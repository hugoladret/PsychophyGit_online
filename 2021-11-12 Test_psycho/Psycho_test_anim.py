
import argparse
import sys
import numpy as np
import os
import imageio
import sys
import json
from time import strftime, gmtime
import MotionClouds as mc
import time
import pandas as pd
from torchvision import datasets, models, transforms

os.environ['DISPLAY'] = ':0.0'

def arg_parse(): 
    parser = argparse.ArgumentParser(description='Psycho_test_anim set root')
    parser.add_argument("--root", dest = 'root', help = 
                        "Directory containing images to perform the training",
                        default = '/tmp/data', type = str)
    parser.add_argument("--N_total_trials", dest = 'n_total_trials', help = 
                        "Number of trials for the experiment",
                        default = 10 , type = int)
    parser.add_argument("--Fixation_length", dest = 'fixation_length', help = 
                        "Select the time of fixation before stimulus",
                        default = .25 , type = float)
    parser.add_argument("--Stim_length", dest = 'stim_length', help = 
                        "Select the time of for the stimulus",
                        default = .25 , type = float)
    parser.add_argument("--to_test", dest = 'to_test', help = 
                    "--True to start the experiment",
                    default = True, type = bool)
    parser.add_argument("--fullscr", dest = 'fullscr', help = 
                    "--True to work in full screen",
                    default = False, type = bool)
    parser.add_argument("--HOST", dest = 'HOST', help = 
                "Set the name of your machine",
                default = os.uname()[1], type = str)
    parser.add_argument("--datetag", dest = 'datetag', help = 
                "Set the datetag of the result's file",
                default = strftime("%Y-%m-%d", gmtime()), type = str)
    return parser.parse_args()

args = arg_parse()
print('\n Initializing')

# parameters
root = args.root
N_total_trials = args.n_total_trials
fixation_length = args.fixation_length  # length of fixation, in second
stim_length = args.stim_length   # length of stim, in second
to_test = args.to_test 
fullscr = args.fullscr 
datetag = args.datetag
HOST = args.HOST
mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])
transforms_norm =  transforms.Normalize(mean=mean, std=std) # to normalize colors on the imagenet dataset
# transform function for DCNN input's image processing
transform_serre = transforms.Compose([
    transforms.ToTensor(),    # Convert the image to PyTorch Tensor data type.
    transforms_norm ]) #Normalizœe the image 

path_serre_in = '/Users/jjn/Desktop/Serre_2007'
image_dataset_serre = datasets.ImageFolder(path_serre_in, transform=transform_serre) # save the dataset 
save_file = f'{datetag}_results_psycho_serre_{HOST}.json'
df_test = pd.DataFrame([], columns=['answer', 'time', 'correct', 'filename']) 
# TODO generate/get stim
    
if to_test:
    exp_observer = input('What is your name? ')
    from psychopy import  event, core,  visual

    win = visual.Window([1400, 800], fullscr=fullscr, color=[0, 0, 0])
    mouse = event.Mouse(newPos=(0, 0), visible=False)
    x0, y0 = mouse.getPos()
    event.clearEvents()
    
    instructions = """
    At each trial you see one natural scene, report if you percieve an animal.

    Move the mouse to the right if there is an animal in the scene,
    move the mouse to the left if there is an no animal in the scene.

    Move the mouse to begin the experiment.
    """
    msg = visual.TextStim(win, text=instructions, alignHoriz='center', alignVert='center', color='black')
    msg.draw()
    win.flip()
    while not mouse.mouseMoved(distance=.05): 
        event.clearEvents()
    fixation = visual.TextStim(win, text='Ready?', alignHoriz='center', alignVert='center', color='black')
    
    bitmap = visual.ImageStim(win, image_dataset_serre.imgs[0][0], mask='gauss', size=0.8, units='height', interpolate=True)
    bitmap.autolog = False 
    
    start_time = time.time()
    print("Test started")
    msg.setText('+')
    N_trial = 3
    # run experiment
    for i_trial in range(N_total_trials):
        clock = core.Clock()
        if i_trial % N_trial:
            fixation.setText(f'{i_trial:03d}/{N_total_trials:03d}')
        else:
            fixation.setText(f'.')
        fixation.draw()
        win.flip()
        original_image = image_dataset_serre.imgs[i_trial][0]
        bitmap.setImage(original_image)

         # Times the trial
        while clock.getTime() < fixation_length + stim_length:
            if clock.getTime() < fixation_length:  # fixation
                fixation.draw()
            elif clock.getTime() < fixation_length + stim_length: 
                bitmap.draw()
            win.flip()
        
        mouse.setPos(newPos=(0, 0))
        mouse.setVisible(True)
        x0, y0 = mouse.getPos()
        event.clearEvents()
        
        msg.draw()
        win.flip()

        while not mouse.mouseMoved(distance=.015): 
            # this creates a never-ending loop
            # until we move the mouse
            event.clearEvents()
        mouse.setVisible(False)

        dt = clock.getTime()

        x, y = mouse.getPos()
        if x < 0:
            answer = 'distractor'
        else: #elif x > 0:
            answer = 'animal'
            if x == 0: print('this should not happen 😤')
        event.clearEvents() 

        ans = event.getKeys() 
        
        if ans == ['escape', 'q']:
            win.close()
            core.quit()
        correct = 'animal' if 'animal' in image_dataset_serre.imgs[i_trial][0] else 'distractor'
        print('At trial ', i_trial, 'your answer is ',  answer, '(correct=', correct, ');')   
        df_test.loc[i_trial] = {'answer':answer, 'time':dt, 'correct':correct, 'filename':image_dataset_serre.imgs[i_trial][0]}
    print('saving')

    df_test.to_json(save_file)

    print('exiting')
    event.clearEvents() 
    win.close()
    core.quit()       
