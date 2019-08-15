import os
import re
import json


RE_JSON = r'</script><script id="data">window.___r = (.*?); window.___prefetches'

def get_jsons(string, re_str=RE_JSON):  
    json_str = re.findall(re_str, string)[0]
    json_data = json.loads(json_str)
    return json_data



######################   For Test   #####################

# for i in range(140):
#     with open('./data/HtmlResults/'+str(i+1)+'.txt', 'r', encoding='utf-8') as f:
#         text = f.read()
#         jsonData = get_jsons(text, RE_JSON)
#     if jsonData:
#         with open('./results_json/'+str(i+1)+'.json','w',encoding='utf-8') as t:
#             t.write(jsonData)
