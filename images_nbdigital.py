from IPython.display import HTML, Markdown, display
from PIL import Image

import sqlite3
import pandas as pd
import os
import re

small_scale = 0.59
large_scale = 1.58

illustrations_db = "/mnt/disk1/illustrations_bookshelf.db"
bigdatabase = "/mnt/disk1/illustrations_all.db"


def query(db, sql, params=()):
    with sqlite3.connect(db) as con:
        res = con.execute(sql, params).fetchall()
    return res

def pdquery(db, sql, params=()):
    with sqlite3.connect(db) as con:
        res = pd.read_sql_query(sql, con, params=params)
    return res

def get_urls_from_illustration_data(illus, part = True, scale = None, cuts = True, delta = 0):
    """From infomration about a picture on a page in a book (or newspaper) generate a link to a picture.
    part sets size of output of page, it takes the value True or a number. If part is True it returns the cut out of image.
    illus is a dictionary of with entries and values like this: 
    {'height': 270, 'hpos': 251, 'page': 'digibok_2017081626006_0018', 'resolution': 400, 'vpos': 791, 'width': 373} 
    the variable cuts, if true allows cropping of image - restricted images must not go over 1024 x 1024 pixels"""
    
    if scale == None:
        if illus['resolution'] >= 300 or illus['resolution'] < 100:
            scale = large_scale
        else:
            scale = small_scale
            
    height = int(illus['height']) + 2*delta
    width = int(illus['width']) + 2*delta
    vpos = int(illus['vpos']) - delta
    hpos = int(illus['hpos']) - delta
    
    if cuts != False:
        if width * scale > 1024:
            width = int(1024/scale)
        if height * scale > 1024:
            height = int(1024/scale)
            
    urn = f"URN:NBN:no-nb_{illus['page']}"
    if part == True:
        # return cut out
        url = f"https://www.nb.no/services/image/resolver/{urn}/{int(hpos*scale)},{int(vpos*scale)},{int(width*scale)},{int(height*scale)}/full/0/native.jpg"
    else:
        # return whole page
        url = f"https://www.nb.no/services/image/resolver/{urn}/full/0,{part}/0/native.jpg"    
    return url

def display_finds(r, width = 500):
    """A list of urls in r is displayed as HTML"""
    base = "https://www.nb.no/items/"
    rows = []
    for row in r:
        urnstring = re.findall("URN[^/]*", row)[0]
        prefix, doctyp, urn, page = urnstring.split('_')
        #print(f'{prefix}_{doctyp}_{urn}?page={page}')
        rows += [f"<tr><td><a href='{base}{prefix}_{doctyp}_{urn}?page={int(page) + 1}' target='_'><img src='{row}'  width={width}'></a></td></tr>" ]
    return HTML("""<html><head></head>
     <body>
     <table>
     {rows}
     </table>
     </body>
     </html>
     """.format(rows=' '.join(rows)))

def get_pictures(text="sommeridyll", part = 300, cuts = False, hits = 10):
    pics = pdquery(bigdatabase, f"select  page, rank from pictures_small where text match '{text}' order by rank limit 200")   
    picture_pages = pics.sort_values(by="rank")
    illustrations =[]
    for x in picture_pages.head(hits).iterrows():
        if isinstance(part, int):
            res = pdquery(illustrations_db, "select * from illustrations where page = ? group by page", params = (x[1].page,))
            #print(res)
        else:
            res = pdquery(illustrations_db, "select * from illustrations where page = ?", params = (x[1].page,))  
            #print(res)
        illustrations += [dict(i[1]) for i in res.iterrows()]
        
    images = [get_urls_from_illustration_data(i, delta=50, cuts=cuts, part=part) for i in illustrations]
    return images