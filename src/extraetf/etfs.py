import requests
import json

import importlib.resources as resources
from extraetf import __name__ as pkg_name

BASE_URL = "https://extraetf.com/api-v3/search/full/"

LEVERAGE_PARAMS = {
    "all" : "leverage=1",
    "long-only": "leverage_from=1&leverage_to=1",
    "long-leveraged": "leverage_from=1.001",
    "short": "leverage_from=-1&leverage_to=-1",
    "short-leveraged": "leverage_to=-1.01"
}

LEVERAGE_OPTIONS = ["all", "long-only", "long-leveraged", "short", "short-leveraged"]
ORDERING_OPTIONS = ["asc", "desc"]
SORT_OPTIONS = [
"symbol",
"market_cap",
"return_year_to_date_real",
"ter",
"currency",
"assets_under_management",
"return_1_week_real",
"return_1_month_real",
"return_3_month_real",
"return_6_month_real",
"return_1_year_real",
"return_3_years_ago_real",
"return_5_years_ago_real",
"price_date",
"period_last_year",
"period_2_years_ago",
"period_3_years_ago",
"period_4_years_ago",
"period_5_years_ago",
"yield_distribution_current_year",
"distribution_interval",
"distribution_months",
"distribution_cagr__year_1",
"distribution_cagr__year_3",
"distribution_cagr__year_5",
"distribution_cagr__from_creation",
"number_of_holding_combined",
"portfolio_items_weight",
"xlm",
"benchmark_trackingerror_1y",
"launch_date",
"volatility_1_year",
"volatility_3_years",
"sharpe_ratio_1_year",
"sharpe_ratio_3_years",
"mdd_1_year",
"mdd_3_years",
"tracking_difference_mean_yearly",
"tracking_difference_trailing_M1",
"tracking_difference_trailing_M3",
"tracking_difference_trailing_M6",
"tracking_difference_trailing_M12",
"tracking_difference_trailing_M36",
"tracking_difference_trailing_M0",
"tracking_difference_trailing_currency",
"tracking_difference_trailing_date",
"earnings_per_share",
"calculated_return_price_1w",
"calculated_return_price_1m",
"calculated_return_price_3m",
"calculated_return_price_6m",
"calculated_return_price_1y",
"calculated_return_price_ytd",
"dividend_yield",
"dividend_frequency",
"the_type_of_dividend_in_a_corporate_action",
"indicated_annual_dividend",
"price_to_eps",
"price_to_book",
"ps_ratio",
"price_to_cash_flow",
"ms_pe_growth_ratio",
"return_on_investment",
"price_change_percentage_24h_in_currency_eur",
"price_change_percentage_7d_in_currency_eur",
"price_change_percentage_14d_in_currency_eur",
"price_change_percentage_30d_in_currency_eur",
"price_change_percentage_60d_in_currency_eur",
"price_change_percentage_200d_in_currency_eur",
"price_change_percentage_1y_in_currency_eur",
"ath_change_percentage_eur",
"market_cap_rank",
"sentiment_votes_up_percentage",
"ongoing_charge_kiid",
"shareclass_currency",
"latest_net_assets_value",
"fund_portfolio_n_number_of_holdings",
"risk_and_rating_1_alpha",
"risk_and_rating_3_alpha",
"risk_and_rating_1_volatility",
"risk_and_rating_3_volatility",
"risk_and_rating_1_sharpe_ratio",
"risk_and_rating_3_sharpe_ratio",
"risk_and_rating_1_max_drawdown",
"risk_and_rating_3_max_drawdown"
]

# read etf_filters.json
filters_path = resources.files(pkg_name) / "resources" / "etf_filters.json"
with filters_path.open() as f:
    data = json.load(f)
    filter_options = data["filters"]

def show_sort_options():
    return SORT_OPTIONS

def show_filter_options():
    return list(filter_options.keys())

def get_filter_id_from_label(key, label):
    for entry in filter_options[key]:
        if entry["label"] == label:
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
            if "from" in value or "to" in value:
                if "from" in value:
                    params+=f"&{key}_from={value['from']}"
                if "to" in value:    
                    params+=f"&{key}_to={value['to']}"
            else:
                for subkey, subvalue in value.items():
                    subid = get_filter_id_from_label(key, subkey)
                    if "from" in subvalue:       
                        params+=f"&{key}__{subid}_from={subvalue['from']}"
                    if "to" in subvalue:    
                        params+=f"&{key}__{subid}_to={subvalue['to']}"
            continue
    
    return params

def parse_response(response):
    json = response.json()

    results = []

    for result in json["docs"]:

        name = result["fondname"]
        isin = result["isin"]
        week_1 = result["return_1_week_real"]
        month_1 = result["return_1_month_real"]
        month_3 = result["return_3_month_real"]
        month_6 = result["return_6_month_real"]
        current_year = result["return_year_to_date_real"]
        year_1 = result["return_1_year_real"]
        year_3 = result["return_3_years_ago_real"]
        year_5 = result["return_5_years_ago_real"]
        costs = result["ter"]
        volat_1 = result["volatility_1_year"]
        volat_3 = result["volatility_3_years"]
        sharpe_1 = result["sharpe_ratio_1_year"]
        sharpe_3 = result["sharpe_ratio_3_years"]
        try:
            drawdown_1 = result["risk_measures"]["1_year"]["max_drawdown"]
        except KeyError:
            drawdown_1 = None
        try:
            drawdown_3 = result["risk_measures"]["3_years"]["max_drawdown"]
        except KeyError:
            drawdown_3 = None         

        entry = {
            "name": name, 
            "isin": isin,
            "costs": costs,
            "week_1": week_1,
            "month_1": month_1,
            "month_3": month_3,
            "month_6": month_6,  
            "current_year": current_year,
            "year_1": year_1, 
            "year_3": year_3, 
            "year_5": year_5, 
            "volat_1": volat_1,
            "volat_3": volat_3,
            "sharpe_1": sharpe_1,
            "sharpe_3": sharpe_3, 
            "drawdown_1": drawdown_1,
            "drawdown_3": drawdown_3
        }

        results.append(entry)

    return results    
        

def search(sort_by, ordering, leverage="long-only", limit: int=25, filters=None ):

    if sort_by not in SORT_OPTIONS:
        raise Exception(f"Invalid sort_by option: {sort_by}")

    if ordering not in ORDERING_OPTIONS:
        raise Exception(f"Invalid ordering option: {ordering}")

    if leverage not in LEVERAGE_OPTIONS:
        raise Exception(f"Invalid leverage option: {leverage}")
                
    url = BASE_URL

    if ordering == "desc":
        sort_by = f"-{sort_by}"    

    url += f"?&{LEVERAGE_PARAMS[leverage]}&ordering={sort_by}&limit={limit}"
    if filters:
        url += convert_filter_to_params(filters) 

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    else:
        results = parse_response(response)

    return results    

