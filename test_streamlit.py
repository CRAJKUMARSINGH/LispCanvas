import streamlit as st

# Test if set_page_config is available
if hasattr(st, 'set_page_config'):
    print("set_page_config is available")
    getattr(st, 'set_page_config')(page_title="Test App", layout="wide")
    getattr(st, 'title')("Streamlit Test")
    getattr(st, 'write')("set_page_config works correctly!")
else:
    print("set_page_config is NOT available")
    print("Available attributes in st module:")
    print([attr for attr in dir(st) if not attr.startswith('_')])