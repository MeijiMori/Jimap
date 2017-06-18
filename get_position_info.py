#!
# -*- coding: utf-8 -*-

import re

def get_place_candidate(search_place):
    # DATA DIR
    DATA_DIR = "./jimapn_data"
    # PREFECTURES CODE
    PREFECTURES_CODE = {
            1  : unicode('北海道',  "utf-8"),
            2  : unicode('青森県',  "utf-8"),
            3  : unicode('岩手県',  "utf-8"),
            4  : unicode('宮城県',  "utf-8"),
            5  : unicode('秋田県',  "utf-8"),
            6  : unicode('山形県',  "utf-8"),
            7  : unicode('福島県',  "utf-8"),
            8  : unicode('茨城県',  "utf-8"),
            9  : unicode('栃木県',  "utf-8"),
            10 : unicode('群馬県',  "utf-8"),
            11 : unicode('埼玉県',  "utf-8"),
            12 : unicode('千葉県',  "utf-8"),
            13 : unicode('東京都',  "utf-8"),
            14 : unicode('神奈川県',"utf-8"),
            15 : unicode('新潟県',  "utf-8"),
            16 : unicode('富山県',  "utf-8"),
            17 : unicode('石川県',  "utf-8"),
            18 : unicode('福井県',  "utf-8"),
            19 : unicode('山梨県',  "utf-8"),
            20 : unicode('長野県',  "utf-8"),
            21 : unicode('岐阜県',  "utf-8"),
            22 : unicode('静岡県',  "utf-8"),
            23 : unicode('愛知県',  "utf-8"),
            24 : unicode('三重県',  "utf-8"),
            25 : unicode('滋賀県',  "utf-8"),
            26 : unicode('京都府',  "utf-8"),
            27 : unicode('大阪府',  "utf-8"),
            28 : unicode('兵庫県',  "utf-8"),
            29 : unicode('奈良県',  "utf-8"),
            30 : unicode('和歌山県',"utf-8"),
            31 : unicode('鳥取県',  "utf-8"),
            32 : unicode('島根県',  "utf-8"),
            33 : unicode('岡山県',  "utf-8"),
            34 : unicode('広島県',  "utf-8"),
            35 : unicode('山口県',  "utf-8"),
            36 : unicode('徳島県',  "utf-8"),
            37 : unicode('香川県',  "utf-8"),
            38 : unicode('愛媛県',  "utf-8"),
            39 : unicode('高知県',  "utf-8"),
            40 : unicode('福岡県',  "utf-8"),
            41 : unicode('佐賀県',  "utf-8"),
            42 : unicode('長崎県',  "utf-8"),
            43 : unicode('熊本県',  "utf-8"),
            44 : unicode('大分県',  "utf-8"),
            45 : unicode('宮崎県',  "utf-8"),
            46 : unicode('鹿児島県',"utf-8"),
            47 : unicode('沖縄県',  "utf-8"),
            }

    # search
    m = re.search(u"(.*[県府都道])", search_place)

    if m:
        #print "match"
        #print "search_place : {0}".format(search_place)
        #print search_place
        #print m.group(0)
        #print len(PREFECTURES_CODE)
        code = 0
        for i in xrange(len(PREFECTURES_CODE)):
            if PREFECTURES_CODE[i + 1] == m.group(0):
                print i + 1
                code = i + 1
                break
            else:
                #print "NONE"
                pass

        if code == 0:
            print "Prefectures code is Not Found ..."
        data_dir = DATA_DIR + "/" + "position_info"
        data_file = data_dir + "/" + "{0:02}000-09.0b".format(code) + "/" \
                + "{0:02}_2015.csv".format(code)
        print "read file : {0}".format(data_file)
        candidate = []
        with open(data_file, "r") as df:
            file_line = df.readline()
            count = 0
            while file_line != "":
                #print file_line
                line = re.split(r"(,)", file_line)
                #print line
                #x = 0
                #for l in line:
                #    print x, l
                #    x += 1
                tmp_place_name = line[2] + line[6] + line[10]
                tmp_latitude = line[12]
                tmp_longitude = line[14]
                #print tmp_place_name
                #print tmp_latitude
                #print tmp_longitude
                p = re.compile(r"(\")")
                place_name = p.sub("",tmp_place_name)
                latitude = p.sub("", tmp_latitude)
                longitude = p.sub("", tmp_longitude)
                #print "place_name : {0}".format(place_name)
                #print "latitude : {0}".format(latitude)
                #print "longitude : {0}".format(longitude)
                #print "print : {0}".format(search_place)
                # position csv file's encode is shift-jis
                match = re.match(search_place.encode('shift-jis'), place_name)
                if match:
                    candidate.append(count)
                    candidate[count] = {
                            "place_name" : place_name,
                            "latitude" : latitude,
                            "longitude" : longitude,
                            }
                    count += 1
                else:
                    #print "place name none match"
                    pass

                file_line = df.readline()
        #print "candidate >>> "
        for i in xrange(len(candidate)):
            #print "place_name : {0}".format(candidate[i]["place_name"])
            #print "latitude : {0}".format(candidate[i]["latitude"])
            #print "longitude : {0}".format(candidate[i]["longitude"])
            pass

        return candidate
    else:
        print "None match"
        return None

if __name__ == '__main__':
    #search_place = unicode("愛媛県松山市", "utf-8")
    #search_place = unicode("東京都品川"  , "utf-8")
    #search_place = unicode("北海道札幌市", "utf-8")
    #search_place = unicode("京都府"      , "utf-8")
    search_place = unicode("香川県善通寺市上吉田町", "utf-8")
    cand = get_place_candidate(search_place)
    for i in xrange(len(cand)):
        print "place_name : {0}".format(cand[i]["place_name"])
        print "latitude : {0}".format(cand[i]["latitude"])
        print "longitude : {0}".format(cand[i]["longitude"])

