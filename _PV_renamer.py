#this script performs batch rename of photo and video files to the current widely accepted template, 
#XXX_YYYYMMDD_HHMMSS, where XXX - IMG or VID, YMD and HMS - date and time.
#No more confusion by multiple different DSC00001's in your photo archive!
#The script checks if the existing photo and video file names in a folder conform to the template. 
#If not, it extracts the date and time from exif or file properties and performs renaming.

import os
import time
from PIL import Image
#from datetime import datetime

ph_ext = ('jpg', 'jpeg', 'raw', 'nef', 'dng', 'cr2') #extensions of photo files. Easily added if needed.
vid_ext = ('3gp', 'mov', 'mp4', 'mpg') #the same for video. Capitalized extensions processed below.

def ftype(pv_file): #determines if a file is photo, video or other type.
 f_type = 'other'
 pt_index = pv_file.rfind('.')
 f_ext = pv_file[pt_index:].strip('.').casefold()
 if f_ext in ph_ext:
  f_type = 'IMG'
 elif f_ext in vid_ext:
  f_type = 'VID'
 return f_type 


def is_template(pv_file): #determines if a file name conforms to template
 pt_index = pv_file.rfind('.')
 f_name = pv_file[:pt_index] #extracts file name 
 f_ext = pv_file[pt_index:].strip('.').casefold() #extracts extension and decapitalizes it 
 f_parts = f_name.split('_') #
 f_type = ftype(pv_file)
 istemplate = False
 if f_type == 'other':
  return f_type, istemplate, f_name, f_ext
 #checks if file name contains correct parts separated by underscores and 1st part corresponds to file type (IMG or VID)
 if f_type != 'other' and len(f_parts) >= 3 and len(f_parts[1]) == 8 and len(f_parts[2]) == 6 and f_parts[0] == f_type: 
  istemplate = True
 return f_type, istemplate, pv_file, f_name, f_ext


def date_extract(pv_file, *args): #date extraction. Uses exif if exists and file 'modified time' if not.
 data_modified = os.path.getmtime(pv_file) 
 tt_loc = time.localtime(data_modified) 
 data_mod = time.strftime("%Y%m%d_%H%M%S", tt_loc)
 dates = [data_mod] #for photos, exifs are added into list
 f_type = args[0] if len(args) > 0 else ftype(pv_file)
 if f_type != 'IMG':
  print(dates)
 else: #extract exifs, compare with data_mod, return earliest exif date # exif tags: https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
  try:
   exif = Image.open(pv_file)._getexif() #36867 - orig, 36868 - digitized, 306 - datetime # https://exiftool.org/TagNames/EXIF.html
  except AttributeError:
   exif = dict(Image.open(pv_file).getexif())
  except:
   exif = {}
  exif_keys = {} if type(exif) != dict else exif.keys() #check for missing exifs
  if 36867 in exif_keys:
   dt_orig = exif[36867] # format '2008:02:19 19:26:36'
   dt_orig = dt_orig.replace(':', '').replace(' ', '_')   #easier to convert the exif date format straight to template string.
   if dt_orig[8] == '_' and dt_orig[:8].isdigit() and dt_orig[9:].isdigit() and len(dt_orig) == 15: #checking the result thoroughly.
    dates.append(dt_orig)
  if 36868 in exif_keys:
   dt_dig = exif[36868] 
   dt_dig = dt_dig.replace(':', '').replace(' ', '_')   
   if dt_dig[8] == '_' and dt_dig[:8].isdigit() and dt_dig[9:].isdigit() and len(dt_dig) == 15:
    dates.append(dt_dig)
  if 306 in exif_keys:
   dt_dt = exif[306] 
   dt_dt = dt_dt.replace(':', '').replace(' ', '_')   
   if dt_dt[8] == '_' and dt_dt[:8].isdigit() and dt_dt[9:].isdigit() and len(dt_dt) == 15:
    dates.append(dt_dt)
  print(dates)
 return dates[0] if len(dates) == 1 else min(dates[1:]) #earliest exif if any exists or date modified if not.
 #counting on strict xxxxxxxx_xxxxxx format! #if any exif, we trust it.


def filerename(pv_file):
 istempl = is_template(pv_file)  
 file_type = istempl[0]
 is_templ = istempl[1]
 templ_name = 'other'
 if not is_templ and (file_type == 'IMG' or file_type == 'VID'):
  t_str = date_extract(pv_file, file_type) #already formatted  # use exif or modified if no exif data! 
  templ_name = '"' + file_type + '_' + t_str + '_orig_' + pv_file + '"'
  cmd_os = 'rename' + ' "' + pv_file + '" ' + templ_name
  os.system(cmd_os) #sources are on HDD backup # better make copy, then sort manually and move orig to orig folder
 return_str = pv_file + '\t' + templ_name
 print(return_str)
 return return_str


file_list = os.listdir()
rename_log = [] 
for file_cur in file_list: #loops over all files in a folder. We're not going into subfolders in this version.
 templ_string = filerename(file_cur)
 rename_log.append(templ_string) 

rename_log.sort() #sort by name
with open ('__img_table_srt.csv', 'w') as tbl: #creates log txt with and new names
 for i in range(len(rename_log)):
  tbl.write(rename_log[i] + '\n')
 
