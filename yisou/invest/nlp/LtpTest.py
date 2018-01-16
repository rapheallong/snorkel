# -*- coding:utf8 -*-
import urllib
if __name__ == '__main__':
    url_get_base = "http://api.ltp-cloud.com/analysis/"
    args = {
        'api_key' : 'b9D0w08oEOkGTAsF1sxfJK6DOXCQtECRtlSlCqlA',
        'text' : '我是中国人。',
        'pattern' : 'all',
        'format' : 'plain'
    }
    result = urllib.urlopen(url_get_base, urllib.urlencode(args)) # POST method
    content = result.read().strip()
    print content