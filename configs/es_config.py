#es index name
ES_INDEX_NAME = 'testing_index'

#es index body
INDEX_BODY = {
   "mappings":{
      "properties":{
         "parent_artist":{
            "type":"text"
         },
         "artist":{
            "type":"text"
         },
         "album":{
            "type":"text"
         },
         "song":{
            "type":"text"
         },
         "raw_verse":{
            "type":"text"
         },
         "verse_vector":{
            "type":"dense_vector",
            "dims":2
         }
      }
   }
}

#regex patterns for cleaning verses
#just to be safe keep the order
from collections import OrderedDict
REGEX_PATTERNS = OrderedDict()
REGEX_PATTERNS['\[.*intro.*\]'] = ''
REGEX_PATTERNS['\[.*outro.*\]'] = ''
REGEX_PATTERNS['(\[.*chorus.*\]|\(.*chorus.*\))'] = ''
REGEX_PATTERNS['(\[.*verse.*|.*bridge.*\]|\(.*verse.*|.*bridge.*\))'] = ''
REGEX_PATTERNS['\[(?!.*chorus.*|.*verse.*|.*bridge.*|.*intro.*|.*outro.*).*\]'] = ''
REGEX_PATTERNS['\{(.*?)\}'] = ''
REGEX_PATTERNS['\{\*(.*?)\*\}'] = ''
REGEX_PATTERNS['\((?!.*chorus.*|.*verse.*|.*bridge.*).*\)'] = ''
REGEX_PATTERNS['\*[^\*]*'] = ''
REGEX_PATTERNS['\?+'] = ''
REGEX_PATTERNS['[|]\*[^|\{|\(|\[]*'] = ''
REGEX_PATTERNS["\'"]=''
REGEX_PATTERNS['\\n']=' '
REGEX_PATTERNS['&amp;']='and'
REGEX_PATTERNS['  ']=' '