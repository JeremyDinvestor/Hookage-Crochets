#!/usr/bin/env python3
"""Builds the static multi-page site (real URLs, SEO tags, sitemap).
Usage:  python3 tools/build.py --url https://yourdomain.com
Run it again after changing products in tools/data.py or page text in tools/templates/."""
import os,re,sys,json,html,datetime
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(HERE);sys.path.insert(0,HERE)
from data import *
SITE=(sys.argv[sys.argv.index("--url")+1] if "--url" in sys.argv else SITE_DEFAULT).rstrip("/")
IMGDIR=os.path.join(ROOT,"assets","images");TODAY=datetime.date.today().isoformat()
DIM={f[:-4]:list(Image.open(os.path.join(IMGDIR,f)).size) for f in os.listdir(IMGDIR) if f.endswith(".jpg")}
esc=html.escape
def ic(n): return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{IC[n]}</svg>'
def money(n): return "₦{:,}".format(n)
def T(name): return open(os.path.join(HERE,"templates",name+".html"),encoding="utf8").read()
P=[dict(id=i,slug=s,n=n,c=c,p=p,im=im,b=b,r=r,rv=rv,kind=k,d=d,tags=tg) for i,(s,n,c,p,im,b,r,rv,k,d,tg) in enumerate(PRODUCTS)]
SLUG={x["slug"]:x for x in P}
LINK={"#home":"index.html","#shop":"shop.html","#shop/sale":"shop.html","#shop/Sunset":"shop.html?q=Sunset","#shop/Ocean":"shop.html?q=Ocean","#shop/Bloom":"shop.html?q=Bloom","#custom":"custom.html","#faq":"faq.html","#track":"track.html","#learn":"learn.html","#gallery":"community.html","#about":"about.html","#contact":"contact.html","#cart":"cart.html","#wishlist":"wishlist.html"}
for _c,_v in CATEGORIES.items(): LINK["#shop/"+_c]=_v[0]
def fix(s):
    s=re.sub(r'href="(#[^"]*)"',lambda m:'href="%s"'%LINK.get(m.group(1),m.group(1)),s)
    s=re.sub(r'<i data-ic="(\w+)"></i>',lambda m:ic(m.group(1)),s)
    def dims(m):
        n=m.group(1);d=DIM.get(n)
        return f'<img src="assets/images/{n}.jpg"'+(f' width="{d[0]}" height="{d[1]}"' if d else "")
    s=re.sub(r'<img src="assets/images/([\w-]+)\.jpg"(?![^>]*width=)',dims,s)
    s=re.sub(r'<img (?![^>]*(loading|fetchpriority))',r'<img loading="lazy" ',s)
    return s
def img(name,alt,eager=False,cls=""):
    d=DIM[name];extra='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="assets/images/{name}.jpg" alt="{esc(alt)}" width="{d[0]}" height="{d[1]}" {extra}{(" class=%s"%cls) if cls else ""}>'
def card(x,add=False):
    badge=f'<span class="bdg">{x["b"]}</span>' if x["b"] else ""
    a=f'<button class="btn sm alt" data-add="{x["id"]}" type="button" style="margin-top:6px;align-self:flex-start">Add to cart</button>' if add else ""
    return (f'<div class="pcard" data-id="{x["id"]}" data-href="{x["slug"]}.html"><div class="pi"><a href="{x["slug"]}.html" aria-label="{esc(x["n"])}">{img(x["im"],x["n"]+", handmade "+x["kind"].lower())}</a>{badge}'
     f'<button class="hrt" data-h="{x["id"]}" aria-label="Save {esc(x["n"])} to wishlist" aria-pressed="false" type="button">{ic("heart")}</button></div>'
     f'<b><a href="{x["slug"]}.html">{esc(x["n"])}</a></b><small>{money(x["p"])}</small><div class="st">★★★★★ <span>({x["rv"]})</span></div>{a}</div>')
CATLINK={c:v[0] for c,v in CATEGORIES.items()}
NAV=[("shop","Shop","shop.html",[(c,v[0]) for c,v in CATEGORIES.items()]+[("All pieces","shop.html")]),
("custom","Custom Crochet","custom.html",[("Start a custom design","custom.html"),("How it works","faq.html"),("Track your order","track.html")]),
("collections","Collections","shop.html",[("Granny square","shop.html?q=granny"),("Mesh and open-weave","shop.html?q=mesh"),("Checkerboard","shop.html?q=checker"),("Bikinis and beach sets","shop.html?q=bikini")]),
("learn","Learn","learn.html",[("Beginner guides","learn.html"),("Care and maintenance","learn.html"),("Styling ideas","learn.html"),("Community","community.html")]),
("about","About","about.html",[])]
WM='<span class="wm" aria-hidden="true">'+''.join(f'<span class="wv" style="--i:{i}">{c}</span>' for i,c in enumerate('Hookagé'))+'</span>'
LOGO='<svg width="36" height="36" viewBox="10 6 100 100" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><g class="hk"><path d="M20 100V38Q20 16 40 16Q58 16 58 34" stroke="currentColor" stroke-width="9"/></g><path d="M82 100V36" stroke="currentColor" stroke-width="9"/><circle class="dt" cx="82" cy="24" r="5" fill="#e8590c" stroke="none"/><path class="y" pathLength="100" d="M20 72C36 50 54 92 82 66C96 62 102 70 100 80C98 90 88 90 86 84" stroke="#e8590c" stroke-width="6"/></svg>'
LOADER='<div id="loader" role="status" aria-label="Loading Hookagé"><div class="lg">'+LOGO+WM+'</div></div>'
def header(active):
    lis=""
    for key,label,href,sub in NAV:
        cur=' aria-current="page"' if key==active else ""
        if sub: lis+=f'<li class="dd"><a href="{href}"{cur}>{label}</a><ul>'+"".join(f'<li><a href="{h}">{t}</a></li>' for t,h in sub)+"</ul></li>"
        else: lis+=f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>{ic("truck")}Free shipping on orders over ₦50,000</span><span>{ic("spark")}Custom orders available</span><span>{ic("flower")}New season colours just dropped!</span></div></div>
<header><div class="wrap hd"><a class="logo" href="index.html" aria-label="Hookagé home">{LOGO}{WM}</a>
<nav aria-label="Main"><ul>{lis}</ul></nav>
<div class="ic"><button class="ib" id="sb" type="button" aria-label="Search" aria-expanded="false">{ic("search")}</button><button class="ib" id="tg" type="button" aria-label="Switch to dark mode" aria-pressed="false">☾</button>
<a class="ib" href="wishlist.html" aria-label="Wishlist">{ic("heart")}<span class="bd" id="wc" hidden>0</span></a>
<a class="ib" href="track.html" aria-label="Track your order">{ic("user")}</a>
<a class="ib" href="cart.html" aria-label="Cart">{ic("bag")}<span class="bd" id="cc">0</span></a></div></div>
<div class="wrap sbar" id="sbar" hidden><form id="sf" role="search" action="shop.html" method="get"><input type="search" id="hq" name="q" placeholder="Search dresses, tops, bags" aria-label="Search the shop" style="margin:0"><button class="btn" type="submit">Search</button></form><ul class="sug" id="sug" hidden></ul></div></header>
<div class="toast" id="ts" role="status"></div>'''
def footer(link=lambda h:h):
    L=lambda h,t:f'<a href="{link(h)}">{t}</a>'
    SHOPL="".join(L(v[0],c.replace("&","&amp;")) for c,v in CATEGORIES.items())
    SOC="".join(f'<a href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{n} (opens in a new tab)">{ic(i)}</a>' for n,u,i in SOCIAL)
    return f'''<footer><div class="wrap">
<div class="ft"><div class="fb"><a class="logo" href="{link("index.html")}" aria-label="Hookagé home" style="color:var(--on-foot)"><svg width="30" height="30" viewBox="10 6 100 100" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><g class="hk"><path d="M20 100V38Q20 16 40 16Q58 16 58 34" stroke="currentColor" stroke-width="9"/></g><path d="M82 100V36" stroke="currentColor" stroke-width="9"/><circle class="dt" cx="82" cy="24" r="5" fill="#e8590c" stroke="none"/><path class="y" pathLength="100" d="M20 72C36 50 54 92 82 66C96 62 102 70 100 80C98 90 88 90 86 84" stroke="#e8590c" stroke-width="6"/></svg>{WM}</a><p>Handmade crochet wear, made by hand and made for you. Ready-to-wear pieces and one-of-a-kind custom designs.</p><div class="soc">{SOC}</div></div>
<nav aria-label="Shop links"><h2 class="fh">Shop</h2>{SHOPL}</nav>
<nav aria-label="Company links"><h2 class="fh">Company</h2>{L("about.html","About us")}{L("custom.html","Custom crochet")}{L("learn.html","Crochet academy")}{L("community.html","Community")}</nav>
<nav aria-label="Help links"><h2 class="fh">Help</h2>{L("faq.html","FAQ")}{L("faq.html","Shipping and returns")}{L("track.html","Track your order")}{L("contact.html","Contact us")}</nav></div>
<div class="fbt"><div class="row"><select id="rg2" aria-label="Delivery region"></select><div class="chips" id="thc" style="margin:0"><span><input type="radio" name="th" id="th1" value="light"><label for="th1">Light</label></span><span><input type="radio" name="th" id="th2" value="dark"><label for="th2">Dark</label></span><span><input type="radio" name="th" id="th3" value="auto"><label for="th3">Auto</label></span></div></div><p class="fc">© 2026 Hookagé. All rights reserved. More than crochet. It's a lifestyle. ♡</p></div>
</div></footer><button class="ib" id="bt" type="button" aria-label="Back to top">Back to top</button>'''
if __name__!="__main__" or True:
    pass
def head(title,desc,path,ld=None,noindex=False,og="assets/images/og-image.jpg",preload=None):
    url=SITE+("/" if path=="index.html" else "/"+path)
    robots='<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ldh="".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in (ld or []))
    pre=f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">\n' if preload else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1e3a32">
<meta property="og:type" content="website"><meta property="og:site_name" content="Hookagé"><meta property="og:locale" content="en_NG">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Hookagé handmade crochet wear">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{SITE}/{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{pre}<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@800&family=Caveat:wght@400&family=Figtree:wght@400;500;600&family=Fraunces:wght@500&display=swap">
<link rel="stylesheet" href="styles.css">
<script>try{{var t=localStorage.getItem("hk-th");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<script>(function(){{var s=true;try{{var n=performance.getEntriesByType("navigation")[0],seen=sessionStorage.getItem("hk-intro");s=!seen||(n&&n.type==="reload");sessionStorage.setItem("hk-intro","1")}}catch(e){{}}if(s&&!matchMedia("(prefers-reduced-motion:reduce)").matches)document.documentElement.classList.add("splash")}})()</script>
{ldh}</head>'''
def page(file,key,title,desc,body,ld=None,noindex=False,pg=None,preload=None,attrs=""):
    out=head(title,desc,file,ld,noindex,preload=preload)+f'\n<body data-page="{pg or key}">\n'+LOADER+'\n<div id="top"></div>\n'+header(key)+f'\n<main id="main">\n<section class="pg on" id="pg-{pg or key}"{attrs}>\n{body}\n</section>\n</main>\n'+footer()+'\n<script src="products.js" defer></script>\n<script src="config.js" defer></script>\n<script src="script.js" defer></script>\n</body>\n</html>\n'
    open(os.path.join(ROOT,file),"w",encoding="utf8").write(fix(out));PAGES.append((file,noindex))
def h1ize(s,cls="pt"):
    s=s.replace("<h2",f'<h1 class="{cls}"',1);return s.replace("</h2>","</h1>",1)
def crumbs(items):
    h='<nav class="bc" aria-label="Breadcrumb">'+" › ".join(f'<a href="{u}">{esc(t)}</a>' if u else f'<span aria-current="page">{esc(t)}</span>' for t,u in items)+"</nav>"
    ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":SITE+"/"+(u if u!="index.html" else "")} for i,(t,u) in enumerate(items) if u]}
    return h,ld
PAGES=[]
ORG={"@context":"https://schema.org","@type":"OnlineStore","name":"Hookagé","url":SITE+"/","logo":SITE+"/assets/icon-512.png","image":SITE+"/assets/images/og-image.jpg","description":"Handmade crochet wear for women, kids, and the beach, plus custom crochet designs made to order.","email":EMAIL,"areaServed":["NG","GH","KE","ZA","Worldwide"],"currenciesAccepted":"NGN"}
WEB={"@context":"https://schema.org","@type":"WebSite","name":"Hookagé","url":SITE+"/","potentialAction":{"@type":"SearchAction","target":SITE+"/shop.html?q={search_term_string}","query-input":"required name=search_term_string"}}
# ---------- home
hero_alt="Model in a handmade crochet bucket hat surrounded by colourful yarn strands"
hero=f'''<div class="hero" id="hero"><div class="ph">{img("hero",hero_alt,True)}</div><div class="scr" aria-hidden="true">Wear your story ♡</div><div class="wrap tx"><div class="eb">Handmade crochet wear</div><h1>Made by hand.<br>Made for you.</h1><p>From stylish everyday pieces to custom designs, Hookagé brings your crochet dreams to life.</p><div class="row"><a class="btn" href="shop.html">Shop collection {ic("arrow")}</a><a class="btn alt" href="custom.html">Create your own {ic("arrow")}</a></div></div><button class="arw l" data-hn="-1" aria-label="Previous slide" type="button">‹</button><button class="arw r" data-hn="1" aria-label="Next slide" type="button">›</button><div class="dots" role="group" aria-label="Choose slide"><button type="button" data-hs="0" class="on" aria-label="Slide 1"></button><button type="button" data-hs="1" aria-label="Slide 2"></button><button type="button" data-hs="2" aria-label="Slide 3"></button><button class="pz" id="hp" type="button" aria-label="Pause slideshow">❚❚</button></div></div>'''
cats="".join(f'<a class="cat" href="{v[0]}">{img(v[3],c+" crochet wear")}<span>{c.replace("&","&amp;")}<i>{ic("arrow")}</i></span></a>' for c,v in CATEGORIES.items())
cm="".join(img(f"com-{i}",f"Customer wearing Hookagé handmade crochet, photo {i}") for i in range(1,6))
acd=[("Beginner Guides","Start from the basics","ac-1"),("Care &amp; Maintenance","Keep your pieces beautiful","ac-2"),("Styling Ideas","Wear it your way","ac-3"),("Crochet Journal","Stories, tips &amp; inspiration","ac-4")]
ac="".join(f'<a href="learn.html">{img(i,"Crochet academy: "+re.sub("&amp;","and",t))}<div><b>{t}</b><small>{s}</small></div></a>' for t,s,i in acd)
home=T("home")
for a,b in [('<div class="hero" id="hero"></div>',hero),('<div class="g4" id="cats"></div>',f'<div class="g4" id="cats">{cats}</div>'),('<div class="g5" id="fp"></div>','<div class="g5" id="fp">'+"".join(card(SLUG[s]) for s in FEATURED)+'</div>'),('<div class="scroller" id="cm"></div>',f'<div class="scroller" id="cm">{cm}</div>'),('<div class="ac" id="ach"></div>',f'<div class="ac" id="ach">{ac}</div>')]:
    assert a in home,a;home=home.replace(a,b)
page("index.html","home","Hookagé | Handmade Crochet Wear & Custom Crochet Designs","Shop handmade crochet wear for women, kids, and the beach, or order a custom crochet design made to your size and colours. Ships across Africa and worldwide.",home,[ORG,WEB],preload="assets/images/hero.jpg")
# ---------- shop + categories
SHOPDESC={"All":("shop.html","Shop Handmade Crochet Wear | Hookagé","Shop handmade crochet dresses, tops, sets, beachwear, kids' wear, and bags. Every piece is made by hand and can be customised to your size and colours.","Shop handmade crochet wear","Browse every handmade crochet piece in the Hookagé collection: dresses, tops, sets, beachwear, kids' wear, and bags. Each one is made by hand and can be customised to your size and colours.")}
for c,(f,h1,intro,_t,_s,_d) in CATEGORIES.items(): SHOPDESC[c]=(f,f"{h1} | Hookagé",intro,h1,intro)
for c,(f,title,desc,h1,intro) in SHOPDESC.items():
    items=[x for x in P if c=="All" or x["c"]==c]
    chips="".join(f'<a class="chip{" on" if k==c else ""}" href="{u}"{" aria-current=page" if k==c else ""}>{esc(k)}</a>' for k,u in [("All","shop.html")]+[(k,v[0]) for k,v in CATEGORIES.items()])
    bc,bld=crumbs([("Home","index.html")]+([("Shop","shop.html")] if c!="All" else [])+[(h1 if c=="All" else c,None)])
    il={"@context":"https://schema.org","@type":"CollectionPage","name":h1,"description":intro,"url":SITE+"/"+f,"mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":SITE+"/"+x["slug"]+".html","name":x["n"]} for i,x in enumerate(items)]}}
    body=f'<div class="wrap s">{bc}<h1 class="pt">{esc(h1)}</h1><p class="muted intro">{esc(intro)}</p><label class="sr-only" for="sq">Search this page</label><input type="search" id="sq" placeholder="Search {"all pieces" if c=="All" else esc(c.lower())}, e.g. bikini, mesh, checker" autocomplete="off"><div class="chips" id="ft">{chips}</div><div class="row" style="justify-content:space-between;margin-bottom:12px"><span class="muted" id="rc">{len(items)} pieces</span><label class="l">Sort <select id="so" style="width:auto;margin:0 0 0 6px"><option value="pop">Most popular</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option></select></label></div><div class="g5" id="sg">{"".join(card(x,True) for x in items)}</div></div>'
    page(f,"shop",title,desc,body,[bld,il],pg="shop",attrs=f' data-cat="{esc(c)}"')
# ---------- products
for x in P:
    f=x["slug"]+".html";sz=CATEGORIES[x["c"]][4]
    dsz=CATEGORIES[x["c"]][5]
    chips="".join(f'<button class="chip{" on" if v==dsz else ""}" data-sz="{v}" type="button">{v}</button>' for v in sz)
    bc,bld=crumbs([("Home","index.html"),(x["c"],CATLINK[x["c"]]),(x["n"],None)])
    rel=[y for y in P if y["id"]!=x["id"] and y["c"]==x["c"]]+[y for y in P if y["id"]!=x["id"] and y["c"]!=x["c"]]
    body=f'''<div class="wrap s">{bc}<div class="two" id="pd"><div class="pimg">{img(x["im"],x["n"]+", handmade "+x["kind"].lower()+" by Hookagé",True)}</div><div><div class="eb">{esc(x["c"])}</div><h1 class="pt" style="font-size:clamp(28px,4vw,38px)">{esc(x["n"])}</h1><div class="st" style="margin:6px 0">★★★★★ <span>{x["r"]} ({x["rv"]} reviews)</span></div><p style="font-size:26px;margin:6px 0;font-family:Fraunces,Georgia,serif">{money(x["p"])}</p><p class="muted">{esc(x["d"])} Handmade to order from soft cotton yarn, and available in custom sizes and colours.</p><div class="l" style="font-weight:600">Size</div><div class="chips" style="margin-top:6px">{chips}</div><div class="line"><span class="muted">Material</span><span>Soft cotton yarn</span></div><div class="line"><span class="muted">Care</span><span>Hand wash cool, dry flat</span></div><div class="line"><span class="muted">Made</span><span>By hand, in 5 to 10 days</span></div><div class="row" style="margin-top:16px"><button class="btn" data-addp="{x["id"]}" type="button">Add to cart</button><button class="btn alt" data-h="{x["id"]}" id="wbtn" aria-pressed="false" type="button">{ic("heart")}<span id="wlab">Save to wishlist</span></button><a class="btn alt" href="custom.html">Customize this piece</a></div></div></div><div class="s"><h2>You may also like</h2><div class="g5">{"".join(card(y) for y in rel[:5])}</div></div></div>'''
    pl={"@context":"https://schema.org","@type":"Product","name":x["n"],"description":x["d"],"image":[SITE+f"/assets/images/{x['im']}.jpg"],"sku":x["slug"],"category":x["c"],"brand":{"@type":"Brand","name":"Hookagé"},"offers":{"@type":"Offer","url":SITE+"/"+f,"priceCurrency":"NGN","price":str(x["p"]),"availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition"}}
    desc=(x["d"]+f" Handmade by Hookagé, {money(x['p'])}. Custom sizes and colours available.")[:158]
    page(f,"shop",f'{x["n"]} – Handmade {x["kind"]} | Hookagé',desc,body,[bld,pl],pg="prod")
# ---------- content pages from templates
INFO={"custom":("custom.html","Custom Crochet Wear Made to Your Design | Hookagé","Send us your idea or sketch and we will crochet it by hand to your size and colours. Get a quote in 48 hours. Worldwide delivery.","custom"),
"learn":("learn.html","Crochet Academy: Beginner Guides, Care & Styling | Hookagé","Free crochet beginner guides, care and maintenance tips, and styling ideas from the Hookagé makers.","learn"),
"gallery":("community.html","Real People. Real Style. #HookageMade | Hookagé","See how our community wears Hookagé handmade crochet. Tag #HookageMade for a chance to be featured.","learn"),
"about":("about.html","About Hookagé | Handmade Crochet Made with Care","Hookagé makes handmade crochet wear and custom designs with African colour and craft at heart, for people everywhere.","about"),
"contact":("contact.html","Contact Hookagé | Orders, Quotes & Questions","Message Hookagé on WhatsApp or email for custom quotes, orders, and questions. Replies within 48 hours.","about"),
"faq":("faq.html","FAQ: Custom Orders, Delivery, Care & Returns | Hookagé","Answers about custom crochet orders, delivery across Africa and worldwide, deposits, care, and returns.","about"),
"cart":("cart.html","Your Cart | Hookagé","Review your Hookagé cart and check out.","shop"),
"track":("track.html","Track Your Order | Hookagé","Check the status of your Hookagé order or custom crochet piece.","shop")}
for k,(f,title,desc,nav) in INFO.items():
    body=h1ize(T(k))
    if k=="gallery":
        tiles="".join(f'<a class="tile" href="shop.html" aria-label="Customer look {i+1}">{img(n,"Customer wearing Hookagé handmade crochet")}</a>' for i,n in enumerate([f"com-{j}" for j in range(1,6)]+["granny-top-cardigan-set","cream-mesh-top","textured-crop-top","tangerine-beach-set","brown-stripe-mesh-sweater"]))
        body=body.replace('<div class="g5" id="gl"></div>',f'<div class="g5" id="gl">{tiles}</div>')
    if k=="learn": body=body.replace('<div class="ac" id="ac2" style="margin-bottom:24px"></div>',f'<div class="ac" id="ac2" style="margin-bottom:24px">{ac}</div>')
    ld=None
    if k=="faq":
        qa=re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>",body,re.S)
        ld=[{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":re.sub("<.*?>","",q),"acceptedAnswer":{"@type":"Answer","text":re.sub("<.*?>","",a)}} for q,a in qa]}]
    page(f,nav,title,desc,body,ld,noindex=k in("cart","track"),pg=k)
# wishlist (client-side, not indexed)
wl='<div class="wrap s"><h1 class="pt">Your wishlist</h1><p class="muted" id="wsub">Pieces you have saved. They stay here on this device.</p><div class="row" id="wact" style="margin-bottom:16px" hidden><button class="btn sm" id="wall" type="button">Add all to cart</button><button class="btn sm alt" id="wclr" type="button">Clear wishlist</button></div><div class="g5" id="wg"></div><div id="wempty" hidden><h2>Your wishlist is empty</h2><p class="muted">Tap the heart on any piece to save it for later.</p><a class="btn" href="shop.html">Browse the shop</a></div></div>'
page("wishlist.html","shop","Your Wishlist | Hookagé","Your saved Hookagé pieces.",wl,noindex=True,pg="wishlist")
# 404
open(os.path.join(ROOT,"404.html"),"w",encoding="utf8").write(fix(head("Page not found | Hookagé","The page you are looking for could not be found.","404.html",noindex=True)+'\n<body data-page="404">\n'+LOADER+'\n<div id="top"></div>\n'+header("")+'\n<main id="main"><section class="pg on" id="pg-404"><div class="wrap s" style="text-align:center;padding:60px 0"><h1 class="pt">Page not found</h1><p class="muted">Sorry, we could not find that page.</p><a class="btn" href="index.html">Back to home</a> <a class="btn alt" href="shop.html">Shop the collection</a></div></section></main>\n'+footer()+'\n<script src="products.js" defer></script>\n<script src="config.js" defer></script>\n<script src="script.js" defer></script>\n</body>\n</html>\n'))
# ---------- data for the browser, sitemap, robots, manifest
open(os.path.join(ROOT,"products.js"),"w",encoding="utf8").write("/* Generated by tools/build.py: edit tools/data.py instead */\nwindow.HK_PRODUCTS="+json.dumps(P,ensure_ascii=False)+";\nwindow.HK_IMG="+json.dumps(DIM)+";\nwindow.HK_IC="+json.dumps(IC)+";\nwindow.HK_CATS="+json.dumps({c:{"file":v[0],"sizes":v[4],"def":v[5],"tile":v[3]} for c,v in CATEGORIES.items()})+";\nwindow.HK_FEATURED="+json.dumps([SLUG[s]["id"] for s in FEATURED])+";\n")
pr={"index.html":"1.0","shop.html":"0.9","custom.html":"0.9"}
urls="".join(f'<url><loc>{SITE}/{"" if f=="index.html" else f}</loc><lastmod>{TODAY}</lastmod><priority>{pr.get(f,"0.8" if f in [v[0] for v in CATEGORIES.values()] else "0.7")}</priority></url>\n' for f,n in PAGES if not n)
open(os.path.join(ROOT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nDisallow: /cart.html\nDisallow: /track.html\nDisallow: /wishlist.html\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(ROOT,"site.webmanifest"),"w").write(json.dumps({"name":"Hookagé","short_name":"Hookagé","description":"Handmade crochet wear and custom crochet","start_url":"/","display":"standalone","background_color":"#fbf7f0","theme_color":"#1e3a32","icons":[{"src":"assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/icon-512.png","sizes":"512x512","type":"image/png"}]},indent=2))
keep={f for f,_ in PAGES}|{"404.html"}
for f in os.listdir(ROOT):
    if f.endswith(".html") and f not in keep: os.remove(os.path.join(ROOT,f)); print("removed old page",f)
print(f"Built {len(PAGES)+1} pages for {SITE}")
