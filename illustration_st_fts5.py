import dhlab.module_update as mu
#mu.update("nbpictures", silent = True)
from nbpictures import urns_from_super, iiif_manifest, display_finds, get_urls_from_illustration_data, get_illustration_data_from_book
from IPython.display import HTML, Markdown, display
import streamlit as st
from PIL import Image

def markdown_books(books, width = 100):
    """A dictionary of urns - urls is displayed """
    
    markdown_wrapper = lambda x: """
    <body>{body}</body>""".format(body = x)

    div_wrapper = lambda x: """<div>{div_content}</div>""".format(div_content = x)
    book_divs = ""
    for u in books:
        mf = iiif_manifest(u)
        thumbnail = "<h3>Forside</h3> <img src='{thumbnail}'></img> <h3>Metadata</h3>".format(thumbnail = mf['thumbnail']['@id'])
        metainfo =  '\n'.join(["<b>{label}</b> {val}".format(label = x['label'], val = x['value']) for x in mf['metadata'] if x['label'] in ['Tittel', 'Tilgang','Publisert','Varig lenke']])        
        imgs = '\n'.join(["<img  src='{img_http}' width = {width}></img>".format(img_http = pic_url, width = width) for pic_url in books[u]])
        book_divs += div_wrapper(thumbnail + "<p>" + metainfo + "</p>" + imgs) 
        
    return book_divs

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Se mer om å drive analytisk DH på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb), og korpusanalyse via web [her](https://beta.nb.no/korpus/)')


search = st.text_input('Søk etter', '')
period_slider = st.slider(
    'Angi periode - år mellom 1500 og 2014',
    1700, 2020, (1500, 2020)
) 
open_access = st.checkbox('Vis bare bøker som er mer eller mindre fritt tilgjengelig.', value = True)
if open_access:
    conditions = {'digitalAccessibleOnly':'true','profile':'wwwnbno'}
else:
    conditions = None

if search == "":
    urns = ["URN:NBN:no-nb_digibok_2017081626006"]
else:
    try:   
        urns = urns_from_super(search, period=("{s}0101".format(s = period_slider[0]), "{s}1231".format(s=period_slider[1])), conditions = conditions)
    except:
        urns = []
        

antallbøker = st.number_input('Antall bøker fra trefflisten', 1, 20, 5) 
bildestørrelse = st.number_input('Bildestørrelse', 50, 500, 150)

mdata = dict()

c = st.checkbox('Vis kun et utsnitt av bildene - for bøker med forskjellig grad av tilgangskontroll', value = True)


delta = st.number_input('Utvid bildesnittet (fungerer best om bildet er fritt tilgjengelig)', 0, 50, 0) 

books = {u:[get_urls_from_illustration_data(ill, cuts = c, delta = delta) for ill in get_illustration_data_from_book(u)[:50]] for u in urns[:antallbøker]}

#urls = [get_urls_from_illustration_data(ur, cuts = c, delta = delta) for ur in get_illustration_data_from_book(u) ]
#st.markdown('\n'.join(["![]({i})".format(i=u) for u in urls][:100]))
#st.markdown("<style>div {margin-top:1px; margin-bottom:2px}</style>\n" +
#    '\n'.join(["""<div><img src="{i}"  width=100% max-width=600px; /></div>""".format(i=u) for u in urls][:100]), unsafe_allow_html = True)

md_of_pics = markdown_books(books, width = bildestørrelse)
st.markdown(md_of_pics, unsafe_allow_html = True)
