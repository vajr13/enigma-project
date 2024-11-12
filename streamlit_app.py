import streamlit as st
import time

# Definisi rotor dan reflektor
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fungsi untuk memutar rotor sesuai posisi awal
def rotate(rotor, offset):
    return rotor[offset:] + rotor[:offset]

# Fungsi plugboard untuk menukar huruf
def plugboard_swap(char, plugboard):
    return plugboard.get(char, char)

# Fungsi enkripsi satu karakter
def encrypt_character(char, rotor1, rotor2, rotor3, reflector, plugboard):
    char = plugboard_swap(char, plugboard)
    char = rotor1[ord(char) - ord('A')]
    char = rotor2[ord(char) - ord('A')]
    char = rotor3[ord(char) - ord('A')]
    char = reflector[ord(char) - ord('A')]
    char = chr(rotor3.index(char) + ord('A'))
    char = chr(rotor2.index(char) + ord('A'))
    char = chr(rotor1.index(char) + ord('A'))
    char = plugboard_swap(char, plugboard)
    return char

# Fungsi enkripsi atau dekripsi keseluruhan pesan
def enigma_process(message, rotor1, rotor2, rotor3, rotor_pos1, rotor_pos2, rotor_pos3, plugboard):
    processed_message = ""
    rotor1 = rotate(rotor1, rotor_pos1 - 1)
    rotor2 = rotate(rotor2, rotor_pos2 - 1)
    rotor3 = rotate(rotor3, rotor_pos3 - 1)
    for char in message:
        if char.isalpha():
            processed_message += encrypt_character(char.upper(), rotor1, rotor2, rotor3, reflector, plugboard)
            rotor1 = rotate(rotor1, 1)  # Putar rotor pertama setelah setiap karakter
    return processed_message

# Streamlit interface
st.title("Enigma Machine with Configurable Rotor and Plugboard")
message = st.text_input("Masukkan pesan", "")

# Pengaturan posisi rotor dalam satu baris dengan jarak
st.subheader("Setel Posisi Rotor (1-26) dalam satu baris")
col1, spacer, col2, spacer, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    rotor_pos1 = st.selectbox("Posisi Rotor 1", list(range(1, 27)), index=0)
with col2:
    rotor_pos2 = st.selectbox("Posisi Rotor 2", list(range(1, 27)), index=0)
with col3:
    rotor_pos3 = st.selectbox("Posisi Rotor 3", list(range(1, 27)), index=0)

# Initialize plugboard and selected button
if "plugboard" not in st.session_state:
    st.session_state.plugboard = {}
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None
if "pending_pair" not in st.session_state:
    st.session_state.pending_pair = None

# Tampilkan kotak A-Z untuk Plugboard
st.subheader("Plugboard: Klik dua huruf untuk memasangkan")

cols = st.columns(13)  # Menampilkan dua kolom dengan masing-masing 13 huruf
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i, char in enumerate(alphabet):
    col = cols[i % 13]  # Mengatur tata letak ke dalam dua kolom
    
    # Menampilkan kotak bawah untuk menunjukkan pasangan
    paired_char = st.session_state.plugboard.get(char, "")
    col.markdown(f"<div style='text-align: center; font-size: 1.5em;'>{paired_char}</div>", unsafe_allow_html=True)

    # Kotak atas yang dapat diklik untuk memilih pasangan
    if col.button(f"{char}", key=f"button_{char}"):
        if st.session_state.selected_button is None:
            st.session_state.selected_button = char
        elif st.session_state.selected_button == char:
            st.session_state.selected_button = None
        else:
            char1 = st.session_state.selected_button
            char2 = char
            st.session_state.pending_pair = (char1, char2)
            st.session_state.selected_button = None

# Update pasangan plugboard jika ada pasangan tertunda
if st.session_state.pending_pair:
    char1, char2 = st.session_state.pending_pair
    if char1 in st.session_state.plugboard:
        del st.session_state.plugboard[st.session_state.plugboard[char1]]
        del st.session_state.plugboard[char1]
    if char2 in st.session_state.plugboard:
        del st.session_state.plugboard[st.session_state.plugboard[char2]]
        del st.session_state.plugboard[char2]
    time.sleep(0.5)  # Delay sebelum menampilkan pasangan baru
    st.session_state.plugboard[char1] = char2
    st.session_state.plugboard[char2] = char1
    st.session_state.pending_pair = None

# Tombol reset plugboard
if st.button("Reset Plugboard"):
    st.session_state.plugboard.clear()
    st.session_state.selected_button = None
    st.write("Plugboard telah direset.")

# Proses enkripsi atau dekripsi
if message:
    processed_message = enigma_process(message, rotor_1, rotor_2, rotor_3, rotor_pos1, rotor_pos2, rotor_pos3, st.session_state.plugboard)
    st.write("Pesan yang diproses:", processed_message)
