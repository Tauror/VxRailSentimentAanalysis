import os
import csv
import json
import time
import numpy as np


def readJson(file):
    with open(file, 'r', encoding='utf-8') as f:
        json_str = f.read()
        json_data = json.loads(json_str)

    return json_data


def getComments(json_data):
    comments = []
    # get the tille and question in the json of commentPage
    file_id = list(json_data['posts']['models'].keys())[0]
    title = json_data['posts']['models'][file_id]['title']
    # question = [i['c'][0]['t'] for i in json_data['posts']['models'][file_id]['media']['richtextContent']['document']]
    question = []
    if json_data['posts']['models'][file_id]['media']:
        for i in json_data['posts']['models'][file_id]['media']['richtextContent']['document']:
            try:
                if len(i['c']):
                    question.append(i['c'][0]['t'])
            except KeyError:
                print(file_id+' 没有获取完整的question！')
        question = ' '.join(question)


    created_time = json_data['posts']['models'][file_id]['created']/1000
    ts = time.localtime(created_time)
    created_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    comments.append([file_id, title, created_time, question])

    # get the comments and comments' time in the json of commentPage
    try:
       t = json_data['commentsPage']['keyToChatCommentLinks']['commentsPage--[post:\''+file_id+'\']']
    except KeyError:
        file_id = list(json_data['posts']['models'].keys())[1]
    
    commentsIds_Times = [[i['id'], i['created']] for i in json_data['commentsPage']['keyToChatCommentLinks']['commentsPage--[post:\''+file_id+'\']']]
    for commentsId, commentsTimes in commentsIds_Times:
        comment = ''
        document = json_data['comments']['models'][commentsId]['media']['richtextContent']['document']
        l = len(document)
        for i in range(l):
            if 'c' in document[i].keys():
                j = len(document[i]['c'])
                if j:
                    for jj in range(j):
                        try:
                            comment += document[i]['c'][jj]['t']
                        except KeyError:
                            print(commentsId+' 没有对应的键值！')
        ts = time.localtime(commentsTimes)
        commentsTimes = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        comments.append([file_id, commentsId, commentsTimes, comment])
        
    print('Get '+file_id+' comments successfully!')
    return comments

def write_comments(data, path=''):
    with open(path+'./data.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)




######################   For Test   #####################

if __name__ == "__main__":
    mPATH = os.getcwd()
    path = '/data/JsonResults/'
    data = []
    for file in os.listdir(mPATH+path):
        json_data = readJson(mPATH+path+file)
        print('Read '+file+' successfully!')
        comments = getComments(json_data)
        for comment in comments:
            comment.insert(0,file)
            data.append(comment)

    [rows, cols] = np.array(data).shape

    write_comments(data, path=mPATH+'/mTest')

