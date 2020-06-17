###################################################################
##                        CONFIGURATION                          ##
###################################################################

# CREDENTIALS
LMS_USERNAME = "put your lms username here"
LMS_PASSWORD = "put your lms password here"

# COURSES
COURSES = {
    "Networking Essentials": "https://lms.tech.sjp.ac.lk/course/view.php?id=183",
    "Web Application Development":"https://lms.tech.sjp.ac.lk/course/view.php?id=188"
}

# download directory for videos
DOWNLOAD_DIRECTORY = "./downloads/"

###################################################################
##                                                               ##
###################################################################


import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

# settings
payload = {
    "username": LMS_USERNAME,
    "password": LMS_PASSWORD
}

session_requests = requests.session()

login_url = "https://lms.tech.sjp.ac.lk/login/index.php"
response = session_requests.post(login_url, data=payload)

print("Log: LMS login completed.")

# list to store video links
vids = {

}

for course_name, course_url in COURSES.items():
    print("Log: Checking for course directory inside the download directory: " + course_name)

    # if directory for each course is not present, make those
    if not(os.path.isdir(DOWNLOAD_DIRECTORY + course_name)):
        os.mkdir(DOWNLOAD_DIRECTORY + course_name)

    print("Log: Grabbing video links from " + course_name)

    # request course page
    r = session_requests.get(course_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # hyperlinks in the page
    a_tags = soup.findAll(
        src="https://lms.tech.sjp.ac.lk/theme/image.php/klass/core/1592306653/f/mpeg-24")

    # get video links (in differnt pages)
    for a_tag in a_tags:
        vid_page = a_tag.parent["href"]
        vid_page_html = session_requests.get(vid_page)
        vid_soup = BeautifulSoup(vid_page_html.text, "html.parser")
        vid_source_tags = vid_soup.findAll("source")

        for vid_source_tag in vid_source_tags:
            if (course_name not in vids):
                vids[course_name] = []
            vids[course_name].append(vid_source_tag["src"])

    # get video links (in same page)
    vid_source_tags = soup.findAll("source")
    for vid_source_tag in vid_source_tags:
        if (course_name not in vids):
            vids[course_name] = []
        vids[course_name].append(vid_source_tag["src"])

print("Log: Video link gathering completed.")


# download video files
for course_name, vid_links in vids.items():
    print("Log: Downloading videos form " + course_name)
    for vid_link in vid_links:

        # get video filename from url
        vid_file_name = os.path.basename(vid_link)

        # download path for the video file
        vid_file_path = DOWNLOAD_DIRECTORY + course_name + "/" + vid_file_name

        print("Log: Checking if " + vid_file_name + " already exists.")

        # check if file already exists
        if (os.path.isfile(vid_file_path)):
            print("Log: This file already exists. Delete current file if you want to download again.")
            continue;
        
        print("Log: Downloading " + vid_file_name)

        # request the file 
        r = session_requests.get(vid_link, stream=True)

        # for download progress
        total_size = int(r.headers.get('content-length', 0))
        block_size = 16 * 1024

        # download progress bar
        t = tqdm(total=total_size, unit='iB', unit_scale=True)

        # download files chunks
        with open(vid_file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=block_size):
                t.update(len(chunk))
                f.write(chunk)
        
        # close progress bar
        t.close()

print("Downloading completed!.")
