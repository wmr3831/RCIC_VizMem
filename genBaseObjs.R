# Details ----------------------------------------------------------------------
#
# @title genBaseFace
# @details Format base image for RC stimulus generation
# @author Willow Rose (ejb3831@rit.edu)
#
# References -------------------------------------------------------------------
#
# @libraries
# DeBruine, L. (2022). webmorphR: Reproducible Stimuli. R library. 
# https://zenodo.org/badge/latestdoi/357819230
#
# Parameters -------------------------------------------------------------------
#
# @param imName image file name to be formated
# @param writeDir directory to write output image
# @param outName output image name
# @param imForm image output format
# @param imDims stimulus image dimensions in pixels, should always be a square
#
# Output -----------------------------------------------------------------------
#
# @return nothing, output image saved to writeDir

# Setup ------------------------------------------------------------------------

# Load libraries
library(webmorphR)
library(dplyr)

# Set parameters
imDir <- "./stimuli/baseImgs"
writeDir <- "./grayStim"
outName <- "base"
imForm <- "jpg"
imDims <- 512

# Load image to be formated
files <-read_stim(imDir)

#plot(b_img)

# p_img <- b_img %>%
#   auto_delin(model = "fpp106", replace = T)
  #align(procrustes = T)

# Format image -----------------------------------------------------------------


stim_names <- lapply((1:length(files)), function (x) {paste("stim", x, sep = '_')})
for(x in 1:length(stim_names)) {
  files[x] %>% resize(width = imDims, height = imDims) %>% greyscale() %>% write_stim(dir = writeDir, names = stim_names[x], format = imForm, overwrite = T)
}
# Resize image to imDims and convert to grayscale
# lapply(files, function (x) {
#   x %>% resize(width = imDims, height = imDims) %>% greyscale() %>% write_stim(dir = writeDir, names = stim_names, format = imForm, overwrite = T)
# })


  