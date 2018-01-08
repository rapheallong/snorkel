from snorkel.parser import Parser
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *
import sys
import requests

from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from snorkel.models import construct_stable_id
import warnings


class ParserConnection(object):
    '''
    Default connection object assumes local parser object
    '''

    def __init__(self, parser):
        self.parser = parser

    def _connection(self):
        raise NotImplemented

    def parse(self, document, text):
        return self.parser.parse(document, text)


class URLParserConnection(ParserConnection):
    '''
    URL parser connection
    '''

    def __init__(self, parser, retries=5):
        self.retries = retries
        self.parser = parser
        self.request = self._connection()

    def _connection(self):
        '''
        Enables retries to cope with CoreNLP server boot-up latency.
        See: http://stackoverflow.com/a/35504626

        Create a new object per connection to make multiprocessing threadsafe.

        :return:
        '''
        requests_session = requests.Session()
        retries = Retry(total=self.retries,
                        connect=self.retries,
                        read=self.retries,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        # Mac OS bug -- without this setting multiprocessing requests will fail
        # when the server has boot-up latency associated with model loading
        # See: http://stackoverflow.com/questions/30453152/python-multiprocessing-and-requests
        if sys.platform in ['darwin']:
            requests_session.trust_env = False
        requests_session.mount('http://', HTTPAdapter(max_retries=retries))
        return requests_session

    def post(self, url, data, allow_redirects=True):
        '''

        :param url:
        :param data:
        :param allow_redirects:
        :param timeout:
        :return:
        '''
        resp = self.request.post(url, data=data, allow_redirects=allow_redirects)
        return resp.content.strip()

    def parse(self, document, text):
        '''
        Return parse generator
        :param document:
        :param text:
        :return:
        '''
        return self.parser.parse(document, text, self)


class LTPParser(Parser):
    def __init__(self):
        self.endpoint = 'http://api.ltp-cloud.com/analysis/'
        self.apikey = 'p1D5d2m0o0LznXxcfBfJXPrNnXvZLBivUgdO3eVk'

    def connect(self):
        return URLParserConnection(self)

    def parse(self, document, text, conn):
        if len(text.strip()) == 0:
            sys.stderr.write("Warning, empty document {0} passed to CoreNLP".format(document.name if document else "?"))
            return

        # handle encoding (force to unicode)
        if isinstance(text, str):
            text = text.encode('utf-8', 'error')
        try:
            args = {
                'api_key': self.apikey,
                'text': text,
                'pattern': 'all',
                'format': 'json'
            }
            docs = conn.post(self.endpoint, args)
        except:
            warnings("http error")
        position=0
        for doc in docs:
            offset=0
            for para in doc:
                for sent in para:
                    p = defaultdict(list)
                    loc=0
                    for w in sent:
                        p['words'].append(w['cont'])
                        p['lemmas'].append(w['cont'])
                        p['pos_tags'].append(w['pos'])
                        p['ner_tags'].append(w['ne'])
                        p['char_offsets'].append(w['id'])
                        p['entity_cids'].append(w['id'])
                        p['dep_parents'].append(w['parent'])
                        p['dep_labels'].append(w['relate'])
                        p['char_offsets'].append(loc)
                        loc+=len(w['cont'])
                    p['abs_char_offsets']=[offset+l for l in p['char_offsets']]
                    text="".join(p['words'])
                    offset+=len(text)
                    p['entity_cids'] = ['O' for _ in p['words']]
                    p['entity_types'] = ['O' for _ in p['words']]
                    p['position']=position
                    p['document'] = document
                    p['text'] = text
                    abs_sent_offset = p['abs_char_offsets'][0]
                    abs_sent_offset_end = abs_sent_offset + p['char_offsets'][-1] + len(p['words'][-1])
                    if document:
                        p['stable_id'] = construct_stable_id(document, 'sentence', abs_sent_offset,
                                                                 abs_sent_offset_end)

                    position+=1
                    yield p
