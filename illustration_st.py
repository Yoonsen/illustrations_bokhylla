import dhlab.module_update as mu
#mu.update("nbpictures", silent = True)
from nbpictures import urns_from_super, iiif_manifest, display_finds, get_urls_from_illustration_data,get_illustration_data_from_book
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
if search == "":
    urns = ["URN:NBN:no-nb_digibok_2017081626006"]
else:
    urns = urns_from_super(search, period=("{s}0101".format(s = period_slider[0]), "{s}1231".format(s=period_slider[1])))

u = st.selectbox("Velg en bok (URN) fra listen under", urns[:10])

mdata = dict()
try:
    mdata = {x['label']:x['value'] for x in iiif_manifest(urns[0])['metadata']}
    c = not 'alle' in mdata['Tilgang']
except:
    True
    
#u = st.text_input('URN', urns[0])

c = st.checkbox('Vis bare en del av bildene - om boken ikke er åpen for alle', value = c)

st.markdown('\n'.join(['**' + x + '**: ' + mdata[x] for x in mdata]), unsafe_allow_html=True)

urls = [get_urls_from_illustration_data(ur, cuts = c) for ur in get_illustration_data_from_book(u) ]
#st.markdown('\n'.join(["![]({i})".format(i=u) for u in urls][:100]))
st.markdown('\n'.join(["""<img src="{i}" alt="drawing" width="600"/>""".format(i=u) for u in urls][:100]), unsafe_allow_html = True)