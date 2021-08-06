# Trading Python Project

This python project aims to parse & summarise trading data.

## Description

This project takes an input csv file (`input.csv`) and outputs another csv file (`output.csv`).

The input file must be formatted with the following columns: `TimeStamp`,`Symbol`,`Quantity`,`Price`.

The output file produced will have the following columns: `symbol`,`MaxTimeGap`,`Volume`,`WeightedAveragePrice`,`MaxPrice`.

## Definitions

- `Symbol`: the symbol of the instrument being traded.
- `Maximum time gap`: 'time gap' is the amount of time that passes between consecutive trades of a symbol. If only 1 trade is in the file then the gap is 0.
- `Total Volume traded`: sum of the quantity for all trades in a symbol).
- `Max Trade Price`: self-explanatory.
- `Weighted Average Price`: average price per unit traded (not per trade). Result is truncated to whole numbers.
