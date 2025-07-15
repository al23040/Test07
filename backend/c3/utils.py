from .models import Subject, Registration, AvailableCourse,get_session, subject


def text_replace(text: str):
    text = text.replace("Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉ", "Ｒｅａｄｉｎｇ＆Ｗｒｉｔｉｎｇ　")
    text = text.replace("Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅ", "Ｌｉｓｔｅｎｉｎｇ＆Ｓｐｅａｋｉｎｇ　")
    text = text.replace("＜数理基礎科目＞", "")
    text = text.replace("コンピュータアーキテクチャ", "コンピュータアーキテクチャ ")
    text = text.replace("データ構造とアルゴリズム１", "データ構造とアルゴリズム１ ")
    text = text.replace("データ構造とアルゴリズム2", "データ構造とアルゴリズム2 ")
    text = text.replace("バスケットボール（テクニカ", "バスケットボール（テクニカル） ")
    text = text.replace("バスケットボール（スポーツ", "バスケットボール（スポーツコミュニケーション） ")
    text = text.replace("スキー（スポーツコミュニケ", "スキー（スポーツコミュニケーション） ")
    text = text.replace("テニス（スポーツコミュニケ", "テニス（スポーツコミュニケーション） ")
    text = text.replace("ソフトボール（テクニカル）", "ソフトボール（テクニカル） ")
    text = text.replace("ソフトボール（スポーツコミ", "ソフトボール（スポーツコミュニケーション） ")
    text = text.replace("バレーボール（テクニカル）", "バレーボール（テクニカル） ")
    text = text.replace("バレーボール（スポーツコミ", "バレーボール（スポーツコミュニケーション） ")
    text = text.replace("バドミントン（テクニカル）", "バドミントン（テクニカル） ")
    text = text.replace("バドミントン（スポーツコミ", "バドミントン（スポーツコミュニケーション） ")
    text = text.replace("卓球（スポーツコミュニケー", "卓球（スポーツコミュニケーション） ")
    text = text.replace("サッカー（スポーツコミュニ", "サッカー（スポーツコミュニケーション） ")
    text = text.replace("フットサル（スポーツコミュ", "フットサル（スポーツコミュニケーション） ")
    text = text.replace("フラッグフットボール（テク", "フラッグフットボール（テクニカル） ")
    text = text.replace("フラッグフットボール（スポ", "フラッグフットボール（スポーツコミュニケーション） ")
    text = text.replace("軟式野球（スポーツコミュニ", "軟式野球（スポーツコミュニケーション） ")
    text = text.replace("ウェルネス・スポーツ（テク", "ウェルネス・スポーツ（テクニカル） ")
    text = text.replace("ウェルネス・スポーツ（スポ", "ウェルネス・スポーツ（スポーツコミュニケーション） ")

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
            "credit": course.credit,
            "semester": course.semester_offered,
            "year": course.year_offered,
        }

    return None

def get_completed_courses(user_id):
    completed_courses = []
    session = get_session()
    courses = session.query(Registration).filter_by(user_id=user_id).all()
    session.close()
    for course in courses:
        details = get_course(course.code)
        completed_course = {
            "subject_name": details["subject_name"],
            "code": details["code"],
            "grade": None,
            "category": details["category"],
            "requirement": details["requirement"],
            "credit": details["credit"],
            "semester": details["semester"],
            "year": details["year"],
            "time_slot": None,
            "day_of_week": None,
            "prerequisites": None
        }
        completed_courses.append(completed_course)

    return completed_courses

def get_all_courses(user_id):
    all_courses = []
    session = get_session()
    # completed_courses = session.query(Registration.code).filter_by(user_id=user_id).all()
    # completed_codes = [row.code for row in completed_courses]
    # cources = session.query(Subject).filter(~Subject.code.in_(completed_codes)).all()
    courses = session.query(Subject).all()
    session.close()
    for course in courses:
        all_course = {
            "subject_name": course.subject_name,
            "code": course.code,
            "grade": None,
            "category": course.category,
            "requirement": course.requirement,
            "credit": course.credit,
            "semester": course.semester_offered,
            "year": course.year_offered,
            "time_slot": None,
            "day_of_week": None,
            "prerequisites": None

        }
        all_courses.append(all_course)

    return all_courses

def get_available_courses(user_id):
    available_courses = []
    session = get_session()
    courses = session.query(AvailableCourse).filter_by(user_id=user_id).all()
    session.close()
    for course in courses:
        available_course = {
            "subject_name": course.subject_name,
            "code": course.code,
            "grade": None,
            "category": course.category,
            "requirement": course.requirement,
            "credit": course.credit,
            "semester": course.semester_offered,
            "year": course.year_offered,
            "time_slot": None,
            "day_of_week": None,
            "prerequisites": None
        }
        available_courses.append(available_course)
    return available_courses

def submit_available_courses(user_id, semester_offered: int, year_offered: int):
    if semester_offered == 1:
        next_year = year_offered
        next_semester = 2
    elif semester_offered == 2:
        next_year = year_offered + 1
        next_semester = 1
    else:
        raise ValueError("semester_offered must be 1 (前期) or 2 (後期)")

    session = get_session()
    courses = session.query(Subject).all()
    available_courses = []
    for course in courses:
        if int(course.year_offered) == next_year and int(course.semester_offered) == next_semester:
            available_courses.append(course)

    session.query(AvailableCourse).filter_by(user_id=user_id).delete()
    for course in available_courses:
        new_entry = AvailableCourse(
            user_id=user_id,
            code=course.code,
            subject_name=course.subject_name,
            category=course.category,
            requirement=course.requirement,
            credit=course.credit,
            semester_offered=course.semester_offered,
            year_offered=course.year_offered
        )
        session.add(new_entry)

    session.commit()






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