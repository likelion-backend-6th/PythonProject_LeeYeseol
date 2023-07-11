import psycopg2
from psycopg2 import sql
import os

# db 설정
conn = psycopg2.connect(
    host='localhost',
    dbname='library',
    user='yes',
    password='pass'
)
cur = conn.cursor()


# console 삭제
def clear():
    os.system('cls')


# 데이터 입력 기능
def data_input():
    while True:
        print('--------------------------------------')
        print('---------------도서 입력 ---------------')
        print('--------------------------------------')
        id = int(input('도서ID를 입력하세요: '))
        book_title = input('도서명을 입력하세요: ')
        book_author = input('저자를 입력하세요: ')
        book_publisher = input('출판사 정보를 입력하세요: ')
        book_is_available = input('도서 상태를 입력하세요 (0: 대출중/1: 대출가능)')

        cur.execute("""INSERT INTO books (book_id, title, author, publisher, is_available) VALUES (%s,%s,%s,%s,%s);""",
                    (id, book_title, book_author, book_publisher, book_is_available))
        conn.commit()

        print('데이터베이스 저장 성공')
        choice = input('계속 입력 하시겠습니까? (Y/N): ')
        if choice == 'N':
            break


### 도서 정보 조회 기능
def book_search():
    while True:
        print('-------------도서 정보 조회 서브메뉴------------')
        print('1. 전체 도서 테이블 표기')
        print('2. id나 title로 도서 정보 조회')
        print('3. 메인 메뉴로 나가기')
        select = input('사용자 선택: ')

        if select == '1':
            print('--------------------------------------')
            print('------------도서 정보 조회 -------------')
            print('--------------------------------------')
            print('| 도서ID |    도서명    |  저자  |  출판사 |  도서 상태  | ')
            cur.execute('''SELECT * FROM books ORDER BY book_id;''')
            rows = cur.fetchall()
            for row in rows:
                if row[4] == True:
                    print('|   ' + str(row[0]) + '   |  ' + str(row[1]) + '  |  ', str(row[2]) +
                          '  |  ' + str(row[3]) + '  |  ' + '대출 가능' + '  | ')
                else:
                    print('|   ' + str(row[0]) + '   |  ' + str(row[1]) + '  |  ', str(row[2]), '  |  ' + str(row[3])
                          + '  |  ' + '대출 불가능' + '  |')
            print('======= 도서 정보 조회 완료 =======\n')

        elif select == '2':
            while True:
                clear()
                print('--------------------------------------')
                print('------------도서 정보 조회 -------------')
                print('--------------------------------------')
                id = str(input("찾고자 하는 book id나 title을 입력하세요: \n"))

                print('| 도서ID |    도서명    |  저자  |  출판사 |  도서 상태  | ')

                # string input => title 로 검색
                if id.isnumeric():
                    cur.execute('''SELECT * FROM books WHERE book_id = %s;''', id)
                # book id 로 검색
                else:
                    cur.execute('''SELECT * FROM books WHERE title = %s;''', id)

                rows = cur.fetchall()

                for row in rows:
                    if row[4] == True:
                        print('|   ' + str(row[0]) + '   |  ' + str(row[1]) + '  |  ', str(row[2]) +
                              '  |  ' + str(row[3]) + '  |  ' + '대출 가능' + '  | ')
                    else:
                        print('|   ' + str(row[0]) + '   |  ' + str(row[1]) + '  |  ', str(row[2]),
                              '  |  ' + str(row[3])
                              + '  |  ' + '대출 불가능' + '  | ')

                        print('--------------------------------------')
                        print('---------- 해당 도서 대출 정보 ---------')
                        print('--------------------------------------')
                        print('| 대출ID |  회원ID  |  이름  | 도서ID |   도서명   |  대출 일자 |  반납 일자  | \n')

                        # 도서가 대출 중인 상태인 경우, 도서의 대출 정보를 함께 출력합니다
                        cur.execute('''SELECT * FROM loans WHERE book_id = %s;''', str(row[0]))
                        loans_info = cur.fetchall()

                        for loan in loans_info:
                            print('|   ' + str(loan[0]) + '   |   ' + str(loan[1]) + '   |   ' + str(loan[2]) +
                                  '  |  ' + str(loan[3]) + '   |   ' + str(loan[4]) + '   |   ' + loan[5].strftime(
                                '%Y-%m-%d')
                                  + '  |  ' + str(loan[6]) + '  | ')

                print(' ==========도서 조회 완료========== ')
                choice = input('계속 조회 하시겠습니까? (Y/N): ')
                if choice == 'N':
                    break
        elif select == '3':
            break
        else:
            print('잘못된 메뉴입니다\n')
            pass


# ### 3. 도서 대출 기능
def book_loan(*args):
    while True:
        clear()
        id = str(input("대출 하고자 하는 book id나 title을 입력하세요: \n"))
        # book id 로 검색
        if id.isnumeric():
            cur.execute('''SELECT * FROM books WHERE book_id = %s;''', id)
        # string input => title 로 검색
        else:
            cur.execute('''SELECT * FROM books WHERE title = %s;''', id)
        rows = cur.fetchall()

        # 대출이 이미 되어있는 경우
        if rows[0][4] == False:
            print('대출이 불가합니다.')

        # 대출 가능할 때 대출 진행
        else:
            # loan id 생성
            # 새로 입력된 책 id를 기존 loans 테이블 마지막 id보다 1크게 만들기
            try:
                cur.execute('''SELECT loan_id FROM loans ORDER BY loan_id;''')
                loan_book_ids = cur.fetchall()
                last_loan_book_ids = loan_book_ids[-1][0] + 1

            # 기존 id가 없는 경우 1로 시작
            except IndexError:
                last_loan_book_ids = 1

            # loan_date ==> 현재 날짜
            cur.execute(""" SELECT Now()::Date;""")
            input_date = cur.fetchall()
            l_date = input_date[0][0]

            # 입력받은 user_id를 토대로 user_name 찾기
            cur.execute('''SELECT user_name FROM users WHERE user_id = %s;''', args)
            name = cur.fetchall()
            # loan table에 대출정보 저장하기
            cur.execute(
                """INSERT INTO loans (loan_id, user_id, user_name, book_id, title, loan_date, return_date) VALUES (
                %s,%s,%s,%s,%s,%s,NULL);""",
                (int(last_loan_book_ids), int(args[0]), name[0][0], int(rows[0][0]), rows[0][1], l_date))

            # books 테이블에 대출 불가능으로 바꾸기
            cur.execute('''UPDATE books SET is_available = FALSE WHERE book_id= %s''', id)
            conn.commit()

        print('==========도서 대출 완료==========')

        choice = input('계속 도서 대출을 진행하시겠습니까? (Y/N): ')
        if choice == 'N':
            break


# 도서 반납 기능
def return_book():
    while True:
        clear()
        print('--------------------------------------')
        print('------------도서 반납 메뉴 -------------')
        print('--------------------------------------')

        id = str(input("반납을 원하는 book id나 title을 입력하세요: \n"))

        # 반납한 날짜
        cur.execute(""" SELECT Now()::Date;""")
        input_date = cur.fetchall()
        r_date = input_date[0][0]

        # loans table 반납 날짜 업데이트
        cur.execute('''UPDATE loans SET return_date = %s WHERE book_id= %s''', (r_date, id))
        # books table 대출 가능으로 업데이트
        cur.execute('''UPDATE books SET is_available = TRUE WHERE book_id= %s''', id)
        conn.commit()
        print('=============도서 반납 완료=============')

        choice = input('계속해서 반납하시겠습니까? (Y/N): ')
        if choice == 'N':
            break


# 대출 정보 조회 기능
def loan_search():
    clear()
    print('-----------------------------------')
    print('-------대출한 도서 정보 조회-----------')
    print('-----------------------------------\n')

    cur.execute('''SELECT * FROM loans ORDER BY loan_date;''')
    loans_info = cur.fetchall()

    print('| 대출ID |  회원ID  |  이름  | 도서ID |   도서명   |  대출 일자 |  반납 일자  |')

    for loan in loans_info:
        print('|   ' + str(loan[0]) + '   |   ' + str(loan[1]) + '   |   ' + str(loan[2]) +
              '  |  ' + str(loan[3]) + '   |   ' + str(loan[4]) + '   |   ' + loan[5].strftime('%Y-%m-%d')
              + '  |  ' + str(loan[6]) + '  | ')
    print('======= 대출 도서 정보 조회 완료 =======\n')


# 종료 기능
def off():
    print('-----------------------------------')
    print('----------메뉴를 종료합니다----------')
    cur.close()
    conn.close()


### CLI 기반 메뉴
# Select Main Menu
def select_main_menu():
    print('-----------------------------------')
    print('     도서관 관리 시스템 메인 메뉴      ')
    print('-----------------------------------')
    print(' 0. 도서 정보 입력 \n 1. 도서 정보 조회 \n 2. 도서 대출\n 3. 도서 반납\n 4. 대출 정보 조회\n 5. 종료\n ')
    print('6. 이전 메뉴로 돌아가기')
    print('-----------------------------------')
    menu_num = input()
    print('사용자 선택 메뉴---> ', menu_num)
    return menu_num


def main():
    user_id = input('user_id를 입력하세요: ')
    while True:
        menu = select_main_menu()
        if menu == '0':
            data_input()
        elif menu == '1':
            book_search()
        elif menu == '2':
            book_loan(user_id)
        elif menu == '3':
            return_book()
        elif menu == '4':
            loan_search()
        elif menu == '5':
            off()
            clear()
            break
        elif menu == '6':
            clear()
            pass

if __name__ =="__main__":
    main()
