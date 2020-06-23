## USJP-Tech-LMS-Downloader
_Download and sync online lecture videos & PDFs from Japura Tech LMS to your local machine easily!._

### Features
- Automatically download all lecture PDFs.
- Automatically download all lecture videos.
- Skip already downloaded lectures (can be used to keep your local copy in sync with LMS one).

### Prerequisites
- Python 3 or above ([Download](https://www.python.org/)).
- pipenv ([Download](https://pipenv.pypa.io/en/latest/)).


### Instructions
1. Download this repository using ``git clone`` or zip download option.
2. Navigate to downloaded directory in your terminal.
3. Run ``pipenv shell`` and then ``pipenv install`` to install dependencies.
4. Open ``download_pdf.py`` or ``download_video.py`` with your text editor.
5. Under ``CONFIGURATION`` put your username and password.
6. Then, copy course urls you want to download/keep in sync with and place in ``COURSES`` dictionary. You can use the course name as key for each course url. This will be used to make directories inside ``./downloads`` directory.

ex,
```python
COURSES = {
    "my course name": "my course url"
}
```
7. If you want to use a custom download directory, simply change the value of ``DOWNLOAD_DIRECTORY``.

8. After that, save your changes and go back to the terminal.
9. Run ``download_pdf.py`` or ``download_video.py`` to start downloading.
