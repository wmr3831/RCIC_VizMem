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
library(purrr)
library(tools)

# Set parameters
im_dir <- './grayStim' 
stim_path <- './img'
stim_seed <- 1729
num_trials <- 100
im_size <- 512
lab <- "stim"

#trace(generateStimuli2IFC, edit=T)
base_imgs <- list.files(im_dir, pattern = "*.jpg", full.names = T)
img_names <- list.files(im_dir, pattern = "*.jpg", full.names = F)
img_names <- gsub("\\..*","", img_names)


# Generate stimuli -------------------------------------------------------------


# Run garbage collection to free memory
gc()


# Generate stimuli
# @param ncores number of cpu cores dedicated to task
# If script runs into memory errors/crashes, set ncores = 1
# for (x in 1:length(base_imgs)) {
#   y <- list(base_imgs[x])
#   names(y) <- img_names[x]
#   generateStimuli2IFC(base_face_files = y, noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 4)
# }


generateStimuli2IFC(base_face_files = list(stim1 = base_imgs[1]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim2 = base_imgs[2]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim3 = base_imgs[3]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim4 = base_imgs[4]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim5 = base_imgs[5]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim6 = base_imgs[6]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim7 = base_imgs[7]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim8 = base_imgs[8]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim9 = base_imgs[9]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim10 = base_imgs[10]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim11 = base_imgs[11]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim12 = base_imgs[12]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim13 = base_imgs[13]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim14 = base_imgs[14]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)
generateStimuli2IFC(base_face_files = list(stim15 = base_imgs[15]), noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 2)

# lapply(base_imgs, function (x) {
#   y <- list(x)
#   name <- gsub("\\..*","", file_path_sans_ext(x))
#   print(name)
#   names(y) <- c()
#   print(y)
#   #generateStimuli2IFC(base_face_files = y, noise_type = 'sinusoid', label = lab, n_trials = num_trials, img_size = im_size, stimulus_path = stim_path, seed = stim_seed, ncores = 4)
# })



