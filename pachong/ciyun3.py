import jieba
from stylecloud import gen_stylecloud
def cloud(file_name):
    with open(file_name,'r',encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用 隔开
        #制作中文云词
        gen_stylecloud(text=result,
                       font_path='pachong/simhei.ttf',
                       palette='cartocolors.diverging.TealRose_2',
                       output_name='t2.png',
                       icon_name='fas fa-plane',
                       ) #必须加中文字体，否则格式错误
        
if __name__ == "__main__":
    file_name = 'pachong/dan_mu.txt'
    cloud(file_name)
