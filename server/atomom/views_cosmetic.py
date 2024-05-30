from django.shortcuts import render, redirect
from django.http import JsonResponse
import pymysql
import json
import random

def cosmetic(request):
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

    file_path = 'json_files/test_jay.json'
    with open(file_path, 'r', encoding='utf-8') as json_file:
        # JSON 데이터 파싱
        parsed_data = json.load(json_file)

        # 첫 번째 데이터에서 ':' 이후의 내용 제거하여 출력
        first_data = parsed_data['originaltext'].split(':')[0]  # ':' 이전 부분만 선택
        print(first_data)
        try:
            with connection.cursor() as cursor:
                # 첫 번째 데이터가 'atopy'인 경우에만 goodForOily 컬럼의 값을 가져오는 쿼리 실행
                if first_data == 'atopy':
                    sql = """
                        SELECT pr.product_id, p.*
                        FROM (
                                SELECT i.id AS ingredients_id
                                FROM atomom_ingredients i
                                WHERE i.goodForOily = 1
                                LIMIT 5
                             ) 
                            AS atomom_ingredients
                            JOIN atomom_pirelation pr ON atomom_ingredients.ingredients_id = pr.ingredients_id
                            JOIN atomom_product p ON pr.product_id = p.id
                            LIMIT 7;
                    """
                    cursor.execute(sql)

                    # 결과 가져오기
                    results = cursor.fetchall()

        finally:
            # 연결 닫기
            connection.close()
    
    # 세션에서 이전에 선택된 레코드를 가져옴
    previous_record_id = request.session.get('previous_record_id')
    
    # 새로운 레코드 선택
    new_record = None
    while True:
        new_record = random.choice(results) if results else None
        # 이전에 선택된 레코드와 다른 경우 반복 종료
        if new_record['id'] != previous_record_id:
            break
    
    # 새로운 레코드를 세션에 저장
    request.session['previous_record_id'] = new_record['id'] if new_record else None
    
    context = {
        'first_data': first_data,
        'record': new_record,
    }
    return render(request, 'cosmetic.html', context)
