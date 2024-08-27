import ast
import time

# todo extra filter op vennootschapstype (bepaalde items worden geblacklist)
# those are in the enterprise.csv 
# omschrijving van de codes in code.csv


def filter_juridicalForm_and_juridicalSituation(file, ondernemingsset):
    with open(ondernemingsset) as o:
        ondernemingen = ast.literal_eval(o.read())
    
    #geen stopzetting of faillisement of dergelijke
    juridicalsituation_whitelist = {"000", "001", "002", "020", "090", "100"}
    # geen NV, ziekenfonds, overheid, ...
    juridicalForm_blacklist = {"014", "019", "017", "018", "020", "021", "025", "029", "040", "070", "117", "121", "123", 
                               "124", "125", "126", "127", "128", "129", "155", "160", "217", "218", "722", "723", "724"}
    juridicalForm_blacklist_ranges = [(301, 392), (400, 422)]

    for interval in juridicalForm_blacklist_ranges:
        juridicalForm_blacklist.update(map(str,range(interval[0], interval[1]+1)))

    onderneming_nummers = set()

    with open(file, encoding="utf8") as f:
        line = f.readline()
        while True:
            line = f.readline()
            if not line:
                print('eof')
                break
            values = line.strip().replace('"', '').split(',')
            
            if (values[2] in juridicalsituation_whitelist 
                and values[4] not in juridicalForm_blacklist 
                and values[0] in ondernemingen):
                onderneming_nummers.add(values[0])
            
    ond = open("ondernemingen.txt", 'w')
    ond.write(str(onderneming_nummers))
    ond.close()

    # if you want to do something later with this info save as separate file
    # with open(file, encoding="utf8") as f, open("filter_juridical.csv", "w") as csv_file:
    #     line = f.readline()
    #     csv_file.write(line)
    #     while True:
    #         line = f.readline()
    #         if not line:
    #             print('eof')
    #             break
    #         values = line.strip().replace('"', '').split(',')
            
    #         if values[2] in juridicalsituation_whitelist and values[4] not in juridicalForm_blacklist:
    #             csv_file.write(line)
            

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

    onderneming_nummers = set()
    vestiging_nummers = set()
    query = schilders.union(schrijnwerker).union(sanitair).union(elektricien).union(zonnepanelen).union(
        vloerverwarming).union(airco).union(dakwerken).union(stukadoor)
    with open(file) as f:
        while True:
            line = f.readline()
            if not line:
                print('eof')
                break
            values = line.strip().replace('"', '').split(',')

            if values[3] in query:  # and values[0][1:2] == '0':
                if values[0][0:1] == '0':
                    onderneming_nummers.add(values[0])
                else:
                    vestiging_nummers.add(values[0])

    ond = open("ondernemingen.txt", 'w')
    ond.write(str(onderneming_nummers))
    ond.close()

    vest = open("vestigingen.txt", "w")
    vest.write(str(vestiging_nummers))
    vest.close()

    # with open('filter_ondernemingen.csv', mode='w') as csv_file:
    #     line = '"ondernemingsnummer"\n'
    #     csv_file.write(line)
    #     for item in onderneming_nummers:
    #         csv_file.writelines('"' + item + '"\n')
    #
    # with open('filter_vestigingen.csv', mode='w') as csv_file:
    #     line = '"vestigingsnummer"\n'
    #     csv_file.write(line)
    #     for item in vestiging_nummers:
    #         csv_file.writelines('"' + item + '"\n')

    print("activity filtering done")

    return


def filter_zipcodes(file):
    postcodes_first_mailing = ["3980", "3580", "3945", "2430", "2431", "3290", "3293", "3294", "3560", "2440", "3970", "2450"]
    postcodes = ["3581", "3582", "3971",
                 "2200", "2250", "2400", "2490", "2260", "3545", "3550", "3500", "3501", "3510", "3511", "3512", 
                 "2280", "2288", "2560", "2270", "2240", "2242", "2243", "3540", "3390", "3391", "3270", "3271", 
                 "3272", "3460", "3461", "3200", "3201", "3202", "2230", "3520", "3530",
                 "3600", "3210", "3110", "3111", "3118", "3220", "3221", "3000", "3001", "3010", "3012", "3018"]

    with open(file, encoding="utf8") as f, open("filter_address.csv", "w") as csv_file:
        line = f.readline()
        csv_file.write(line)
        while True:
            line = f.readline()
            if not line:
                print('eof')
                break
            values = line.strip().replace('"', '').split(',')
            # postcode in de lijst, niet in het buitenland en adres niet geschrapt en straat ingevuld
            if values[4] in postcodes and values[2] == '' and values[12] == '' and values[7] != '':
                csv_file.write(line)


def combine_zip_activity_filter(adresfile, ondernemingsset):
    with open(ondernemingsset) as o:
        ondernemingen = ast.literal_eval(o.read())

    denomdict = get_denomination_dictionary("data/denomination.csv")

    with open(adresfile, encoding="ISO-8859-1") as a, \
            open("result_parsing.csv", "w", encoding="utf8") as output:

        line = a.readline()
        output.write('"Naam", ')
        output.write(line)
        while True:
            line = a.readline()
            if not line:
                print('eof')
                break
            values = line.strip().replace('"', '').split(',')
            if values[0] in ondernemingen:
                output.write('"' + denomdict[values[0]] + '", ')
                output.write(line)


def get_denomination_dictionary(denominationfile):
    # language 0 = indeterminate, 1 = FR, 2 = NL, taal klopt niet altijd
    # type 1 is naam voluit, 2 is afkorting, 3 ook afkorting
    # todo: aanpassen zodat NL prio heeft, dan indeterminate, en dan FR

    denomdict = {}
    with open(denominationfile, encoding="utf8") as d:
        while True:
            line = d.readline()
            if not line:
                print('eof')
                break
            values = line.strip().replace('"', '').split(',')
            # if values[1] in ["0", "2"]:
            denomdict[values[0]] = values[3]
    return denomdict


def main():
    # not needed again unless the activities change

    print("filter in the list of activities")
    filter_activities("data/activity.csv")

    print("filter adressen")
    filter_zipcodes("data/address.csv")

    print("filter ondernemingenlijst op vennootschapsvorm en juridische situatie")
    filter_juridicalForm_and_juridicalSituation("data/enterprise.csv", "ondernemingen.txt")

    print("combineer adresfilter met ondernemingelijst en voeg naam toe")
    combine_zip_activity_filter("filter_address.csv", "ondernemingen.txt")



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
