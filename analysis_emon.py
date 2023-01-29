#pip3 install xlrd==1.2.0
#pip3 install openpyxl

import pandas as pd
import os
from openpyxl import load_workbook

queries_list=[]

def analysis(out_excel, summary_df_list, analysis_type, analysis_col_list, writer, is_transpose=0):
    analysis_df = pd.DataFrame(columns=["tpch-queries"])
    for i in range(len(queries_list)):
        j = queries_list[i]
        analysis_df.loc[j] = ['q'+str(j)]

    #print(analysis_df)    
    out_excel_sheet_name = analysis_type
    for col_name in analysis_col_list:
        print("--------------------------------- procss metrics " + col_name)
        col_list=[]
        for i in range(len(summary_df_list)):
            print("process file "+ str(i))                
            df = summary_df_list[i]
            col_value = df.loc[col_name,'aggregated']
            col_list.append(col_value)       
        
        analysis_df.loc[:,col_name] = col_list
    if is_transpose == 1:
        analysis_df = analysis_df.T
    print(analysis_df)
    analysis_df.to_excel(writer, sheet_name=out_excel_sheet_name)
    writer.save()
    writer.close()


out_excel = 'analysis.xlsx'
if os.path.isfile(out_excel):
    os.remove(out_excel)

dataframe = pd.DataFrame(list())
# writing empty DataFrame to the new csv file
dataframe.to_excel(out_excel)

summary_df_list=[]
for i in range(1,23):            
    in_excel = 'summary_q'+str(i)+'.xlsx'
    isExist = os.path.exists(in_excel)
    print("try file " + in_excel + " " + str(isExist))
    if isExist == True:
        print("========> read " +in_excel )
        in_excel_sheet_name = 'system view'        
        df = pd.read_excel(in_excel, sheet_name=in_excel_sheet_name, index_col=0)
        summary_df_list.append(df)
        queries_list.append(i)



ExcelWorkbook = load_workbook(out_excel)
writer = pd.ExcelWriter(out_excel, engine = 'openpyxl')
writer.book = ExcelWorkbook

analysis_list=['top-down', 'memory']
print("==============================> analysis top-down");
top_down_col_list=['metric_TMA_Retiring(%)','metric_TMA_Bad_Speculation(%)','metric_TMA_Frontend_Bound(%)', 'metric_TMA_Backend_Bound(%)']
analysis(out_excel, summary_df_list, 'top-down',top_down_col_list, writer)

print("==============================> analysis memory");
top_down_col_list=['metric_memory bandwidth read (MB/sec)','metric_memory bandwidth write (MB/sec)','metric_memory bandwidth total (MB/sec)', 'metric_NUMA %_Reads addressed to local DRAM','metric_NUMA %_Reads addressed to remote DRAM']
analysis(out_excel, summary_df_list, 'memroy',top_down_col_list, writer)

print("==============================> analysis CPU");
top_down_col_list=['metric_CPU operating frequency (in GHz)', 'metric_CPU utilization %', 'metric_CPU utilization% in kernel mode', 'metric_CPI', 'metric_kernel_CPI', 'metric_TMA_Frontend_Bound(%)', 'metric_TMA_..Fetch_Latency(%)', 'metric_TMA_....ICache_Misses(%)', 'metric_TMA_....ITLB_Misses(%)',
    'metric_TMA_....Branch_Resteers(%)', 'metric_TMA_..Fetch_Bandwidth(%)', 'metric_TMA_Bad_Speculation(%)', 'metric_TMA_..Branch_Mispredicts(%)', 'metric_TMA_Backend_Bound(%)', 'metric_TMA_Retiring(%)']
analysis(out_excel, summary_df_list, 'CPU',top_down_col_list, writer, 1)


print("==============================> analysis backend bound");
top_down_col_list=['metric_TMA_Backend_Bound(%)', 'metric_TMA_..Memory_Bound(%)', 'metric_TMA_....L1_Bound(%)', 'metric_TMA_......DTLB_Load(%)', 'metric_TMA_......Lock_Latency(%)', 'metric_TMA_......Split_Loads(%)', 'metric_TMA_......4K_Aliasing(%)',
'metric_TMA_......FB_Full(%)','metric_TMA_....L2_Bound(%)','metric_TMA_....L3_Bound(%)','metric_TMA_......Data_Sharing(%)','metric_TMA_......L3_Hit_Latency(%)','metric_TMA_......SQ_Full(%)','metric_TMA_....DRAM_Bound(%)','metric_TMA_......MEM_Bandwidth(%)'
,'metric_TMA_......MEM_Latency(%)','metric_TMA_........Local_DRAM(%)','metric_TMA_........Remote_DRAM(%)','metric_TMA_........Remote_Cache(%)','metric_TMA_....Store_Bound(%)','metric_TMA_......Store_Latency(%)','metric_TMA_......False_Sharing(%)','metric_TMA_......Split_Stores(%)'
,'metric_TMA_......Streaming_Stores(%)','metric_TMA_......DTLB_Store(%)','metric_TMA_..Core_Bound(%)','metric_TMA_....Divider(%)','metric_TMA_....Ports_Utilization(%)','metric_TMA_......Ports_Utilized_0(%)','metric_TMA_........Serializing_Operation(%)','metric_TMA_........Mixing_Vectors(%)','metric_TMA_......Ports_Utilized_1(%)'
,'metric_TMA_......Ports_Utilized_2(%)','metric_TMA_......Ports_Utilized_3m(%)','metric_TMA_........ALU_Op_Utilization(%)','metric_TMA_........Load_Op_Utilization(%)','metric_TMA_........Store_Op_Utilization(%)']
analysis(out_excel, summary_df_list, 'backend bound',top_down_col_list, writer, 1)

print("==============================> analysis cache and TLB");
top_down_col_list=['metric_CPU operating frequency (in GHz)', 'metric_CPU utilization %', 'metric_CPU utilization% in kernel mode', 'metric_CPI', 'metric_kernel_CPI', 'metric_L1D MPI (includes data+rfo w/ prefetches)', 'metric_L1D demand data read hits per instr', 'metric_L1-I code read misses (w/ prefetches) per instr',
'metric_L2 demand data read hits per instr', 'metric_L2 MPI (includes code+data+rfo w/ prefetches)', 'metric_L2 demand data read MPI', 'metric_L2 demand code MPI',
'metric_LLC MPI (includes code+data+rfo w/ prefetches)', 'metric_LLC code references hit in LLC per instr (prefetches included)', 'metric_LLC data read references hit in LLC per instr (prefetches included)', 'metric_LLC data read MPI (demand+prefetch)', 'metric_LLC code read MPI (demand+prefetch)', 
'metric_LLC all LLC prefetches (per instr)', 'metric_ITLB (2nd level) MPI', 'metric_ITLB (2nd level) large page MPI', 'metric_DTLB (2nd level) load MPI', 'metric_DTLB load miss latency (in core clks)', 'metric_DTLB store miss latency (in core clks)',
'metric_ITLB miss latency (in core clks)', 'metric_TMA_Frontend_Bound(%)', 'metric_TMA_..Fetch_Latency(%)', 'metric_TMA_....ICache_Misses(%)', 'metric_TMA_....ITLB_Misses(%)','metric_TMA_....Branch_Resteers(%)', 'metric_TMA_..Fetch_Bandwidth(%)', 'metric_TMA_Bad_Speculation(%)', 
'metric_TMA_..Branch_Mispredicts(%)', 'metric_TMA_Backend_Bound(%)', 'metric_TMA_Retiring(%)']
analysis(out_excel, summary_df_list, 'Cache and TLB',top_down_col_list, writer, 1)

print("==============================> analysis DTLB");
top_down_col_list=['metric_TMA_....L1_Bound(%)','metric_TMA_......DTLB_Load(%)','metric_TMA_........Load_STLB_Hit(%)', 'metric_TMA_........Load_STLB_Miss(%)', 'metric_TMA_......DTLB_Store(%)', 'metric_TMA_........Store_STLB_Hit(%)', 'metric_TMA_........Store_STLB_Miss(%)',
'metric_TMA_....L2_Bound(%)','metric_TMA_....L3_Bound(%)','metric_TMA_......DTLB_Store(%)','metric_TMA_........Store_STLB_Hit(%)', 'metric_TMA_........Store_STLB_Miss(%)',
'metric_ITLB (2nd level) MPI','metric_ITLB (2nd level) large page MPI', 'metric_STLB data page hits per instr', 'metric_DTLB (2nd level) load MPI','metric_DTLB (2nd level) store MPI',
'metric_DTLB load miss latency (in core clks)','metric_DTLB store miss latency (in core clks)','DTLB_LOAD_MISSES.STLB_HIT','DTLB_LOAD_MISSES.STLB_HIT:c1','DTLB_LOAD_MISSES.WALK_ACTIVE','DTLB_LOAD_MISSES.WALK_COMPLETED',
'DTLB_STORE_MISSES.STLB_HIT','DTLB_STORE_MISSES.STLB_HIT:c1','DTLB_STORE_MISSES.WALK_ACTIVE', 'DTLB_STORE_MISSES.WALK_COMPLETED']
analysis(out_excel, summary_df_list, 'DTLB',top_down_col_list, writer, 1)


print("==============================> analysis ITLB");
top_down_col_list=['metric_TMA_....ITLB_Misses(%)', 'metric_ITLB (2nd level) MPI', 'metric_ITLB (2nd level) large page MPI', 'metric_ITLB miss latency (in core clks)', 'metric_STLB data page hits per instr', 'ITLB_MISSES.STLB_HIT', 'ITLB_MISSES.WALK_ACTIVE', 'ITLB_MISSES.WALK_COMPLETED', 'ITLB_MISSES.WALK_COMPLETED_2M_4M','metric_TMA_....ICache_Misses(%)', 'metric_L1-I code read misses (w/ prefetches) per instr', 'ICACHE_DATA.STALLS', 'ICACHE_TAG.STALLS']
analysis(out_excel, summary_df_list, 'ITLB',top_down_col_list, writer, 1)
