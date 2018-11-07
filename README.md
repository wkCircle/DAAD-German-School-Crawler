#German School Crawler
Description: The programm is based python selenium package and the website German Academic Exchange Service (https://www.daad.de/en/) 
-> Information for foreigners 
-> Study Programmes 
-> All study programmes (https://www.daad.de/deutschland/studienangebote/studiengang/en/) to crawl school program list and its details
You can also filter out some results by making some conditions at the left hand side bar of the 'All study programmes' page.
Then you can copy the address link and assign it to the argument variable 'source_web'

1. Please make sure you have installed selenium package on python environment. Command: 
	$pip install selenium.
2. Please first download webdriver and move the file to the directory that contains your python.exe This will allow selenium to control your browser.
For more details, please refer to: https://www.seleniumhq.org/download/ and download the correct driver based on the browser you want to use.
(Note: these webdrivers are developed by thrid parties instead of seleniumhq!)
3. Modify the program into yours:
3.a modify the 'save_path' to determine the output file path
3.b modify the 'source_web': it's the initial page (usually page 1) to crawl school program list. The program will automatically compute how many pages and results sould be crawled. To turn it off, please make 'AutoComputePages=False' at line 167 and specify 'totalPages' at line 162

4. Then you can run the program to automatically crawl all school program web links of each page and also the contents of those links.
5. The final output will contains 18 columns as showed in the following and be saved in the file specified by the argument 'save_path':
		Link,				Name,				School,			Location,	Language of instruction,	Standard length of studies,		Degree,			Area of Focus,Tuition fees,		Admission requirements (Germany),	Admission requirements (Link),	Admission Mode,			Admission Semester,		Lecture Period,		Website,		International Office (AAA),		AAA Mail,			AAA Link
https://www.daad.de/deutschland/stud...,Computational Engineering Science,RWTH Aachen University,	Aachen,			German,				3 semesters,		Master (Master of Science),		,		,		A first degree is a requirement...,		https://...		open admission,		Summer and Winter Semester,	09.10.2017 - 02.02.2018,	http:...,	International... Tel.: 0241 80-90660,	international@rwth-aachen.de,	http://www.campus...
...
