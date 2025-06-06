# Exporting the current iOS lock screen wallpaper

[中文](README.md)

This repository provides Python and Node.js scripts to convert `cpbitmap` files
extracted from an iOS backup into regular PNG images.

## Background

When you set a photo as your iPhone wallpaper and later delete that photo, you
can still recover it from a device backup. The general steps are:

1. Back up your iPhone using iTunes.
2. Use a tool such as iPhone Backup Extractor to export the home directory
   from the backup.
3. Locate the `cpbitmap` files that store the wallpapers and convert them with
   the scripts in this repository.

## Step 1 Backup

1. Back up your device in iTunes. You may need to update iTunes to a version compatible with your iOS.
2. Choose to store the backup locally.

## Step 2 Extract files from the backup

1. Run your backup extraction tool and select the exported home directory.
2. Find the lock screen wallpaper `cpbitmap` file (the home screen uses the same
   format if present).

## Step 3 Convert using Python or JS

1. Pick either the Python or JS script.
2. Install dependencies:
   1. Python: `pip install -r python/requirements.txt`
   2. JS: `npm install`
3. Run the converter:
   1. Python: `python python/convert_cpbitmap.py {source} {destination}`
   2. JS: `node js/index.js {source} {destination}`

## Notes

The cpbitmap format changed around iOS 11, so many older tools no longer work.
The format features 16-pixel row alignment with BGRA pixel order. See the
`samples` directory for examples of incorrect conversions.

## References

* Discussion of wallpaper dimensions:
  <https://forums.macrumors.com/threads/iphone-6-plus-wallpaper-dimensions.1775299/page-2>
* Related gists:
  <https://gist.github.com/sillygwailo/6631402>
* StackOverflow answer detailing the file format:
  <https://stackoverflow.com/questions/7998324/dot-cpbitmap-images-imgaename-cpbitmap/48158807#48158807>
* Additional example code:
  <https://gist.github.com/sfan5/8280735>
