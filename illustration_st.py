import dhlab.module_update as mu
mu.update("nbpictures", silent = True)
from nbpictures import show_illustrations_urn, urns_from_super
from IPython.display import HTML, Markdown, display
import streamlit as st


st.text_input('Søk etter', 'Churchill')
              
urns = urns_from_super("Churchill", period=('19200101', '19900101'))


st.write(urns)
              
u = st.text_input('URN', urns[0])

st.write(show_illustrations_urn(u, 'fri'))