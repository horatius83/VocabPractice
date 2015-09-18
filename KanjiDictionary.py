import xml.etree.ElementTree as ET

class KanjiDictionary:
    def __init__(self,filename):
        self.Open(filename)
        
    def Open(self,filename):
        def processEntry(entry):
            def getText(path):
                e = entry.find(path)
                if e != None:
                    return e.text
                else:
                    return None
            processedEntry = {
                'literal' : getText('./literal'),
                'grade' : getText('./misc/grade'),
                'stroke_count' : getText('./misc/stroke_count'),
                'jlpt_level' : getText('./misc/jlpt'),
                'frequency' : getText('./misc/freq'),
                'on' : [x.text for x in entry.findall('./reading_meaning/rmgroup/reading[@r_type="ja_on"]')],
                'kun' : [x.text for x in entry.findall('./reading_meaning/rmgroup/reading[@r_type="ja_kun"]')],
                #the query should be ./reading_meaning/rmgroup/meaning[not(@m_lang)]
                'meaning' : [x.text for x in entry.findall('./reading_meaning/rmgroup/meaning') if x.attrib == {}]
                }
            return processedEntry 

        tree = ET.parse(filename)
        root = tree.getroot()
        self.entries = { }
        for child in (x for x in root if x.tag == "character"):
            processedEntry = processEntry(child)
            if processedEntry['on'] != [] or processedEntry['kun'] != []:
                self.entries[processedEntry['literal']] = processedEntry
        

    
