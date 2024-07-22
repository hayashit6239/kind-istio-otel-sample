# 概要
[Kind × Scaffold で手軽に継続的な開発を体験したい](https://zenn.dev/t_hayashi/articles/25fa08aada1edc)という記事のサンプルリポジトリです。

# 利用手順
上記記事を参照ください。

# リポジトリ内容
## Kind で構築するクラスター構成
コントロールプレーン 1 台とワーカー 2 台の構成です。

![f44a36909955-20240718](https://github.com/user-attachments/assets/446ace61-cd5c-4418-a2c5-a6d3ba3f0d41)

## Scaffold でデプロイするアプリケーション構成
FastAPI で作成した簡単なアプリケーションです。
リクエストを受け付ける想定の Backend for Frontend の後ろに Backend-A, Backend-B がいるような形になっています。

![f159ae7827f6-20240718](https://github.com/user-attachments/assets/88a6570b-d763-4808-8b90-3f342fde3425)

## OpenTelemetry & OpenObserve でのオブザーバビリティ検証
OpenTelemetry で計装済みなので Otel Collector と OpenObserve もデプロイしてトレースを可視化できます。

![6018a079e1d8-20240721](https://github.com/user-attachments/assets/e66d16e5-715d-4850-987b-9787111aed2a)

OpenObserve での可視化結果はこちらです。

![ad584a315b6b-20240721](https://github.com/user-attachments/assets/08cae378-9b53-4c96-a432-c2d913af35a0)

## Istio & Kiali でのサービスメッシュ検証
Istio と Prometheus と Kiali をデプロイしてトラフィックを可視化できます。

![3516d13e6dd1-20240717](https://github.com/user-attachments/assets/e97497b3-6845-4845-a357-1e4e28915664)

