from hashlib import md5
from math import ceil
from os import getcwd, path, walk
from re import compile

# from py_vmdetect import VMDetect


def join_chunk(file_path: str):
    dir_name, filename, ext = get_file_info_from_path(file_path)
    files = []
    searched_regex = compile(filename)
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for filename in filenames:
            if searched_regex.search(filename):
                files.append(path.join(dirpath, filename))
    files.sort()
    concat_bytes = b""
    for file in files:
        f = open(file, "rb")
        concat_bytes += f.read()
        f.close()
    return concat_bytes


def write_to_chunk(content: bytes, out_dir: str):
    half = ceil(len(content) / 2)
    list_bytes = list(content)
    for i in range(0, 2):
        if i == 0:
            out = open(out_dir, "wb+")
        else:
            out = open(get_indexed_path(out_dir, i), "wb+")
        out.write(bytes(list_bytes[i*half:i*half+half]))
        out.close()


def get_indexed_path(file_path: str, idx: int):
    dir_name, filename, ext = get_file_info_from_path(file_path)
    return path.join(dir_name, f"{filename}_{str(idx)}.{ext}")


def get_file_info_from_path(file_path: str):
    dir_name = path.dirname(file_path)
    file = path.basename(file_path)
    filename, ext = file.split(".")
    return dir_name, filename, ext


# def is_env_vm():
#     vmd = VMDetect()
#     return vmd.is_vm()


def generate_source_hash():
    curr_dir = path.join(getcwd(), "app")
    searched_regex = compile(r"\.py$")
    str_to_hashed = ""
    for (dirpath, dirnames, filenames) in walk(curr_dir):
        for filename in filenames:
            if searched_regex.search(filename):
                f = open(path.join(curr_dir, filename))
                str_to_hashed += f.read()
                f.close()

    return md5(str_to_hashed.encode()).hexdigest()


def is_source_modified():
    initial_hash = generate_source_hash()
    filepath = path.join(getcwd(), "app", ".secret")
    file = open(filepath, "r")
    stored_hash = file.read()
    file.close()
    print(initial_hash, stored_hash)
    return stored_hash != initial_hash
