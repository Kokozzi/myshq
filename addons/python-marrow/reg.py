import re

match = re.search(r'number=(?P<number>\d+)', 'jajaj\n\nnumber=23\n\n', re.MULTILINE)

print match.groupdict()