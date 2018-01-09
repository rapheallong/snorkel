#encoding=utf-8
import ahocorasick

ac=ahocorasick.Automaton()
file='/Users/yixinc-d/workspace/work2/snorkel/yisou/data/companname.csv'
f = open(file)
for c in f:
    c=c.strip()
    ac.add_word(c,c)
ac.make_automaton()
str='据网易科技获悉，垂直移动美妆服务平台美人妆APP近期获得数千万元A轮融资，投资机构为深圳鼎瑞祥资本。'
for i in ac.iter(str):
    print i