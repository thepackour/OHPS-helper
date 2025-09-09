### 레벨 클리어 알림
#### {
**'type':** 'level clear'

**'submitted_at'**: created_at *(/clears/add_level_clear)*

**'user_id':** c\['user_id'\] *(/clears/add_level_clear)*

**'level_id':** c\['level_id\'] *(/clears/add_level_clear)*

**'exp_before':** u\['exp'\] *(/clears/add_level_clear)*

**'exp_after':** u\['exp'\] + l\['exp'\] *(/clears/add_level_clear)*
#### }
###
### 올클리어(퀘스트 클리어) 알림
#### {
**'type':** 'quest clear'

**'submitted_at'**: created_at *(/clears/add_quest_clear)*

**'user_id':** c\['user_id'\] *(/clears/add_quest_clear)*

**'quest_id':** c\['quest_id\'] *(/clears/add_quest_clear)*

**'exp_before':** u\['exp'\] *(/clears/add_quest_clear)*

**'exp_after':** u\['exp'\] + q\['exp'\] *(/clears/add_quest_clear)*
#### }
###
### 챌린지 클리어 알림
#### {
**'type':** 'challenge clear'

**'submitted_at'**: created_at *(/challenges/add_challenge_clear)*

**'user_id'**: u\['user_id'\] *(/challenges/add_challenge_clear)*

**'level':** level *(/challenges/add_challenge_clear)*
#### }
###
### 티어 승급 알림
#### {
**'type':** 'tier up'

**'submitted_at'**: created_at *(/challenges/add_challenge_clear)*

**'user_id'**: u\['user_id'\] *(/challenges/add_challenge_clear)*

**'tier':** level.split("-")\[0\] *(/challenges/add_challenge_clear)*