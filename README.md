# extraetf-scraper

This is a web scraper for ETF (and stock) data from the extraetf website.

[Extraetf](https://extraetf.com) is a German website, that provides information
about ETFs, stocks, funds and crypto. It offers the ability to search, sort and filter ETFs 
and stocks by many metrics.

This Python package makes accessing the data from extraetf easier.  

## Usage

Install the package from PyPi

    $ pip install extraetf-scraper

To import do 

    >>> from extraetf import etfs, stocks

Search for 100 stocks with highest performance last year and a marketcap > 10 billion EUR. 

    >>> response = stocks.search(sort_by="calculated_return_price_1y", ordering="desc", limit=100, filters={"ms_marketcap": {"gt": 10000000000}})

You can then show the top10 results like

    >>> for entry in response[:10]:
    ...     print(entry["year_1"], entry["isin"], entry["name"])
    ... 
    994.8275862 JP3236330001 Kioxia Holdings Corp
    513.3682831 US7731221062 Rocket Lab USA Inc
    495.1188986 US5017971046 L Brands Inc
    435.3982301 CNE100001T72 Yangtze Optical Fibre and Cable Joint Stock Ltd Co
    370.2093398 GB00B2QPKJ12 Fresnillo PLC
    321.0526316 JP3148800000 Ibiden Co Ltd
    306.25 US78392B1070 SK Hynix Inc
    297.1493729 US5951121038 Micron Technology Inc.
    283.9276323 IE00BKVD2N49 Seagate Technology Holdings PLC
    274.3169399 US82575P1075 Sibanye Stillwater Ltd (ADR)

You can show all possible sort options for ETFs like

    >>> etfs.show_sort_options()
    ['symbol', 'market_cap', 'return_year_to_date_real', 'ter', ...

Search for 500 ETFs with highest Sharpe ratio last year

    >>> response = etfs.search(sort_by="sharpe_ratio_1_year", ordering="desc", limit=500)
    >>> for entry in response[:10]:
    ...     print(entry["sharpe_1"], entry["year_1"], entry["isin"], entry["name"])
    ... 
    18.42 None LU1190417599 Amundi Smart Overnight Return UCITS ETF C-EUR
    18.37 None LU2082999306 Amundi Smart Overnight Return UCITS ETF D-EUR
    12.34 2.44698 LU2898088419 Ossiam Serenity Euro
    4.55 38.01092 LU1812092168 Amundi Stoxx Europe Select Dividend 30 UCITS ETF
    4.54 2.50162 IE00BD9MMF62 JPMorgan EUR Ultra-Short Income Active UCITS ETF (Acc)
    4.53 38.30012 DE0002635299 iShares STOXX Europe Select Dividend 30 UCITS ETF (DE)
    4.47 2.56119 IE00BCRY6557 iShares € Ultrashort Bond UCITS ETF (Dist)
    4.42 2.56116 IE000RHYOR04 iShares € Ultrashort Bond UCITS ETF (Acc)
    4.36 45.89505 LU0592216393 Xtrackers Spain UCITS ETF (Acc)
    4.36 45.93412 LU0994505336 Xtrackers Spain UCITS ETF (Dist)

For more examples have a look at the jupyter notebooks in the [notebooks](https://github.com/asmaier/extraetf/tree/main/notebooks) directory.
