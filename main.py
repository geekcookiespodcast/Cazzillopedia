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

if __name__ == "__main__":
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
    t = Template("""
    <!DOCTYPE HTML>
<!-- saved from url=(0037)http://geekcookies.github.io/episodi/ -->
<!DOCTYPE html PUBLIC "" ""><HTML lang="en-us"><HEAD><META content="IE=11.0000" 
http-equiv="X-UA-Compatible">
   <LINK href="http://gmpg.org/xfn/11" rel="profile">   
<META http-equiv="X-UA-Compatible" content="IE=edge">   
<META http-equiv="content-type" content="text/html; charset=utf-8">   <!-- Enable responsiveness on mobile devices--> 
  
<META name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1"> 
  <TITLE>          Episodi · Geek Cookies.       </TITLE>   <!-- CSS -->   <LINK 
href="Episodi%20·%20Geek%20Cookies__file/poole.css" rel="stylesheet">   <LINK 
href="Episodi%20·%20Geek%20Cookies__file/syntax.css" rel="stylesheet">   <LINK 
href="Episodi%20·%20Geek%20Cookies__file/lanyon.css" rel="stylesheet">   <LINK 
href="Episodi%20·%20Geek%20Cookies__file/css.css" rel="stylesheet">     <!-- Icons --> 
  <LINK href="/public/apple-touch-icon-precomposed.png" rel="apple-touch-icon-precomposed" 
sizes="144x144">   <LINK href="/public/favicon.ico" rel="shortcut icon">   <!-- RSS --> 
  <LINK title="RSS" href="/feed.xml" rel="alternate" type="application/rss+xml"> 
  
<SCRIPT>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-56320158-1', 'auto');
  ga('send', 'pageview');

</SCRIPT>
   
<META name="GENERATOR" content="MSHTML 11.00.10570.1001"></HEAD>   
<BODY class="theme-base-0g"><!-- Target for toggling the sidebar `.sidebar-checkbox` is for regular
     styles, `#sidebar-checkbox` for behavior. --> 
<INPUT class="sidebar-checkbox" id="sidebar-checkbox" type="checkbox"> <!-- Toggleable sidebar --> 
<DIV class="sidebar" id="sidebar">
<DIV class="sidebar-item">
<P>Join the Dark Side of the Geek: we have Cookies.</P></DIV><NAV class="sidebar-nav"><A 
class="sidebar-nav-item" href="http://geekcookies.github.io/episodi/">Home</A><A 
class="sidebar-nav-item" 
href="http://geekcookies.github.io/contactus/">Contattaci</A><A class="sidebar-nav-item active" 
href="http://geekcookies.github.io/episodi/">Episodi</A><A class="sidebar-nav-item" 
href="http://geekcookies.github.io/whatisthis/">Cos’è GeekCookies</A><A class="sidebar-nav-item" 
href="http://geekcookies.github.io/whoarewe/">Chi siamo</A><!--Theese elements culd not be the active page:external link--> 
    <A class="sidebar-nav-item" 
href="http://geekcookies.github.io/feed.xml">Feed RSS</A><A class="sidebar-nav-item" 
href="http://geekcookies.github.io/amazon/">Amazon</A><A class="sidebar-nav-item" 
href="http://geekcookies.github.io/itunes/">iTunes</A></NAV>
<DIV class="sidebar-item">
<P>    Basato su <A href="http://jekyllrb.com/">jekyll</A> e sul template <A 
href="http://lanyon.getpoole.com/">poole/lanyon</A>.     </P></DIV></DIV><!-- Wrap is the content to shift when toggling the sidebar. We wrap the
         content to avoid any CSS collisions with our real content. --> 
    
<DIV class="wrap">
<DIV class="masthead">
<DIV class="container">
<H3 class="masthead-title"><IMG class="site-logo" src="Episodi%20·%20Geek%20Cookies__file/icon.png"> 
            <A title="Home" href="http://geekcookies.github.io/">Geek 
Cookies.</A>             <SMALL>the Dark Side of the Geek.</SMALL>           
</H3></DIV></DIV>
<DIV class="container content">
<DIV class="page">
<H1 class="page-title">Cazzilli</H1>
<UL>

{% for cazz in cazzinput %}
        <LI>
        <P>{{ cazz['Data']}} » {{ cazz['Nome']}} » {{ cazz['Cazzillo']}} {% for udl in cazz['urldomainlist'] %} <a href="{{udl['url']}}"> {{udl['domain']}}</a>{% endfor %}</P></LI>
    {% endfor %}


  
</UL></DIV></DIV></DIV><LABEL class="sidebar-toggle" 
for="sidebar-checkbox"></LABEL>
<SCRIPT>
      (function(document) {
        var toggle = document.querySelector('.sidebar-toggle');
        var sidebar = document.querySelector('#sidebar');
        var checkbox = document.querySelector('#sidebar-checkbox');

        document.addEventListener('click', function(e) {
          var target = e.target;

          if(!checkbox.checked ||
             sidebar.contains(target) ||
             (target === checkbox || target === toggle)) return;

          checkbox.checked = false;
        }, false);
      })(document);
    </SCRIPT>
   </BODY></HTML>
    """)

    # write the rendered template to a file
    with open("geekcookies_cazzilli_telegram.html", "w+") as fow:
            fow.write(t.render(cazzinput=cazzillidict))