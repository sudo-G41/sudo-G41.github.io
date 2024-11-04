---
title: "리스트를 이용하여 폴더 찾기"
excert: "python os 라이브러리와 dir명령어를 이용하여 파일 검색"
categories:
  - dev
tags:
  - python
  - python os
  - windows cmd
  - dir
  - dir /b
last_modified_at: 2024-11-04T23:53:00+09:00

toc_label: I.N.D.E.X
toc: true
toc_sticky: true

author_profile: false
sitemap :
  changefreq : daily
  priority : 1.0
---

# 목표
python windows 명령어 사용하기

사용할 윈도우 명령어
- dir (옵션 /b )

python os를 사용

# 코드
```python
from os import popen

with open("list.csv", "r", encoding="utf-8-sig") as file:
    # 현재 폴더 내 폴더 이름 저장
    lst = popen("dir /b").readlines()
    # 찾아야할 폴더 리스트
    flist = file.readlines()

    #필요 없는 파일(.vscode 등) 제거
    lst = lst[2:-1]

    dic = {}
    # 현재 저장된 폴더들 이름 형식이 날짜_이름 형식이어서 딕셔너리에 해당 형식을 찾기 쉽게 저장
    # {이름:날짜_이름}
    for l in lst:
        l = l.strip()
        if l not in dic:
            k = l[len("2024-10-21_"):]
            if k:
                dic[k]=l

    for file_name in flist:
        file_name = file_name.strip()
        file_name = str(file_name)
        dir_name = dic[file_name]
        a = popen(f"dir /b {dir_name}").readlines()
        if a:
            # csv파일로 저장 하는데 dir로 검색된 내용 뒤에 \n이 붙어있으므로 print 기본값을 이용하면 개행이 2번 되므로 end를 변경
            print(f"{file_name},",a[0],end="")
        else:
            print(file_name)
```

# 설명
list.csv에 정의된 폴더 이름을 가지고 해당 폴더 내 사전순 첫번째 파일 이름을 찾는 코드이다.

해당 코드를 작성한 이유는 필요없는 파일들과 폴더를 지우고 필요한 파일 폴더만 남기기 위래 만든 코드이다.

코드를 설명하자면

``` python
  lst = popen("dir /b").readlines()
```
에서 현재 경로의 모든 폴더를 저장한다.
``` python
  flist = file.readlines()
```
을 통해 내가 찾고자 하는 폴더를 리스트에 저장합니다.
``` python
  a = popen(f"dir /b {dir_name}").readlines()
```
를 이용해서탐색을 진행한다.

구조를 조금 더 살펴보면 "dir /b 경로" 을 이용하여 탐색을 진행하는데

dir은 windows에 있는 ls와 같은 명령어로 해당 경로의 파일과 폴더를 보여주는 명령어이지만
리눅스와의 차이점은 ls는 파일 및 폴더만 보여준다면, dir은 여러 정보와 같이 보여준다.

이런 불필요한 정보를 빼고 출력하기 위해 /b옵션을 넣어 출력 시켰다.

# 마지막으로
사실 subprocess나 pandas를 사용하면 좋긴 한데

* pandas안쓴지 오래라 기억이 안남
* subprocess를 쓰려 했는데  windows 오류남 파일을 못찾는다고 하면서

그래서 그냥 os를 사용해서 작성 하였다.