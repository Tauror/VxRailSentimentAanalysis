import urllib.request,re
from collections import defaultdict
import csv
from textblob import TextBlob


#search the key word
keyword = 'vxrail'
url = "https://www.dell.com/community/forums/searchpage/tab/message?filter=location&q=" + keyword + "&location=category:English&collapse_discussion=true"
data = urllib.request.urlopen(url).read().decode("utf-8","ignore")

#get the num of results
patResultsNum = '<div aria-level="4" role="heading" class="search-result-count">(.*?)results'
resultNum = re.findall(patResultsNum,data,re.S)
resultNum = resultNum[0].strip()
print(resultNum)

#for each all pages
result = defaultdict(list) 
# for page in range(1,(int(resultNum)-1)/10 + 2):
for page in range(1,2):
    url = "https://www.dell.com/community/forums/searchpage/tab/message?filter=location&q=" + keyword + "&location=category:English&page=" + str(page) + "&collapse_discussion=true"
    currentPage = urllib.request.urlopen(url).read().decode("utf-8","ignore")
    patArticleUrl = '<a class="lia-link-navigation verified-icon".*?href="(.*?)"'
    articleUrls = re.findall(patArticleUrl,currentPage,re.S)

    #get the article by current page
    for articleUrl in articleUrls:
        articleUrl = "https://www.dell.com" + articleUrl
        print(articleUrl)
        articleData = urllib.request.urlopen(articleUrl).read().decode("utf-8","ignore")

        patQuestion = '<div itemprop="text" id="bodyDisplay".*?<div class="lia-message-body-content">(.*?)</div>'
        resultQuestion = re.findall(patQuestion,articleData,re.S)
        for i in range(len(resultQuestion)):
            resultQuestion[i] = " ".join(resultQuestion[i].split())
            resultQuestion[i] = re.sub('<.*?>','',resultQuestion[i])
            resultQuestion[i] = re.sub('&nbsp;','',resultQuestion[i])
            print(resultQuestion[i])
        print(resultQuestion)

        patAnwser = '<div itemprop="text" id="bodyDisplay_.*?<div class="lia-message-body-content">(.*?)</div>'
        resultAnswer = re.findall(patAnwser,articleData,re.S)
        for i in range(len(resultAnswer)):
            resultAnswer[i] = " ".join(resultAnswer[i].split())
            resultAnswer[i] = re.sub('<.*?>','',resultAnswer[i])
            resultAnswer[i] = re.sub('&nbsp;','',resultAnswer[i])
            t = TextBlob(resultAnswer[i])
            s = t.sentiment
            print(resultAnswer[i])
            result[resultQuestion[0]].append(resultAnswer[i])

with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, result.keys())
    w.writeheader()
    w.writerow(result)


    print('-------------------')

