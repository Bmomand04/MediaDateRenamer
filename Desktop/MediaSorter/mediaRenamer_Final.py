import os
import exiftool
import json

#Brishna Momand
#----------------------------------------------------------------------------------------------------------------------------------------
#Media Renamer Script
#This script renames each picture or video to the date it was originally taken/filmed by reading it's EXIF tag
#For example, 'image1' was originally taken May 2, 2025 - 'image1' will be titled 'MAY2_2025' or 'DEC14_2004'. Format : (MONTHDAY_YEAR)
#Makes it a lot more easy and clear to see date of media when scrolling through large folders
#----------------------------------------------------------------------------------------------------------------------------------------

#os.mkdir("Test") #creates single directory
#os.makedirs("2025/Janurary/Vacation") #nested folders in dir
#os.mkdir("singlefolder")
#os.rmdir("singlefolder") #delete directory
#flag = my_image.has_exif # bool for if media has exif
#print(flag) if media has exif tags
#print(dir(my_image)) #lists all exif tags (not specific to media)


folder_path = r"C:\Users\user\Desktop\MediaSorter\Test"
with exiftool.ExifToolHelper() as et:
    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        # Skip if not a file
        if not os.path.isfile(old_path):
            continue
        metadata_str = et.execute("-j", old_path)
        metadata_list = json.loads(metadata_str)
        metadata = metadata_list[0]

        # Get original date
        date = metadata.get("EXIF:DateTimeOriginal") or metadata.get("QuickTime:CreateDate")
        if not date:
            print(f"{filename}: No original date found, skipping")
            continue

        #print('\n',date)
        split = date.split(':')
        #print(split)

        months_short = {'01' : 'JAN','02' : 'FEB','03' : 'MAR', '04' : 'APR', '05' : 'MAY', '06' : 'JUN',
                '07' : 'JUL','08' : 'AUG','09' : 'SEP','10' : 'OCT','11' : 'NOV','12' : 'DEC'}

        new_name = ""
        DAY = ""
        UNDERSCORE = "_"
        split_name = filename.split('.')
        EXT = '.' + split_name[-1]

        MONTH = str(split[1])

        DAY_PREV = str(split[2])
        i = 0
        while i < 2:
            DAY += DAY_PREV[i]
            i += 1

        YEAR = str(split[0])


        new_name += months_short[MONTH]
        new_name += DAY
        new_name += UNDERSCORE
        new_name += YEAR
        new_name += EXT

        #print(new_name)

        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)

