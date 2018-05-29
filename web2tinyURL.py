import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options # adjust Chrome window size
import time, re, os
import tkinter # access clipboard (built-in method)
import german_school_Crawler as gsc # import the German school crawling python file

if __name__ == '__main__':
    # Hyperparams
    tinyurlweb = r'https://tinyurl.com/'
    path = r'C:\Users\rreal\Downloads\German_CS_MS.csv'
    sleepSecs = 1
    stringlenThreshold = 30 # target web string len being larger than this will be converted to the shorter one
    continueRow = 0 # this para will be auto computed (接續上次程式中斷的地方，接著Target file 繼續分析)
    pageload_timeout = 10
    # load daeta
    df = pd.read_csv(path, sep=',', encoding='utf-8', header='infer', na_filter=False)
    print( 'Successfully load data of size ', df.shape )
    # check save_path already exists or not
    if os.path.isfile(path[:-4]+ r'_tinyurl.csv'):
        ans = input( 'the file that data will be saved in has already exists, rewrite file?[y/n]\n(Otherwise, data will be written starting from End of file.)' )
        if ans == 'y': os.remove( path[:-4] + r'_tinyurl.csv')
        elif ans =='n':
            alreadyexistsDF = pd.read_csv(path[:-4]+r'_tinyurl.csv', sep=',', encoding='utf-8', header='infer', na_filter=False)
            continueRow = len(alreadyexistsDF)
            print( 'Then sys will not rewrite file but save data from the end of file.')
            print( 'Continue from row data no. %d' % (continueRow+1))

    # open browser GUI, then adjust window size
    browser = gsc.LoadBrowser( 'Chrome' )
    browser.set_window_position(0,0)
    browser.set_window_size(1366,768)
    browser.set_page_load_timeout(pageload_timeout)
    # tinter to control clipboard
    tk = tkinter.Tk()
    tk.withdraw() # make tk windwo disappear
    tk.update()
    

    # initialize tinyURL.com website
    _ = gsc.Crawler( browser, tinyurlweb, sleep=sleepSecs, timeout=pageload_timeout)
    # located target web address string ( at idx=0,10,14,17(=-1) )
    idxlist = [0, 8, 9, 10, 14, -1]
    for row_num, row in df.iterrows():
        if row_num < continueRow: continue # jump to the row data where the programm stopped last time.
        for idx in idxlist:
            # omit those non-website string
            if row[idx] == '': continue
            else: targetlist = re.findall( r'(http://\S+|https://\S+)', row[idx])
            if targetlist == []: continue
            print( '(row data ID, column idx, no. of web str found) is (%d,%d,%d)' % (row_num+1, idx, len(targetlist)), end='\n')
            for target in targetlist:
                if len(target) < stringlenThreshold: continue
                # send original web string and submit    
                browser.find_element_by_id("url").click()
                browser.find_element_by_id("url").clear()
                browser.find_element_by_id("url").send_keys(target)
                try: browser.find_element_by_id("submit").click()
                except TimeoutException:
                    print('time out after %d when loading page, stop loading and proceed to next operations' % pageload_timeout)
                    browser.execute_script('window.stop()')
                time.sleep(sleepSecs)
                # find converted web address string (shorter)
                # click to auto copy target string to clipboard
                tk.clipboard_clear()
                tk.clipboard_append('') # append empty string to create CLIPBOARD object
                browser.find_element_by_xpath("//a[@id='copy_div']/small").click() # copy
                tk.update() # update values so that copied string now stays on clipboard
                time.sleep(0.03)
                # fetch clipboard content and update value in row
                webStr = tk.clipboard_get()
                row[idx] = re.sub( re.escape(target), webStr, row[idx]  )
                print('Source str\t%s\nNew str\t %s' % (target, webStr) )
            # end for loop // targetlist
        # end for loop //idxlist
        # save data (Series type)
        if row_num == 0: # the first time, so write headers into file
            firsttime = True
        else:
            firsttime = False
        df.iloc[row_num, :].to_frame().T.to_csv(path[:-4] + r'_tinyurl.csv', sep=',', encoding='utf-8', mode='a+', na_rep='', index=False, header=firsttime)
        print( 'data sucessfully saved up to {:3}'.format(row_num+1))
    # end for loop //df.iterrows()
    tk.destroy()
    browser.quit()
    print( 'All data sucessfully converted and saved, sys returned.' )
    
