import json
import requests
from bs4 import BeautifulSoup

# 先把所有人物做成一个list
def string2list(country):
    """convert name string to name list"""
    country = country.replace("'", '')
    return country.split()

wei = "'荀攸' '徐晃' '庞德'  '曹操'  '张郃' '荀彧' '司马昭' '曹仁' '曹植' '典韦' '郭嘉' '乐进' '张辽' '夏侯惇' '曹真' '曹爽' '曹纯' '司马炎' '司马懿' '邓艾' '夏侯渊' '贾诩' '许褚' '司马师' '夏侯楙' '蔡瑁' '曹嵩' '邹氏' '程昱' '刘氏' '清河公主' '于禁' '蒯越' '钟会' '文聘' '曹昂'"
shu = "'关兴' '魏延' '诸葛亮' '诸葛瞻' '法正' '黄忠' '关羽' '赵云' '姜维' '张飞' '徐庶' '马良' '诸葛瑾'  '糜芳'  '刘禅' '黄月英' '庞统' '马超' '祝融'  '黄承彦' '沙摩柯' '甘氏' '糜竺' '刘备' '关平' '张苞' '糜氏' '蒋琬' '马谡'"
wu = "'孙坚' '太史慈' '孙策' '大乔' '周泰' '孙权' '黄盖' '周瑜' '甘宁' '吴国太'  '吕蒙' '曹丕' '鲁肃'  '孙尚香' '陆逊' '程普' '徐盛' '孙氏'  '韩当' '张昭' '孙韶' '蒋钦' '凌统' '丁奉' '小乔'"
others = "'袁术' '马腾' '陈宫' '公孙瓒'  '吕布'  '袁绍' '董卓' '孟获' '貂蝉' '吕伯奢' '刘辩' '韩遂' '丁原' '张角' '袁谭' '刘胜' '公孙越' '张梁' '张宝'  '庞德公' '袁熙'  '刘表'  '卢植' '刘协' '王允' '袁尚' '高顺' '张绣' '刘启' '卞氏' '黄祖' '蔡氏'"

wei = string2list(wei)
shu = string2list(shu)
wu = string2list(wu)
others = string2list(others)

all_people = wei + shu + wu + others 

# 使用一个for loop来爬去122个武将的图片和简介
base_url = "https://baike.baidu.com/item/"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
        }

descriptions = {} # save all people descriptions
path = './images/' # save images to this floder

for name in all_people:
    print('Now is %s' % name)
    url = base_url + name
    html = requests.get(url, headers=headers).content.decode('utf8')
    soup = BeautifulSoup(html,'lxml')
    
    # 存储人物简介
    metatag = soup.find("meta", {"name": "description"})
    if metatag:
        descriptions[name] = metatag['content']
    else: # 如果不存在
        descriptions[name] = "暂时没有公开的信息"
        print('%s has no descriptions' % name)
    
    # 存储图片
    summary = soup.find("div", {"class": "summary-pic"})
    if summary: # 如果存在summary-pic再保存图片
        link = summary.img['src']
        pic = requests.get(link)
        f = open(path + name + '.jpg', 'wb')
        f.write(pic.content)
        f.close()
        print('Save image')
    else:
        print('%s has no picture' % name)
        
# 爬取的结果中，有些人物的结果不对，针对这些人物设定
correct_urls = {}
correct_urls['卞氏'] = "https://baike.baidu.com/item/%E6%AD%A6%E5%AE%A3%E5%8D%9E%E7%9A%87%E5%90%8E"
correct_urls['刘氏'] = "https://baike.baidu.com/item/%E5%88%98%E5%A4%AB%E4%BA%BA/9659436"
correct_urls['邹氏'] = "https://baike.baidu.com/item/%E9%82%B9%E5%A4%AB%E4%BA%BA/18168"
correct_urls['甘氏'] = "https://baike.baidu.com/item/%E7%94%98%E5%A4%AB%E4%BA%BA/16927"
correct_urls['糜氏'] = "https://baike.baidu.com/item/%E9%BA%8B%E5%A4%AB%E4%BA%BA/8576154"
correct_urls['孙氏'] = "https://baike.baidu.com/item/%E9%99%86%E5%AD%99%E6%B0%8F/22471611"
correct_urls['蔡氏'] = "https://baike.baidu.com/item/%E8%94%A1%E5%A4%AB%E4%BA%BA/9508399"
correct_urls['庞德公'] = "https://baike.baidu.com/item/%E5%BA%9E%E5%BE%B7%E5%85%AC/1693895"
correct_urls['黄祖'] = "https://baike.baidu.com/item/%E9%BB%84%E7%A5%96/17037"


for name, url in correct_urls.items():
    print('Now is %s' % name)
    html = requests.get(url, headers=headers).content.decode('utf8')
    soup = BeautifulSoup(html,'lxml')
    
    # 人物简介
    metatag = soup.find("meta", {"name": "description"})
    if metatag:
        descriptions[name] = metatag['content']
    else: # 如果不存在
        descriptions[name] = "暂时没有公开的信息"
        print('%s has no descriptions' % name)
    
    # 图片
    summary = soup.find("div", {"class": "summary-pic"})
    if summary: # 如果存在summary-pic再保存图片
        link = summary.img['src']
        pic = requests.get(link)
        f = open(path + name + '.jpg', 'wb')
        f.write(pic.content)
        f.close()
        print('Save image')
    else:
        print('%s has no picture' % name)
        
# 这下所有人物都有正确的简介了，图片的话122人中，只有曹嵩没有图片。在互动百科中找到曹嵩的图片，人工添加
# 下面保存人物介绍到JSON格式的文件中。设置ensure_ascii=False，就能正常看到中文了。
with open('data.json', 'w') as f:
    json.dump(descriptions, f, ensure_ascii=False)

# read json
# with open('data.json', 'r') as f:
#     data = json.load(f)