import pandas as pd


def main():
    panda = pd.read_csv('result_pandas.csv')
    print(panda.iloc[:, 0])
    pd_nrs = panda.iloc[:, 0]
    
    parse = pd.read_csv('result_parsing.csv')
    print(parse.iloc[:, 1])
    prs_nrs = parse.iloc[:, 1]

    prs_nrs = [word[2:-1] for word in parse.iloc[:, 1]]
    print(prs_nrs)

    result = panda[~panda.iloc[:, 0].isin(prs_nrs)]
    result.to_csv('difference.csv')
    
    #todo
    


    # df = panda.iloc[:, 0]]

    # print(parse['"EntityNumber"'].head())

    # df=panda[~panda.columns[0].isin(parse[:, 1])]
    #.dropna(how = 'all')

    # df.to_csv('difference.csv')

if __name__ == "__main__":
    main()
