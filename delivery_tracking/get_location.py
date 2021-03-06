from typing import Tuple
import requests
import json


class GetLocationError(Exception):
    pass


class NoSearchResultError(Exception):
    pass


def get_location(keyword: str) -> dict:
    headers: dict = {'Authorization': ''}  # secret key
    params: dict = {'analyze_type': 'similar', 'query': keyword}

    res = requests.get(
        'https://dapi.kakao.com/v2/local/search/keyword.json?', headers=headers, params=params)

    if res.status_code == 200:  # 정상적으로 정보를 가져왔을 경우
        data: dict = json.loads(res.text)
        if data['meta']['total_count'] != 0:  # 검색결과가 존재할 경우
            # 첫번째 검색결과가 올바른 정보라고 가정
            loc: dict = {
                'lat': data['documents'][0]['y'],
                'lng': data['documents'][0]['x'],
                'name': data['documents'][0]['place_name'],
                'step': int
            }
            return loc
        else:
            raise NoSearchResultError('검색결과가 존재하지 않습니다')  # 검색결과가 존재하지 않을 경우
    else:
        data: dict = json.loads(res.text)
        # 가져오지 못했을 경우 Status 객체를 반환하므로 그 안의 msg를 출력
        raise GetLocationError(data['message'])


if __name__ == "__main__":
    try:
        location: dict = get_location(
            '')  # 조회시 keyword는 1. 전화번호 2. 택배사 + 지점이름
        print(location)
    except GetLocationError as e:
        print(e)
    except NoSearchResultError as e:
        print(e)
