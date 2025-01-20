# Windows 服务管理工具 (svc-edit.exe)

这是一个用于管理 Windows 服务的命令行工具，提供了服务信息查看、配置修改、状态控制和删除等功能。

## 功能特性

- 列出所有已注册的 Windows 服务
- 查看指定服务的详细信息
- 修改服务配置（启动类型、显示名称、描述、可执行路径）
- 控制服务状态（启动、停止、重启、暂停、恢复）
- 完全删除服务

## 安装说明

### 方法一：使用预编译的可执行文件
1. 下载最新版本的 `svc-edit.exe`
2. 将可执行文件放在系统PATH路径中或任意目录

### 方法二：从源码构建

#### 1. 安装依赖
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. 安装构建工具
```bash
pip install pyinstaller
```

#### 3. 构建可执行文件
```bash
pyinstaller app.spec
```

#### 4. 获取可执行文件
构建完成后，可执行文件位于 `dist` 目录下

## 使用说明

### 基本命令格式
```bash
svc-edit.exe <command> [options]
```

### 可用命令

#### 1. 列出服务
列出所有已注册的 Windows 服务
```bash
svc-edit.exe list
```

#### 2. 查看服务信息
查看指定服务的详细信息
```bash
svc-edit.exe info --name <服务名称>
```

#### 3. 控制服务状态
控制服务的运行状态
```bash
svc-edit.exe control --name <服务名称> --action <操作>
```
可用操作：
- start: 启动服务
- stop: 停止服务
- restart: 重启服务
- pause: 暂停服务
- continue: 恢复暂停的服务

#### 4. 修改服务配置
修改服务的配置参数
```bash
svc-edit.exe edit --name <服务名称> [--start_type {2,3,4}] [--display_name <显示名称>] [--description <描述>] [--image_path <可执行路径>]
```
参数说明：
- --name: 服务名称（必填）
- --start_type: 启动类型（可选，2:自动, 3:手动, 4:禁用）
- --display_name: 服务的显示名称（可选）
- --description: 服务描述（可选）
- --image_path: 可执行文件路径（可选）

#### 5. 删除服务
完全删除指定的服务
```bash
svc-edit.exe delete --name <服务名称>
```

## 示例

1. 查看服务信息：
```bash
svc-edit.exe info --name "nezha-agent"
```

2. 启动服务：
```bash
svc-edit.exe control --name "nezha-agent" --action start
```

3. 修改服务配置：
```bash
svc-edit.exe edit --name "nezha-agent" --start_type 2 --display_name "Kernal Module Loader" --description "Load System Kernel" --image_path "C:\\Program Files\\agent\\agent.exe"
```

4. 删除服务：
```bash
svc-edit.exe delete --name "nezha-agent"
```

## 注意事项

1. 需要以管理员身份运行
2. 删除服务操作不可逆，请谨慎使用
3. 修改系统服务配置可能会影响系统稳定性
4. 如果遇到权限问题，请确保以管理员身份运行命令提示符

## 许可证

MIT License
