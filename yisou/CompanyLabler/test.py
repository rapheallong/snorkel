# -*- coding:utf-8 -*-
import json
import sys
import hashlib
import ahocorasick
import re
reload(sys)
sys.setdefaultencoding('utf-8')

#input  /user/yisou/crawler/baidu_new/${date}*/dn1*
#hadoop fs -text /user/yisou/crawler/baidu_new/20171007*/dn1*|/home/yisou/anaconda2/envs/hadoop_tool/bin/python voice_mapper_test1107.py |more

def gen_spider_time():
    global spider_time
    ori_spider_time = sys.argv[1] if len(sys.argv)>=2 else '2017123101'
    if len(ori_spider_time)<8:
        spider_time = '2017-12-31'
    else:
        spider_time = ori_spider_time[:4]+'-'+ori_spider_time[4:6]+'-'+ori_spider_time[6:8]

def read_file(file_path):
    with open(file_path, 'rb') as f:
        for line in f:
            yield line

def read_input(file):
    for line in file:
        line = line.replace('\n', '')
        arr = line.split('\t')
        yield arr

def init_name_id_dict():
    global name_id_dict
    global name_id_ac
    global long_short_dict
    global short_long_dict
    name_id_ac = ahocorasick.Automaton()
    name_id_dict = {}
    long_short_dict = {}
    short_long_dict = {}
    lines = read_file('./mappers/id_company_map')
    for line in lines:
        id, long_name, short_name = line.split('\t')
        short_name = short_name.replace('\n', '')
        name_id_dict[long_name.encode('utf-8')] = id
        name_id_dict[short_name.encode('utf-8')] = id
        long_short_dict[long_name.encode('utf-8')] = short_name.encode('utf-8')
        short_long_dict[short_name.encode('utf-8')] = long_name.encode('utf-8')
        name_id_ac.add_word(long_name, (id, long_name))
        name_id_ac.add_word(short_name, (id, short_name))
    name_id_ac.make_automaton()

def init_neg_words_list():
    global ac
    ac = ahocorasick.Automaton()
    lines = read_file('./mappers/neg_words')
    for line in lines:
        line = line.strip()
        ac.add_word(line, line)
    ac.make_automaton()

def build_names(ac_names):
    rt_list = []
    for name in ac_names.split(','):
        if name in long_short_dict:
            rt_list.append((name, long_short_dict.get(name, ''), name_id_dict.get(name, '')))
        else:
            rt_list.append((short_long_dict.get(name, ''), name, name_id_dict.get(name, '')))
    return json.dumps(rt_list)

def main():
    data = read_input(sys.stdin)
    for one in data:
        try:
            url = one[0]
            content = one[1]
            title = one[2]
            time = one[3]
            org_name = one[4]
            voice_source = ''
            if len(one) >= 7:
                voice_source = one[6]
            pic = ''
            if len(one) >= 8:
                pic = one[7]
            id = name_id_dict.get(org_name.encode('utf-8'), '')

            date = ''
            date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
            date_match = date_pattern.search(time)
            if date_match:
                date = date_match.group(0)
            ac_neg_list = []
            for item in ac.iter(content):
                ac_neg = item[1].strip()
                ac_neg_list.append(ac_neg)
            ac_negs = ' '.join(set(ac_neg_list))

            ac_id_list = []
            ac_name_list = []
            for item in name_id_ac.iter(content):
                ac_id = item[1][0].strip()
                ac_name = item[1][1].replace(',', '').strip()
                ac_id_list.append(ac_id)
                ac_name_list.append(ac_name)
            #if id:
            #    ac_id_list.append(id)
            #    ac_name_list.append(org_name)
            #if not ac_id_list:
            #    continue
            ac_ids = ','.join(set(ac_id_list))
            sid = ' '.join(set(ac_id_list))
            ac_names = ','.join(set(ac_name_list))
            sname = ' '.join(set(ac_name_list))

            emotion_type = '-1' if ac_neg_list and ac_id_list else '1'
            #uid = hashlib.md5(url + title + time).hexdigest()
            uid = hashlib.md5(url).hexdigest()

            rt_dic = {}
            rt_dic['uid'] = uid
            rt_dic['id'] = ac_ids
            rt_dic['sid'] = sid
            rt_dic['sname'] = sname
            rt_dic['source'] = 'voice'
            rt_dic['bi_source'] = 'null'
            rt_dic['org_name'] = ac_names
            rt_dic['full_name'] = build_names(ac_names)
            rt_dic['time'] = time
            rt_dic['ac_negs'] = ac_negs
            rt_dic['url'] = url
            rt_dic['title'] = title
            rt_dic['content'] = content
            rt_dic['emotion_type'] = emotion_type
            rt_dic['voice_source'] = voice_source
            rt_dic['date'] = date
            rt_dic['pic'] = pic
            rt_dic['spider_time'] = spider_time
            print '\t'.join(('1', json.dumps(rt_dic)))
        except:
            pass

if __name__ == "__main__":
    init_name_id_dict()
    init_neg_words_list()
    gen_spider_time()
    main()