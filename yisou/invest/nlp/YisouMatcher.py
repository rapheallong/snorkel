from snorkel.matchers import RegexMatchEach,RegexMatch,Matcher

class ORGMatcher(RegexMatchEach):
    def __init__(self, *children, **kwargs):
        kwargs['attrib'] = 'pos_tags'
        kwargs['rgx'] = 'ni|nrz|nz|n|ns|nz|nh|nr|nd|eng'
        super(ORGMatcher, self).__init__(*children, **kwargs)