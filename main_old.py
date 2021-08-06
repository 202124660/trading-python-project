import time


class Instrument:
    def __init__(self):
        self.all_trades = []
        self.by_symbol_all_trades = {}
        self.by_symbol_output_values = {}
        self.symbols = []
        self.volume_has_been_calculated = False

    def csv_to_list(self, filename='input.csv'):
        with open(filename) as input_file:
            for line in input_file:
                split_line = line.split(',')
                self.all_trades.append([int(split_line[0]), split_line[1], int(split_line[2]), int(split_line[3])])  # store in list of lists and convert to appropriate datatypes

    def group_by_symbol(self):
        for trade in self.all_trades:  # loop over all trades from input csv
            symbol = trade[1]
            if symbol in self.symbols:  # check if symbol already exists in symbol index list
                self.by_symbol_all_trades[symbol].append(trade)  # find index of symbol and insert trade data at that index
            else:
                self.symbols.append(symbol)  # add newly identified symbol to symbol index list
                self.by_symbol_all_trades[symbol] = [trade]  # insert trade data for new symbol in a new list for that symbol

    def create_dictionary_by_symbol(self):
        if self.by_symbol_output_values == {}:
            for symbol in self.symbols:
                self.by_symbol_output_values[symbol] = {}

    def find_max_time_gap(self):
        self.create_dictionary_by_symbol()
        for symbol, symbol_trades in self.by_symbol_all_trades.items():  # loop over each group of trades with the same symbol
            time_gaps_for_symbol = []
            if len(symbol_trades) > 1:  # check that there is more than one trade for this symbol
                for trade_num in range(1, len(symbol_trades)):  # loop over each trade for this symbol, starting with the 2nd trade (as we're taking trades in pairs)
                    # if trade_num != 1:  # check that this isn't the first pair of trades for this symbol
                    time_gaps_for_symbol.append(symbol_trades[trade_num][0] - symbol_trades[trade_num-1][0])  # find index of symbol and insert time gap for this pair of trades
                    # else:
                    #     time_gaps_for_symbol = [symbol_trades[trade_num][0] - symbol_trades[trade_num - 1][0]]  # insert time gap for new symbol in a new list for that symbol
            else:
                time_gaps_for_symbol = [0]  # if only 1 trade for that symbol, insert 0 as the only time gap
            self.by_symbol_output_values[symbol]['MaxTimeGap'] = max(time_gaps_for_symbol)  # insert max time gap for this symbol to new dict

    def find_total_volume(self):
        self.create_dictionary_by_symbol()
        for symbol, symbol_trades in self.by_symbol_all_trades.items():  # loop over each group of trades with the same symbol
            total_vol = 0  # total volume counter for this symbol
            for trade in symbol_trades:  # loop over each trade for this symbol
                total_vol += trade[2]  # add trade quantity to the total volume counter
            self.by_symbol_output_values[symbol]['Volume'] = total_vol  # insert total volume for this symbol to new dict
        self.volume_has_been_calculated = True

    def find_weighted_avg_price(self):
        if not self.volume_has_been_calculated:  # check if total volume hasn't yet been calculated, as this will be needed for calculations
            self.find_total_volume()  # if it hasn't, then use find_total_volume() method to store total volume for each symbol
        for symbol, symbol_trades in self.by_symbol_all_trades.items():  # loop over each group of trades with the same symbol
            symbol_total = 0  # total 'quantity * price' counter for this symbol, to be divided by total volume later
            for trade in symbol_trades:  # loop over each trade for this symbol
                symbol_total += trade[2] * trade[3]  # add trade quantity to the total volume counter
            symbol_weighted_avg_price = symbol_total / self.by_symbol_output_values[symbol]['Volume']  # divide 'quantity * price' counter for this symbol by symbol's total volume, to get weighted avg price
            self.by_symbol_output_values[symbol]['WeightedAveragePrice'] = int(symbol_weighted_avg_price)  # insert truncated weighted avg price for this symbol to new dict

    def find_max_price(self):
        for symbol, symbol_trades in self.by_symbol_all_trades.items():  # loop over each group of trades with the same symbol
            symbol_max_price = 0  # variable to store current highest price for this symbol, starting at 0
            for trade in symbol_trades:  # loop over each trade for this symbol
                if trade[3] > symbol_max_price:  # check whether this trade has higher price than current max
                    symbol_max_price = trade[3]  # and if so, replace 'highest price' variable with new, higher, price
            self.by_symbol_output_values[symbol]['MaxPrice'] = symbol_max_price  # insert max price for this symbol to new dict

    def write_outputs(self, filename='output.csv'):
        sorted_dict = {k: self.by_symbol_output_values[k] for k in sorted(self.by_symbol_output_values)}  # fastest dictionary sort, source: https://stackoverflow.com/questions/50493838/fastest-way-to-sort-a-python-3-7-dictionary
        with open(filename, "w") as output_file:
            for symbol in sorted_dict.keys():  # loop over each symbol
                output_file.write(f'{symbol},{",".join(str(val) for val in [*sorted_dict[symbol].values()])}\n')  # unpacks vals to list using *, then converts vals to strings, then adds commas between vals and adds the symbol to the front. '*' was used for faster speed with small dicts (https://stackoverflow.com/questions/16228248/how-can-i-get-list-of-values-from-dict)

    # def sort_alphabetically(self, list_of_lists):
    #     sorted_list = sorted(list_of_lists, key=lambda x: x[0])
    #     return sorted_list


if __name__ == '__main__':
    start_time = time.time()
    instrument = Instrument()
    time1 = time.time()
    instrument.csv_to_list(filename='input.csv')
    time2 = time.time()
    instrument.group_by_symbol()
    time3 = time.time()
    instrument.find_max_time_gap()
    time4 = time.time()
    instrument.find_total_volume()
    time5 = time.time()
    instrument.find_weighted_avg_price()
    time6 = time.time()
    instrument.find_max_price()
    time7 = time.time()
    instrument.write_outputs(filename='output.csv')
    end_time = time.time()

    t1 = time1-start_time
    t2 = time2-time1
    t3 = time3-time2
    t4 = time4-time3
    t5 = time5-time4
    t6 = time6-time5
    t7 = time7-time6
    t8 = end_time-time7

    times_list = [t1, t2, t3, t4, t5, t6, t7, t8]
    for num, i in enumerate(times_list):
        print(num, '{:g}'.format(float('{:.{p}g}'.format(i, p=3))))
    print('Total time:', end_time-start_time)
    # print('sped up writer')
