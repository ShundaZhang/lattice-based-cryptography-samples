# 8 周学习路径

这条路线假设你已经会一点 Python，但不默认你熟悉格或后量子密码。如果你数学基础比较强，可以把前两周压缩；如果你更偏工程背景，建议不要跳过手算和 toy code。

建议第一天先做三件事：

1. 看 README 中推荐的 YouTube 视频，先建立图像直觉。
2. 读 [math-primer.md](math-primer.md)，补齐向量、矩阵、点积、范数、行列式和模运算。
3. 读 [visual-guide.md](visual-guide.md)，把格、好基/坏基、SVP/CVP/BDD、LWE 样本和解密阈值看成图。

## 第 0 阶段：准备知识

目标：

- 会算向量内积、范数、矩阵乘法和行列式。
- 理解模 `q` 的加法、乘法和逆元。
- 熟悉 Python list、tuple、dataclass、itertools。

阅读：

- [math-primer.md](math-primer.md)
- [visual-guide.md](visual-guide.md)

练习：

- 手算 `mod 17` 下 `3 * x = 1` 的解。
- 写一个函数计算两个整数向量的点积。
- 完成 [exercises.md](exercises.md) 的 1-12 题。

## 第 1 周：整数格和几何直觉

学习内容：

- 格的定义。
- 格基不唯一。
- 基本域和 determinant。
- 二维格点枚举。

代码：

```bash
python3 examples/01_lattice_basics.py
```

你应该能回答：

- 为什么 `(2, 0), (0, 2)` 和 `(2, 2), (0, 2)` 可能生成不同形状但相关的格？
- 为什么短基更适合做近似最近点？

## 第 2 周：SVP、CVP、BDD

学习内容：

- SVP：找非零最短格向量。
- CVP：找离目标点最近的格点。
- BDD：目标点离某个格点足够近时的解码问题。

动手：

- 在二维格里枚举系数 `[-3, 3]`，找短向量。
- 尝试把一个目标点投影到最近格点。
- 完成 [exercises.md](exercises.md) 的 13-24 题。

思考：

- 为什么低维枚举可行，高维枚举不可行？
- 为什么“近似”问题也足够构造安全系统？

## 第 3 周：LLL 规约

学习内容：

- Gram-Schmidt 正交化。
- size reduction。
- Lovasz condition。
- LLL 的输出质量。

代码：

```bash
python3 examples/02_lll_reduction.py
```

你应该能解释：

- LLL 为什么不一定找出最短向量？
- 规约后的基为什么更适合 Babai nearest plane？

## 第 4 周：SIS 和 LWE

学习内容：

- SIS 的短解困难性。
- LWE 样本 `(a, <a,s> + e mod q)`。
- search-LWE 和 decision-LWE。
- LWE 加密正确性：噪声必须小于解码阈值。

代码：

```bash
python3 examples/03_toy_lwe_encrypt.py
```

你应该能推导：

```text
v - <s, u> = bit * floor(q/2) + small_noise mod q
```

练习：

- 完成 [exercises.md](exercises.md) 的 25-36 题。

## 第 5 周：攻击视角和参数直觉

学习内容：

- 维度 `n`、样本数 `m`、模数 `q`、噪声大小之间的关系。
- 暴力搜索为什么只适合 tiny 参数。
- LWE 的 primal attack 和 dual attack 粗略直觉。
- BKZ block size 与攻击成本。

代码：

```bash
python3 examples/04_tiny_lwe_attack.py
```

思考：

- 为什么 `q^n` 会迅速爆炸？
- 增大噪声为什么既能提高安全性，又可能造成解密失败？

## 第 6 周：Ring-LWE、Module-LWE 和 NTRU

学习内容：

- 多项式环 `Z_q[x]/(x^n + 1)`。
- 卷积乘法和 NTT。
- Ring-LWE 的效率与结构假设。
- Module-LWE 的折中。
- NTRU 的短多项式和反元素。

建议阅读：

- Kyber/ML-KEM 的高层设计。
- Dilithium/ML-DSA 的高层设计。
- Falcon/FN-DSA 的 NTRU lattice 和高斯采样思想。

## 第 7 周：真实标准和工程实现

学习内容：

- ML-KEM：KEM API、压缩、NTT、多项式采样、CCA 安全。
- ML-DSA：challenge、response、拒绝采样、hint。
- Falcon/FN-DSA：NTRU trapdoor、高斯采样、浮点实现风险。
- 常数时间和 side-channel。

动手：

- 读一个成熟参考实现，不急着重写。
- 给 toy code 写测试，故意调大噪声观察失败率。
- 完成 [exercises.md](exercises.md) 的 37-45 题。

## 第 8 周：FHE 与隐私计算

学习内容：

- LWE/RLWE 型加密的噪声增长。
- leveled FHE 与 bootstrapping。
- BFV/BGV/CKKS 的适用场景。
- 同态乘法为什么比同态加法更贵。

动手：

- 用一个 FHE 库跑 CKKS 向量加法和乘法。
- 解释 scale、rescale、modulus chain 的作用。

## 后续项目建议

1. 给本仓库加入多项式环模块，实现 negacyclic convolution。
2. 写一个 tiny Ring-LWE 加密样例。
3. 实现一个小型 NTRU keygen/encrypt/decrypt，并观察参数失败。
4. 写一个 LWE 参数扫描脚本，统计不同噪声下的解密失败率。
5. 阅读 ML-KEM 标准，画出 keygen、encaps、decaps 数据流。
