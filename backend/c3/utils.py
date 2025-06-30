from .models import Subject, Registration, get_session

def text_replace(text: str):
    text = text.replace("Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉ", "Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉｎｇ　")
    text = text.replace("Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅ", "Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅａｋｉｎｇ　")
    text = text.replace("＜数理基礎科目＞", "")
    text = text.replace("コンピュータアーキテクチャ", "コンピュータアーキテクチャ ")
    text = text.replace("データ構造とアルゴリズム１", "データ構造とアルゴリズム１ ")
    text = text.replace("データ構造とアルゴリズム2", "データ構造とアルゴリズム2 ")

    return text

def get_course(code):
    session = get_session()
    course = session.query(Subject).filter_by(code=code).first()
    if course:
        session.close()
        return {
            "subject_name": course.subject_name,
            "code": course.code,
            "category": course.category,
            "requirement": course.requirement,
            "credit": course.credit
        }

    return None

def make_send_courses(courses: list):
    send_courses = []
    for course in courses:
        course_data = get_course(course["code"])
        if course_data is not None:
            send_courses.append(course_data)

    return send_courses

def make_send_available_courses(semester_offered: int, year_offered: int, send_courses: list):
    base_year = 2023
    limit_grade = year_offered - base_year + 1
    limit_semester = semester_offered
    print(limit_grade, limit_semester)

    taken_codes = set(course["code"] for course in send_courses)

    session = get_session()
    all_courses = session.query(Subject).all()

    send_available_courses = []
    for course in all_courses:
        if course.code in taken_codes:
            continue

        course_grade = int(course.year_offered)
        course_semester = int(course.semester_offered)
        course_order = (course_grade, course_semester)
        limit_order = (limit_grade, limit_semester)

        if course_order <= limit_order:
            send_available_courses.append({
                "subject_name": course.subject_name,
                "code": course.code,
                "category": course.category,
                "requirement": course.requirement,
                "credit": course.credit
            })

    return send_available_courses

def make_send_credits_data(send_courses):
    university_common_credits = 0
    informatics_credits = 0

    common_math_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    language_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    social_sciences_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    major_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    pe_health_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    common_engineering_credits = {
        "compulsory": 0,
        "elective_compulsory": 0,
        "elective": 0
    }

    for course in send_courses:
        category = course["category"]
        requirement = course["requirement"]
        credit = int(course["credit"])  # 必ずintとして扱う

        if category == "全学共通科目":
            university_common_credits += credit

        elif category == "共通数理科目":
            if requirement == "必修":
                common_math_credits["compulsory"] += credit
            elif requirement == "選択必修":
                common_math_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                common_math_credits["elective"] += credit

        elif category == "言語科目":
            if requirement == "必修":
                language_credits["compulsory"] += credit
            elif requirement == "選択必修":
                language_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                language_credits["elective"] += credit

        elif category == "人文社会系教養科目":
            if requirement == "必修":
                social_sciences_credits["compulsory"] += credit
            elif requirement == "選択必修":
                social_sciences_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                social_sciences_credits["elective"] += credit

        elif category == "専門科目":
            if requirement == "必修":
                major_credits["compulsory"] += credit
            elif requirement == "選択必修":
                major_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                major_credits["elective"] += credit

        elif category == "体育健康科目":
            if requirement == "必修":
                pe_health_credits["compulsory"] += credit
            elif requirement == "選択必修":
                pe_health_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                pe_health_credits["elective"] += credit

        elif category == "共通工学系教養科目":
            if requirement == "必修":
                pe_health_credits["compulsory"] += credit
            elif requirement == "選択必修":
                pe_health_credits["elective_compulsory"] += credit
            elif requirement == "選択":
                pe_health_credits["elective"] += credit

        elif category == "情報科目":
            informatics_credits += credit

    return {
        "university_common_credits": university_common_credits,
        "common_math_credits": common_math_credits,
        "language_credits": language_credits,
        "social_sciences_credits": social_sciences_credits,
        "major_credits": major_credits,
        "informatics_credits": informatics_credits,
        "PE_health_credits": pe_health_credits,
        "common_engineering_credits": common_engineering_credits
    }