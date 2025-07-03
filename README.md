# personality-insight

### 명령어
```bash
source venv/bin/activate        # 맥 가상환경 활성화
.\venv\Scripts\Activate.ps1     # 윈도우 가상환경 활성화
pip freeze > requirements.txt   # 현재 환경의 패키지 목록 저장
pip install -r requirements.txt # 설치
```

## 데이터 분석
### 주제: Extrovert vs. Introvert Behavior Data
#### 링크
https://www.kaggle.com/datasets/rakeshkapilavai/extrovert-vs-introvert-behavior-data/data

#### 데이터 예시
```
Time_spent_Alone,Stage_fear,Social_event_attendance,Going_outside,Drained_after_socializing,Friends_circle_size,Post_frequency,Personality
4.0,No,4.0,6.0,No,13.0,5.0,Extrovert
9.0,Yes,0.0,0.0,Yes,0.0,3.0,Introvert
9.0,Yes,1.0,2.0,Yes,5.0,2.0,Introvert
0.0,No,6.0,7.0,No,14.0,8.0,Extrovert
3.0,No,9.0,4.0,No,8.0,5.0,Extrovert
1.0,No,7.0,5.0,No,6.0,6.0,Extrovert
4.0,No,9.0,3.0,No,7.0,7.0,Extrovert
2.0,No,8.0,4.0,No,7.0,8.0,Extrovert
10.0,Yes,1.0,3.0,Yes,0.0,3.0,Introvert
0.0,No,8.0,6.0,No,13.0,8.0,Extrovert
3.0,No,9.0,6.0,No,15.0,5.0,Extrovert
10.0,Yes,3.0,1.0,Yes,4.0,0.0,Introvert
2.0,No,6.0,4.0,No,12.0,10.0,Extrovert
```

### 컬럼설명

- `Time_spent_Alone`: 하루 평균 혼자 보내는 시간 (시간 단위)
- `Stage_fear`: 대중 앞에서 발표하거나 무대에 설 때 두려움을 느끼는지 여부 (Yes/No)
- `Social_event_attendance`: 사회적 모임이나 행사에 참석하는 횟수
- `Going_outside`: 외출 빈도 (일주일 또는 하루 기준)
- `Drained_after_socializing`: 사람들과 어울린 뒤 피로감을 느끼는지 여부 (Yes/No)
- `Friends_circle_size`: 친밀한 친구나 교류하는 사람의 수 (네트워크 크기)
- `Post_frequency`: SNS(소셜미디어)에서 게시물을 올리는 빈도
- `Personality`: 해당 사람의 성격 유형 (Extrovert: 외향형 / Introvert: 내향형)
