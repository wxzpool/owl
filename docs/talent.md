# talent设计思路

talent是owl系统的核心，其主要用途是用于owl子系统与overlord的交互

其本质实现基于grpc实现

功能需求

1. 任务管理
    - 从overlord接受任务，保存入库
    - 向supervisor提供服务，获取任务列表
    - 向log_receiver提供服务，回写任务状态
    
    plot_task_create(task_id, p图参数) 从overlord生成任务
    plot_task_stop(task_id) 强制停止p图任务
    plot_task_status(task_id, status) 显示本地执行的任务状态，如果未指定task_id则本地所有符合status状态的任务
    plot_task_update(task_id) 更新任务状态
    get_plot_tasks() 获取所有pending状态的任务

   PlotTaskStatusResponse type:
        - on_create
        - on_stop
   
    P图阶段说明

    启动Start：    

    overlord发起 -> talent接收 -> supervisor分配 -> 进程启动 -> log_receiver监控

    initialized -> received -> pending -> started -> running(supervisor持续监控) -> finished

    拦截Stop：

    overlord发起 -> talent接收 -> supervisor拦截

    scheduled -> received -> stopping -> stopped

    任务失败:

    supervisor监控 -> 进程丢失 -> 回报

    failed
    
    数据结构
   
    表名: plot_tasks
   
    | 字段名 | 类型 | 用途 | 默认值 | 备注 | 
    | --- | --- | --- | --- | --- |
    | id | int 自增 | 排序 | 自增字段 | |
    | create_time | datetime | 记录创建时间 | |
    | update_time | datetime | 记录最后修改时间 | | 
    | worker_id | string32 | 本机的唯一标识 | 不为空，必填 | uuid4 |
    | task_id | string32 | 任务唯一标识 | 不为空，必填 | uuid4 |
    | plot_pid | int | 任务对应的进程号 | null | 由supervisor回写 |
    | log_pid | int | 任务对应的日志收集器进程号 | null | 由supervisor回写 |
    | status | string | 当前任务状态 | received | 由talent、supervisor、log_receiver共同写 |
    | plot_id | string | plot 进程生成的id | null | 由log_receiver回写 |
    | fpk | string | Farmer公钥 | null | 由talent的plot_task_create写入 |
    | ppk | string | Pool公钥 | null | 由talent的plot_task_create写入 |
    | memo | string | memo | null | 由talent的plot_task_create写入 |
    | ksize | int | p图大小 | 不为空，必填 | 由talent的plot_task_create写入 |
    | cache1 | string | cache1的路径 | 不为空，必填 | 由talent的plot_task_create写入 |
    | cache2 | string | cache2的路径 | 不为空，必填 | 由talent的plot_task_create写入 |
    | threads | int | p图进程cpu使用数量 | 不为空，必填 | 由talent的plot_task_create写入 |
    | buffer | int | p图进程内存使用量(MiB) | 不为空，必填 | 由talent的plot_task_create写入 |
    | stripe_size | int | stripe size | null | 由log_receiver回写 |
    | buckets | int | buckets size | null | 由log_receiver回写 |
    | progress | float | 进度 | 0.0 | 由log_receiver回写 |
    | p1_t1_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t1_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t2_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t2_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t3_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t3_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t4_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t4_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t5_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t5_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t6_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t6_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_t7_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p1_t7_cpu | float | 该阶段cpu使用 | null | 由log_receiver回写 |
    | p1_total_time | float | p1总耗时 | null | 由log_receiver回写 |
    | p1_total_cpu | float | p1总耗用cpu | null | 由log_receiver回写 |
    | p1_table_1_now_size | int | table_1_now_size大小 | null | 由log_receiver回写 |
    | p2_t7_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t7_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t6_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t6_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t5_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t5_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t4_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t4_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t3_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t3_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t2_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t2_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t1_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_t1_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p2_total_time | float | p2总耗时 | null | 由log_receiver回写 |
    | p2_total_cpu | float | p2总耗用cpu | null | 由log_receiver回写 |
    | p3_t1_2_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t1_2_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t2_3_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t2_3_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t3_4_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t3_4_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t4_5_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t4_5_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t5_6_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t5_6_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t6_7_time | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_t6_7_cpu | float | 该阶段花费时间 | null | 由log_receiver回写 |
    | p3_total_time | float | p3总耗时 | null | 由log_receiver回写 |
    | p3_total_cpu | float | p3总耗用cpu | null | 由log_receiver回写 |
    | p4_total_time | float | p4总耗时 | null | 由log_receiver回写 |
    | p4_total_cpu | float | p4总耗用cpu | null | 由log_receiver回写 |
    | total_time | float | p1-4总耗时 | null | 由log_receiver回写 |
    | total_cpu | float |  p1-4总耗用cpu | null | 由log_receiver回写 |
    | copy_time | float | 复制时间 | null | 由log_receiver回写 |
    | copy_cpu | float | 复制耗用cpu | null | 由log_receiver回写 |
    | dest_type | string | 最终写入的类型 | nfs | (local|nfs) 由talent的plot_task_create写入 |
    | dest_path | string | 最终写入路径 | 不为空，必填 | 由talent的plot_task_create写入 |
    | dest_file_name | string | 最终文件名 | null | 由log_receiver回写 |
    
    

   