 from tradingview_screener.query import Query


def main():


    query = Query()
    count, df = query.get_scanner_data()
    print(f"Results count: {count}")
    print(df)


    
if __name__ == "__main__":
    main()
