import sys
import requests


def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(100*downloaded/total)
                print(done)

print('[*] Downloading test file of size 100 MB...')
download('https://speed.hetzner.de/100MB.bin', '100MB.bin')
print('[*] Done!')
