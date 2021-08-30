# 検索例１：<主語>-<述語>を指定して<目的語>を取得する
## 例1-1）「大阪電気通信大学(Q7105556)」（主語）の「位置する行政区(P131)」（述語）となる目的語（?o）を取得する　
```
select ?o
where{
    <http://www.wikidata.org/entity/Q7105556>  <http://www.wikidata.org/prop/direct/P131> ?o .
}
```
[クエリを実行](https://w.wiki/aMq)

## 例1-2）「大阪電気通信大学(Q7105556)」（主語）の「設立(P571)」（述語）となる目的語（?o）を取得する　
```
select ?o
where{
    <http://www.wikidata.org/entity/Q7105556>  <http://www.wikidata.org/prop/direct/P571> ?o .
}
```
[クエリを実行](https://w.wiki/aMs)

## 例1-1+）「大阪電気通信大学(Q7105556)」（主語）の「位置する行政区(P131)」（述語）となる目的語（?o）を取得する【＋名称（ラベル）も合わせて取得する】　
```
select ?o ?label
where{
    <http://www.wikidata.org/entity/Q7105556>  <http://www.wikidata.org/prop/direct/P131> ?o .
    ?o <http://www.w3.org/2000/01/rdf-schema#label> ?label . #名称の取得
    FILTER(lang(?label)="ja")     # 名称の言語を日本語(ja)に限定
}
```
[クエリを実行](https://w.wiki/aMz)

## 例1-3）「大阪電気通信大学(Q7105556)」（主語）の「位置する行政区(P131)」（述語）となる目的語（?o）を取得する【＋名称（ラベル）も合わせて取得する】　
```
select ?o ?label ?o2
where{
    <http://www.wikidata.org/entity/Q7105556> <http://www.wikidata.org/prop/direct/P131> ?o .
    <http://www.wikidata.org/entity/Q7105556> <http://www.wikidata.org/prop/direct/P571> ?o2 .
    ?o <http://www.w3.org/2000/01/rdf-schema#label> ?label . #名称の取得
    FILTER(lang(?label)="ja")     # 名称の言語を日本語(ja)に限定
}
```
[クエリを実行](https://w.wiki/aN7)



# 検索例２：<主語>-<述語>を指定して<目的語>を取得する
## 例2-1）「位置する行政区（P131）」（述語）が「寝屋川市（Q389633）」（目的語）となる「主語（?s）」の一覧を取得する　　
```
select ?s
where{
    ?s  <http://www.wikidata.org/prop/direct/P131> <http://www.wikidata.org/entity/Q389633> .
}
LIMIT 100
```
[クエリを実行](https://w.wiki/aMv)

## 例2-1+）「位置する行政区（P131）」（述語）が「寝屋川市（Q389633）」（目的語）となる「主語（?s）」の一覧を取得する【名称あり】　　
```
select ?s ?label
where{
    ?s  <http://www.wikidata.org/prop/direct/P131> <http://www.wikidata.org/entity/Q389633> .
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER(lang(?label)="ja")
}
LIMIT 100
```
[クエリを実行](https://w.wiki/aNP)


## 例2-2）「分類（instance-of）（P31）」（述語）が「大学 （Q389633）」（目的語）となる「主語（?s）」+名称の一覧を取得する　　
```
select ?s ?label
where{
  ?s  <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q3918> .
  ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
  FILTER(lang(?label)="ja")
} LIMIT 100

```
[クエリを実行](https://w.wiki/aNQ)

## 例2-2+）「分類（instance-of）（P31）」（述語）が「大学 （Q389633）」（目的語）となる「主語（?s）」+名称（※あれば…）の一覧を取得する　　
```
select ?s ?label
where{
  ?s  <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q3918> .
  OPTIONAL{
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER(lang(?label)="ja")
  }
} LIMIT 100
```
[クエリを実行](https://w.wiki/aNS)

# より複雑な検索例
## 例3）集約（グループ化）とカウントを利用したランキング
- 分類(P31)が大学(Q3918)となる主語(?s)と，その主語(?s)の国(P17)の目的語(?country)を取得する．
- さらに，取得した結果を目的語(?country)が同一のもので集約(グループ化)し，
- それぞれのグループに含まれる主語(?s)の数をカウントする．
- その結果「国ごとの大学の数のランキング」を取得できる．　　
```
select ?country ?label  (count(?s) AS ?c) 
where{
    ?s <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q3918>  .
    ?s <http://www.wikidata.org/prop/direct/P17> ?country .
   OPTIONAL{
     ?country <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
     FILTER(lang(?label)="ja")
     }
} GROUP BY ?country ?label
ORDER BY DESC(?c) 
```
[クエリを実行](https://w.wiki/aNU)










