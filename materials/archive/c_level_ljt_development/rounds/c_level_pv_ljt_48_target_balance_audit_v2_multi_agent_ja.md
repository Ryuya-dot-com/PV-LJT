# Cレベル向けPhrasal Verb LJT 48項目マスター: 全体バランス監査 v2 Multi-Agent

作成日: 2026-07-04

対象ファイル:

- `c_level_pv_ljt_48_target_master_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v2_multi_agent.tsv`

## v1からの主な変更

マルチエージェント候補生成を用いて、以下7スロットを改稿した。

| Slot | PV | v1 score | v2 score | 変更内容 |
|---|---|---:|---:|---|
| cljt_010 | play out | 84 | 92 | negotiations/agreementからtrial/verdictへ変更 |
| cljt_022 | cut off | 76 | 91 | speech interruptionからcredit access terminationへ変更 |
| cljt_030 | put up | 61 | 90 | display/attach senseからmoney/security senseへ変更 |
| cljt_033 | open up | 84 | 91 | policy/opportunitiesからlegal appeal optionsへ変更 |
| cljt_035 | fill in | 78 | 90 | information-topic frameからtemporary substitute frameへ変更 |
| cljt_036 | hold up | 84 | 90 | payment/receiptからpermit/blueprintへ変更 |
| cljt_040 | come out | 76 | 90 | reveal senseからpublic stance senseへ変更 |

## 形式検証

v2_multi_agentは以下の機械チェックを通過した。

- マスター行数: 96
- ターゲット数: 48
- マスター内条件: acceptable 48 / unacceptable 48
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- List A/Bは全ターゲットで相補的
- 各リストは48ターゲットを1回ずつ提示
- 各リスト内で同一条件の連続は最大3試行
- ターゲットPV形は全センテンス内で検出可能
- ターゲットPV形は全項目で第3語以降に出現
- 文長は全項目で5から10語の範囲内
- 機械検証上の問題: 0件

## スコア分布

| スコア | ターゲット数 |
|---:|---:|
| 100 | 5 |
| 92 | 1 |
| 91 | 2 |
| 90 | 7 |
| 88 | 5 |
| 86 | 5 |
| 85 | 1 |
| 84 | 3 |
| 81 | 1 |
| 80 | 18 |

要約:

- 平均: 86.08
- 中央値: 86
- 最小: 80
- 最大: 100
- 90点以上: 15/48
- 85点以上: 26/48
- 80点以上: 48/48
- 80点未満: 0/48

v1では80点未満が4ターゲット残っていたが、v2_multi_agentでは0になった。これは大きな改善である。一方で、80点ちょうどの項目が18ターゲット残っており、90点水準の完成版としてはまだ粗い。

## v2で強くなった項目

| Slot | PV | 新スコア | コメント |
|---|---|---:|---|
| cljt_010 | play out | 92 | legal event/outcome contrastにより、unacceptable文の曖昧性が大きく減った。 |
| cljt_022 | cut off | 91 | `credit line` vs `credit rating`により、同一語彙ドメイン内でPV-object fitを問える。 |
| cljt_030 | put up | 90 | `required deposit` vs `required estimate`により、display sense問題を回避した。 |
| cljt_033 | open up | 91 | appeal-domainに固定し、availability senseを測りやすくした。 |
| cljt_035 | fill in | 90 | broad topic frameを避け、substitute-for senseに切り替えた。 |
| cljt_036 | hold up | 90 | permit processとblueprint documentの差により、receipt問題を回避した。 |
| cljt_040 | come out | 90 | reveal/literal readingを避け、public stance senseに固定した。 |

## まだ90点水準に届かない主要項目

次に優先して改稿すべき項目は、80から84点に残っている項目である。

| Priority | Slot | PV | Score | 理由 |
|---:|---|---|---:|---|
| 1 | cljt_015 | put on | 80 | 多義性が強く、文脈一文でsenseを固定しにくい。 |
| 2 | cljt_019 | get off | 80 | literal/legal/escape readingsが競合しやすい。 |
| 3 | cljt_009 | get on | 80 | C1向けには易しすぎる可能性がある。 |
| 4 | cljt_023 | bring in | 80 | introduce/earn/arrestなど複数senseが残る。 |
| 5 | cljt_026 | set out | 80 | begin/explain/display sensesの競合がある。 |
| 6 | cljt_027 | break down | 80 | malfunction/analyze/emotional-collapse sensesが競合する。 |
| 7 | cljt_031 | turn around | 80 | improve/reverse/physical turningの競合がある。 |
| 8 | cljt_032 | back up | 80 | support/copy/reverse sensesの整理が必要。 |
| 9 | cljt_044 | point out | 81 | 指摘可能な対象かどうかの一般意味で解ける恐れがある。 |
| 10 | cljt_046 | follow up | 84 | object selectionが業務知識に寄る可能性がある。 |

この10項目のうち、少なくとも5項目を90点前後へ引き上げると、全体の説得力はかなり上がる。

## 査読者としての判定

v2_multi_agentの現時点の妥当性は、100点満点で88点程度である。

強み:

- 80点未満の明確なブロッカーが消えた。
- 低スコア4項目が、いずれも90点前後の候補に置き換わった。
- List A/Bの形式バランスは維持されている。
- 音声LJTとしての基本制約は満たしている。

弱み:

- 80点ちょうどの保持項目が18ターゲットあり、C1向けとしてはまだ易しい項目・多義性が残る項目が多い。
- スコアは専門家レビュー前の設計評価であり、心理測定上の難度・弁別力ではない。
- ElevenLabs録音前に、ネイティブレビューでacceptable自然さとunacceptable near-miss性を独立評価する必要がある。

次の推奨手順:

1. `put on`, `get off`, `get on`, `bring in`, `set out`, `break down`, `turn around`, `back up`, `point out`, `follow up`から5から8項目を選び、同じマルチエージェント方式で改稿する。
2. 改稿後、90点以上を20から24ターゲット程度まで増やす。
3. その後、ネイティブスピーカー3名以上によるpre-audio acceptability reviewへ進む。
4. レビューで通った項目だけをElevenLabs録音対象にする。

