---
title: "[중급] 리버스 코드 엔지니어링 훈련 (with KISA Academy)"
excert: "Reversing study"
categories:
  - sec
tags:
  - reversing
  - x64(32)dbg
  - PEview
  - HxD
  - KISA
  - CoreSecurity
last_modified_at: 2025-03-24T13:16:00+09:00

toc_label: 첫 게시물 목차 테스트
toc: true
toc_sticky: true

author_profile: false
sitemap :
  changefreq : daily
  priority : 1.0
---

# test head
--------------

# 실습에서 사용하는 툴

1. x64(32)dbg
1. PEview
1. HxD

# 설명

1. 실행파일을 타겟으로 잡고 어떻게 생겼는지 알아보는 과정
1. 디버깅에서 DnSpy(.net), ida 같은거 많음 

## 실행파일
실행파일은(C 기준)
main.c -> 컴파일 -> main.o -> 링킹 -> p포멧을 지닌 실행파일(PE) 
PE는 엔트리포인트 가 어디고 DLL, IAT를 실행파일 헤더에 넣음

실행 시
a.out -> loader -> push memory

이때 PE과정이 없으면 loader가 어디에 올릴지 몰라 대충 찍어 널음 그래서 링커가 작업을 해둔 메모리 공간에 넣음

물리메모리(물리주소)
초창기에는 
|메모리|
-------
|a.out|
|     |
|b.out|
|     |
|c.out|
|.....|

여서 막 침범 했는데

지금은 가상메모리를 만들어 가상 메모리에 올려서 공간 침덤 대책을함  
이떄 가상메모리 또한 물리메모리에 적제 하지 않으면 못쓰는건 같음  
그래서 테이블을 두고 물리메모리에 가상메모리의 주소를 넣어 거기를 바라보게 하는 것이 메핑 테이블이다.

이것을 확인해보자
x64dbg 툴로 cale.exe 두개 켜보자(x64를 2개 실행해서 각각 같은 calc.exe 열기)
그러면 memory open을 보면 같은 메모리 공간에 다른 PID를 확인가능(x64 dbg 제목 보자)

여기서 좀 더 가보면 ntdll.dll일 있는데 이건 기능 기준이라 각 각 할당 할 필요 없고 하나만 할당하고 가상메모리가 메핑테이블을 이용해 가져다 쓰는거

```
PID 5372---ㄱ  물리메모리 어딘가  
PID 4644-----> NTdll.dll
```

## PE

PEview로 cale.exe를 보자

PE파일은 MZ로 시작
MZ........... < MS-Dos 과정중 호환성을 위해 DOS HEAD와 스턱코드를 놔두고 밑에 붙여놓음

그리서 IMAGE_NT_HEADER 목록을 보면 첫 구간에 PE로 시작하는 것을 볼 수 있는데 이게
4byte 값에 e_lfanew(offset)가 있음

## file offset

헥스레이에 담겨있는 값은 스토리지 값

PEview는 RVA는 가상메모리값 file offset는 

데이터를 올릴때 section alignment가 있음 이거 크기 = 단위 정도로 생각해보자

PE헤더네는 NT헤더에 파일헤더에 어디서 실행될지 있고  
image optional헤더에 중요정보가 들어있음

EBP ESP -> memory stack의 베이스포인트, 스택포인트(top 포인터)

직접 보자

x32 켜서 cale.exe 실행 후 F9누름
memory map에서 calc.exe부분에 우클릭 팔로우 인 덤프 클릭 하면 해당 베이스 기준으로 메모리에 올라간 것을 확인 가능

여기서 컨트롤 G 누르고 메모리 주소 + 이미지 offset new 값(RVA값) 하면 그만큼 이동해서 PE를 찾아 볼 수 있음

MZ -> PE로 넘어가는 것

다른것도 볼 수 있음

즉 옵셔널 헤더 중요하다

### IMAGE_SECTION_DEADER .text

pointer to Raw Date 

### .idata
#### IMPORT Adderess Table

API 목록 볼 수 있음  
커널에 해당 요청 보낸테니 API 목록 중요  
악성코드가 주로 쓰는 API 보면 있음(사실 난 악성코드 분석업무 아니라... ㅎㅎ..)

컴파일 시 바로 main으로 들어가는 것이 아닌 stub code로 들어감감

## 실습

1. 섹션 삽입 문제
    - PE_Section.exe와 InsertMe 두 종류가 있음
    - PE_Section.exe를 실행해보면 "Insert Section into PE File"라는 문구가 나옴
    - 이걸 x32로 실행 -> F9 실행
    - Az아이콘(Find String)를 눌러보자
    - 여기서 파일 내 문자열을 확인 가능한데 메인인 Insert... 찾아보자
    - 해당 메모리로 이동해서 조금 올려보면 push ebp를 볼 수 있는데 여기가 main이라고 합니다.
    - 여기다가 더블클릭으로 주석 달고 F4를 눌러 EIP를 등록
    - 여기서 strcmp부분으로 다시 이동
    - F4를 눌러 해당 부분까지 실행
    - 스택부분(우하단)을 보면 .text, .extra, 8을 보면 2개의 문자열 8글자 비교하여 -1,0,1을 출력

이제 해보세요....??

1. 섹션명
1. 섹션개수
1. SectionAkignment & File Alignment 고려
1. 섹션 속성 부여

dk wlsKW anjs rothfldlswl ahfmrpTek...

wlsWK ahfmrpTek...

처음에는 섹션 사이즈 늘리기(섹션 파일 헤더 -> #오브 섹션의 RVA값 확인)
사이즈 오브 이미지를 늘려서 우리가 추가 할 것도 추가해줘야 함
섹션 복사
마지막 밑으로 붙여넣기
그 후 RVA값, 사이즈오브 로우데이터 값 포인터 투 로우데이터 값 변경

IAT <= 이거 뭔 소리인지 모르지만 call of ref말하는듯?

exe파일은 쉘 코드를 못불러옴 왜냐 모르니까....
그래서 셀프바인딩을 진행함

## 레지스터
EAX: 함수가 반환하는 리턴값 리턴 저장소랍니다.  
EBX: ??? 이거 뭐하는거야? 라고 하...? DS(데이터세그먼트에서 저장할 때)  
ECX: 루프 수 저장할 때 한답니다(for문에서 씁니다...?)  
EDX: I/O pointer에 사용한다 합니다. 강사님은 별로 못봤답니다. 막 써도 솔직히 모른답니다...  
EBP: 스택 시작점 기준점 함수가 스택 형식으로 돌아가잔아 이걸 각 함수마다 스택영역 정해줄 때 해당 값으로 스태의 시작점을 적어주는거 int *stack 같은거  
ESP: 이건 위에서 설정한 스택의 top 값  
ESI: 무언가를 복재할 때 복사 할 것의 위치  
EDI: 무언가를 복재할 때 복사 할 위치  
EIP: 실행중인 위치  

## 플래그
GS: 전
CS: code
DS: 데이터
SS: 스택 -> SS:[포인터 주소] 형식

## 보통 함수가 돌아가는 루틴
1. 기존 EBP를 새로 불러진 함수의 스택에 저장(돌아갈 장소)
1. mov로 현재 ESP를 자신의 EBP로 만듬(EBP에 ESP 값을 저장) ESP 0x01 EBP 0x00 => ESP 0x01 EBP 0x01 이런식으로
1. ESP =& FFFFFFF0 즉 1의자리만 0으로 만들고 나머지는 그대로 가져옴
1. sub ESP, 20 -> 이걸 왜 하는데? -> 저 20이 스택의 크기다 이 멍청아

나는 멍청이야.....

:wq