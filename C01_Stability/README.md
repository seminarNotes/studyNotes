# Stability
<p align="right">
최초 작성일 : 2024-12-11 / 마지막 수정일 : 2025-01-07
</p>

## 1. Stability 

제어 공학에서 선형 시불변 시스템(Linear Time-Invariant)는 아래와 같이 기술된다.

$$\dot{x}(t) = Ax(t) + Bu(t)$$
$$y(t) = Cx(t) + Du(t)$$

시스템 행렬 $A$는 상태 행렬, $B$는 입력 행렬, $C$는 출력 행렬, $D$는 직접 전달 행렬, $x(t)$는 상태 변수, $y(t)$는 출력 변수이다. 그러면, Laplace 변환과 행렬 연산을 통해 입력과 출력의 관계를 결정하는 전달함수 $G(s)$는 상태 방정식으로부터 아래와 같이 유도된다.

$$G(s) = C(sI - A)^{-1}B + D$$

이러한 이유로, 방정식 $\text{det}(sI - A)$의 해, 즉, 행렬 $A$의 고유값이 시스템의 특징을 결정하는 중요한 변수로 작용한다.

시스템에서 안정성이라고 하는 것은 여러 관점이 있다. 상태 변수 $x(t)$가 어느 정도 유계 될 수 있는지, 수렴할 수 있는지, 어느 정도의 속도로 수렴할 수 있는지 등이다. 아래 글에서 다루고자 하자는 안정성은 상태 변수가 $0$으로 수렴하는가에 대한 것이고, 점근적 안정성(asymptotic stability)라고 한다.

$$\lim_{t \to \infty} x(t) = 0$$

시스템이 안정적인지 확인하기 위해서는 상태 변수 $x(t)$가 $0$으로 수렴하는지 확인해야한다. 다시 말해, 시스템의 안정성과 상태변수 수렴성은 대응된다. 초기값을 $x(0)=0$이라 가정했을 때, 위 상태 방정식의 해는 

$$\int_{0}^{t} e^{A(t-s)}Bu(s)ds$$

로 계산된다. 따라서, 행렬 $A$에 의해 상태변수의 수렴성이 결정되기 때문에, 행렬 $A$를 분석하는 것이 중요하다. 이 작업은 상태 방정식과 상태 방정식의 해가 연속 시간 시스템 일 경우와 이산 시간 시스템일 경우가 다르다. 먼저, 연속 시간 시스템에 대해 알아본다.

## 2. Hurwitz 안정성 기준(연속 시간 시스템)

### 2-1. 고유값을 이용한 시스템 안정성 판별

시스템의 상태 방정식과 출력 방정식이 아래와 같이 주어졌다고 가정하자.

$$
\begin{align*}
\dot{x}(t) & = A x(t) + B u(t) \\
y(t) & = C x(t) + D u(t)
\end{align*}
$$

위 두 개의 방정식은 각각 아래와 같은 해를 갖는다.

$$
\begin{align*}
x(t) & = e^{At} x_0 + \int_0^t e^{A(t-\tau)} B u(\tau) \, d\tau \\
y(t) & = C \left( e^{At} x_0 + \int_0^t e^{A(t-\tau)} B u(\tau) \, d\tau \right) + D u(t)
\end{align*}
$$

시스템의 안정성이라는 것은 직관적으로, 상태 변수 $x(t)$와 출력 변수 $y(t)$가 시간이 지남에 따라 발산하지 않는다는 것, 즉, 상수로 수렴하거나 적당한 구간에 의해 유계인 것을 의미한다. 두 변수 $x(t)$, $y(t)$의 수렴성을 결정하는 것은 행렬 지수 함수(matrix exponential) $e^{At}$이고, 따라서, 앞서 언급했던 것과 동일하게 시스템의 안정성은 결국 행렬 지수 함수 $e^{At}$의 수렴성에 의해 결정되고, 이것은 행렬 $A$와 관련이 있다. 아래에서는 행렬 $A$가 어떤 조건을 가질 때, 시스템이 안정적인지를 생각해본다. 계산 편의상 상태 방정식은 아래와 같이 제한한다.

$$
\dot{x}(t) = Ax(t)
$$

행렬 $A$에 따라 행렬 지수 함수 $e^{At}$의 수렴성을 결정하기 위해, 먼저 함수의 정의를 써보자.

$$
e^{At} = \sum_{k \geq 0} \frac{(At)^k}{k!}
$$

여기서, 만약 행렬 $A$가 대각화 가능하다(diagonalizable)면, 행렬 $A$는 

$$
A = V\Lambda V^{-1}
$$

이고, 행렬 지수 함수의 정의에 대입을 하면,

$$
e^{At} = Ve^{\Lambda t}V^{-1}
$$

대각행렬 $\Lambda$의 지수 함수 $e^{\Lambda t}$는 아래와 같다.

$$
e^{\Lambda t} =
\begin{bmatrix}
e^{\lambda_1 t} & 0 & \cdots & 0 \\
0 & e^{\lambda_2 t} & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & e^{\lambda_n t}
\end{bmatrix}
$$

여기서, $\lambda_1, \lambda_2, \ldots, \lambda_n$은 행렬 $A$의 고유값이다. 따라서, 이를 통해 알 수 있는 사실은 선형 시스템 $\dot{x}(t) = Ax(t)$이 안정적이다라는 것과 행렬 $A$의 고유값의 실수부가 모두 음수인 것(All eigenvalues of $A$ have negative real parts)은 동치인 것이다. 그래서, 시스템의 상태 행렬 중 위와 같이 모든 eigenvalue의 실수부가 음수인 행렬을 Hurwtiz 행렬이라 한다.

$$ A\text{ is Hurwitz if Re }\lambda_{i}(A) < 0\text{ for all }i $$

만약 $A$가 대각화가 되지 않는 행렬이라고 하자. 그러면 행렬 $A$를 Jordan form으로 표현할 수 있다.

$$
A = PJP^{-1}
$$

여기서, $J$는 Jordan Blocks으로 이루어진 블록 대각 행렬이다.

$$
J =
\begin{bmatrix}
J_1 & 0 & \cdots & 0 \\
0 & J_2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & J_k
\end{bmatrix}
$$

그리고, 각각의 Jordan Block $J_{i}$은 행렬 $A$의 eigenvalue을 성분으로 한다.

$$
J_i =
\begin{bmatrix}
\lambda_i & 1 & 0 & \cdots & 0 \\
0 & \lambda_i & 1 & \cdots & 0 \\
\vdots & \vdots & \ddots & \ddots & 0 \\
0 & 0 & \cdots & \lambda_i & 1 \\
0 & 0 & \cdots & 0 & \lambda_i
\end{bmatrix}
$$

따라서, 대각화 가능한 행렬과 동일하게 행렬 지수 함수 $e^{At}$의 수렴성은 $A$의 eigenvalue에 의해 결정된다.

### 2-2. LMI을 이용한 시스템 안정성 판별

앞에서 알아본 내용에 따르면, 시스템에 포함되어 있는 행렬 $A$의 고유값을 계산함으로써, 아래와 같은 동치 조건으로 손쉽게 시스템의 안정성을 판단할 수 있다.

$$ \dot{x}(t) = Ax(t)\text{ is stable if and only if }A\text{ is Hurwitz} $$

하지만, 계산 과학에서 행렬 $A$의 고유값을 계산하는 것은 상당히 복잡도가 높고, 계산량이 많은 작업이다. 그래서, 고유값을 통해 시스템의 안정성을 판단하는 것은 수학적으로는 훌륭한 도구가 될 수 있지만, 계산 과학에서는 다른 대안이 필요하다. 고유값 계산보다 계산량이 적고, 동일하게 시스템의 안정성을 판단할 수 있는 또 다른 도구는 행렬 부등식(LMI, Linear Matrix Inequality)이다. LMI와 아래 동치 조건을 이용하여 더 적은 계산량을 통해 시스템의 안정성을 조사할 수 있다.

$$ A\text{ is Hurwitz if and only if there exists a }P > 0\text{ such that }A^{T}P + PA < 0 $$

**(증명)** 행렬 $A$가 Hurwitz라 가정한다. 임의의 positive definite 행렬 $Q > 0$에 대해, 행렬 $P$를 아래와 같이 쓴다면,

$$ P = \int_{0}^{\infty} e^{A^{T}s}Qe^{As} ds $$

그렇다면, 행렬 $A$는 Hurwitz이기 때문에 고유값이 모두 $0$보다 작고, 위 행렬 $P$의 수렴성이 보장된다. 또한, 행렬 $P$에 대해 integral by parts를 적용하면 아래를 얻는다.

$$PA = \int_{0}^{\infty} e^{A^{T}s}Qe^{As}A ds = \int_{0}^{\infty} e^{A^{T}s}\frac{d}{ds} e^{As} ds = -Q - \int_{0}^{\infty} A^{T} e^{A^{T}s}Qe^{As} ds = -Q - A^{T}P $$

따라서, $A$가 Hurwitz이면, 적당한 행렬 $P$가 존재해서 $PA + A^{T} P = -Q < 0$를 만족한다.

반대로, 행렬 $A$에 대해 적당한 행렬 $P >0$가 존재해서 부등식 $PA + A^{T} P < 0$을 만족한다 가정하고, 행렬 $A$에 대한 시스템이 안정적임을 확인해보자. 시스템이 안정적임을 보이는 가장 보편적인 방법은 시스템에 대응하는 Lyapunov 함수 $V(x)$을 찾아 Lyapunov 안정성 조건을 만족하는지 확인하는 것이다. $V(x) = x^{T}Px$라 두면, nonzero $x$에 대해 항상 $V(x) > 0$을 만족하고, $V(x) = 0$을 만족한다. 또한,

$$ \dot{V}(x(t)) =  \dot{x}^{T}(t)Px(t) + x^{T}(t)P\dot{x}(t) $$

이 때, 시스템 방정식 $\dot{x}(t) = Ax(t)$에 의해 식은 아래와 같이 정리된다.

$$ \dot{x}^{T}(t)Px(t) + x^{T}(t)P\dot{x}(t) = x^{T}(t) A^{T}Px(t) + x^{T}(t)PAx(t)=x^{T}(t)(A^{T}P + PA) x(t) < 0 $$

마지막 부등호는 가정에 의해 보장된다. 따라서, 해당 시스템은 전역적으로 안정적이며, 이는 행렬 $A$가 Hurwitz임을 의미한다.

## 3. Schur 안정성 기준(이산 시간 시스템)

### 3-1. 고유값을 이용한 시스템 안정성 판별


이제 이산적 모델에 대한 시스템에 대해 생각한다. 컴퓨터에 시뮬레이션이나 연산을 하는 경우, 모두 이산적으로 처리하기 때문에 이 역시 중요한 내용이다. 시스템의 상태 방정식과 출력 방정식이 아래와 같이 주어졌다고 가정하자.

$$
\begin{align*}
x_{k+1} &= A_d x_{k} + B_d u_{k} \\
y_{k} &= C_d x_{k} + D_d u_{k}
\end{align*}
$$

위 두 개의 방정식은 각각 아래와 같은 해를 갖는다.

$$
\begin{align*}
x_{k} & = A_d^k x_{0} + \sum_{i=0}^{k-1} A_d^{k-1-i} B_d u_{i} \\
y_{k} & = C_d \left( A_d^k x_{0} + \sum_{i=0}^{k-1} A_d^{k-1-i} B_d u_{i} \right) + D_d u_{k}
\end{align*}
$$

연속 시스템 모델과 유사하게, 시스템의 안정성이라는 것은 상태 변수 $x_{k}$와 출력 변수 $y_{k}$가 시간이 지남에 따라 발산하지 않는 것이므로, 두 변수의 수렴성을 결정하는 요소에 대해 생각하면 된다. 두 변수 $x_{k}$, $y_{k}$에서 수렴성을 결정 짓는 요소는 상태 행렬 $A_{d}$의 거듭 제곱 $A_d^{k}$이다. 행렬 $A_d^{k}$가 수렴하기 위해서는 행렬 $A_d$의 스펙트럴 반경(spectral radius)가 1보다 작아야 한다.

$$
\rho(A_d) = \max\{ |\lambda_1|, |\lambda_2|, \ldots, |\lambda_n| \} < 1
$$

연속 모델에서 행렬 $A$가 Hurwitz하다는 것과 대응되어 이산 모델에서는 시스템이 수렴되게 하는 상태 행렬 $A_d$을 Schur matrix라 한다.

$$ A_d\text{ is Schur if }|\lambda_{i}(A)| < 1\text{ for all }i $$

연속 모델과 이산 모델의 안정성의 조건이 다른 이유를 생각해보자. 안정성이라는 것은 결국 행렬 $A$가 누적해서 연산이 되었을 때, 상태 변수 $x(t)$가 발산하지 않아야 하는 것이다. 연속의 경우, 행렬 $A$가 상태 변수 $x(t)$의 시간에 대한 미분에 영향을 주고, 미분한 값이 음수가 되어야지만, 상태 변수는 감소하고, 시스템이 안정적임을 보장 받을 수 있다. 이러한 이유로 행렬 $A$의 고유값이 음수인 것이 요구된다. 반면에 이산 모델인 경우, 상태변수의 $x(k)$는 $x_{k} = A^{k} x_{0}$로 표현 되고, 고정된 초기값 $x_{0}$에 대해 상태변수의 수렴성은 행렬 $A$의 거듭제곱에 의해 결정된다. 따라서, 행렬 $A$의 고유값이 1보다 작아야 한다.

### 3-2. LMI을 이용한 시스템 안정성 판별

위에서 알아본 사실을 정리하면 아래 명제와 같다.

$$
x_{k+1} = A x_{k}\text{ is stable if and only if }A\text{ is Schur}
$$

 이제 연속 모델과 동일한 이유로, 고유값을 직접적으로 계산하여 시스템의 안정성을 판단하기보단 행렬 부등식을 이용하여 시스템의 안정성을 판단한는 아래와 같은 식을 제시하고 증명할 것이다.

$$ A\text{ is Schur if and only if there exists a }P > 0\text{ such that }A^{T}PA - P < 0 $$

**(증명)** 행렬 $A$가 Schur라고 가정한다. 임의의 positive definite 행렬 $Q > 0$에 대해, 행렬 $P$를 아래와 같이 가정하자.

$$ P = \sum_{k \geq 0} (A^{T})^{k} Q A^{k}$$

그러면, 아래를 만족한다.

$$
A^{T}PA - P = \sum_{k \geq 1} (A^{T})^{k} Q A^{k} - \sum_{k \geq 0} (A^{T})^{k} Q A^{k} = - (A^{T})^{0} Q A^{0} = -Q < 0
$$

반대로, 적당한 positive definitive 행렬 $P > 0$가 존재해서 $A^{T}PA - P < 0$를 만족한다고 가정하자. 행렬 $A$가 Schur인 것을 보이기 위해 Lyapunov 함수 $V$를 아래와 같이 정의하고, 안정성 조건을 만족하는지 확인한다. 함수 $V(x) = x^{T} P x$라 가정하면, $V(x) > 0$가 nonzero에 대해 만족하고, $V(0) = 0$를 만족한다. 또한,

$$
V(x_{k+1}) = x_{k+1}^{T} P x_{k+1} = x_{k}^{T} A^{T} P A x_{k} < x_{k}^{T} P x_{k} = V(x_{k})
$$

이고, 함수 $V(x)$는 감소하므로, 대응하는 시스템은 안정적이며, 행렬 $A$는 Schur이다.
