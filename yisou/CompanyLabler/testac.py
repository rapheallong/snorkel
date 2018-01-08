#encoding=utf-8
import ahocorasick

ac = ahocorasick.Automaton()
words=['融资','投资','获得','金山云']
for w in words:
    ac.add_word(w,w)
ac.make_automaton()
str=' 本次融资后，金山云将加大人工智能领域的研发力度，巩固和扩大在视频、游戏等互联网领域的领先地位'
for i in ac.iter(str):
    print i