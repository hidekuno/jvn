import sys 
import nntplib

try:
    s = nntplib.NNTP('news.gmane.org')
    for n in s.list()[1]:
        print(n.group)
    s.quit()
    sys.exit(0)
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
