# fund_pool_multi

1. 基于天天基金网站的爬虫。通过四分卫法和其他相关指标，筛选出基金池，仅供参考。

   - 参考[fun_pool](https://github.com/sdohurt/fund_pool)

   执行步骤：

   - 安装所需的 python 第三方模块（安装语法 pip install <模块名>）
   - 在根目录下打开命令行窗口，执行 python main.py
   - 执行 python filter.py

2. 根据中国证券评选出的基金作为基础基金池。通过五四三二法则和其他相关指标，筛选出基金池，仅供参考。

   - 五四三二法则（近五年在同类排名在 1/5 以内，近三年在同类排名在 1/4 以内，近两年在同类排名在 1/3 以内，近一年在同类排名在 1/2 以内）

   执行步骤：

   - 安装所需的 python 第三方模块（安装语法 pip install <模块名>）
   - 在根目录下打开命令行窗口，执行 python main-golden.py
   - 执行 python filter-golden.py
