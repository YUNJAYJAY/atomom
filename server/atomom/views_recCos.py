# from django.shortcuts import render
# import pymysql
# import json


# def recCos(request):
#     # # MySQL 서버 연결 정보
#     # host = 'localhost'
#     # user = 'root'
#     # password = '20121208'
#     # database = 'atodb'

#     # # MySQL 서버 연결
#     # connection = pymysql.connect(host=host,
#     #                             user=user,
#     #                             password=password,
#     #                             database=database,
#     #                             cursorclass=pymysql.cursors.DictCursor)

#     file_path = 'json_files/test_jay.json'
#     with open(file_path, 'r', encoding='utf-8') as json_file:
#         # JSON 데이터 파싱
#         parsed_data = json.load(json_file)

#         # 첫 번째 데이터에서 ':' 이후의 내용 제거하여 출력
#         first_data = parsed_data['originaltext'].split(':')[0]  # ':' 이전 부분만 선택
#         print(first_data)
#         # try:
#         #     with connection.cursor() as cursor:
#         #         # 첫 번째 데이터가 'atopy'인 경우에만 goodForOily 컬럼의 값을 가져오는 쿼리 실행
#         #         if first_data == 'atopy':
#         #             sql = "SELECT id, korean, english, goodForOily FROM atomom_ingredients WHERE goodForOily = 1;"
#         #             cursor.execute(sql)

#         #             # 결과 가져오기
#         #             oily_records = cursor.fetchall()

#         #             # 결과 출력 또는 필요한 작업 수행
#         #             for record in oily_records:
#         #                 print(record)  # 추려낸 레코드 출력
#         #         else:
#         #             print("첫 번째 데이터가 'atopy'가 아닙니다.")

#         # finally:
#         #     # 연결 닫기
#             # connection.close()
#     context = {
#         'first_data' : first_data,
#         # 'oily_records' : oily_records,
#         # 'record' : record
#     }
#     return render(request, 'recCos.html', context)

# 수정 전 코드 

# views.py
from django.shortcuts import render
import json

def recCos(request):
    name_no_ext = request.session.get('name_no_ext', 'default_value')
    file_path = f'json_files/{name_no_ext}.json'
    with open(file_path, 'r', encoding='utf-8') as json_file:
        # JSON 데이터 파싱
        parsed_data = json.load(json_file)
        
    first_data = parsed_data['originaltext'].split(':')[0]  # ':' 이전 부분만 선택

    context = {
        'name_no_ext' : name_no_ext,
        'first_data' : first_data,
    }
    return render(request, 'recCos.html', context)
