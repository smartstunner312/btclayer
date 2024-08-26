
# Gains Trading Bot

## Introduction

The **Gains Trading Bot** is an automated trading solution specifically designed for interacting with the Gains Network. It fetches live trading data using the Alchemy Arbitrum API and follows the strategies of top traders listed in a sheet extracted from Dune Analytics. The bot mirrors these top traders' actions in a Binance account using the Binance API.

## Workflow

### 1. **Fetching Top Traders' Data**
The bot begins by loading a sheet of top traders, which is extracted from Dune Analytics. This sheet contains the details of traders whose strategies the bot aims to replicate.

### 2. **Fetching Live Data from Alchemy Arbitrum**
Next, the bot connects to the Alchemy Arbitrum URL to fetch real-time data of active traders. This data includes trading positions, volumes, and other relevant metrics that are essential for the bot’s decision-making process.

### 3. **Matching Traders and Strategy Implementation**
The bot compares the traders listed in the Dune Analytics sheet with the live data fetched from Alchemy. When a match is found, the bot follows the matched traders' actions—such as opening, closing, or adjusting positions—and implements these actions in the user's Binance account.

### 4. **Executing Trades on Binance**
Using the Binance API, the bot mirrors the actions of the top traders in real-time. This includes executing trades, managing positions, and following the risk management strategies that align with the traders’ actions in the live data.

### 5. **Generating Output Files**
After execution, the bot generates the following files in the same folder where the bot file and traders sheet are located:
- **GAINS_log.txt**: Logs detailing the bot’s activities, including API calls, decisions made, and any issues encountered.
- **GAINS_stop_signal.txt**: A file indicating when the bot has decided to stop trading, by inputting 'STOP' in this file bot stops taking trades.
- **GAINS_trading_data_df.csv**: A CSV file for storing the trades done by GAINS bot.

## PROBLEM ARISING

### 1. **Bot Not Taking Trades**
The Gains bot is currently not responding to any trades and is not taking any trades. Additionally, no errors are being logged in the log files, making it difficult to diagnose the underlying issue.

## Usage

1. **Run the Bot**:
   ```bash
   python bot.py
   ```

2. **Monitoring**:
   - Logs are generated as **GAINS_log.txt** and are saved in the same folder where the bot file and traders sheet are located.
   - Use the `--verbose` flag for detailed output:
     ```bash
     python bot.py --verbose
     ```
**NOTE**:
- extra **gains_and_gmxv1.csv** file is also provided. this file has huge amount of gains traders.
