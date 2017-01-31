from perfin.portfolio import Stock, Portfolio


def main():

    # define your stocks
    ibm = Stock('IBM')
    ibm.add_transaction('2014-10-12', 100)
    ibm.add_transaction('2015-10-12', 150)
    ibm.add_transaction('2016-10-12', -100)

    appl = Stock('APPL')
    appl.add_transaction('2014-10-6', 10)
    appl.add_transaction('2015-10-6', 15)
    appl.add_transaction('2016-10-6', 30)

    # create your portfolio and add the stocks to it
    portfolio = Portfolio(stocks=[ibm, appl])

    # define the prices you want to use to get the
    prices = {'APPL': 100.32, 'IBM': 171.03}

    weights = portfolio.get_weights(weight_by='value', prices=prices)
    print('weights', weights)

    values = portfolio.get_current_value(prices)
    print('values', values)


if __name__ == '__main__':
    main()