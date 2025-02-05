from flask import Blueprint, request, current_app

data_mgmt_bp = Blueprint('data_mgmt', __name__)


@data_mgmt_bp.route('/select_database')
def select_database():
    """
    TODO: 用户选择当前操作的数据库

    数据库包含的基本信息有：
    1.db_name名称（users）
    2.db_type类型（sqlite，mysql等等）
    3.db_path路径（例如sqlite:///users.db）

    用户通过下拉框选择数据库，或者手动输入自定义的数据库；
    数据库选项显示格式为 *名称(路径)*，手动输入格式自定；
    数据库被设置为db_manager管理的默认数据库，用户的 *查询* 操作均访问该数据库；
    """
    pass


@data_mgmt_bp.route('/refresh_database')
def refresh_database():
    """
    TODO: 刷新当前数据库
    :return:
    """
    pass


@data_mgmt_bp.route('/show_database')
def show_database():
    """
    TODO: 显示当前数据库数据

    用户选择数据库，查询数据库；
    后端检查用户权限，访问数据库，返回数据库条目数量；
    用户可以根据数据量大小选择显示方式：软件内显示db_show，输出为本地cvs文件db_file；
    后端逐一查询数据库条目，进行输出（大文件卡顿风险，考虑异步或是开辟线程执行）；
    :return:
    """
    pass


@data_mgmt_bp.route('/switch_database')
def switch_database():
    """
    TODO: 切换显示数据库

    :return:
    """
    pass
