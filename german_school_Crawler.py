import numpy as np
import pandas as pd
import sys, os
import math
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options # adjust Chrome window size
import time, re

OverviewTabKeys = ['Language of instruction', 'Standard length of studies', 'Degree', 'Area of Focus', 'Tuition fees']
AdmissionTabKeys = ['Admission requirements (Germany)','Admission requirements (Link)','Admission Mode', 'Admission Semester', 'Lecture Period', 'Website']
ContactTabKeys = ['International Office (AAA)', 'AAA Mail', 'AAA Link']
#HrefOnlyKeys = ['Admission requirements (Link)', 'Website']



def LoadBrowser( string ):
    ChromeList = ['chrome', 'Chrome']
    FireFoxList = ['firefox', 'FireFox', 'Firefox']
    IEList = ['ie', 'IE', 'Ie']
    driver = None
    if string in ChromeList:
        driver = webdriver.Chrome()
    elif string in FireFoxList:
        driver = webdriver.Firefox()
    elif string in IEList:
        driver = webdriver.Ie()
    else:
        raise ValueError( string )
    return driver

def Crawler(browser, web_addr, sleep=1, timeout=30):
    if timeout >0: browser.set_page_load_timeout(timeout)
    # Katolon Behavior
    try: browser.get( web_addr ) # open web by selenium webdriver
    except TimeoutException:
        print('time out after %d when loading page, stop loading and proceed to next operations' % timeout)
        browser.execute_script('window.stop()')
    time.sleep(sleep)
    return browser.page_source

# helper function: bs4 parser will mistakenly add semicolon after ampersand(&)'s refentity,
# resulting in invalid web address format
def RefAmpersand(final_soup_href):
    """
    sol method is to first parser codecs into BeautifulSoup using html parser, so '&' would be '&amp;' in original web address.
    Then the function replace '&amp;' with '&' (tranform back) to make web address still valid.
    """
    if final_soup_href != None:
        final_soup_href = re.sub( r'\&amp;', r'&', final_soup_href)
    return final_soup_href

def Parser(soup, task, computePages=True, ref_ampersand=True):
    if task == 'crawlResultsFound':
        targetblock = soup.find( 'div', attrs = {'class':'view-tab', 'id':'course-list'} ) 
        targetblock = targetblock.parent.find('p', attrs={'class':'count-mobile count-mobile-m'})
        sentence = ""
        for idx, string in enumerate(targetblock.stripped_strings):
            if idx == 0:
                totalResults = int(string)
            sentence += string + ' '
        sentence = sentence.strip()
        totalPages = math.ceil( totalResults / 10.0 )
        if computePages:
            return totalPages, totalResults, sentence
        return totalResults, sentence
    
    elif task == 'crawlSchoolList':
        targetblock = soup.find( 'div', attrs = {'class':'view-tab', 'id':'course-list'}).ul 
        headList = targetblock( 'h3')  # contains 10 li tags -> div -> h3. # soup('name') is equiv. to soup.find_all('name')
        df = pd.DataFrame([], columns=['Link','Name','School','Location'], dtype='object')
        for head in headList:
            # program link, program name, name of school, school location
            dictionary = dict()
            if ref_ampersand == True and head.a['href']!=None:
                dictionary['Link'] = RefAmpersand(head.a['href'])     # to see a tags attrs {keys, vals}, use: head.a.attrs
            else:
                dictionary['Link'] = head.a['href']
            dictionary['Name'] = head.a.strong.string.strip()
            dictionary['School'] = head.a.span.string.strip()
            dictionary['Location'] = head.a.contents[-1].replace('•', '').strip()
            # update row data into dataframe
            df = df.append( dictionary , ignore_index = True)
        return df
        

    elif task == 'crawlProgrammDetail':
        targetblock = soup.find( 'div', attrs={'class':'content'} ).ul   # contains 3 li tags representing Overview, Admission, Contact tabs
        [Overview, Admission, Contact] = targetblock('li')
        dictionary = dict()

        # dealwith 3 tabs
        # Overview tab detail
        for div in Overview('div'):
            key = div.h2.string.strip()
            if key in OverviewTabKeys and key not in dictionary:
                str_container = []
                for string in div.p.stripped_strings:
                    str_container.append(string)
                str_container = ' '.join(str_container)
                # store value
                dictionary[key] = str_container
        # Admission tab detail
        for div in Admission('div'):
            if div.h2 != None:
                key = div.h2.string.strip()
            else:
                continue
            if key in AdmissionTabKeys and key not in dictionary:
                str_container = []
                for string in div.p.stripped_strings:
                    str_container.append(string)
                str_container = ' '.join(str_container)
                # store value
                dictionary[key] = str_container
        # Contact tab detail
        for div in Contact('div'):
            # find correct div which contains h2 tag(s) that is International Office (AAA)
            if div.h2 == None:
                continue
            key = div.h2.string.strip()
            if key != 'International Office (AAA)':
                continue
            
            for p in div('p'):
                if p.strong != None: # omit those p tags containing strong subtags
                    continue
                elif p('a', href=True) != None:
                    for a in p('a', href=True):
                        if isMail(a['href']) and not 'AAA Mail' in dictionary:
                            dictionary['AAA Mail'] = a['href'].replace('mailto:', '')
                        elif isWeb(a['href']) and not 'AAA Link' in dictionary:
                            dictionary['AAA Link'] = a['href']
                    if key == 'International Office (AAA)' and key not in dictionary:
                        str_container = []
                        for string in p.stripped_strings:
                            if re.search('Weblink.+|@.+', string): # avoid collecting mails and weblinks
                                continue
                            else:
                                str_container.append(string)
                        str_container = ' '.join(str_container)
                        dictionary['International Office (AAA)'] = str_container
                        break # break for loop over div('p')
        return pd.Series(dictionary)
    
    else:
        raise ValueError( task )

# helper function (True/False function required for bs4 find()/find_all() method
def isMail(href):
    return href and re.compile('mailto:.+').search(href)
def isWeb(href):
    return href and re.compile('http.+').search(href)


if __name__ == '__main__':
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

    # crawl and parser
    # 1. crawl how many results found.
    source_web = re.sub(r'page=\d+', 'page=', source_web) # remove numbers after 'page='
    codecs = Crawler( browser , source_web+str(1), sleep=timeSleep ) # return html
    source_soup = BeautifulSoup( codecs , BSparser)
    totalPages, totalResults, sentence = Parser(source_soup, 'crawlResultsFound', AutoComputePages, ref_amp)
    print(sentence, 'totally %d pages' % (totalPages))

    # 2. crawl each page's program list and the program detail in it.
    save_count = 0
    for i in range(totalPages):
        # 2a. crawl program list # a page usually contains 10 links
        codecs = Crawler( browser , source_web+str(i+1), sleep=timeSleep ) # return html    
        page_soup = BeautifulSoup( codecs, BSparser )
        print( 'crawling and parsing page %d\'s program list...' % (i+1))
        programListDF = Parser( page_soup, 'crawlSchoolList', AutoComputePages, ref_amp )
        # 2b. crawl program detail
        col_tag= OverviewTabKeys + AdmissionTabKeys + ContactTabKeys
        programDetailDF = pd.DataFrame([], columns= col_tag, dtype='object' )
        for idx, [Link, Name, School, Location] in programListDF.iterrows():
            print('Parsing no. %d program details...' % (idx+1) )
            codecs = Crawler( browser, Link )
            program_soup = BeautifulSoup( codecs, BSparser)
            series = Parser( program_soup, 'crawlProgrammDetail', AutoComputePages, ref_amp)
            programDetailDF = programDetailDF.append( series , ignore_index= True)
        # 2c. merge dfs together
        programDetailDF = pd.concat( [ programListDF, programDetailDF ], axis=1, ignore_index=False)

        # 3. save data for every page for loop
        programDetailDF.replace(re.compile(',|\n'), '', inplace=True)
        if i == 0: # the first time, so write headers into file
            firsttime = True
        else:
            firsttime = False
        programDetailDF.to_csv(save_path, sep=',', mode='a+', na_rep='', header=firsttime, index=False, encoding=encoding )
        
        save_count += len(programDetailDF)
        print('data has been saved up to %d in %s' % (save_count, save_path))
        
    # 4. Finally quit selenium
    browser.quit()
