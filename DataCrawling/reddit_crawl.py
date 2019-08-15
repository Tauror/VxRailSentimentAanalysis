from get_urls import get_urls
from get_content import get_content
from get_jsons import get_jsons
from get_comments import getComments,write_comments



if __name__ == "__main__":
    commentsData = []
    urls = get_urls()
    for i, url in enumerate(urls):
        print('Getting:', url)
        # get_response(str(i + 1), url)
        html_content = get_content(url)
        json_data = get_jsons(html_content)
        comments = getComments(json_data)
        for comment in comments:
            comment.insert(0, 'No.'+str(i)+' url')
            commentsData.append(comment)

    write_comments(commentsData)

