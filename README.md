# Windows Service edit Sample

## 用法

在命令行中运行脚本，使用以下格式：

```bash
python main.py <command> [options]
```

### 命令

1. **info** - 显示指定服务的信息

   ```bash
   python main.py info --name <服务名称>
   ```

   - `--name`：指定要查看的服务名称。

2. **list** - 列出所有 Windows 服务

   ```bash
   python main.py list
   ```

3. **edit** - 修改指定服务的启动类型和可执行路径 _(需要管理员权限)_

   ```bash
   python main.py edit --name <服务名称> --starttype <启动类型> --path <可执行路径>
   ```

   - `--name`：指定要编辑的服务名称。
   - `--starttype`：设置服务的启动类型（例如，`2`为自动，`3`为手动，`4`为禁用）。
   - `--path`：设置服务的可执行路径。

### 示例

- 查看服务信息：

  ```bash
  python main.py info --name "nezha-agent"
  ```

- 列出所有服务：

  ```bash
  python main.py list
  ```

- 修改服务启动类型和路径：

  ```bash
  python main.py edit --name "nezha-agent" --starttype 2 --path "C:\\Program Files\\Nezha\\nezha-agent.exe"
  ```
