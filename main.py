class Instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.all_trades = []  # stores every trade for this instrument that comes in, in order
        self.instrument_dict = {}  # stores running totals of output values
        self.keys = ('TimeStamp', 'Quantity', 'Price')
        self.cost_of_all_trades = 0  # counts current total cost of all trades (price * quantity) for weighted avg calc

    def add_trade(self, trade):
        trade.pop('Symbol')  # removes symbol from trade, as all trades in this instrument have the same symbol
        self.all_trades.append(trade)  # adds trade to list of all trades
        if len(self.all_trades) > 1:  # checks whether this is the first trade added for this instrument
            self.update_max_time_gap(trade['TimeStamp'])  # these methods update the running totals
            self.update_total_volume(trade['Quantity'])
            self.update_weighted_avg_price(trade['Quantity'], trade['Price'])
            self.update_max_price(trade['Price'])
        else:
            self.instrument_dict['MaxTimeGap'] = 0  # these methods set initial running total values after the 1st trade
            self.instrument_dict['Volume'] = trade['Quantity']
            self.instrument_dict['WeightedAveragePrice'] = trade['Price']
            self.cost_of_all_trades += trade['Quantity'] * trade['Price']
            self.instrument_dict['MaxPrice'] = trade['Price']

    def update_max_time_gap(self, new_time_stamp):
        new_time_gap = new_time_stamp - self.all_trades[-2]['TimeStamp']  # calculates latest time gap
        if new_time_gap > self.instrument_dict['MaxTimeGap']:
            self.instrument_dict['MaxTimeGap'] = new_time_gap  # updates time gap if this is the largest so far

    def update_total_volume(self, new_quantity):
        self.instrument_dict['Volume'] += new_quantity  # updates total volume by adding latest quantity traded

    def update_weighted_avg_price(self, new_quantity, new_price):
        self.cost_of_all_trades += (new_quantity * new_price)  # updates cost of all trades for weighted avg price calc
        self.instrument_dict['WeightedAveragePrice'] = self.cost_of_all_trades / self.instrument_dict['Volume']  # calculates weighted average price with total cost / total volume

    def update_max_price(self, new_price):
        if new_price > self.instrument_dict['MaxPrice']:
            self.instrument_dict['MaxPrice'] = new_price  # updates max price if this is the greatest so far


if __name__ == '__main__':
    input_filename = 'input.csv'
    output_filename = 'output.csv'
    keys = ('TimeStamp', 'Symbol', 'Quantity', 'Price')
    symbols = []
    instruments = {}

    with open(input_filename) as input_file:
        all_trades = []  # creates empty list to store every trade in order
        for line in input_file:
            split_line = line.split(',')  # converts this line (currently a single string) to a list
            trade = [int(split_line[0]), split_line[1], int(split_line[2]), int(split_line[3])]  # create list of integer data & symbol name for trade
            trade_dict = dict(zip(keys, trade))  # convert integer data & symbol name to dict
            all_trades.append(trade_dict)  # store in list of dicts and convert to appropriate datatypes

    for trade in all_trades:
        if trade['Symbol'] not in symbols:
            symbols.append(trade['Symbol'])  # store symbol name in list of symbol names, if this is the first instance
            instruments[trade['Symbol']] = Instrument(trade['Symbol'])  # stores new class instance in dictionary with its symbol as they key, if this is the first instance
        instruments[trade['Symbol']].add_trade(trade)  # updates class instance with latest trade

    output_dict = {}  # empty dict to store data for outputting
    for symb, instr in instruments.items():
        output_dict[symb] = [instr.instrument_dict['MaxTimeGap'], instr.instrument_dict['Volume'], int(instr.instrument_dict['WeightedAveragePrice']), instr.instrument_dict['MaxPrice']]  # updates dict with data for each instrument
    sorted_dict = {k: output_dict[k] for k in sorted(output_dict)}  # fastest dictionary sort, source: https://stackoverflow.com/questions/50493838/fastest-way-to-sort-a-python-3-7-dictionary
    with open(output_filename, "w") as output_file:
        for symb in sorted_dict.keys():  # loop over each symbol
            output_file.write(f'{symb},{",".join(str(val) for val in sorted_dict[symb])}\n')  # converts vals to strings, then adds commas between vals and adds the symbol to the front
