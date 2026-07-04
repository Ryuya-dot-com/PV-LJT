# Cレベル向けPhrasal Verb LJT 48項目マスター: 全体バランス監査 v1

作成日: 2026-07-04

本監査は、`c_level_pv_ljt_48_target_master_v1.tsv`、`c_level_pv_ljt_list_A_v1.tsv`、`c_level_pv_ljt_list_B_v1.tsv`、`c_level_pv_ljt_list_assignment_v1.tsv`を対象とする。目的は、C1中心の高熟達度学習者向けphrasal verb LJTとして、48ターゲット・複数リスト設計を維持したまま、形式的制約と内容上の弱点を整理することである。

## 生成方針

48ターゲットは、元の`pv_001`から`pv_048`のスロット順を維持して構成した。

- v6から保持した項目: 31ターゲット
- v2置換ペアから差し替えた項目: 17ターゲット
- 各ターゲット: acceptable 1文 + unacceptable 1文
- 全体: 48ターゲット、96文
- List A: 48試行
- List B: 48試行
- List A/Bは各ターゲットについて相補的条件を提示する

なお、v6の既存リストファイルでは`pv_030 put up`が`reserve_not_listed`としてA/Bリストから漏れていた。このv1マスターでは48スロットを維持するために暫定的に含めたが、品質上は「置換または大幅改稿」扱いとする。

## 形式検証

以下の機械チェックは通過した。

- マスター行数: 96
- ターゲット数: 48
- マスター内条件: acceptable 48 / unacceptable 48
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- List A/Bの条件は全ターゲットで相補的
- 各リストは48ターゲットを1回ずつ提示
- 各リスト内で同一条件の連続は最大3試行
- ターゲットPV形は全センテンス内で検出可能
- ターゲットPV形は全項目で第3語以降に出現
- 文長は全項目で5から10語の範囲内

形式面では、音声LJT化の前提条件を満たしている。

## 品質スコア分布

スコアは、v2置換項目についてはCレベル用ルーブリックに基づく自己採点、v6保持項目についてはpre-audio auditの下位評定を同ルーブリック重みに換算した推定値である。したがって、現時点では心理測定的な難度・弁別力ではなく、改稿優先順位として扱う。

| スコア | ターゲット数 |
|---:|---:|
| 100 | 5 |
| 90 | 3 |
| 88 | 5 |
| 86 | 5 |
| 85 | 1 |
| 84 | 6 |
| 81 | 1 |
| 80 | 18 |
| 78 | 1 |
| 76 | 2 |
| 61 | 1 |

要約:

- 平均: 84.19
- 中央値: 84
- 最小: 61
- 最大: 100
- 90点以上: 8/48
- 85点以上: 19/48
- 80点以上: 44/48
- 80点未満: 4/48

90点レベルの完成版を目指す場合、このv1マスターは「形式面は合格、内容面はまだ暫定」である。とくに、80点台前半の項目が多く、C1向けの精密な語彙意味判断としてはネイティブレビュー前の改稿余地が大きい。

## 最優先で直す項目

| Slot | 元PV | 現PV | Score | 判定 | 主な問題 |
|---|---|---|---:|---|---|
| cljt_030 | put up | put up | 61 | 置換または大幅改稿 | v6時点で`reserve_not_listed`。`put up the brochure`が十分に不自然ではない。 |
| cljt_022 | cut off | cut off | 76 | 大幅改稿 | 同一ドメイン近接ミスマッチとして弱く、一般的な意味判断で解ける恐れがある。 |
| cljt_035 | look back | fill in | 78 | 大幅改稿 | `chair`が具体物すぎて、PV意味アクセスではなく粗い目的語異常で判断される。 |
| cljt_040 | come out | come out | 76 | 大幅改稿 | reveal senseとliteral/person-subject readingsの制御が不安定。 |

この4項目は、パイロット前に必ず差し替えまたは再設計すべきである。

## 次点で改稿する項目

80から84点の項目は、形式的には使用可能だが、90点水準には届いていない。主な対象は以下である。

| Slot | 現PV | Score | 改稿理由 |
|---|---|---:|---|
| cljt_001 | break off | 80 | unacceptable文が「提案を中断する」という解釈を完全に排除できるか要確認。 |
| cljt_002 | hand over | 80 | custody/control transferとしての目的語制限をさらに精密化したい。 |
| cljt_009 | get on | 80 | C1学習者にはやや容易な可能性がある。 |
| cljt_010 | play out | 84 | `agreement played out in public`が文脈により許容される可能性がある。 |
| cljt_011 | stand out | 84 | 目立つ対象の選択が一般意味で処理される恐れがある。 |
| cljt_012 | pull back | 80 | `approval`とのミスマッチが抽象的で、レビューが必要。 |
| cljt_013 | run out | 80 | stock/resource cueが強く、C1には容易な可能性がある。 |
| cljt_014 | turn over | 80 | literal/transfer/read-throughの競合を確認する必要がある。 |
| cljt_015 | put on | 80 | 多義性が強く、音声一文でsenseを固定できるか要確認。 |
| cljt_016 | take back | 80 | retract/returnのsense競合に注意。 |
| cljt_018 | pay off | 80 | loan/debt payoff以外のbenefit senseをブロックする必要がある。 |
| cljt_019 | get off | 80 | literal movement/legal escapeなどのsense競合がある。 |
| cljt_020 | turn up | 80 | appear/increase/volume senseの競合を要確認。 |
| cljt_023 | bring in | 80 | introduce/earn/arrestなど多義性が残る。 |
| cljt_026 | set out | 80 | begin/explain/display sensesの競合を要確認。 |
| cljt_027 | break down | 80 | malfunction/analyze/lose control sensesの競合を要確認。 |
| cljt_028 | reach out | 84 | contact senseは明確だが、C1では易しすぎる可能性がある。 |
| cljt_031 | turn around | 80 | improve/reverse/physical turningの競合を要確認。 |
| cljt_032 | back up | 80 | support/copy/reverse sensesを整理する必要がある。 |
| cljt_033 | open up | 84 | `opened up objections`が完全なnear-missとして安定するか要確認。 |
| cljt_034 | take out | 80 | obtain service/document senseとremove/date sensesの競合を要確認。 |
| cljt_036 | hold up | 84 | `receipt`も遅延可能なため、unacceptable文が不安定。 |
| cljt_041 | bring about | 80 | cause senseは明確だが、結果名詞との相性に注意。 |
| cljt_044 | point out | 81 | 「指摘できる対象」の一般意味で判断される恐れがある。 |
| cljt_046 | follow up | 84 | follow-up objectの制限がややタスク一般知識に寄る可能性がある。 |

## 現時点で比較的強い項目

85点以上の19ターゲットは、優先的にネイティブレビューへ回せる。

| Slot | 現PV | Score | 備考 |
|---|---|---:|---|
| cljt_003 | set up | 90 | 置換v2。created entity contrastが強い。 |
| cljt_004 | take up | 88 | 置換v2。agenda/discussion objectの制御が比較的良い。 |
| cljt_005 | put off | 88 | 置換v2。delayable objectの制御が比較的良い。 |
| cljt_006 | take on | 90 | 置換v2。responsibility objectの制御が強い。 |
| cljt_007 | give in | 86 | 置換v2。pressure sourceの制御が明確。 |
| cljt_008 | move up | 100 | ranking contrastが明確。 |
| cljt_017 | sort out | 86 | 置換v2。resolve-problem senseとして比較的良い。 |
| cljt_021 | pass on | 86 | 置換v2。information-transfer sense。 |
| cljt_024 | bring out | 86 | 置換v2。release/publication senseを要固定。 |
| cljt_025 | throw out | 86 | 置換v2。reject-object sense。 |
| cljt_029 | set off | 88 | 置換v2。trigger-event sense。 |
| cljt_037 | shut down | 88 | 置換v2。operation objectの制御が比較的良い。 |
| cljt_038 | turn down | 88 | 置換v2。reject offer/request sense。 |
| cljt_039 | take over | 90 | 置換v2。control/responsibility objectが強い。 |
| cljt_042 | carry out | 100 | task/execution senseが安定。 |
| cljt_043 | rule out | 100 | exclude-possibility senseが安定。 |
| cljt_045 | sum up | 100 | summarize senseが安定。 |
| cljt_047 | lay out | 100 | present/explain structure senseが安定。 |
| cljt_048 | work out | 85 | solve/calculate senseとして概ね使用可能。 |

## 複数リスト設計上の評価

List A/Bの形式的バランスは良好である。

- 各リスト48試行
- 各リスト24 acceptable / 24 unacceptable
- 各ターゲットはA/Bで逆条件
- 同一条件の連続は最大3試行
- 元スロット・元PV・現PV・置換元の追跡が可能

ただし、内容面のバランスは未完成である。v2置換項目は比較的強いが、v6保持項目の多くが80点前後で、C1向けLJTとしては「答えがPV意味アクセスに依存する」水準をさらに高める必要がある。

## 査読者としての判定

この48項目マスターv1は、研究実施用の最終版ではなく、ネイティブレビューとパイロット用改稿のための暫定統合版である。

採点するなら、現時点の妥当性は100点満点で82点程度である。形式設計はかなり整ったが、C1向けとしては、80点前後の項目が多すぎる。90点レベルに近づけるには、まず4つの低スコア項目を置換し、その後80から84点の保持項目を5から8個程度重点改稿する必要がある。

次の推奨手順:

1. `put up`, `cut off`, `fill in`, `come out`を最優先で差し替えまたは大幅改稿する。
2. `play out`, `hold up`, `open up`を含む84点以下の項目をネイティブレビュー前に再設計する。
3. 改稿後に、List A/Bの24/24条件均衡とターゲット位置制約を再検証する。
4. ネイティブレビューでは、各ペアについて「acceptable文の自然さ」と「unacceptable文のnear-miss性」を独立に評価させる。
5. ElevenLabs録音は、少なくとも低スコア4項目と84点以下の改稿が終わるまで保留する。

