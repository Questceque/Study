import aiohttp
import asyncio
import json
import nest_asyncio
from bs4 import BeautifulSoup
from typing import List, Dict

SP500_URL = "https://markets.businessinsider.com/index/components/s&p_500"
CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def get_usd_to_rub(session: aiohttp.ClientSession) -> float:
    xml_data = await fetch(session, CBR_URL)
    soup = BeautifulSoup(xml_data, 'xml')
    usd_rate_element = soup.find("Valute", {'ID': 'R01235'})
    if usd_rate_element:
        usd_rate = usd_rate_element.find("Value").text.replace(',', '.')
        return float(usd_rate)
    return 0.0

async def get_sp500_companies(session: aiohttp.ClientSession) -> List[Dict[str, str]]:

    html = await fetch(session, SP500_URL)
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select(".table__tr")
    companies = []


    for row in rows[1:]:
        cols = row.select(".table__td")
        if len(cols) < 5:
            continue
        name = cols[0].text.strip()
        url = cols[0].find("a")["href"]
        try:
            growth = float(cols[4].text.strip().replace('%', '').replace(',', '.'))
        except ValueError:
            growth = 0.0
        companies.append({"name": name, "url": url, "growth": growth})

    print(f"Найдено компаний: {len(companies)}")
    return companies

async def get_company_data(session: aiohttp.ClientSession, company: Dict[str, str], usd_to_rub: float) -> Dict:
    html = await fetch(session, "https://markets.businessinsider.com" + company["url"])
    soup = BeautifulSoup(html, 'html.parser')

    try:
        code_element = soup.select_one(".price-section__category")
        price_element = soup.select_one(".price-section__current-value")
        pe_element = soup.find(text="P/E Ratio")
        low_52_element = soup.find(text="52 Week Low")
        high_52_element = soup.find(text="52 Week High")

        code = code_element.text.split(" ")[-1] if code_element else "N/A"
        price = float(price_element.text.replace(',', '')) * usd_to_rub if price_element else 0.0
        pe = float(pe_element.find_next().text.replace(',', '')) if pe_element else None
        low_52 = float(low_52_element.find_next().text.replace(',', '')) if low_52_element else 0.0
        high_52 = float(high_52_element.find_next().text.replace(',', '')) if high_52_element else 0.0
        potential_profit = ((high_52 - low_52) / low_52) * 100 if low_52 > 0 else 0.0
    except AttributeError:
        print(f"Ошибка при парсинге компании {company['name']}")
        return {}

    return {
        "code": code,
        "name": company["name"],
        "price": price,
        "P/E": pe,
        "growth": company["growth"],
        "potential profit": potential_profit
    }

async def main():
    async with aiohttp.ClientSession() as session:
        usd_to_rub = await get_usd_to_rub(session)
        if usd_to_rub == 0.0:
            print("ошибка")
            return

        companies = await get_sp500_companies(session)
        tasks = [get_company_data(session, company, usd_to_rub) for company in companies]
        data = await asyncio.gather(*tasks)
        data = [d for d in data if d]

        print(f"Собрано данных о {len(data)} компаниях")
        if data:
            print("Пример данных:", data[0])

        with open("top_price.json", "w") as f:
            json.dump(sorted(data, key=lambda x: x["price"], reverse=True)[:10], f, indent=4)
        with open("top_pe.json", "w") as f:
            json.dump(sorted(data, key=lambda x: x["P/E"])[:10], f, indent=4)
        with open("top_growth.json", "w") as f:
            json.dump(sorted(data, key=lambda x: x["growth"], reverse=True)[:10], f, indent=4)
        with open("top_potential.json", "w") as f:
            json.dump(sorted(data, key=lambda x: x["potential profit"], reverse=True)[:10], f, indent=4)

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
