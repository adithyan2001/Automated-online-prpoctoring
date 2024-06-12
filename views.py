from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
import spApp.fd as fd
import spApp.final as final
# Create your views here.


def CommonHome(request):
    return render(request, 'CommonHome.html')


def SignIn(request):
    msg = ""
    st = ""
    request.session["mark"] = 0
    request.session['username'] = ""
    request.session['NAME'] = ""
    request.session['sid'] = ""
    request.session['cid'] = ""
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("Password")
        user = authenticate(username=email, password=password)
        request.session['username'] = email
        if user is not None:
            if user.is_superuser:
                return HttpResponseRedirect('/AdminHome/')
            elif user.is_staff:
                ds = Company.objects.get(email=email)
                request.session['id'] = ds.id
                return HttpResponseRedirect('/CompanyHome/')
            else:
                ds = Student.objects.get(email=email)
                request.session['id'] = ds.id
                data = Student.objects.values('name')
                print(data)
                return HttpResponseRedirect('/StudentHome/')
        else:
            msg = "Invalid username or password"
    return render(request, 'Signin.html', {"msg": msg})


def CompanySignup(request):
    msg = ""
    data = ""
    if request.POST:
        cname = request.POST.get("cname")
        location = request.POST.get("location")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        website = request.POST.get("website")
        about = request.POST.get("about")
        img = request.FILES["img"]
        Password = request.POST.get("Password")

        try:
            usr = User.objects.create_user(
                username=email, password=Password, is_active=0, is_staff=1)
            usr.save()
            col = Company.objects.create(name=cname, location=location, email=email,
                                         phone=phone, website=website, about=about, image=img, user=usr)
            col.save()
        except:
            msg = "Some Error Occured"
        else:
            msg = "Registartion Completed Successfully."
    return render(request, 'CompanySignup.html', {"msg": msg})


def StudentSignup(request):
    msg = ""
    data = ""

    if request.POST:
        sname = request.POST.get("sname")
        location = request.POST.get("location")
        qual = request.POST.get("qual")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        Password = request.POST.get("Password")

        try:
            usr = User.objects.create_user(
                username=email, password=Password, is_active=1, is_staff=0)
            usr.save()
            col = Student.objects.create(name=sname, location=location, email=email,
                                         phone=phone, qual=qual, adrs=address, user=usr)
            col.save()
        except:
            msg = "Some Error Occured"
        else:
            msg = "Registartion Completed Successfully."
    return render(request, 'StudentSignup.html', {"msg": msg, "data": data})


def AdminHome(request):
    return render(request, 'AdminHome.html')


def AdminViewCompany(request):
    data = Company.objects.all().order_by("-user__is_active")
    if 'search' in request.POST:
        search = request.POST['search']
        data = Company.objects.filter(Q(name__contains=search) | Q(location__contains=search) | Q(
            email__contains=search) | Q(phone__contains=search) | Q(about__contains=search))
    if request.GET:
        id = request.GET.get('id')
        st = request.GET.get('st')
        db = User.objects.get(id=id)
        if st == "Accept":
            db.is_active = 1
            db.save()
            return HttpResponseRedirect('/AdminViewCompany/')
        else:
            db.delete()
            return HttpResponseRedirect('/AdminViewCompany/')
    return render(request, "AdminViewCompany.html", {"data": data})


def AdminViewStudents(request):
    data = Student.objects.all().order_by("-id")
    if 'search' in request.POST:
        search = request.POST['search']
        data = Student.objects.filter(Q(name__contains=search) | Q(location__contains=search) | Q(
            email__contains=search) | Q(phone__contains=search) | Q(qual__contains=search))
    return render(request, "AdminViewStudents.html", {"data": data})


def AdminViewFeedback(request):
    data = ""

    data = Feedback.objects.all().order_by("-id")
    return render(request, "AdminViewFeedback.html", {"data": data})


def CompanyHome(request):
    return render(request, 'CompanyHome.html')


def CompanyPrepareQuestion(request):

    msg = ""
    subcategory = SubCat.objects.all()
    jid = request.GET['id']
    if request.POST:
        question = request.POST.get("question")
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")
        ans = request.POST.get("ans")

        sub = Job.objects.get(id=jid)
        db = Question.objects.create(
            question=question, o1=opt1, o2=opt2, o3=opt3, o4=opt4, ans=ans, job=sub)
        db.save()
        msg = "Questions added Successfully."
        # return HttpResponseRedirect('/CompanyPrepareQuestion/')
    return render(request, 'CompanyPrepareQuestion.html', {"msg": msg, "jid": jid})


def viewAllQuestions(request):
    id = request.GET['id']
    data = Question.objects.filter(job__id=id)
    if request.POST:
        search = request.POST['search']
        data = Question.objects.filter(job__subcat__id=search)

    sc = SubCat.objects.all()

    return render(request, "viewAllQuestions.html", {"data": data, "sc": sc, "cid": id})


def editQuestion(request):
    id = request.GET['id']
    cid = request.GET['cid']
    data = Question.objects.get(id=id)
    if request.POST:
        question = request.POST.get("question")
        opt1 = request.POST.get("opt1")
        opt2 = request.POST.get("opt2")
        opt3 = request.POST.get("opt3")
        opt4 = request.POST.get("opt4")
        ans = request.POST.get("ans")

        data.question = question
        data.o1 = opt1
        data.o2 = opt2
        data.o3 = opt3
        data.o4 = opt4
        data.ans = ans
        data.save()
        return redirect(f"/viewAllQuestions?id={cid}")

    return render(request, "editQuestion.html", {"data": data})


def CompanyViewJobcode(request):
    id = request.session["id"]
    data = ""
    data = Job.objects.filter(company__id=id)
    if request.POST:
        jcode = request.POST.get("jcode")
        request.session["jc"] = jcode
        return HttpResponseRedirect('/CompanyViewExamResult/')
    return render(request, "CompanyViewJobcode.html", {"data": data})


def CompanyViewExamResult(request):
    cid = request.session["cid"]
    jc = request.session["jc"]
    msg = ""
    data = Exam.objects.filter(job__id=jc).order_by("-id")
    print(data)
    return render(request, 'CompanyViewExamResult.html', {"data": data, "msg": msg})


def StudentHome(request):
    sid = request.session["id"]
    flag = False
    if request.POST:
        sname = request.POST.get("sname")
        location = request.POST.get("location")
        email = request.POST.get("email")
        qual = request.POST.get("qual")
        adrs = request.POST.get("adrs")
        phone = request.POST.get("phone")
        Password = request.POST.get("Password")

        db = Student.objects.get(id=sid)
        db.name = sname
        db.location = location
        db.qual = qual
        db.adrs = adrs
        db.phone = phone
        db.save()
        usr = User.objects.get(username=email)
        usr.set_password(Password)
        usr.save()
        msg = "Registration Completed Successfully."

    data = Student.objects.get(id=sid)
    return render(request, 'StudentHome.html', {"data": data, "flag": flag})


def StudentFindJob(request):
    data = ""

    data = Category.objects.all()
    if request.POST:
        job = request.POST.get("cat")
        request.session["jobcat"] = job
        return HttpResponseRedirect('/StudentViewJobs/')

    return render(request, 'StudentFindJob.html', {"data": data})


def StudentViewJobs(request):
    data = ""
    cat = request.session["jobcat"]

    data = SubCat.objects.filter(cat__id=cat)
    return render(request, 'StudentViewJobs.html', {"data": data})


def StudentViewCollege(request):
    subid = request.GET.get("id")
    data = Job.objects.filter(subcat__id=subid)
    return render(request, 'StudentViewCollege.html', {"data": data})


def StudentAttentAptitudeTest(request):
    id = request.session["id"]
    jid = request.GET.get("id")

    if Exam.objects.filter(job__id=jid, student__id=id).exists():
        return HttpResponseRedirect('/StudentViewJobs/')
    else:
        request.session["subid"] = jid
        da, daa = fetch_questions(jid)
        request.session["da"] = da
        request.session["daa"] = daa
        qus = Question.objects.filter(job__id=jid)
        # return HttpResponseRedirect('/StudentViewQuestions/')
    if request.POST:
        video = request.FILES['filename']
        correct = 0
        for q in qus:
            a = request.POST[f'ans{q.id}']
            ca = request.POST[f'cAns{q.id}']
            if a == ca:
                correct += 1
        stu = Student.objects.get(id=id)
        jo = Job.objects.get(id=jid)
        exam = Exam.objects.create(
            student=stu, job=jo, mark=correct, video=video)
        exam.save()
        return redirect(f"/eval?id={exam.id}")

    return render(request, "StudentAttentAptitudeTest.html", {"qus": qus, "da": da})


def eval(request):
    id = request.GET['id']
    ex = Exam.objects.get(id=id)
    from .head_pose_estimation import main
    res = main(f"C:/Users/User/Desktop/main project/SE/static/media/{ex.video}")
    ex.result = res
    from .person_and_phone import main
    res2 = main(f"C:/Users/User/Desktop/main project/SE/static/media/{ex.video}")
    ex.result2 = res2
    ex.save()
    return redirect("/StudentTest")


def fetch_questions(subid):
    aaa = Question.objects.filter(job__id=subid)
    da = [i.id for i in aaa]
    print(da)
    return da, da


def StudentViewQuestions(request):

    import cv2
    import numpy as np
    import math
    from .head_pose_estimation import head_pose_points, draw_annotation_box, get_2d_points
    from .face_detector import get_face_detector, find_faces
    from .face_landmarks import get_landmark_model, detect_marks
    subid = request.session['subid']
    id = request.session["id"]
    data = ""
    if request.POST:
        results = request.session['results']
        if request.POST.get("1") == request.session["ans"]:
            request.session["mark"] += 1
    else:
        results = []
    import random
    da = request.session["da"]
    daa = len(request.session['daa'])
    if len(da) > 0:
        rand_id = random.choice(da)
        data = Question.objects.get(id=rand_id)
        request.session["ans"] = data.ans
        da.remove(rand_id)
        face_model = get_face_detector()

        landmark_model = get_landmark_model()
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        size = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 3D model points.
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            # Right eye right corne
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])

        # Camera internals
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        while True:
            ret, img = cap.read()
            if ret == True:
                faces = find_faces(img, face_model)
                for face in faces:
                    marks = detect_marks(img, landmark_model, face)
                    # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
                    image_points = np.array([
                                            marks[30],     # Nose tip
                                            marks[8],     # Chin
                                            # Left eye left corner
                                            marks[36],
                                            # Right eye right corne
                                            marks[45],
                                            marks[48],     # Left Mouth corner
                                            marks[54]      # Right mouth corner
                                            ], dtype="double")
                    # Assuming no lens distortion
                    dist_coeffs = np.zeros((4, 1))
                    (success, rotation_vector, translation_vector) = cv2.solvePnP(
                        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

                    # Project a 3D point (0, 0, 1000.0) onto the image plane.
                    # We use this to draw a line sticking out of the nose

                    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array(
                        [(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

                    for p in image_points:
                        cv2.circle(
                            img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

                    p1 = (int(image_points[0][0]), int(image_points[0][1]))
                    p2 = (int(nose_end_point2D[0][0][0]),
                          int(nose_end_point2D[0][0][1]))
                    x1, x2 = head_pose_points(
                        img, rotation_vector, translation_vector, camera_matrix)

                    cv2.line(img, p1, p2, (0, 255, 255), 2)
                    cv2.line(img, tuple(x1), tuple(x2), (255, 255, 0), 2)
                    # for (x, y) in marks:
                    #     cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
                    # cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
                    try:
                        m = (p2[1] - p1[1])/(p2[0] - p1[0])
                        ang1 = int(math.degrees(math.atan(m)))
                    except:
                        ang1 = 90

                    try:
                        m = (x2[1] - x1[1])/(x2[0] - x1[0])
                        ang2 = int(math.degrees(math.atan(-1/m)))
                    except:
                        ang2 = 90

                        # print('div by zero error')
                    if ang1 >= 48:
                        print('Head down')
                        results.append('Head down')
                        cv2.putText(img, 'Head down', (30, 30),
                                    font, 2, (255, 255, 128), 3)
                    elif ang1 <= -48:
                        print('Head up')
                        results.append('Head up')
                        cv2.putText(img, 'Head up', (30, 30),
                                    font, 2, (255, 255, 128), 3)

                    if ang2 >= 48:
                        print('Head right')
                        results.append('Head right')
                        cv2.putText(img, 'Head right', (90, 30),
                                    font, 2, (255, 255, 128), 3)
                    elif ang2 <= -48:
                        print('Head left')
                        results.append('Head left')
                        cv2.putText(img, 'Head left', (90, 30),
                                    font, 2, (255, 255, 128), 3)
                    else:
                        request.session['results'] = results
                        return render(request, 'StudentViewQuestions.html', {"d": data})
                        # return render(request, 'StudentViewQuestions.html', {"d": data})
                        # return html_content

                    # cv2.putText(img, str(ang1), tuple(p1), font, 2, (128, 255, 255), 3)
                    # cv2.putText(img, str(ang2), tuple(x1), font, 2, (255, 255, 128), 3)
                # cv2.imshow('img', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
    else:
        mark = request.session["mark"]
        dr = Exam.objects.filter(job__id=subid, student__id=id).count()
        if dr == 0:
            stu = Student.objects.get(id=id)
            if Job.objects.filter(id=subid).exists():
                sub = Job.objects.get(id=subid)
                per = (int(mark) / daa) * 100
                forCut = per / 10
                results = request.session['results']
                hDown = 0
                hUp = 0
                hLeft = 0
                hRight = 0
                if results:
                    for result in results:
                        if result == 'Head down':
                            hDown += 1
                        elif result == 'Head up':
                            hUp += 1
                        elif result == 'Head left':
                            hLeft += 1
                        elif result == 'Head right':
                            hRight += 1
                fiRes = f"In the exam the candidate Head Downs {hDown} times, Head Up {hUp} times, Head Rights {hRight} times and Head Lefts {hLeft} times"
                db = Exam.objects.create(
                    job=sub, student=stu, mark=int(forCut), result=fiRes)
                db.save()

            return redirect('/StudentViewMarksAnswer/')


def stuQus(request):

    import threading

    async def function1():
        import cv2
        import numpy as np
        import math
        from .head_pose_estimation import head_pose_points, draw_annotation_box, get_2d_points
        from .face_detector import get_face_detector, find_faces
        from .face_landmarks import get_landmark_model, detect_marks
        face_model = get_face_detector()

        landmark_model = get_landmark_model()
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        size = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 3D model points.
        model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            # Right eye right corne
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])

        # Camera internals
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        results = []
        while True:
            ret, img = cap.read()
            if ret == True:
                faces = find_faces(img, face_model)
                for face in faces:
                    marks = detect_marks(img, landmark_model, face)
                    # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
                    image_points = np.array([
                                            marks[30],     # Nose tip
                                            marks[8],     # Chin
                                            # Left eye left corner
                                            marks[36],
                                            # Right eye right corne
                                            marks[45],
                                            marks[48],     # Left Mouth corner
                                            marks[54]      # Right mouth corner
                                            ], dtype="double")
                    # Assuming no lens distortion
                    dist_coeffs = np.zeros((4, 1))
                    (success, rotation_vector, translation_vector) = cv2.solvePnP(
                        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

                    # Project a 3D point (0, 0, 1000.0) onto the image plane.
                    # We use this to draw a line sticking out of the nose

                    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array(
                        [(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

                    for p in image_points:
                        cv2.circle(
                            img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

                    p1 = (int(image_points[0][0]), int(image_points[0][1]))
                    p2 = (int(nose_end_point2D[0][0][0]),
                          int(nose_end_point2D[0][0][1]))
                    x1, x2 = head_pose_points(
                        img, rotation_vector, translation_vector, camera_matrix)

                    cv2.line(img, p1, p2, (0, 255, 255), 2)
                    cv2.line(img, tuple(x1), tuple(x2), (255, 255, 0), 2)
                    # for (x, y) in marks:
                    #     cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
                    # cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
                    try:
                        m = (p2[1] - p1[1])/(p2[0] - p1[0])
                        ang1 = int(math.degrees(math.atan(m)))
                    except:
                        ang1 = 90

                    try:
                        m = (x2[1] - x1[1])/(x2[0] - x1[0])
                        ang2 = int(math.degrees(math.atan(-1/m)))
                    except:
                        ang2 = 90

                        # print('div by zero error')
                    if ang1 >= 48:
                        print('Head down')
                        results.append('Head down')
                        cv2.putText(img, 'Head down', (30, 30),
                                    font, 2, (255, 255, 128), 3)
                    elif ang1 <= -48:
                        print('Head up')
                        results.append('Head up')
                        cv2.putText(img, 'Head up', (30, 30),
                                    font, 2, (255, 255, 128), 3)

                    if ang2 >= 48:
                        print('Head right')
                        results.append('Head right')
                        cv2.putText(img, 'Head right', (90, 30),
                                    font, 2, (255, 255, 128), 3)
                    elif ang2 <= -48:
                        print('Head left')
                        results.append('Head left')
                        cv2.putText(img, 'Head left', (90, 30),
                                    font, 2, (255, 255, 128), 3)

                    # cv2.putText(img, str(ang1), tuple(p1), font, 2, (128, 255, 255), 3)
                    # cv2.putText(img, str(ang2), tuple(x1), font, 2, (255, 255, 128), 3)
                # cv2.imshow('img', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
    # code for function 1

    async def function2():
        subid = request.session['subid']
        id = request.session["id"]
        data = ""
        if request.POST:
            if request.POST.get("1") == request.session["ans"]:
                request.session["mark"] += 1
        else:
            results = []
        import random
        da = request.session["da"]
        daa = len(request.session['daa'])
        if len(da) > 0:
            rand_id = random.choice(da)
            data = Question.objects.get(id=rand_id)
            request.session["ans"] = data.ans
            da.remove(rand_id)

            return render(request, 'StudentViewQuestions.html', {"d": data})
        else:
            mark = request.session["mark"]
            dr = Exam.objects.filter(subcat__id=subid, student__id=id).count()
            if dr == 0:
                stu = Student.objects.get(id=id)
                if SubCat.objects.filter(id=subid).exists():
                    sub = SubCat.objects.get(id=subid)
                    per = (int(mark) / daa) * 100
                    forCut = per / 10
                    db = Exam.objects.create(
                        subcat=sub, student=stu, mark=int(forCut))
                    db.save()
            return redirect('/StudentViewMarksAnswer/')

    # code for function 2
    import asyncio

    async def main():
        f1 = loop.create_task(function1())
        f2 = loop.create_task(function2())
        await asyncio.wait([f1, f2])

    # to run the above function we'll
    # use Event Loops these are low level
    # functions to run async functions
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # wait for threads to finish


def StudentViewMarksAnswer(request):
    subid = request.session['subid']
    sid = request.session["id"]
    mark = 0
    if Exam.objects.filter(job__id=subid, student__id=sid).exists():
        ans = Exam.objects.get(job__id=subid, student__id=sid)
        mark = ans.mark
        result = ans.result
    return render(request, 'StudentViewMarksAnswer.html', {"mark": mark, "result": result})


def CustomerAddFeedback(request):
    msg = ""
    cid = request.session['id']
    if request.POST:
        a = request.POST.get("room")
        usr = Student.objects.get(id=cid)
        db = Feedback.objects.create(student=usr, feedback=a)
        db.save()
        msg = "Feedback Added Successfully."
    return render(request, "CustomerAddFeedback.html", {"msg": msg})


def AdminCategory(request):

    msg = ""
    if request.POST:
        cat = request.POST.get("room")
        if Category.objects.filter(name=cat).exists():
            msg = "Already Exists."
        else:
            db = Category.objects.create(name=cat)
            db.save()
            msg = "Category added Successfully."

    data = Category.objects.all().order_by("-id")
    return render(request, 'AdminCategory.html', {"msg": msg, "data": data})


def AdminSubcategory(request):

    msg = ""
    if request.POST:
        subcat = request.POST.get("room")
        cat = request.POST.get("cat")
        c = Category.objects.get(id=cat)
        if SubCat.objects.filter(name=subcat, cat=c).exists():
            msg = "Already Exists."
        else:
            db = SubCat.objects.create(name=subcat, cat=c)
            db.save()
            msg = "Subcategory added Successfully."
    subcategory = Category.objects.all()
    data = SubCat.objects.all().order_by("-id")
    return render(request, 'AdminSubcategory.html', {"msg": msg, "category": subcategory, "data": data})


def CollegeCourse(request):
    id = request.session['id']
    msg = ""
    if request.POST:
        subcat = request.POST.get("cat")
        cat = request.POST.get("room")
        desc = request.POST.get("desc")
        col = Company.objects.get(id=id)
        sub = SubCat.objects.get(id=subcat)
        db = Job.objects.create(company=col, subcat=sub, cutoff=cat, desc=desc)
        db.save()
        msg = "Job added Successfully."
    subcategory = SubCat.objects.all()
    data = Job.objects.filter(company__id=id)

    return render(request, 'CollegeCourse.html', {"msg": msg, "category": subcategory, "data": data})


def StudentTest(request):
    id = request.session["id"]
    msg = ""
    data = Exam.objects.filter(student__id=id)
    print(data)
    return render(request, 'StudentTest.html', {"data": data, "msg": msg})


def StudentPossibleCollege(request):
    subid = request.GET.get("id")
    mark = request.GET.get("mark")
    data = Job.objects.filter(subcat__id=subid, cutoff__lte=mark)
    return render(request, 'StudentPossibleCollege.html', {"data": data, "subid": subid})
