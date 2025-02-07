import csv
from threading import Thread

from flask import Blueprint, request, current_app, jsonify

from server_status import SUCCESS, FAILURE

data_mgmt_bp = Blueprint('data_mgmt', __name__)


@data_mgmt_bp.route('/select_database', methods=['POST'])
def select_database():
    """
    用户选择当前操作的数据库。
    """
    data = request.get_json()
    db_name = data.get('db_name')  # 数据库名称
    db_type = data.get('db_type')  # 数据库类型 ('sqlite', 'mysql' 等)
    db_path = data.get('db_path')  # 数据库路径

    if not db_name or not db_type or not db_path:
        return jsonify({'status': FAILURE, 'message': 'Missing database parameters'})

    try:
        db_manager = current_app.config['db_manager']

        # 将用户选择的数据库设置为默认数据库
        selected_db = {
            'db_name': db_name,
            'db_type': db_type,
            'db_path': db_path
        }
        db_manager.set_default_database(selected_db)

        return jsonify({'status': SUCCESS, 'message': f'Database {db_name} set as default'})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


@data_mgmt_bp.route('/refresh_database', methods=['GET'])
def refresh_database():
    """
    刷新显示当前存储的数据库列表。
    """
    try:
        db_manager = current_app.config['db_manager']
        database_list = db_manager.get_all_databases()  # 假设返回数据库信息的列表

        # 格式化数据库信息，列表显示
        db_display_list = [
            f"{db['db_name']}({db['db_path']})" for db in database_list
        ]
        return jsonify({'status': SUCCESS, 'databases': db_display_list})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


@data_mgmt_bp.route('/get_database', methods=['POST'])
def get_database():
    """
    显示所选数据库数据或保存到本地文件。
    """
    data = request.get_json()
    db_name = data.get('db_name')
    display_mode = data.get('display_mode', 'db_show')  # 'db_show' 或 'db_file'
    limit = data.get('limit', 100)  # 查询数量限制，避免输出过多

    try:
        db_manager = current_app.config['db_manager']
        database = db_manager.get_database(db_name)  # 假设可以通过名称获取数据库实例

        # 检查用户权限及访问数据库
        entries = database.fetch_all(limit=limit)

        if display_mode == 'db_show':  # 直接返回查询结果
            return jsonify({'status': SUCCESS, 'data': entries})
        elif display_mode == 'db_file':  # 导出到 CSV
            # 将数据存储到本地文件
            file_path = f"./exports/{db_name}_export.csv"
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if entries:
                    writer.writerow(entries[0].keys())  # 写入列头
                    for entry in entries:
                        writer.writerow(entry.values())  # 写入数据行
            return jsonify({'status': SUCCESS, 'message': f'Data exported to {file_path}'})
        else:
            return jsonify({'status': FAILURE, 'message': 'Invalid display mode'})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


def async_export_to_csv(database, db_name, limit):
    """
    线程：异步导出大数据集到 CSV 文件。
    """
    file_path = f"./exports/{db_name}_export.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        entries = database.fetch_all(limit)  # 获取所有数据
        if entries:
            writer.writerow(entries[0].keys())  # 写入列头
            for entry in entries:
                writer.writerow(entry.values())  # 写入数据行
    print(f"Data exported to {file_path}")


@data_mgmt_bp.route('/export_database_async', methods=['POST'])
def export_database_async():
    """
    启用异步导出数据库数据到 CSV 文件。
    """
    data = request.get_json()
    db_name = data.get('db_name')
    limit = data.get('limit', 1000)

    try:
        db_manager = current_app.config['db_manager']
        database = db_manager.get_database(db_name)

        thread = Thread(target=async_export_to_csv, args=(database, db_name, limit))
        thread.start()  # 启动异步线程

        return jsonify({'status': SUCCESS, 'message': 'Export task started in background'})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


@data_mgmt_bp.route('/switch_database', methods=['POST'])
def switch_database():
    """
    切换访问的数据库。
    """
    data = request.get_json()
    db_name = data.get('db_name')

    try:
        db_manager = current_app.config['db_manager']
        db_manager.set_default_database({'db_name': db_name})  # 假设通过名称设置默认数据库
        return jsonify({'status': SUCCESS, 'message': f'Database switched to {db_name}'})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})
