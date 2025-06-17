import streamlit as st
import random

st.set_page_config(layout="wide")

# CSS styling
st.markdown("""
    <style>
    input[type="text"] {
        max-width: 120px;
    }
    .tal-liste {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .input-label {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("ℹ️ Om denne app")
    st.markdown("""
    **📘 Formål:**  
    Du får vist en række naturlige tal i tilfældig rækkefølge.  
    Din opgave er at finde og indtaste følgende:
    - Minimum  
    - Q1 (første kvartil)  
    - Median  
    - Q3 (tredje kvartil)  
    - Maksimum  
    - Kvartilbredde (Q3 - Q1)  
    - Variationsbredde (Maks - Min)

    Appen tjekker dine svar og giver dig feedback.

    ---
    **📄 Licens:**  
    Dette projekt bruger [MIT-licensen](https://opensource.org/licenses/MIT).  
    Udviklere: OpenAI ChatGPT og Jens Kaalby Thomsen
    """)

def generer_tal():
    n = random.randint(10, 16)
    if n > 12:
        unikke_tal = random.sample(range(1, 41), k=random.randint(5, 8))
    else:
        unikke_tal = random.sample(range(1, 101), k=n)
    return random.choices(unikke_tal, k=n)

def beregn_kvartiler(tal):
    tal_sorteret = sorted(tal)
    n = len(tal_sorteret)

    def median(liste):
        m = len(liste)
        midt = m // 2
        if m % 2 == 0:
            return (liste[midt - 1] + liste[midt]) / 2
        else:
            return liste[midt]

    min_v = tal_sorteret[0]
    max_v = tal_sorteret[-1]
    variationsbredde = max_v - min_v

    med = median(tal_sorteret)
    if n % 2 == 0:
        nedre_halvdel = tal_sorteret[:n//2]
        oevre_halvdel = tal_sorteret[n//2:]
    else:
        nedre_halvdel = tal_sorteret[:n//2]
        oevre_halvdel = tal_sorteret[n//2+1:]

    q1 = median(nedre_halvdel)
    q3 = median(oevre_halvdel)
    iqr = q3 - q1

    return min_v, q1, med, q3, max_v, iqr, variationsbredde

if 'tal' not in st.session_state or st.button("Ny opgave"):
    st.session_state.tal = generer_tal()
    st.session_state.feedback = ["➖"] * 7

tal = st.session_state.tal
r_min, r_q1, r_med, r_q3, r_max, r_iqr, r_var = beregn_kvartiler(tal)
rigtige = [r_min, r_q1, r_med, r_q3, r_max, r_iqr, r_var]

labels = ["Minimum", "Q1", "Median", "Q3", "Maksimum", "Kvartilbredde", "Variationsbredde"]
keys = ["min", "q1", "median", "q3", "maks", "iqr", "variation"]

st.title("Statistikopgave: Kvartiler og variation")
st.write("### Rækken af tal (i tilfældig rækkefølge):")
st.markdown(f'<div class="tal-liste">{", ".join(map(str, tal))}</div>', unsafe_allow_html=True)

st.write("### Indtast dine svar:")
input_values = []

cols = st.columns(7)
for i in range(7):
    col = cols[i]
    with col:
        st.markdown(f'<div class="input-label">{st.session_state.feedback[i]} <b>{labels[i]}</b></div>', unsafe_allow_html=True)
        user_input = st.text_input("", value="", label_visibility="collapsed", key=f"input_{keys[i]}")
        try:
            val = float(user_input.strip().replace(",", "."))
        except:
            val = None
        input_values.append(val)

if st.button("Tjek svar"):
    fejl = []
    ny_feedback = []

    for i, (bruger, rigtig) in enumerate(zip(input_values, rigtige)):
        if bruger is None or bruger != rigtig:
            fejl.append(f"❌ {labels[i]} er forkert. Rigtigt svar: {rigtige[i]}")
            ny_feedback.append("❌")
        else:
            ny_feedback.append("✅")

    st.session_state.feedback = ny_feedback

    if fejl:
        st.error("Der er fejl i dine svar:")
        for f in fejl:
            st.write(f)
    else:
        st.success("✅ Alle svar er korrekte! Godt gået! 🎉")

if st.button("Vis løsning"):
    st.info("**Løsning:**")
    st.write(f"- Minimum: {r_min}")
    st.write(f"- Q1: {r_q1}")
    st.write(f"- Median: {r_med}")
    st.write(f"- Q3: {r_q3}")
    st.write(f"- Maksimum: {r_max}")
    st.write(f"- Kvartilbredde (Q3 - Q1): {r_iqr}")
    st.write(f"- Variationsbredde (Maks - Min): {r_var}")
