#encoding=utf-8
import jieba
import jieba.posseg
# seg = jieba.cut("汽车音频产品运营商“考拉FM”获时尚资本等A轮投资")
seg2=jieba.posseg.cut("汽车音频产品运营商“考拉FM”获时尚资本等A轮投资")
for i in seg2:
    print i.word,i.flag