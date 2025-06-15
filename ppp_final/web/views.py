# web/views.py

import os
import shutil
import subprocess

from django.conf import settings
from django.shortcuts import render
from .models import Evaluation

from pdf2image import convert_from_path  # pip install pdf2image

def convert_to_png(input_path):
    """
    .docx/.hwpx → PDF → 첫 페이지만 PNG로 변환,
    MEDIA_ROOT/reports/{basename}.png 반환.
    """
    soffice = shutil.which("soffice")
    if not soffice:
        return None

    base = os.path.splitext(os.path.basename(input_path))[0]
    out_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(out_dir, exist_ok=True)

    # 1) LibreOffice → PDF
    subprocess.run([
        soffice, "--headless",
        "--convert-to", "pdf",
        "--outdir", out_dir,
        input_path
    ], check=True)

    pdf_path = os.path.join(out_dir, f"{base}.pdf")
    png_path = os.path.join(out_dir, f"{base}.png")

    # 2) PDF → PNG (첫 페이지만)
    if not os.path.exists(png_path):
        pages = convert_from_path(pdf_path, first_page=1, last_page=1)
        pages[0].save(png_path, "PNG")

    # MEDIA_URL-relative path
    return f"reports/{base}.png"


def index(request):
    # 1) 학생 리스트 (35명)
    students = [
        {"order": i + 1, "name": name, "topic": topic}
        for i, (name, topic) in enumerate([
            ("강연우", "Tottenham Hotspur Football Club"),
            ("김건우", "FC Bayern Munich"),
            ("김민주", "Wolverhampton Wanderers Football Club"),
            ("김솔래", "Paris Saint-Germain Football Club"),
            ("김은주", "Fulham Football Club"),
            ("김재준", "Ulsan Hyundai Football Club"),
            ("김재혁", "Suwon Samsung Bluewings Football Club"),
            ("김한결", "VfL Wolfsburg Fußball GmbH"),
            ("노휘중", "Jeonbuk Hyundai Motors Football Club"),
            ("류원준", "Stade Brestois 29 Football Club"),
            ("민시윤", "Jeonbuk Hyundai Motors Football Club"),
            ("박시현", "FC Seoul"),
            ("박예원", "Shimizu S-Pulse"),
            ("박정연", "Shandong Taishan Football Club"),
            ("박지환", "Jeju United Football Club"),
            ("박채윤", "Suwon Samsung Bluewings Football Club"),
            ("박현", "Ulsan Hyundai Football Club"),
            ("박혜린", "Real Sociedad de Fútbol, S.A.D."),
            ("배은미", "FC Seoul"),
            ("배현찬", "Jeonbuk Hyundai Motors Football Club"),
            ("손유정", "Hannover 96 e.V."),
            ("송경찬", "Busan IPark Football Club"),
            ("안현", "Incheon United Football Club"),
            ("오찬희", "Suwon Samsung Bluewings Football Club"),
            ("이성학", "Dynamo Dresden e.V."),
            ("이용욱", "Pohang Steelers Football Club"),
            ("이원재", "Jeonbuk Hyundai Motors Football Club"),
            ("장은수", "Gwangju Football Club"),
            ("조지형", "FC Seoul"),
            ("주예린", "Gangwon Football Club"),
            ("주조양", "Daegu Football Club"),
            ("최인영", "Suwon Football Club"),
            ("황승재", "Bucheon FC 1995"),
            ("황지우", "Daejeon Hana Citizen Football Club"),
        ])
    ]

    # 2) 기존 평가 불러오기
    eval_dict = {e.order: e for e in Evaluation.objects.all()}

    # 3) POST 요청 처리 (별점, Best, GPT 토글)
    if request.method == 'POST':
        for row in students:
            order = row["order"]
            obj, _ = Evaluation.objects.get_or_create(
                order=order,
                defaults={"name": row["name"], "topic": row["topic"]}
            )
            val = request.POST.get(f"rating_{order}")
            if val is not None:
                r = int(val)
                obj.rating, obj.score = (0, "0") if obj.rating == r else (r, val)
            obj.best = request.POST.get(f"best_{order}") == "on"
            obj.suspected_gpt = request.POST.get(f"gpt_{order}") == "on"
            obj.name, obj.topic = row["name"], row["topic"]
            obj.save()
        eval_dict = {e.order: e for e in Evaluation.objects.all()}

    # 4) 원본 제출 파일 스캔 및 PNG 변환 매핑
    src_dir = os.path.join(settings.MEDIA_ROOT, "reports_src")
    report_map = {}
    if os.path.isdir(src_dir):
        for fname in os.listdir(src_dir):
            name, ext = os.path.splitext(fname)
            if ext.lower() not in (".docx", ".hwpx"):
                continue
            try:
                order = int(name)
            except ValueError:
                continue
            src_path = os.path.join(src_dir, fname)
            png = convert_to_png(src_path)
            if png:
                report_map[order] = png

    # 5) 템플릿용 students_page 구성
    students_page = []
    for row in students:
        order = row["order"]
        e = eval_dict.get(order)
        students_page.append({
            "order":  order,
            "name":   row["name"],
            "topic":  row["topic"],
            "rating": e.rating if e else 0,
            "score":  e.score if e else "",
            "best":   e.best if e else False,
            "gpt":    e.suspected_gpt if e else False,
            "report": report_map.get(order, ""),
        })

    # 6) Best 총개수 계산
    total_best = sum(1 for s in students_page if s["best"])

    # 7) 점수순 정렬 옵션
    sort_score = request.GET.get('sort_score') == '1'
    if sort_score:
        def key_fn(s):
            try:
                sc = int(s['score'])
            except:
                sc = 0
            return (0, -sc) if sc > 0 else (1, s['order'])
        students_page.sort(key=key_fn)

    # 8) 렌더링
    return render(request, "web/index.html", {
        "students_page": students_page,
        "total_best":    total_best,
        "MEDIA_URL":     settings.MEDIA_URL,
        "rating_range":  range(1, 6),
        "sort_score":    sort_score,
    })
