# example script for using PyGaze

# # # # #
# importing the relevant libraries
#import time
import numpy
import constants
import pygame
import os
from pygaze import libscreen
from pygaze import libsound
from pygaze import libtime
from pygaze import eyetracker
from pygaze import liblog
from pygaze import libgazecon

# # # # #
# test the experimeny

# # # # #
# experiment setup

# create display object
disp = libscreen.Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# Logfile
log = liblog.Logfile()

# screen size and white box (wb) locations
dispx = constants.DISPSIZE[0]
dispy = constants.DISPSIZE[1]

wb = dispx * .266
xl = dispx * .01
xr = dispx - (dispx * .01 + wb)
ya = (dispy - wb)/2

							
# create screens
# attention grabber screen
surface = pygame.image.load('stimuli/diamond2.png').convert()

#rotations = []
#for angle in range(73):
#	rotations.append(pygame.transform.rotate(surface, angle))
#	
# load auditory stimuli
attractor_sound = libsound.Sound(soundfile = 'stimuli/auditory stim/attractor.wav')


triplets = range(2)
triplets[0] = os.listdir('stimuli/auditory stim/wav_ABB')
triplets[1] = os.listdir('stimuli/auditory stim/wav_AAB')
numpy.random.shuffle(triplets[0])
numpy.random.shuffle(triplets[1])

tri_sounds = range(2)
tri_sounds[0] = []
for i in triplets[0]:
	tri_sounds[0].append(libsound.Sound(soundfile = 'stimuli/auditory stim/wav_ABB/' + i))

tri_sounds[1] = []
for i in triplets[1]:
	tri_sounds[1].append(libsound.Sound(soundfile = 'stimuli/auditory stim/wav_AAB/' + i))

puppets = os.listdir('stimuli/auditory stim/puppet_wav')
puppet_sounds = []
for i in puppets:
	puppet_sounds.append(libsound.Sound(soundfile = 'stimuli/auditory stim/puppet_wav/' + i))


# trial screens
bg = pygame.image.load('stimuli/background.png').convert()
#bg = pygame.transform.scale(bg, (dispx, dispy))
bgscr = libscreen.Screen()
bgscr.draw_image(bg)

## original stimuli screens
orim = []
reward = {}
files = os.listdir('frames')
for i in range(6):
	reward[i] = {}
	orim.append(i) 
	orim[i] = []
	f = os.listdir('frames/'+ files[i])
	f.sort()
	ii = 0
	for frame in f:
		orim[i].append(pygame.image.load('frames/'+ files[i] + '/' + frame).convert())
		reward[i][ii] = libscreen.Screen()
		reward[i][ii].draw_image(orim[i][ii])
		ii += 1

#reward = {}
#for i in range(6):
#	reward[i] = {}
#	for k in range(24):
#		reward[i][k] = libscreen.Screen()
#		reward[i][k].draw_image(orim[i][k])



# Define AOIs
caoi = libgazecon.AOI('circle', (dispx / 2, dispy / 2), 250)
laoi = libgazecon.AOI('circle', (dispx / 6, dispy / 2), size = dispx / 3)
raoi = libgazecon.AOI('circle', ((dispx / 6) * 5, dispy / 2), size = dispx / 3)

# left and right index for presenting reward
ileft = [0, 2, 4]
iright = [1, 3, 5]

# randomize order of ABB & AAB
triplet_order = numpy.random.randint(0, 2, 1)

# randomize left right order
if numpy.random.randint(0, 2, 1) == 0:
	left = True
else:
	left = False

block_trial = 0
# # # # #
# run the experiment

# calibrate eye tracker
tracker.calibrate()


# start the pre-switch trails
for trial in range(18):
	if trial == 9:
		if left:
			left = False
		else:
			left = True
		if triplet_order == 0:
			triplet_order = 1
		else:
			triplet_order = 0
		block_trial = 0
		
	# start eye tracking
	tracker.start_recording()
	tracker.status_msg("now running trial %d" % trial)
	tracker.log("start %d" % (libtime.clock.get_time()))

	# present attention getter
	scale = .01
	count = 0
	attractor_sound.play()
	bgscr.clear()
	bgscr.draw_image(bg)
	bgscr.draw_image(surface, scale = scale)
	disp.fill(bgscr)
	disp.show()

	t00 = libtime.clock.get_time()
	while (libtime.clock.get_time() - t00) < 400:
		scale += .005
		bgscr.draw_image(surface, scale = scale)
		disp.fill(bgscr)
		disp.show()

	inattention = True
	while inattention:
		#scale += .001
		bgscr.draw_image(surface, scale = scale)
		disp.fill(bgscr)
		disp.show()
		pos = tracker.sample()
		t0 = libtime.clock.get_time()
		if caoi.contains(pos):
			pos = tracker.sample()
			t1 = libtime.clock.get_time()
			while (t1 - t0) < 100 and caoi.contains(pos):
				pos = tracker.sample()
				t1 = libtime.clock.get_time()
			if (t1 - t0) > 100:
				inattention = False
				tracker.log_var('EVENT', 'start %d' % trial)
				tracker.log_var('EVENT_TIME', '%d' % libtime.clock.get_time())
													
		if (t0 - t00) > 1500:
			attractor_sound.play()
			bgscr.clear()
			bgscr.draw_image(bg)
			scale = .01
			bgscr.draw_image(surface, scale = scale)
			disp.fill(bgscr)
			disp.show()
			
			t00 = libtime.clock.get_time()
			while (libtime.clock.get_time() - t00) < 400:
				scale += .005
				bgscr.draw_image(surface, scale = scale)
				disp.fill(bgscr)
				disp.show()
				
			#t00 = libtime.clock.get_time()
			inattention = True
			count += 1
		if count == 5:
			tracker.stop_recording()
			tracker.calibrate()
			tracker.start_recording()
			count = 0

	# anticipation and cue period
	#play sounds
	t00 = libtime.clock.get_time()
	while (libtime.clock.get_time() - t00) < 1:
		tri_sounds[triplet_order][block_trial].play()

	anticipation = 'none'
	rt = 0
	#t00 = libtime.clock.get_time()
	time = libtime.clock.get_time() - t00
	while time < 2699:
		pos = tracker.sample()
		t0 = libtime.clock.get_time()
		if raoi.contains(pos):
			pos = tracker.sample()
			t1 = libtime.clock.get_time()
			while (t1 - t0) < 100 and raoi.contains(pos):
				pos = tracker.sample()
				t1 = libtime.clock.get_time()
			if (t1 - t0) > 100:
				anticipation = 'right'
				if rt == 0:
					rt = (t1 - t00) - 1800
		t0 = libtime.clock.get_time()
		if laoi.contains(pos):
			pos = tracker.sample()
			t1 = libtime.clock.get_time()
			while (t1 - t0) < 100 and laoi.contains(pos):
				pos = tracker.sample()
				t1 = libtime.clock.get_time()
			if (t1 - t0) > 100:
				anticipation = 'left'
				if rt == 0:
					rt = (t1 - t00) - 1800
		time = libtime.clock.get_time() - t00
		if time > 1699:
			# remove star when triplets end
			bgscr.clear()	
			bgscr.draw_image(bg)
			disp.fill(bgscr)
			disp.show()

	# reward period
	t00 = libtime.clock.get_time()
#	bgscr.clear()	
#	bgscr.draw_image(bg)
#	disp.fill(bgscr)
#	disp.show()
	
	ii = numpy.random.randint(0,3,1)
	if left:
		iindex = ileft
	else:
		iindex = iright

	tracker.log_var('EVENT', 'reward %d' % trial)
	tracker.log_var('EVENT_TIME', 'time %d' % libtime.clock.get_time())

	while (libtime.clock.get_time() - t00) < 1700:
		puppet_sounds[ii].play() 
		#libtime.pause(50)
		#print libtime.clock.get_time()
		k = 0 #frame_count
		disp.fill(reward[iindex[ii]][k])
		ft = disp.show()
		
		while k < 23:
			k += 1
			disp.fill(reward[iindex[ii]][k])
			ft = disp.show()
			libtime.clock.pause(40)
	
	# prepare for next trial with background screen
	disp.fill(bgscr)
	disp.show()

	# log stuff
	log.write([trial + 1, left, pos, anticipation, rt, triplets[triplet_order][block_trial], puppets[ii]])
	block_trial += 1
	
	tracker.stop_recording()

# end the experiment
tracker.close()
log.close()
disp.close()