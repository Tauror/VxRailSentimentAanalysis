# VxRail Sentiment Aanalysis
This is a project to use web crawler to collect comments and complains, thumb up ,etc data from public communities against VxRail product, use TextBlob/snowNLP to analyze sentimental trends, since we keep shipping new release to the field, would it realy making things better granularly or nothing changes.
This view is subjective, all from public media as data source.


## 1. Main Python Packages Used:
### for Crawling
* re: https://docs.python.org/3/library/re.html 
* selenium：https://selenium-python.readthedocs.io/
* requests：https://2.python-requests.org/en/master/
* json：https://docs.python.org/3/library/json.html

### for Sentimental Analysis
* TextBlob：https://textblob.readthedocs.io/en/dev/index.html

## 2. data source update
* 2019/8/15: crawled data from Reddit: https://www.reddit.com/search/?q=vxrail
 ![Sentiment survey of VxRail on Reddit.png](/SentimentAanalysis/Sentiment_Survey_of_VxRail_on_Reddit.png)
* keep going on...




* PS:两个在线工具：
1. 在线爬虫工具：Octoparse
https://hackernoon.com/twitter-scraping-text-mining-and-sentiment-analysis-using-python-b95e792a4d64

2. 在线语言分析工具（提供模型）：MonkeyLearn
https://monkeylearn.com/blog/creating-sentiment-analysis-model-with-scrapy/

3. sklearn逻辑回归模型的情感分析例子
https://towardsdatascience.com/sentiment-analysis-with-python-part-1-5ce197074184

