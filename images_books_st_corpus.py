import pandas as pd
import re
import dhlab.api.dhlab_api as api
import dhlab as dh

import streamlit as st
from PIL import Image

def display_finds(r, width = 300):
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
            rows.append((urn, int(page), f"[![-- visning --]({row})]({base}{prefix}_{doctyp}_{urn}?page={int(page) + 1})"))
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

col1, col2, col3, col4 = st.columns([5,2,2,2])
with col1:
    search = st.text_input('Skriv en liste med ord eller fraser', '', help="For å lage fraser sett ordene i anførselstegn. Det kan være lurt å benytte såkalt trunkert søk. For å få treff på alle ord som starter med _krig_, søk etter _krig*_.")

with col2:
    dist = st.number_input("Avstand mellom ord/fraser", min_value=0, max_value=500, value=5, help="Ved å sett 0 kan det ikke komme noen ord mellom, med 5 kan det være alt inntil 5 ord mellom - verdiene kan ligge mellom 0 og 500")

with col3:
    part = st.number_input("Størrelse på visning", min_value = 50, max_value = 1500, value = 300, step = 50, help = "En størrelse på 500 gir en grei bildegjengivelse, og mulig lesbar tekst. Graden av forstørrelse kan påvirke hva som er tillatt å gjengi. Defaultverdien på 300 kan vise treff i de fleste bøker. Gå ned i størrelse for å få tilgang til flere sider, eller bare for å få plass til flere på skjermen.")

with col4:
    sort = st.selectbox("Sorter bildene", "relevans år forfatter boktittel".split())
    
search = f"NEAR({search}, {dist})"

r = get_pictures(text= search, part=part)
ill, urns = display_finds(r)

corpus = dh.Corpus(doctype="digibok", limit=0)
corpus.extend_from_identifiers([x[1] for x in urns]) # urns is alist of pairs - second is a book urn
df = corpus.corpus
df.year = df.year.astype(int)
df['mark'] = df[["authors", "title", "year"]].apply(
    lambda x: ' -- '.join(x.astype(str)),
    axis=1
)

if sort == "forfatter":
    table = df.sort_values(by='authors')[["urn", "mark"]].set_index('urn')
elif sort == 'år':
    table = df.sort_values(by='year')[["urn", "mark"]].set_index('urn')
elif sort == 'boktittel':
    table = df.sort_values(by='title')[["urn", "mark"]].set_index('urn')
else:
    table = df[["urn", "mark"]].set_index('urn')

st.write(f"##### Illustrasjoner i {len(table)} bøker")

for urn in table.index:
    #st.write(u)
    try:
        title = str(table.loc[urn].values[0])
    except:
        title = urn
    #st.write(ill)
    ustring = " ".join([v[1][0] for v in ill[ill.urn == urn.split('_')[-1]].sort_values(by='page')[['link']].iterrows()])
    st.write(f"{title}")
    st.write(ustring) 
