sampletoken.json을 복사한 뒤 token.json으로 이름을 바꿔, 디스코드 봇의 토큰과 Gemini API 키를 입력하여주시기 바랍니다.
# discordTarot
2024년 2학기 자료구조 수행평가를 위해 제작하게 된 프로젝트입니다.
총 제작기간: 4시간 30분

![image](https://github.com/user-attachments/assets/81c48c18-616e-4871-9fdd-1d4e974bcdb1)

사용자에게서 6개의 숫자를 입력받아 나온 타로 카드의 해석을 인공지능이 해주는 디스코드 봇입니다.

## 작동 원리
![image](https://github.com/user-attachments/assets/1e3c39fb-f68d-408e-a55d-196b2ce8b769)

유저에게서 0~21까지의 숫자 중 6개를 드롭메뉴를 통해 입력받는다.

![image](https://github.com/user-attachments/assets/52ebdf6b-218c-4bc0-acbc-1b13d8c1274d)

유저에게서 입력받은 값들을 다른 랜덤 값으로 바꾼다. (예: 1 -> 5, 4 -> 19 등...)

![image](https://github.com/user-attachments/assets/14b1d7bf-5cc0-4f48-8fb5-129b2e18208d)

6 칸의 리스트를 0 혹은 1로 채운다. (카드의 정방향 혹은 역방향 구분)

![image](https://github.com/user-attachments/assets/55e13fc4-2d8b-4a20-8ec5-72dcc02c62c0)

프롬프트가 적용된 AI에게 n번째 리스트(올해 회고, 미래 전망, 연애운, 직업운, 인간관계, 가져야 할 마음가짐)와 뽑힌 카드를 물어봐, 운세를 받는다.

## 주 사용 기술
- `discord.py`: 디스코드 봇을 만들기 위한 라이브러리
- `Gemini API`: 구글의 인공지능 Gemini를 사용하기 위한 API

Thanks to. 이승우 - 챗GPT API를 활용한 챗봇 만들기(개정판)
