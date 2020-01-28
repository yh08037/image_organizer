# This Python file uses the following
#encoding: utf-8

import os
import re
import sys
import shutil


# 폴더 내부 모든 파일 이름의 리스트로 부터 20190720_143647.png 와 같은
# 형식의 파일만을 선별하여 사진 파일 이름의 리스트를 반환합니다.

def getPhotoNames(file_list):
    p = re.compile('\d{8}_\d{6}[.][a-zA-z]{3,4}')
    result = []
    for item in file_list:
        m = p.match(item)
        if m:
            result.append(m.group())
    return result



# 사진 파일 이름 리스트로 부터 날짜와 시간을 추출합니다.

def preprocess(photo_list):
    date = []
    time = []

    for photo in photo_list:
        date = int(photo[4:6]), int(photo[6:8])
        
        hour = float(photo[9:11])
        min = float(photo[11:13])
        sec = float(photo[13:15])
        _time = hour + min/60 + (sec/60)/60
        time.append(_time)

    return date, time



def argsort(seq):
    return [x for x,y in sorted(enumerate(seq), key = lambda x: x[1])]



# 메인 무한 루프

while True:
    
    # 바탕화면 경로 정의, 바탕화면으로 디렉터리 이동

    path_home = 'C:/Users/김도훈/Desktop'
    os.chdir(path_home)


    # 작업대상인 폴더의 이름을 입력받습니다.
    
    while True:
        folder = input('장소를 분류할 날짜의 사진폴더 이름 입력 : ')
        path_dir = path_home + '/' + folder


        # 입력받은 이름의 폴더가 바탕화면에 존재하지 않을 경우 다시 입력받습니다.

        if not os.path.exists(path_dir):
            print('존재하지 않는 폴더입니다. 다시 입력해주세요.\n')
            continue


        # 입력받은 이름의 폴더가 바탕화면에 존재할 경우

        # 폴더 내부의 전체 파일 이름 목록을 생성하고, 오름차순으로 정렬합니다.
        
        file_list = os.listdir(path_dir)
        file_list.sort()


        # getPhotoNames() 함수를 통해 폴더 내에서 사진 파일만을 선별한 리스트를 생성합니다.

        photo_list = getPhotoNames(file_list)
        num_photos = len(photo_list)


        # 입력받은 폴더 내에 사진 파일 형식에 맞는 이름의 파일이 없을 경우 다시 입력받습니다.
        
        if num_photos == 0:
            print('폴더 내에 사진이 존재하지 않습니다. 다시 입력해주세요.\n')
        else:
            break

    print()
    print('총 사진 수 :', num_photos)

    num_places = int(input('분류할 장소의 수 입력 : '))
    print()
    print('%d개 장소의 이름을 시간 순서대로 입력해주세요.' %num_places)
    name_places = []
    for i in range(num_places):
        name_places.append(input('장소 %d : ' %(i+1)))

    print()
    print('시간 간격을 기준으로 분류합니다.')

    date, time = preprocess(photo_list)

    time_interval = [ (time[i+1]-time[i]) for i in range(num_photos-1) ]
    time_interval.insert(0, 0)

    boundarys = argsort(time_interval)[-(num_places-1):]
    boundarys.append(num_photos)
    boundarys.sort()

    dirName = folder + ' 장소별 정리'

    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print('바탕화면에 "' + dirName + '" 폴더를 생성하였습니다.')
    else:
        print(dirName + " 폴더가 이미 존재합니다.")
        sys.exit()

    path_place = path_home + '/' + dirName

    cnt = 0
    names = []
    for i in range(num_places):
        tmp = []
        while cnt < boundarys[i]:
            tmp.append(photo_list[cnt])
            cnt += 1
        names.append(tmp)

    i = 0
    for name in names:
        dirPlace = name_places[i] + ' (%d.%d)' %(date[0], date[1])
        os.chdir(path_place)
        os.mkdir(dirPlace)
        os.chdir(path_home)
        path_new = path_place + '/' + dirPlace
        for pic in name:
            shutil.copy(path_dir+'/'+pic, path_new+'/'+pic)
        i+=1
    else:
        print('복사 완료')

    print()

    breakstate = 0

    while True:
        flag = input('계속 진행하겠습니까? Y: 다음 폴더 작업 진행, N: 프로그램 종료    ').lower()

        if flag == 'y' or flag == 'yes' or flag == 'o':
            breakstate = 1
            break
        elif flag == 'n' or flag == 'no' or flag == 'x':
            breakstate = 2
            break

    if breakstate == 2:
        break

    print('\n')
