#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script transforms the full size training and test images
provided as part of the original data set into two sets of
lower resolution images more suitable for learning.
"""
from numbers import Number
from PIL import Image
import os
import glob

def make_thumbnails_of_folder(folder_path, output_size, 
                              output_folder=None, verbose=False):
    """
    Creates a new thumbnail images for each file in a folder.
    
    Note that images that have already been converted will not
    be processed again, so it is safe to run this method twice on
    the same folder.
    
    Parameters
    ----------
    folder_path: str
        Path to the folder in which the images reside
    
    output_size: tuple (width, height)
        The dimensions of the output images in pixels
        
    output_folder: [optional] str
        An optional path to an output folder. If None (default) then
        the images will be saved in `folder_path`
    
    verbose: bool [False]
        If True, prints progress for each file as they are processed.
        False by default.
    
    Returns
    -------
    output_files: list of str
        A list of filepaths for all the images that were created.
    """
    # Check input
    assert os.path.exists(folder_path), "input folder_path {} does not exist".format(folder_path)
    assert type(output_size) == tuple, "output_size must be a tuple with two entries, (width, height)"
    assert len(output_size) == 2, "output_size must be a tuple with two entries, (width, height)"
    assert isinstance(output_size[0], Number), "The first element of output_size was not a number"
    assert isinstance(output_size[1], Number), "The second element of output_size was not a number"
    
    # Determine where the images will be saved
    folder_path = os.path.abspath(folder_path)
    if output_folder != None and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    elif output_folder == None:
        output_folder = folder_path
    
    # Determine the file extension for each output filed
    width, height = output_size
    suffix = "_{}x{}.png".format(width, height)
    
    # Get all of the images from within the folder. Make sure to skip images 
    # that contain the suffix because that means they've already been converted
    input_files_all = glob.glob(os.path.join(folder_path, "*.png"))
    input_files = [f for f in input_files_all if suffix not in f]
    print(len(input_files_all))
    output_files = []
    if verbose:
        print("Converting {} files...".format(len(input_files)))
        
    for idx, input_image_path in enumerate(input_files):
    
        # Determine the output filepath
        filename = os.path.basename(input_image_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_folder, name + suffix)
        if os.path.exists(output_path):
            if verbose:
                print("\tSkipping {} because it has already been converted".format(filename))
            continue
        
        # Convert and save the image
        if verbose:
            print("\tFile: {}\tof\t{}".format(idx, len(input_files)))
        img = Image.open(input_image_path)
        img.thumbnail(output_size)
        img.save(output_path)
        
        # Append the file to the list of output files to be returned
        output_files.append(output_path)
    
    # All done!
    if verbose:
        print("Finished converting {} files!".format(len(output_files)))
    return output_files
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The folders you want to process")
    parser.add_argument("width", help="The width of the output image thumbnails", type=int)
    parser.add_argument("height", help="The height of the output images thumbnails", type=int)
    parser.add_argument("-o", "--output", help="The folder the output images will be saved in")
    parser.add_argument("-s", "--silent", help="Do not show any progress output", action="store_true")
    args = parser.parse_args()

    make_thumbnails_of_folder(folder_path=args.input, 
                              output_size=(args.width, args.height), 
                              output_folder=args.output,
                              verbose=not args.silent)