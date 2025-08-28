# users
### id : VARCHAR(255)
- PK
- 디스코드 사용자 ID (개발자 도구)로 지정
### last_level_clear : INT
- nullable
### last_quest_clear : INT
- nullable
### username : VARCHAR(255)
### level : INT
- 기본값 1
### exp : BIGINT
- 기본값 0
### tier : TINYINT
- 기본값 4
- enum 등으로 1~4까지 티어 이름 부여
### main_hand : VARCHAR(255)
- 아마 왼손 or 오른손
- nullable
### number_of_keys : VARCHAR(255)
- 아마 숫자
- nullable
### multi_input_direction : VARCHAR(255)
- 아마 왼쪽 or 오른쪽 계단
- nullable
### details : VARCHAR(4096)
- nullable
### created_at : TIMESTAMP
### deleted_at : TIMESTAMP


# quests
### id : SMALLINT
- PK
### name : VARCHAR(255)
### stars : TINYINT
### type : TINYINT
- 0 : 일반 퀘스트
- 1 : 합동 퀘스트
- 2 : 이벤트 퀘스트
### req : TINYINT
- 0 : 합동 or 이벤트 퀘스트인 경우
- 1 : 한손 클리어
- 2 : 한손 완플
- 3 : 한손 3키 클리어
- 더 추가될 예정
### exp : SMALLINT
- 올클리어 보상


# levels
### id : MEDIUMINT
- PK
### quest_id : SMALLINT
- FK _(ref. quests)_
### artist : VARCHAR(255)
### song : VARCHAR(255)
### creator : VARCHAR(255)
### exp : SMALLINT


# level_clears
### id : INT
- PK
### user_id : VARCHAR(255)
- FK _(ref. users)_
### level_id : MEDIUMINT
- FK _(ref. levels)
### created_at : TIMESTAMP


# quest_clears
### id : INT
- PK
### user_id : VARCHAR(255)
- FK _(ref. users)_
### quest_id : SMALLINT
- FK _(ref. quests)_
### created_at : TIMESTAMP


# collab_quest_progress
### id : SMALLINT
- PK
### level_clear_id : INT
- FK
### part : VARCHAR(255)
- 1-A-5 : 1번째 맵 A형 5번째 파트
- 4-B-9 : 4번째 맵 B형 9번째 파트
### video : VARCHAR(255)
### created_at : TIMESTAMP