import os
import sys
import tkinter as tk
from getopt import getopt
from tkinter import filedialog, messagebox, simpledialog

from aes import AES256
from utils import join_chunk, write_to_chunk

argumentList = sys.argv[1:]

options = "hi:o:k:m:"

long_options = ["input=", "help", "mode=", "key=", "output="]


def count_args():
    return len(sys.argv)


def check_key_len(key):
    key_len = len(key)
    return not (key_len != 16 and key_len != 32)


def main():
    root = tk.Tk()
    root.withdraw()
    key = ""
    mode = "E"
    out = ""
    path = ""

    try:
        args, values = getopt(argumentList, options, long_options)

        for curr_arg, curr_val in args:
            if curr_arg in ("-h", "--help"):
                print(
                    "Run without any arguments to enter GUI mode\n[-m, --mode] (E)ncrypt/ (D)ecrypt (Default mode is Encrypt)\n[-i, --input] For input file path\n[-p, --plain] For plain text input\n[-o, --output] For output file path"
                )
                sys.exit()
            elif curr_arg in ("-m", "--mode"):
                mode = curr_val
            elif curr_arg in ("-i", "--input"):
                path = curr_val
            elif curr_arg in ("-k", "--key"):
                key = curr_val
            elif curr_arg in ("-o", "--output"):
                out = curr_val

    except getopt.error as err:
        print(str(err))

    if count_args() == 1:
        mode_of_proc = messagebox.askyesno(
            "AES", "Press yes to enter encryption mode or no to decrypt"
        )
        if mode_of_proc:
            mode = "E"
        else:
            mode = "D"
        key = simpledialog.askstring(
            "Input", "Please enter the key", parent=root)
        if not key:
            messagebox.showerror("Error", "Key is required")
            sys.exit()
        elif not check_key_len(key):
            messagebox.showerror("Error", "Invalid key size")
            sys.exit()
        path = filedialog.askopenfilename(title="Please choose input file")
        if not path:
            messagebox.showerror("Error", "Input file is required")
            sys.exit()
        _, file_ext = os.path.splitext(path)

        out_dir = filedialog.askdirectory(title="Please specify output folder")
        if not out_dir:
            messagebox.showerror("Error", "Output folder is required")
            sys.exit()
        if mode == "E":
            out = out_dir + "/encrypted" + file_ext
        elif mode == "D":
            out = out_dir + "/decrypted" + file_ext

    if key == "":
        sys.exit("Key is required")
    elif not check_key_len(key):
        sys.exit("Invalid key size")

    if path == "":
        sys.exit("Please provide input path")
    else:
        my_aes = AES256(key)
        if mode == "E":
            file = open(path, "rb")
            raw = file.read()
            encrypted = my_aes.encrypt(raw)
            if out is None:
                print(encrypted)
            else:
                write_to_chunk(encrypted, out)
                # outFile = open(out, "wb+")
                # outFile.write(encrypted)
                # outFile.close()
        elif mode == "D":
            raw_join = join_chunk(path)
            # file = open(path, "rb")
            # raw = file.read()
            decrypted = my_aes.decrypt(raw_join)
            if out is None:
                print(decrypted)
            else:
                outFile = open(out, "wb+")
                outFile.write(decrypted)
                outFile.close()
        else:
            sys.exit("Invalid method")


if __name__ == "__main__":
    main()
