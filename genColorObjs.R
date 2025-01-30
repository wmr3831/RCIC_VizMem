library(magick)

imDir <- "./grayStim"
writeDir <- "./colorStim"
file_ext <- ".jpg"

base_imgs <- list.files(imDir, pattern = "*.jpg", full.names = T)
im_names <- list.files(imDir, pattern = "*.jpg", full.names = F)
im_names <- gsub("\\..*","", im_names)
imgs <- lapply(base_imgs, function (x) {image_convert(image_read(x), colorspace = 'rgb')}) 

mapply(function(x, y) {
  for(i in c(1:180)) {
    rotation <- i/180
    pos <- image_modulate(x, brightness = 100, saturation = 100, hue = 100 + rotation)
    neg <- image_modulate(x, brightness = 100, saturation = 100, hue = 100 - rotation)
    image_write(pos, paste(writeDir, "/", y, "_d", i, file_ext, sep = ''), format = "jpg")
    image_write(neg, paste(writeDir, "/", y, "_d", 360 - i, file_ext, sep = ''), format = "jpg")
  }
}, imgs, im_names)