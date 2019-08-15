import requests


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def get_content(url):
    try:
        response = requests.get(url, headers=headers, verify=False)
        url_content = response.content.decode('utf-8')
        return url_content
    except Exception as e:
        print('Failed: %s' % str(e) )
        return False



######################   For Test   #####################

# url = 'https://www.reddit.com/r/sysadmin/comments/88ivbo/has_anyone_here_done_the_hyperconverged/'
# html_content = get_content(url)

# print('-------')