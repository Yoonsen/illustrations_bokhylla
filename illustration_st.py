import dhlab.module_update as mu
mu.update("nbpictures", silent = True)
from nbpictures import show_illustrations_urn, urns_from_super
from IPython.display import HTML, Markdown, display
import streamlit as st


def show_illustrations_urn(urn, tilgjengelig = 'fritt'):
   
    display(Markdown('\n'.join(['**' + x['label'] + '**: ' + x['value'] for x in iiif_manifest(urn)['metadata']])))
    
    if tilgjengelig.lower().startswith('fri'):
        c = False
    else:
        c = True
    return display_finds(
    [
        get_urls_from_illustration_data(u, cuts = c) for u in 
        get_illustration_data_from_book(urn)
    ]
)

st.text_input('Søk etter', 'Churchill')
              
urns = urns_from_super("Churchill", period=('19200101', '19900101'))


st.write(urns)
              
u = st.text_input('URN', urns[0])

st.write(show_illustrations_urn(u, 'fri'))