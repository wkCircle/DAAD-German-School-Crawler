# German School Crawler
## Overview
The programm is based on the python selenium package and the website [German Academic Exchange Service](https://www.daad.de/en/) 
to crawl study program information that user requests and save them as a csv file. 
The [main](https://www.daad.de/deutschland/studienangebote/studiengang/en/) crawl page can be accessed through: entering into [German Academic Exchange Service](https://www.daad.de/en/) -> Information for foreigners -> Study Programmes -> All study programmes.

You can also filter out some results by making some conditions at the left hand side bar of the 'All study programmes' page.
Then you can copy the address link and assign it to the argument variable 'source_web'.

## Installation

1. Please make sure you have installed all the required packages, especially the selenium and beautifulsoup on python environment. Command:
	```
	$ pip install selenium.
	$ pip install BeautifulSoup4
	$ pip install lxml
	$ pip install html5lib
	```
2. Please first download webdriver and move it to the directory which also contains your python.exe This will allow selenium to control your browser. For more details, please refer to: https://www.seleniumhq.org/download/ and download the correct driver based on the browser you want to use. (Note: these webdrivers are developed by thrid parties instead of seleniumhq!)

3. Modify the setting in the source code file *german_school_Crawler.py*:
    ```
    # save_path: the file_name you wish to save under a specified path. E.g.,
    save_path = r'C:\Users\userA\Downloads\German_Econ_MS.csv'
    
    # source_web: the page website waited to be crawled.
    # You SHALL have put all conditions and have filtered out the results by using the side bar of DAAD. 
    # And then copy & paste the web address. E.g., 
    source_web = 'https://www.daad.de/deutschland/studienangebote/studiengang/en/?a=result&q=&degree=37&subjects%5B380%5D=1&studyareas%5B380%5D=1&studyfields%5B394%5D=1&studyfields%5B390%5D=1&courselanguage=2&locations=&universities%5B1%5D=1&admissionsemester=&sort=name&page=1'
    
    # (optional) the variable totalPages can be auto computed, and the crawler will crawl pages until the end of totalPages.
    # If you wish to crawl a specific number of pages, pls uncomment the var and set a number to it, and 
    # set the var AutoComputePages in the following as False. E.g.,
    totalPages = 32
    ```
    ```
    # (Do not modify unless you know it) environ setting
    BSparser = 'lxml'
    AutoComputePages = True # if False, should specify totalPages
    ref_amp = True
    encoding ='utf-8'
    timeSleep = 3
    ```
    ```
    # browser: decide wich broswer to use. options can be 'Chrome', 'FireFox', or 'IE'. Notice that your webdriver 
    # should correspond to the browser you wish to use. Please see point 2, Installation for more details. E.g.,
    browser = LoadBrowser( 'Chrome' )
    ```

4. Then you can run the program to automatically crawl all school programs and their details. The program will automatically save the result at **save_path**.

5. Sample result is displayed in the below:

|Link|Name|School|Location|Language of instruction|Standard length of studies|Degree|Area of Focus|Tuition fees|Admission requirements (Germany)|Admission requirements (Link)|Admission Mode|Admission Semester|Lecture Period|Website|International Office (AAA)|AAA Mail|AAA Link|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| http<span>s://</span>w<span>ww.daad.de</span>/deutschland/stud...,Computational | Engineering Science | RWTH Aachen University | Aachen |German | 3 semesters| Master (Master of Science)| | | A first degree is a requirement...| https://... | open admission|	Summer and Winter Semester| 09.10.2017 - 02.02.2018 | http:... |	International... Tel.: 0241 80-90660 |	internatio<span>nal@</span>rwth-aachen.de | ht<span>tp://ww</span>w.campus... |
