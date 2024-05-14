#!/bin/bash

# 使用 grep 和 awk 从 ps 命令的输出中提取 observer 进程的 PID
PIDS=($(ps -ef | grep observer | grep -v grep | awk '{print $2}'))

# 核心范围数组
CORE_RANGES=("0-15" "16-31" "32-47" "48-63" "64-79" "80-95" "96-111" "112-127" "128-143")

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
        echo "PID 的数量超过了核心范围的数量"
        break  # 跳出循环，如果 PID 的数量超过了核心范围的数量
    fi
done

