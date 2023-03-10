# Необходимые дополнительные библиотеки:
# 1. magic(установка: pip install python-magic)
# 2. утилита lzip для linux(установка: sudo apt get install lzip(Ubuntu))
# Остальные библиотеки и утилиты предусатнволены изначально
# Скрипт успешно работает только на Unix-подобных системах

import magic
import uu
import os
import time

print(magic.from_file('file'))

path='file'

while True:
    s = magic.from_file(path)
    print(s)
    if 'uuencoded' in s:
        uu.decode(path, path, mode=None, quiet=False)
    elif 'ar archive' in s:
        os.popen('ar x file')
        time.sleep(1)
        os.popen('cp flag file')
        os.popen('rm flag')
    
    elif 'cpio' in s:
        os.popen('cpio -i < file')
        time.sleep(1)
        os.popen('cp flag file')
        os.popen('rm flag')

    elif 'bzip2' in s:
        os.popen('mv file file.bz2')
        os.popen('bzip2 -d file.bz2')
        time.sleep(1)

    elif 'gzip' in s:
        os.popen('mv file file.gz')
        time.sleep(1)
        os.popen('gunzip -c file.gz > file')
        time.sleep(1)
        os.popen('rm file.gz')

    elif 'lzip' in s:
        os.popen('mv file file.lz')
        os.popen('lzip -d file.lz')
        time.sleep(1)

    elif 'LZ4' in s:
        os.popen('mv file file.lz4')
        time.sleep(1)
        os.popen('lz4 -dc file.lz4 > file')
        time.sleep(1)
        os.popen('rm file.lz4')

    elif 'LZMA' in s:
        os.popen('mv file file.xz')
        os.popen('lzma -d file.xz')
        time.sleep(1)

    elif 'lzop' in s:
        os.popen('mv file file.lzo')
        os.popen('lzop -d file.lzo')
        time.sleep(1)
        os.popen('rm file.lzo')
    
    elif 'XZ' in s:
        os.popen('mv file file.xz')
        os.popen('xz -dc file.xz > file')
        time.sleep(1)
        os.popen('rm file.xz')

    elif 'ASCII' in s and 'uuencode' not in s:
        os.popen('cat file | xxd -r -p 2>&1 > file2')
        time.sleep(1)
        f = open('file2', 'r').read()
        print(f)
        break
    else:
        print("Decoder for this type NOT FOUND")
        break
