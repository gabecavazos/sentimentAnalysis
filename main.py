import streamlit as st

st.set_page_config(page_title = "My Webpage", page_icon = ":smirk:", layout = 'wide')

#---- HEADER SECTION ----
with st.container():
    st.subheader("Fake Friends")
    st.title("see if yo homies fake or nah")
    st.write("we worked very hard on dis")
    st.write("[get rick rolled>](https://www.youtube.com/watch?v=At8v_Yc044Y)")

#---- WHAT I DO ----
with st.container():
    st.write("----")
    left, right = st.columns(2)
    with left:
        st.header("What I do")