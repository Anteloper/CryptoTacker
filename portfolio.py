import requests

coins = [("BTC", 0.0), ("BCH", 0.0), ("ETH", 0.0), ("LTC", 0.0), ("IOTA", 0.0), ("DASH", 0.0), ("XMR", 0.0)]

def main():
    priceString = getPriceString()
    coinPrices = fillPrices(priceString)
    output(coinPrices)


def getPriceString():
    coinString = ""
    for coin in coins:
        coinString += coin[0] + ","

    requestString = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + coinString[:-1] + "&tsyms=USD"
    txt = requests.get(requestString).text
    txt = txt.replace('"', '')
    txt = txt.replace('{', '')
    txt = txt.replace('}', '')
    return txt

#Returns an array of coin prices corresponding to the coinsOwned indices
def fillPrices(fullString):
    coinPrices = []
    for coin in coins:
        startString = coin[0] + ":USD:"
        startIndex = fullString.find(startString) + len(startString)
        endIndex = fullString.find(',', startIndex)
        price = fullString[startIndex:endIndex]
        coinPrices.append(float(price))
    return coinPrices


def output(coinPrices):
    netWorth = 0
    USDAmounts = []
    percentages = []
    for i, price in enumerate(coinPrices):
        dollarValue = coins[i][1] * price
        USDAmounts.append(dollarValue)
        netWorth += dollarValue

    for dollarAmount in USDAmounts:
        percentages.append(dollarAmount/netWorth * 100)

    coins.append(("TOTAL", "---"))
    coinPrices.append("")
    USDAmounts.append((sum(USDAmounts)))
    percentages.append((sum(percentages)))

    print("Coin         Price        Dollar Amount Owned     Coin Amount Owned    Percentage of Net Worth")

    for i in range(len(coins)):
        coinOwned = ""
        price = ""
        if(i == len(coins)-1):
            print()
        else:
            coinOwned = formatDecimal(coins[i][1])
            price = "$" + formatDecimal(coinPrices[i])

        dollarsOwned = formatDecimal(USDAmounts[i])

        percentageOwned = formatDecimal(percentages[i])

        firstSpace = " " * (6 + (9-len(price)) + (5-len(coins[i][0])))
        secondSpace = " " * (12 + (7-len(dollarsOwned)))
        thirdSpace = " " * (18  + (3-len(coinOwned)))
        fourthSpace = " " * (15 + (7 - len(percentageOwned)))

        print(coins[i][0] + firstSpace + price + secondSpace + "$" + dollarsOwned +
        thirdSpace + coinOwned + fourthSpace + percentageOwned + "%")


#Formats a float to have 2 decimal places
def formatDecimal(number):
    numString = str(round(number, 2))
    decimalPlaces = len(numString[(numString.find(".")):])
    if(decimalPlaces < 3):
        numString += "0" * (3-decimalPlaces)
    return numString
main()
