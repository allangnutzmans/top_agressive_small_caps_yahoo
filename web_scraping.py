import requests
import pandas as pd
from bs4 import BeautifulSoup

num_paginas = int(input("Número de páginas desejadas: "))


def rowIndex(num_paginas):
    urls = []
    for pagina_atual in range(num_paginas):
        pagina_atual *= 25
        url_count = "?count=25&offset=" + str(pagina_atual)
        url = "https://finance.yahoo.com/screener/predefined/aggressive_small_caps" + url_count
        urls.append(url)
    scrape(urls)


def scrape(urls):
    data = {}

    for url in urls:
        print(url)
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")

        # head
        thead = doc.thead
        thead = thead.contents

        # extrair head
        for tr in thead:
            for th in tr.find_all('th'):
                header = th.text
                data.setdefault(header, [])  # Use setdefault to initialize if not exists

        # body
        tbody = doc.tbody
        trcts = tbody.contents

        # extrair cada linha do body
        for tr in trcts:
            row_data = []
            for td in tr.find_all('td'):
                row_data.append(td.text)

            for idx, header_key in enumerate(data.keys()):
                data[header_key].append(row_data[idx])

    # salvar no excel
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel("output.xlsx", index=False)


# Call the function
rowIndex(num_paginas)
