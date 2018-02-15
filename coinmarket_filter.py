#!/usr/bin/env python2

"""
Program to retrieve a list of coins (along with info like - price_usd &
circulating supply) from `coinmarketcap.com` optionally filtered based
on criteria.
A `coins.csv` file will be generated in the working directory which can be
imported in Excel for further analysis.

Note: API source: https://coinmarketcap.com/api/

Sample commands for execution

1. `python coinmarket_filter.py`

2. `python coinmarket_filter.py -h` (help on options)

3. `python coinmarket_filter.py --ge-price 5000`

4. `python coinmarket_filter.py --le-price 0.05 --ge-circulating-supply 6700000000`

"""

import argparse
import json
import sys
import urllib2
import csv


def get_coins(le_price, ge_price, le_circulating_supply, ge_circulating_supply):

    response = urllib2.urlopen(
        'https://api.coinmarketcap.com/v1/ticker/?limit=0'
    )
    all_coin_data = json.load(response)

    with open('coins.csv', 'wb') as coin_file:
        csv_writer = csv.writer(coin_file, delimiter=',')
        csv_writer.writerow(['Name', 'Price (USD)', 'Circulating Supply'])

        for coin_data in all_coin_data:
            price = coin_data['price_usd']
            if price:
                price = float(price)
            circulating_supply = coin_data['available_supply']
            if circulating_supply:
                circulating_supply = float(circulating_supply)

            if le_price and price > le_price:
                continue
            elif ge_price and price < ge_price:
                continue

            if (le_circulating_supply and
                circulating_supply > le_circulating_supply):
                continue
            elif (ge_circulating_supply and
                  circulating_supply < ge_circulating_supply):
                continue

            csv_writer.writerow([coin_data['name'], price, circulating_supply])

    print("DONE!!! Generated a \"coins.csv\" file")


def main():
    parser = argparse.ArgumentParser(
        description='Criteria based filtering of coins from coinmarketcap.com'
    )
    parser.add_argument(
        '--le-price',
        help='Less than equal to price (US $)',
        type=float,
        dest='le_price'
    )
    parser.add_argument(
        '--ge-price',
        help='Greater than equal to price (US $)',
        type=float,
        dest='ge_price'
    )
    parser.add_argument(
        '--le-circulating-supply',
        help='Less than equal to circulating supply',
        type=float,
        dest='le_circulating_supply'
    )
    parser.add_argument(
        '--ge-circulating-supply',
        help='Greater than equal to circulating supply',
        type=float,
        dest='ge_circulating_supply'
    )

    args = parser.parse_args()

    if args.le_price and args.ge_price:
        sys.exit(
            "Not allowed to specify both the following options together: "
            "--le-price and --ge-price"
        )
    elif args.le_circulating_supply and args.ge_circulating_supply:
        sys.exit(
            "Not allowed to specify both the following options together: "
            "--le-circulating-supply and --ge-circulating-supply"
        )
    else:
        get_coins(args.le_price,
                  args.ge_price,
                  args.le_circulating_supply,
                  args.ge_circulating_supply)


if __name__ == '__main__':
    main()
