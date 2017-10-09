## これらの結果を生んだNCTM概要
- len(tags) = len(Coordinates) = 98534 
- K = 100
- alpha = 0.1
- beta= 0.1
- gamma= 0.1
- eta = 1.0
- max_iter = 1000

つまるところ， `goodtags.csv`，`goodCoords.csv`にあるデータをそのままNCTMにぶち込んでいる.
このままだとsample数が増やせない(時間の都合により)ので，さらに絞って結果をみる必要がある.

ちなみに今生成されているデータを見てみると，タグはやはりうまく分かれていない．
