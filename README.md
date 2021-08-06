# Trading Python Project

This python project aims to parse & summarise trading data.

## Description

This project takes an input csv file (`input.csv`) and outputs another csv file (`output.csv`).

The input file must be formatted with the following columns: `TimeStamp`, `Symbol`, `Quantity` and `Price`.

The output file produced will have the following columns: `Symbol`, `MaxTimeGap`, `Volume`, `WeightedAveragePrice` and `MaxPrice`.

## Definitions

Precise definitios of the output columns are as follows:

- `Symbol`: the symbol of the instrument being traded.
- `Maximum time gap`: 'time gap' is the amount of time that passes between consecutive trades of a symbol. If only 1 trade is in the file then the gap is 0.
- `Total volume traded`: sum of the quantity for all trades in a symbol).
- `Maximum trade price`: the highest price per unit in a single trade.
- `Weighted average price`: average price per unit traded (not per trade). Result is truncated to whole numbers.

NB: `main_old.py` is a first attempt at implementing this project. While it outputs the correct csv file, the implementation is flawed and inflexible. `main.py` is the improved version.