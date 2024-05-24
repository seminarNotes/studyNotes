# 수치해석학 내용 정리
과학 뿐만 아니라 사회, 공학 등에서의 이론에서는 모델을 통해, 관측값과 현상을 설명한다. 이러한 모델은 관측값의 이해와 예측값의 개선을 설명하는 데에도 효과적이며,관련된 문제를 해결하고, 기술을 개발하는데 필수적이다. 모델은 이미 관측된 값을 잘 설명할 수 있어야하기 때문에, 관측값과 모델값의 차이가 최소화가 되는 모델을 결정 해야 한다.  

최소자승문제(Least Sqaured Method)는 위와 같은 문제를 해결하기 위한 방법이며, 모델 파라미터에 대한 선형 또는 비선형에 따라 접근 방법이 달라진다. 선형 최소자승문제의 경우, pseudo invervse나 SVD(Singular Value Decomposition)를 이용해 해를 구할 수 있지만, 비선형 문제의 경우, Close-from Solution이 없기 때문에 반복을 통해 해를 찾는 방법을 사용한다. 이 때, 반복을 통해 해를 찾는 방법을 Iterative Maximization이라 하며, 대표적인 방법으로, Gradient Descent, Gaussian-Netwon 방법, Levenberg-Marquadt 방법 등이 있다.

---

## 선형 최소자승문제(Linear Least Sqaured Method)
$n$개의 관측치가 주어져 있고, 관측값을 설명하는 모델의 파라미터의 수가 $m$라 가정하자. 그러면, 고정된 $i$번 째 관측치 $y_{i}$와 모델값 $F(x_{i}, \bold{p})$의 차이를 $e_{i}$의 제곱합이 최소가 되도록 순서쌍 $\bold{p}$을 결정하는 문제이다. 따라서, 아래와 같이 기술 할 수 있다.
$$
\bold{p}^{*} = \text{arg min} \sum_{1 \leq i \leq n} e_{i}^{2} = \text{arg min} \sum_{1 \leq i \leq n} (y_i - F(x_{i}, \bold{p}))^{2}
$$

위 수식을 행렬 곱으로 표현하면,

$$
E(\bold{p}) = \sum_{1 \leq \i \leq n} e_{i}^{2} = e^{T}e = ||e||^2
$$

한편, 모델은 $m$개의 파라미터에 의해 결정 되고, $\bold{x}$를 입력값으로 하는 함수이기 때문에 아래와 같이 쓸 수 있다.

$$
\F(\bold{x}, \bold{p}) = \sum_{1 \leq i \leq n} a_{j}(\bold{x})p_{j} = 
\left[
\begin{matrix}
a_{1}(\bold{x}), a_{2}(\bold{x}), \cdots, a_{m}(\bold{x})
\end{matrix}
\right]

\left[
\begin{matrix}
p_{1} \\ p_{2} \\\vdots \\ p_{m}
\end{matrix}
\right]

= \left[
\begin{matrix}
a_{1}(x_{1}), a_{2}(x_{1}), \cdots, a_m(x_{1}) \\
a_{1}(x_{2}), a_{2}(x_{2}), \cdots, a_m(x_{2}) \\
\vdots \\
a_{1}(x_{n}), a_{2}(x_{n}), \cdots, a_m(x_{n}) \\
\end{matrix}
\right]

\left[
\begin{matrix}
p_{1} \\ p_{2} \\ \vdots \\ p_{m}
\end{matrix}
\right]

= A \bold{p}
$$

이제 최소값을 계산하기 위해, $\frac{\partial E(\bold{p})}{\partial \bold{p}} = 0$인 $\bold{p}$를 계산한다.

$$
\frac{\partial E(\bold{p})}{\partial \bold{p}} = \frac{\partial}{\partial \bold{p}} ||\bold{y} - A \bold{p}||^{2} = -2(\bold{y} - A \bold{p})^{T} = 0
$$

위 방정식으로부터 아래와 같은 닫힌 형식의 해를 계산할 수 있다.

$$
\bold{p} = (A^{T}A)^{-1}A^{T}\bold{y}
$$

요약하면, 선형 회귀 분석과 같은 선형 최소자승문제가 주어졌을 경우, 우리는 계수 행렬을 적절히 표현하여, 데이터 분포를 가장 잘 설명하는 모델의 파라미터를 위와 같이 계산할 수 있다.


라이브러리 설치 및 변수 선언
```python
import numpy as np

CONSTANT_EPSILON = 1e-8
CONSTANT_TOLERANCE = 1e-6
CONSTANT_ITERATION = 100
```

다변수 함수에 대한 최적화, 수치해석을 하는 경우, gradient vector, jacobian matrix, gaussian elimination을 자주 계산하기 때문에 해당 계산을 하는 함수를 먼저 정의 한다.

```python
def vector_gradient(function_F, variable_X, epsilon = CONSTANT_EPSILON) :
	F = function_F
	X = np.asarray(variable_X, dtype = float)
	FX = F(X)
	n = len(X)
	vector_grad = np.zeros(n)

	for idx in range(n) :
		X_step = np.copy(X)
		X_step[idx] += epsilon
		vector_grad[idx] = (F(X_step) - FX) / epsilon

	return vector_grad

def matrix_jacobian(function_F, variable_X, epsilon = CONSTANT_EPSILON) :
	F = function_F
	X = np.asarray(variable_X, dtype = float)
	n = len(X)
	m = len(F(X))
	matrix_J = np,zeros((m, n))
	FX = F(X)
	for idx in range(n) :
		X_step = np.copy(X)
		X_step[idx] += epsilon
		matrix_J[:, idx] = (F(X_step) - FX) / epsilon

	return matrix_J

def vector_euclidean_norm(vector_X) :
	norm = 0 
	n = len(vector_X)
	for idx in range(n) :
		norm += vector_X[idx] ** 2
	
	return norm ** 0.5

def matrix_gaussian_elimination(matrix_A, vector_b) :
	n = len(A)
	augmented_matrix = [matrix_A[idx] + [b[idx] for idx in range(n)]

	for idx1 in range(n) :
		max_row = max(range(idx1, n), key = lambda r : abs(augmented_matrix[r][idx1]))
		augmented_matrix[idx1], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[idx1]
		
		diag = augmented_matrix[idx1][idx1]
		for idx2 in range(idx1, n + 1) :
			augmented_matrix[idx1][idx2] /= diag

		for idx2 in range(idx1 + 1, n) :
			factor = augmented_matrix[idx2][idx1]

			for idx3 in range(idx1, n + 1) :
				augmented_matrix[idx2][idx3] -= factor * augmented_matrix[idx1][idx3]

	# Back Substitution
	X = [0 for _ in range(n)]
	for idx1 in range(n - 1, -1, -1) :
		X[idx1] = augmented_matrix[idx1][n] - sum(augmented_matrix[idx1][idx2] * X[idx2] for idx2 in range(idx1 + 1, n))

	return X

	"""
    	for instance,
        
    	matrix_A = [[2,1,-1],[0,1,1],[0,0,-1]]
        b = [8,2,1]
        n = len(matrix_A)
        >> X = [2,3,-1]
	"""
``` 

## Gradient Descent  
Gradient Descent 방법은 Gradient의 반대 방향으로 매개변수를 이동하는 방법으로 이동 크기는 Gradient의 크기에 비례한다.

``` math
x_{k+1} = x_{k} - \alpha J^{T}F
```

``` python
def algorithm_gradient_descent(function_F, variable_X, learning_rate = 0.01, tol = CONSTANT_TOLERANCE, max_iter = CONSTANT_ITERATION, epsilon = CONSTANT_EPSILON) :
	F = function_F
	X = np.asarray(variable_X, dtype = float)
	grad_F = vector_gradient(F, X, epsilon)
	grad_F(F,X)
	for idx in range(max_iter) :
		grad = grad_F(F, X)
		X = X - learning * grad

		if np.linalg.norm(grad) < tol :
			break

	return X
```

## Gaussian-Newton Method

``` math
x_{k+1} = x_{k} - (J^{T}J)^{-1}J^{T}F
```

Gaussian-Newton는 이동할 Step 사이즈를 (Gradient/Curvature)로 결정하는데, 이는 Gradient의 변화가 급격하면 (Curvature가 크면), 조금만 이동하고, Gradient의 변화가 적으면(Curvature가 작으면) 조금 더 크게 이동하하면서 해결하는 방식이다. Gaussian-Netwon이 Gradient Descent보다 더 정확하고 빠르게 해를 찾을 수 있다. 그러나, $J^{T}J$가 singular에 가까울 수록 수치적으로 불안정하여 해가 발산할 수 있따는 문제점이 존재했다.
```python
def algorithm_gaussian_newton(function_F, varible_X, tol = CONSTANT_TOLERANCE, max_iter = CONSTANT_ITERATION) :
	F = function_F
	X = np.asarray(variable_X, dtype = float)
	for idx in range(max_iter) :
		J = matrix_jacobian(F, X)
		r = F(X)
		JTJ = np.dot(J.T, J)
		g = np.dot(J.T, r)
		delta_X = np.array(maxtrix_gaussian_elimination(JTJ.tolist(), (-g).tolist()))
		X = X + delta_X
		if vector_euclidean_norm(delta_X) < tol :
			break

	return X
```

## Levenberg Method

Levenberg Method는 두 방법을 혼합한 것이고, 아래의 식으로 작성한다.

``` math
x_{k+1} = x_{k} - (J^{T}J + \mu * I)^{-1}J^{T}F
```

Gaussian-Newton 방식에 Gradient Descent 방식을 혼합해서 수치적으로 불안정한 해의 발산에 대한 위험을 관리한다. $\mu$는 damping factor인데, 이 값이 낮으면 Gaussian-Netwon과 유사하고, 반대의 경우, Gradient Descent와 유사하다. 이 때, Gradient Descent와 유사할 경우, 수렴 속도가 느리다는 문제가 여전히 존재한다.

``` python 
def algorithm_levenberg(function_F, variable_X, tol = CONSTANT_TOLERANCE, max_iteration = CONSTNAT_ITERATION, lambda_init = 1e-3, lambda_factor = 10) :
	F = function_F
	X = np.array(variable_X, dtype = float)
	lamdba_ = lambda_init
	for idx in range(max_iter) :
		J = matrix_jacobian(F, X) :
		r = F(X)
		JTJ = J.T @ J
		g = J.T @ r
		A = JTJ + lambda_ * np.eye(len(X))
		delta_X = np.linalg.solve(A, -g)
		new_X = X + delta_X

		if np.linalg.norm(F(new_X)) < np.linalg.norm(r) :
			X = new_X
			lambda_ /= lamdbda_factor
		else :
			lamdba_ *= lamdbda_factor

	return X
```


## Levenberg-Marquadt Method
Levenberg-Marqaudt는 Levenberg Method가 Gradient Descent 방식으로 동작할 때, 수렴 속도가 느리다는 단점을 보완하며, 아래의 수식이 주어진다.

``` math
x_{k+1} = x_{k} - (J^{T}J + \mu * diag(J^{T}J))^{-1}J^{T}F
```

항등 행렬(I) 대신 $diag(J^{T}J)$를 곱하는데, $J^{T}J$가 Hessian의 근사 행렬이기 때문에 $J^{T}J$의 대각 원소들은 각 매개 변수 축으로의 곡률을 의미한다.


``` python 
def algorithm_levenberg(function_F, variable_X, tol = CONSTANT_TOLERANCE, max_iteration = CONSTNAT_ITERATION, lambda_init = 1e-3, lambda_factor = 10) :
	F = function_F
	X = np.array(variable_X, dtype = float)
	lamdba_ = lambda_init
	for idx in range(max_iter) :
		J = matrix_jacobian(F, X) :
		r = F(X)
		JTJ = J.T @ J
		g = J.T @ r
        D = np.eye(len(A))
        np.fill_diagonal(D, val = A.diagonal())
        A = JTJ + lambda_ * D
		delta_X = np.linalg.solve(A, -g)
		new_X = X + delta_X

		if np.linalg.norm(F(new_X)) < np.linalg.norm(r) :
			X = new_X
			lambda_ /= lamdbda_factor
		else :
			lamdba_ *= lamdbda_factor

	return X
```



























