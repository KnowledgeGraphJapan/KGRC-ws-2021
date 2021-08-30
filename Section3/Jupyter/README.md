ここにおいてある jupyter notebook を実行するには kotlin kernel が必要です。

https://github.com/Kotlin/kotlin-jupyter を参照して、conda または pip でご自身の環境に合わせて kotlin kernel をインストールしてください。
また この kotlin kernel, notebook を実行するためには JDK 11 （以上）が必要です。

```
% sudo apt install openjdk-jdk-11
% git clone https://github.com/KnowledgeGraphJapan/KGRC-ws-2021.git
% pip install kotlin-jupyter-kernel
% cd KGRC-ws-2021/Section3
% jupyter notebook
```
Windows 10 のWSLなどで動作確認を行っています。
