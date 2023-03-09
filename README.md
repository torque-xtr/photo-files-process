# photo-files-process
scripts for batch photo processing

PV renamer renames photos and video files into currently accepted format like "IMG_date_time" according to EXIF "data taken" or "date modified" data (if EXIF is absent). Original file name is appended to the end of format string.

PV_back_rename does just the reverse, if filename has template string with _orig_ attached after it.
