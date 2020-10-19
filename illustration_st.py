import dhlab.module_update as mu
#mu.update("nbpictures", silent = True)
from nbpictures import urns_from_super, iiif_manifest, display_finds, get_urls_from_illustration_data,get_illustration_data_from_book
from IPython.display import HTML, Markdown, display
import streamlit as st



search = st.text_input('Søk etter', 'Churchill')
              
urns = urns_from_super(search, period=('19200101', '19900101'))

u = st.selectbox("velg en bok", urns[:5])
              
#u = st.text_input('URN', urns[0])
c = st.checkbox('deler')
st.markdown('\n'.join(['**' + x['label'] + '**: ' + x['value'] for x in iiif_manifest(u)['metadata']]), unsafe_allow_html=True)

urls = [get_urls_from_illustration_data(ur, cuts = c) for ur in get_illustration_data_from_book(u) ]
st.markdown('\n'.join(["![]({i})".format(i=u) for u in urls]))