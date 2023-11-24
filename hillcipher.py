from tkinter import *
from tkinter import ttk
import numpy as np
import sympy
import string
import random
from math import gcd
alphabet = string.ascii_lowercase
msg_length =0

def modulo_multiplicative_inverse(A, M):
    # This will iterate from 0 to M-1
    for i in range(0, M):
        # If we have our multiplicative inverse, then return it
        if (A * i) % M == 1:
            return i
    # If we didn't find the multiplicative inverse in the loop above,
    # then it doesn't exist for A under M
    return -1

def decode(key_matrix, dimension, encrypted_message):
    matrix = sympy.Matrix(key_matrix)
    adj = (matrix.adjugate() % 26)  # TO FIND ADJOINT OF KEY MATRIX

    mat = np.matrix(key_matrix)

    det = (round(np.linalg.det(mat)) % 26)  # TO FIND DETERMINANT

    mult_inverse = modulo_multiplicative_inverse(det, 26)

    inv_m = (mult_inverse * adj) % 26

    decrypted_message = ""

    for index, i in enumerate(encrypted_message):
        values = []
        if index % dimension == 0:
            for j in range(0, dimension):
                if (index + j < len(encrypted_message)):
                    values.append([alphabet.index(encrypted_message[index + j])])
                else:
                    values.append([random.randint(0, 25)])
            vector = np.matrix(values)
            vector = inv_m * vector
            vector %= 26
            for j in range(0, dimension):
                decrypted_message += alphabet[vector[j]]

    return decrypted_message

def decode_hill():
    global msg_length
    # Clear previous error and decrypted text
    decode_error_label.config(text="")
    decrypted_text_label.config(text="")

    # Retrieve values from the input fields
    dimension = int(decoder_dimensions_entry.get())
    key_matrix = decoder_key_matrix_entry.get("1.0", "end-1c")  # Get the content of the Text widget
    encrypted_message = encrypted_text_entry.get()
    msg_length = len(encrypted_message)
    key = np.array([list(map(int, row.split())) for row in key_matrix.splitlines()])
    det = round(np.linalg.det(key))

    if det == 0 or det % 2 == 0 or det % 13 == 0:
        decode_error_label.config(text="Matrix is not invertible mod 26")
    else:
        decrypted_message = decode(key, dimension, encrypted_message)
        if(msg_length%dimension == 0):
            decrypted_text_label.config(text="Decrypted message: " + decrypted_message)
        else:
            decrypted_text_label.config(text="Decrypted message: " + decrypted_message[:-1])

    # Clear input fields
    decoder_dimensions_entry.delete(0, 'end')
    decoder_key_matrix_entry.delete("1.0", "end-1c")
    encrypted_text_entry.delete(0, 'end')

def encode(message, dimension, key):
    global msg_length 
    msg_length = len(message)
    encrypted_message = ""
    
    # Group message into vectors and generate the encrypted message
    for index, i in enumerate(message):
        values = []
        # Make blocks of N values
        if index % dimension == 0:
            for j in range(0, dimension):
                if (index + j < len(message)):
                    values.append([alphabet.index(message[index + j])])
                else:
                    values.append([random.randint(0, 25)])
            # Generate vectors and work with them
            vector = np.matrix(values)
            vector = key * vector
            vector %= 26
            for j in range(0, dimension):
                encrypted_message += alphabet[vector.item(j)]
    return encrypted_message.upper()

def encode_hill():
    
    # Clear previous error and encrypted text
    error_label.config(text="")
    encrypted_text_label.config(text="")

    # Retrieve values from the input fields
    dimension = int(dimensions_entry.get())
    key_matrix = key_matrix_entry.get("1.0", "end-1c")  # Get the content of the Text widget
    original_text = original_text_entry.get()
    msg_length = len(original_text)
    key = np.array([list(map(int, row.split())) for row in key_matrix.splitlines()])
    det = round(np.linalg.det(key))

    if det == 0 or det % 2 == 0 or det % 13 == 0:
        error_label.config(text="Matrix is not invertible mod 26")
    else:
        encrypted_text = encode(original_text, dimension, key)
        encrypted_text_label.config(text="Encrypted message: " + encrypted_text)

    # Clear input fields
    dimensions_entry.delete(0, 'end')
    key_matrix_entry.delete("1.0", "end-1c")
    original_text_entry.delete(0, 'end')

root = Tk()
root.geometry("444x333")
root.title("Hill Cipher")

notebook = ttk.Notebook(root)

tab1 = Frame(notebook)
tab2 = Frame(notebook)

notebook.add(tab1, text="Hill Encoder")
notebook.add(tab2, text="Hill Decoder")
notebook.pack(expand=True, fill="both")

# Add input fields to tab1
Label(tab1, text="Dimensions:").pack()
dimensions_entry = Entry(tab1)
dimensions_entry.pack()

Label(tab1, text="Key Matrix:").pack()
key_matrix_entry = Text(tab1, width=40, height=10)  # You can adjust the size as needed
key_matrix_entry.pack()

Label(tab1, text="Original Text:").pack()
original_text_entry = Entry(tab1)
original_text_entry.pack()


encode_button = Button(tab1, text="Encode", command=encode_hill)
encode_button.pack()

# Error message label for encoding
error_label = Label(tab1, text="", fg="red")
error_label.pack()

# Encrypted text label
encrypted_text_label = Label(tab1, text="")
encrypted_text_label.pack()

# Add input fields to tab2 for decoding
Label(tab2, text="Dimensions:").pack()
decoder_dimensions_entry = Entry(tab2)
decoder_dimensions_entry.pack()

Label(tab2, text="Key Matrix:").pack()
decoder_key_matrix_entry = Text(tab2, width=40, height=10)
decoder_key_matrix_entry.pack()

Label(tab2, text="Encrypted Text:").pack()
encrypted_text_entry = Entry(tab2)
encrypted_text_entry.pack()

decode_button = Button(tab2, text="Decode", command=decode_hill)
decode_button.pack()

# Error message label for decoding
decode_error_label = Label(tab2, text="", fg="red")
decode_error_label.pack()

# Decrypted text label
decrypted_text_label = Label(tab2, text="")
decrypted_text_label.pack()


root.mainloop()
