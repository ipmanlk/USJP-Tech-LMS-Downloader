import requests
import re
import os
from bs4 import BeautifulSoup
from pathlib import Path

###################################################################
##                        CONFIGURATION                          ##
###################################################################

# CREDENTIALS
LMS_USERNAME = "put your lms username here"
LMS_PASSWORD = "put your lms password here"

# COURSES
COURSES = {
    "Networking Essentials": "https://lms.tech.sjp.ac.lk/course/view.php?id=183",
}

# download directory for PDFs
DOWNLOAD_DIRECTORY = Path("./downloads/pdf/")

###################################################################
##                                                               ##
###################################################################

# settings
payload = {
    "username": LMS_USERNAME,
    "password": LMS_PASSWORD
}

session_requests = requests.session()

login_url = "https://lms.tech.sjp.ac.lk/login/index.php"
response = session_requests.post(login_url, data=payload)

print("Log: LMS login completed.")

# list to store pdf links
pdfs = {

}

for course_name, course_url in COURSES.items():
    print("Log: Checking for course directory inside the download directory: " + course_name)

    # if directory for each course is not present, make those
    if not(os.path.isdir(DOWNLOAD_DIRECTORY / course_name)):
        os.mkdir(DOWNLOAD_DIRECTORY / course_name)

    print("Log: Grabbing PDF links from " + course_name)

    # request course page
    r = session_requests.get(course_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # hyperlinks in the page
    a_tags = soup.findAll(
        src="https://lms.tech.sjp.ac.lk/theme/image.php/klass/core/1592306653/f/pdf-24")

    # gather pdf links
    for a_tag in a_tags:
        if (course_name not in pdfs):
            pdfs[course_name] = []
        pdfs[course_name].append(a_tag.parent["href"])

print("Log: PDF link gathering completed.")


# download pdfs files
for course_name, pdf_links in pdfs.items():
    print("Log: Downloading PDFs form " + course_name)
   
    for pdf_link in pdf_links:
        # check if pdf file is already downloaded
        with open(DOWNLOAD_DIRECTORY / "log.txt", 'r') as log_file:
            log_file_content = log_file.read()
            
            if (pdf_link in log_file_content):
                print("Log: This PDF is already downloaded : " + pdf_link)
                continue
        
        print("Log: Downloading : " + pdf_link)
                
        # download pdf to memory
        r = session_requests.get(pdf_link)
        
        # extract content-disposition from headers
        d = r.headers['content-disposition']

        # extract filename from content-disposition info
        pdf_file_name = re.findall("filename=(.+)", d)[0]
        pdf_file_name = pdf_file_name[:-1]
        pdf_file_name = pdf_file_name[1:]

        # path to save pdf file
        pdf_file_path = DOWNLOAD_DIRECTORY / course_name / pdf_file_name

        # write pdf to the disk
        pdf_file = open(pdf_file_path, "wb")
        pdf_file.write(r.content)
        pdf_file.close()

        # write a log as pdf downloaded (to skip duplicate downloads)
        log_file = open(DOWNLOAD_DIRECTORY / "log.txt", "a")
        log_file.write(pdf_link + "\n")
        log_file.close()


print("Downloading completed!.")
