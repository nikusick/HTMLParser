import asyncio
import re
from typing import List
import aiohttp


class HTMLTelParser:

    tel_regex = r"(((\+7|8)?[\s(-]*\d{3}[-)\s]*)?\d{3}-\d{2}-\d{2})"

    def transform_tel(self, tel: str):
        tel = tel.replace(' ', '')
        tel = tel.replace('(', '')
        tel = tel.replace(')', '')
        tel = tel.replace('-', '')
        tel = tel.replace('+7', '8')
        if len(tel) == 7:
            tel = '8495' + tel
        elif len(tel) == 6:
            tel = '8' + tel
        return tel

    async def get_phones(self, client: aiohttp.ClientSession, url: str):
        async with client.get(url, ssl=False) as response:
            html = await response.read()
            telephones = re.findall(self.tel_regex, html.decode())
            await asyncio.sleep(1)
            return url, list({self.transform_tel(tel[0]) for tel in telephones})

    async def get_all_phones(self, urls: List[str]):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=None), trust_env=True,
                                         timeout=aiohttp.ClientTimeout(15)) as client:
            tasks = [self.get_phones(client, url) for url in urls]
            return await asyncio.gather(*tasks)


def main():
    html_tel_parser = HTMLTelParser()
    res = asyncio.run(html_tel_parser.get_all_phones(['https://hands.ru/company/about', 'https://repetitors.info']))
    print(res)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
