import socket
import threading
import matplotlib.pyplot as plt
from collections import deque
import ast  # 用于将字符串转换为列表
from matplotlib.animation import FuncAnimation

# 设置服务器端口和地址
HOST = '0.0.0.0'  # 监听所有可用的接口
PORT = 5050

# 创建服务器端 socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# 设置绘图
fig, ax = plt.subplots()
x_data = deque(maxlen=100)  # 存储 x 轴数据的队列（最多100个数据点）
y_data = deque(maxlen=100)  # 存储 y 轴数据的队列（最多100个数据点）
z_data = deque(maxlen=100)  # 存储 z 轴数据的队列（最多100个数据点）
line_x, = ax.plot([], [], label="X Acceleration")
line_y, = ax.plot([], [], label="Y Acceleration")
line_z, = ax.plot([], [], label="Z Acceleration")
ax.set_xlabel('Time')
ax.set_ylabel('Acceleration Value')
ax.legend()

# 设置动画
def update_plot(frame):
    # 更新 x, y, z 方向的加速度数据
    line_x.set_xdata(range(len(x_data)))
    line_x.set_ydata(x_data)

    line_y.set_xdata(range(len(y_data)))
    line_y.set_ydata(y_data)

    line_z.set_xdata(range(len(z_data)))
    line_z.set_ydata(z_data)

    ax.relim()  # 重新计算数据范围
    ax.autoscale_view()  # 自动缩放视图
    return line_x, line_y, line_z

# 线程函数：用于接收并处理数据
def receive_data():
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    
    try:
        while True:
            data = client_socket.recv(1024)  # 每次读取 1024 字节数据
            if not data:
                break
            data_str = data.decode()
            # 处理数据
            try:
                # 解析数据，将字符串转为列表
                sensor_data = ast.literal_eval(data_str)  # 这将把字符串形式的列表转换为真实的列表
                if len(sensor_data) == 3:  # 确保数据是 x, y, z 三个加速度值
                    x, y, z = map(float, sensor_data)  # 将字符串转换为浮动类型
                    # 将数据添加到队列中
                    x_data.append(x)
                    y_data.append(y)
                    z_data.append(z)
                else:
                    print(f"Invalid data format (not 3 values): {data_str}")
            except (ValueError, SyntaxError):
                print(f"Invalid data format: {data_str}")
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        client_socket.close()  # 关闭连接

# 启动接收数据的线程
data_thread = threading.Thread(target=receive_data, daemon=True)
data_thread.start()

# 设置 FuncAnimation，每100ms更新一次图形
ani = FuncAnimation(fig, update_plot, interval=10, blit=True)

# 显示图形
plt.show()

# 让主线程保持运行，防止程序退出
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    server_socket.close()  # 关闭服务器
