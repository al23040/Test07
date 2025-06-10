def text_replace(text: str) -> text:
    text = text.replace("Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉ", "Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉｎｇ　")
    text = text.replace("Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅ", "Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅａｋｉｎｇ　")
    text = text.replace("＜数理基礎科目＞", "")
    text = text.replace("コンピュータアーキテクチャ", "コンピュータアーキテクチャ ")
    text = text.replace("データ構造とアルゴリズム１", "データ構造とアルゴリズム１ ")
    text = text.replace("データ構造とアルゴリズム2", "データ構造とアルゴリズム2 ")

    return text

def make_send_data(courses: list)