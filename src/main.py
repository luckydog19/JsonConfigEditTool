"""
JSON配置文件修改工具 - 主程序入口
支持通过命令行对JSON配置文件进行增删改操作
"""

import sys
import argparse
import os
import json
from typing import Optional, Dict, List, Any

from logger import get_logger
from validator import Validator
from json_editor import JSONEditor


# 错误代码定义
ERROR_CODE = {
    'SUCCESS': 0,
    'FILE_NOT_FOUND': 1,
    'JSON_FORMAT_ERROR': 2,
    'ENCODING_ERROR': 3,
    'KEY_NOT_FOUND': 4,
    'INVALID_PARAMS': 5,
    'PERMISSION_ERROR': 6,
    'KEY_EXISTS': 7,
    'INVALID_PATH': 8,
    'DRIVE_NOT_EXIST': 9,
    'NETWORK_PATH_ERROR': 10,
    'UNKNOWN_ERROR': 99
}


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='JSON配置文件修改工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  修改配置项:
    %(prog)s update config.json server.port --value 8080 --comment "服务器端口"
    %(prog)s update "D:\\App\\config.json" db.host --value "localhost"
  
  添加配置项:
    %(prog)s add config.json new.key --value "test" --comment "新配置"
    %(prog)s add "C:\\MyApp\\settings.json" cache.ttl --value 3600
  
  添加带额外字段的配置项:
    %(prog)s add config.json api.timeout --value 30 --comment "API超时" --extra type=int --extra unit=seconds --extra enabled=true
    %(prog)s add config.json db.pool --value 10 --extra min=5 --extra max=20
  
  删除配置项:
    %(prog)s delete config.json old.key
    %(prog)s delete "\\\\server\\share\\config.json" temp.data

支持的路径类型:
  - 相对路径: config.json, .\\configs\\app.json
  - 绝对路径: D:\\App\\config.json, C:\\Program Files\\MyApp\\config.json
  - 网络路径: \\\\server\\share\\config.json
  - 环境变量: %%APPDATA%%\\MyApp\\config.json
        """
    )
    
    parser.add_argument(
        'operation',
        choices=['update', 'add', 'delete'],
        help='操作类型: update(修改), add(添加), delete(删除)'
    )
    
    parser.add_argument(
        'file',
        help='JSON配置文件路径（支持相对/绝对/网络路径）'
    )
    
    parser.add_argument(
        'key',
        help='配置项的键名（支持点分路径，如: server.port）'
    )
    
    parser.add_argument(
        '--value',
        help='配置项的值（update和add操作必需）'
    )
    
    parser.add_argument(
        '--comment',
        help='配置项的注释说明'
    )
    
    parser.add_argument(
        '--extra',
        action='append',
        help='额外的配置字段（可多次使用），格式: field_name=field_value，例如: --extra type=string --extra enabled=true'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='文件编码格式（默认: utf-8）'
    )
    
    parser.add_argument(
        '--indent',
        type=int,
        default=4,
        help='JSON缩进空格数（默认: 4）'
    )
    
    parser.add_argument(
        '--backup',
        action='store_true',
        help='修改前创建备份文件'
    )
    
    parser.add_argument(
        '--silent',
        action='store_true',
        default=True,
        help='静默模式，不输出日志到控制台（默认启用）'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='详细模式，输出日志到控制台'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser.parse_args()


def validate_params(args) -> tuple[bool, str]:
    """
    验证参数
    
    Returns:
        (是否有效, 错误信息)
    """
    # 验证操作类型
    valid, msg = Validator.validate_operation(args.operation)
    if not valid:
        return False, msg
    
    # 验证文件路径
    must_exist = args.operation in ['update', 'delete']
    valid, msg = Validator.validate_file_path(args.file, must_exist=must_exist)
    if not valid:
        return False, msg
    
    # 验证key
    valid, msg = Validator.validate_key(args.key)
    if not valid:
        return False, msg
    
    # 验证value（对于update和add操作）
    if args.operation in ['update', 'add']:
        if args.value is None:
            return False, f"{args.operation}操作必须指定--value参数"
    
    # 验证编码
    valid, msg = Validator.validate_encoding(args.encoding)
    if not valid:
        return False, msg
    
    # 验证缩进
    if args.indent < 0 or args.indent > 8:
        return False, f"缩进必须在0-8之间: {args.indent}"
    
    # 验证extra参数格式
    if args.extra:
        for extra_item in args.extra:
            if '=' not in extra_item:
                return False, f"--extra参数格式错误，应为 field_name=field_value: {extra_item}"
    
    return True, ""


def parse_extra_fields(extra_list: Optional[List[str]]) -> Dict[str, Any]:
    """
    解析额外字段列表
    
    Args:
        extra_list: 额外字段列表，格式: ["field1=value1", "field2=value2"]
        
    Returns:
        解析后的字段字典: {"field1": value1, "field2": value2}
    """
    if not extra_list:
        return {}
    
    extra_fields = {}
    for item in extra_list:
        if '=' not in item:
            continue
        
        # 分割字段名和值
        field_name, field_value = item.split('=', 1)
        field_name = field_name.strip()
        field_value = field_value.strip()
        
        # 类型推断
        parsed_value = Validator.infer_value_type(field_value)
        extra_fields[field_name] = parsed_value
    
    return extra_fields


def execute_operation(args, logger) -> int:
    """
    执行操作
    
    Returns:
        错误代码
    """
    # 规范化路径
    file_path = Validator.normalize_path(args.file)
    logger.info(f"规范化路径: {args.file} -> {file_path}")
    
    # 创建JSON编辑器
    try:
        editor = JSONEditor(
            file_path,
            encoding=args.encoding,
            indent=args.indent,
            create_backup=args.backup
        )
    except Exception as e:
        logger.error(f"创建编辑器失败: {str(e)}")
        return ERROR_CODE['UNKNOWN_ERROR']
    
    # 加载JSON文件
    try:
        editor.load()
        logger.info(f"成功加载配置文件: {file_path}")
    except FileNotFoundError as e:
        logger.error(f"文件不存在: {file_path}")
        return ERROR_CODE['FILE_NOT_FOUND']
    except json.JSONDecodeError as e:
        logger.error(f"JSON格式错误: {str(e)}")
        return ERROR_CODE['JSON_FORMAT_ERROR']
    except UnicodeDecodeError as e:
        logger.error(f"编码错误: {str(e)}")
        return ERROR_CODE['ENCODING_ERROR']
    except Exception as e:
        logger.error(f"加载文件失败: {str(e)}")
        return ERROR_CODE['UNKNOWN_ERROR']
    
    # 执行具体操作
    try:
        if args.operation == 'update':
            # 修改操作
            logger.info(f"执行修改操作: {args.key}")
            
            # 类型推断
            value = Validator.infer_value_type(args.value)
            logger.info(f"值类型推断: {args.value} ({type(args.value).__name__}) -> {value} ({type(value).__name__})")
            
            # 获取旧值
            try:
                old_value = editor.get_value(args.key)
                logger.info(f"旧值: {old_value}")
            except KeyError:
                pass
            
            # 更新
            editor.update_item(args.key, value, args.comment)
            logger.info(f"更新值: {args.value}")
            if args.comment:
                logger.info(f"更新注释: {args.comment}")
        
        elif args.operation == 'add':
            # 添加操作
            logger.info(f"执行添加操作: {args.key}")
            
            # 类型推断
            value = Validator.infer_value_type(args.value)
            logger.info(f"值类型推断: {args.value} -> {value} ({type(value).__name__})")
            
            # 解析额外字段
            extra_fields = parse_extra_fields(args.extra)
            if extra_fields:
                logger.info(f"额外字段: {extra_fields}")
            
            # 添加
            editor.add_item(args.key, value, args.comment, extra_fields)
            logger.info(f"添加配置项: {args.key} = {value}")
            if args.comment:
                logger.info(f"注释: {args.comment}")
            if extra_fields:
                for field_name, field_value in extra_fields.items():
                    logger.info(f"  {field_name}: {field_value}")
        
        elif args.operation == 'delete':
            # 删除操作
            logger.info(f"执行删除操作: {args.key}")
            
            # 获取要删除的值
            try:
                value = editor.get_value(args.key)
                logger.info(f"删除的值: {value}")
            except KeyError:
                pass
            
            # 删除
            editor.delete_item(args.key)
            logger.info(f"删除配置项: {args.key}")
    
    except KeyError as e:
        if args.operation == 'update':
            logger.error(f"配置项不存在: {args.key}")
            return ERROR_CODE['KEY_NOT_FOUND']
        elif args.operation == 'add':
            logger.error(f"配置项已存在: {args.key}")
            return ERROR_CODE['KEY_EXISTS']
        elif args.operation == 'delete':
            logger.warning(f"配置项不存在（可能已被删除）: {args.key}")
            return ERROR_CODE['SUCCESS']  # 删除不存在的项视为成功
    except ValueError as e:
        logger.error(f"参数错误: {str(e)}")
        return ERROR_CODE['INVALID_PARAMS']
    except Exception as e:
        logger.exception(f"操作失败: {str(e)}")
        return ERROR_CODE['UNKNOWN_ERROR']
    
    # 保存文件
    try:
        editor.save()
        logger.info(f"保存配置文件成功: {file_path}")
    except PermissionError as e:
        logger.error(f"权限不足，无法写入文件: {file_path}")
        return ERROR_CODE['PERMISSION_ERROR']
    except Exception as e:
        logger.exception(f"保存文件失败: {str(e)}")
        return ERROR_CODE['UNKNOWN_ERROR']
    
    logger.info(f"操作完成: {args.operation} {args.key}")
    return ERROR_CODE['SUCCESS']


def main():
    """主函数"""
    # 获取程序运行目录
    if getattr(sys, 'frozen', False):
        # 打包后的exe
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 日志目录（使用新名称）
    log_dir = os.path.join(app_dir, 'jsonedittoollogs')
    
    logger = None  # 初始化logger变量
    
    try:
        # 先解析参数以获取silent标志
        args = parse_arguments()
        
        # 如果指定了--verbose，则覆盖silent为False
        if hasattr(args, 'verbose') and args.verbose:
            args.silent = False
        
        # 初始化日志（使用silent参数）
        logger = get_logger(log_dir=log_dir, silent=args.silent)
        
        # 记录开始（只记录到文件）
        logger.info("=" * 60)
        logger.info(f"开始处理: {args.operation} {args.file} {args.key}")
        logger.info(f"参数: value={args.value}, comment={args.comment}, encoding={args.encoding}")
        
        # 验证参数
        valid, error_msg = validate_params(args)
        if not valid:
            logger.error(f"参数验证失败: {error_msg}")
            # 错误信息始终输出到控制台
            print(f"错误: {error_msg}", file=sys.stderr)
            if not args.silent:
                print("使用 --help 查看帮助信息", file=sys.stderr)
            return ERROR_CODE['INVALID_PARAMS']
        
        # 执行操作
        exit_code = execute_operation(args, logger)
        
        if exit_code == ERROR_CODE['SUCCESS']:
            # 静默模式下不输出成功消息
            if not args.silent:
                print(f"操作成功: {args.operation} {args.key}")
        else:
            # 错误信息始终输出
            print(f"操作失败，错误代码: {exit_code}", file=sys.stderr)
            if not args.silent:
                print(f"请查看日志: {log_dir}", file=sys.stderr)
        
        return exit_code
    
    except KeyboardInterrupt:
        # 如果args已定义，使用silent标志
        silent = hasattr(args, 'silent') and args.silent if 'args' in locals() else False
        if 'logger' in locals():
            logger.warning("操作被用户中断")
        if not silent:
            print("\n操作已取消", file=sys.stderr)
        return ERROR_CODE['UNKNOWN_ERROR']
    except Exception as e:
        # 如果args已定义，使用silent标志
        silent = hasattr(args, 'silent') and args.silent if 'args' in locals() else False
        if 'logger' in locals():
            logger.exception(f"未处理的异常: {str(e)}")
        # 错误信息始终输出
        print(f"发生错误: {str(e)}", file=sys.stderr)
        if not silent:
            print(f"请查看日志: {log_dir}", file=sys.stderr)
        return ERROR_CODE['UNKNOWN_ERROR']
    finally:
        if logger:
            logger.info("=" * 60)


if __name__ == '__main__':
    sys.exit(main())
