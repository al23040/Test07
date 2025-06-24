import requests
from bs4 import BeautifulSoup
import csv

url = "http://syllabus.sic.shibaura-it.ac.jp/syllabus/2023/MatrixL011.html"
response = requests.get(url)
response.encoding = "utf-8"  # 文字コードを指定
soup = BeautifulSoup(response.text, "html.parser")

# 科目行(tr.subject)を全部取得
subject_rows = soup.find_all("tr", class_="subject")

subjects = []
for tr in subject_rows:
    tds = tr.find_all("td")
    if len(tds) < 6:
        continue

    category = tds[0].get_text(strip=True)  # 科目区分
    subject_code = tds[2].get_text(strip=True)  # 科目コード
    subject_name = tds[3].get_text(strip=True)  # 科目名
    credit = tds[4].get_text(strip=True)  # 単位
    grade = tds[12].get_text(strip=True)  # 学年（13列目、index12）

    # 必要に応じて「requirement」や「term」も入れる（HTML構造に合わせて調整）
    # requirementは凡例の記号(◎, ○, △)が6〜9列目にあるかも

    # requirementの判定（6〜9列目のtdを調査してマークがあるところを判定例）
    requirement = None
    for i in range(5, 9):
        mark = tds[i].get_text(strip=True)
        if mark in ["◎", "○", "△", "□", "☆"]:
            requirement = mark
            break

    subjects.append({
        "category": category,
        "code": subject_code,
        "subject_name": subject_name,
        "credit": credit,
        "grade": grade,
        "requirement": requirement or ""
    })

# 結果表示（例）
for s in subjects[:5]:
    print(s)

with open('subjects.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['code', 'subject_name', 'category', 'requirement', 'credit'])
    writer.writeheader()  # ヘッダー行を書き込む

    for course in subjects:
        # 必要なキーだけ取り出して書き込む
        writer.writerow({
            'code': course['code'],
            'subject_name': course['subject_name'],
            'category': course['category'],
            'requirement': course['requirement'],
            'credit': course['credit']
        })

print("CSVファイルに書き出し完了しました。")
