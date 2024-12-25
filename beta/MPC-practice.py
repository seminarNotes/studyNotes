import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 시뮬레이션 설정
x_grid_size = 1000  # x축 범위를 1000으로 확장
y_grid_size = 200   # y축 범위를 200으로 설정
N = 10  # 예측 구간 (Prediction Horizon)
M = 5   # 제어 구간 (Control Horizon)
total_steps = 100  # 전체 시뮬레이션 단계 (long-term 관측을 위해 증가)

# 초기 상태 및 목표 궤적 설정
x_initial = np.array([0, y_grid_size / 2, 0, 0])  # 초기 위치를 (0, 100)으로 설정
x_target = np.linspace(0, x_grid_size, total_steps)

# 목표 궤적: 다양한 함수로 정의 (y_grid_size에 맞게 조정)
y_targets = [
    (100 * 0.5 * np.sin(x_target * (np.pi / 1000)) + 100 / 2, 
     "Sine Wave", r"$y = 100 \sin\left(\frac{\pi x}{1000}\right) + 100$"),
    (0.0005 * (x_target - 1000 / 2) ** 2 + 100 / 4, 
     "Convex", r"$y = 0.0005 (x - 500)^2 + 50$"),
    (-0.0005 * (x_target - 1000 / 2) ** 2 + 100 * 0.75, 
     "Concave", r"$y = -0.0005 (x - 500)^2 + 150$"),
    (100 * 0.5 * np.sin(x_target * (2 * np.pi / 1000)) + 100 / 2, 
     "High Frequency Sine Wave", r"$y = 100 \sin\left(\frac{2 \pi x}{1000}\right) + 100$"),
    (100 / 10 * np.exp(x_target / 1000) + 100 / 4, 
     "Exponential", r"$y = 20 \exp\left(\frac{x}{1000}\right) + 50$"),
    (np.piecewise(x_target, 
              [x_target < 250, 
               (x_target >= 250) & (x_target < 750), 
               x_target >= 750],
              [lambda x: 0.3 * x + 25,   # 첫 번째 구간
               lambda x: -0.1 * x + 125, # 두 번째 구간
               lambda x: -0.2 * x + 200]), # 세 번째 구간
     "Piecewise Linear", r"$y = \text{piecewise linear}$"),

    (0.0005 * (x_target - 1000 / 2) ** 2 + 20 * np.sin(x_target * (2 * np.pi / 1000)) + 100 / 10, 
     "Quadratic with Oscillation", r"$y = 0.0005 (x - 500)^2 + 20 \sin\left(\frac{2 \pi x}{1000}\right) + 20$"),
    (75 * np.exp(-2 * x_target / 1000) * np.sin(6 * x_target * np.pi / 1000) + 75, 
     "Damped Oscillation (Faster Decay)", r"$y = 75 \exp\left(-\frac{2x}{1000}\right) \sin\left(\frac{6 \pi x}{1000}\right) + 75$"),
    (0.15 * x_target + 30 * np.sin(2 * x_target * np.pi / 500) + 50, 
     "Linear with Small Oscillation", r"$y = 0.15 x + 30 \sin\left(\frac{2 \pi x}{500}\right) + 50$")
]

# 시스템 행렬 정의 (모바일 로봇 모델: 위치 및 속도)
dt = 1.0  # 시간 간격
A = np.array([[1, 0, dt, 0], 
              [0, 1, 0, dt], 
              [0, 0, 1, 0], 
              [0, 0, 0, 1]])
B = np.array([[0.5 * dt**2, 0], 
              [0, 0.5 * dt**2], 
              [dt, 0], 
              [0, dt]])

Q = np.eye(4) * 10  # 상태 가중치 (스케일 조정)
R = np.eye(2) * 0.1  # 입력 가중치 (스케일 조정)

# 제약 조건 설정
u_min, u_max = -1.0, 1.0  # 입력 제약
x_min, x_max = 0, x_grid_size  # x축 상태 제약
y_min, y_max = 0, y_grid_size  # y축 상태 제약

# 비용 함수 정의 (제약 조건 포함)
def mpc_cost(u, x_current, trajectory_target):
    u = u.reshape(N, 2)  # 예측 구간만큼의 제어 입력
    x = x_current.copy()
    J = 0
    for k in range(N):
        # 목표 위치에 대한 오차 계산
        target_position = np.array([trajectory_target[k, 0], trajectory_target[k, 1], 0, 0])
        J += (x - target_position).T @ Q @ (x - target_position)
        
        # 제어 구간 내에서는 제어 입력에 대한 비용 추가
        if k < M:
            J += u[k].T @ R @ u[k]
        
        # 상태 갱신 (상태 제약 적용)
        x = A @ x + B @ np.clip(u[k], u_min, u_max)
        
        # x와 y 축 상태 범위 제약 적용
        x[0] = np.clip(x[0], x_min, x_max)
        x[1] = np.clip(x[1], y_min, y_max)
        
    return J

# 시각화 설정
fig, axs = plt.subplots(3, 3, figsize=(15, 15))
fig.suptitle("MPC-Controlled Mobile Robot for Various Trajectories", fontsize=16)

# 각 목표 궤적에 대해 시뮬레이션 수행 및 시각화
for i, (y_target, title, equation) in enumerate(y_targets):
    # 목표 궤적 생성
    trajectory_target = np.vstack([x_target, y_target]).T
    
    # 초기 상태 및 시뮬레이션
    x = x_initial.copy()
    trajectory_followed = [x[:2].copy()]
    u_previous = np.zeros(N * 2)  # 이전 제어 입력 초기화
    
    for step in range(total_steps - N):
        # 예측 구간의 목표 궤적 설정 (이동 예측 윈도우 적용)
        target_segment = trajectory_target[step:step + N]
        
        # 최적화 수행
        result = minimize(mpc_cost, u_previous, args=(x, target_segment), method='SLSQP', 
                          bounds=[(u_min, u_max)] * (N * 2), options={'maxiter': 100, 'ftol': 1e-4})
        
        # 최적화된 첫 번째 제어 입력 적용
        optimal_u = result.x.reshape(N, 2)[0]  # 첫 번째 제어 입력을 사용
        x = A @ x + B @ np.clip(optimal_u, u_min, u_max)  # 상태 갱신 및 제어 입력 제약 적용
        trajectory_followed.append(x[:2].copy())
        
        # 현재 최적화 결과를 다음 단계의 초기 제어 입력으로 사용
        u_previous = result.x
    
    # 결과 시각화
    trajectory_followed = np.array(trajectory_followed)
    ax = axs[i // 3, i % 3]
    ax.plot(x_target, y_target, label="Target Trajectory", linestyle="--", color="blue")
    ax.plot(trajectory_followed[:, 0], trajectory_followed[:, 1], label="MPC Controlled Path", color="red")
    ax.set_xlim(0, x_grid_size)
    ax.set_ylim(0, y_grid_size)
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_title(f"{title}\n{equation}", fontsize=10)
    ax.legend()
    ax.grid()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
