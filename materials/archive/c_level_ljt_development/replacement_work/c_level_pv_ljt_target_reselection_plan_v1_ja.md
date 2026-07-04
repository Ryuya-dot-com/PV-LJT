# Cレベル向けPV-LJTターゲット再選定計画 v1

状態: 作業計画。まだproduction freezeではない。

## 目的

現行v5/v6監査で弱いと判断された17ターゲットを、CEFR C1中心の
学習者に適したPV senseへ差し替える。48項目というテスト長は維持するが、
既存48 PV formの保持は優先しない。

参照する候補表:

- `c_level_pv_ljt_replacement_candidate_pool_v1.tsv`
- `c_level_pv_ljt_design_spec_v1_ja.md`
- `c_level_pv_ljt_item_review_rubric_v1.tsv`

## 再選定の原則

1. PV formではなくPV senseを選ぶ。
2. C1学習者が知っていても、文脈内での自動化・collocation・argument
   structureが問えるsenseを優先する。
3. unacceptable文はsame-domain near-missにする。
4. 多義性が強くても、短文内でtarget senseを安定して絞れるなら候補に残す。
5. 頻度が高くても、韻律依存・literalすぎる・不可能名詞でしか落とせない
   senseは除外する。

## 差し替え優先の17ターゲット

既存v6 auditに基づき、以下はproduction poolへ直接持ち込まない。

- `give out`
- `put in`
- `take in`
- `sit back`
- `hold back`
- `come along`
- `make out`
- `get down`
- `put out`
- `clean up`
- `keep up`
- `look out`
- `look back`
- `go up`
- `go down`
- `come on`
- `come in`

## 第一候補案

| replace | primary candidate | 理由 |
|---|---|---|
| give out | turn out | prove/be discovered senseは短文で安定し、属性判断のnear-missを作りやすい |
| put in | take up | 議題・問題を扱うsenseで、会議/制度文脈のC1項目にしやすい |
| take in | figure out | understand/determine senseが安定し、問題解決文脈で作りやすい |
| sit back | step back | 物理姿勢ではなく客観的に距離を置くsenseを狙える |
| hold back | give in | 交渉・要求への譲歩senseで、韻律依存が少ない |
| come along | play out | 交渉・過程が展開するsenseでC1向け文脈を作りやすい |
| make out | sort out | 問題解決/理由把握senseで、perceptual ambiguityを避けられる |
| get down | go over | 詳細確認・検討senseで、学術/専門文脈に適する |
| put out | bring out | releaseまたはmake noticeable senseとして再設計可能 |
| clean up | throw out | 権威者による却下senseで、法的/委員会文脈を作れる |
| keep up | carry on | 継続senseは安定。ただしC1にはやや易しいためanchor候補 |
| look out | open up | 機会・アクセスが開けるsenseでabstract contextを作れる |
| look back | move on | 談話移行senseまたは困難後の前進senseで作れる |
| go up | build up | 単純な数値上昇よりprogressive accumulationを問える |
| go down | shut down | 下降senseを避け、operation停止senseへ置換 |
| come on | turn down | discourse/prosody依存を避け、拒否senseへ置換 |
| come in | take over | enter/involvementの多義性を避け、control transfer senseへ置換 |

## 予備候補

予備候補は、第一候補がexpert reviewで落ちた場合、または48項目全体の
register/source/particle balanceを整えるために使う。

- `set up`
- `take on`
- `bring up`
- `wind up`
- `go through`
- `hold up`
- `get through`
- `fill out`
- `pass on`
- `set off`
- `bring down`
- `put off`
- `come about`
- `close down`
- `fill in`
- `come around`
- `break out`
- `walk out`
- `go around`
- `come off`

## 重要な設計判断

### 1. 元の17項目と意味を対応させない

差し替えは、元のPVと意味的に似たPVを探す作業ではない。目的は48項目全体で
C1向けPV-LJTの妥当性を最大化することである。したがって、弱いtarget senseは
思い切って別のsense領域に置換する。

### 2. PHaVE rankは採用理由の一部にすぎない

PHaVE rankやsense shareは有用だが、LJTの採否は以下で決まる。

- same-domain near-missを作れるか
- alternate senseでキーが崩れないか
- TTSで韻律依存にならないか
- C1学習者にとって簡単すぎないか

### 3. primary候補もproductionではない

第一候補はまだproduction candidateではない。次に各候補について
acceptable/unacceptable文を作成し、`c_level_pv_ljt_item_review_rubric_v1.tsv`
で90点以上を取るか確認する。

## 次の具体的作業

1. 第一候補17件に対してacceptable/unacceptable sentence pairを作る。
2. 既存で維持予定の31件と合わせ、48 target senseの仮masterを作る。
3. 語数、target position、overt cue、same-domain near-miss、base verb/particle
   分布を自動監査する。
4. expert review formを作る。

