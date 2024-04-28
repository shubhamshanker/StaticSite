import os
import shutil


def copy_files_recursive(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for filename in os.listdir(src_path):
        from_path = os.path.join(src_path, filename)
        to_path = os.path.join(dst_path, filename)
        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_files_recursive(from_path, to_path)