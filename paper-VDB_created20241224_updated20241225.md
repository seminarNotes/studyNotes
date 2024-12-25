아래 논문은 Variational Discriminator Bottleneck (VDB)라는 새로운 접근 방법을 소개하였고, 기존 변분 기법을 GAN과 모방 학습(Imitation Learning) 등에 확장하였다. 

- Title : Variational Discriminator Bottleneck: Improving Imitation Learning, Inverse RL, and GANs by Constraining Information Flow.
- Authors : Xue Bin Peng, Angjoo Kanazawa, Sam Toyer, Pieter Abbeel, Sergey Levine
- arXiv ID: arXiv:1810.00821
- Submitted: October 1, 2018 (v1), Last Revised: August 25, 2020 (v4)
---
# Abstract

**Adversarial learning methods have been proposed for a wide range of applications, but the training of adversarial models can be notoriously unstable.** Effectively balancing the performance of the generator and discriminator is critical, since a discriminator that achieves very high accuracy will produce relatively uninformative gradients. **In this work, we propose a simple and general technique to constrain information flow in the discriminator by means of an information bottleneck.** By enforcing a constraint on the mutual information between the observations and the discriminator’s internal representation, we can effectively modulate the discriminator’s accuracy and maintain useful and informative gradients. We demonstrate that our proposed variational discriminator bottleneck (VDB) leads to significant improvements across three distinct application areas for adversarial learning algorithms. Our primary evaluation studies the applicability of the VDB to imitation learning of dynamic continuous control skills, such as running. **We show that our method can learn such skills directly from raw video demonstrations, substantially outperforming prior adversarial imitation learning methods.** The VDB can also be combined with adversarial inverse reinforcement learning to learn parsimonious reward functions that can be transferred and re-optimized in new settings. Finally, we demonstrate that VDB can train GANs more effectively for image generation, improving upon a number of prior stabilization methods.

- Adversarial learning methods have been proposed for a wide range of applications, but the training of adversarial models can be notoriously unstable. (적대적 학습(adversarial learning) 방법은 다양한 응용 분야에서 제안 되어 왔지만, 학습은 매우 불안정해 질 수 있다)
- In this work, we propose a simple and general technique to constrain information flow in the discriminator by means of an information bottleneck. (이 연구에서 정보 병목(information bottleneck)을 사용해서 판별자(discriminator) 내의 정보 흐름을 제한하는 일반적인 기법을 제안한다.)
- We show that our method can learn such skills directly from raw video demonstrations, substantially outperforming prior adversarial imitation learning methods. (제안된 방법은 비디오 시연에서 직접 학습할 수 있고, 기존 적대적 모방 학습 방법을 상당히 능가하는 것을 보여준다.)
# 1. Introduction
# 2. Related Work
# 3. Preliminaries

## Standard Framework
데이터 셋 ${x_{i}, y_{i}}$가 주어졌다고 하자. label $y_{i}$를 feature $x_{i}$에 대해 standard maximum likelihood estimation $q(y_{i}|x_{i})$은 아래와 같은 최적화 문제에 의해 결정된다.

$$ \min_{q} E_{x,y \sim p(x,y)}[- \log q(y|x)]$$

하지만, 이 접근 방식은 과적합(overfitting)과 데이터의 잡음에 민감하다는 한계점이 존재한다.

## Information Bottleneck
Alemi et al. (2016)은 Information Bottleneck을 사용해서 위 문제를 해결하려고 했다. 이 방법은 먼저 입력값 $x$과 잠재변수 $z$ 사이의 상호 정보 $I(X,Z)$를 제어하는 encoder $E(z|x)$를 소개하는 것으로 시작된다. 이 방법은 $x$에서 중요 정보만 $z$로 전달하도록 제어하는 것으로 상호 정보의 상한 $I_{c}$에 대해 $I(X,Z) \leq I_{c}$를 만족시켜, 잠재변수 $z$가 $x$의 모든 정보를 복사하지 못하도록 제약한다.

아래와 같은 목적 함수를 정의한다.

$$ J(q, E) = \min_{q, E} E_{x, y \sim p(x, y}[ E_{z \sim E(z|x)}[- \log q(y|z)] ] $$
$$ \text{subject to } I(X,Z) \leq I_{c}$$

여기서,
- $E(z|x)$ : 입력 $x$를 잠재공간 $z$로 매핑하는 인코더(Encoder)
- $q(y|z)$ : $z$를 기반으로 $y$를 예측하는 모델
- $I(X,Z)$ : x와 z 사이의 상호 정보

한편, 상호 정보 $I(X, Z)$는 $X$와 $Z$ 간의 상관성을 측정하는 함수로, 아래와 같이 정의된다.

$$
I(X,Z) = \int p(x,z) \log \frac{p(x, z)}{p(x)p(z)} dx dz
$$

위 식을 정리하면,

$$
I(X, Z) = \int p(x) E_{z \sim E(z|x)} \left[ \log \frac{E(z|x)}{p(z)} \right] dx
$$

인데, 일반적으로, $p(z) = \int E(z|x)p(x)dx$를 직접 계산하는 것은 매우 어렵다. 대신에, variational lower bound는 잠재 변수의 분포 $p(z)$를 근사하는 $r(z)$를 정의하고, KL divergence의 성질에 의해 아래와 같은 부등식을 만족한다.

$$
KL[p(z) \Vert r(z)] = \int p(z) \log \frac{p(z)}{r(z)} dz \geq 0
$$

정리 하면,

$$
\int p(z) \log p(z) dz \geq \int p(z) \log r(z) dz
$$

을 만족한다. 이제 이 부등식을 이용해서 $I(X,Z)$의 상한을 게산하자.

$$
I(X,Z)= \int p(x) E_{z \sim E(z|x)} \left[ \log \frac{E(z|x)}{p(z)} \right] dx \leq \int p(x) E(z|x) \log \frac{E(z|x)}{r(z)} dz dx
$$

그리고, 이 식은 KL divergence에 의해 근사되고, 아래오 같이 표현된다.

$$
I(X,Z) \leq E_{x \sim p(x)} [KL[E(z|x) \Vert r(z)]]
$$

요약하면, 위에서 정의한 최적화 문제에서 contraint를 위해 $p(z)$를 계산하기엔 feasible하지 않아, 다른 upper 조건을 활용하여, 새로운 contraint를 얻었다. 이것을 이용하여 아래와 같이 다시 최적화 문제를 정의한다.

$$ \tilde{J}(q, E) = \min_{q, E} E_{x, y \sim p(x, y}[ E_{z \sim E(z|x)}[- \log q(y|z)] ] $$
$$ \text{subject to } E_{x \sim p(x)} [KL[E(z|x) \Vert r(z)]] \leq I_{c}$$

이제 위 최적화 문제를 해결하기 위해, Lagrange Multiplier $\beta$를 사용해서 아래와 같은 문제로 변환한다.

$$
\min_{q, E} E_{x, y \sim p(x, y}[ E_{z \sim E(z|x)}[- \log q(y|z)] ] + \beta (E_{x \sim p(x)} [KL[E(z|x) \Vert r(z)]] - I_{c})
$$

# 4. Variational Discriminator Bottle

이 section에서는 기존 GAN 구조에 Variational Information Bottleneck(VIB)을 적용해서 Variational Discriminator Bottleneck(VDB)라는 새로운 방법을 제시한다. 해당 방법은 GAN의 Discriminator를 개선하는 데 중점을 두고 있다.

먼저, standard GAN framework부터 생각해보자. GAN은 discriminator $D$와 generator $G$가 존재해서, discriminator $D$는 목표 데이터 분포 $p*(x)$의 샘플 데이터와 generator $G(x)$으로부터 생성된 가상 샘플 데이터를 정확하게 구분하는 것을 목표로 한다.

$$
\max_{G} \min_{D} E_{x \sim p*(x)}[- \log (D(x))] + E_{x \sim G(x)}[- \log (1-D(x)]
$$

여기에 discriminator $D$에 encoder $E$를 도입해서 샘플 데이터 $x$를 확률적 인코딩 $z \sim E(z|x)$로 매핑하는 Variational Information Bottleneck을 통합하고, 원래 특징 $X$와 encoding $Z$ 간의 상호정보 $I(X,Z)$에 constraint $I_{c}$를 적용한다. 이 후, discriminator $D$는 encoder 분포로부터 추출된 샘플을 분류하도록 학습된다. 이에 대략적인 그림은 아래와 같다.

![image](https://github.com/user-attachments/assets/b6681f27-fb53-4c89-93f0-db68f4af26e5)

discriminator를 위한 정규 목표 함수 $J(D,E)$는 아래 식과 같이 주어진다.

$$
J(D,E) = \min_{D,E} E_{x \sim p*(x)} [ E_{z \sim E(z|x)} [- \log (D(z))] ] + E_{x \sim G(x)}[ E_{z \sim E(z|x)} [- \log (1 - D(z))]]
$$

$$
\text{subejct to } E_{x \sim \tilde{p}(x)} [KL[E(z|x) \Vert r(z)]] \leq I_{c}
$$

여기서, $\tilde{p} = \frac{1}{2} p* + \frac{1}{2}G $은 목표 데이터 분포와 generator의 평균이다. 논문에서는 이 부분을 regularizer as the variational discriminator bottleneck (VDB)라 한다. 이 목표 함수를 최적화 하기 위해 Lagrange multiplier $\beta$를 도입하여, 아래와 같이 최적화 문제로 변환한다.

$$
J(D,E) = \min_{D,E} \max_{\beta \geq 0} E_{x \sim p*(x)} [ E_{z \sim E(z|x)} [- \log (D(z))] ] + E_{x \sim G(x)}[ E_{z \sim E(z|x)} [- \log (1 - D(z))]] + \beta( E_{x \sim \tilde{p}(x)} [KL[E(z|x) \Vert r(z)]] - I_{c})
$$

Section 4.1. 또 다시 언급되고, 실험 단계에서 보여줄 결과이지만, $x$와 $z$ 사이에 구체적인 상호 정보 제약을 가하는 것은 더 좋은 성능을 내기 위해 아주 중요하다. 그래서 논문에서는 상호 정보 $I_{c}$에 대한 특정 제약을 적용하기 위해서 이중 경사 하강법(dual gradient descent)를 통해 $\beta$를 업데이트한다.


$$ D, E \text{ are updated by } \arg \min_{D, E} L(D, E, \beta) $$

$$ \beta \text{ is updated by } \max(0, \beta + \alpha_{\beta}(E_{x \sim \tilde{p}(x)} [KL[E(z|x) \Vert r(z)]] - I_{c})) $$

여기서, $L(D, E, \beta)$은 Lagrangian으로, 아래 식과 같이 정의되고,

$$
L(D, E, \beta) = E_{x \sim p*(x)} [ E_{z \sim E(z|x)} [- \log (D(z))] ] + E_{x \sim G(x)}[ E_{z \sim E(z|x)} [- \log (1 - D(z))]] + \beta( E_{x \sim \tilde{p}(x)} [KL[E(z|x) \Vert r(z)]] - I_{c})
$$

$\alpha_{\beta}$은 dual gradient descent에서 dual variable을 위한 stepsize를 의미한다.

논문에서 소개하고 있는 실험에서는 사전 분포 $r(z)$은 평균이 $0$이고, identity matrix $I$를 공분산으로 갖는 표준 gaussian distribution $N(0, I)$로 모델링된다. Encoder $E(z|x) = N(\mu_{E}(x), \Sigma_{x}(x))$는 잠재 변수 $Z$에 대해 평균이 $\mu_{E}(x)$이고, 공분산 행렬이 $\Sigma_{x}(x)$인 Gaussian Disbritubition을 모델링한다. 다시 말해, Encoder는 실제 데이터 $x$를 기반으로 잠재 변수 $z$의 확률 분포를 학습한다. KL loss를 계산할 때, 두 분포의 균형을 맞추는 것이 GAN의 안정적인 학습을 위해 필수적이기 때문에 각 데이터 배치(batch)는 실제 데이터 분포 $p*(x)$와 생성 데이터 분포 $G(x)$에서 동일한 개수의 샘플을 포함한다. generator를 위해 아래와 같은 단순화된 목적 함수를 사용한다.

$$
\max_{G} E_{x \sim G(x)} [- \log (1 - D(\mu_{E}(x)))]
$$

여기서 KL loss는 discriminator와 encoder의 정규화에만 사용되고, generator는 KL 제약을 받지 않는다. 이것은 generator의 학습 비중을 줄이고, 효율적으로 진짜 데이터를 생성하도록 유도하기 위한 설계이다. 또한, 논문은 실험 단계에서 $Z$ 전체에 걸친 기댓값을 계산하는 대신, encoder의 분포의 평균 $\mu_{E}(x)$에서 $D$를 평가하여 기대값을 근사화하는 것이 작업에 충분하고, 이를 통해 계산 비용을 줄이고 실험적으로 성능에 큰 영향을 미치지 않는다는 것을 언급한다. 마지막으로, discriminator는 간단한 linear-sigmoid 구조를 통해 계산 효율성을 높이고, $z$와의 상호작용을 단순화한다.

$$
D(z) = \sigma(w_{D}^{T}z + b_{D})
$$

# Reference 
[1] Peng, Xue Bin, et al. "Variational Discriminator Bottleneck: Improving Imitation Learning, Inverse RL, and GANs by Constraining Information Flow." *arXiv preprint arXiv:1810.00821* (2018).

---

# A. Prior Knowledge 

## GAN (Gernative Adversarial Network)
GAN은 생성자(Genertor)와 판별자(Discriminator)라는 두 개의 신경망이 경쟁적으로 학습하는 구조를 의미한다. 생성자는 데이터를 생성하고, 판별자는 생성된 데이터가 진짜(real)인지 가짜(fake)인지 판별한다. GAN의 목표는 생성자가 판별자를 속일 수 있을만큼 진짜 같은 데이터를 생성하는 것이다.

GAN의 학습은 아래 최적화 문제로 정의된다.

$$min_{G}[max_{D} [V(D,G)]]$$

여기서 $V(D, G)$는 생성자 $G$와 판별자 $D$ 간의 목표 함수이고,

$$ V(D, G) = E_{x \sim p_{data}(x)} [log D(x)] + E_{z \sim p_{z}(z)} [log(1 - D(G(z)))]$$

이다. 여기서,

- $D(x)$ : 판별자가 입력 $x$이 진짜 데이터일 확률을 출력
- $G(z)$ : 생성자가 잠재 변수 $z$에서 생성한 데이터
- $p_{data}(x)$ : 실제 데이터 분포
- $p_{z}(z)$ : 생성자의 입력으로 사용되는 잠재 공간(latent space)의 분포

### Generator  
생성자는 잠재 변수 $z$ ~ $p(z)$로부터 진짜 데이터와 유사한 데이터를 생성하는 역할을 한다. 목표는 판별자를 속여서 $D(G(z))$를 높이는 것이다. 생성자의 손실 함수는 판별자가 생성한 데이터 $G(z)$를 진짜로 분류하게 만드는 것을 목표로 한다.

$$ L_{G} = - E_{z}[logD(G(z))] $$

### Discriminator
판별자는 입력 데이터가 진짜(real)인지 가짜(fake)인지 구별하는 역할을 한다. 생성자가 학습할 수 있는 신호(gradient)를 제공한다. 판별자는 이진 분류를 수행하므로 출력값은 확률 $D(x) \in [0,1]$이다.
판별자의 손실 함수는 진짜 데이터에 대해 높은 확률($D(x) = 1$)을 출력하고, , 가짜 데이터에 대해 낮은 확률($D(x) = 0$)을 출력하는 것을 목표로 한다.

$$ L_{D} = -(E_{x \sim p_{data}(x)} [log D(x)] + E_{z \sim p_{z}(z)} [log(1 - D(G(z)))]) $$

## VAE (Variational Autoencoder)
VAE은 확률적 생성 모델로, 데이터의 분포를 명시적으로 학습한다. VAE는 입력 데이터를 저자치원의 잠재 공간에 매핑하고, 이 잠재 변수에서 데이터를 재구성한다. 이 과정에서 확률 분포를 학습하여 데이터 생성 및 표현을 가능하게 한다.

- 인코더(Encoder) : 입력 데이터 $x$를 잠재 변수 $z$의 확률 분포 $q(z|x)$로 매핑
- 디코드(Decoder) : 잠재 변수 $z$에서 원래 데이터를 복원하도록 $p(x|z)$를 학습

VAE의 학습 목표는 변분 추론(Variational Inference)을 통해 입력 데이터 $x$의 잠재 변수 $z$를 학습하는 것이다. 
데이터의 가능도를 최대화 하기 위해 아래와 같은 손실 함수를 최적화 한다.

$$ log p(x) \geq  E_{x \sim p_{data}(x)} [log p(x|z)] - KL(g(z|x) \Vert p(z)) $$

여기서 

- $p(x|z)$ : 디코더가 $z$를 기반으로 $x$를 복원하는 확률 분포
- $q(z|x)$ : 인코더가 $x$로부터 $z$의 분포를 학습
- $KL(g(z|x) \Vert p(z))$ : $g(z|x)$과 잠재 공간의 사전 분포 $p(z)$ 간의 Kullback-Leibler diverge
