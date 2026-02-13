from extraetf import etfs, stocks


def test_convert_filters_etfs():
    filters = {
        "asset_class": ["Aktien"],   
        "product_type":["ETF", "ETC"],
        "country": ["USA"], 
        "risk_measures": {"1 Jahr": {"from": -50, "to": -10}}, 
        "aum": {"from": 50},
    }

    params = etfs.convert_filter_to_params(filters)
    assert params == "&asset_class=2&product_type=etf,etc&country=22&risk_measures__1_year_from=-50&risk_measures__1_year_to=-10&aum_from=50" #noqa: E501

def test_convert_filters_stocks():
    filters = {
        "country": ["Deutschland"],
        "dividend": [True],
        "ms_marketcap": {"gt": 1000000000},
        "dividend_yield": {"gt": 3, "lt": 15},
        "sector": ["Grundmaterialien"],
    }

    params = stocks.convert_filter_to_params(filters)
    assert params == "&country=de&dividend=true&ms_marketcap__gt=1000000000&dividend_yield__gt=3&dividend_yield__lt=15&sector=101" #noqa: E501


    