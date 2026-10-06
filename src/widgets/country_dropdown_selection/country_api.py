from requests_cache import CachedSession
from requests.adapters import HTTPAdapter
from typing import Any, List
from dataclasses import dataclass

@dataclass
class Country:
    name: str = "default"               # Country's name
    slug: str = "default"
    alpha2_code: str = "DEFAULT"        # Country's alpha2 code (2 letter code representing its name)
    alpha3_code: str = "DEFAULT"        # Country's alpha3 code (3 letter code representing its name)
    flag: str = "DEFAULT"               # URL for a svg file of the country's flag
    currency_code: str = "DEFAULT"      # ISO 3166-1 country code, representing its currency (i.e USD and EUR)
    currency_symbol: str = "DEFAULT"    # Country's currency symbol

class CountryApiWrapper:
    def __init__(self, base_url: str = 'https://countries.dev', cache_name: str = 'countryCache', backend: str = 'sqlite') -> None:
        self._session = CachedSession(cache_name=cache_name, backend=backend)
        self._base_url = base_url
        self._session.headers.update({
            "Content-Type": "application/json"
        })
        self._adapter = HTTPAdapter(pool_connections=20, pool_maxsize=50)
        self._session.mount('http://', self._adapter)
        self._session.mount('https://', self._adapter)

    def _request(self, method, endpoint:str , **kwargs) -> Any:
        url = f'{self._base_url}{endpoint}'
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_all_countries(self) -> List[Country]:
        response = self._request(method='GET', endpoint='/countries')
        all_countries: List[Country] = []
        for item in response:
            #all_countries.append(Country(**item))
            all_countries.append(Country(
                name=item['name'],
                slug=item['flag'],
                alpha2_code=item['alpha2Code'],
                alpha3_code=item['alpha3Code'],
                flag=f'static/{item['alpha2Code']}.svg',
                currency_code=item['currencies'][0]['code'],
                currency_symbol=item['currencies'][0]['symbol']
            ))

    def get_country_by_name(self, name: str) -> List[Country]:
        response = self._request(method='GET', endpoint=f'/name/{name}')#[0]
        all_countries: List[Country] = []
        for item in response:
            all_countries.append(Country(
                name=item['name'],
                slug=item['flag'],
                alpha2_code=item['alpha2Code'],
                alpha3_code=item['alpha3Code'],
                flag=f'static/{item['alpha2Code']}.svg',
                currency_code=item['currencies'][0]['code'],
                currency_symbol=item['currencies'][0]['symbol']
            ))
        return all_countries

    def close(self):
        self._session.close()
