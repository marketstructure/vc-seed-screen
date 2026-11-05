#!/usr/bin/env python3
"""Comparable-company data puller for vc-seed-screen.

Pulls revenue, growth, margin, and valuation multiples for listed companies
using yfinance (US/global) or akshare (China A-shares / HK).

Usage:
    python3 comps.py --ticker MDB --source yfinance
    python3 comps.py --symbol 600519 --source akshare
    python3 comps.py --ticker SNOW,AAPL,MSFT --source yfinance
"""

import argparse
import json
import sys


def pull_yfinance(tickers):
    """Pull key financials from yfinance for one or more tickers."""
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance not installed. Install with: pip install yfinance"}

    results = []
    for ticker in tickers:
        t = yf.Ticker(ticker)
        info = t.info
        results.append({
            "ticker": ticker,
            "company": info.get("longName", "?"),
            "market_cap": info.get("marketCap", None),
            "total_revenue": info.get("totalRevenue", None),
            "gross_margin": info.get("grossMargins", None),
            "revenue_growth": info.get("revenueGrowth", None),
            "price_to_sales": info.get("priceToSalesTrailing12Months", None),
            "enterprise_to_revenue": info.get("enterpriseToRevenue", None),
            "currency": info.get("currency", "?"),
            "source": "yfinance",
        })
    return results


def pull_akshare(symbols):
    """Pull financial abstracts from akshare for China A-share / HK stocks."""
    try:
        import akshare as ak
    except ImportError:
        return {"error": "akshare not installed. Install with: pip install akshare"}

    results = []
    for symbol in symbols:
        try:
            df = ak.stock_financial_abstract(symbol=symbol)
            # Extract the most recent period row
            latest = df.iloc[0].to_dict() if len(df) > 0 else {}
            results.append({
                "symbol": symbol,
                "data": {str(k): str(v) for k, v in latest.items()},
                "source": "akshare",
            })
        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e),
                "source": "akshare",
            })
    return results


def main():
    parser = argparse.ArgumentParser(description="Pull comparable company financials")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticker", help="yfinance ticker(s), comma-separated (e.g. MDB,SNOW)")
    group.add_argument("--symbol", help="akshare symbol(s), comma-separated (e.g. 600519)")
    parser.add_argument("--source", choices=["yfinance", "akshare"], required=True,
                        help="Data source to use")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.source == "yfinance":
        tickers = [t.strip() for t in args.ticker.split(",")]
        result = pull_yfinance(tickers)
    else:
        symbols = [s.strip() for s in args.symbol.split(",")]
        result = pull_akshare(symbols)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if isinstance(result, dict) and "error" in result:
            print(result["error"], file=sys.stderr)
            sys.exit(1)
        for item in result:
            if "error" in item:
                print(f"  {item.get('ticker', item.get('symbol', '?'))}: ERROR — {item['error']}")
                continue
            if item["source"] == "yfinance":
                print(f"  {item['company']} ({item['ticker']})")
                print(f"    Market cap:  {item.get('market_cap', '?')}")
                print(f"    Revenue:     {item.get('total_revenue', '?')}")
                print(f"    Gross margin:{item.get('gross_margin', '?')}")
                print(f"    Rev growth:  {item.get('revenue_growth', '?')}")
                print(f"    P/S:         {item.get('price_to_sales', '?')}")
                print(f"    EV/Rev:      {item.get('enterprise_to_revenue', '?')}")
                print(f"    Currency:    {item.get('currency', '?')}")
                print(f"    [yfinance]")
            else:
                print(f"  {item['symbol']} [akshare]")
                for k, v in item.get("data", {}).items():
                    print(f"    {k}: {v}")
            print()


if __name__ == "__main__":
    main()
