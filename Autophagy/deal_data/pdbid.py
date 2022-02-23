
import bs4
import requests
import pandas as pd
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MCDB.settings")
django.setup()
from app import models

def pdbSearch(name):
    pdb = []
    # try:
    #     url = 'https://www.uniprot.org/uniprot/'+name
    #     page = requests.get(url)
    #     soup = bs4.BeautifulSoup(page.text, "html5lib")
    #     uniports = soup.find_all(class_='pdb')
    #     for uniport in uniports:
    #         set1.add(uniport.string)
    # except:
    #     set1 = set()

    cookies = {
        '_ga': 'GA1.2.1923498727.1595773784',
        '_gid': 'GA1.2.322086251.1595773784',
        '_gat_gtag_UA_3923365_3': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://www.rcsb.org',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.rcsb.org/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    data = {"query": {"parameters": {"value": name}, "service": "text", "type": "terminal", "node_id": 0}, "return_type": "entry", "request_options": {"pager": {"start": 0,
                                                                                                                                                                 "rows": 1000}, "scoring_strategy": "combined", "sort": [{"sort_by": "score", "direction": "desc"}]}, "request_info": {"src": "ui", "query_id": "f13c12e09dc43d395a2b3625f00f9dad"}}

    page = s.post('https://www.rcsb.org/search/data',
                  headers=headers, cookies=cookies, data=json.dumps(data))
    res = json.loads(page.text)
    if 'statusCode' in res:
        return []
    for data in res['result_set']:
        pdb.append(data['identifier'])
    # print(len(pdb))
    cookies = {
        '_ga': 'GA1.2.1923498727.1595773784',
        '_gid': 'GA1.2.322086251.1595773784',
        '_gat_gtag_UA_3923365_3': '1',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://www.rcsb.org',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.rcsb.org/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    data = {"attributes": None, "identifiers": pdb,
            "returnType": "entry", "report": "search_summary"}

    page = s.post('https://www.rcsb.org/search/gql',
                  headers=headers, cookies=cookies, data=json.dumps(data))
    res = json.loads(page.text)
    # print(res)
    if 'statusCode' in res:
        return []
    return res


s = requests.session()
s.keep_alive = False
# pdbSearch('O60885')

fk = {}
level = {}
genes = models.gene.objects.all()
for gene in genes:
    fk[gene.uniprotKB] = gene.gene
    level[gene.uniprotKB] = gene.level
file = pd.read_excel(io='data.xlsx', sheet_name=1)

es = []
names = file.iloc[:, 15]
models.pdb.objects.all().delete()
print(names)
cnt = 0
fkkk = 0
for name in names:
    fkkk+=1
    print(fkkk,name)
    # if fkkk<1133:
        # continue
    js = pdbSearch(name)
    for data in js:
        cnt += 1
        mt = data['data']['exptl'][0]['method']
        if 'resolution' in data['data']['exptl'][0]:
            mt += ' '+str(data['data']['exptl'][0]['resolution'])+' Å'
        models.pdb.objects.create(
            id=cnt,
            uniprot=name,
            gene=fk[name],
            pdb=data['identifier'],
            date=data['data']['initial_release_date'],
            method=mt,
            level=level[name]
        )


# cnt = 0
# # names=names[:10]
# dnames = []
# pdbid = []
# date = []
# method = []
# resolution = []
# for name in names:
#     # if cnt==2:
#     #     break
#     cnt += 1
#     print(cnt)
#     js = pdbSearch(name)
#     for data in js:
#         dnames.append(name)
#         # print(data['data']['exptl'])
#         if len(data['data']['exptl']) > 1:
#             print(name)
#         pdbid.append(data['identifier'])
#         date.append(data['data']['initial_release_date'])
#         mt = data['data']['exptl'][0]['method']
#         if 'resolution' in data['data']['exptl'][0]:
#             mt += ' '+str(data['data']['exptl'][0]['resolution'])+' Å'
#         method.append(mt)

# data = pd.DataFrame(data=[dnames, pdbid, date, method, resolution], index=[
#                     'UniProtKB ID', 'pdb', 'date', 'method', 'resolution'], columns=range(1, len(dnames)+1)).T
# data.to_csv('data/rcsb.csv')
