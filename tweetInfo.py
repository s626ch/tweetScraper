import os
from selenium import webdriver
import time
import sys
import shutup;shutup.please() # ignore deprecation warnings for the love of god

tweetinput = len(sys.argv)
print()
print("Total tweets:", tweetinput - 1)

if tweetinput == 1:
    print("Please paste links to tweets!")
    print()
else:
    #workingdir = os.path.dirname(__file__) # get where this is at
    workingdir = os.getcwd() # get current working directory; this works better cross platform vs above line that only works on windows
    #! windows
    if sys.platform == 'win32':
        workingdriverpath = os.path.join(workingdir, 'chromedriver.exe')
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36' # the UA *has* to be specified because ssstwitter deters headless instances
    #! linux
    if sys.platform == 'linux':
        workingdriverpath = os.path.join(workingdir, 'chromedriverlinux')
        useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    #! mac
    if sys.platform == 'darwin':
        workingdriverpath = os.path.join(workingdir, 'chromedrivermac')
        os.chmod(workingdriverpath, 755) # set file as executable
        useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    options.add_argument('--lang=en_US') 
    options.add_argument(f'user-agent={useragent}')
    if sys.platform == 'linux':
        options.add_argument('--remote-debugging-port=6959') #? needed to stop "unknown error: DevToolsActivePort file doesn't exist"
    driver = webdriver.Chrome(executable_path=workingdriverpath, chrome_options=options)

    for i in range(1, tweetinput):
        tweeturl = str(sys.argv[i])
        nitterurl = tweeturl.replace("https://twitter.com/", "https://nitter.1d4.us/")

        driver.get(nitterurl)
        time.sleep(2)
        tweetinfo = {} # dictionary for tweet info
        authname = driver.find_element_by_xpath("//*[@id='m']/div/div/div[1]/div/div/div/a[1]").get_attribute("title")
        authhandle = driver.find_element_by_xpath("//*[@id='m']/div/div/div[1]/div/div/div/a[2]").get_attribute("title")
        print()
        try:
            replyingto = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='replying-to']").text
            print(f"Tweet author: {authname} - {authhandle} - {replyingto}")
        except:
            print(f"Tweet author: {authname} - {authhandle}")
        tweettext = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='tweet-content media-body']").text
        tweetedat = driver.find_element_by_xpath("//*[@id='m']/div/div/p[@class='tweet-published']").text
        if tweettext != "":
            print(tweettext)
        else: 
            pass
        print(f"Tweeted: {tweetedat}")
        # try to grab all images
        try:
            tweetimages = {}
            for i in range(0,4):
                tweetimages[f'{str(i)}'] = driver.find_elements_by_xpath("//*[@id='m']/div/div/div[@class='attachments']/div[@class='gallery-row']/div[@class='attachment image']/a[@class='still-image']")[i].get_attribute("href")
                print(f"Image url {i + 1}: {tweetimages[str(i)]}")
        except:
            pass
        # try to grab video
        if driver.find_elements_by_xpath("//*[@id='m']/div/div/div[@class='attachments card']/div[@class='gallery-video']/div[@class='attachment video-container']/video"):
            # this is going to open a new tab, using a download service, to get the video url, since nitter uses blob storage (cringe)
            sssurl = tweeturl.replace("https://twitter.com/", "https://ssstwitter.com/")
            driver.execute_script("window.open('');") # open new tab
            driver.switch_to.window(driver.window_handles[1]) # switch to new tab
            driver.get(sssurl) # go to page
            time.sleep(2) # this is needed so it doesn't scream if it can't instantly find the button, because...it does that.
            #driver.find_element_by_tag_name('html').screenshot('web_screenshot.png') #? this was needed to figure out why the page wouldn't properly load, turns out it was a UA issue
            videourl = driver.find_element_by_xpath("//*[@id='mainpicture']/div/a[3]").get_attribute("href") # grab video url
            driver.close() # close current tab with video
            driver.switch_to.window(driver.window_handles[0]) # switch back to main tab
            print(f"Video url: {videourl}")
        else:
            pass
        tweetreplies = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='tweet-stats']/span[1]").text
        tweetrts = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='tweet-stats']/span[2]").text
        tweetqrts = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='tweet-stats']/span[3]").text
        tweetlikes = driver.find_element_by_xpath("//*[@id='m']/div/div/div[@class='tweet-stats']/span[4]").text
        if tweetreplies == "":
           tweetreplies = "0"
        if tweetrts == "":
           tweetrts = "0"
        if tweetqrts == "":
           tweetqrts = "0"
        if tweetlikes == "":
           tweetlikes = "0"
        print(f"Replies: {tweetreplies} - Retweets: {tweetrts} - Quote Retweets: {tweetqrts} - Likes: {tweetlikes}")
        print()
    driver.quit()
