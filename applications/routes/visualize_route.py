from logging import getLogger

from flask import Blueprint, jsonify, request, current_app

from server_status import SUCCESS, FAILURE

viz_bp = Blueprint('visualization', __name__)
logger = getLogger(__name__)

@viz_bp.route('/get_table_list', methods=['GET'])
def get_table_list():
    """
    功能：返回数据库中的所有表列表
    """
    try:
        db_manager = current_app.config['db_manager']
        tables = db_manager.get_all_tables()
        return jsonify({'status': SUCCESS, 'tables': tables})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


@viz_bp.route('/get_table_preview', methods=['POST'])
def get_table_preview():
    """
    功能：获取选定表的预览数据
    """
    data = request.get_json()
    table_name = data.get('table_name')
    limit = data.get('limit', 10)

    try:
        db_manager = current_app.config['db_manager']
        preview_data = db_manager.get_preview_data(table_name, limit)
        return jsonify({'status': SUCCESS, 'preview': preview_data})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})

@viz_bp.route('/get_table_columns', methods=['POST'])
def get_table_columns():
    """
    功能：获取表的字段列表
    """
    data = request.get_json()
    table_name = data.get('table_name')

    try:
        db_manager = current_app.config['db_manager']
        columns = db_manager.get_table_columns(table_name)
        return jsonify({'status': SUCCESS, 'columns': columns})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})

import matplotlib.pyplot as plt
import io
import base64


@viz_bp.route('/generate_line_chart', methods=['POST'])
def generate_line_chart():
    """
    功能：生成线图
    """
    data = request.get_json()
    table_name = data.get('table_name')
    x_field = data.get('x_field')
    y_field = data.get('y_field')

    try:
        db_manager = current_app.config['db_manager']
        dataset = db_manager.get_data_for_fields(table_name, x_field, y_field)

        # 使用 Matplotlib 生成图表
        plt.figure()
        plt.plot(dataset[x_field], dataset[y_field], color='blue', marker='o')
        plt.xlabel(x_field)
        plt.ylabel(y_field)
        plt.title(f"{y_field} vs {x_field}")

        # 保存为图像
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({'status': SUCCESS, 'chart': f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})

@viz_bp.route('/generate_bar_chart', methods=['POST'])
def generate_bar_chart():
    """
    功能：生成柱状图
    """
    data = request.get_json()
    table_name = data.get('table_name')
    x_field = data.get('x_field')
    y_field = data.get('y_field')

    try:
        db_manager = current_app.config['db_manager']
        dataset = db_manager.get_data_for_fields(table_name, x_field, y_field)

        # 使用 Matplotlib 生成柱状图
        plt.figure()
        plt.bar(dataset[x_field], dataset[y_field], color='orange')
        plt.xlabel(x_field)
        plt.ylabel(y_field)
        plt.title(f"{y_field} by {x_field}")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({'status': SUCCESS, 'chart': f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})

@viz_bp.route('/generate_pie_chart', methods=['POST'])
def generate_pie_chart():
    """
    功能：生成饼图
    """
    data = request.get_json()
    table_name = data.get('table_name')
    category_field = data.get('category_field')
    value_field = data.get('value_field')

    try:
        db_manager = current_app.config['db_manager']
        dataset = db_manager.get_data_for_fields(table_name, category_field, value_field)

        # 使用 Matplotlib 生成饼图
        plt.figure()
        plt.pie(dataset[value_field], labels=dataset[category_field], autopct='%1.1f%%',
                colors=['blue', 'green', 'red'])
        plt.title(f"{value_field} Distribution")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({'status': SUCCESS, 'chart': f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})

@viz_bp.route('/get_multiple_datasets', methods=['POST'])
def get_multiple_datasets():
    """
    功能：合并选中的数据源，准备用于可视化
    """
    data = request.get_json()
    tables_info = data.get('tables_info')  # 包含 {table_name, x_field, y_field} 列表

    try:
        db_manager = current_app.config['db_manager']
        datasets = []
        for table_info in tables_info:
            dataset = db_manager.get_data_for_fields(table_info['table_name'], table_info['x_field'],
                                                     table_info['y_field'])
            datasets.append({'table': table_info['table_name'], 'data': dataset})

        return jsonify({'status': SUCCESS, 'datasets': datasets})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})
