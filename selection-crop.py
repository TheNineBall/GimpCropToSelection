#!/usr/bin/env python
from gimpfu import *
import os

'''crops image and saves the crop coordinates in crop.txt (same path as the image)'''
def cropSelection(image):
    selection,x1,y1,x2,y2=pdb.gimp_selection_bounds(image)
    name = os.path.basename(image.filename)
    path = os.path.dirname(image.filename)
    if not selection:
        pdb.gimp_message("No selection")
    else:
        #gimp.message('L=%d\nU=%d\nR=%d\nD=%d' % (x1,y1,x2-x1,y2-y1))
        try:
            f = open(os.path.join(path, "crop.txt"), 'a+')
        except IOError:
            f = open(os.path.join(path, "crop.txt"), 'w')
        f.write('%s\t%d\t%d\t%d\t%d\n' % (name,x1,y1,x2-x1,y2-y1))
        f.close()    
        image.resize(x2-x1, y2-y1, -x1, -y1)
    pdb.gimp_displays_flush()
    layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(image, layer, image.filename, image.filename)
    display=gimp._id2display(image.ID)
    pdb.gimp_display_delete(display)


### Registration
desc='Crop Selection'
register(
    'Crop',
    desc,
    desc,
    '',
    '',
    '2019',
    desc,
    '*',
    [(PF_IMAGE, "image", "Input image", None)],[],
    cropSelection,menu="<Image>/Select")

main()