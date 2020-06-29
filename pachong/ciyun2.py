import pandas as pd
import time
import requests
import json
from fake_useragent import UserAgent
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
import stylecloud
def get_cut_words(content_series):
    # 读入停用词表
    stop_words = [] 

    with open("pachong/stoplist.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())

    # 添加关键词
    my_words = ['周杰伦', '一首歌', '好好听', '方文山', '30多岁']    
    for i in my_words:
        jieba.add_word(i) 

#     自定义停用词
    my_stop_words = ['歌有', '真的', '这首', '一首', '一点', 
                    '反正', '一段', '一句', '首歌', '啊啊啊', 
                    '哈哈哈', '转发', '微博', '那段', '他会'
                    ]   
    stop_words.extend(my_stop_words)               

    # 分词
    word_num = jieba.lcut(content_series.str.cat(sep='。'), cut_all=False)

    # 条件筛选
    word_num_selected = [i for i in word_num if i not in stop_words and len(i)>=2]

    return word_num_selected


def get_qq_comment(page_num):
    # 存储数据
    df_all = pd.DataFrame()

    for i in range(page_num):
        # 打印进度
        print('我正在获取第{}页的信息'.format(i))

        # 获取URL
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?biztype=2&topid=12924001&cmd=8pagenum={}&pagesize=25'.format(i)

        # 添加headers
        headers = {
            'user-agent': UserAgent().random
        }

        # 发起请求
        try:
            r = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            continue

        # 解析网页
        json_data = json.loads(r.text)

        # 获取数据
        comment_list = json_data['comment']['commentlist']

        # 昵称
        nick_name = [i.get('nick') for i in comment_list]
        # 评论内容
        content = [i.get('rootcommentcontent') for i in comment_list]
        # 评论时间
        comment_time = [i.get('time') for i in comment_list]
        # 点赞数
        praise_num = [i.get('praisenum') for i in comment_list]

        # 存储数据
        df = pd.DataFrame({
            'nick_name': nick_name,
            'content': content,
            'comment_time': comment_time,
            'praise_num': praise_num
        })

        # 追加数据
        df_all = df_all.append(df, ignore_index=True)

        # 休眠一秒
        time.sleep(1)

    return df_all


# 运行函数
df = get_qq_comment(page_num=20) 
text1 = get_cut_words(content_series=df.content)
text1[:5] 
['致敬', '久石', '人生', '旋转', '木马']
stylecloud.gen_stylecloud(text=' '.join(text1), 
                          max_words=1000,
                          collocations=False,
                          font_path='‪pachong/simhei.ttf',
                          icon_name='fas fa-music',
                          size=624,
                          output_name='QQ音乐评论词云图.png')