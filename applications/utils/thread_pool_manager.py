import threading
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Callable, Any, Dict, Optional, List


class ThreadPoolManager:
    """
    线程池管理类（支持为每个任务提供独立的停止事件）
    """

    # 单例模式：共享一个线程池实例
    _executor: Optional[ThreadPoolExecutor] = None
    _lock = threading.Lock()  # 确保线程池的线程安全
    _task_events: Dict[Future, threading.Event] = {}  # 存储每个任务的 Future 与对应的 stop_event 映射
    _app_context = None

    @staticmethod
    def _init_pool(max_workers: int):
        """
        初始化线程池（私有方法，用来懒加载线程池）
        """
        with ThreadPoolManager._lock:
            if ThreadPoolManager._executor is None:
                ThreadPoolManager._executor = ThreadPoolExecutor(max_workers=max_workers)
                print(f"线程池初始化完成，最大线程数：{max_workers}")

    @staticmethod
    def initialize(max_workers: int = 5, app=None):
        """
        初始化线程池（懒加载方法）
        """
        ThreadPoolManager._init_pool(max_workers)
        ThreadPoolManager._app_context = app

    @staticmethod
    def submit_task(func: Callable, *args, **kwargs) -> Future:
        """
        提交任务到线程池，自动生成独立的 stop_event 并绑定到任务
        """
        if ThreadPoolManager._executor is None:
            raise RuntimeError("线程池尚未初始化，请先调用 'initialize' 方法!")

        # 为任务创建独立的 stop_event
        stop_event = threading.Event()
        kwargs['stop_event'] = stop_event  # 将 stop_event 作为任务的参数传入
        kwargs['app'] = ThreadPoolManager._app_context
        # 提交任务
        future = ThreadPoolManager._executor.submit(func, *args, **kwargs)

        # 存储任务的 Future 和 stop_event 的映射关系
        ThreadPoolManager._task_events[future] = stop_event

        print(f"任务提交成功：{func.__name__}，参数：{args}, {kwargs}")
        return future

    @staticmethod
    def stop_task(future: Future):
        """
        停止指定任务（触发该任务的 stop_event）
        """
        if future in ThreadPoolManager._task_events:
            stop_event = ThreadPoolManager._task_events[future]
            stop_event.set()  # 触发停止事件
            print(f"任务 {future} 的停止事件已触发。")
        else:
            print("任务不存在，无法触发停止事件。")

    @staticmethod
    def shutdown(wait: bool = True) -> None:
        """
        关闭线程池并清理所有任务及其 stop_event
        """
        if ThreadPoolManager._executor:
            # 清理所有任务的 stop_event
            for stop_event in ThreadPoolManager._task_events.values():
                stop_event.set()  # 触发所有任务的停止事件

            ThreadPoolManager._executor.shutdown(wait=wait)
            print("线程池已关闭。")
            ThreadPoolManager._executor = None

        # 清空任务与事件的映射关系
        ThreadPoolManager._task_events.clear()

    @staticmethod
    def execute_many(tasks: List[Callable], *args, **kwargs) -> List[Any]:
        """
        执行多个任务，并等待所有任务完成
        :param tasks: 任务列表，包含多个函数
        :param args: 通用参数（所有函数共享参数）
        :param kwargs: 通用关键字参数
        :return: 返回所有任务的结果列表
        """
        if ThreadPoolManager._executor is None:
            raise RuntimeError("线程池尚未初始化，请先调用 'initialize' 方法!")

        # 提交所有任务到线程池
        futures = [ThreadPoolManager.submit_task(task, *args, **kwargs) for task in tasks]

        # 等待任务完成，并收集结果
        results = []
        for future in as_completed(futures):
            results.append(future.result())
        return results