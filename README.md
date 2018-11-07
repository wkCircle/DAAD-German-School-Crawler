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
    # params setting
    save_path = r'C:\Users\rreal\Downloads\German_Econ_MS.csv'
    # 'page=' (wihout number) should appear in the end of the variable source_web
    source_web = 'https://www.daad.de/deutschland/studienangebote/studiengang/en/?a=result&q=&degree=37&subjects%5B380%5D=1&studyareas%5B380%5D=1&studyfields%5B394%5D=1&studyfields%5B390%5D=1&courselanguage=2&locations=&universities%5B1%5D=1&admissionsemester=&sort=name&page=1'
    #totalPages = 32 # can be computed automatically
    # if totalPages is specified, then AutoComputePages should be False.

    # environ setting
    BSparser = 'lxml'
    AutoComputePages = True # if False, should specify totalPages
    ref_amp = True
    encoding ='utf-8'
    timeSleep = 3
    # check old file exists or not
    if os.path.isfile(save_path):
            ans = input( 'File already exists, rewrite it?[y/n]')
            if ans == 'y':
                os.remove(save_path)
                
    # decide wich broswer to use
    browser = LoadBrowser( 'Chrome' )
    ```

3.a modify the 'save_path' to determine the output file path
3.b modify the 'source_web': it's the initial page (usually page 1) to crawl school program list. The program will automatically compute how many pages and results sould be crawled. To turn it off, please make 'AutoComputePages=False' at line 167 and specify 'totalPages' at line 162

4. Then you can run the program to automatically crawl all school program web links of each page and also the contents of those links.
5. The final output will contains 18 columns as showed in the following and be saved in the file specified by the argument 'save_path':
		Link,				Name,				School,			Location,	Language of instruction,	Standard length of studies,		Degree,			Area of Focus,Tuition fees,		Admission requirements (Germany),	Admission requirements (Link),	Admission Mode,			Admission Semester,		Lecture Period,		Website,		International Office (AAA),		AAA Mail,			AAA Link
https://www.daad.de/deutschland/stud...,Computational Engineering Science,RWTH Aachen University,	Aachen,			German,				3 semesters,		Master (Master of Science),		,		,		A first degree is a requirement...,		https://...		open admission,		Summer and Winter Semester,	09.10.2017 - 02.02.2018,	http:...,	International... Tel.: 0241 80-90660,	international@rwth-aachen.de,	http://www.campus...
...
