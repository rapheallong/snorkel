1,目的是提取公司名，一个是以现有的公司名，通过tagging model（bi-lstm之类）
训练模型。做法是 
1) 用已有公司名标记数据
2) 训练模型

2,可以尝试使用dataprogramming方法。

1) 分词，通过ngram生成mention，但是有个问题，现有的分词工具词性
标注很不准
