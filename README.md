# モデルベースマッチング

Open3Dを用いた3Dモデルベースマッチングを一連で紹介していきます。
説明や手法の詳細をだいぶ割愛してるので、適宜調査してね。


## 導入
1. **Dockerfileをビルドしてイメージを作成**（数十分かかるのでコーヒーでも飲みながら）

    ```terminal
    $ ./build-docker-image.sh
    ```

2. **イメージからコンテナ作成 ＆ Run**

    ```terminal
    $ ./run-docker-container.sh
    ```

3. **実行やらなんやらする**

    ubuntu 18.04の環境に切り替わるので、`pip3 list`でopen3d 0.8.0が入ってることを確認する。
    `python3 check.py`や`python3 icp.py`でモデルベースマッチングのサンプルコードを実行する。

4. **終わったらexit**

5. **コンテナは止まってないので、コンテナを止める**

    ```terminal
    $ ./stop-docker-container.sh
    ```


## ダウンサンプリング
点群データを等間隔など、何らかの規則性に基づいて間引く手法。

点群データは、生のままだと情報量が多すぎて不必要に処理を重くすることがあります。

全体の3次元幾何構造の意味を失わずに点群数を減らすことがしばしば求められます。

以下の実装では、ボクセルダウンサンプリングという手法によって間引こうと思います。

```py
x = 30.
voxel_size = np.abs((target.get_max_bound() - target.get_min_bound())).max() / x
```

> 点群を1/x程度に粗くするサイズ (ダウンサンプリングするサイズに相当)

```py
source_down = source.voxel_down_sample(voxel_size)
target_down = target.voxel_down_sample(voxel_size)
```

> ダウンサンプリング処理

---
## 法線推定
CGではモデルの表面・平面(テクスチャや形状等)が既知な為、それを元に法線が算出できます。

しかし点群データでは、ただの点っていう情報しか無いが為に、どの点とどの点がどの様に平面を張ってるかが分からない状態です。

法線推定は、点群情報から「表面・平面の特徴を掴もう！」とするような手法と思ってくれたら、一時的に幸せになれます。

以下の実装では、色々ある内の、KDTreeSearchParamhybridという法線推定アルゴリズムを用いて推定してみます。

```py
 source_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 30))
 target_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 30))
```

> KDTreeSearchParamHybridアルゴリズムを用いて推定

---
## 特徴量計算
ダウンサンプリングされた点群と、法線推定の情報を用いて特徴量を算出する。

以下の実装では、色々ある内の、FPFH特徴量を用いています。

[FPFHの紹介があるやつ](http://isl.sist.chukyo-u.ac.jp/Archives/Nagoya-CV-PRML-2015March-Hashimoto.pdf)

```py
source_fpfh = o3d.registration.compute_fpfh_feature(source_down, o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 100))
target_fpfh = o3d.registration.compute_fpfh_feature(target_down, o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 100))
```

> FPFH特徴量の計算処理

---
## RANSACによるGlobal Registration
点群の位置合わせパラメータ推定をRANSACによって行う。

以下の実装では、Point-To-PointアルゴリズムをベースにRANSACする。

### RANSAC

外れ値を含むデータから、外れ値の影響を除外して、ある数式モデルのパラメータを調整する手法

今回の数式モデルは、以下で説明するPoint-To-PointやPoint-To-Planeの式に該当します。


**Point-To-Point**

対応点同士の距離の2乗和が最も小さくなるように、RとT(回転並進行列)を推定する手法

<div style="text-align: center;">

$argminE = \sum_{i=1}^{n} || P_{ti} - (RP_{si} + T) ||^2$

</div>

**Point-To-Plane**

対応する点へのベクトルとPtの法線の内積が最も小さくなるようにRとTを推定する手法

<div style="text-align: center;">
    
$argminE = \sum_{i=1}^{n} || N_{ti}・(P_{ti} - (RP_{si} + T)) ||^2$

</div>

```py
o3d.registration.registration_ransac_based_on_feature_matching(source_down, target_down,
            source_fpfh, target_fpfh,
            distance_threshold,
            o3d.registration.TransformationEstimationPointToPoint(), 4,
            [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)],
            o3d.registration.RANSACConvergenceCriteria(max_iteration = 400000, max_validation = 5000))
```

> Point-To-Pointベースで、400000回だけRANSACを回す処理

---
## ICPによるRefinement

```py
est_ptpln = o3d.registration.TransformationEstimationPointToPlane()
criteria = o3d.registration.ICPConvergenceCriteria(max_iteration = 50)
distance_threshold = voxel_size

o3d.registration.registration_icp(source, target, distance_threshold, result_ransac.transformation, est_ptpln, criteria)
```

> ICPによるRefinement処理



