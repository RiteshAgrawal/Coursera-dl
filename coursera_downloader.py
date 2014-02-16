import urllib2
import time
import re
import subprocess
from collections import OrderedDict

course_url = "https://class.coursera.org/datasci-001/lecture/preview"
page_contents = urllib2.urlopen(course_url)
section_identifier = "course-item-list-header expanded"
url1_identifier = "data-modal-iframe"
url2_identifier = "video/mp4"
section_number=0
part_number=0
data_url1 = OrderedDict()

regular_exp = "[A-Z]*[a-z]*\(\d\d*:\d\d*\)</a>"		
########################################################
#		   WARNING			       #
#It will not select files which don't have time in them#
########################################################


for line in page_contents.readlines():
    if section_identifier in line:
    	section_number+=1
    	part_number = 0
    if url1_identifier in line:
    	part_number+=1
    	url = line.split("\"")
    	url1 = url[1]
    if re.search(regular_exp,line):
	file_name = line.split("</a>")[0]
	file_full_name = str(section_number) + " - " + str(part_number) + " " + file_name
	data_url1[file_full_name] = url1

for file_full_name,url1 in data_url1.items():
	video_url_contents = urllib2.urlopen(url1)
	for line in video_url_contents:
	    if url2_identifier in line:
	    	url = line.split("\"")
	    	url2 = url[3]
	   	print "Fetching video :" +  file_full_name + "\nPlease wait................................................"
		subprocess.call(["wget","--output-document", file_full_name,url2])

