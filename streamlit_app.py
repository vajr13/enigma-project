import streamlit as st

# Definisikan rotors dan reflektor
rotor_1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Fungsi untuk memutar rotor
def rotate(rotor):
    return rotor[1:] + rotor[0]

# Fungsi untuk enkripsi satu karakter
def encrypt_character(char, rotor1, rotor2, rotor3, reflector):
    # Lewatkan rotor pertama
    char = rotor1[ord(char) - ord('A')]
    # Lewatkan rotor kedua
    char = rotor2[ord(char) - ord('A')]
    # Lewatkan rotor ketiga
    char = rotor3[ord(char) - ord('A')]
    # Reflektor
    char = reflector[ord(char) - ord('A')]
    # Kembali melalui rotor (arah sebaliknya)
    char = chr(rotor3.index(char) + ord('A'))
    char = chr(rotor2.index(char) + ord('A'))
    char = chr(rotor1.index(char) + ord('A'))
    return char

# Fungsi utama Enigma (simetris untuk enkripsi dan dekripsi)
def enigma_process(message, rotor1, rotor2, rotor3):
    processed_message = ""
    for char in message:
        if char.isalpha():  # Hanya huruf yang dienkripsi/didekripsi
            # Proses enkripsi atau dekripsi (karena simetris)
            processed_char = encrypt_character(char.upper(), rotor1, rotor2, rotor3, reflector)
            processed_message += processed_char
            # Putar rotor setelah setiap huruf
            rotor1 = rotate(rotor1)
            rotor2 = rotate(rotor2)
            rotor3 = rotate(rotor3)
    return processed_message

# Streamlit Interface
st.title("Enigma Machine")

# Pilih posisi awal rotor
rotor1_position = st.number_input("Posisi Rotor 1 (1-26)", min_value=1, max_value=26, value=1)
rotor2_position = st.number_input("Posisi Rotor 2 (1-26)", min_value=1, max_value=26, value=1)
rotor3_position = st.number_input("Posisi Rotor 3 (1-26)", min_value=1, max_value=26, value=1)

# Pengaturan awal untuk rotors sesuai posisi input user
rotor1 = rotor_1[rotor1_position - 1:] + rotor_1[:rotor1_position - 1]
rotor2 = rotor_2[rotor2_position - 1:] + rotor_2[:rotor2_position - 1]
rotor3 = rotor_3[rotor3_position - 1:] + rotor_3[:rotor3_position - 1]

# Input pesan
message = st.text_input("Masukkan pesan untuk dienkripsi/dekripsi:")

# Proses enkripsi/dekripsi
if message:
    processed_message = enigma_process(message, rotor1, rotor2, rotor3)
    st.write(f"Pesan yang diproses: {processed_message}")

