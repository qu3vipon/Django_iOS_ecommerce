# Requirements
- Python >= 3.7
- Poetry >= 1.0

<br>

# iOS 앱 시연 영상
[동영상 보기](https://youtu.be/Go3h9PNa0l8)

<br>

# API 문서 
## Authentication

Basic Auth: 개발 편의를 위해 사용 

- Basic Auth  `<username:password>`

Token Auth

- HTTP Header `Authorization Token <#$%134asdf>`



<hr>

## Exception Codes

### 기본

- permission_denied: 권한 없음 (다른 유저의 정보에 접근한 경우)

### 회원가입

- TakenNumber: 이미 가입된 휴대폰 전화번호
- InvalidNumber: 휴대폰 인증이 완료되지 않은 상태(인증 요청도 되지 않은 상태)
- ResendSMS: 휴대폰 인증 번호 재발송
- UnauthorizedMobileNumber: 휴대폰 인증이 완료되지 않은 상태
- InvalidToken: 휴대폰 인증 번호 틀렸을 때
- TakenUsername: username 중복

### 장바구니

- ProductOptionNotMatching: 옵션에 해당하는 상품이 올바르게 입력되지 않은 경우

> 예시) 상품: 우유 2종 / 옵션: 미나리 10g

- UnauthorizedException: 인증되지 않은 사용자의 접근 -> authentication 필요
- InvalidOptionIdException: 옵션 id와 부모 상품의 id가 매칭되지 않을 경우


### 홈화면

- InvalidOrderingException : 허용하지 않는 정렬 기준이 입력된 경우

> 신상품에는 '-sales', '-price', 'price', 베스트에는 '-create_at', '-sales', '-price', 'price', 알뜰쇼핑에는 '-created_at', '-sales', '-price', 'price'만 올 수 있음



<hr>

## User

회원가입 및 마이컬리 페이지



<hr>

### POST/ Check Duplicates

URL: http://marketbroccoli.ga/accounts/duplicates/

회원가입 전, Username 중복 검사 API

- Authorization: No Auth

#### Headers

Content-Type: application/json

#### Body

raw (application/json)

```json
{
    "username": "admin1"
}
```

#### Returns

```json
# 성공
{
    "username": "admin1"
}

# 실패
{
    "detail": "username이 이미 존재합니다.",
    "status": 400,
    "code": "TakenUsername"
}
```



<hr>

### POST/ Mobile Token Create

URL: http://marketbroccoli.ga/accounts/m-token-create/

휴대폰 인증번호 요청 API -> 문자 발송

- 휴대폰 인증번호: 6자리 랜덤 숫자
- Authorization: No Auth

#### Headers

Content-Type: application/json

#### Body

raw (application/json)

```json
{
    "number": "01011112222"
}
```

#### Returns

```json
# 성공
{
    "number": "+821011112222",
    "token": "335670"
}

# 실패
{
    "detail": "이미 가입된 번호입니다.",
    "status": 400,
    "code": "TakenNumber"
}
```



<hr>

### POST/ Mobile Token Authenticate

URL: http://marketbroccoli.ga/accounts/m-token-auth/

휴대폰 인증번호 문자 수령 후, 인증번호 입력하면 검증하는 API

- Authorization: No Auth

#### Headers

Content-Type: application/json

#### Body

raw (application/json)

```json
 {
    "number": "01011112222",
    "token": "123456"
}
```

#### Returns

```json
# 성공
{
    "number": "010-1111-2222",
    "is_authenticated": true
}

# 실패
{
    "detail": "토큰값이 유효하지 않습니다.",
    "status": 400,
    "code": "InvalidToken"
}
```



<hr>

### POST/ User Create

URL: http://marketbroccoli.ga/accounts/

회원가입 요청 API

> 휴대폰 인증된 휴대폰 번호로만 회원가입 가능

- Authorization: No Auth
- Optional Field: `birht_date`, `gender`

> `gender`: `m`, `f`, `n` 중 선택

#### Headers

Content-Type: application/json

#### Body

raw (application/json)

```json
{
    "username": "test1",
    "email": "test1@example.com",
    "password": "test123",
    "name": "test1",
    "mobile": "01011112222",
    "address": {
        "address_name": "지번주소",
        "road_address": "도로명주소",
        "zip_code": "123456"
    },
    "birth_date": "2020-02-02",
    "gender": "m"
}
```

### Returns

```json
# 성공
{
    "id": 1,
    "email": "test1@example.com",
    "username": "test1",
    "name": "test1",
    "mobile": {
        "number": "010-1111-2222",
        "is_authenticated": true
    },
    "address": {
        "address_name": "지번주소",
        "road_address": "도로명주소",
        "zip_code": "123456"
    },
    "birth_date": "2020-02-02",
    "gender": "m",
    "last_login": null
}

# 실패
{
    "username": [
        "A user with that username already exists."
    ],
    "status": 400,
    "code": "invalid"
}
```



<hr>

### POST/ User Auth Token

URL: http://marketbroccoli.ga/accounts/auth-token/

회원가입 후, 최초 로그인 시 유저의 인증토큰 반환하는 API

> 유저마다 고유한 인증토큰 생성
> 유저의 고유한 동작시(주문 등) 반드시 인증 필요
> 유저 인증토큰과 모바일 인증토큰 다름

- Authorization: No Auth

#### Headers

Content-Type: application/json

#### Body

raw (application/json)

```json
{
	"username": "admin",
	"password": "admin123"
}
```

#### Returns

```json
# 성공
{
    "token": "3f3eaf3787bd0b35fb9ca2692d81e30d5b80fa95",
    "user": {
        "id": 1,
        "email": "admin@example.com",
        "username": "admin",
        "name": "",
        "mobile": {
            "number": "010-1111-0000",
            "is_authenticated": false
        },
        "address": {
            "address_name": "지번주소",
            "road_address": "도로명주소",
            "zip_code": "456123"
        },
        "birth_date": null,
        "gender": "n",
        "last_login": "2020-04-25T23:53:48.970126+09:00"
    }
}

# 실패
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ],
    "status": 400,
    "code": "invalid"
}
```



<hr>

### GET/ User Detail

URL: http://marketbroccoli.ga/accounts/1/

개별 유저의 정보를 반환하는 API

> url: `/accounts/<user_id>/`

- Authorization: Basic / Token

- Permissions: 로그인 된 유저 자신의 정보만 요청 가능

  > 예) user1(id=1)로 authentication하고 user2(id=2)로 요청 시 403 forbidden



<hr>

## Cart

장바구니

- 자신의 장바구니만 접근 가능 (Authentication 필수)



<hr>

### GET/ Cart List

URL: http://marketbroccoli.ga/kurly/cart/

장바구니 리스트 API

- Authorization: Basic / Token

#### Returns

```json
# 성공
[
    {
        "id": 162,
        "product": {
            "pk": 1398,
            "name": "[비박스] 멀티 이유식 머그 4종",
            "discount_rate": 0.0,
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        },
        "option": {
            "pk": 1709,
            "name": "[비박스] 멀티 이유식 머그 네온퍼플",
            "price": 11000,
            "product": 1398
        },
        "quantity": 30
    },
    {
        "id": 361,
        "product": {
            "pk": 200,
            "name": "[쥬니] 호주산 프리미엄 램 등심 200g(냉동)",
            "price": 14500,
            "discount_rate": 0.0,
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        },
        "quantity": 2
    }
]
```



<hr>

### POST/ Cart Create (Add Item)

URL: http://marketbroccoli.ga/kurly/cart/

장바구니에 상품 추가 API

> 장바구니에 상품이 이미 존재하는 경우, 장바구니 아이템 수량 증가
>
> option이 존재하지 않는 상품은 `null` 입력

- Authorization: Basic / Token

#### Body

raw (application/json)

```json
{
	"product": 1398,
	"option": 1709,
	"quantity": 2
}
```

#### Returns

```json
# 성공
{
    "id": 162,
    "product": {
        "pk": 1398,
        "name": "[비박스] 멀티 이유식 머그 4종",
        "discount_rate": 0.0,
        "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
    },
    "option": {
        "pk": 1709,
        "name": "[비박스] 멀티 이유식 머그 네온퍼플",
        "price": 11000,
        "product": 1398
    },
    "quantity": 30
}

# 실패-1 (존재하지 않는 상품)
{
    "product": [
        "Invalid pk \"1\" - object does not exist."
    ],
    "status": 400,
    "code": "invalid"
}

# 실패-2 (상품-옵션 매칭 오류)
{
    "detail": "상품과 옵션이 매칭되지 않습니다.",
    "status": 400,
    "code": "ProductOptionNotMatching"
}
```



<hr>

### GET/ Cart Detail

URL: http://marketbroccoli.ga/kurly/cart/162/

개별 장바구니 객체 확인 API

> url: `/kurly/cart/<cart_id>/`

- Authorization: Basic / Token

#### Path Variable

<card_id>

#### Returns

```json
# 성공
{
    "id": 162,
    "product": {
        "pk": 1398,
        "name": "[비박스] 멀티 이유식 머그 4종",
        "discount_rate": 0.0,
        "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
    },
    "option": {
        "pk": 1709,
        "name": "[비박스] 멀티 이유식 머그 네온퍼플",
        "price": 11000,
        "product": 1398
    },
    "quantity": 30
}

# 실패 (다른 user의 장바구니에 접근한 경우)
{
    "detail": "You do not have permission to perform this action.",
    "status": 403,
    "code": "permission_denied"
}
```



<hr>

### PATCH/ Cart Update

URL: http://marketbroccoli.ga/kurly/cart/162/

장바구니 페이지에서 상품의 옵션/수량 수정 API

- id에 해당하는 장바구니 객체의 정보를 수정
  - 옵션, 수량만 수정 가능
- Authorization: Basic / Token

#### Body

raw (application/json)

```json
{
	"product": 1398,
	"option": 1609,
	"quantity": 1
}
```

#### Path Variable

<cart_id>

#### Returns

```json
# 성공
{
    "id": 162,
    "product": {
        "pk": 1398,
        "name": "[비박스] 멀티 이유식 머그 4종",
        "discount_rate": 0.0,
        "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
    },
    "option": {
        "pk": 1709,
        "name": "[비박스] 멀티 이유식 머그 네온퍼플",
        "price": 11000,
        "product": 1398
    },
    "quantity": 1
}
```



<hr>

### DELETE/ Cart Delete

URL: http://marketbroccoli.ga/kurly/cart/30/

장바구니에 들어있는 객체 삭제

- Authorization: Basic / Token

성공시 204

#### Path Variable

<cart_id>

#### Returns

```json
# 성공
Status: 204 No Content

# 실패 (다른 user의 장바구니 접근한 경우)
{
    "detail": "You do not have permission to perform this action.",
    "status": 403,
    "code": "permission_denied"
}
```



<hr>

## Home

메인 페이지



<hr>

### GET/ Main Images 

URL: http://marketbroccoli.ga/kurly/images/

홈 화면 상단 이미지 10개 

#### Returns

```json
[
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585902036.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585815851.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585707374.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585632736.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585558857.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585746708.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1583112496.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1580465698.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585534858.jpg",
    "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/mobile_img_1585699841.jpg"
]
```



<hr>

### GET/ MD'S PICK

URL: http://marketbroccoli.ga/kurly/md/

- MD의 추천 상품 목록

- 카테고리 별 6개 상품 * 전체 15개 카테고리 = 총 90개 상품

#### Returns

```json
# 성공
[
  {
        "id": 2,
        "thumb_image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg",
        "name": "무농약 통셀러리 500g",
        "price": 3900,
        "discount_rate": 0.0,
        "summary": "아삭아삭 청량한 식감"
    },
  ...
]
```



<hr>

### GET/ Recommendation

URL: http://marketbroccoli.ga/kurly/recommend/?count=1/

- 추천 상품 리스트 반환
- `count`라는 key로 url에 value 입력시 해당 개수만큼의 물품 반환
  - 미입력시 default로 30개 반환

#### Query Params

count (optional)



<hr>

### GET/ New

URL: http://marketbroccoli.ga/kurly/recommend/new?count=5/

- 등록일자 최신순 상품 리스트 반환

- `count`라는 key로 url에 value 입력시 해당 개수만큼의 물품 반환

  - 미입력시 default로 30개 반환

- 신상품 내에서  '인기상품순', '낮은가격순', '높은가격순' 정렬 가능

  > 인기상품순: url에 '-sales' 추가
  > ex) http://marketbroccoli.ga/kurly/new/-sales/
  >
  > 낮은가격순: url에 'price' 추가
  > ex)http://marketbroccoli.ga/kurly/new/price/
  >
  > 높은가격순: url에 '-price' 추가
  > ex) http://marketbroccoli.ga/kurly/new/-price/

#### Query Params

count (optional)

#### Returns

```json
# 성공

# 실패 (정렬 기준 오류)
{
    "detail": "허용하지 않는 정렬 기준입니다.",
    "status": 400,
    "code": "InvalidOrderingOption"
}
```



<hr>

### GET/ Best

URL: http://marketbroccoli.ga/kurly/best?count=5/

판매량 내림차순 상품 리스트 반환

- `count`라는 key로 url에 value 입력시 해당 개수만큼의 물품 반환
  - 미입력시 default로 30개 반환
- 베스트 내에서 '신상품순',  '낮은가격순', '높은가격순' 정렬 가능

> 신상품순 : url에 '-created_at' 추가
> ex) http://marketbroccoli.ga/kurly/best/-created_at/
>
> 낮은가격순: url에 'price' 추가 
> ex)http://marketbroccoli.ga/kurly/best/price/ 
>
> 높은가격순: url에 '-price' 추가
> ex) http://marketbroccoli.ga/kurly/best/-price/

#### Query Params

count (optional)

#### Returns

```json
# GET/ New와 동일
```



<hr>

### GET/ Discount

URL: http://marketbroccoli.ga/kurly/discount/-sales?count=5/

- 할인율 내림차순 상품 리스트 반환 (알뜰상품)

- `count`라는 key로 url에 value 입력시 해당 개수만큼의 물품 반환
  미입력시 default로 30개 반환

- 알뜰상품 내에서 '신상품순', '인기상품순', '낮은가격순', '높은가격순' 정렬 가능

  > 신상품순 : url에 '-created_at' 추가
  > ex) http://marketbroccoli.ga/kurly/discount/-created_at/
  >
  > 인기상품순: url에 '-sales' 추가
  > ex) http://marketbroccoli.ga/kurly/discount/-sales/
  >
  > 낮은가격순: url에 'price' 추가
  > ex)http://marketbroccoli.ga/kurly/discount/price/
  >
  > 높은가격순: url에 '-price' 추가
  > ex) http://marketbroccoli.ga/kurly/discount/-price/

#### Query Params

count (optional)

#### Returns

```json
# GET/ NEW와 동일
```



<hr>

## Category

카테고리 및 상품 세부 페이지



<hr>

### GET/ Category List

URL: http://marketbroccoli.ga/kurly/category/

전체 카테고리 정보(id, 이름, 서브카테고리 목록)와 아이콘 이미지를 반환

#### Returns

```json
[
    {
        "id": 1,
        "name": "채소",
        "image_bk": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img_bk.png",
        "image_pp": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img_pp.png",
        "subcategories": [
            {
                "id": 1,
                "name": "기본채소"
            },
            	...
            {
                "id": 7,
                "name": "파프리카・피망・고추"
            }
        ]
    }
  	...
  ]
```



<hr>

### GET/ Subcategory Detail

URL: http://marketbroccoli.ga/kurly/subcategory/45/

해당 서브 카테고리 내의 상품 전체 출력

#### Path Variable

<subcategory_id>

#### Returns

```json
# 성공
[
    {
        "id": 236,
        "thumb_image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg",
        "name": "매실청 950g",
        "price": 8900,
        "discount_rate": 0.0,
        "summary": "따뜻하게 즐겨도 시원하게 즐겨도 맛있는 매실청"
    },
  	...
]
```



<hr>

## Product

상품 페이지



<hr>

### GET/ Product Detail

URL: http://marketbroccoli.ga/kurly/product/200/

상품의 세부 정보 출력

#### Path Variable

<product_id>

#### Returns

```json
{
    "id": 200,
    "name": "[쥬니] 호주산 프리미엄 램 등심 200g(냉동)",
    "summary": "구이용 (100g 당 판매가 : 7,250원)",
    "price": 14500,
    "discount_rate": 0.0,
    "unit": "1팩",
    "amount": "200g",
    "package": "냉동/종이포장",
    "made_in": "호주산",
    "description": "설명",
    "images": [
        {
            "name": "check",
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        },
        {
            "name": "detail",
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        },
        {
            "name": "main",
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        },
        {
            "name": "thumb",
            "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
        }
    ],
    "options": []
}
```

<hr>

### GET/ Product Option

URL: http://marketbroccoli.ga/kurly/product/14/option/

상품이 가지고 있는 옵션의 정보만 반환

#### Path Variable

<product_id>/option

#### Returns

```json
# 성공-1 (옵션이 존재하는 상품)
{
    "options": [
        {
            "pk": 2,
            "name": "청도미나리 500g",
            "price": 6500,
            "product": 14
        },
        {
            "pk": 1,
            "name": "청도미나리 300g",
            "price": 4200,
            "product": 14
        }
    ]
}

# 성공-2 (옵션이 존재하지 않는 상품)
{
    "options": []
}
```



<hr>

### GET/ Product Non-Login

URL: http://marketbroccoli.ga/kurly/product/?id=1398&option=1709

- 비로그인 장바구니 생성을 위한 상품 정보 반환
- `id`와 `option`이라는 key로 각각 `상품id`와 `옵션id`를 받아 해당하는 상품의 정보반환
  - `option`이 없는 경우, 생략 가능

### Query Params

id, option_id (optinal)

#### Returns

```json
# 성공
{
    "pk": 1709,
    "name": "[비박스] 멀티 이유식 머그 네온퍼플",
    "price": 11000,
    "product": {
        "pk": 1398,
        "name": "[비박스] 멀티 이유식 머그 4종",
        "price": 11000,
        "discount_rate": 0.0,
        "image": "https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/img.jpg"
    }
}
```

<hr>
