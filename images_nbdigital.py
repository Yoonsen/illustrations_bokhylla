import dhlab.module_update as mu
#mu.update("nbpictures", silent = True)
from nbpictures import iiif_manifest, display_finds, get_urls_from_illustration_data, get_illustration_data_from_book, large_scale, small_scale
from IPython.display import HTML, Markdown, display
import streamlit as st
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