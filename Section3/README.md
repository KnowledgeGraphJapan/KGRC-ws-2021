# これまでに作成されてきたデータ、オントロジー

## 主語, 動詞, 目的語の3つ組データ（まだらの紐）: 東京都市大学 勝島修平さん作成
* http://challenge.knowledge-graph.jp/submissions/2019/katsushima/knowledge_graph_data.xlsx

```
Holmes,come,coach	
Holmes,come,garden_of_Roylott	
Julia,come,bedroom_of_Helen	
```

## Wikidata を用いたオントロジー
* https://github.com/takanori-ugai/KGRCOntology
```
<http://kgc.knowledge-graph.jp/data/SpeckledBand/fear> a fjs:basic_emotion .
fjs:basic_emotion  rdfs:label "basic emotion"@en .
fjs:basic_emotion  a rdfs:Class .
fjs:basic_emotion  rdfs:seeAlso <http://www.wikidata.org/entity/Q16748867> .
fjs:basic_emotion rdfs:subClassOf fjs:emotion .
fjs:emotion a rdfs:Class .
fjs:emotion rdfs:label "emotion"@en .
```
```
<http://kgc.knowledge-graph.jp/data/SpeckledBand/bed>  rdfs:subClassOf fjs:furniture .
fjs:furniture a rdfs:Class .
fjs:furniture rdfs:label "furniture"@en .
<http://kgc.knowledge-graph.jp/data/SpeckledBand/bed>  rdfs:subClassOf fjs:sleeping_place .
fjs:sleeping_place a rdfs:Class .
fjs:sleeping_place rdfs:label "sleeping place"@en .
```

## 殺害手段オントロジー
* https://github.com/KGChallenge/Challenge/blob/master/Means/KnowledgeGraph/root-ontology_modify2.ttl
```
<http://kgchallenge.github.io/ontology/毒殺> rdf:type owl:Class ;
    rdfs:subClassOf <http://kgchallenge.github.io/ontology/殺害方法> ,
    [ rdf:type owl:Restriction ;
      owl:onProperty <http://kgchallenge.github.io/ontology/hasSymptom> ;
      owl:someValuesFrom <http://kgchallenge.github.io/ontology/嘔吐>
    ] ,
    [ rdf:type owl:Restriction ;
    owl:onProperty <http://kgchallenge.github.io/ontology/hasSymptom> ;
    owl:someValuesFrom <http://kgchallenge.github.io/ontology/めまい>
    ] ,
    [ rdf:type owl:Restriction ;
    owl:onProperty <http://kgchallenge.github.io/ontology/hasSymptom> ;
    owl:someValuesFrom <http://kgchallenge.github.io/ontology/青白い>
    ] ,
    [ rdf:type owl:Restriction ;
    owl:onProperty <http://kgchallenge.github.io/ontology/hasSymptom> ;
    owl:someValuesFrom <http://kgchallenge.github.io/ontology/震え>
    ] ;
    rdfs:label "PoisonKilling"@en , "毒殺"@ja .
    
kd:beDizzy a kgcf:めまい .
kd:turnPale a kgcf:青白い .
```

## SHACLによる動機付け：動機がある人に HasMotivation のタイプを付与する
* https://github.com/KGChallenge/Challenge/blob/master/Motivation/KnowledgeGraph/InferenceMotivation.ttl
```
# お金を失う可能性のある人
sh:LoseMoneyMotivation
  a sh:NodeShape ;
  sh:targetClass kgc:Person ;
  sh:order 2 ;
  sh:rule [
    a sh:SPARQLRule ;
    sh:construct """
      PREFIX kgc: <http://kgc.knowledge-graph.jp/ontology/kgc.owl#>
      PREFIX kd: <http://kgc.knowledge-graph.jp/data/SpeckledBand/>
      PREFIX kgcf: <http://kgchallenge.github.io/ontology/#> 
      PREFIX kdf: <http://kgchallenge.github.io/data/#> 
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
      CONSTRUCT {
        $this kgcf:hasMotivation kdf:greed_for_money ;
	      kgcf:want_to_kill ?target .
      } WHERE {  
        VALUES ?lose_pred {kd:give kd:pay kd:lose} .
        VALUES ?get_pred {kd:have} .
        ?subclass_of_scene rdfs:subClassOf kgc:Scene .
        
        {
          ?_ kgc:subject $this ;
             kgc:hasPredicate ?lose_pred ;
             kgc:what kd:money ;
             kgc:if ?if .
        } UNION {
          ?__ kgc:whom $this ;
              kgc:hasPredicate ?get_pred ;
              kgc:what kd:money ;
              kgc:if ?if .
        }
	      # ?if の先がsituationである
        # situation が 未来の要素なら←これは何らかのsituationからifで参照されていればいい？
        # 誰かが死ぬことで未来のsituationが起きる条件を満たさないならば
        # その人がターゲット # 条件を壊すのは人とは限らないけど...
        {
          ?if a ?subclass_of_scene ;
              kgc:subject ?target .
        } UNION {
          ?if a ?subclass_of_scene ;
              kgc:whom ?target .
        }
      }
      """ ;
  ] .
```

## 動機、手段タグ付き文：青空文庫で公開されているアーサー・コナン・ドイルの、23の短編小説
* https://github.com/okajima-s/kgc2018-fllml/blob/master/src/data/train.tsv
* 使用例：https://github.com/okajima-s/kgc2018-fllml/blob/master/src/20181125_kgc_FLL-ML_program.pdf
