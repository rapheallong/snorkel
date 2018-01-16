from snorkel.parser import  DocPreprocessor
from snorkel.models import Document
import codecs

class CSVDocPreprocessor(DocPreprocessor):
    def parse_file(self, fp, file_name):
        with codecs.open(fp, encoding=self.encoding) as csv:
            for line in csv:
                name,text = line.rsplit(',', 2)
                stable_id = self.get_stable_id(name)
                doc = Document(
                    name=name, stable_id=stable_id, meta={'file_name': file_name}
                )
                yield doc, text
class DirectoryProprocessor(DocPreprocessor):
    def __init__(self,dir,parser):
        self.parser=parser
        self.dir=dir

    def parse_file(self, fp, file_name):
        self.parser
