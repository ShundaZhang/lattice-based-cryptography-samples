# Lattice-Based Cryptography 学习指南与 Python Samples

这个仓库是一份面向入门到进阶的格基密码学学习材料。它包含：

- 系统学习路线：从整数格、困难问题、LLL/BKZ，到 LWE、SIS、NTRU、ML-KEM、ML-DSA 和全同态加密。
- 初学者数学基础：补齐向量、矩阵、点积、范数、行列式、模运算、噪声这些必要前置知识。
- 图形化解释：用 SVG 和 Mermaid 图说明格、好基/坏基、基本域、SVP/CVP/BDD、LWE 解密阈值。
- 概念与应用清单：帮助你把数学对象、算法、密码构造和真实系统联系起来。
- 纯 Python 示例：不用第三方依赖，直接运行小规模 LLL、Toy LWE 加密/解密、Tiny LWE 暴力攻击。
- 习题与答案：45 道题，覆盖计算题、证明思路题、实现题和安全直觉题。

> 安全提示：本仓库里的密码代码都是教学 toy implementation，参数极小，也没有常数时间实现、KEM transform、拒绝采样、侧信道防护或生产级随机数处理。不要用于任何真实安全场景。

## 快速开始

```bash
python3 --version
python3 examples/01_lattice_basics.py
python3 examples/02_lll_reduction.py
python3 examples/03_toy_lwe_encrypt.py
python3 examples/04_tiny_lwe_attack.py
python3 -m unittest discover -s tests
```

如果你想把它作为本地包安装：

```bash
python3 -m pip install -e .
```

## 仓库结构

```text
.
├── assets/
│   ├── attacker-vs-user.png
│   ├── fundamental-domain.svg
│   ├── good-vs-bad-basis.svg
│   ├── lattice-basis.svg
│   ├── lattice-core-intuition.png
│   ├── lwe-noise-intuition.png
│   ├── lwe-decoding.svg
│   ├── lwe-samples.svg
│   └── svp-cvp-bdd.svg
├── docs/
│   ├── applications.md       # 应用场景与真实标准
│   ├── answers.md            # 习题答案
│   ├── concepts.md           # 核心概念清单
│   ├── exercises.md          # 习题
│   ├── intuitive-explanation.md # 最通俗的核心原理解释
│   ├── learning-guide.md     # 8 周学习路径
│   ├── math-primer.md        # 初学者数学基础
│   └── visual-guide.md       # 图形化概念解释
├── examples/
│   ├── 01_lattice_basics.py
│   ├── 02_lll_reduction.py
│   ├── 03_toy_lwe_encrypt.py
│   └── 04_tiny_lwe_attack.py
├── lattice_crypto/
│   ├── attacks.py
│   ├── integer_lattice.py
│   ├── lll.py
│   └── lwe.py
└── tests/
    └── test_lattice_crypto.py
```

## 一句话理解

格基密码学使用高维离散格上的困难问题构造密码系统。典型困难问题包括 SVP、CVP、SIS、LWE、Ring-LWE、Module-LWE 和 NTRU 相关问题。它的重要性来自两点：

1. 很多格问题在高维下没有已知高效经典或量子算法。
2. 格结构能支持丰富构造：KEM、公钥加密、数字签名、身份基加密、属性基加密、全同态加密和零知识证明。

## 初学者推荐顺序

如果你是第一次学 lattice-based cryptography，建议按这个顺序走：

1. 看推荐视频，先建立图像直觉。
2. 读 [docs/intuitive-explanation.md](docs/intuitive-explanation.md)，先用最通俗的话理解“没钥匙难，有钥匙易”。
3. 读 [docs/math-primer.md](docs/math-primer.md)，补线性代数和模运算。
4. 读 [docs/visual-guide.md](docs/visual-guide.md)，用图理解格、基、SVP/CVP/BDD 和 LWE。
5. 跑 `examples/01_lattice_basics.py` 和 `examples/02_lll_reduction.py`。
6. 读 [docs/concepts.md](docs/concepts.md)，把术语串起来。
7. 跑 `examples/03_toy_lwe_encrypt.py` 和 `examples/04_tiny_lwe_attack.py`。
8. 做 [docs/exercises.md](docs/exercises.md)，再对照 [docs/answers.md](docs/answers.md)。

## 推荐 YouTube 视频

首推：

[Lattice-based cryptography: The tricky math of dots](https://youtu.be/QDdOoYdb748)

推荐理由：

- 时长短，适合第一次接触。
- 图形化解释强，重点讲 basis vectors、同一个格的多组基、SVP、CVP 和 GGH 加密直觉。
- 先建立“点阵 + 好基/坏基 + 最近点困难”的画面感，再读 LWE/Module-LWE 会轻松很多。

如果你想系统补课，再看 Alfred Menezes 的公开课程：

[Lattice-Based Cryptography - Cryptography 101](https://cryptography101.ca/lattice-based-cryptography/)

## 必须掌握的概念地图

### 数学基础

- 向量空间、内积、范数、矩阵、行列式。
- 整数模运算、有限环、多项式环。
- 格：由整数线性组合生成的离散点集。
- 格基：同一个格可以有很多组基，好基短且近似正交，坏基长且倾斜。
- 基本域与行列式：衡量格点密度。
- Gaussian heuristic：估计随机格最短向量长度的经验规则。

### 计算问题

- SVP：找非零最短格向量。
- CVP：找离目标点最近的格点。
- BDD：目标点保证离某个格点很近时的 CVP 变体。
- uSVP：最短向量明显唯一的 SVP 变体。
- SIS：找短整数向量 `x`，使 `A x = 0 mod q`。
- LWE：从带噪声线性方程中恢复 secret 或区分随机样本。
- Ring-LWE / Module-LWE：把 LWE 放到多项式环或模块结构中，提高效率并得到紧凑密钥。
- NTRU：基于多项式环中的短向量和近似商结构的经典格密码体系。

### 算法工具

- 枚举：低维精确找短向量。
- LLL：多项式时间格基规约算法，输出近似短且较正交的基。
- BKZ：块规约算法，现代格攻击和安全估计的核心。
- Babai nearest plane：用规约后的基近似解 CVP/BDD。
- Primal attack / dual attack：分析 LWE 安全性的两类常见思路。

### 密码构造

- Regev LWE 公钥加密。
- GPV trapdoor 与格基签名。
- NTRU 加密与 NTRU 格签名。
- Kyber / ML-KEM：基于 Module-LWE/Module-LWR 风格的 KEM。
- Dilithium / ML-DSA：基于 Module-LWE/SIS 风格的签名。
- Falcon / FN-DSA：基于 NTRU lattice 与高斯采样思想的签名。
- GSW/BGV/BFV/CKKS：常见格基全同态加密路线。

## 应用场景

- 抗量子密钥交换和 KEM：TLS、VPN、服务间通信、长期保密数据保护。
- 抗量子数字签名：软件包签名、固件签名、证书、区块链账户。
- 全同态加密：加密数据库查询、隐私机器学习、云上密文计算。
- 隐私计算：安全聚合、联邦学习、私有集合相关协议。
- 密码分析：用 LLL/BKZ 攻击弱参数 RSA、背包密码、ECDSA nonce 泄漏、Hidden Number Problem。
- 高级密码：属性基加密、身份基加密、函数加密、零知识证明中的格承诺。

## 推荐学习路径

1. 第 1 周：线性代数、模运算、整数格定义，跑 `01_lattice_basics.py`。
2. 第 2 周：SVP/CVP/BDD 与格基质量，手工枚举二维短向量。
3. 第 3 周：LLL 算法，跑 `02_lll_reduction.py`，理解 size reduction 和 Lovasz 条件。
4. 第 4 周：SIS 与 LWE，推导 LWE 加密正确性，跑 `03_toy_lwe_encrypt.py`。
5. 第 5 周：攻击视角，跑 `04_tiny_lwe_attack.py`，体会参数维度为什么重要。
6. 第 6 周：Ring-LWE、Module-LWE、NTRU，多项式环 `Z_q[x]/(x^n + 1)`。
7. 第 7 周：PQC 标准，学习 ML-KEM、ML-DSA、Falcon/FN-DSA 的设计取舍。
8. 第 8 周：全同态加密与隐私计算，理解噪声增长、bootstrapping、CKKS 近似计算。

更完整的路线见 [docs/learning-guide.md](docs/learning-guide.md)。

## 图形化导览

最通俗的核心原理解释见 [docs/intuitive-explanation.md](docs/intuitive-explanation.md)，配有三张 AI 风格概念图：

- 高维点阵里的最近点
- 攻击者视角和合法用户视角
- LWE 的线性方程与小噪声

核心图解见 [docs/visual-guide.md](docs/visual-guide.md)，包括：

- 二维格和基向量
- 好基与坏基
- 基本域和 determinant
- SVP / CVP / BDD
- LWE 样本生成
- Toy LWE 解密阈值
- LWE 加密数据流
- LLL 工作循环
- KEM 接口

## 习题入口

- 习题：[docs/exercises.md](docs/exercises.md)
- 答案：[docs/answers.md](docs/answers.md)

## 官方标准参考

- NIST FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard, ML-KEM。
- NIST FIPS 204: Module-Lattice-Based Digital Signature Standard, ML-DSA。
- NIST FIPS 205: Stateless Hash-Based Digital Signature Standard, SLH-DSA。它不是格基方案，但属于 NIST PQC 签名标准组合。

## 公开学习资料

- [A Gentle Introduction to Lattice-Based Cryptography](https://cryptography101.ca/wp-content/uploads/2026/02/Lattice-cryptgraphy.pdf)，Alfred Menezes 的入门讲义。
- [Lattice-Based Cryptography - Cryptography 101](https://cryptography101.ca/lattice-based-cryptography/)，视频、讲义和 slides，覆盖 SIS、LWE、lattices、Ring/Module 结构。
- [CSE 599: Lattices and Lattice-based Cryptography](https://courses.cs.washington.edu/courses/cse599s/22sp/)，华盛顿大学课程页面，适合进阶参考。
- [Lattice Based Cryptography for Beginners](https://eprint.iacr.org/2015/938)，IACR ePrint 上面向初学者的讲义。
- [A quick introduction to Lattice Cryptography](https://cjeudy.github.io/videos/a_quick_intro_to_lattice_cryptography)，短视频配套页面，适合快速获得整体景观。
- [NIST PQC FIPS approval](https://csrc.nist.gov/News/2024/postquantum-cryptography-fips-approved)，NIST 后量子标准官方公告。

## 学习建议

不要先追求把生产级 Kyber 或 Dilithium 从头实现出来。更稳的路线是：

1. 先能用二维、三维格画出和算出短向量。
2. 再能手写 LLL 的关键步骤。
3. 然后用 toy LWE 解释正确性、安全性和参数失败。
4. 最后阅读标准文档和参考实现，补齐常数时间、采样、压缩、序列化、KEM transform 等工程细节。
