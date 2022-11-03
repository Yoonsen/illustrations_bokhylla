import pandas as pd
import re
import dhlab.api.dhlab_api as api

import streamlit as st
from PIL import Image

def display_finds(r, width = 500):
    """A list of urls in r is displayed as Markdown"""
    base = "https://www.nb.no/items/"
    rows = []
    pages = []
    urns = []
    urnstore = []
    for row in r:
        
        urnstring = re.findall("URN[^/]*", row)[0]
        prefix, doctyp, urn, page = urnstring.split('_')
        title = f"{prefix}_{doctyp}_{urn}" #urnstring #iiif_manifest(f"{prefix}_{doctyp}_{urn}")['label']
        urnpage = f"{urn}_{page}"
        if not urn in urnstore:
            urns.append((urn, title))
            urnstore.append(urn)
        if not urnpage in pages:
            rows.append((urn, int(page), f"[![Foo]({row})]({base}{prefix}_{doctyp}_{urn}?page={int(page) + 1})"))
            pages.append(f"{urn}_{page}")
            
            
    result = pd.DataFrame(rows, columns=['urn', 'page', 'link'])
    return result, urns

@st.cache(suppress_st_warning=True, show_spinner = False)
def get_pictures(text="", part = True):
    return api.images(text=text, part=part)

st.set_page_config(page_title="Images", layout="wide", initial_sidebar_state="auto", menu_items=None)

image = Image.open('NB-logo-no-eng-svart.png')

st.image(image, width = 200)

st.markdown('Sjekk [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb) for mer om DH ved Nasjonalbiblioteket')

col1, col2 = st.columns(2)
with col1:
    search = st.text_input('Skriv en liste med ord eller fraser', '', help="For å lage fraser sett ordene i anførselstegn")

with col2:
    part = st.number_input("Maks avstand mellom ord/fraser", min_value=0, max_value=500, value=5, help="Ved å sett 0 kan det ikke komme noen ord mellom, med 5 kan det være alt inntil 5 ord mellom - verdiene kan ligge mellom 0 og 500")

search = f"NEAR({search}, {part})"
#print(search)
r = get_pictures(text= search, part=500)
ill, urns = display_finds(r)

for u in urns:
    title = u[1]
    urn = u[0]
    ustring = " ".join([v[1][0] for v in ill[ill.urn == urn].sort_values(by='page')[['link']].iterrows()])
    st.write(f"## {title}")
    st.write(ustring) 
