# 告警事件任务状态

STATUS_NO_RESPONSE = 'NO_RESPONSE'
STATUS_PROCESSING = 'PROCESSING'
STATUS_RESOLVED = 'RESOLVED'
STATUS_REVOKED = 'REVOKED'
STATUS_TIMEOUT = 'TIMEOUT'

# 需要升级的告警状态
STATUS_NEED_UPGRADE = [STATUS_NO_RESPONSE]

# 未关闭事件列表
STATUS_NOT_CLOSED = [0, 1, 2, 3]

# 资源类型的消息
RESOURCE_TYPE = ['HostHighCpuLoad', 'HostOutOfMemory', 'HostOutOfDiskSpace',
                 'HostHighCpu1mAverageLoad', 'HostHighCpu5mAverageLoad', 'HostHighCpu15mAverageLoad']

# 资源标记
RES_TAG = 'res_mark'
# 已发送告警消息标记
DELAY_SEND_TAG = 'delay_send'
# 查看延时的关联时间,单位小时
DELAY_TIME = 2