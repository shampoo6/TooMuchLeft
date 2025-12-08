import concurrent.futures
import os
import shutil

test_dir_name = 'test_dir'
test_file_count = 3000
file_size = 1

shutil.rmtree(test_dir_name, ignore_errors=True)
os.makedirs(test_dir_name, exist_ok=False)


def mk_file(file_name):
    with open(file_name, 'wb') as f:
        f.write(os.urandom(file_size))


with concurrent.futures.ThreadPoolExecutor() as executor:
    fs = executor.map(mk_file, [os.path.join(test_dir_name, f'test_{i}.jpg') for i in range(test_file_count)])
    concurrent.futures.as_completed(fs)
print('make over')
