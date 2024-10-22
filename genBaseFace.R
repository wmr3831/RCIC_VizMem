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
imName <- "basePre.jpg"
writeDir <- "./"
outName <- "base"
imForm <- "jpg"
imDims <- 512

# Load image to be formated
b_img <- read_stim(imName)

#plot(b_img)

# p_img <- b_img %>%
#   auto_delin(model = "fpp106", replace = T)
  #align(procrustes = T)

# Format image -----------------------------------------------------------------

# Resize image to imDims and convert to grayscale
p_img <- b_img %>%
  resize(width = imDims, height = imDims) %>%
  greyscale()

# Display formated image
plot(p_img)

# Write stim to writeDir
write_stim(p_img, dir = writeDir, names = c(outName), format = imForm, overwrite = T)

#draw_tem(p_img)
#plot(p_img)
  