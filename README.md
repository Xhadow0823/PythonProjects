# Python FP-growth

### 目前進度
+ generated all $freqItemSets$
+ found a way to calc. the $confidence$ of item
+ limited the recursive under level 5
+ generate all $AssociationRules$
+ Finish all requires UwU

### 目前問題
+ Level 2 以上的數量會浮動(已找到問題) p.s. 找總務!! (已解決)
+ 時間問題已改善但有待驗證  (真的滿快的)


#### To-do-list
- 製作專案報告
- 找時間開會簡報


---
# 報告摘要

## 程式碼撰寫流程
+ 參考資源: 
    + [Apriori演算法](https://medium.com/marketingdatascience/%E4%BD%A0%E6%80%8E%E9%BA%BC%E8%99%95%E7%90%86%E9%A1%A7%E5%AE%A2%E4%BA%A4%E6%98%93%E8%B3%87%E8%A8%8A-apriori%E6%BC%94%E7%AE%97%E6%B3%95-1523b1f8443b)
    + [Associating Rule 關聯式法則應用— Apriori & FP-Growth](https://medium.com/@tinahuang_4101/associating-rule-%E9%97%9C%E8%81%AF%E5%BC%8F%E6%B3%95%E5%89%87%E6%87%89%E7%94%A8-apriori-fp-growth-3ab46deeeb77)
    + [Association rule learning-Wikipedia](https://en.wikipedia.org/wiki/Association_rule_learning#Apriori_algorithm)
+ 演算法理解: *參考網站清單*
+ 改良程式碼
+ 增加程式碼功能
+ 改善演算效率
+ 

## 原始版本問題
+ $FP-tree$ 結構不穩定
+ 遞迴深度過深
+ 運算效率不佳
+ $FrequentItemSet$資料結構不實用
+ 原始版本沒有生成$AssociationRule$的功能

## 問題解決辦法
- $FP-tree$結構不穩定原因:
    - $dataSet$的排序方式不穩定
    - 對策: 以$tuple$方式增加比較項目
- 改善遞迴深度過深:
    - 對策: 在$mineTree$過程中呼叫遞迴時加入限制: 當此次遞洄的$preFix$引數長度小於4時
- 運算效率不佳原因
- 改善$FrequentItemSet$資料結構:
    - 為了使計算$confidence$的過程更加快速，將原本的`list(freqItem)` 改為`{frozenset(freqItem):item出現次數}`
- 生成$AssociationRule$的功能:
    - 實作函式 `AllAssRul(freqSet)` 計算所有$AssociationRule$數量