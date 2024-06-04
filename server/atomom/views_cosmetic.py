# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# import pymysql
# import json
# import random

# def cosmetic(request):
#     # MySQL 서버 연결 정보
#     host = 'localhost'
#     user = 'root'
#     password = '20121208'
#     database = 'atodb'
#     # MySQL 서버 연결
#     connection = pymysql.connect(host=host,
#                                 user=user,
#                                 password=password,
#                                 database=database,
#                                 cursorclass=pymysql.cursors.DictCursor)

#     file_path = 'json_files/test_jay.json'
#     with open(file_path, 'r', encoding='utf-8') as json_file:
#         # JSON 데이터 파싱
#         parsed_data = json.load(json_file)

#         # 첫 번째 데이터에서 ':' 이후의 내용 제거하여 출력
#         first_data = parsed_data['originaltext'].split(':')[0]  # ':' 이전 부분만 선택
#         print(first_data)
#         try:
#             with connection.cursor() as cursor:
#                 # 첫 번째 데이터가 'atopy'인 경우에만 goodForOily 컬럼의 값을 가져오는 쿼리 실행
#                 if first_data == 'atopy':
#                     sql = """
#                         SELECT pr.product_id, p.*
#                         FROM (
#                                 SELECT i.id AS ingredients_id
#                                 FROM atomom_ingredients i
#                                 WHERE i.goodForOily = 1
#                                 LIMIT 5
#                              ) 
#                             AS atomom_ingredients
#                             JOIN atomom_pirelation pr ON atomom_ingredients.ingredients_id = pr.ingredients_id
#                             JOIN atomom_product p ON pr.product_id = p.id
#                             LIMIT 7;
#                     """
#                     cursor.execute(sql)

#                     # 결과 가져오기
#                     results = cursor.fetchall()

#         finally:
#             # 연결 닫기
#             connection.close()
    
#     # 세션에서 이전에 선택된 레코드를 가져옴
#     previous_record_id = request.session.get('previous_record_id')
    
#     # 새로운 레코드 선택
#     new_record = None
#     while True:
#         new_record = random.choice(results) if results else None
#         # 이전에 선택된 레코드와 다른 경우 반복 종료
#         if new_record['id'] != previous_record_id:
#             break
    
#     # 새로운 레코드를 세션에 저장
#     request.session['previous_record_id'] = new_record['id'] if new_record else None
    
#     context = {
#         'first_data': first_data,
#         'record': new_record,
#     }
#     return render(request, 'cosmetic.html', context)


# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql
import os

def cosmetic(request):
    skin_type = request.GET.get('skin_type', 'oily')

    # MySQL 서버 연결 정보
    host = 'localhost'
    user = 'root'
    password = '20121208'
    database = 'atodb'

    # MySQL 서버 연결
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 피부 유형에 따라 SQL 쿼리 작성
            if skin_type == 'oily':
                sql = """
                SELECT p.id, p.brand, p.name
                FROM atomom_ingredients i
                JOIN atomom_pirelation pr ON i.id = pr.ingredients_id
                JOIN atomom_pcrelation pc ON pr.product_id = pc.product_id
                JOIN atomom_product p ON pc.product_id = p.id
                WHERE i.goodForOily = 1
                AND i.badForOily = 0
                AND pc.medium_id = 1
                AND i.hazardScoreMax IN (1, 2, 3)
                AND i.allergy = 0
                # ORDER BY RAND()
                LIMIT 5

                """
            elif skin_type == 'dry':
                sql = """
                SELECT p.id, p.brand, p.name, p.subName
                FROM atomom_ingredients i
                JOIN atomom_pirelation pr ON i.id = pr.ingredients_id
                JOIN atomom_pcrelation pc ON pr.product_id = pc.product_id
                JOIN atomom_product p ON pc.product_id = p.id
                WHERE i.goodForDry = 1
                AND i.badForDry = 0
                AND pc.medium_id = 1
                AND i.hazardScoreMax IN (1, 2, 3)
                AND i.allergy = 0
                # ORDER BY RAND()
                LIMIT 5
                """
            elif skin_type == 'sensitive':
                sql = """
                SELECT p.id, p.brand, p.name, p.subName
                FROM atomom_ingredients i
                JOIN atomom_pirelation pr ON i.id = pr.ingredients_id
                JOIN atomom_pcrelation pc ON pr.product_id = pc.product_id
                JOIN atomom_product p ON pc.product_id = p.id
                WHERE i.goodForSensitive = 1
                AND i.badForSensitive = 0
                AND pc.medium_id = 1
                AND i.hazardScoreMax IN (1, 2, 3)
                AND i.allergy = 0
                # ORDER BY RAND()
                LIMIT 5
                """
            else:
                return HttpResponse("Invalid skin type selected.")

            cursor.execute(sql)
            results = cursor.fetchall()

    finally:
        # 연결 닫기
        connection.close()
    
    static_dir = 'static/cosmetic'
    for result in results:
        product_image_name = f"{result['name']}.png"
        image_path = os.path.join(static_dir, product_image_name)
        if os.path.exists(image_path):
            result['image_url'] = f"/static/cosmetic/{product_image_name}"
        else:
            result['image_url'] = '/static/cosmetic/default.png'  # 이미지가 없을 경우 기본 이미지
        
    context = {
        'results': results,
        'skin_type': skin_type,
    }
    return render(request, 'cosmetic.html', context)
