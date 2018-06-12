import requests


if __name__ == '__main__':
    url = 'http://0.0.0.0:8000'
    res_count = {}
    for _ in range(10):
        re = requests.get(url).text
        if re in res_count.keys():
            res_count[re] += 1
        else:
            res_count[re] = 1
    print(res_count)
