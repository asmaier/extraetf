import requests
import json

import importlib.resources as resources
from extraetf import __name__ as pkg_name

BASE_URL = "https://extraetf.com/api-v3/stock/search/full"

ORDERING_OPTIONS = ["asc", "desc"]

# sorting
SORT_OPTIONS = [
"isin",
"country",
"earnings_per_share",
"currency_of_annual_filing",
"dividend_yield",
"market_cap",
"last_price",
"morningstar_standard_name",
"calculated_return_price_1w",
"calculated_return_price_1m",
"calculated_return_price_3m",
"calculated_return_price_6m",
"calculated_return_price_1y",
"calculated_return_price_ytd",
"sparplan_faehig",
"the_type_of_dividend_in_a_corporate_action",
"indicated_annual_dividend",
"price_to_eps",
"price_to_book",
"ps_ratio",
"price_to_cash_flow",
"ms_pe_growth_ratio",
"return_on_investment",
]

# read stock_filters.json
filters_path = resources.files(pkg_name) / "resources" / "stock_filters.json"
with filters_path.open() as f:
    data = json.load(f)
    filter_options = data["filters"]

# add missing options
filter_options["ms_marketcap"] = [
      {
        "id": "ms_marketcap",
        "label": "ms_marketcap",
        "count": 0,
        "min": None,
        "max": None
      }
    ]
filter_options["dividend_yield"] = [
      {
        "id": "dividend_yield",
        "label": "dividend_yield",
        "count": 0,
        "min": None,
        "max": None
      }
    ]

def show_sort_options():
    return SORT_OPTIONS

def show_filter_options():
    return list(filter_options.keys())

def get_filter_id_from_label(key, label):
    for entry in filter_options[key]:
        if entry["name"] == label:
            id = entry["id"]
            return str(id).lower() if isinstance(id, bool) else str(id)

def convert_filter_to_params(filter):
    params = ""
    for key, value in filter.items():
        if key not in filter_options:
            raise Exception(f"Invalid filter option: {key}")
        # categorical filters
        if isinstance(value, list):
            params+=f"&{key}="
            params+=",".join([get_filter_id_from_label(key, v) for v in value])
            continue
        # numerical filters
        if isinstance(value, dict):
            if "gt" in value or "lt" in value:
                if "gt" in value:
                    params+=f"&{key}__gt={value['gt']}"
                if "lt" in value:    
                    params+=f"&{key}__lt={value['lt']}"
            else:
                for subkey, subvalue in value.items():
                    subid = get_filter_id_from_label(key, subkey)
                    if "gt" in subvalue:       
                        params+=f"&{key}__{subid}__gt={subvalue['gt']}"
                    if "lt" in subvalue:    
                        params+=f"&{key}__{subid}__lt={subvalue['lt']}"
            continue
    
    return params

def parse_response(response):
    json = response.json()

    results = []

    for result in json["results"]:

        name = result["morningstar_standard_name"]
        isin = result["isin"]
        country = result["country"]
        sector = result["sector_code"]
        industry = result["industry_code"]
        earnings_per_share = result["earnings_per_share"]
        dividend_yield = result["dividend_yield"]
        market_cap = result["market_cap"]
        price_to_eps = result["price_to_eps"] # KGV
        price_to_book = result["price_to_book"] # KBV
        ps_ratio = result["ps_ratio"] # KUV
        price_to_cash_flow = result["price_to_cash_flow"] # KCV
        return_on_investment = result["return_on_investment"]
        week_1 = result["calculated_return_price_1w"]
        month_1 = result["calculated_return_price_1m"]
        month_3 = result["calculated_return_price_3m"]
        month_6 = result["calculated_return_price_6m"]
        current_year = result["calculated_return_price_ytd"]
        year_1 = result["calculated_return_price_1y"]        

        entry = {
            "name": name, 
            "isin": isin,
            "country": country,
            "sector": sector,
            "industry": industry,
            "earnings_per_share": earnings_per_share,
            "dividend_yield": dividend_yield,
            "market_cap": market_cap,
            "price_to_eps": price_to_eps,
            "price_to_book": price_to_book,
            "ps_ratio": ps_ratio,
            "price_to_cash_flow": price_to_cash_flow,
            "return_on_investment": return_on_investment,
            "week_1": week_1,
            "month_1": month_1,
            "month_3": month_3,
            "month_6": month_6,  
            "current_year": current_year,
            "year_1": year_1, 
        }

        results.append(entry)

    return results    
        

def search(sort_by, ordering, limit: int=25, filters=None ):

    if sort_by not in SORT_OPTIONS:
        raise Exception(f"Invalid sort_by option: {sort_by}")

    if ordering not in ORDERING_OPTIONS:
        raise Exception(f"Invalid ordering option: {ordering}")
                
    url = BASE_URL

    if ordering == "desc":
        sort_by = f"-{sort_by}"    

    url += f"?&ordering={sort_by}&limit={limit}"
    if filters:
        url += convert_filter_to_params(filters) 

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    else:
        results = parse_response(response)

    return results    
