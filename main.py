import winreg
import argparse
import win32serviceutil
import win32service
import win32api

def list_services():
    """
    列出所有注册的 Windows 服务名称。
    """
    try:
        registry_path = "SYSTEM\\CurrentControlSet\\Services"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            print("已注册的服务列表：")
            i = 0
            while True:
                try:
                    service_name = winreg.EnumKey(key, i)
                    print(service_name)
                    i += 1
                except OSError:
                    break
    except PermissionError:
        print("权限不足，请以管理员身份运行脚本。")
    except Exception as e:
        print(f"发生错误: {e}")

def get_service_info(service_name):
    """
    获取并打印指定 Windows 服务的信息。
    """
    info = {}
    try:
        registry_path = f"SYSTEM\\CurrentControlSet\\Services\\{service_name}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            # 获取 Start 类型
            info["StartType"] = winreg.QueryValueEx(key, "Start")[0]
            # 获取 DisplayName
            info["DisplayName"] = winreg.QueryValueEx(key, "DisplayName")[0]
            # 获取 Description
            try:
                info["Description"] = winreg.QueryValueEx(key, "Description")[0]
            except FileNotFoundError:
                info["Description"] = "无描述"
            # 获取 ImagePath
            info["ImagePath"] = winreg.QueryValueEx(key, "ImagePath")[0]

        # 打印服务信息
        print(f"服务名称: {service_name}")
        print(f"启动类型: {info['StartType']} (2: 自动, 3: 手动, 4: 禁用)")
        print(f"显示名称: {info['DisplayName']}")
        print(f"描述: {info['Description']}")
        print(f"可执行路径: {info['ImagePath']}")

    except FileNotFoundError:
        print(f"服务 '{service_name}' 不存在，请检查服务名称。")
    except PermissionError:
        print("权限不足，请以管理员身份运行脚本。")
    except Exception as e:
        print(f"发生错误: {e}")

def control_service(service_name, action):
    """
    控制服务状态
    action: start|stop|restart|pause|continue
    """
    try:
        if action == "start":
            win32serviceutil.StartService(service_name)
            print(f"服务 '{service_name}' 已启动")
        elif action == "stop":
            win32serviceutil.StopService(service_name)
            print(f"服务 '{service_name}' 已停止")
        elif action == "restart":
            win32serviceutil.RestartService(service_name)
            print(f"服务 '{service_name}' 已重启")
        elif action == "pause":
            win32serviceutil.PauseService(service_name)
            print(f"服务 '{service_name}' 已暂停")
        elif action == "continue":
            win32serviceutil.ResumeService(service_name)
            print(f"服务 '{service_name}' 已恢复")
        else:
            print(f"未知的操作: {action}")
    except win32service.error as e:
        print(f"操作失败: {e.strerror}")
    except Exception as e:
        print(f"发生错误: {e}")

def set_service_config(service_name, start_type=None, display_name=None, description=None, image_path=None):
    """
    修改 Windows 服务的配置。
    """
    try:
        registry_path = f"SYSTEM\\CurrentControlSet\\Services\\{service_name}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_SET_VALUE) as key:
            if start_type is not None:
                winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, start_type)
                print(f"启动类型已设置为 {start_type}")

            if display_name is not None:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, display_name)
                print(f"显示名称已设置为 '{display_name}'")

            if description is not None:
                winreg.SetValueEx(key, "Description", 0, winreg.REG_SZ, description)
                print(f"描述已设置为 '{description}'")
            
            if image_path is not None:
                winreg.SetValueEx(key, "ImagePath", 0, winreg.REG_SZ, image_path)
                print(f"ImagePath 已设置为 '{image_path}'")

    except FileNotFoundError:
        print(f"服务 '{service_name}' 不存在，请检查服务名称。")
    except PermissionError:
        print("权限不足，请以管理员身份运行脚本。")
    except Exception as e:
        print(f"发生错误: {e}")

def delete_service(service_name):
    """
    完全删除指定的 Windows 服务。
    步骤：
    1. 检查服务是否存在
    2. 如果服务正在运行，则停止服务
    3. 从SCM中删除服务
    4. 删除服务注册表项
    """
    try:
        # 检查服务是否存在
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)
            if status[1] == win32service.SERVICE_RUNNING:
                print(f"服务 '{service_name}' 正在运行，正在停止...")
                control_service(service_name, "stop")
        except win32service.error as e:
            if e.winerror != 1060:  # 1060 = 服务不存在
                raise

        # 从SCM中删除服务
        print(f"正在从服务控制管理器中删除服务 '{service_name}'...")
        win32serviceutil.RemoveService(service_name)
        
        # 删除服务注册表项
        try:
            registry_path = f"SYSTEM\\CurrentControlSet\\Services\\{service_name}"
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
        except FileNotFoundError:
            pass  # 如果注册表项已被删除则忽略

        print(f"服务 '{service_name}' 已完全删除")

    except win32service.error as e:
        if e.winerror == 1072:  # 服务已被标记为删除
            print("服务已被标记为删除，将在系统重启后完全移除")
        else:
            print(f"删除服务时发生错误: {e.strerror}")
    except PermissionError:
        print("权限不足，请以管理员身份运行脚本。")
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="管理 Windows 服务的配置")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出所有注册的服务")

    # info 子命令
    info_parser = subparsers.add_parser("info", help="打印指定服务的信息")
    info_parser.add_argument("--name", type=str, required=True, help="服务名称")

    # control 子命令
    control_parser = subparsers.add_parser("control", help="控制服务状态")
    control_parser.add_argument("--name", type=str, required=True, help="服务名称")
    control_parser.add_argument("--action", type=str, required=True, 
                              choices=["start", "stop", "restart", "pause", "continue"],
                              help="""要执行的操作：
                              start - 启动服务
                              stop - 停止服务
                              restart - 重启服务
                              pause - 暂停服务
                              continue - 恢复暂停的服务""")

    # edit 子命令
    edit_parser = subparsers.add_parser("edit", help="编辑指定服务的配置")
    edit_parser.add_argument("--name", type=str, required=True, help="服务名称")
    edit_parser.add_argument("--start_type", type=int, choices=[2, 3, 4], help="启动类型 (2: 自动, 3: 手动, 4: 禁用)")
    edit_parser.add_argument("--display_name", type=str, help="服务的显示名称")
    edit_parser.add_argument("--description", type=str, help="服务的描述")
    edit_parser.add_argument("--image_path", type=str, help="服务的可执行文件路径 (ImagePath)")

    # delete 子命令
    delete_parser = subparsers.add_parser("delete", help="删除指定的服务")
    delete_parser.add_argument("--name", type=str, required=True, help="要删除的服务名称")

    args = parser.parse_args()

    if args.command == "list":
        list_services()
    elif args.command == "info":
        get_service_info(args.name)
    elif args.command == "control":
        control_service(args.name, args.action)
    elif args.command == "edit":
        set_service_config(
            service_name=args.name,
            start_type=args.start_type,
            display_name=args.display_name,
            description=args.description,
            image_path=args.image_path
        )
    elif args.command == "delete":
        delete_service(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
