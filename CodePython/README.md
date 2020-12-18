# Webcrawling Hahow's website

This directory stores the codes that webcrawls the information we need in this project.

**Webcrawling_SinglePage.py** is our first attempt to fetch information in from one webpage that is defined in the first place. In **Webcrawling_MultiPage.py** we try to crawl over every courses that has the key word "Python" in the course title. Lastly, **Webcrawling_All.py** manage to find all the comments of the courses that has the key word "Python" in their title. 


## Issues regarding implementation

These Python scripts involved using the package, Pandas. We can't install Pandas using Python 3.9 on a MacOS Big Sur. This is why we are using older Python versions.
