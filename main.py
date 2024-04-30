import re

def altairFix(codeString, path):
    regex = '{\'url\': \'.*\'}'
    exchange = '{\'url\': \'' + path +'.*\'}'
    code = re.sub(regex, 'path', codeString)
    return code

