# 수치해석학 내용 정리


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

```math
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

$$x_{k+1} = x_{k} - (J^{T}J)^{-1}J^{T}F$$

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
$$x_{k+1} = x_{k} - (J^{T}J + \mu * I)^{-1}J^{T}F$$

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

$$x_{k+1} = x_{k} - (J^{T}J + \mu * diag(J^{T}J))^{-1}J^{T}F$$

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



























