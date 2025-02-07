from flask import Blueprint, request, jsonify
import os
import shutil
import uuid
import time
from threading import Thread, Event
import json

# 模拟数据库连接模块和模型处理模块
from applications.models.model_ml import MLModel
from server_status import SUCCESS, FAILURE

ml_bp = Blueprint("ml", __name__)
inference_tasks = {}  # 全局保存异步推理任务：task_id -> {status, result}


@ml_bp.route('/ml_interface', methods=['POST'])
def ml_interface():
    """
    功能：机器学习模型选择，缓存模型并存数据库
    """
    data = request.get_json()
    ml_name = data.get('ml_name')
    ml_type = data.get('ml_type')
    ml_model_path = data.get('ml_model')

    # 优化: 如果用户拖动模型文件加载
    if data.get('drag_file'):
        ml_name = os.path.splitext(os.path.basename(ml_model_path))[0]

    # 存储模型到工程目录
    project_model_path = f"./ml_models_cache/{ml_name}/"
    try:
        if not os.path.exists(project_model_path):
            os.makedirs(project_model_path)
        shutil.copy(ml_model_path, project_model_path)
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': f'Error copying model: {str(e)}'})

    # 保存模型参数到数据库
    ml_model = MLModel()
    result = ml_model.add_model({
        "ml_name": ml_name,
        "ml_type": ml_type,
        "ml_path": project_model_path
    })

    if result:
        return jsonify({'status': SUCCESS, 'message': 'Model saved successfully.'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Failed to save model.'})


@ml_bp.route('/ml_script', methods=['POST'])
def ml_script():
    """
    功能：自定义推理脚本支持
    """
    data = request.get_json()
    script_name = data.get('ml_name')
    script_path = data.get('ml_model')

    # 优化: 如果用户拖动脚本文件加载
    if data.get('drag_file'):
        script_name = os.path.splitext(os.path.basename(script_path))[0]

    # 存储脚本到工程目录
    project_script_path = f"./scripts_cache/{script_name}/"
    try:
        if not os.path.exists(project_script_path):
            os.makedirs(project_script_path)
        shutil.copy(script_path, project_script_path)
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': f'Error copying script: {str(e)}'})

    # 添加到数据库
    ml_model = MLModel()
    result = ml_model.add_model({
        "ml_name": script_name,
        "ml_type": "script",
        "ml_path": project_script_path
    })

    if result:
        return jsonify({'status': SUCCESS, 'message': 'Script saved successfully.'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Failed to save script.'})


@ml_bp.route('/ml_inference', methods=['POST'])
def ml_inference():
    """
    功能：加载模型或脚本，选择数据，执行推理
    """
    data = request.get_json()
    ml_name = data.get('ml_name')
    input_data = data.get('input_data')
    is_async = data.get('async', False)

    # 从数据库加载模型
    ml_model = MLModel()
    model_info = ml_model.get_model(ml_name)

    if not model_info:
        return jsonify({'status': FAILURE, 'message': 'Model not found'})

    # 预处理数据: 假设数据格式化逻辑在 preprocess_data 函数中
    preprocessed_data = preprocess_data(input_data)

    # 异步推理
    if is_async:
        task_id = str(uuid.uuid4())
        thread = Thread(target=async_inference, args=(task_id, model_info, preprocessed_data))
        thread.start()
        inference_tasks[task_id] = {"status": "running", "result": None}
        return jsonify({'status': SUCCESS, 'task_id': task_id, 'message': 'Inference started.'})

    # 同步推理
    result = run_inference(model_info, preprocessed_data)
    if result:
        save_inference_result(ml_name, result)
        return jsonify({'status': SUCCESS, 'result': result})
    else:
        return jsonify({'status': FAILURE, 'message': 'Inference failed'})


def async_inference(task_id, model_info, preprocessed_data):
    """
    在独立线程中执行异步推理
    """
    try:
        result = run_inference(model_info, preprocessed_data)
        save_inference_result(model_info["ml_name"], result)
        inference_tasks[task_id]["status"] = "completed"
        inference_tasks[task_id]["result"] = result
    except Exception as e:
        inference_tasks[task_id]["status"] = "failed"
        inference_tasks[task_id]["result"] = str(e)


def run_inference(model_info, data):
    """
    实际执行推理逻辑
    """
    if model_info["ml_type"] == "script":
        # 执行外部脚本
        script_path = os.path.join(model_info["ml_path"], "inference.py")
        # 模拟执行脚本，返回推理结果
        result = os.system(f"python {script_path} {json.dumps(data)}")
        return result
    else:
        # 使用模型库加载模型进行推理 (假设为 scikit-learn 或 tensorflow)
        model_path = os.path.join(model_info["ml_path"], "model.pkl")
        # 模拟加载模型进行推理
        result = {"prediction": [0, 1, 0, 1]}  # 假设的推理结果
        return result


def save_inference_result(ml_name, result):
    """
    保存推理结果到数据库/文件
    """
    timestamp = time.time()
    result_id = f"{ml_name}_{int(timestamp)}"
    file_path = f"./results/{result_id}.json"
    if not os.path.exists('./results'):
        os.makedirs('./results')
    with open(file_path, 'w') as result_file:
        json.dump({'ml_name': ml_name, 'timestamp': timestamp, 'result': result}, result_file)
    return result_id


@ml_bp.route('/ml_output_raw', methods=['GET'])
def ml_output_raw():
    """
    显示原始推理结果
    """
    data = request.get_json()
    result_id = data.get('result_id')
    try:
        with open(f"./results/{result_id}.json", 'r') as result_file:
            result = json.load(result_file)
            return jsonify({'status': SUCCESS, 'data': result})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})


@ml_bp.route('/ml_output_file', methods=['POST'])
def ml_output_file():
    """
    将推理结果保存到文件
    """
    data = request.get_json()
    result_id = data.get('result_id')
    save_path = data.get('save_path', './exported_results')

    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        shutil.copy(f"./results/{result_id}.json", save_path)
        return jsonify({'status': SUCCESS, 'message': f'Result saved to {save_path}'})
    except Exception as e:
        return jsonify({'status': FAILURE, 'message': str(e)})