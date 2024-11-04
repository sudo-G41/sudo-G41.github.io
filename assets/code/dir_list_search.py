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