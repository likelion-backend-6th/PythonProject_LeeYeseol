## Python Library project

-----------------------------------------
### Project Summary
- Python을 활용하여 console기반의 도서관 관리 시스템을 개발
- PostgreSQL을 활용하여 데이터 관리


-----------------------------------------------
### Project Check List
<details>
<summary> Check Lists </summary>
<div markdown="1">       

#### 1. 데이터 입력 기능(data_input)
- [x]  사용자는 콘솔을 통해 도서의 정보를 입력하여 데이터베이스에 저장

#### 2. 도서 정보 조회 기능(book_search)
- [x]  사용자는 도서의 ID 혹은 이름을 입력하여 도서의 정보를 조회
- [x] 도서의 정보는 도서의 ID, 이름, 저자, 출판사 정보를 포함
- [x] 도서의 상태(대출 가능, 대출 중)가 표시
- [x] 도서의 상태는 도서가 대출 가능한 상태인지, 대출 중인 상태인지를 표기
- [x] 도서가 대출 중인 상태인 경우, 도서의 대출 정보를 함께 출력
#### 3. 도서 대출 기능(book_loan)
- [x] 사용자는 콘솔을 통해 도서의 ID 혹은 이름을 입력하여 도서를 대출합니다.
- [x] 대출하면 도서의 상태를 대출중으로 변경합니다.
- [x] 대출중인 도서를 모두 출력합니다.
- [x] 도서가 이미 대출 중일 경우, 대출이 불가능하다고 출력합니다.
#### 4. 도서 반납 기능 
- [x] 반납을 원하는 도서의 ID 혹은 이름을 입력하여 반납합니다.
- [x] 반납하면 도서의 상태가 대출 가능으로 변경됩니다.

#### 5. 대출 정보 조회 기능 

- [x] 대출한 도서의 정보를 모두 조회할 수 있습니다.
- [x] 대출 정보는 도서의 ID, 대출 받은 user 이름, 도서명, 대출 날짜, 반납일자로 구성됩니다.
- [x] 대출 정보는 대출 날짜를 기준으로 내림차순으로 정렬됩니다.

#### 6. 종료 기능 

- [x] 사용자는 프로그램을 종료할 수 있습니다.

#### 0. CLI 기반 메뉴 

- [x] 사용자는 콘솔을 통해 메뉴를 선택할 수 있습니다.
- [x] 사용자가 선택한 메뉴에 따라 해당 기능을 실행합니다.
- [x] 사용자는 메뉴를 통해 프로그램을 종료할 수 있습니다.
- [x] 사용자는 메뉴를 통해 이전 메뉴로 돌아갈 수 있습니다.
- [x] 메뉴 선택시 콘솔을 삭제하여 사용자가 선택한 메뉴만 출력합니다.
- [x]  사용자는 메뉴를 통해 프로그램을 종료
</div>
</details>

-------------------------------------------------
### Database Schema

###  books table

| Column Name  |     Data Type     |      Constraints       |
|:------------:|:-----------------:|:----------------------:|
|   `book_id `   |      INTEGER      | PRIMARY KEY, NOT NULL |
|    `title`     |   VARCHAR(100)    |        NOT NULL       |
|   ` author`    |   VARCHAR(100)    |        NOT NULL       |
| ` publisher `  |   VARCHAR(100)    |        NOT NULL       |
| `is_available` |      BOOLEAN      | NOT NULL, DEFAULT TRUE|
###  loans table

|   Column Name   |  Data Type   |      Constraints      |
|:---------------:|:------------:|:---------------------:|
|   `loan_id `    |   INTEGER    | PRIMARY KEY, NOT NULL |
|   `user_id `    |   INTEGER    | FOREIGN KEY, NOT NULL |
|   `user_name`   | VARCHAR(100) |       NOT NULL        |
|   `book_id `    |   INTEGER    | FOREIGN KEY, NOT NULL |
|    ` title`     | VARCHAR(100) |       NOT NULL        |
|  ` loan_date `  |     DATE     |       NOT NULL        |
| ` return_date ` |     DATE     |       NULL            |


###  users table

| Column Name |     Data Type     |      Constraints       |
|:-----------:|:-----------------:|:----------------------:|
| `user_id `  |      INTEGER      | PRIMARY KEY, NOT NULL |
| `user_name` |   VARCHAR(100)    |        NOT NULL       |



----------------------------------------------
### Project 회고
- 시간투자를 많이 못해서 아쉽다.
- 좀 더 깔끔하게 코드를 작성하지 못한게 매우 아쉽다.
- 모듈화를 시켜서 깔끔하게 작성해봐야겠다.
- 