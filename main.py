import os
import re
import sys
from collections import defaultdict
import json
from io import StringIO
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

print(sys.argv)
message = sys.argv[2]
rules = load(StringIO(sys.argv[1]), Loader=Loader)
results = defaultdict(dict)

for group, keywords in rules.items():
    pattern = fr'\[{group}:(.*?)\]'
    match = re.search(pattern, message, re.DOTALL)
    if match:
        found = [s.strip() for s in match.group(1).split(',')]
        for keyword in keywords:
            results[group][keyword] = "true" if keyword in found else "false"
            print(f"{group}.{keyword}={results[group][keyword]}")


output = open(os.getenv('GITHUB_OUTPUT'), 'a') if os.getenv('GITHUB_OUTPUT') else sys.stdout
with output as output:
    output.write(f"results={json.dumps(results)}\n")