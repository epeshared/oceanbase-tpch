#!/bin/bash

# taskset -cp 0-15 166959
# taskset -cp 16-31 168708
# taskset -cp 32-47 170528
# taskset -cp 48-63 172366
# taskset -cp 64-79 174116
# taskset -cp 80-95 175888
# taskset -cp 96-111 177632
# taskset -cp 112-127 179398
# taskset -cp 128-143 181163

# 使用 grep 和 awk 从 ps 命令的输出中提取 observer 进程的 PID
PIDS=($(ps -ef | grep observer | grep -v grep | awk '{print $2}'))

# 核心范围数组
CORE_RANGES=("0-7,80-87" "8-15,88-95" "16-23,96-103" "24-31,104-111" "32-39,112-119")

# 检查 PID 数量是否大于或等于核心范围数组的长度
if [ ${#PIDS[@]} -lt ${#CORE_RANGES[@]} ]; then
    echo "Warning: Not enough PIDs found for all core ranges."
fi

# 遍历 PIDS 和 CORE_RANGES
for i in "${!PIDS[@]}"; do
    if [ $i -lt ${#CORE_RANGES[@]} ]; then
        if ps -p ${PIDS[$i]} > /dev/null; then
            echo "===>taskset -cpa ${CORE_RANGES[$i]} ${PIDS[$i]}"
            taskset -cpa ${CORE_RANGES[$i]} ${PIDS[$i]}
            echo "Set PID ${PIDS[$i]} to cores ${CORE_RANGES[$i]}"
        else
            echo "PID ${PIDS[$i]} not found."
        fi
    else
        break  # 跳出循环，如果 PID 的数量超过了核心范围的数量
    fi
done

