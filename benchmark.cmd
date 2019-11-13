@echo off

echo size,alg,time > benchmark.log
for %%s in ("10" "100" "1000" "10000") do (
    for %%a in ("fg" "ew" "lp" "ml" "im" "eb") do (
        python benchmark.py %%s %%a >> benchmark.log
    )
)
