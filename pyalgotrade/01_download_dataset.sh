#!/bin/sh

python -m "pyalgotrade.tools.quandl" --source-code="WIKI" --table-code="ORCL" --from-year=2016 --to-year=2019 --storage=./data/ --force-download --frequency=daily