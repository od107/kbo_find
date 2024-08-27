import pandas as pd


def main():
    panda = pd.read_csv('result_pandas.csv')
    #print(panda.iloc[:, 0])
    
    parse = pd.read_csv('result_parsing.csv')
    #print(parse.iloc[:, 1])

    prs_nrs = [word[2:-1] for word in parse.iloc[:, 1]]

    result = panda[~panda.iloc[:, 0].isin(prs_nrs)]
    result.to_csv('difference.csv')


if __name__ == "__main__":
    main()
