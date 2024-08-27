# pandas version of the script
# to learn pandas and compare performance


import pandas as pd
import time

# todo extra filter op vennootschapstype (bepaalde items worden geblacklist)
# those are in the enterprise.csv 
# omschrijving van de codes in code.csv


def filter_activities(file):
    schilders = {"43341", "43342", "4334", "4334101", "4334201", "3109111", "31099", "31092"}
    schrijnwerker = {"4332", "43320", "16291", "16100", "43332", "16240", "47522", "16210", "162", "161", "1610",
                     "1624", "433201", "4759901", "1621", "161001", "1624002", "1629102", "1629106", "1624001",
                     "1624003", "1629103", "4332004", "4332005", "1629", "1629101", "4332002", "432003", "1629104",
                     "1629105", "4332001", "16230"}
    sanitair = {"23420", "47527", "2342", "1722", "17220", "4673", "25991", "2342001", "2223004", "4322101", "28140",
                "43221", "22230"}
    elektricien = {"43211", "33200", "2651004", "7112101", "2732001", "27320", "43222", "275", "38213", "27110",
                   "27402", "25930", "2651", "27900", "26510"}
    zonnepanelen = {"47540"} #, "35110"}
    vloerverwarming = {"4322", "4322202", "43222", "27520", "33110"}
    airco = {"28250", "2825003", "4322201", "4329", "432"}
    dakwerken = {"43910", "43999", "4391001", "4399101", "43991", "43291"}
    carrossier = {"52290"}
    auto_onderhoud = {"45203", "45201", "7120907", "451", "4730002", "4778802", "4511", "4520301", "4520101", "4532001",
                      "45402", "45320"}
    stukadoor = {"43310"}

    query = schilders.union(schrijnwerker).union(sanitair).union(elektricien).union(zonnepanelen).union(
        vloerverwarming).union(airco).union(dakwerken).union(stukadoor)

    df = pd.read_csv(file)
    #    EntityNumber  ActivityGroup  NaceVersion  NaceCode Classification
    # 0  0200.065.765              6         2008     84130           MAIN

    df1 = df[df['NaceCode'].isin([int(i) for i in query])]
    df2 = df1[df1['EntityNumber'].str.startswith('0')]
   
    ondernemingen = df2['EntityNumber'].drop_duplicates()
    ondernemingen.to_csv('ondernemingen.csv', index=False)

    print("activity filtering done")
    print(f'Number of records: {len(ondernemingen)}')
    # 163153 vs 154074 originally

    return


def filter_zipcodes(file):
    postcodes_first_mailing = ["3980", "3580", "3945", "2430", "2431", "3290", "3293", "3294", "3560", "2440", "3970", "2450"]
    postcodes = ["3581", "3582", "3971",
                 "2200", "2250", "2400", "2490", "2260", "3545", "3550", "3500", "3501", "3510", "3511", "3512", 
                 "2280", "2288", "2560", "2270", "2240", "2242", "2243", "3540", "3390", "3391", "3270", "3271", 
                 "3272", "3460", "3461", "3200", "3201", "3202", "2230", "3520", "3530",
                 "3600", "3210", "3110", "3111", "3118", "3220", "3221", "3000", "3001", "3010", "3012", "3018"]

    df = pd.read_csv(file,  dtype='object')
    #    EntityNumber TypeOfAddress CountryNL CountryFR Zipcode       MunicipalityNL       MunicipalityFR        StreetNL        StreetFR HouseNumber  Box ExtraAddressInfo DateStrikingOff
    # 0  0200.065.765          REGO       NaN       NaN    9070         Destelbergen         Destelbergen   Panhuisstraat   Panhuisstraat           1  NaN              NaN             NaN
    
    # postcode in de lijst, niet in het buitenland en adres niet geschrapt en straat ingevuld
    df = df[df['Zipcode'].isin(postcodes)]
    df = df[df['CountryNL'].isnull()]
    df = df[df['DateStrikingOff'].isnull() & df['StreetNL'].notnull()]
    df.to_csv('filter_address.csv', index=False)

    print("zipcodes filtered")
    print(f'Number of records: {len(df.index)}')
    # 161541 vs 161499 originally

def filter_juridicalForm_and_juridicalSituation(file, ondernemingsset):
    
    #geen stopzetting of faillisement of dergelijke
    juridicalsituation_whitelist = {"000", "001", "002", "020", "090", "100"}
    # geen NV, ziekenfonds, overheid, ...
    juridicalForm_blacklist = {"014", "019", "017", "018", "020", "021", "025", "029", "040", "070", "117", "121", "123", 
                               "124", "125", "126", "127", "128", "129", "155", "160", "217", "218", "722", "723", "724"}
    juridicalForm_blacklist_ranges = [(301, 392), (400, 422)]

    for interval in juridicalForm_blacklist_ranges:
        juridicalForm_blacklist.update(map(str,range(interval[0], interval[1]+1)))


    ond = pd.read_csv(ondernemingsset, index_col=0)
    #ond.set_index('EntityNumber')
    #    EntityNumber
    #0  0206.848.639
    # print("ond")
    # print(ond.head())

    jur = pd.read_csv(file, index_col=0)
    #   EnterpriseNumber Status  JuridicalSituation  TypeOfEnterprise  JuridicalForm  JuridicalFormCAC   StartDate
    #0     0200.065.765     AC                   0                 2          416.0               NaN  09-08-1960
    jur = jur[jur['JuridicalSituation'].isin(int(i) for i in juridicalsituation_whitelist)]
    jur = jur[~jur['JuridicalForm'].isin(int(i) for i in juridicalForm_blacklist)]
    #jur.set_index('EnterpriseNumber')

    #jur = pd.merge(ond, jur, how='inner', left_on = 'EntityNumber', right_on='EnterpriseNumber')
    # print("jur")
    # print(jur.head())
   # jur.to_csv('juridical.csv', index=False)

   


    # with open(file, encoding="utf8") as f:
    #     line = f.readline()
    #     while True:
    #         line = f.readline()
    #         if not line:
    #             print('eof')
    #             break
    #         values = line.strip().replace('"', '').split(',')
            
    #         if (values[2] in juridicalsituation_whitelist 
    #             and values[4] not in juridicalForm_blacklist 
    #             and values[0] in ondernemingen):
    #             onderneming_nummers.add(values[0])
            
    # ond = open("ondernemingen.txt", 'w')
    # ond.write(str(onderneming_nummers))
    # ond.close()


    #denomdict = get_denomination_dictionary("data/denomination.csv")

    denom = pd.read_csv('data/denomination.csv', index_col=0)
    denom = denom[denom['Language'].isin([0, 2]) & denom['TypeOfDenomination'] == 1]
    #todo For some reason some TypeOfDenomination = 3 are still included
    
    #denom.set_index('EntityNumber')
    # print("denom")
    # print(denom.head())
    #EntityNumber  Language  TypeOfDenomination                          Denomination
#0  0200.065.765         2                   1  Intergemeentelijke Vereniging Veneco

    adr = pd.read_csv('filter_address.csv', index_col=0)
    #adr.set_index('EntityNumber')
    # print("adr")
    # print(adr.head())


    df1 = pd.merge(ond, jur, how = 'inner', left_index=True, right_index=True)
    df2 = pd.merge(denom, adr, how = 'inner', left_index=True, right_index=True)
    result = pd.merge(df1, df2, how = 'inner', left_index=True, right_index=True)
    result.to_csv('result_pandas.csv')
  


    # with open(adresfile, encoding="ISO-8859-1") as a, \
    #         open("doublefilter_address.csv", "w", encoding="utf8") as output:

    #     line = a.readline()
    #     output.write('"Naam", ')
    #     output.write(line)
    #     while True:
    #         line = a.readline()
    #         if not line:
    #             print('eof')
    #             break
    #         values = line.strip().replace('"', '').split(',')
    #         if values[0] in ondernemingen:
    #             output.write('"' + denomdict[values[0]] + '", ')
    #             output.write(line)



def main():

    print("filter in the list of activities")
    filter_activities("data/activity.csv")

    print("filter adressen")
    filter_zipcodes("data/address.csv")

    print("filter ondernemingenlijst op vennootschapsvorm en juridische situatie")
    print("combineer adresfilter met ondernemingelijst en voeg naam toe")
    filter_juridicalForm_and_juridicalSituation("data/enterprise.csv", "ondernemingen.csv")



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

