# Details ----------------------------------------------------------------------
# 
# @title genStim
# @details Generate stimuli for 2IFC reverse correlation task
# @author Willow Rose (ejb3831@rit.edu)
#
# References -------------------------------------------------------------------
#
# @libraries
# Ron Dotsch (2016). rcicr: Reverse correlation image classification toolbox.
# R package version 0.3.4.1. 
#
# Parameters -------------------------------------------------------------------
# 
# @param base_img base image for stimulus generation
# @param stim_path path to directory to save stimulus images
# @param stim_seed noise seed for reproducable results
# @param num_trials number of trials to generate stimuli images for
# @param im_size size of base image in pixels
# @param lab labels for output stimuli
# 
# Output -----------------------------------------------------------------------
#
# @return nothing, stimuli images saved to stim_path

# Setup ------------------------------------------------------------------------

# Load libraries
library(rcicr)

# Set parameters
base_img <- list('base' = 'base.jpg')
stim_path <- './img'
stim_seed <- 1974
num_trials <- 300
im_size <- 512
lab <- "stim"

#trace(generateStimuli2IFC, edit=T)

# Generate stimuli -------------------------------------------------------------

# Run garbage collection to free memory
gc()

# Generate stimuli
# @param ncores number of cpu cores dedicated to task
# If script runs into memory errors/crashes, set ncores = 1
generateStimuli2IFC(base_face_files = base_img, noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores=1)

