# 核心概念清单

## 1. 整数格

给定线性无关向量 `b1, ..., bn`，它们生成的格是：

```text
L(B) = { z1*b1 + z2*b2 + ... + zn*bn | zi in Z }
```

矩阵 `B` 的行或列可以看作格基。本仓库代码统一把基向量当作矩阵的行。

同一个格有无穷多组基。好基一般短且接近正交，坏基通常很长、很倾斜。许多格算法的目标就是把坏基规约成较好的基。

## 2. 基本域与行列式

基本域是基向量张成的平行多面体。满秩格的行列式等于基本域体积：

```text
det(L) = |det(B)|
```

行列式越小，单位体积内格点越密。许多安全估计会把维度、行列式和最短向量估计联系起来。

## 3. 最短向量问题 SVP

SVP 要找格中非零最短向量：

```text
find v in L, v != 0, minimizing ||v||
```

精确 SVP 在高维很难。密码学通常依赖近似版本或相关问题的困难性。

## 4. 最近向量问题 CVP

CVP 给定目标点 `t`，找最近格点：

```text
find v in L minimizing ||t - v||
```

CVP 通常比 SVP 更难。Babai nearest plane 是一个经典近似算法，它依赖较好的格基。

## 5. 有界距离解码 BDD

BDD 是 CVP 的特殊情形：目标点保证离某个格点足够近。LWE 解密可以看作一种带结构的 BDD：密文含有接近某个格点的噪声扰动，私钥帮助把它解码回来。

## 6. LLL 规约

LLL 是 Lenstra、Lenstra、Lovasz 提出的多项式时间格基规约算法。它通过两类操作改善基：

- size reduction：让后面的基向量减少在前面基向量方向上的投影。
- Lovasz condition：如果局部顺序不够好，就交换相邻基向量。

LLL 不能保证找到真正最短向量，但在密码分析和数论计算中非常有用。

## 7. BKZ 规约

BKZ 可以看作更强的块版本 LLL。它每次在一个维度为 `beta` 的块内调用 SVP oracle 或枚举算法。`beta` 越大，规约越强，成本也越高。现代格密码安全估计常讨论攻击者能承受多大的 BKZ block size。

## 8. SIS

SIS，Short Integer Solution，给定随机矩阵 `A in Z_q^{n x m}`，找一个短向量 `x` 使得：

```text
A x = 0 mod q
```

SIS 常用于哈希、承诺、签名方案。直觉上，模方程容易有很多解，但要求解很短会变难。

## 9. LWE

LWE，Learning With Errors，给定样本：

```text
(a_i, b_i = <a_i, s> + e_i mod q)
```

其中 `s` 是 secret，`e_i` 是小噪声。任务是恢复 `s`，或判断这些样本和均匀随机样本是否可区分。

噪声是 LWE 的灵魂：

- 没有噪声时，就是普通线性方程组。
- 噪声太小时，容易被攻击。
- 噪声太大时，解密容易失败。

## 10. Ring-LWE 与 Module-LWE

LWE 的矩阵很大。Ring-LWE 把向量和矩阵结构放进多项式环，例如：

```text
Z_q[x] / (x^n + 1)
```

Module-LWE 位于普通 LWE 和 Ring-LWE 之间，保留较高效率，同时避免过强的环结构假设。ML-KEM 和 ML-DSA 都使用 module-lattice 风格结构。

## 11. NTRU

NTRU 使用多项式环中的短多项式和卷积乘法。它历史很长、速度快，也启发了 Falcon/FN-DSA 这类基于 NTRU lattice 的签名。

## 12. KEM

KEM，Key Encapsulation Mechanism，不直接加密任意长消息，而是封装一个共享密钥：

```text
keygen -> pk, sk
encaps(pk) -> ciphertext, shared_secret
decaps(sk, ciphertext) -> shared_secret
```

现代混合加密通常用 KEM 建立对称密钥，再用 AEAD 加密数据。

## 13. 数字签名

格基签名常见路线：

- Fiat-Shamir with aborts：Dilithium/ML-DSA 的核心风格。
- hash-and-sign with trapdoor：GPV/Falcon 思想相关。
- SIS 派生签名：签名是满足公开关系的短向量。

## 14. 全同态加密

全同态加密允许在密文上计算。格基 FHE 的核心主题包括：

- 噪声增长。
- 模数切换。
- relinearization。
- bootstrapping。
- BFV/BGV 适合精确整数或模运算。
- CKKS 适合近似实数和机器学习推理。

