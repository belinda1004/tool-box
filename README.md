# tool-box
The small but useful tools that I wrote.

# 1. Convert images to pdf file
  convert_images_to_pdf.py
  - The user specifies the path of the images and the file name of the target PDF file
  - If the target file already exists, the user can choose to overwrite it or re-specify the target file name
  - The user can also choose to convert all images in the specified path, or confirm all images in the specified path one by one
  
# 2. Dictionary
  spider_dictionary.py
  - Source: https://www.dictionary.com/
  
# 3. Weather forecast
  spider_weather.py
  - Source: https://www.weather.com.au/, https://auspost.com.au/
  - Get forecast for main cities of Australia.
  - Query detailed forecast by postcode
  
# 4. Random quotes
  spider_randomQuotes.py
  - Source: https://www.goodreads.com/
  - Generate a random quote.

# 5. For MAC/IPhone users, convert the creation time and last modified time to the original shooting time for the exported photoes. 
  mac_get_original_time_for_export_photo_video.py
 MAC users always find that when we export photos/videos from "Apple Photo", if we want to get the photos in the familiar formats (jpeg, tiff or png), or get more customized export photos, we can not use the "Export Unmodified Original" option. The exported photos' creation time are the current time that we do the export, but not the original shooting time. 
 This script works to recovery the creation time and last modified time in the photo/video property to the actual shooting time.
