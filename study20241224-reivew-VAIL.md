
# Abstract

**Adversarial learning methods have been proposed for a wide range of applications, but the training of adversarial models can be notoriously unstable.** Effectively balancing the performance of the generator and discriminator is critical, since a discriminator that achieves very high accuracy will produce relatively uninformative gradients. **In this work, we propose a simple and general technique to constrain information flow in the discriminator by means of an information bottleneck.** By enforcing a constraint on the mutual information between the observations and the discriminator’s internal representation, we can effectively modulate the discriminator’s accuracy and maintain useful and informative gradients. We demonstrate that our proposed variational discriminator bottleneck (VDB) leads to significant improvements across three distinct application areas for adversarial learning algorithms. Our primary evaluation studies the applicability of the VDB to imitation learning of dynamic continuous control skills, such as running. **We show that our method can learn such skills directly from raw video demonstrations, substantially outperforming prior adversarial imitation learning methods.** The VDB can also be combined with adversarial inverse reinforcement learning to learn parsimonious reward functions that can be transferred and re-optimized in new settings. Finally, we demonstrate that VDB can train GANs more effectively for image generation, improving upon a number of prior stabilization methods.

- Adversarial learning methods have been proposed for a wide range of applications, but the training of adversarial models can be notoriously unstable. (적대적 학습(adversarial learning) 방법은 다양한 응용 분야에서 제안 되어 왔지만, 학습은 매우 불안정해 질 수 있다)
- In this work, we propose a simple and general technique to constrain information flow in the discriminator by means of an information bottleneck. (이 연구에서 정보 병목(information bottleneck)을 사용해서 판별자(discriminator) 내의 정보 흐름을 제한하는 일반적인 기법을 제안한다.)
- We show that our method can learn such skills directly from raw video demonstrations, substantially outperforming prior adversarial imitation learning methods. (제안된 방법은 비디오 시연에서 직접 학습할 수 있고, 기존 적대적 모방 학습 방법을 상당히 능가하는 것을 보여준다.)
# 1. Introduction
# 2. Related Work
# 3. Preliminaries



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
