import dhlab.module_update as mu
#mu.update("nbpictures", silent = True)
from nbpictures import urns_from_super, iiif_manifest, display_finds, get_urls_from_illustration_data,get_illustration_data_from_book, display_books
from IPython.display import HTML, Markdown, display
import streamlit as st
from PIL import Image

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Se mer om å drive analytisk DH på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb), og korpusanalyse via web [her](https://beta.nb.no/korpus/)')


search = st.text_input('Søk etter', '')
period_slider = st.slider(
    'Angi periode - år mellom 1700 og 2014',
    1700, 2020, (1700, 2020)
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
        
u = st.selectbox("Velg en bok (URN) fra listen under", urns[:10])

mdata = dict()
c = False

try:
    mdata = {x['label']:x['value'] for x in iiif_manifest(u)['metadata']}
    c = not 'alle' in mdata['Tilgang']
except:
    'ingen funn'
c = st.checkbox('Vis kun et utsnitt av bildene - for bøker med forskjellig grad av tilgangskontroll', value = c)

#u = st.text_input('URN', urns[0])


st.markdown('\n'.join(['**' + x + '**: ' + mdata[x] for x in mdata]), unsafe_allow_html=True)

delta = st.number_input('Utvid bildesnittet (fungerer best om bildet er fritt tilgjengelig)', 0, 50, 0) 

books = {u:[get_urls_from_illustration_data(ill, cuts = c, delta = delta) for ill in get_illustration_data_from_book(u)[:20]] for u in urns[:5]}

#urls = [get_urls_from_illustration_data(ur, cuts = c, delta = delta) for ur in get_illustration_data_from_book(u) ]
#st.markdown('\n'.join(["![]({i})".format(i=u) for u in urls][:100]))
#st.markdown("<style>div {margin-top:1px; margin-bottom:2px}</style>\n" +
#    '\n'.join(["""<div><img src="{i}"  width=100% max-width=600px; /></div>""".format(i=u) for u in urls][:100]), unsafe_allow_html = True)

st.markdown(display_books(books), unsafe_allow_html = True)
