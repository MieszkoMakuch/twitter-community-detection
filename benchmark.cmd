@echo off

echo size,alg,time > benchmark.log
for %%s in ("10000") do (
    for %%a in ("lp" "ml") do (
        python benchmark.py %%s %%a >> benchmark.log
    )
)
