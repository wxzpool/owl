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