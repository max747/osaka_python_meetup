import csv
import json
import os
import sys
import unicodedata


def read_zipcodecsv_as_dict(filename):
    with open(filename, encoding="cp932") as csvfile:
        """
            郵便番号データファイルの形式
            http://www.post.japanpost.jp/zipcode/dl/readme.html

            0. 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
            1. （旧）郵便番号（5桁）………………………………………　半角数字
            2. 郵便番号（7桁）………………………………………　半角数字
            3. 都道府県名　…………　半角カタカナ（コード順に掲載）　（注1）
            4. 市区町村名　…………　半角カタカナ（コード順に掲載）　（注1）
            5. 町域名　………………　半角カタカナ（五十音順に掲載）　（注1）
            6. 都道府県名　…………　漢字（コード順に掲載）　（注1,2）
            7. 市区町村名　…………　漢字（コード順に掲載）　（注1,2）
            8. 町域名　………………　漢字（五十音順に掲載）　（注1,2）
            9. 一町域が二以上の郵便番号で表される場合の表示　（注3）　（「1」は該当、「0」は該当せず）
            10. 小字毎に番地が起番されている町域の表示　（注4）　（「1」は該当、「0」は該当せず）
            11. 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
            12. 一つの郵便番号で二以上の町域を表す場合の表示　（注5）　（「1」は該当、「0」は該当せず）
            13. 更新の表示（注6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
            14. 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、
                「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
        """
        reader = csv.reader(csvfile)
        dicts = []
        # 半角カナを全角に置き換える処理
        normalize = lambda s: unicodedata.normalize("NFKC", s)

        for row in reader:
            dicts.append({
                "zipcode": row[2],
                "pref_kana": normalize(row[3]),
                "city_kana": normalize(row[4]),
                "street_kana": normalize(row[5]),
                "pref_name": row[6],
                "city_name": row[7],
                "street_name": row[8],
            })

        return dicts


def main():
    latest_dir = os.path.join("download", "latest")

    csvfiles = [name for name in os.listdir(latest_dir) if name.lower().endswith(".csv")]
    if len(csvfiles) == 0:
        print("no csv file in a specified directory: {}".format(latest_dir))
        sys.exit(1)
    if len(csvfiles) > 1:
        print("cannot specify csv file: more than one csv file found")
        sys.exit(1)

    csvfile = os.path.join(latest_dir, csvfiles[0])
    d = read_zipcodecsv_as_dict(csvfile)
    print(json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
