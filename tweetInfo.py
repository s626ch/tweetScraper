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
    workingdir = os.path.dirname(__file__) # get where this is at
    workingdriverpath = os.path.join(workingdir, 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--log-level=3")
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
        print(tweettext)
        print(f"Tweeted: {tweetedat}")
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