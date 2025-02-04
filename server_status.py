"""
Server return status define file
"""

### 1. 通用状态
SUCCESS = 0			# 操作成功完成
FAILURE = 1			# 操作失败
PENDING = 2			# 操作正在处理中，尚未完成
TIMEOUT = 3			# 操作超时，未能在规定时间内完成
RETRYING = 4		# 操作正在重试中

### 2. 数据相关状态
DATA_FOUND = 10			# 成功找到请求的数据
DATA_NOT_FOUND = 11		# 未找到请求的数据
DATA_INVALID = 12		# 提供的数据无效或不合法
DATA_CONFLICT = 13		# 数据冲突（如唯一键重复）
DATA_UPDATED = 14		# 数据已成功更新
DATA_DELETED = 15		# 数据已成功删除

### 3. 权限相关状态
AUTHORIZED = 20			# 请求已授权
UNAUTHORIZED = 21		# 请求未授权，需要登录或权限验证
FORBIDDEN = 22			# 请求被禁止，用户无权限访问
PERMISSION_DENIED = 23	# 权限不足，无法执行操作

### 4. 资源相关状态
RESOURCE_AVAILABLE = 30			# 资源可用
RESOURCE_UNAVAILABLE = 31		# 资源不可用
RESOURCE_EXHAUSTED = 32			# 资源耗尽（如内存、磁盘空间）
RESOURCE_LOCKED = 33			# 资源被锁定，无法访问

### 5. 网络相关状态
CONNECTED = 40			    # 连接成功
DISCONNECTED = 41			# 连接断开
CONNECTION_FAILED = 42		# 连接失败
NETWORK_ERROR = 43			# 网络错误

### 6. 文件相关状态
FILE_UPLOADED = 50			# 文件上传成功
FILE_UPLOAD_FAILED = 51		# 文件上传失败
FILE_DOWNLOADED = 52		# 文件下载成功
FILE_DOWNLOAD_FAILED = 53	# 文件下载失败
FILE_NOT_FOUND = 54			# 文件未找到

### 7. 任务相关状态
TASK_STARTED = 60			# 任务已启动
TASK_COMPLETED = 61			# 任务已完成
TASK_FAILED = 62			# 任务失败
TASK_CANCELLED = 63			# 任务已取消
TASK_QUEUED = 64			# 任务已加入队列，等待执行

### 8. 验证相关状态
VALIDATION_PASSED = 70			# 验证通过
VALIDATION_FAILED = 71			# 验证失败
INVALID_INPUT = 72			    # 输入无效
MISSING_REQUIRED_FIELD = 73		# 缺少必填字段

### 9. API 相关状态
API_CALL_SUCCESSFUL = 80		# API 调用成功
API_CALL_FAILED = 81			# API 调用失败
RATE_LIMIT_EXCEEDED = 82		# 超出 API 调用频率限制
ENDPOINT_NOT_FOUND = 83			# API 端点未找到

### 10. 缓存相关状态
CACHE_HIT = 90			# 缓存命中
CACHE_MISS = 91			# 缓存未命中
CACHE_UPDATED = 92		# 缓存已更新
CACHE_EXPIRED = 93		# 缓存已过期

### 11. 自定义状态
CUSTOM_STATUS_1 = 100		# 自定义状态1
CUSTOM_STATUS_2 = 101		# 自定义状态2