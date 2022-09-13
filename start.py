import requests

proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890", "ftp": "ftp://127.0.0.1:7890"}

# url =

payload={}
files=[

]
headers = {
  'Cookie': 'PHPSESSID=6jk2o11cran41brfm0ta5r99f9vrn5e3; __cf_bm=Pn5SLTlzx78Lbg_WssdwZlWW9BRZP4B_33dKwVk2F.g-1663040884-0-ARu+oGTRfDEuZyESQvnPPOcn2o0NBtpa/59wS/6mlE0QySEkG0yi7GVNm1Q32phF8AiqeHjwogp6gTUwjbVANuv01mF+MKAqhumTMBld+jNr; yuid_b=EGlTkJA'
}
i = 0
while True:
  response = requests.request("GET", "https://www.pixiv.net/ajax/illust/10089636"+str(i)+"?ref=https%3A%2F%2Fwww.pixiv.net%2Fartworks%2F100896360&lang=zh", headers=headers, data=payload, files=files, proxies=proxies)
  print(response.text)
  i+=1
