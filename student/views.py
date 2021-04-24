from datetime import datetime, timezone, timedelta

from django.shortcuts import render, redirect

from student import models


# Create your views here.
def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def to_index(request):
    return render(request, 'index.html')


# 学生登陆
def student_login(request):
    if request.method == 'POST':
        stu_id = request.POST.get('id')
        password = request.POST.get('password')
        print("id", stu_id, "password", password)

        student = models.Student.objects.get(id=stu_id)
        print(student)
        if password == student.password:
            paper = models.Paper.objects.filter(major=student.major)
            grade = models.Grade.objects.filter(sid=student.id)

            return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})

        else:
            return render(request, 'index.html', {'message': '密码不正确'})


# 教师登陆
def teacher_login(request):
    if request.method == 'POST':
        tea_id = request.POST.get('id')
        password = request.POST.get('password')

        teacher = models.Teacher.objects.get(id=tea_id)
        print(teacher)
        if password == teacher.password:
            paper = models.Paper.objects.filter(tid=teacher.id)

            return render(request, 'teacher.html', {'teacher': teacher, 'paper': paper})

        else:
            return render(request, 'index.html', {'message': '密码不正确'})


# 教师查看成绩
def show_grade(request):
    subject1 = request.GET.get('subject')
    grade = models.Grade.objects.filter(subject=subject1)

    data1 = models.Grade.objects.filter(subject=subject1, grade__lt=60).count()
    data2 = models.Grade.objects.filter(subject=subject1, grade__gte=60, grade__lt=70).count()
    data3 = models.Grade.objects.filter(subject=subject1, grade__gte=70, grade__lt=80).count()
    data4 = models.Grade.objects.filter(subject=subject1, grade__gte=80, grade__lt=90).count()
    data5 = models.Grade.objects.filter(subject=subject1, grade__gte=90).count()

    data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}

    return render(request, 'show_grade.html', {'grade': grade, 'data': data, 'subject': subject1})


def query_student(request):
    sid = request.GET.get('id')
    sex = request.GET.get('sex')
    subject = request.GET.get('subject')

    tid = request.GET.get('tid')
    teacher = models.Teacher.objects.get(id=tid)
    paper = models.Paper.objects.filter(tid=teacher.id)

    from django.db import connection
    cursor = connection.cursor()
    sql = """select * from grade,student where student.id=grade.sid_id 
                and student.id like %s and grade.subject like %s and student.sex like %s and '1'='1'"""
    val = ('%' + sid + '%', '%' + subject + '%', '%' + sex + '%')
    cursor.execute(sql, val)
    result = dict_fetch_all(cursor)

    return render(request, 'teacher.html', {'teacher': teacher, 'result': result, 'paper': paper})


# tuple => dict
def dict_fetch_all(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# 考试
def start_exam(request):
    sid = request.GET.get('sid')
    subject1 = request.GET.get('subject')

    student = models.Student.objects.get(id=sid)
    paper = models.Paper.objects.filter(subject=subject1)
    count = models.Paper.objects.get(subject=subject1).pid.all().count()

    start_time = models.Paper.objects.get(subject=subject1).exam_time.astimezone(timezone(timedelta(hours=8)))
    duration = models.Paper.objects.get(subject=subject1).duration
    deadline = start_time + duration
    print(datetime.now())
    now = datetime.now().replace(microsecond=0).astimezone(timezone(timedelta(hours=8)))

    countdown = deadline - now
    if deadline < now:
        countdown = 0
    passphrase = models.Paper.objects.get(subject=subject1).passphrase
    if passphrase is not None and request.POST.get('phrase') != passphrase:
        paper = models.Paper.objects.filter(major=student.major)
        grade = models.Grade.objects.filter(sid=student.id)
        return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade, 'message': '口令不正确'})

    return render(request, 'exam.html',
                  {'student': student, 'paper': paper, 'subject': subject1, 'count': count, 'countdown': countdown})


# 计算成绩
def cal_grade(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')

        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(major=student.major)
        grade = models.Grade.objects.filter(sid=student.id)

        # 时间有效性判断
        start_time = models.Paper.objects.get(subject=subject1).exam_time.astimezone(timezone(timedelta(hours=8)))
        duration = models.Paper.objects.get(subject=subject1).duration
        now = datetime.now().astimezone(timezone(timedelta(hours=8)))
        if now - start_time > duration:
            return render(request, 'index.html',
                          {'student': student, 'paper': paper, 'grade': grade, 'message': '考试已结束'})

        question = models.Paper.objects.filter(subject=subject1).values("pid").values('pid__id', 'pid__answer',
                                                                                      'pid__score')

        my_grade = 0
        all_grade = 0
        for p in question:
            q_id = str(p['pid__id'])
            true_ans = p['pid__answer']

            if len(true_ans) == 1:
                my_ans = request.POST.get(q_id)
                if true_ans == my_ans:
                    my_grade += p['pid__score']
            elif len(true_ans) > 1:
                # $(qid)A $(qid)B $(qid)C $(qid)D
                my_ans = """"""
                if request.POST.get(q_id + "A") is not None:
                    my_ans += "A"
                if request.POST.get(q_id + "B") is not None:
                    my_ans += "B"
                if request.POST.get(q_id + "C") is not None:
                    my_ans += "C"
                if request.POST.get(q_id + "D") is not None:
                    my_ans += "D"
                if my_ans == true_ans:
                    my_grade += p['pid__score']

            all_grade += p['pid__score']

        models.Grade.objects.create(sid_id=sid, subject=subject1, grade=my_grade, all_grade=all_grade)

        return render(request, 'index.html',
                      {'student': student, 'paper': paper, 'grade': grade, 'all_grade': all_grade})

    elif request.method == 'GET':
        sid = request.GET.get('sid')
        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(major=student.major)
        grade = models.Grade.objects.filter(sid=student.id)

        return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})


def log_out(request):
    return redirect('/login/')
