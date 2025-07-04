# personality-insight

### 명령어
```bash
source venv/bin/activate        # 맥 가상환경 활성화
.\venv\Scripts\Activate.ps1     # 윈도우 가상환경 활성화
pip freeze > requirements.txt   # 현재 환경의 패키지 목록 저장
pip install -r requirements.txt # 설치
```

## 동작 사진
<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/fecfab5f-e3fa-4015-b421-62e29a992f04" width="400">
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/8ece6ca9-8f55-40ab-9a21-1b8289581da2" width="400">
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/967b4196-7e03-489c-af2e-de243574e3c0" width="300">
    </td>
  </tr>
</table>



## 데이터 분석
### 주제: Extrovert vs. Introvert Behavior Data

- Extrovert 및 Introvert의 특징을 도표로 정리하고 간단한 설문조사를 통한 성향분석 프로그램을 개발한다.

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
...
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

## 🧰 데이터 분석 및 시각화 스택

### 📊 데이터 처리
- **Pandas**  
  - Snowflake 테이블 또는 AWS S3에서 불러온 데이터를 전처리 및 집계
  - 결측치 처리, 그룹별 평균 계산 등 통계 분석 수행

### 📈 데이터 시각화
- **Plotly**  
  - 막대그래프, 히스토그램 등 대화형 시각화 구현  
- **Streamlit**  
  - 실시간 필터링 및 대시보드 형태의 결과 공유  
  - 사용자 친화적인 웹 UI 제공

### 🧠 머신러닝 모델링
- **Scikit-learn**
  - `RandomForestClassifier` 로 성격 유형 분류 모델 구현
  - `train_test_split` , `accuracy_score`, `classification_report` 등으로 성능 평가
  - `predict_proba()` 로 예측 결과에 대한 확률 출력

### 🏢 데이터 웨어하우스
- **Snowflake**  
  - `Snowpark` API로 SQL 없이 파이썬 코드로 데이터 조작 가능  
  - `STAGE`, `COPY INTO`, `FILE FORMAT` 등으로 외부 S3 데이터 적재  
  - Role 기반으로 접근 권한 제어

### ☁️ 클라우드 연동
- **AWS S3**  
  - 설문/로그 등 원시 데이터를 저장하는 데이터 레이크 역할  
- **IAM Role 연동**  
  - Snowflake에서 S3에 접근할 수 있도록 외부 스테이지에 Role 부여


### 결측치 및 이상치 분석

```
📌 컬럼별 결측치 개수:
TIME_SPENT_ALONE             0
STAGE_FEAR                   0
SOCIAL_EVENT_ATTENDANCE      0
GOING_OUTSIDE                0
DRAINED_AFTER_SOCIALIZING    0
FRIENDS_CIRCLE_SIZE          0
POST_FREQUENCY               0
PERSONALITY                  0
dtype: int64
--------------------------------------------------
📊 TIME_SPENT_ALONE 컬럼의 IQR 분석:
  - Q1 (25%): 2.0
  - Q3 (75%): 7.0
  - IQR      : 5.0
  - 하한선 (Q1 - 1.5*IQR): -5.5
  - 상한선 (Q3 + 1.5*IQR): 14.5
--------------------------------------------------
🚨 TIME_SPENT_ALONE 이상치 개수: 0
```

### 🧪 모델 평가 결과 (`RandomForestClassifier`)

| Metric        | Introvert | Extrovert | Macro Avg | Weighted Avg |
|---------------|-----------|-----------|-----------|--------------|
| **Precision** | 0.91      | 0.94      | 0.92      | 0.92         |
| **Recall**    | 0.93      | 0.91      | 0.92      | 0.92         |
| **F1-score**  | 0.92      | 0.92      | 0.92      | 0.92         |
| **Support**   | 278       | 302       | 580       | 580          |

- 🎯 **정확도(Accuracy)**: `0.92`
