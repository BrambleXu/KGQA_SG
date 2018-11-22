import pandas as pd

def assign_group(people_group, group, group_name=''):
    group = group.replace("'", '')
    group = group.split()
    for people in group:
        people_group[people] = group_name
    return people_group

path = '../raw_data/triples.csv'
df = pd.read_csv(path, header=0)

# 更改：超昂 为 曹昂
df.at[145, 'head'] = '曹昂'

# 记录有多少人
head_identicle_people = set(df['head'].tolist())
tail_identicle_people = set(df['tail'].tolist())
all_identicle_people = set.union(head_identicle_people, tail_identicle_people)
people_count = len(all_identicle_people)

# 势力分布
wei = "'曹丕' '荀攸' '徐晃' '庞德'  '曹操'  '张郃' '荀彧' '司马昭' '曹仁' '曹植' '典韦' '郭嘉' '乐进' '张辽' '夏侯淳' '曹真' '曹爽' '曹纯' '司马炎' '司马懿' '邓艾' '夏侯渊' '贾诩' '许褚' '司马师' '夏侯楙' '蔡瑁' '曹嵩' '邹氏' '程昱' '刘氏' '清河公主' '于禁' '蒯越' '钟会' '文聘' '曹昂'"
shu = "'关兴' '魏延' '诸葛亮' '诸葛瞻' '法正' '黄忠' '关羽' '赵云' '姜维' '张飞' '徐庶' '马良' '诸葛瑾'  '糜芳'  '刘禅' '黄月英' '庞统' '马超' '祝融'  '黄承彦' '沙摩柯' '甘氏' '糜竺' '刘备' '关平' '张苞' '糜氏' '蒋琬' '马谡'"
wu = "'孙坚' '太史慈' '孙策' '大乔' '周泰' '孙权' '黄盖' '周瑜' '甘宁' '吴国太'  '吕蒙' '鲁肃'  '孙尚香' '陆逊' '程普' '徐盛' '孙氏'  '韩当' '张昭' '孙韶' '蒋钦' '凌统' '丁奉' '小乔'"
others = "'袁术' '马腾' '陈宫' '公孙瓒'  '吕布'  '袁绍' '董卓' '孟获' '貂蝉' '吕伯奢' '刘辩' '韩遂' '丁原' '张角' '袁谭' '刘胜' '公孙越' '张梁' '张宝'  '庞德公' '袁熙'  '刘表'  '卢植' '刘协' '王允' '袁尚' '高顺' '张绣' '刘启' '卞氏' '黄祖' '蔡氏'"

# 构建人物和势力对应的字典
people_group = {}
people_group = assign_group(people_group, wei, group_name='魏国')
people_group = assign_group(people_group, shu, group_name='蜀国')
people_group = assign_group(people_group, wu, group_name='吴国')
people_group = assign_group(people_group, others, group_name='群雄')

# 给每个人物添加势力
df['head_group'] = df['head'].map(lambda x:people_group[x])
df['tail_group'] = df['tail'].map(lambda x:people_group[x])

# 去除relation
df = df.drop(['relation'], axis=1)

# 保存结果为txt文件
path = '../raw_data/triples_processed.txt'
df.to_csv(path, header=None, index=None, sep=',')
print('The processed file is saved to ' + path)