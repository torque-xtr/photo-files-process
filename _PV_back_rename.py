#delete template from file name if renamed not correctly. Reverses PV_renamer results. Leaves [25:] part of a name if not empty.
import os

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
 
file_list = os.listdir()
i = 0
for fname in file_list:
 i += 1
 if is_template(fname)[1] and '_orig_' in fname: #checks if the file has been renamed. Leaves genuine template names intact.
  os.system('rename' + ' "' + fname + '" "' + fname[25:] + '"') #double quotes for file names containing spaces etc
  print(i, '\t', fname, '\t', fname[25:])
