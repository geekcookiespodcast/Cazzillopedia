# -*- coding: utf-8 -*-
# NOTE: richiede intallazione di jinja via pip install jinja2
# NOTE: testato su
import urllib.request
import csv
from datetime import datetime
from jinja2 import Template
import io

def cazzillo_text_parser(cazzillotext):
    """Parse a string containing http[s] urls in it. Return the a dict with
    urls and domains.

    Input
    =====

    text : str with http[s] urls in it

    Output
    ======

    list of {'urls':urls,'domains':domains} : urls, domains are list, empty if no url.

    """
    from urllib.parse import urlparse
    import re
    # url matching regex from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    # python version from [Url extraction in python](http://ryancompton.net/2015/02/16/url-extraction-in-python/)
    # https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py
    WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

    urls = re.findall(WEB_URL_REGEX, cazzillotext)
    domains = [urlparse(suburl).netloc for suburl in re.findall(r'(https?://[^\s]+)', cazzillotext)]
    return [{'url': u, 'domain': d} for u, d in zip(urls, domains)]


# retrieve the file in memory
try:
    with urllib.request.urlopen('https://docs.google.com/spreadsheets/d/1KyLkkGDPqYh6TUgBLaysjX3w6oIm2YPDc7tWffQJeDE/export?format=csv&id=KEY&gid=0') as response:
        respo = response.read()
except:
    print("Impossibile scaricare il file csv da Google")
    exit()

# generate a fake file pointer with io
fake_file = io.StringIO(respo.decode("utf-8"))
# read the fake file in a csv dict and convert to list
cazzillidict = list(csv.DictReader(fake_file))
for cazz in cazzillidict:
    # extract urls and domains
    cazz['urldomainlist'] = cazzillo_text_parser(cazz['Cazzillo'])

    if cazz['urldomainlist'] == []:
        del cazz['Nome']
        del cazz['Cazzillo']
        del cazz['urldomainlist']
        del cazz['Data']
    else:
        # convert Data to datetime
        cazz['Data'] = datetime.strptime(cazz['Data'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')

# Data example:
#{'Cazzillo'     : 'Altro package manager molto famoso perac è homebrew https://brew.sh/, in particolare cask installa programmi per Mac proprio eliminando lo scarica apri copia in applicazioni etc, tutto da command line https://caskroom.github.io/ #cazzillo',
# 'Data'         : datetime.datetime(2017, 8, 10, 19, 29, 12, tzinfo=datetime.timezone(datetime.timedelta(0), 'UTC')),
# 'Nome'         : "Mario D'Amore",
# 'urldomainlist': [
#                   {'domain': 'brew.sh', 'url': 'https://brew.sh/'},
#                   {'domain': 'caskroom.github.io', 'url': 'https://caskroom.github.io/'}
#                  ]
# }

# rendering the data with jinja2 and bootstrap CDN css (you need to be online!)
t = Template(
"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cazzillopedia</title>
  <meta name="description" content="Cazzillopedia da Telefram">
  <meta name="author" content="geekcookies">
<!-- Latest compiled and minified CSS bootstrap3 -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>

<body>
<H1 ALIGN=CENTER><P><B>Elenco Cazzilli</B></H1></P>
<div class="container-fluid">
{% for cazz in cazzinput %}
<div class="cazzilloentry">
    <div class="img-rounded" style="background-color:#D6EAF8;">
    
    <div style="float: left"> {{ cazz['Cazzillo']}} </div>
    <div style="text-align: right"> {{ cazz['Nome']}}</div>
    <div style="text-align: right"> {{ cazz['Data']}} </div>
            <ol>
                {% for udl in cazz['urldomainlist'] %}
                    <li><a href="{{udl['url']}}">{{udl['domain']}}</a></li>
                {% endfor %}
            </ol>
    </div>
</div>
{% endfor %}
</div>
</body>
</html>
""")

# write the rendered template to a file
with open("geekcookies_cazzilli_telegram.csv.html", "w+") as fow:
        for a in t.render(cazzinput=cazzillidict):
            try:
                fow.write(a)
            except:
                print(".")