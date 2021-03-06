# -*- coding: utf-8 -*-
import urllib
import re
import urllib2
import sys

def info_extractor(url):
    _VALID_URL = r'(?:http://)?(?:www\.)?watchcartoononline\.com/([^/]+)'
    mobj = re.match(_VALID_URL, url)
    video_id = mobj.group(1)
    webpage = urllib2.urlopen(url).read()
    video_url = re.search(r'<iframe id="(.+?)0" (.+?)>',
                            webpage).group()
    video_url = re.search('src="(.+?)"',
                            video_url).group(1).replace(' ','%20')
    params = urllib.urlencode({'fuck_you':'','confirm':'Click Here to Watch Free!!'})
    request = urllib2.Request(video_url,params)
    video_webpage = urllib2.urlopen(request).read()
    final_url =  re.findall(r'file: "(.+?)",',
                            video_webpage)
    return urllib.unquote(final_url[-1]).replace(' ','%20')

def downloader(fileurl,file_name):
    u = urllib2.urlopen(fileurl)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "[watchcartoononline-dl]  Downloading %s (%s bytes)" %(file_name, file_size)
    file_size_dl = 0
    block_size = 8192

    #Download loop
    while True:
        buffer = u.read(block_size)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%s [%3.2f%%]" % (convertSize(file_size_dl), file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        #print status
        sys.stdout.write("\r        %s" % status)
        sys.stdout.flush()

    #Download done. Close file stream
    f.close()

def convertSize(n, format='%(value).1f %(symbol)s', symbols='customary'):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs
    """
    SYMBOLS = {
    'customary'     : ('B', 'K', 'Mb', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
    }
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

if __name__ == '__main__':
    url = raw_input("url ?  ")
    final_url = info_extractor(url)
    name = final_url.split('/')[-1]
    downloader(final_url,name)
