import logging
import logging.handlers
import sys
import time
import datetime
import json
import numpy as np
from binance.client import Client
from web3 import Web3
from time import sleep
import pandas as pd
import logging
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import math
import csv
from web3 import Web3
from web3.datastructures import AttributeDict
from hexbytes import HexBytes
from decimal import Decimal, ROUND_FLOOR
import logging
import traceback
import pytz



# ONly make global if we want them to be modifies by any function else it doesnt cause any issues when called from inside a function
global leverage, threshold_balance, number_of_try, proxy_contract ,alchemy_url, percent_we_can_loose_stop_loss, ABI , traders_list, trading_data_df_path, dex_name, receiver_email, trading_data_df_length_stored, last_email_sent_date  



# EMail password for mail service
sender_email = "bigtestnet@gmail.com"             #here you can add your working email
email_password = "sfrv ilta umzp oaan"            #here password is the 'app password' of email which is generated after 2 step verification



# Google sheets           
# #these are the google sheet credential files which can be generated using google 
# cloud console. for further information you can reach out to this yt video to add your own gsheet.https://www.youtube.com/watch?v=zCEJurLGFRk              
credentials_file ={
  "type": "service_account",
  "project_id": "big-testnet-sheet",
  "private_key_id": "b628fd9782aac13bbeee431bd02a3bbec7014e58",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDaYxfHLS6yRsln\ni4qL4j+TR+Tez2PpNy8WtXyzOEjU/us7OBjdtLEVU92d/BEmxnTgBgg9Ap/JZn53\nrz+0c3f7mUApImGL+WRSJVEbL5Yxo5SOvHknk0sLCa5MqhFSpjm9QedI036zGdoZ\nko3xe/bDFGmENjG9mq0RW0pjeD+OEVfV5g8tbBXH+WoOKncp5b6N8Akrd31wcvAu\nNDPZCe1eQdDHpKhQAYzodbWR7HSGOF04386S3ec2BWNCHer7FzgyNJ2kSFPaU3O3\nflwPg68XPCny9vJC6KWgwxV1a+sy0JojUr0Ps1b0m8OYR5f3OX8m6VemqUf+7Nxb\nSFw0FT51AgMBAAECggEAGz39vxmeh9wnLxy702/NdPKktPujb7nzzI4mqFem1DUZ\nhGlexrdN2MZ9sIG7ZP4gIbr2559ubcn0kDsDBCBcUP0gwRDaIMMjNdEUYUMKJhaN\nB1Iw/dQUqiOSw9r6LrhwHvD76DyDw1U//O0oej13voWLFRRKl6eWG8Jq0OY07WR2\n3RqyTKPECcc0t74IJmKOjiMW/71WwYkS9+0mu5DLUNwMN5vweMWfRfBB91hxdRut\nlDlmyJCK/2Iey1iAmJkxEa9c7g+wldKZrZbQBb0rm9LOvbVcEyYgYP0QkkYNTpiF\nrsy4gwbushyAFLsKefeaD08MnTZE70LeihLoSdXKIQKBgQD6dD51vRhk99DkB7H2\nNC/pKzTvC1ehfw5R+CPxmHOUDOTpXz2sVt8pkwmIaz1INadZBZZoWGk8PeEkGOc0\nNzSAGSkBPikMTxEU3856XDUUJLPEuw87uAyjiM0KbuLbV6jaSEUU5FmqS43wQ1fg\nbq3Ph+j4cm6ttwCh4xvYiNt+IQKBgQDfORHf1nyk04hWNdtPioIQxEL+KtrF0NDs\n3zvZzC0zOjHeRFzeB8VMPtoddaU6r623ugoXB0VDqKeyi+H84cgQzncdwG+YaX01\noporcX6dS8/ME53ppYpdIrIc/Ts0dSG2d5BaFn80hdHQYYtXViCrY4Baz9b891Wd\nOlKQsBmt1QKBgAnIgKgYuts20vIVWt5DK5vwFCFCUCn+zJBnIQBO9DTUTBzRm5cf\nzZfSJo0tozcu4VqY3Uc2LOYthJ3kWyOvBF38nZ1u0Cuq6v/lvisJbwlaZatJo06x\n4cyBi4Dc0/+9bNsZ95jZUqdUTDcWalhZ+nAg3vjVf31JqLyqImxS7EABAoGBAN3A\nYwpbmC1h2tHR5NFqxnUDk43NYtIa9EIsLdfapph6Wmn0vdDwJUbuNV4IriDTvx6C\nmV1xIpTpKdcMcW73mPlhMiIDNplRSkqLAt7fe6mlU4PnhPtEMWT+f7SeuD8PkXMj\n6eok6S9zNRDupi8X55J7YVpVmLxqtMlh0/3ag1gVAoGAeAuHX3gYtyq7KNIOVoxq\noWhH0SmHu8jcO3VPTJbck2cBIqz+4qy5jA2Ldr7uz/rg36qPozFUBbk4hz3PZxg1\nlg1IKmB43XVkg4SjMnMUiTO7LJKVphB1hKEt/3shlpbBphCa4JAfuH/1BIUoDgmC\npTVWOStkA0pZ6B12p+hVoY4=\n-----END PRIVATE KEY-----\n",
  "client_email": "big-testnet-55gb@big-testnet-sheet.iam.gserviceaccount.com",
  "client_id": "109091773716702844167",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/big-testnet-55gb%40big-testnet-sheet.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Specify the ID of the Google Sheet    
sheet_id = "13e3Cnfor04OzLxgUOQhw1Fty0ojo1wf1pBDwEbNyDjU"
google_sheet_url = "https://docs.google.com/spreadsheets/d/13e3Cnfor04OzLxgUOQhw1Fty0ojo1wf1pBDwEbNyDjU/edit?usp=sharing"
# https://www.youtube.com/watch?v=zCEJurLGFRk   Refer to this video in future if needed for google sheet api operations in gspread operations
# https://docs.google.com/spreadsheets/d/1VXp8vOTvSqBH_zB1A9eIsaSIEVQslZTTljHsO5Mqfk0/edit#gid=0 link to google sheet


# Email IDs
receiver_email = ["jrai3069@gmail.com","sahilll.singh.33@gmail.com","sainath@knit.finance"]


# Naming the decenteralized exchange
dex_name = ["GAINS"]
DEX = ["GAINS"]


# Initialize an empty list to store dictionaries
ban_positions_info_list = []


our_leverage = 10

max_leverage_for_stop_price = 150 # This is extreme case (150) on the exchange for the tokens.
min_leverage_for_stop_price = 2 # This is our choice. Note: Make sure it is never less than or equal to 1, as stop price will become 0.

threshold_balance = 50
investement_risk_factor = 1
number_of_try = 4    # will try n-1 times
percent_we_can_loose_stop_loss = 0.2 #Ratio of how much we are ready to loose our colletral)
profit_percent = 0.02 #Amount ratio we want to gain
price_difference_ratio = 0.80 # ratio for price difference deviation allowed from alchemy price : binance price
retry_time = 1 # retry time for trading in seconds
ban_time_hours = 48 # Ban time for postions which had exceptions because they returned some code instead of "True".
dex_max_leverage = 160 # Check this from the DEX website
trading_data_df_length_stored = 0 # Trading_data_df_length_stored initially zero
last_email_sent_date = None # Summary email sent date
summary_sending_hour = 18 #  The time at which summary email is sent in every 24 hrs (24 hrs format)


# alchemy_url = "https://arb-mainnet.g.alchemy.com/v2/GttxMXc3k0mK2OpL1byqViOk0AkEaVkN"   # Only for Gains


proxy_contract = "0xFF162c694eAA571f685030649814282eA457f169"     # for Gains
alchemy_url = "https://arb-mainnet.g.alchemy.com/v2/xO9lyeofQORAnkDQKHrnXfT1s-7P3yEk"  #From John(2) # this is the alchemy arbitrum url created from 'https://www.alchemy.com' 



stop_signal_path = f"{dex_name[0]}_stop_signal.txt"
# keep stop_signal = "" or Keep it as stop_signal = "STOP"


# Load the top 100 traders list from the CSV file
traders_list = pd.read_csv("Top_Traders_Universal_Data_30_07_2024.csv")


# Path to the trading_data_df
trading_data_df_path = f"{dex_name[0]}_trading_data_df.csv"



# Test Net id and password
# forextraworksid@gmail.com
# S#H4LUR2q6P&#/z          
# # Binance API credentials its testnet
# api_key = '3604203c3f9974d7780f0c89bc8d28d850b18de2651c800c21bf8ba375c5fbe8'
# api_secret = '4cc1ee105ff3bc6cdd88cf4a6b70330b8230a4c8f200cef4d1c016bdde0a4c08'



# Creating stop singal file
with open(stop_signal_path, "w") as f:
    print(f"Created {stop_signal_path}")




    #### DF initiator


# Initiating dataframe to manage all trades
trading_data_df = pd.DataFrame(columns=[
            'time', 
            'trade_order_id', 
            'address', 
            'symbol', 
            'is_long_short', 
            'trade_type',
            'leads_price',
            'price', 
            'weighted_score_ratio',
            'leads_max_volume',
            'leads_leverage',
            'leads_transaction_quantity', 
            'leads_transaction_amount', 
            'our_leverage',
            'our_transaction_quantity', 
            'our_transaction_amount', 
            'leads_total_hold', 
            'leads_total_investment',
            'avg_leads_coin_price',
            'our_total_hold', 
            'our_total_investment',
            'avg_coin_price', 
            'total_hold_ratio', 
            'stop_loss_price', 
            'stop_loss_order_id', 
            'is_stop_loss_executed',
            'is_liquidated', 
            'take_profit_price', 
            'take_profit_order_id', 
            'PNL',
            'DEX',
            'available_balance'])



ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AboveMax","type":"error"},{"inputs":[],"name":"AlreadyExists","type":"error"},{"inputs":[],"name":"BelowMin","type":"error"},{"inputs":[],"name":"BlockOrder","type":"error"},{"inputs":[],"name":"DoesntExist","type":"error"},{"inputs":[],"name":"InitError","type":"error"},{"inputs":[{"internalType":"address","name":"_initializationContractAddress","type":"address"},{"internalType":"bytes","name":"_calldata","type":"bytes"}],"name":"InitializationFunctionReverted","type":"error"},{"inputs":[],"name":"InvalidAddresses","type":"error"},{"inputs":[],"name":"InvalidCollateralIndex","type":"error"},{"inputs":[],"name":"InvalidFacetCutAction","type":"error"},{"inputs":[],"name":"InvalidInputLength","type":"error"},{"inputs":[],"name":"NotAllowed","type":"error"},{"inputs":[],"name":"NotAuthorized","type":"error"},{"inputs":[],"name":"NotContract","type":"error"},{"inputs":[],"name":"NotFound","type":"error"},{"inputs":[],"name":"Overflow","type":"error"},{"inputs":[],"name":"Paused","type":"error"},{"inputs":[],"name":"WrongAccess","type":"error"},{"inputs":[],"name":"WrongIndex","type":"error"},{"inputs":[],"name":"WrongLength","type":"error"},{"inputs":[],"name":"WrongOrder","type":"error"},{"inputs":[],"name":"WrongParams","type":"error"},{"inputs":[],"name":"WrongTradeType","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"inputs":[],"name":"ZeroValue","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"target","type":"address"},{"indexed":false,"internalType":"enum IAddressStore.Role","name":"role","type":"uint8"},{"indexed":false,"internalType":"bool","name":"access","type":"bool"}],"name":"AccessControlUpdated","type":"event","signature":"0x8d7fdec37f50c07219a6a0859420936836eb9254bf412035e3acede18b8b093d"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"gns","type":"address"},{"internalType":"address","name":"gnsStaking","type":"address"}],"indexed":false,"internalType":"struct IAddressStore.Addresses","name":"addresses","type":"tuple"}],"name":"AddressesUpdated","type":"event","signature":"0xe4f1f9461410dada4f4b49a4b363bdf35e6069fb5a0cea4b1147c32affbd954a"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"facetAddress","type":"address"},{"internalType":"enum IDiamondStorage.FacetCutAction","name":"action","type":"uint8"},{"internalType":"bytes4[]","name":"functionSelectors","type":"bytes4[]"}],"indexed":false,"internalType":"struct IDiamondStorage.FacetCut[]","name":"_diamondCut","type":"tuple[]"},{"indexed":false,"internalType":"address","name":"_init","type":"address"},{"indexed":false,"internalType":"bytes","name":"_calldata","type":"bytes"}],"name":"DiamondCut","type":"event","signature":"0x8faa70878671ccd212d20771b795c50af8fd3ff6cf27f4bde57e5d4de0aeb673"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event","signature":"0x7f26b83ff96e1f2b6a682f133852f6798a09c465da95921460cefb3847402498"},{"inputs":[{"components":[{"internalType":"address","name":"facetAddress","type":"address"},{"internalType":"enum IDiamondStorage.FacetCutAction","name":"action","type":"uint8"},{"internalType":"bytes4[]","name":"functionSelectors","type":"bytes4[]"}],"internalType":"struct IDiamondStorage.FacetCut[]","name":"_faceCut","type":"tuple[]"},{"internalType":"address","name":"_init","type":"address"},{"internalType":"bytes","name":"_calldata","type":"bytes"}],"name":"diamondCut","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x1f931c1c"},{"inputs":[{"internalType":"bytes4","name":"_functionSelector","type":"bytes4"}],"name":"facetAddress","outputs":[{"internalType":"address","name":"facetAddress_","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xcdffacc6"},{"inputs":[],"name":"facetAddresses","outputs":[{"internalType":"address[]","name":"facetAddresses_","type":"address[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x52ef6b2c"},{"inputs":[{"internalType":"address","name":"_facet","type":"address"}],"name":"facetFunctionSelectors","outputs":[{"internalType":"bytes4[]","name":"facetFunctionSelectors_","type":"bytes4[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xadfca15e"},{"inputs":[],"name":"facets","outputs":[{"components":[{"internalType":"address","name":"facetAddress","type":"address"},{"internalType":"bytes4[]","name":"functionSelectors","type":"bytes4[]"}],"internalType":"struct IGNSDiamondLoupe.Facet[]","name":"facets_","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x7a0ed627"},{"inputs":[],"name":"getAddresses","outputs":[{"components":[{"internalType":"address","name":"gns","type":"address"},{"internalType":"address","name":"gnsStaking","type":"address"}],"internalType":"struct IAddressStore.Addresses","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa39fac12"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"enum IAddressStore.Role","name":"_role","type":"uint8"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x95a8c58d"},{"inputs":[{"internalType":"address","name":"_rolesManager","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc4d66de8"},{"inputs":[{"internalType":"address[]","name":"_accounts","type":"address[]"},{"internalType":"enum IAddressStore.Role[]","name":"_roles","type":"uint8[]"},{"internalType":"bool[]","name":"_values","type":"bool[]"}],"name":"setRoles","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x101e6503"},{"inputs":[],"name":"FeeNotListed","type":"error"},{"inputs":[],"name":"GroupNotListed","type":"error"},{"inputs":[],"name":"PairAlreadyListed","type":"error"},{"inputs":[],"name":"PairNotListed","type":"error"},{"inputs":[],"name":"WrongFees","type":"error"},{"inputs":[],"name":"WrongLeverages","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"string","name":"name","type":"string"}],"name":"FeeAdded","type":"event","signature":"0x482049823c85e038e099fe4f2b901487c4800def71c9a3f5bae2de8381ec54f6"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"FeeUpdated","type":"event","signature":"0x8c4d35e54a3f2ef1134138fd8ea3daee6a3c89e10d2665996babdf70261e2c76"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"string","name":"name","type":"string"}],"name":"GroupAdded","type":"event","signature":"0xaf17de8e82beccc440012117a600dc37e26925225d0f1ee192fc107eb3dcbca4"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"GroupUpdated","type":"event","signature":"0xcfde8f228364c70f12cbbac5a88fc91ceca76dd750ac93364991a333b34afb8e"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"string","name":"from","type":"string"},{"indexed":false,"internalType":"string","name":"to","type":"string"}],"name":"PairAdded","type":"event","signature":"0x3adfd40f2b74073df2a84238acdb7f460565a557b3cc13bddc8833289bf38e09"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"maxLeverage","type":"uint256"}],"name":"PairCustomMaxLeverageUpdated","type":"event","signature":"0x5d6c9d6dd6c84fa315e799a455ccb71230e5b88e171c48c4853425ce044e9bce"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"PairUpdated","type":"event","signature":"0x123a1b961ae93e7acda9790b318237b175b45ac09277cd3614305d8baa3f1953"},{"inputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"openFeeP","type":"uint256"},{"internalType":"uint256","name":"closeFeeP","type":"uint256"},{"internalType":"uint256","name":"oracleFeeP","type":"uint256"},{"internalType":"uint256","name":"triggerOrderFeeP","type":"uint256"},{"internalType":"uint256","name":"minPositionSizeUsd","type":"uint256"}],"internalType":"struct IPairsStorage.Fee[]","name":"_fees","type":"tuple[]"}],"name":"addFees","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x0c00b94a"},{"inputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bytes32","name":"job","type":"bytes32"},{"internalType":"uint256","name":"minLeverage","type":"uint256"},{"internalType":"uint256","name":"maxLeverage","type":"uint256"}],"internalType":"struct IPairsStorage.Group[]","name":"_groups","type":"tuple[]"}],"name":"addGroups","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x60283cba"},{"inputs":[{"components":[{"internalType":"string","name":"from","type":"string"},{"internalType":"string","name":"to","type":"string"},{"components":[{"internalType":"address","name":"feed1","type":"address"},{"internalType":"address","name":"feed2","type":"address"},{"internalType":"enum IPairsStorage.FeedCalculation","name":"feedCalculation","type":"uint8"},{"internalType":"uint256","name":"maxDeviationP","type":"uint256"}],"internalType":"struct IPairsStorage.Feed","name":"feed","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint256","name":"groupIndex","type":"uint256"},{"internalType":"uint256","name":"feeIndex","type":"uint256"}],"internalType":"struct IPairsStorage.Pair[]","name":"_pairs","type":"tuple[]"}],"name":"addPairs","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xdb7c3f9d"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"fees","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"openFeeP","type":"uint256"},{"internalType":"uint256","name":"closeFeeP","type":"uint256"},{"internalType":"uint256","name":"oracleFeeP","type":"uint256"},{"internalType":"uint256","name":"triggerOrderFeeP","type":"uint256"},{"internalType":"uint256","name":"minPositionSizeUsd","type":"uint256"}],"internalType":"struct IPairsStorage.Fee","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4acc79ed"},{"inputs":[],"name":"feesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x658de48a"},{"inputs":[],"name":"getAllPairsRestrictedMaxLeverage","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x678b3fb0"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"groups","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bytes32","name":"job","type":"bytes32"},{"internalType":"uint256","name":"minLeverage","type":"uint256"},{"internalType":"uint256","name":"maxLeverage","type":"uint256"}],"internalType":"struct IPairsStorage.Group","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x96324bd4"},{"inputs":[],"name":"groupsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x885e2750"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"isPairIndexListed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x281b7ead"},{"inputs":[{"internalType":"string","name":"_from","type":"string"},{"internalType":"string","name":"_to","type":"string"}],"name":"isPairListed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x1628bfeb"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairCloseFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x836a341a"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairCustomMaxLeverage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x24a96865"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairJob","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x302f81fc"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairMaxLeverage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x281b693c"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairMinLeverage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x59a992d0"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairMinPositionSizeUsd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x5e26ff4e"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairOpenFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x8251135b"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairOracleFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xf7acbabd"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairSpreadP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa1d54e9b"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"pairTriggerOrderFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xe74aff72"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"pairs","outputs":[{"components":[{"internalType":"string","name":"from","type":"string"},{"internalType":"string","name":"to","type":"string"},{"components":[{"internalType":"address","name":"feed1","type":"address"},{"internalType":"address","name":"feed2","type":"address"},{"internalType":"enum IPairsStorage.FeedCalculation","name":"feedCalculation","type":"uint8"},{"internalType":"uint256","name":"maxDeviationP","type":"uint256"}],"internalType":"struct IPairsStorage.Feed","name":"feed","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint256","name":"groupIndex","type":"uint256"},{"internalType":"uint256","name":"feeIndex","type":"uint256"}],"internalType":"struct IPairsStorage.Pair","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xb91ac788"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"pairsBackend","outputs":[{"components":[{"internalType":"string","name":"from","type":"string"},{"internalType":"string","name":"to","type":"string"},{"components":[{"internalType":"address","name":"feed1","type":"address"},{"internalType":"address","name":"feed2","type":"address"},{"internalType":"enum IPairsStorage.FeedCalculation","name":"feedCalculation","type":"uint8"},{"internalType":"uint256","name":"maxDeviationP","type":"uint256"}],"internalType":"struct IPairsStorage.Feed","name":"feed","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint256","name":"groupIndex","type":"uint256"},{"internalType":"uint256","name":"feeIndex","type":"uint256"}],"internalType":"struct IPairsStorage.Pair","name":"","type":"tuple"},{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bytes32","name":"job","type":"bytes32"},{"internalType":"uint256","name":"minLeverage","type":"uint256"},{"internalType":"uint256","name":"maxLeverage","type":"uint256"}],"internalType":"struct IPairsStorage.Group","name":"","type":"tuple"},{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"openFeeP","type":"uint256"},{"internalType":"uint256","name":"closeFeeP","type":"uint256"},{"internalType":"uint256","name":"oracleFeeP","type":"uint256"},{"internalType":"uint256","name":"triggerOrderFeeP","type":"uint256"},{"internalType":"uint256","name":"minPositionSizeUsd","type":"uint256"}],"internalType":"struct IPairsStorage.Fee","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x9567dccf"},{"inputs":[],"name":"pairsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xb81b2b71"},{"inputs":[{"internalType":"uint256[]","name":"_indices","type":"uint256[]"},{"internalType":"uint256[]","name":"_values","type":"uint256[]"}],"name":"setPairCustomMaxLeverages","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xd79261fd"},{"inputs":[{"internalType":"uint256[]","name":"_ids","type":"uint256[]"},{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"openFeeP","type":"uint256"},{"internalType":"uint256","name":"closeFeeP","type":"uint256"},{"internalType":"uint256","name":"oracleFeeP","type":"uint256"},{"internalType":"uint256","name":"triggerOrderFeeP","type":"uint256"},{"internalType":"uint256","name":"minPositionSizeUsd","type":"uint256"}],"internalType":"struct IPairsStorage.Fee[]","name":"_fees","type":"tuple[]"}],"name":"updateFees","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xe57f6759"},{"inputs":[{"internalType":"uint256[]","name":"_ids","type":"uint256[]"},{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bytes32","name":"job","type":"bytes32"},{"internalType":"uint256","name":"minLeverage","type":"uint256"},{"internalType":"uint256","name":"maxLeverage","type":"uint256"}],"internalType":"struct IPairsStorage.Group[]","name":"_groups","type":"tuple[]"}],"name":"updateGroups","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x11d79ef5"},{"inputs":[{"internalType":"uint256[]","name":"_pairIndices","type":"uint256[]"},{"components":[{"internalType":"string","name":"from","type":"string"},{"internalType":"string","name":"to","type":"string"},{"components":[{"internalType":"address","name":"feed1","type":"address"},{"internalType":"address","name":"feed2","type":"address"},{"internalType":"enum IPairsStorage.FeedCalculation","name":"feedCalculation","type":"uint8"},{"internalType":"uint256","name":"maxDeviationP","type":"uint256"}],"internalType":"struct IPairsStorage.Feed","name":"feed","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint256","name":"groupIndex","type":"uint256"},{"internalType":"uint256","name":"feeIndex","type":"uint256"}],"internalType":"struct IPairsStorage.Pair[]","name":"_pairs","type":"tuple[]"}],"name":"updatePairs","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x10efa5d5"},{"inputs":[],"name":"AllyNotActive","type":"error"},{"inputs":[],"name":"AlreadyActive","type":"error"},{"inputs":[],"name":"AlreadyInactive","type":"error"},{"inputs":[],"name":"NoPendingRewards","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"ally","type":"address"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint256","name":"volumeUsd","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountGns","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountValueUsd","type":"uint256"}],"name":"AllyRewardDistributed","type":"event","signature":"0x0d54fedb563328d37f00fe5ba0bf7689519f8cf02318562adfe7b4bfab8cf4b4"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"ally","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountGns","type":"uint256"}],"name":"AllyRewardsClaimed","type":"event","signature":"0x3dfe9be199655709d01d635bf441264a809a090c98ed7aae9abdc85f7dcbc09d"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"ally","type":"address"}],"name":"AllyUnwhitelisted","type":"event","signature":"0x6900afc1a924abca16a7f560e2dac3d71008c1cd1d88de8a85b6e4267116d186"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"ally","type":"address"}],"name":"AllyWhitelisted","type":"event","signature":"0x80495287b7fdd5e00b7c8c1eb065c5b63474d11ffb062cc82c13da77dda8424d"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"address","name":"referrer","type":"address"}],"name":"ReferrerRegistered","type":"event","signature":"0x0e67f4bbcd5c51b7365ca2dd861dc8094e393ca60de2ceae9d831761a839e92a"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"referrer","type":"address"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint256","name":"volumeUsd","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountGns","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountValueUsd","type":"uint256"}],"name":"ReferrerRewardDistributed","type":"event","signature":"0x74e9754b45c636e199e3d7bb764fae1a9acce47a984d10dcfd74849ec4babc4f"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"referrer","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountGns","type":"uint256"}],"name":"ReferrerRewardsClaimed","type":"event","signature":"0x25deb48f8299e9863bda34f0d343d51341ac7ac30bf63dbeb2e8212bc4a20bf1"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"referrer","type":"address"}],"name":"ReferrerUnwhitelisted","type":"event","signature":"0x6dd169357c2e2b04fd13a8807a11892b88875b7c70eeb73c3b6642c58516f0db"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"referrer","type":"address"},{"indexed":true,"internalType":"address","name":"ally","type":"address"}],"name":"ReferrerWhitelisted","type":"event","signature":"0x15ad1d28b052a6cc2dd1d34d9e06a1847055d520e2163017e6e8aad6431b7f6a"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"UpdatedAllyFeeP","type":"event","signature":"0x2f33e68d48a82acaa58e3dcb12a4c7738cdfe7041d35f0e29ec8c39b780b370c"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"UpdatedOpenFeeP","type":"event","signature":"0x4dec17ad9a229f707b7c2fb9531cd3b9c548f9eca80c03457ca38a0bb1df35fe"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"UpdatedStartReferrerFeeP","type":"event","signature":"0xb85b70acaeb40f1a2351367c48842ee0ea24ec05d411d99d80bf7a020c0dbb0f"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"UpdatedTargetVolumeUsd","type":"event","signature":"0x7e6042545b314fbe2e138616211d5c38934823f783b83a140ea84f0eb2ae115d"},{"inputs":[],"name":"claimAllyRewards","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xee6cf884"},{"inputs":[],"name":"claimReferrerRewards","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x65cbd307"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint256","name":"_volumeUsd","type":"uint256"},{"internalType":"uint256","name":"_pairOpenFeeP","type":"uint256"},{"internalType":"uint256","name":"_gnsPriceUsd","type":"uint256"}],"name":"distributeReferralReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function","signature":"0xfa3c8dbf"},{"inputs":[{"internalType":"address","name":"_ally","type":"address"}],"name":"getAllyDetails","outputs":[{"components":[{"internalType":"address[]","name":"referrersReferred","type":"address[]"},{"internalType":"uint256","name":"volumeReferredUsd","type":"uint256"},{"internalType":"uint256","name":"pendingRewardsGns","type":"uint256"},{"internalType":"uint256","name":"totalRewardsGns","type":"uint256"},{"internalType":"uint256","name":"totalRewardsValueUsd","type":"uint256"},{"internalType":"bool","name":"active","type":"bool"}],"internalType":"struct IReferrals.AllyDetails","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x92e67406"},{"inputs":[],"name":"getReferralsAllyFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x97436b5f"},{"inputs":[],"name":"getReferralsOpenFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x06350917"},{"inputs":[],"name":"getReferralsStartReferrerFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x843b9e5d"},{"inputs":[],"name":"getReferralsTargetVolumeUsd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x71159fd1"},{"inputs":[{"internalType":"address","name":"_referrer","type":"address"}],"name":"getReferrerDetails","outputs":[{"components":[{"internalType":"address","name":"ally","type":"address"},{"internalType":"address[]","name":"tradersReferred","type":"address[]"},{"internalType":"uint256","name":"volumeReferredUsd","type":"uint256"},{"internalType":"uint256","name":"pendingRewardsGns","type":"uint256"},{"internalType":"uint256","name":"totalRewardsGns","type":"uint256"},{"internalType":"uint256","name":"totalRewardsValueUsd","type":"uint256"},{"internalType":"bool","name":"active","type":"bool"}],"internalType":"struct IReferrals.ReferrerDetails","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xcbe0f32e"},{"inputs":[{"internalType":"uint256","name":"_pairOpenFeeP","type":"uint256"},{"internalType":"uint256","name":"_volumeReferredUsd","type":"uint256"}],"name":"getReferrerFeeP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4e583b31"},{"inputs":[{"internalType":"address","name":"_ally","type":"address"}],"name":"getReferrersReferred","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa73a3e35"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTraderActiveReferrer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x036787e5"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTraderLastReferrer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x46dbf572"},{"inputs":[{"internalType":"address","name":"_referrer","type":"address"}],"name":"getTradersReferred","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x32a7b732"},{"inputs":[{"internalType":"uint256","name":"_allyFeeP","type":"uint256"},{"internalType":"uint256","name":"_startReferrerFeeP","type":"uint256"},{"internalType":"uint256","name":"_openFeeP","type":"uint256"},{"internalType":"uint256","name":"_targetVolumeUsd","type":"uint256"}],"name":"initializeReferrals","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc8b0d710"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"address","name":"_referrer","type":"address"}],"name":"registerPotentialReferrer","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x9b8ab684"},{"inputs":[{"internalType":"address[]","name":"_allies","type":"address[]"}],"name":"unwhitelistAllies","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x3450191e"},{"inputs":[{"internalType":"address[]","name":"_referrers","type":"address[]"}],"name":"unwhitelistReferrers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x92b2bbae"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"updateAllyFeeP","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x97365b74"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"updateReferralsOpenFeeP","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xdfed4fcb"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"updateReferralsTargetVolumeUsd","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x66ddd309"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"updateStartReferrerFeeP","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x03e37464"},{"inputs":[{"internalType":"address[]","name":"_allies","type":"address[]"}],"name":"whitelistAllies","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc72d02e3"},{"inputs":[{"internalType":"address[]","name":"_referrers","type":"address[]"},{"internalType":"address[]","name":"_allies","type":"address[]"}],"name":"whitelistReferrers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x507cd8de"},{"inputs":[],"name":"WrongFeeTier","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256[]","name":"feeTiersIndices","type":"uint256[]"},{"components":[{"internalType":"uint32","name":"feeMultiplier","type":"uint32"},{"internalType":"uint32","name":"pointsThreshold","type":"uint32"}],"indexed":false,"internalType":"struct IFeeTiers.FeeTier[]","name":"feeTiers","type":"tuple[]"}],"name":"FeeTiersUpdated","type":"event","signature":"0xa6ec87cc1a516d9ebb5c03260f77d2bd8c22dc8d28d71e740b320fbd4d704131"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256[]","name":"groupIndices","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"groupVolumeMultipliers","type":"uint256[]"}],"name":"GroupVolumeMultipliersUpdated","type":"event","signature":"0xb173e04a52e3de8d79b981e4ffc87d49e6577ceab559ebf36a70bba02cc2569c"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint32","name":"day","type":"uint32"},{"indexed":false,"internalType":"uint224","name":"points","type":"uint224"}],"name":"TraderDailyPointsIncreased","type":"event","signature":"0x4f6f49815b9e6682a4f6bc21ba0b5261e803cc5d56c97477a5dc75925fd74e68"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint32","name":"day","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"feeMultiplier","type":"uint32"}],"name":"TraderFeeMultiplierCached","type":"event","signature":"0x136cc4347dc65b38625089ea9df2874eda024554dc7d0a363036d6fa6d7e4c9e"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint32","name":"day","type":"uint32"}],"name":"TraderInfoFirstUpdate","type":"event","signature":"0x8aa104927dea7fb70b6e5eb2e2891e3022714eea9e80c493fdabffce48b42393"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"components":[{"internalType":"uint32","name":"lastDayUpdated","type":"uint32"},{"internalType":"uint224","name":"trailingPoints","type":"uint224"}],"indexed":false,"internalType":"struct IFeeTiers.TraderInfo","name":"traderInfo","type":"tuple"}],"name":"TraderInfoUpdated","type":"event","signature":"0x211bcdec669891da564d4d5bd35fa76cf6cc72a218db19f402ec042770fb83fb"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint32","name":"fromDay","type":"uint32"},{"indexed":false,"internalType":"uint32","name":"toDay","type":"uint32"},{"indexed":false,"internalType":"uint224","name":"expiredPoints","type":"uint224"}],"name":"TraderTrailingPointsExpired","type":"event","signature":"0x964f0f6a92f6d7eedbff7670a2e850f5511e59321724a9dbef638c8068b7527b"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint256","name":"_normalFeeAmountCollateral","type":"uint256"}],"name":"calculateFeeAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4f09a236"},{"inputs":[{"internalType":"uint256","name":"_feeTierIndex","type":"uint256"}],"name":"getFeeTier","outputs":[{"components":[{"internalType":"uint32","name":"feeMultiplier","type":"uint32"},{"internalType":"uint32","name":"pointsThreshold","type":"uint32"}],"internalType":"struct IFeeTiers.FeeTier","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xeccea3e2"},{"inputs":[],"name":"getFeeTiersCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa89db8e5"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint32","name":"_day","type":"uint32"}],"name":"getFeeTiersTraderDailyInfo","outputs":[{"components":[{"internalType":"uint32","name":"feeMultiplierCache","type":"uint32"},{"internalType":"uint224","name":"points","type":"uint224"}],"internalType":"struct IFeeTiers.TraderDailyInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x794d8520"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getFeeTiersTraderInfo","outputs":[{"components":[{"internalType":"uint32","name":"lastDayUpdated","type":"uint32"},{"internalType":"uint224","name":"trailingPoints","type":"uint224"}],"internalType":"struct IFeeTiers.TraderInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xacbaaf33"},{"inputs":[{"internalType":"uint256","name":"_groupIndex","type":"uint256"}],"name":"getGroupVolumeMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x31ca4887"},{"inputs":[{"internalType":"uint256[]","name":"_groupIndices","type":"uint256[]"},{"internalType":"uint256[]","name":"_groupVolumeMultipliers","type":"uint256[]"},{"internalType":"uint256[]","name":"_feeTiersIndices","type":"uint256[]"},{"components":[{"internalType":"uint32","name":"feeMultiplier","type":"uint32"},{"internalType":"uint32","name":"pointsThreshold","type":"uint32"}],"internalType":"struct IFeeTiers.FeeTier[]","name":"_feeTiers","type":"tuple[]"}],"name":"initializeFeeTiers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x33534de2"},{"inputs":[{"internalType":"uint256[]","name":"_feeTiersIndices","type":"uint256[]"},{"components":[{"internalType":"uint32","name":"feeMultiplier","type":"uint32"},{"internalType":"uint32","name":"pointsThreshold","type":"uint32"}],"internalType":"struct IFeeTiers.FeeTier[]","name":"_feeTiers","type":"tuple[]"}],"name":"setFeeTiers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xeced5249"},{"inputs":[{"internalType":"uint256[]","name":"_groupIndices","type":"uint256[]"},{"internalType":"uint256[]","name":"_groupVolumeMultipliers","type":"uint256[]"}],"name":"setGroupVolumeMultipliers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x944f577a"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint256","name":"_volumeUsd","type":"uint256"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"updateTraderPoints","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xfed8a190"},{"inputs":[],"name":"WrongWindowsCount","type":"error"},{"inputs":[],"name":"WrongWindowsDuration","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint48","name":"windowsDuration","type":"uint48"},{"indexed":true,"internalType":"uint48","name":"windowsCount","type":"uint48"}],"name":"OiWindowsSettingsInitialized","type":"event","signature":"0x13a1cf276d620019ba08cdbba6c90fc281a94ee3481ea8aff3b514c8ab4d0ac2"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"uint128","name":"valueAboveUsd","type":"uint128"},{"indexed":false,"internalType":"uint128","name":"valueBelowUsd","type":"uint128"}],"name":"OnePercentDepthUpdated","type":"event","signature":"0x636bd42d4023c080480c167f471d64277a2a04d8f812420062908ace34475092"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"components":[{"internalType":"uint128","name":"oiLongUsd","type":"uint128"},{"internalType":"uint128","name":"oiShortUsd","type":"uint128"}],"indexed":false,"internalType":"struct IPriceImpact.PairOi","name":"totalPairOi","type":"tuple"}],"name":"PriceImpactOiTransferredPair","type":"event","signature":"0xbc0bf036cfe0e40ec07eeea05e96c6a78f2bc92a80f5d10b9179a2649e3bb717"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"pairsCount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"prevCurrentWindowId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"prevEarliestWindowId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newCurrentWindowId","type":"uint256"}],"name":"PriceImpactOiTransferredPairs","type":"event","signature":"0x73a54fbb7b96ef55a35eecf33a61c9ae379cbb38a4d6de352ee3e7c456211a22"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint48","name":"windowsDuration","type":"uint48"},{"internalType":"uint256","name":"pairIndex","type":"uint256"},{"internalType":"uint256","name":"windowId","type":"uint256"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"uint128","name":"openInterestUsd","type":"uint128"}],"indexed":false,"internalType":"struct IPriceImpact.OiWindowUpdate","name":"oiWindowUpdate","type":"tuple"}],"name":"PriceImpactOpenInterestAdded","type":"event","signature":"0xb8b5cf1c4a93075d32b38049f7ad65e6608d90f232123dd65d55a5ed06988cb5"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint48","name":"windowsDuration","type":"uint48"},{"internalType":"uint256","name":"pairIndex","type":"uint256"},{"internalType":"uint256","name":"windowId","type":"uint256"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"uint128","name":"openInterestUsd","type":"uint128"}],"indexed":false,"internalType":"struct IPriceImpact.OiWindowUpdate","name":"oiWindowUpdate","type":"tuple"},{"indexed":false,"internalType":"bool","name":"notOutdated","type":"bool"}],"name":"PriceImpactOpenInterestRemoved","type":"event","signature":"0xde1fe3df38229b603f1a7a96f1ac6159116b2a48dada12998a226039786f7ca6"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint48","name":"windowsCount","type":"uint48"}],"name":"PriceImpactWindowsCountUpdated","type":"event","signature":"0xcd8ae5cbabd45f9918819404692cdffaab6769e8cf5a597405518a1b33419d71"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint48","name":"windowsDuration","type":"uint48"}],"name":"PriceImpactWindowsDurationUpdated","type":"event","signature":"0x5c4b755bc1cf4bae3a95cfc185b1e390e2289a97933671d8a098a4131b020664"},{"inputs":[{"internalType":"uint256","name":"_openInterestUsd","type":"uint256"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"bool","name":"_long","type":"bool"}],"name":"addPriceImpactOpenInterest","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x96839490"},{"inputs":[{"internalType":"uint48","name":"_windowsDuration","type":"uint48"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"uint256","name":"_windowId","type":"uint256"}],"name":"getOiWindow","outputs":[{"components":[{"internalType":"uint128","name":"oiLongUsd","type":"uint128"},{"internalType":"uint128","name":"oiShortUsd","type":"uint128"}],"internalType":"struct IPriceImpact.PairOi","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x823ef2ac"},{"inputs":[{"internalType":"uint48","name":"_windowsDuration","type":"uint48"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"uint256[]","name":"_windowIds","type":"uint256[]"}],"name":"getOiWindows","outputs":[{"components":[{"internalType":"uint128","name":"oiLongUsd","type":"uint128"},{"internalType":"uint128","name":"oiShortUsd","type":"uint128"}],"internalType":"struct IPriceImpact.PairOi[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0d12f7cb"},{"inputs":[],"name":"getOiWindowsSettings","outputs":[{"components":[{"internalType":"uint48","name":"startTs","type":"uint48"},{"internalType":"uint48","name":"windowsDuration","type":"uint48"},{"internalType":"uint48","name":"windowsCount","type":"uint48"}],"internalType":"struct IPriceImpact.OiWindowsSettings","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xb56df676"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"}],"name":"getPairDepth","outputs":[{"components":[{"internalType":"uint128","name":"onePercentDepthAboveUsd","type":"uint128"},{"internalType":"uint128","name":"onePercentDepthBelowUsd","type":"uint128"}],"internalType":"struct IPriceImpact.PairDepth","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x375bb2bb"},{"inputs":[{"internalType":"uint256[]","name":"_indices","type":"uint256[]"}],"name":"getPairDepths","outputs":[{"components":[{"internalType":"uint128","name":"onePercentDepthAboveUsd","type":"uint128"},{"internalType":"uint128","name":"onePercentDepthBelowUsd","type":"uint128"}],"internalType":"struct IPriceImpact.PairDepth[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0d569f27"},{"inputs":[{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"bool","name":"_long","type":"bool"}],"name":"getPriceImpactOi","outputs":[{"internalType":"uint256","name":"activeOi","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xb6d92b02"},{"inputs":[{"internalType":"uint256","name":"_openPrice","type":"uint256"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"bool","name":"_long","type":"bool"},{"internalType":"uint256","name":"_tradeOpenInterestUsd","type":"uint256"}],"name":"getTradePriceImpact","outputs":[{"internalType":"uint256","name":"priceImpactP","type":"uint256"},{"internalType":"uint256","name":"priceAfterImpact","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x7ea95f32"},{"inputs":[{"internalType":"uint48","name":"_windowsDuration","type":"uint48"},{"internalType":"uint48","name":"_windowsCount","type":"uint48"}],"name":"initializePriceImpact","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x01d5664a"},{"inputs":[{"internalType":"uint256","name":"_openInterestUsd","type":"uint256"},{"internalType":"uint256","name":"_pairIndex","type":"uint256"},{"internalType":"bool","name":"_long","type":"bool"},{"internalType":"uint48","name":"_addTs","type":"uint48"}],"name":"removePriceImpactOpenInterest","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xd01c9202"},{"inputs":[{"internalType":"uint256[]","name":"_indices","type":"uint256[]"},{"internalType":"uint128[]","name":"_depthsAboveUsd","type":"uint128[]"},{"internalType":"uint128[]","name":"_depthsBelowUsd","type":"uint128[]"}],"name":"setPairDepths","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x6474b399"},{"inputs":[{"internalType":"uint48","name":"_newWindowsCount","type":"uint48"}],"name":"setPriceImpactWindowsCount","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x10751b4f"},{"inputs":[{"internalType":"uint48","name":"_newWindowsDuration","type":"uint48"}],"name":"setPriceImpactWindowsDuration","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x39b0fc82"},{"inputs":[],"name":"CollateralAlreadyActive","type":"error"},{"inputs":[],"name":"CollateralAlreadyDisabled","type":"error"},{"inputs":[],"name":"MaxSlippageZero","type":"error"},{"inputs":[],"name":"MissingCollaterals","type":"error"},{"inputs":[],"name":"NoSl","type":"error"},{"inputs":[],"name":"NoTp","type":"error"},{"inputs":[],"name":"TradeInfoCollateralPriceUsdZero","type":"error"},{"inputs":[],"name":"TradeOpenPriceZero","type":"error"},{"inputs":[],"name":"TradePairNotListed","type":"error"},{"inputs":[],"name":"TradePositionSizeZero","type":"error"},{"inputs":[],"name":"TradeSlInvalid","type":"error"},{"inputs":[],"name":"TradeTpInvalid","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"collateral","type":"address"},{"indexed":false,"internalType":"uint8","name":"index","type":"uint8"},{"indexed":false,"internalType":"address","name":"gToken","type":"address"}],"name":"CollateralAdded","type":"event","signature":"0xa02b5df63a0ca2660cbe23b5eb92c7f2ae514aee4a543a6032b38ef338865dbf"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"index","type":"uint8"}],"name":"CollateralDisabled","type":"event","signature":"0x09a6e6672fd5a685707eca1eeb3a3ef190ccf5ceaf9a78e410859f2d7983cc92"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"index","type":"uint8"},{"indexed":false,"internalType":"bool","name":"isActive","type":"bool"}],"name":"CollateralUpdated","type":"event","signature":"0x98bbde8d067842c4760a76b32aebf2cd4feb8f07ddcf20d81c619c16f0242ecb"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"collateral","type":"address"},{"indexed":false,"internalType":"uint8","name":"index","type":"uint8"},{"indexed":false,"internalType":"address","name":"gToken","type":"address"}],"name":"GTokenUpdated","type":"event","signature":"0x347ad17cfe896bbbbdf75fa51fd03a1f1366df72ba0baf20ebed1ea1394a8ecd"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"tradeId","type":"tuple"},{"indexed":false,"internalType":"uint64","name":"openPrice","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"tp","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"sl","type":"uint64"},{"indexed":false,"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"name":"OpenOrderDetailsUpdated","type":"event","signature":"0x57166866105b85933cf7d2f84637e524028a4ca84133309f14b2ce0dfc113498"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"}],"name":"PendingOrderClosed","type":"event","signature":"0xf0e19a36a85c073783ad5d0a8026dffa190d250d673c8c80b687cbef125571f3"},{"anonymous":false,"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"indexed":false,"internalType":"struct ITradingStorage.PendingOrder","name":"pendingOrder","type":"tuple"}],"name":"PendingOrderStored","type":"event","signature":"0xc1f6d032e333e12d4ba1d8cdf8c4abc1bcaab7381a4eaa19a918a28f223f519d"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"tradeId","type":"tuple"}],"name":"TradeClosed","type":"event","signature":"0xedf2f9a86d6e2127c61aaaeb10a282ee4e0aa89ea19c7db37df80fece027a493"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"tradeId","type":"tuple"},{"indexed":false,"internalType":"uint120","name":"collateralAmount","type":"uint120"}],"name":"TradeCollateralUpdated","type":"event","signature":"0xce228a7b1b8e239798e94cb2ba581d57501692fc1d29719a891125f1f393826d"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"tradeId","type":"tuple"},{"indexed":false,"internalType":"uint64","name":"newSl","type":"uint64"}],"name":"TradeSlUpdated","type":"event","signature":"0x38f5d5d40d9c4a41aa03d21461f1b07aa6b4ef035fb9d21f02d53a82c712a002"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"indexed":false,"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"components":[{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint32","name":"tpLastUpdatedBlock","type":"uint32"},{"internalType":"uint32","name":"slLastUpdatedBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"},{"internalType":"uint48","name":"lastOiUpdateTs","type":"uint48"},{"internalType":"uint48","name":"collateralPriceUsd","type":"uint48"},{"internalType":"uint48","name":"__placeholder","type":"uint48"}],"indexed":false,"internalType":"struct ITradingStorage.TradeInfo","name":"tradeInfo","type":"tuple"}],"name":"TradeStored","type":"event","signature":"0xc7bc74b68a1f77466e2402a7ce12e5b172bdeef942334e0df67d522309257b90"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"tradeId","type":"tuple"},{"indexed":false,"internalType":"uint64","name":"newTp","type":"uint64"}],"name":"TradeTpUpdated","type":"event","signature":"0x3d045f25e6a6757ae5ca79ce5d28d84d69713804353a02c521d6a5352c0f9e20"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"enum ITradingStorage.TradingActivated","name":"activated","type":"uint8"}],"name":"TradingActivatedUpdated","type":"event","signature":"0x4b502c3b75c299352edc7887297ae0f7c401ed654650a4c0e663458b6ed75fe4"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"address","name":"_gToken","type":"address"}],"name":"addCollateral","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc6783af1"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"}],"name":"closePendingOrder","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x4fb70bba"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"}],"name":"closeTrade","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x8583909b"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getAllPendingOrders","outputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"internalType":"struct ITradingStorage.PendingOrder[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x2d11445f"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getAllTradeInfos","outputs":[{"components":[{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint32","name":"tpLastUpdatedBlock","type":"uint32"},{"internalType":"uint32","name":"slLastUpdatedBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"},{"internalType":"uint48","name":"lastOiUpdateTs","type":"uint48"},{"internalType":"uint48","name":"collateralPriceUsd","type":"uint48"},{"internalType":"uint48","name":"__placeholder","type":"uint48"}],"internalType":"struct ITradingStorage.TradeInfo[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xeb50287f"},{"inputs":[{"internalType":"uint256","name":"_offset","type":"uint256"},{"internalType":"uint256","name":"_limit","type":"uint256"}],"name":"getAllTrades","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xdffd8a1f"},{"inputs":[{"internalType":"uint8","name":"_index","type":"uint8"}],"name":"getCollateral","outputs":[{"components":[{"internalType":"address","name":"collateral","type":"address"},{"internalType":"bool","name":"isActive","type":"bool"},{"internalType":"uint88","name":"__placeholder","type":"uint88"},{"internalType":"uint128","name":"precision","type":"uint128"},{"internalType":"uint128","name":"precisionDelta","type":"uint128"}],"internalType":"struct ITradingStorage.Collateral","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xbb33a55b"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"}],"name":"getCollateralIndex","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x5c3ed7c3"},{"inputs":[],"name":"getCollaterals","outputs":[{"components":[{"internalType":"address","name":"collateral","type":"address"},{"internalType":"bool","name":"isActive","type":"bool"},{"internalType":"uint88","name":"__placeholder","type":"uint88"},{"internalType":"uint128","name":"precision","type":"uint128"},{"internalType":"uint128","name":"precisionDelta","type":"uint128"}],"internalType":"struct ITradingStorage.Collateral[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x78b92636"},{"inputs":[],"name":"getCollateralsCount","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa3e15d09"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"enum ITradingStorage.CounterType","name":"_type","type":"uint8"}],"name":"getCounters","outputs":[{"components":[{"internalType":"uint32","name":"currentIndex","type":"uint32"},{"internalType":"uint32","name":"openCount","type":"uint32"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Counter","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0212f0d6"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getGToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x6a0aff41"},{"inputs":[{"internalType":"enum ITradingStorage.TradeType","name":"_tradeType","type":"uint8"}],"name":"getPendingOpenOrderType","outputs":[{"internalType":"enum ITradingStorage.PendingOrderType","name":"","type":"uint8"}],"stateMutability":"pure","type":"function","constant":true,"signature":"0xc8157967"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"}],"name":"getPendingOrder","outputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"internalType":"struct ITradingStorage.PendingOrder","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xc6e729bb"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getPendingOrders","outputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"internalType":"struct ITradingStorage.PendingOrder[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4c73cb25"},{"inputs":[{"internalType":"uint64","name":"_openPrice","type":"uint64"},{"internalType":"uint64","name":"_currentPrice","type":"uint64"},{"internalType":"bool","name":"_long","type":"bool"},{"internalType":"uint24","name":"_leverage","type":"uint24"}],"name":"getPnlPercent","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"pure","type":"function","constant":true,"signature":"0xb19962e5"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint32","name":"_index","type":"uint32"}],"name":"getTrade","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x15878e07"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint32","name":"_index","type":"uint32"}],"name":"getTradeInfo","outputs":[{"components":[{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint32","name":"tpLastUpdatedBlock","type":"uint32"},{"internalType":"uint32","name":"slLastUpdatedBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"},{"internalType":"uint48","name":"lastOiUpdateTs","type":"uint48"},{"internalType":"uint48","name":"collateralPriceUsd","type":"uint48"},{"internalType":"uint48","name":"__placeholder","type":"uint48"}],"internalType":"struct ITradingStorage.TradeInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x75cd812d"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTradeInfos","outputs":[{"components":[{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint32","name":"tpLastUpdatedBlock","type":"uint32"},{"internalType":"uint32","name":"slLastUpdatedBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"},{"internalType":"uint48","name":"lastOiUpdateTs","type":"uint48"},{"internalType":"uint48","name":"collateralPriceUsd","type":"uint48"},{"internalType":"uint48","name":"__placeholder","type":"uint48"}],"internalType":"struct ITradingStorage.TradeInfo[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0d1e3c94"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"_orderType","type":"uint8"}],"name":"getTradePendingOrderBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x067e84dd"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTraderStored","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xbed8d2da"},{"inputs":[{"internalType":"uint32","name":"_offset","type":"uint32"},{"internalType":"uint32","name":"_limit","type":"uint32"}],"name":"getTraders","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0e503724"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTrades","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4bfad7c0"},{"inputs":[],"name":"getTradingActivated","outputs":[{"internalType":"enum ITradingStorage.TradingActivated","name":"","type":"uint8"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4115c122"},{"inputs":[{"internalType":"address","name":"_gns","type":"address"},{"internalType":"address","name":"_gnsStaking","type":"address"},{"internalType":"address[]","name":"_collaterals","type":"address[]"},{"internalType":"address[]","name":"_gTokens","type":"address[]"}],"name":"initializeTradingStorage","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x1b7d88e5"},{"inputs":[{"internalType":"uint8","name":"_index","type":"uint8"}],"name":"isCollateralActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4d140218"},{"inputs":[{"internalType":"uint8","name":"_index","type":"uint8"}],"name":"isCollateralListed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x1d2ffb42"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"internalType":"struct ITradingStorage.PendingOrder","name":"_pendingOrder","type":"tuple"}],"name":"storePendingOrder","outputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"trade","type":"tuple"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"}],"internalType":"struct ITradingStorage.PendingOrder","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function","signature":"0x93f9384e"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"_trade","type":"tuple"},{"components":[{"internalType":"uint32","name":"createdBlock","type":"uint32"},{"internalType":"uint32","name":"tpLastUpdatedBlock","type":"uint32"},{"internalType":"uint32","name":"slLastUpdatedBlock","type":"uint32"},{"internalType":"uint16","name":"maxSlippageP","type":"uint16"},{"internalType":"uint48","name":"lastOiUpdateTs","type":"uint48"},{"internalType":"uint48","name":"collateralPriceUsd","type":"uint48"},{"internalType":"uint48","name":"__placeholder","type":"uint48"}],"internalType":"struct ITradingStorage.TradeInfo","name":"_tradeInfo","type":"tuple"}],"name":"storeTrade","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function","signature":"0x9f30b640"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"toggleCollateralActiveState","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x49f7895b"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"address","name":"_gToken","type":"address"}],"name":"updateGToken","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x63450d74"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"},{"internalType":"uint64","name":"_openPrice","type":"uint64"},{"internalType":"uint64","name":"_tp","type":"uint64"},{"internalType":"uint64","name":"_sl","type":"uint64"},{"internalType":"uint16","name":"_maxSlippageP","type":"uint16"}],"name":"updateOpenOrderDetails","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xeb2dfde8"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"},{"internalType":"uint120","name":"_collateralAmount","type":"uint120"}],"name":"updateTradeCollateralAmount","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x5a68200d"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"},{"internalType":"uint64","name":"_newSl","type":"uint64"}],"name":"updateTradeSl","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x1053c279"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_tradeId","type":"tuple"},{"internalType":"uint64","name":"_newTp","type":"uint64"}],"name":"updateTradeTp","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xb8f741d4"},{"inputs":[{"internalType":"enum ITradingStorage.TradingActivated","name":"_activated","type":"uint8"}],"name":"updateTradingActivated","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xb78f4b36"},{"inputs":[],"name":"NoPendingTriggerRewards","type":"error"},{"inputs":[],"name":"TimeoutBlocksZero","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"rewardsPerOracleGns","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"oraclesCount","type":"uint256"}],"name":"TriggerRewarded","type":"event","signature":"0x82bfbe6a1c6cb1077af1001e76028d28d03bf40ac393b689ea90d22e10d3f2da"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oracle","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardsGns","type":"uint256"}],"name":"TriggerRewardsClaimed","type":"event","signature":"0x0e430d4d92cf840e4840d7defc88d12f7b5d7e45222f5d571914c734e1cc8335"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"timeoutBlocks","type":"uint16"}],"name":"TriggerTimeoutBlocksUpdated","type":"event","signature":"0x652d3f2e78702ea06eebce1653dfcd9731f4d9888a0032700b1b7b0b051ad6b8"},{"inputs":[{"internalType":"address","name":"_oracle","type":"address"}],"name":"claimPendingTriggerRewards","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x63790a1b"},{"inputs":[{"internalType":"uint256","name":"_rewardGns","type":"uint256"}],"name":"distributeTriggerReward","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x69f5395e"},{"inputs":[{"internalType":"address","name":"_oracle","type":"address"}],"name":"getTriggerPendingRewardsGns","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x9fd0bdad"},{"inputs":[],"name":"getTriggerTimeoutBlocks","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x1187f9bd"},{"inputs":[{"internalType":"uint256","name":"_orderBlock","type":"uint256"}],"name":"hasActiveOrder","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x8765f772"},{"inputs":[{"internalType":"uint16","name":"_timeoutBlocks","type":"uint16"}],"name":"initializeTriggerRewards","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xe2c3542b"},{"inputs":[{"internalType":"uint16","name":"_timeoutBlocks","type":"uint16"}],"name":"updateTriggerTimeoutBlocks","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x9e353611"},{"inputs":[],"name":"AboveGroupMaxOi","type":"error"},{"inputs":[],"name":"AbovePairMaxOi","type":"error"},{"inputs":[],"name":"AlreadyBeingMarketClosed","type":"error"},{"inputs":[],"name":"BelowMinPositionSizeUsd","type":"error"},{"inputs":[],"name":"CollateralNotActive","type":"error"},{"inputs":[],"name":"DelegateNotApproved","type":"error"},{"inputs":[],"name":"DelegatedActionNotAllowed","type":"error"},{"inputs":[],"name":"NoOrder","type":"error"},{"inputs":[],"name":"NoTrade","type":"error"},{"inputs":[],"name":"NotWrappedNativeToken","type":"error"},{"inputs":[],"name":"NotYourOrder","type":"error"},{"inputs":[],"name":"PendingTrigger","type":"error"},{"inputs":[],"name":"PriceImpactTooHigh","type":"error"},{"inputs":[],"name":"PriceZero","type":"error"},{"inputs":[],"name":"WaitTimeout","type":"error"},{"inputs":[],"name":"WrongLeverage","type":"error"},{"inputs":[],"name":"WrongOrderType","type":"error"},{"inputs":[],"name":"WrongSl","type":"error"},{"inputs":[],"name":"WrongTp","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"bool","name":"bypass","type":"bool"}],"name":"ByPassTriggerLinkUpdated","type":"event","signature":"0x06e17fbb36333cd9cb0220b0e3cb4ce4d9d6b543f762e8ca6038422e24fa59e4"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"pendingOrderId","type":"tuple"},{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"}],"name":"ChainlinkCallbackTimeout","type":"event","signature":"0x3f709185dd46048fccc37c6e34d58fff306fc7991fdbae962679345db3ed2e32"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"}],"name":"CouldNotCloseTrade","type":"event","signature":"0x051ed9aeed13c97b879c0dd2b13c76171e2760abe3d62bca140dc70b39bd86f1"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"bool","name":"open","type":"bool"}],"name":"MarketOrderInitiated","type":"event","signature":"0x3a60290d7335bce64a807e90f39655517bb5fa702423fa8fac283a5ea16d3a97"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newValueBlocks","type":"uint256"}],"name":"MarketOrdersTimeoutBlocksUpdated","type":"event","signature":"0x91e136d1ad9bf0a586afd0c7699533d033f9092cc48c9e2e16a8c1bc87a33456"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint256","name":"nativeTokenAmount","type":"uint256"}],"name":"NativeTokenWrapped","type":"event","signature":"0x4140bfb1a8c58243a51a8ab319eda78a7382befc5ff76598e746df60996b9d0d"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"}],"name":"OpenLimitCanceled","type":"event","signature":"0x30a872d1bbd3e31dbb65ce3a53ede9f12b497e1b134c66e64a10f850c4391bf0"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"},{"indexed":false,"internalType":"uint64","name":"newPrice","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"newTp","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"newSl","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"maxSlippageP","type":"uint64"}],"name":"OpenLimitUpdated","type":"event","signature":"0x11c151b754cb223cb771e3d8ece99deae21de397c95d3b1ca4ccb995620766bf"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"}],"name":"OpenOrderPlaced","type":"event","signature":"0xb57382e21e3ceb31b5beda26d7cc7e459dc52a0b1f5ae0c9b4e603401b7dc642"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"bool","name":"byPassesLinkCost","type":"bool"}],"name":"TriggerOrderInitiated","type":"event","signature":"0x1472b674eddef9a7145c9353c62f5c03cfcf54556c14c3a0ebbf394da6e0c9ea"},{"inputs":[{"internalType":"uint32","name":"_index","type":"uint32"}],"name":"cancelOpenOrder","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x85886333"},{"inputs":[{"internalType":"uint32","name":"_index","type":"uint32"}],"name":"closeTradeMarket","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xbdb340cd"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"}],"name":"closeTradeMarketTimeout","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x03537a5f"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"},{"internalType":"bytes","name":"_callData","type":"bytes"}],"name":"delegatedTradingAction","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function","signature":"0x737b84cd"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getByPassTriggerLink","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x85898e08"},{"inputs":[],"name":"getMarketOrdersTimeoutBlocks","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa4bdee80"},{"inputs":[{"internalType":"address","name":"_trader","type":"address"}],"name":"getTradingDelegate","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x4aac6480"},{"inputs":[],"name":"getWrappedNativeToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x1d9478b6"},{"inputs":[{"internalType":"uint16","name":"_marketOrdersTimeoutBlocks","type":"uint16"},{"internalType":"address[]","name":"_usersByPassTriggerLink","type":"address[]"}],"name":"initializeTrading","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x5179cecf"},{"inputs":[{"internalType":"address","name":"_token","type":"address"}],"name":"isWrappedNativeToken","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x84e93347"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"_trade","type":"tuple"},{"internalType":"uint16","name":"_maxSlippageP","type":"uint16"},{"internalType":"address","name":"_referrer","type":"address"}],"name":"openTrade","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x4465c3e4"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"}],"name":"openTradeMarketTimeout","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x0cff665e"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"internalType":"struct ITradingStorage.Trade","name":"_trade","type":"tuple"},{"internalType":"uint16","name":"_maxSlippageP","type":"uint16"},{"internalType":"address","name":"_referrer","type":"address"}],"name":"openTradeNative","outputs":[],"stateMutability":"payable","type":"function","payable":true,"signature":"0x080e83e1"},{"inputs":[],"name":"removeTradingDelegate","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x031c722b"},{"inputs":[{"internalType":"address","name":"_delegate","type":"address"}],"name":"setTradingDelegate","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x604755cf"},{"inputs":[{"internalType":"uint256","name":"_packed","type":"uint256"}],"name":"triggerOrder","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xeb9359aa"},{"inputs":[{"internalType":"address[]","name":"_users","type":"address[]"},{"internalType":"bool[]","name":"_shouldByPass","type":"bool[]"}],"name":"updateByPassTriggerLink","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x9bf1584e"},{"inputs":[{"internalType":"uint16","name":"_valueBlocks","type":"uint16"}],"name":"updateMarketOrdersTimeoutBlocks","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x52d029d2"},{"inputs":[{"internalType":"uint32","name":"_index","type":"uint32"},{"internalType":"uint64","name":"_triggerPrice","type":"uint64"},{"internalType":"uint64","name":"_tp","type":"uint64"},{"internalType":"uint64","name":"_sl","type":"uint64"},{"internalType":"uint16","name":"_maxSlippageP","type":"uint16"}],"name":"updateOpenOrder","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xa4bb127e"},{"inputs":[{"internalType":"uint32","name":"_index","type":"uint32"},{"internalType":"uint64","name":"_newSl","type":"uint64"}],"name":"updateSl","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xb5d9e9d0"},{"inputs":[{"internalType":"uint32","name":"_index","type":"uint32"},{"internalType":"uint64","name":"_newTp","type":"uint64"}],"name":"updateTp","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xf401f2bb"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"BorrowingFeeCharged","type":"event","signature":"0x2aac04047becf1d92defe3c1ee644bdd7b50ae634a7e5ebfca84c2be3fc63344"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"GTokenFeeCharged","type":"event","signature":"0xfe4ab97508a97bb85ad1e2680662e58549e51982d965eed4ef6d7fcd4cc4295f"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"GnsStakingFeeCharged","type":"event","signature":"0x8e4c272f039ef17bb8cb5a5bc5d6f0cebf9c5037dceae9528bb05b0c4f5a7b80"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"GovFeeCharged","type":"event","signature":"0xeb561f0609b402569e8a7e8fe9d4f408b92c96fb83001b2cd78fd55c29bbbac3"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"indexed":false,"internalType":"struct ITradingStorage.Trade","name":"t","type":"tuple"},{"indexed":true,"internalType":"address","name":"triggerCaller","type":"address"},{"indexed":false,"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"priceImpactP","type":"uint256"},{"indexed":false,"internalType":"int256","name":"percentProfit","type":"int256"},{"indexed":false,"internalType":"uint256","name":"amountSentToTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collateralPriceUsd","type":"uint256"},{"indexed":false,"internalType":"bool","name":"exactExecution","type":"bool"}],"name":"LimitExecuted","type":"event","signature":"0xc10f67c0e22c53149183a414c16a62334103432a2c48b839a057cd9bd5fdeb99"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"enum ITradingCallbacks.CancelReason","name":"cancelReason","type":"uint8"}],"name":"MarketCloseCanceled","type":"event","signature":"0x1d7048e18d77f0864147aec27ae4b78d421fe35ddde1ea0ec535562c4a90cc58"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint24","name":"leverage","type":"uint24"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"bool","name":"isOpen","type":"bool"},{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"enum ITradingStorage.TradeType","name":"tradeType","type":"uint8"},{"internalType":"uint120","name":"collateralAmount","type":"uint120"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"uint64","name":"tp","type":"uint64"},{"internalType":"uint64","name":"sl","type":"uint64"},{"internalType":"uint192","name":"__placeholder","type":"uint192"}],"indexed":false,"internalType":"struct ITradingStorage.Trade","name":"t","type":"tuple"},{"indexed":false,"internalType":"bool","name":"open","type":"bool"},{"indexed":false,"internalType":"uint64","name":"price","type":"uint64"},{"indexed":false,"internalType":"uint256","name":"priceImpactP","type":"uint256"},{"indexed":false,"internalType":"int256","name":"percentProfit","type":"int256"},{"indexed":false,"internalType":"uint256","name":"amountSentToTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collateralPriceUsd","type":"uint256"}],"name":"MarketExecuted","type":"event","signature":"0xbbd5cfa7b4ec0d44d4155fcaad32af9cf7e65799d6b8b08f233b930de7bcd9a8"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"enum ITradingCallbacks.CancelReason","name":"cancelReason","type":"uint8"}],"name":"MarketOpenCanceled","type":"event","signature":"0x377325122a5a86014bf0a307dc0c8eab0bf1e2858ff6e1522a7551e6df253782"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"PendingGovFeesClaimed","type":"event","signature":"0x0b92b2d73b4c8443d11985dbf6a8cfdfc03b93d6679aab94b7d4fb5842dd0cb0"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"ReferralFeeCharged","type":"event","signature":"0x264425c9f39f6b517f96e5447a9347098bfbe112753fada5068de9fdf6d5168c"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"amountCollateral","type":"uint256"}],"name":"TriggerFeeCharged","type":"event","signature":"0x9460073dee9bbc6b4566aae39b3ec7308696e65ec5d376434076d72afabe3eba"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"address","name":"triggerCaller","type":"address"},{"indexed":false,"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"indexed":false,"internalType":"enum ITradingCallbacks.CancelReason","name":"cancelReason","type":"uint8"}],"name":"TriggerOrderCanceled","type":"event","signature":"0x0766d5a97748cddd280198f717da563fe9aad4d38e5bd546fe56d04fbc68a3cd"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"valueP","type":"uint8"}],"name":"VaultClosingFeePUpdated","type":"event","signature":"0x1be5a8e0282c1b895f845900a8efe7585790659f1b4f062f17000e2712dd8601"},{"inputs":[],"name":"claimPendingGovFees","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x36c3dba2"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint64","name":"price","type":"uint64"},{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"}],"internalType":"struct ITradingCallbacks.AggregatorAnswer","name":"_a","type":"tuple"}],"name":"closeTradeMarketCallback","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x4b0b5629"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint64","name":"price","type":"uint64"},{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"}],"internalType":"struct ITradingCallbacks.AggregatorAnswer","name":"_a","type":"tuple"}],"name":"executeTriggerCloseOrderCallback","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc61a7ad4"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint64","name":"price","type":"uint64"},{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"}],"internalType":"struct ITradingCallbacks.AggregatorAnswer","name":"_a","type":"tuple"}],"name":"executeTriggerOpenOrderCallback","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x3b0c5938"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getPendingGovFeesCollateral","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x2c6fe6d1"},{"inputs":[],"name":"getVaultClosingFeeP","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa5b26e46"},{"inputs":[{"internalType":"uint8","name":"_vaultClosingFeeP","type":"uint8"}],"name":"initializeCallbacks","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xec98ec83"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint64","name":"price","type":"uint64"},{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"}],"internalType":"struct ITradingCallbacks.AggregatorAnswer","name":"_a","type":"tuple"}],"name":"openTradeMarketCallback","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x13ebc2c6"},{"inputs":[{"internalType":"uint8","name":"_valueP","type":"uint8"}],"name":"updateVaultClosingFeeP","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xcbc8e6f2"},{"inputs":[],"name":"BorrowingWrongExponent","type":"error"},{"inputs":[],"name":"BorrowingZeroGroup","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"groupIndex","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"currentBlock","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"accFeeShort","type":"uint64"}],"name":"BorrowingGroupAccFeesUpdated","type":"event","signature":"0xb4297e7afacc3feba1f03e1a444e70031a62f3ae4d6372c2b0cb3e0e62e8568e"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"groupIndex","type":"uint16"},{"indexed":false,"internalType":"bool","name":"long","type":"bool"},{"indexed":false,"internalType":"bool","name":"increase","type":"bool"},{"indexed":false,"internalType":"uint72","name":"delta","type":"uint72"},{"indexed":false,"internalType":"uint72","name":"newOiLong","type":"uint72"},{"indexed":false,"internalType":"uint72","name":"newOiShort","type":"uint72"}],"name":"BorrowingGroupOiUpdated","type":"event","signature":"0xb36af604fa0e5c3505abb63091d204895a517928138498bb965622d2258bdeb5"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"groupIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"indexed":false,"internalType":"uint72","name":"maxOi","type":"uint72"},{"indexed":false,"internalType":"uint48","name":"feeExponent","type":"uint48"}],"name":"BorrowingGroupUpdated","type":"event","signature":"0x8f029f3a48396ff1466df7488d31984ab9265a55be3de042cd03662ad2c894ca"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"},{"indexed":false,"internalType":"uint64","name":"initialPairAccFee","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"initialGroupAccFee","type":"uint64"}],"name":"BorrowingInitialAccFeesStored","type":"event","signature":"0x0630d8200c5131fd33e89f6e386588553026397795e46cfc6736e4af82f4e6d9"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"currentBlock","type":"uint256"},{"indexed":false,"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"indexed":false,"internalType":"uint64","name":"accFeeShort","type":"uint64"}],"name":"BorrowingPairAccFeesUpdated","type":"event","signature":"0x12515cf8712ede0f0e48dd7513c14f22f116a6b3f95bd493da7511cf7dcbadd7"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"prevGroupIndex","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"newGroupIndex","type":"uint16"}],"name":"BorrowingPairGroupUpdated","type":"event","signature":"0x2281c18b617b78612026764ea9d5175174342c49b30da77900f7518a83242fa7"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"bool","name":"long","type":"bool"},{"indexed":false,"internalType":"bool","name":"increase","type":"bool"},{"indexed":false,"internalType":"uint72","name":"delta","type":"uint72"},{"indexed":false,"internalType":"uint72","name":"newOiLong","type":"uint72"},{"indexed":false,"internalType":"uint72","name":"newOiShort","type":"uint72"}],"name":"BorrowingPairOiUpdated","type":"event","signature":"0x012adc2457c8405bb9a0f2f3be4cc4bff84f095e6a16535b080facddec7804d3"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":true,"internalType":"uint16","name":"groupIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"indexed":false,"internalType":"uint48","name":"feeExponent","type":"uint48"},{"indexed":false,"internalType":"uint72","name":"maxOi","type":"uint72"}],"name":"BorrowingPairParamsUpdated","type":"event","signature":"0x3984f24e4863ca281d86902d6706218ef6b050f256dcc978dbe508eaf8c3a431"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":true,"internalType":"address","name":"trader","type":"address"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"uint32","name":"index","type":"uint32"},{"indexed":false,"internalType":"bool","name":"open","type":"bool"},{"indexed":false,"internalType":"bool","name":"long","type":"bool"},{"indexed":false,"internalType":"uint256","name":"positionSizeCollateral","type":"uint256"}],"name":"TradeBorrowingCallbackHandled","type":"event","signature":"0x1d4556af371eac83495a853ba4f1af8a2d4e0c76ab08719dbd24b372cfc0acc3"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getAllBorrowingPairs","outputs":[{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint48","name":"accLastUpdatedBlock","type":"uint48"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingData[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint72","name":"long","type":"uint72"},{"internalType":"uint72","name":"short","type":"uint72"},{"internalType":"uint72","name":"max","type":"uint72"},{"internalType":"uint40","name":"__placeholder","type":"uint40"}],"internalType":"struct IBorrowingFees.OpenInterest[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint16","name":"groupIndex","type":"uint16"},{"internalType":"uint48","name":"block","type":"uint48"},{"internalType":"uint64","name":"initialAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"initialAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"prevGroupAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"prevGroupAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"pairAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"pairAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"__placeholder","type":"uint64"}],"internalType":"struct IBorrowingFees.BorrowingPairGroup[][]","name":"","type":"tuple[][]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x48da5b38"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_groupIndex","type":"uint16"}],"name":"getBorrowingGroup","outputs":[{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint48","name":"accLastUpdatedBlock","type":"uint48"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingData","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xfff24740"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_groupIndex","type":"uint16"}],"name":"getBorrowingGroupOi","outputs":[{"components":[{"internalType":"uint72","name":"long","type":"uint72"},{"internalType":"uint72","name":"short","type":"uint72"},{"internalType":"uint72","name":"max","type":"uint72"},{"internalType":"uint40","name":"__placeholder","type":"uint40"}],"internalType":"struct IBorrowingFees.OpenInterest","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x13a9baae"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_groupIndex","type":"uint16"},{"internalType":"uint256","name":"_currentBlock","type":"uint256"}],"name":"getBorrowingGroupPendingAccFees","outputs":[{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint64","name":"groupAccFeeDelta","type":"uint64"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xd2b9099a"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16[]","name":"_indices","type":"uint16[]"}],"name":"getBorrowingGroups","outputs":[{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint48","name":"accLastUpdatedBlock","type":"uint48"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingData[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint72","name":"long","type":"uint72"},{"internalType":"uint72","name":"short","type":"uint72"},{"internalType":"uint72","name":"max","type":"uint72"},{"internalType":"uint40","name":"__placeholder","type":"uint40"}],"internalType":"struct IBorrowingFees.OpenInterest[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xfbbf9740"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint32","name":"_index","type":"uint32"}],"name":"getBorrowingInitialAccFees","outputs":[{"components":[{"internalType":"uint64","name":"accPairFee","type":"uint64"},{"internalType":"uint64","name":"accGroupFee","type":"uint64"},{"internalType":"uint48","name":"block","type":"uint48"},{"internalType":"uint80","name":"__placeholder","type":"uint80"}],"internalType":"struct IBorrowingFees.BorrowingInitialAccFees","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xab6192ed"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getBorrowingPair","outputs":[{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint48","name":"accLastUpdatedBlock","type":"uint48"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingData","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x5d5bf24d"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getBorrowingPairGroupIndex","outputs":[{"internalType":"uint16","name":"groupIndex","type":"uint16"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xe6a6633f"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getBorrowingPairGroups","outputs":[{"components":[{"internalType":"uint16","name":"groupIndex","type":"uint16"},{"internalType":"uint48","name":"block","type":"uint48"},{"internalType":"uint64","name":"initialAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"initialAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"prevGroupAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"prevGroupAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"pairAccFeeLong","type":"uint64"},{"internalType":"uint64","name":"pairAccFeeShort","type":"uint64"},{"internalType":"uint64","name":"__placeholder","type":"uint64"}],"internalType":"struct IBorrowingFees.BorrowingPairGroup[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xfd03e048"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getBorrowingPairOi","outputs":[{"components":[{"internalType":"uint72","name":"long","type":"uint72"},{"internalType":"uint72","name":"short","type":"uint72"},{"internalType":"uint72","name":"max","type":"uint72"},{"internalType":"uint40","name":"__placeholder","type":"uint40"}],"internalType":"struct IBorrowingFees.OpenInterest","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0077b57e"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"internalType":"uint256","name":"_currentBlock","type":"uint256"}],"name":"getBorrowingPairPendingAccFees","outputs":[{"internalType":"uint64","name":"accFeeLong","type":"uint64"},{"internalType":"uint64","name":"accFeeShort","type":"uint64"},{"internalType":"uint64","name":"pairAccFeeDelta","type":"uint64"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0c7be6ca"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getPairMaxOi","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x5667b5c0"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getPairMaxOiCollateral","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x274d1278"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"internalType":"bool","name":"_long","type":"bool"}],"name":"getPairOiCollateral","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xeb2ea3a2"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"}],"name":"getPairOisCollateral","outputs":[{"internalType":"uint256","name":"longOi","type":"uint256"},{"internalType":"uint256","name":"shortOi","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xf6f7c948"},{"inputs":[{"components":[{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"address","name":"trader","type":"address"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"uint256","name":"collateral","type":"uint256"},{"internalType":"uint256","name":"leverage","type":"uint256"}],"internalType":"struct IBorrowingFees.BorrowingFeeInput","name":"_input","type":"tuple"}],"name":"getTradeBorrowingFee","outputs":[{"internalType":"uint256","name":"feeAmountCollateral","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x0804db93"},{"inputs":[{"components":[{"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"internalType":"address","name":"trader","type":"address"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"uint64","name":"openPrice","type":"uint64"},{"internalType":"bool","name":"long","type":"bool"},{"internalType":"uint256","name":"collateral","type":"uint256"},{"internalType":"uint24","name":"leverage","type":"uint24"}],"internalType":"struct IBorrowingFees.LiqPriceInput","name":"_input","type":"tuple"}],"name":"getTradeLiquidationPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x30b3c31f"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"address","name":"_trader","type":"address"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"internalType":"uint32","name":"_index","type":"uint32"},{"internalType":"uint256","name":"_positionSizeCollateral","type":"uint256"},{"internalType":"bool","name":"_open","type":"bool"},{"internalType":"bool","name":"_long","type":"bool"}],"name":"handleTradeBorrowingCallback","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xfc79e929"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_groupIndex","type":"uint16"},{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint72","name":"maxOi","type":"uint72"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingGroupParams","name":"_value","type":"tuple"}],"name":"setBorrowingGroupParams","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x9fed9481"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16[]","name":"_indices","type":"uint16[]"},{"components":[{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint72","name":"maxOi","type":"uint72"},{"internalType":"uint48","name":"feeExponent","type":"uint48"}],"internalType":"struct IBorrowingFees.BorrowingGroupParams[]","name":"_values","type":"tuple[]"}],"name":"setBorrowingGroupParamsArray","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x02c4e7c1"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"components":[{"internalType":"uint16","name":"groupIndex","type":"uint16"},{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint48","name":"feeExponent","type":"uint48"},{"internalType":"uint72","name":"maxOi","type":"uint72"}],"internalType":"struct IBorrowingFees.BorrowingPairParams","name":"_value","type":"tuple"}],"name":"setBorrowingPairParams","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x33b516cf"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16[]","name":"_indices","type":"uint16[]"},{"components":[{"internalType":"uint16","name":"groupIndex","type":"uint16"},{"internalType":"uint32","name":"feePerBlock","type":"uint32"},{"internalType":"uint48","name":"feeExponent","type":"uint48"},{"internalType":"uint72","name":"maxOi","type":"uint72"}],"internalType":"struct IBorrowingFees.BorrowingPairParams[]","name":"_values","type":"tuple[]"}],"name":"setBorrowingPairParamsArray","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xeb1802f8"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"internalType":"bool","name":"_long","type":"bool"},{"internalType":"uint256","name":"_positionSizeCollateral","type":"uint256"}],"name":"withinMaxBorrowingGroupOi","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x801c7961"},{"inputs":[],"name":"InvalidCandle","type":"error"},{"inputs":[],"name":"OracleAlreadyListed","type":"error"},{"inputs":[],"name":"RequestAlreadyPending","type":"error"},{"inputs":[],"name":"SourceNotOracleOfRequest","type":"error"},{"inputs":[],"name":"T","type":"error"},{"inputs":[],"name":"TransferAndCallToOracleFailed","type":"error"},{"inputs":[],"name":"WrongCollateralUsdDecimals","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkFulfilled","type":"event","signature":"0x7cc135e0cebb02c3480ae5d74d377283180a2601f8f644edf7987b009316c63a"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkRequested","type":"event","signature":"0xb5e6e01e79f91267dc17b4e6314d5d4d03593d2ceee0fbb452b750bd70ea5af9"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"components":[{"internalType":"contract IUniswapV3Pool","name":"pool","type":"address"},{"internalType":"bool","name":"isGnsToken0InLp","type":"bool"},{"internalType":"uint88","name":"__placeholder","type":"uint88"}],"indexed":false,"internalType":"struct IPriceAggregator.UniV3PoolInfo","name":"newValue","type":"tuple"}],"name":"CollateralGnsUniV3PoolUpdated","type":"event","signature":"0x1edbae8d78eb52b7442e21be32c837a2c2521fd9d806d1f469f2c9e8f469ab75"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"address","name":"value","type":"address"}],"name":"CollateralUsdPriceFeedUpdated","type":"event","signature":"0x272401831c29114837867a7463e326c1b024e3dd2f0f108dec76352011db4fea"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"jobId","type":"bytes32"}],"name":"JobIdUpdated","type":"event","signature":"0x764c19c693af0da42ec6c6bed68a2dd1a2fa93d24785fcfce58ffa29ae313606"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountLink","type":"uint256"}],"name":"LinkClaimedBack","type":"event","signature":"0xc4fc8431efbe3edf6cca5a73401623d342a9fad5807bcb502d2efca245cb6ffd"},{"anonymous":false,"inputs":[{"components":[{"internalType":"bytes32","name":"id","type":"bytes32"},{"internalType":"address","name":"callbackAddress","type":"address"},{"internalType":"bytes4","name":"callbackFunctionId","type":"bytes4"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"components":[{"internalType":"bytes","name":"buf","type":"bytes"},{"internalType":"uint256","name":"capacity","type":"uint256"}],"internalType":"struct BufferChainlink.buffer","name":"buf","type":"tuple"}],"indexed":false,"internalType":"struct Chainlink.Request","name":"request","type":"tuple"}],"name":"LinkRequestCreated","type":"event","signature":"0x170ae993ffa82f60cce26e128cf75e11b7deba03fe29685e5881a76c8452765c"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"value","type":"address"}],"name":"LinkUsdPriceFeedUpdated","type":"event","signature":"0xca648bfe353681131df098ecd895a5ec41f502a93a1223aa1b77f67fc271f2a3"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"value","type":"uint8"}],"name":"MinAnswersUpdated","type":"event","signature":"0x6bc925491f55f56cb08a3ff41035fb0fdeae0cecc94f8e32e9b8ba2ad17fa7f9"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"address","name":"value","type":"address"}],"name":"OracleAdded","type":"event","signature":"0xbf21de46ba0ce5e377db4224a7253064e85c704765b54881c2ad551a30a28d0b"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"address","name":"oldOracle","type":"address"}],"name":"OracleRemoved","type":"event","signature":"0x0adc4a8d7cd2f125c921a2f757c5c86749579208090d4fbb65c26bae90179ac0"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"address","name":"oldOracle","type":"address"},{"indexed":false,"internalType":"address","name":"newOracle","type":"address"}],"name":"OracleReplaced","type":"event","signature":"0x36f00e7308d970ca7446a252b7a1dd9c9cb50ea4559b602e595fc53967ac9dd9"},{"anonymous":false,"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"indexed":true,"internalType":"uint16","name":"pairIndex","type":"uint16"},{"indexed":false,"internalType":"bytes32","name":"request","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"priceData","type":"uint256"},{"indexed":false,"internalType":"bool","name":"isLookback","type":"bool"},{"indexed":false,"internalType":"bool","name":"usedInMedian","type":"bool"}],"name":"PriceReceived","type":"event","signature":"0x1d01fcc0e82c93f463da710266800aff752bf7da2435090b30616276602eb75a"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"indexed":false,"internalType":"struct ITradingStorage.Id","name":"pendingOrderId","type":"tuple"},{"indexed":true,"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"indexed":true,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":true,"internalType":"bytes32","name":"job","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"nodesCount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"linkFeePerNode","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"fromBlock","type":"uint256"},{"indexed":false,"internalType":"bool","name":"isLookback","type":"bool"}],"name":"PriceRequested","type":"event","signature":"0xff0844642ee620558da9bd3e51a00e4e70e563b544dd6ef6529fd4068eea8dc9"},{"anonymous":false,"inputs":[{"components":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"orderId","type":"tuple"},{"internalType":"uint256","name":"spreadP","type":"uint256"},{"internalType":"uint64","name":"price","type":"uint64"},{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"}],"indexed":false,"internalType":"struct ITradingCallbacks.AggregatorAnswer","name":"a","type":"tuple"},{"indexed":false,"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"}],"name":"TradingCallbackExecuted","type":"event","signature":"0x3c7b39f62241be54daf88ab94fbb4f3b7e92a2abb908f2d2b4ce3d14dadd5a4f"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"newValue","type":"uint32"}],"name":"TwapIntervalUpdated","type":"event","signature":"0xc99f383ecd620c333255bd2aef929eedd6808999bac9bfc5f53e10d876abf1ce"},{"inputs":[{"internalType":"address","name":"_a","type":"address"}],"name":"addOracle","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xdf5dd1a5"},{"inputs":[],"name":"claimBackLink","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x6f37d263"},{"inputs":[{"internalType":"bytes32","name":"_requestId","type":"bytes32"},{"internalType":"uint256","name":"_priceData","type":"uint256"}],"name":"fulfill","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x4357855e"},{"inputs":[],"name":"getChainlinkToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x165d35e1"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint256","name":"_normalizedValue","type":"uint256"}],"name":"getCollateralFromUsdNormalizedValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x36f6def7"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getCollateralGnsUniV3Pool","outputs":[{"components":[{"internalType":"contract IUniswapV3Pool","name":"pool","type":"address"},{"internalType":"bool","name":"isGnsToken0InLp","type":"bool"},{"internalType":"uint88","name":"__placeholder","type":"uint88"}],"internalType":"struct IPriceAggregator.UniV3PoolInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xd1d80eb8"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getCollateralPriceUsd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xbbb4e3f9"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getCollateralUsdPriceFeed","outputs":[{"internalType":"contract IChainlinkFeed","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x9641c1f5"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"}],"name":"getGnsPriceCollateralAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x1de109d2"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getGnsPriceCollateralIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xa91fa361"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getGnsPriceUsd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x891e656c"},{"inputs":[],"name":"getLimitJobId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xf4b0664d"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"internalType":"uint256","name":"_positionSizeCollateral","type":"uint256"}],"name":"getLinkFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x9cf0cc0e"},{"inputs":[],"name":"getLinkUsdPriceFeed","outputs":[{"internalType":"contract IChainlinkFeed","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xb144bbf0"},{"inputs":[],"name":"getMarketJobId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x8e667ac8"},{"inputs":[],"name":"getMinAnswers","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x69b53230"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x10a9de60"},{"inputs":[],"name":"getOracles","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x40884c52"},{"inputs":[{"internalType":"bytes32","name":"_id","type":"bytes32"}],"name":"getPendingRequest","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x88b12d55"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_pairIndex","type":"uint16"},{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"_orderType","type":"uint8"},{"internalType":"uint256","name":"_positionSizeCollateral","type":"uint256"},{"internalType":"uint256","name":"_fromBlock","type":"uint256"}],"name":"getPrice","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xf51d0dc0"},{"inputs":[{"internalType":"bytes32","name":"_requestId","type":"bytes32"}],"name":"getPriceAggregatorOrder","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"},{"internalType":"enum ITradingStorage.PendingOrderType","name":"orderType","type":"uint8"},{"internalType":"uint16","name":"pairIndex","type":"uint16"},{"internalType":"bool","name":"isLookback","type":"bool"},{"internalType":"uint32","name":"__placeholder","type":"uint32"}],"internalType":"struct IPriceAggregator.Order","name":"","type":"tuple"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x7d0fcd1e"},{"inputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"index","type":"uint32"}],"internalType":"struct ITradingStorage.Id","name":"_orderId","type":"tuple"}],"name":"getPriceAggregatorOrderAnswers","outputs":[{"components":[{"internalType":"uint64","name":"open","type":"uint64"},{"internalType":"uint64","name":"high","type":"uint64"},{"internalType":"uint64","name":"low","type":"uint64"},{"internalType":"uint64","name":"ts","type":"uint64"}],"internalType":"struct IPriceAggregator.OrderAnswer[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x9f62038f"},{"inputs":[],"name":"getRequestCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x3fad1834"},{"inputs":[],"name":"getTwapInterval","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function","constant":true,"signature":"0x3e742e3b"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint256","name":"_collateralValue","type":"uint256"}],"name":"getUsdNormalizedValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function","constant":true,"signature":"0xbbad411a"},{"inputs":[{"internalType":"address","name":"_linkToken","type":"address"},{"internalType":"contract IChainlinkFeed","name":"_linkUsdPriceFeed","type":"address"},{"internalType":"uint24","name":"_twapInterval","type":"uint24"},{"internalType":"uint8","name":"_minAnswers","type":"uint8"},{"internalType":"address[]","name":"_nodes","type":"address[]"},{"internalType":"bytes32[2]","name":"_jobIds","type":"bytes32[2]"},{"internalType":"uint8[]","name":"_collateralIndices","type":"uint8[]"},{"internalType":"contract IUniswapV3Pool[]","name":"_gnsCollateralUniV3Pools","type":"address[]"},{"internalType":"contract IChainlinkFeed[]","name":"_collateralUsdPriceFeeds","type":"address[]"}],"name":"initializePriceAggregator","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x488b411a"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"removeOracle","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x80935dbf"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"},{"internalType":"address","name":"_a","type":"address"}],"name":"replaceOracle","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x25e589cd"},{"inputs":[{"internalType":"bytes32","name":"_jobId","type":"bytes32"}],"name":"setLimitJobId","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xe0bb91c2"},{"inputs":[{"internalType":"bytes32","name":"_jobId","type":"bytes32"}],"name":"setMarketJobId","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x85f276b8"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"contract IUniswapV3Pool","name":"_uniV3Pool","type":"address"}],"name":"updateCollateralGnsUniV3Pool","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xea06d1bd"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"contract IChainlinkFeed","name":"_value","type":"address"}],"name":"updateCollateralUsdPriceFeed","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xc07d2844"},{"inputs":[{"internalType":"contract IChainlinkFeed","name":"_value","type":"address"}],"name":"updateLinkUsdPriceFeed","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x5beda778"},{"inputs":[{"internalType":"uint8","name":"_value","type":"uint8"}],"name":"updateMinAnswers","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x44eb8ba6"},{"inputs":[{"internalType":"uint24","name":"_twapInterval","type":"uint24"}],"name":"updateTwapInterval","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xb166a495"},{"inputs":[],"name":"Incomplete","type":"error"},{"inputs":[],"name":"InvalidCollateral","type":"error"},{"inputs":[],"name":"InvalidMaxIndex","type":"error"},{"inputs":[],"name":"StateAlreadyCopied","type":"error"},{"inputs":[],"name":"TradingNotPaused","type":"error"},{"inputs":[],"name":"UnknownChain","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint16","name":"groupsCount","type":"uint16"}],"name":"BorrowingFeesGroupsCopied","type":"event","signature":"0x1b43c788d4b7cc12f87bcc2d82bb79af4e020b6ce5873073dd03aeeb260f9193"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"pairsCount","type":"uint256"}],"name":"BorrowingFeesPairOisCopied","type":"event","signature":"0x8140b9f8c050d5c619189c1086a0b71e37f7a64570832aa99630e213bc573db3"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"pairsCount","type":"uint256"}],"name":"BorrowingFeesPairsCopied","type":"event","signature":"0x8d288d49f0d1e6f6c794cbf2878b79d58f15aea64cba568a9eb161f220ce4e9c"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"balance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"govFees","type":"uint256"}],"name":"CollateralTransferred","type":"event","signature":"0x9c480fe4b458d282b357cd084719069ad52a0f61b3cad1a5404cad84275df95d"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"LegacyLimitOrderSkipped","type":"event","signature":"0xe2db30bf307122de186fe744495a674e475b322106bcd2258de1ec674a72204f"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"fromIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toIndex","type":"uint256"}],"name":"LimitsCopied","type":"event","signature":"0x964a4bb7d7d1ffdcfef28a704276aaaf213b8f4661869e1da12a78f7aafb7ece"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"}],"name":"MarkedAsDone","type":"event","signature":"0x3fc951e21ca09685afb9ddb09ddc070bcc0a4df5a83e30e9d89c8d8dfae44e9b"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tradersCount","type":"uint256"}],"name":"PairTradesCopied","type":"event","signature":"0x7b6ebdacba0b68936d0a6c968dcb4b94361854c8bbbb9cbf7c4089b21309e1ac"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"uint256","name":"pairIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"prevIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newIndex","type":"uint256"}],"name":"TradeCopied","type":"event","signature":"0x9a2e687f2e96cb6af8f2dc868ea2def2f6e7ceae23735aae78c25c8ab0c8a81b"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"tradersCount","type":"uint256"}],"name":"TraderDelegationsCopied","type":"event","signature":"0x0b9649501e0355375bdfcd349c799126512858a0791e564ebadee948941c799d"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"collateralIndex","type":"uint8"},{"indexed":false,"internalType":"uint16","name":"fromPairIndex","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"toPairIndex","type":"uint16"}],"name":"TradesCopied","type":"event","signature":"0xbed7a2543d6e2b6b127e58a1c8224d7e8e2b05db57afeaafdcd3bf5e98a25c5b"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"address[]","name":"_traders","type":"address[]"}],"name":"copyAllState","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x16d6761c"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"copyBorrowingFeesGroups","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xbb28454e"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"copyBorrowingFeesPairs","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xf1234caa"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint256","name":"_maxIndex","type":"uint256"}],"name":"copyLimits","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xa2da5cba"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"copyPairOis","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xb9fa5364"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"address[]","name":"_traders","type":"address[]"}],"name":"copyTraderDelegations","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0x2041cb92"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"uint16","name":"_maxPairIndex","type":"uint16"}],"name":"copyTrades","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xf3828168"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"},{"internalType":"enum ITradingStateCopy.COPY_STAGE","name":"_stage","type":"uint8"}],"name":"getCollateralStageState","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function","signature":"0x3298c266"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"getCollateralState","outputs":[{"internalType":"enum ITradingStateCopy.COPY_STATE","name":"","type":"uint8"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function","signature":"0xcf4bb1a9"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"markAsDone","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xd7a5d283"},{"inputs":[{"internalType":"uint8","name":"_collateralIndex","type":"uint8"}],"name":"transferBalance","outputs":[],"stateMutability":"nonpayable","type":"function","signature":"0xf01162c3"}]')




class Collector:
    def __init__(self):
        self.content = []
        self.built_in_print = print  # Save the original print function

    def start_collecting(self):
        global print
        print = self.collect_prints

    def collect_prints(self, *args, **kwargs):
        output = " ".join(map(str, args))  # Convert all arguments to strings
        self.content.append(output)
        self.built_in_print(*args, **kwargs)  # Print to standard output

    def stop_collecting(self):
        global print
        print = self.built_in_print  # Restore the original print function





# Google sheet number dictionary
dex_to_open_positions_dictionary = {
    "GMXV1" : 1, # Index 3 corresponds to the fourth sheet
    "GMXV2" : 2,
    "GAINS" : 3, 
    "MUX" : 4,
}




## (READY) (August 4th 2024) (this buys atleast min_qty) (with email top button) (try adn except in sheets and emailing)
## ----------------------Complete Trading Bot Class for all trading related things--------------------------
class Trading_Things: 
    
    def __init__(self):
        try:
            # Specify the path to your service account JSON file
            # credentials_file = "btc-server-trading-data-77c9789d4ab9.json"
            # https://www.youtube.com/watch?v=zCEJurLGFRk&t=1318s   Refer to this video in future if needed for google sheet api operations in gspread operations
            # https://docs.google.com/spreadsheets/d/1VXp8vOTvSqBH_zB1A9eIsaSIEVQslZTTljHsO5Mqfk0/edit#gid=0 link to google sheet

            # Initiating googlesheets service client
            self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            # Load credentials from the service account file
            self.creds = Credentials.from_service_account_info(credentials_file, scopes=self.scopes)
            # Authorize the client using the loaded credentials
            self.g_client = gspread.authorize(self.creds)
            # Open the workbook by its ID
            self.g_workbook = self.g_client.open_by_key(sheet_id)

            # Access the worksheet, worksheet at index 0 corresponds to the first sheet
            self.trading_worksheet = self.g_workbook.get_worksheet(0)
            # Check if the first row is empty
            if not self.trading_worksheet.row_values(1):
                # Define the column names
                column_names = [
                    'time',
                    'trade_order_id',
                    'address',
                    'symbol',
                    'is_long_short',
                    'trade_type',
                    'leads_price',
                    'price',
                    'weighted_score_ratio',
                    'leads_max_volume',
                    'leads_leverage',
                    'leads_transaction_quantity',
                    'leads_transaction_amount',
                    'our_leverage',
                    'our_transaction_quantity',
                    'our_transaction_amount',
                    'leads_total_hold',
                    'leads_total_investment',
                    'avg_leads_coin_price',
                    'our_total_hold',
                    'our_total_investment',
                    'avg_coin_price',
                    'total_hold_ratio',
                    'stop_loss_price',
                    'stop_loss_order_id',
                    'is_stop_loss_executed',
                    'is_liquidated',
                    'take_profit_price',
                    'take_profit_order_id',
                    'PNL',
                    'DEX',
                    'available_balance'
                ]

                # Insert column names into the first row
                self.trading_worksheet.append_row(column_names)

        except Exception as e:
            content = f"Error \"{e}\" happened while uploading open positions to google sheets.\nException: {traceback.format_exc()}"
            print(content)
            self.send_message("ALERT", content)



#---Others----------
    def get_current_time(self):
        india_timezone = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(india_timezone).strftime("%H:%M:%S %d %B %Y")
        return current_time

    # Function to generate HTML with the date and Google Sheet link
    def generate_html_with_date(self):
        # Get the current date
        current_time = self.get_current_time()
        current_date = ' '.join(current_time.split(' ')[1:4])  # Extracting date part
        
        html_content = f"""
        <html>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background: transparent;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background: transparent; padding: 0 10px;">
            <tr>
                <td style="text-align: center;">
                <a href="{google_sheet_url}" style="
                    display: inline-block; width: 100%; max-width: 600px; /* Full width but not exceeding 600px */
                    padding: 10px 20px; /* Increased padding for taller button */
                    font-size: 16px; font-weight: bold; color: #fff; background-color: #007bff; 
                    text-decoration: none; border: none; /* Remove border */
                    border-radius: 4px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    transition: background-color 0.3s ease;
                    text-align: center; /* Center text in the button */
                    height: auto; /* Allow button height to adjust automatically */
                    line-height: 1.2; /* Adjust line-height to better fit the increased height */
                    box-sizing: border-box; /* Include padding and border in element's width and height */
                    margin-bottom: 20px; /* Space below the button */
                "> 
                    Google Sheet Live
                </a>
                </td>
            </tr>
            <tr>
                <td style="height: 20px;"></td> <!-- Blank line for additional space -->
            </tr>
            </table>
        </body>
        </html>
        """
        return html_content

    # Gmail services
    def gmail_alerts_binance(self, new_row):

        try:
            message_trade =  f"{new_row['is_long_short'][0]} : {new_row['trade_type'][0]} : {new_row['symbol'][0]} : {new_row['DEX'][0]} at {new_row['time'][0]}"
            message = MIMEMultipart()  
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email)
            message["Subject"] = message_trade
    
            # Extract data from new_row dictionary
            time = new_row['time'][0]
            trade_order_id = new_row['trade_order_id'][0]
            address = new_row['address'][0]
            symbol = new_row['symbol'][0]
            is_long_short = new_row['is_long_short'][0]
            trade_type = new_row['trade_type'][0]
            leads_price = new_row['leads_price'][0]  
            price = new_row['price'][0]
            weighted_score_ratio = new_row['weighted_score_ratio'][0]
            leads_max_volume = new_row['leads_max_volume'][0]
            leads_leverage = new_row['leads_leverage'][0]
            leads_transaction_quantity = new_row['leads_transaction_quantity'][0]
            leads_transaction_amount = new_row['leads_transaction_amount'][0]
            our_leverage = new_row['our_leverage'][0]
            our_transaction_quantity = new_row['our_transaction_quantity'][0]
            our_transaction_amount = new_row['our_transaction_amount'][0]
            leads_total_hold = new_row['leads_total_hold'][0]
            leads_total_investment = new_row['leads_total_investment'][0] 
            avg_leads_coin_price = new_row['avg_leads_coin_price'][0]
            our_total_hold = new_row['our_total_hold'][0]
            our_total_investment = new_row['our_total_investment'][0] 
            avg_coin_price = new_row['avg_coin_price'][0]
            total_hold_ratio = new_row['total_hold_ratio'][0]
            stop_loss_price = new_row['stop_loss_price'][0]
            stop_loss_order_id = new_row['stop_loss_order_id'][0]
            is_stop_loss_executed = new_row['is_stop_loss_executed'][0]
            is_liquidated = new_row['is_liquidated'][0]
            take_profit_price = new_row['take_profit_price'][0]
            take_profit_order_id = new_row['take_profit_order_id'][0]
            PNL = new_row['PNL'][0]
            DEX = new_row['DEX'][0]
            available_balance = new_row['available_balance'][0]

            # Format data into rows for the table
            rows = [
                ["Time", str(time)],
                ["Trade Order ID", str(trade_order_id)],
                ["Leads Address", str(address)],
                ["Symbol", str(symbol)],
                ["Long/Short", str(is_long_short)],
                ["Trade Type", str(trade_type)],  # Updated to match `new_row`
                ["Leads Price", str(leads_price) + " USDT"],  # Added column
                ["Price", str(price) + " USDT"],
                ["Weighted Score Ratio", str(weighted_score_ratio)],  # Added column
                ["Leads Max Volume", str(leads_max_volume) + " USDT"],  # Added column
                ["Leads Leverage", str(leads_leverage)],
                ["Leads Transaction Quantity", str(leads_transaction_quantity) + ' ' + str(symbol)],
                ["Leads Transaction Amount", str(leads_transaction_amount) + " USDT"],
                ["Our Leverage", str(our_leverage)],
                ["Our Transaction Quantity", str(our_transaction_quantity) + ' ' + str(symbol)],
                ["Our Transaction Amount", str(our_transaction_amount) + " USDT"],
                ["Leads Total Hold", str(leads_total_hold) + ' ' + str(symbol)],
                ["Leads Total Investment", str(leads_total_investment) + " USDT"],  # Added column
                ["Average Leads Coin Price", str(avg_leads_coin_price) + " USDT"],  # Added column
                ["Our Total Hold", str(our_total_hold) + ' ' + str(symbol)],
                ["Our Total Investment", str(our_total_investment) + " USDT"],  # Added column
                ["Average Coin Price", str(avg_coin_price) + " USDT"],
                ["Total Hold Ratio", str(total_hold_ratio)],
                ["Stop Loss Price", str(stop_loss_price) + " USDT"],
                ["Stop Loss Order ID", str(stop_loss_order_id)],
                ["Is Stop Loss Executed", str(is_stop_loss_executed)],
                ["Is Liquidated", str(is_liquidated)],
                ["Take Profit Price", str(take_profit_price) + " USDT"],
                ["Take Profit Order ID", str(take_profit_order_id)],
                ["PNL", str(PNL) + " USDT"],
                ["DEX", str(DEX)],  # Updated to match `new_row`
                ["available_balance", str(available_balance)],
            ]


            # Create the table
            table_html = self.create_table_html(rows)

            message.attach(MIMEText(self.generate_html_with_date(), "html"))

            # Attach table as HTML to the email
            message.attach(MIMEText(table_html, "html"))

            email_server = smtplib.SMTP("smtp.gmail.com", 587)
            email_server.starttls()
            email_server.login(sender_email, email_password)
            email_server.sendmail(sender_email, receiver_email, message.as_string())

        except Exception as e:
            print(f"Error occurred while constructing or sending the email.\nException: {traceback.format_exc()}")

    # Function to create a table as HTML from rows
    def create_table_html(self, rows):
        """Create a striped table as HTML."""
        table_html = "<table style='width: 70%; border-collapse: collapse;'>"
        for i, row in enumerate(rows):
            if i % 2 == 0:
                table_html += "<tr style='background-color: #f2f2f2;'>"
            else:
                table_html += "<tr style='background-color: #ffffff;'>"
            table_html += f"<td style='width: 50%; padding: 8px; color: black; font-weight: bold;'>{row[0]}</td>"
            table_html += "<td style='padding: 8px; color: black;'>:</td>"
            table_html += f"<td style='width: 50%; padding: 8px; color: black;'>{row[1]}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        return table_html

    # Emailer
    def send_message(self, message_type, content):

        email_server = smtplib.SMTP("smtp.gmail.com", 587)
        email_server.starttls()
        email_server.login(sender_email, email_password)

        if message_type == "ALERT":
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = ", ".join(receiver_email)
                message["Subject"] = f"ALERT {DEX}: Attention required in binance server at {self.get_current_time()}"
                message.attach(MIMEText(self.generate_html_with_date(), "html"))
                body = (f"{content}")
                message.attach(MIMEText(body, "plain"))         

                email_server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                print(f"Error occurred while sending the ALERT message.\nException: {traceback.format_exc()}")

                
        elif message_type == "UPDATE":
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = ", ".join(receiver_email)
                message["Subject"] = "24 HRS SUMMARY: Liquidated trade got closed."
                message.attach(MIMEText(self.generate_html_with_date(), "html"))
                body = (f"{content}")
                message.attach(MIMEText(body, "plain"))         

                email_server.sendmail(sender_email, receiver_email, message.as_string())

            except Exception as e:
                print(f"Error occurred while sending the UPDATE message.\nException: {traceback.format_exc()}")
                
        elif message_type == "CRASHED":
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = ", ".join(receiver_email)
                message["Subject"] = f"CRASHED {DEX}: Program stopped due to outside error at {self.get_current_time()}"
                message.attach(MIMEText(self.generate_html_with_date(), "html"))
                body = (f"{content}")
                message.attach(MIMEText(body, "plain"))         

                email_server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                print(f"Error occurred while sending the CRASHED message.\nException: {traceback.format_exc()}")
                
        else:
            print("Invalid message type, try sending 'ALERT', 'UPDATE' or 'CRASHED'")



#---Sheets and DF Management----------
    def clear_google_sheet(self, sheet_number, password):
        
        for sheet in sheet_number:      
            if (sheet in [0, 1, 2, 3, 4, 5, 6]) & (password == "yesdeleteit"):

                # Access the worksheet, worksheet at index 0 corresponds to the first sheet
                worksheet = self.g_workbook.get_worksheet(sheet)
                
                # Clear the contents of the worksheet
                worksheet.clear()
                
                print(f"Cleared Successfully sheet {sheet}")
                
            else:
                print("Wrong Sheet Number or Password, Kindly try : 0, 1 or 2")

    # Function to insert trading data to google sheet
    def insert_row_to_google_sheet_traders(self, data):
        try:
            # Define the values to be inserted as a new row
            values = [
                data['time'][0],
                data['trade_order_id'][0],
                data['address'][0],
                data['symbol'][0],
                data['is_long_short'][0],
                data['trade_type'][0],
                data['leads_price'][0],
                data['price'][0],
                data['weighted_score_ratio'][0],
                data['leads_max_volume'][0],
                data['leads_leverage'][0],
                data['leads_transaction_quantity'][0],
                data['leads_transaction_amount'][0],
                data['our_leverage'][0],
                data['our_transaction_quantity'][0],
                data['our_transaction_amount'][0],
                data['leads_total_hold'][0],
                data['leads_total_investment'][0],
                data['avg_leads_coin_price'][0],
                data['our_total_hold'][0],
                data['our_total_investment'][0],
                data['avg_coin_price'][0],
                data['total_hold_ratio'][0],
                data['stop_loss_price'][0],
                data['stop_loss_order_id'][0],
                data['is_stop_loss_executed'][0],
                data['is_liquidated'][0],
                data['take_profit_price'][0],
                data['take_profit_order_id'][0],
                data['PNL'][0],
                data['DEX'][0],
                data['available_balance'][0]
            ]

            # Append the row to the worksheet
            self.trading_worksheet.append_row(values)

            print("Row inserted successfully into G-Sheet:TRADING.")

        except Exception as e:
            content = f"Error \"{e}\" happened while appending new trade to google sheets.\nException: {traceback.format_exc()}"
            print(content)
            self.send_message("ALERT", content)

    # trading_data_df is defined globally
    def add_to_trading_data_df(self, time, trade_order_id, address, symbol, is_long_short, trade_type, leads_price, price, weighted_score_ratio, leads_max_volume, leads_leverage, leads_transaction_quantity,
                        leads_transaction_amount, our_leverage, our_transaction_quantity, our_transaction_amount, leads_total_hold, leads_total_investment, avg_leads_coin_price,
                        our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_price, stop_loss_order_id,
                        is_stop_loss_executed,is_liquidated, take_profit_price, take_profit_order_id, PNL):

        global trading_data_df 

        def side_convention(is_long_short, trade_type):
            if is_long_short == "LONG":
                if trade_type == "BUY":
                    return "OPEN"
                elif trade_type == "SELL": ### it shoudl be SELL
                    return "CLOSE"
                elif trade_type == "BANNED":
                    return "BANNED"
                elif trade_type == "LIQUIDATED":
                    return "LIQUIDATED"
                else:
                    return None
            elif is_long_short == "SHORT":
                if trade_type == "BUY":
                    return "CLOSE"
                elif trade_type == "SELL":
                    return "OPEN"
                elif trade_type == "BANNED":
                    return "BANNED"
                elif trade_type == "LIQUIDATED":
                    return "LIQUIDATED"
                else:
                    return None
            else:
                return None  # Handle invalid input

        new_row = {
            'time': [time],
            'trade_order_id': [trade_order_id],
            'address': [address],
            'symbol': [symbol],
            'is_long_short': [is_long_short],
            'trade_type': [side_convention(is_long_short, trade_type)],
            'leads_price': [leads_price],
            'price': [price],
            'weighted_score_ratio': [weighted_score_ratio],
            'leads_max_volume': [leads_max_volume],
            'leads_leverage': [leads_leverage],
            'leads_transaction_quantity': [leads_transaction_quantity],
            'leads_transaction_amount': [leads_transaction_amount],
            'our_leverage': [our_leverage],
            'our_transaction_quantity': [our_transaction_quantity],
            'our_transaction_amount': [our_transaction_amount],
            'leads_total_hold': [leads_total_hold],
            'leads_total_investment': [leads_total_investment],
            'avg_leads_coin_price': [avg_leads_coin_price],
            'our_total_hold': [our_total_hold],
            'our_total_investment': [our_total_investment],
            'avg_coin_price': [avg_coin_price],
            'total_hold_ratio': [total_hold_ratio],
            'stop_loss_price': [stop_loss_price],
            'stop_loss_order_id': [stop_loss_order_id],
            'is_stop_loss_executed': [is_stop_loss_executed],
            'is_liquidated': [is_liquidated],
            'take_profit_price': [take_profit_price],
            'take_profit_order_id': [take_profit_order_id],
            'PNL': [PNL],
            'DEX': dex_name,
            'available_balance': [self.return_available_balance()],
        }
        
        # To insert trading data to google sheet
        self.insert_row_to_google_sheet_traders(new_row)
        
        self.gmail_alerts_binance(new_row)
        
        new_row_df = pd.DataFrame(new_row)

        trading_data_df = pd.concat([trading_data_df, new_row_df], ignore_index=True)

        # Extract the header and the row from the dictionary
        header = new_row_df.keys()
        row = [value[0] for value in new_row.values()]

        # Check if the file exists
        file_exists = os.path.isfile(trading_data_df_path)

        # Open the file in append mode
        with open(trading_data_df_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # If the file does not exist, write the header
            if not file_exists:
                writer.writerow(header)
            # Write the new row
            writer.writerow(row)

        print(f"New row added to {trading_data_df_path}")
        

    def get_and_upload_open_positions_to_sheets(self):
        try:
            # Access the specific worksheet
            self.positions_worksheet = self.g_workbook.get_worksheet(dex_to_open_positions_dictionary[DEX[0]]) # Index 0 corresponds to the 1st sheet

            # Define the column names
            column_names = [
                'time',
                'trade_order_id',
                'address',
                'symbol',
                'is_long_short',
                'last_trade_type',
                'leads_total_hold',
                'leads_total_investment',
                'leads_leverage',
                'avg_leads_coin_price',
                'our_total_hold',
                'our_total_investment',
                'our_leverage',
                'avg_coin_price',
                'total_hold_ratio',
                'stop_loss_price',
                'stop_loss_order_id',
                'take_profit_price',
                'take_profit_order_id',
                'DEX'
            ]
            
            # Prepare the list of values to write
            values = [column_names]  # Add column names as the first row

            # Group by address, symbol, and is_long_short
            grouped_df = trading_data_df.groupby(['address', 'symbol', 'is_long_short'])

            # Iterate over each group
            for name, group in grouped_df:
                # Pass data to the check_old_stop_loss function (address, symbol, position)
                trader_position_df = self.get_position_of_trader_from_trading_data_df(trading_data_df, name[0], name[1], name[2])
                
                if not trader_position_df.empty:
                    data = trader_position_df.iloc[-1]

                    if data['our_total_hold'] != 0:
                        row = [
                            str(data['time']),
                            data['trade_order_id'],
                            data['address'],
                            data['symbol'],
                            data['is_long_short'],
                            data['trade_type'],
                            data['leads_total_hold'],
                            data['leads_total_investment'],
                            data['leads_leverage'],
                            data['avg_leads_coin_price'],
                            data['our_total_hold'],
                            data['our_total_investment'],
                            data['our_leverage'],
                            data['avg_coin_price'],
                            data['total_hold_ratio'],
                            data['stop_loss_price'],
                            data['stop_loss_order_id'],
                            data['take_profit_price'],
                            data['take_profit_order_id'],
                            data['DEX']
                        ]
                        values.append(row)  # Add each row of data

            # Clear all rows
            self.positions_worksheet.clear()  # This clears all content in the sheet

            # Write new data starting from cell A1
            self.positions_worksheet.update('A1', values)

        except Exception as e:
            content = f"Error \"{e}\" happened while uploading open positions to google sheets.\nException: {traceback.format_exc()}"
            print(content)
            self.send_message("ALERT", content)

    def get_summary_and_send_email(self):

        try:
            global last_email_sent_date

            message_trade =  f"{dex_name}: SUMMARY 24 HRS ({summary_sending_hour}:00 yesterday - {summary_sending_hour}:00 today)"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email)
            message["Subject"] = message_trade

            # Convert the 'time' column to datetime format
            trading_data_df['time'] = pd.to_datetime(trading_data_df['time'], format="%H:%M:%S %d %B %Y")

            # Get the current time in IST
            now = self.get_current_time()

            # Convert the 'now' time string to a datetime object
            now = datetime.strptime(now, "%H:%M:%S %d %B %Y")

            # Calculate the start time (summary_sending_hour PM of the previous day)
            previous_day = (now - timedelta(days=1)).replace(hour=summary_sending_hour, minute=0, second=0, microsecond=0)

            # Calculate the end time (summary_sending_hour PM today)
            today = now.replace(hour=summary_sending_hour, minute=0, second=0, microsecond=0)

            # Filter rows from summary_sending_hour PM of the previous day to summary_sending_hour PM today
            last_24_hours = trading_data_df[(trading_data_df['time'] >= previous_day) & (trading_data_df['time'] <= today)]

            # Group by 'address', 'symbol', 'is_long_short' and count the number of unique groups
            unique_group_count = last_24_hours.groupby(['address', 'symbol', 'is_long_short']).ngroups

            # Count the number of rows within the last 24 hours
            row_count = len(last_24_hours)

            # Sum the PNL column within the last 24 hours
            pnl_sum = last_24_hours['PNL'].sum()

            # Count occurrences in 'tradetype' column
            close_count = last_24_hours['trade_type'].value_counts().get('CLOSE', 0)
            open_count = last_24_hours['trade_type'].value_counts().get('OPEN', 0)
            liquidated_count = last_24_hours['trade_type'].value_counts().get('LIQUIDATED', 0)
            banned_count = last_24_hours['trade_type'].value_counts().get('BANNED', 0)

            rows = [
                    ["Time", self.get_current_time()],
                    ["Total POSITIONS", unique_group_count],
                    ["Total Trades", row_count],
                    ["Total OPEN Trades", open_count],
                    ["Total CLOSE Trades", close_count],
                    ["Total LIQUIDATED Trades", liquidated_count],
                    ["Total BANNED Trades", banned_count],
                    ["Total PNL", pnl_sum],
                    ["DEX", dex_name],]

            table_html = self.create_table_html(rows)

            # Attach table as HTML to the email
            message.attach(MIMEText(table_html, "html"))

            # Add the link below the table
            link_text = "\n\nCheck Google Sheet for live server trading updates here:"
            link_url = google_sheet_url
            link_html = f"<p><a href='{link_url}'>{link_text}</a></p>"
            message.attach(MIMEText(link_html, "html"))

            email_server = smtplib.SMTP("smtp.gmail.com", 587)
            email_server.starttls()
            email_server.login(sender_email, email_password)
            email_server.sendmail(sender_email, receiver_email, message.as_string())

            last_email_sent_date = now.date()  # Update the date of the last email sent

        except Exception as e:
            print(f"Error occurred while constructing or sending the email. \nException: {traceback.format_exc()}")



    #---Others----------
    # Get the whole position data
    def get_position_of_trader_from_trading_data_df(self, trading_data_df, address_to_search, symbol_to_search, is_long_short_to_search):
        trader_position_df = trading_data_df[
            (trading_data_df['address'] == address_to_search) &
            (trading_data_df['symbol'] == symbol_to_search) &
            (trading_data_df['is_long_short'] == is_long_short_to_search)
        ]
        return trader_position_df

    # Get last row data of the position
    def get_last_row_of_trader_in_trading_data_df(self, trading_data_df, address_to_search, symbol_to_search, is_long_short_to_search):

        trader_position_df = self.get_position_of_trader_from_trading_data_df(trading_data_df, address_to_search, symbol_to_search, is_long_short_to_search)
        
        if not trader_position_df.empty:
            last_row_trader_personal_df = trader_position_df.iloc[-1]
            
            #print("Last row present.")

            if last_row_trader_personal_df['our_total_hold'] == 0 or last_row_trader_personal_df['trade_type'] == 'BANNED':
                was_last_row_present = True
                return 0, 0, 0, 0, 0, 0, 0, 0, None, 0, was_last_row_present
            else:
                leads_total_hold = float(last_row_trader_personal_df['leads_total_hold'])
                leads_total_investment = float(last_row_trader_personal_df['leads_total_investment'])
                avg_leads_coin_price = float(last_row_trader_personal_df['avg_leads_coin_price'])
                leads_leverage = float(last_row_trader_personal_df['leads_leverage'])

                our_total_hold = float(last_row_trader_personal_df['our_total_hold'])
                our_total_investment = float(last_row_trader_personal_df['our_total_investment'])
                avg_coin_price = float(last_row_trader_personal_df['avg_coin_price'])

                total_hold_ratio = float(last_row_trader_personal_df['total_hold_ratio'])
                stop_loss_order_id = last_row_trader_personal_df['stop_loss_order_id']
                stop_loss_price = float(last_row_trader_personal_df['stop_loss_price'])

                was_last_row_present = True

                return leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present
            
        else:
            was_last_row_present = False
            return 0, 0, 0, 0, 0, 0, 0, 0, None, 0, was_last_row_present
    
    #Fetching open_side value i.e buy or sell
    def sideAndCounterSideForBinance(self, position_side):
        open_side = "BUY" if position_side == "LONG" else "SELL"
        close_side = "SELL" if position_side == "LONG" else "BUY" # Used for SL and TP
        return open_side, close_side
    

    # Checking old stoploss status and inputing new row immedeately if stoploss of the position is executed
    def check_old_stop_loss(self, client, trading_data_df, address, symbol,  position_side):
        
        #Getting Data from leads last row in this position
        leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)

        #Inititalizing variables
        stop_PNL = 0
        PNL = 0

        try:
            if stop_loss_order_id is not None:
                market_order_status = client.futures_get_order(symbol=symbol, orderId=stop_loss_order_id)
                if market_order_status['status'] == 'FILLED':
                    print("\n\n")
                    weighted_score_ratio = traders_list['Ranking_Score'][traders_list['account'] == address].iloc[0] / traders_list['Ranking_Score'].sum()
                    leads_max_volume = traders_list['max_volume'][traders_list['account'] == address].iloc[0]

                    print(f"\n\nSTOP LOSS order filled for [address: {address}, symbol: {symbol}, position_side: {position_side}]")
                    new_leads_total_hold = 0
                    new_our_total_hold = 0
                    new_avg_coin_price = 0
                    new_total_hold_ratio= 0
                    #Fetching open_side value i.e buy or sell
                    open_side, close_side = self.sideAndCounterSideForBinance(position_side)
                    #Now using the details came from the filled order status
                    marketOrderQty, marketOrderPrice = float(market_order_status['executedQty']), float(market_order_status['avgPrice'])
                    new_our_transaction_amount = marketOrderQty * marketOrderPrice

                    # PNL Calculation
                    y = 1 if position_side == "LONG" else -1
                    stop_PNL = marketOrderQty * (marketOrderPrice - avg_coin_price) * (y)      

                    print(f"address: {address}\n"
                            f"symbol: {symbol}\n"
                            f"position_side: {position_side}\n"
                            f"transaction_quantity: {marketOrderQty}\n"
                            f"transaction_amount: {new_our_transaction_amount}\n"
                            f"stop_PNL: {stop_PNL}")
                    
                    # Append new row in the Trading_df with all updated details details.
                    self.add_to_trading_data_df(
                        time=self.get_current_time(), 
                        trade_order_id=stop_loss_order_id,
                        address=address, 
                        symbol=symbol, 
                        is_long_short=position_side,
                        trade_type=close_side,
                        leads_price=0,
                        price=marketOrderPrice,
                        weighted_score_ratio=weighted_score_ratio,
                        leads_max_volume=leads_max_volume,
                        leads_leverage=leads_leverage,
                        leads_transaction_quantity=0,
                        leads_transaction_amount=0,
                        our_leverage=our_leverage,
                        our_transaction_quantity=marketOrderQty,
                        our_transaction_amount=new_our_transaction_amount,
                        leads_total_hold=new_leads_total_hold, 
                        leads_total_investment=leads_total_investment,
                        avg_leads_coin_price=avg_leads_coin_price,
                        our_total_hold=0,
                        our_total_investment=our_total_investment,
                        avg_coin_price=new_avg_coin_price,
                        total_hold_ratio=new_total_hold_ratio,
                        stop_loss_price=0,
                        stop_loss_order_id=None,
                        is_stop_loss_executed=True,
                        is_liquidated=False,
                        take_profit_price=0,
                        take_profit_order_id=None,
                        PNL=stop_PNL
                    )
                    print("\n\n")

                    return True
                    
                elif market_order_status['status'] == 'EXPIRED':
                    print("\n\n")
                    Alert_note = f"Panic, old stoploss orderId status is 'EXPIRED' (Now banning the position for {ban_time_hours}hrs). stop_loss_order_id:{stop_loss_order_id} (Please close the position manually)"
                    #Witing content for email
                    print(Alert_note)
                    content = f"{Alert_note},\n\naddress: {address},\nsymbol:{symbol},\nis_long_short:{position_side},\nstop_loss_order_id:{stop_loss_order_id},\ntime: {self.get_current_time()},\nour_total_hold:{our_total_hold},\navg_coin_price:{avg_coin_price}\n"
                    self.send_message("ALERT", content)
                    self.add_to_ban_list(address, symbol, position_side, stop_loss_order_id, 0, 0, our_total_hold, avg_coin_price) # Added to "ban_positions_info_list"
                    print("\n\n")
                    return False
                
                elif market_order_status['status'] == 'CANCELED':
                    print("\n\n")
                    Alert_note = f"Panic, old stoploss orderId status is already 'CANCELED' (Now banning the position for {ban_time_hours}hrs). stop_loss_order_id:{stop_loss_order_id} (Please close the position manually)"
                    #Witing content for email
                    print(Alert_note)
                    content = f"{Alert_note},\n\naddress: {address},\nsymbol:{symbol},\nis_long_short:{position_side},\nstop_loss_order_id:{stop_loss_order_id},\ntime: {self.get_current_time()},\nour_total_hold:{our_total_hold},\navg_coin_price:{avg_coin_price}\n"
                    self.send_message("ALERT", content)
                    self.add_to_ban_list(address, symbol, position_side, stop_loss_order_id, 0, 0, our_total_hold, avg_coin_price) # Added to "ban_positions_info_list"
                    print("\n\n")
                    return False
                
                else:
                    # print("Old stop-loss order was not filled")
                    return True
                
            else:
                # print("Old stop-loss order was not present in df")
                return True

        except Exception as e:
            Alert_note = f"\n\nException happened while checking old stop_loss through check_old_stop_loss function.\n\naddress: {address}, symbol: {symbol}, position_side: {position_side}"
            print(Alert_note)
            content = f"{Alert_note},\nstop_loss_order_id:{stop_loss_order_id},\ntime: {self.get_current_time()},\nour_total_hold:{our_total_hold},\navg_coin_price:{avg_coin_price}\nException: {traceback.format_exc()}"
            self.send_message("ALERT", content)
            print("\n\n")
            return False

    # To check last stop loss order id status
    def check_last_stop_loss_order_id_status(self, client, trading_data_df):
        # Group by address, symbol, and is_long_short
        grouped_df = trading_data_df.groupby(['address', 'symbol', 'is_long_short'])
        # Iterate over each group
        for name, group in grouped_df:
            # Pass data to the check_old_stop_loss function
            self.check_old_stop_loss(client, trading_data_df, name[0], name[1], name[2])

    def return_available_balance(self):
        # Get account information
        try:
            account_info = client.futures_account()
            available_balance = round(float(account_info['availableBalance']), 2)
            available_balance = str(available_balance)
            return available_balance
        except Exception as e:
            print(f"Error occurred during available balance fetching from Binance for uploading to available_balance column in df.\nException: {traceback.format_exc()}")
            return None

    # Round up to ceiling
    def round_up_to_ceil_with_precision(self, min_qnt, precision):
        # Calculate the raw quantity
        raw_quantity = min_qnt
        # Calculate the factor for the given precision
        precision_factor = 10 ** precision
        # Apply ceiling to round up and then adjust for precision
        rounded_quantity = math.ceil(raw_quantity * precision_factor) / precision_factor
        return rounded_quantity

    # Round off to floor
    def floor_decimal(self, value, precision):
        # Convert the value to a Decimal
        decimal_value = Decimal(str(value))
        # Create a string for the desired precision (e.g., '1.00' for 2 decimal places)
        precision_str = '1.' + '0' * precision
        # Floor the decimal value to the specified precision
        floored_value = decimal_value.quantize(Decimal(precision_str), rounding=ROUND_FLOOR)
        return floored_value




#---Opening----------
    def ultimate_openTrade(self, client, traders_list, address, coin, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage):
        
        print("Time:", self.get_current_time())
        symbol = coin + "USDT"
        current_trade_orderId = None

        # Opening Trades
        def openTrade(client, traders_list, address, symbol, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage):
            
            PNL = 0
            stop_PNL = 0
            nonlocal current_trade_orderId
            # Fetching coin price from Binance
            #---------------------------
            try:
                exchange_information = client.futures_exchange_info()
                symbol_info = next((s for s in exchange_information['symbols'] if s['symbol'] == symbol), None)  # corrected line
                if symbol_info:
                    # Precision for the quantity
                    quantity_precision = next((f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'MARKET_LOT_SIZE'), None)
                    # Precision for the price in dollar
                    price_precision =  next((f['tickSize'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'), None)
                    # Minimum notional value (minimum dollars)
                    min_notional = float(next((f['notional'] for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None))
                    # Get integer value of precision
                    quantity_precision_integer = 0 if '.' not in str(quantity_precision) else len(
                        str(quantity_precision).split('.')[1].rstrip('0')) if str(quantity_precision) else None
                    price_precision_integer = 0 if '.' not in str(price_precision) else len(
                        str(price_precision).split('.')[1].rstrip('0')) if str(price_precision) else None
                    quantity_precision_integer = int(quantity_precision_integer)
                    price_precision_integer = int(price_precision_integer)

                    #Printing lead's qunatity and amount
                    transaction_amount = float(self.floor_decimal(transaction_amount, price_precision_integer))
                    transaction_quantity = float(self.floor_decimal(transaction_quantity, quantity_precision_integer))
                    print(f"Lead's transaction amaount: ", transaction_amount)
                    print(f"Lead's transaction quantity: ", transaction_quantity)

                    if transaction_amount == 0 or transaction_quantity == 0:
                        print("Lead's Quantites are zero when rounded. Rejecting trade.")
                        return True, None
                    
                    print(f"min_notional: {min_notional}")
                    print(f"quantity_precision_integer: {quantity_precision_integer}")
                    print(f"price_precision_integer: {price_precision_integer}")
                    # Getting price on binance
                    try:
                        ticker = client.futures_symbol_ticker(symbol=symbol)
                        price_on_bin = float(ticker['price'])
                        print(f"Current market price of {symbol}: {price_on_bin}")
                    except Exception as e:
                        print(f"Error occurred during coin {symbol} price fetching from Binance.\nxception: {traceback.format_exc()}")
                        return 1001, f"Error occurred during coin {symbol} price fetching from Binance.\nException: {e}"
                                    
                    # Minimum quantity to buy
                    minimum_quantity = min_notional/price_on_bin  * 1.02
                    min_qty = self.round_up_to_ceil_with_precision(minimum_quantity, quantity_precision_integer)
                else:
                    print(f"Symbol {symbol} not found in exchange information.")
                    return 1002, f"Symbol {symbol} not found in exchange information."  # Error code and description , above we used 1005 and its same error check
            except Exception as e:
                print(f"Error occurred during coin info fetching from Binance or min_qty calculation.\nException:{traceback.format_exc()}")
                return 1003, f"Error occurred during coin info fetching from Binance or min_qty calculation.\nException: {e}"


            # Price difference checking
            price_ratio = (asset_price / price_on_bin)
            if not (1 + price_difference_ratio) >= price_ratio >= (1 - price_difference_ratio):
                print(f"Coin {symbol} prices differ by {price_difference_ratio * 100}%, so we are not taking the trade.")
                return 1004, f"Coin {symbol} prices differ by {price_difference_ratio * 100}%, so we are not taking the trade."


            # Setting leverage on binance for the coin
            try:
                response = client.futures_change_leverage(symbol=symbol, leverage=our_leverage)
                print(f"Leverage set to {our_leverage} for {symbol}. Response:{response}")
            except Exception as e:
                print(f"Error occurred during leverage setting on Binance.\nException: {traceback.format_exc()}")
                return 1005, f"Error occurred during leverage setting on Binance.\nException: {e}"


            # Get account information
            try:
                account_info = client.futures_account()
                available_balance = float(account_info['availableBalance'])
                print(f"**Available balance: {available_balance}")
            except Exception as e:
                print(f"Error occurred during available balance fetching from Binance.\nException: {traceback.format_exc()}")
                return 1006, f"Error occurred during available balance fetching from Binance.\nException: {e}"


            # threshold_balance
            if available_balance < threshold_balance:  # Checking minimum
                print(f"Available balance is less than Threshold_Balance:{threshold_balance}, so rejecting the open trade.")
                return 1007, f"Available balance is less than Threshold_Balance:{threshold_balance}, so rejecting the open trade."

            weighted_score_ratio = traders_list['Ranking_Score'][traders_list['account'] == address].iloc[0] / traders_list['Ranking_Score'].sum()
            leads_max_volume = traders_list['max_volume'][traders_list['account'] == address].iloc[0]
            
            print(f"weighted_score_ratio: {weighted_score_ratio}")
            print(f"leads_max_volume: {leads_max_volume}")

            #Calculating volume ratio in case volume ratio goes above 1
            if transaction_amount > leads_max_volume:
                volume_ratio = 1
            else:
                volume_ratio = (transaction_amount / leads_max_volume)
            print(f"volume_ratio: {volume_ratio}")


            # Collateral to invest main
            collateral_to_invest = (available_balance) * (weighted_score_ratio) * (volume_ratio) * (investement_risk_factor)

            
            print("min_qty :",min_qty)
            print("weighted_score_ratio :",weighted_score_ratio)
            print("volume_ratio :",volume_ratio)
            print("collateral_to_invest :",collateral_to_invest)
            
            
            # Calculating quantity to buy with precision
            total_usd_investment = (our_leverage * collateral_to_invest)
            print("total_usd_investment: ",total_usd_investment)
            ideal_quantity = (total_usd_investment / price_on_bin)
            print("ideal_quantity: ",ideal_quantity)
            if ideal_quantity < min_qty:
                # if (ideal_quantity / min_qty) > 0.60:
                print(f"Buying :{min_qty} allowed as (ideal_quantity:{ideal_quantity} < min_qty:{min_qty}).")
                quantity = min_qty 
                # else:
                    # print(f"Cannot buy quantity (={ideal_quantity}) of coin less than min_qty:{min_qty} allowed.")
                    # return 1008, f"Cannot buy quantity (={ideal_quantity}) of coin less than min_qty:{min_qty} allowed."
            else:
                quantity = self.round_up_to_ceil_with_precision(ideal_quantity, quantity_precision_integer)       # check
                print("quantity :", quantity)
            

            # Rechecking old stop loss and filling df if executed                                            # what if no stop loss exist check new
            response_from_old_stop_loss = self.check_old_stop_loss(client, trading_data_df, address, symbol, position_side) 
            print('Trying to check old stop loss status before moving on.')
            if response_from_old_stop_loss == False:
                print(f"Exception happened while check_old_stop_loss.")
                return False, f"Exception happened while check_old_stop_loss."


            # Now check the last row through below function & fetch last row values from Trading_df about the current position
            leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)


            # ------------------------- TAKING TRADE:
            # Getting side for trades
            open_side, close_side = self.sideAndCounterSideForBinance(position_side)

            # Try to palce order for upto number_of_try times
            for i in range(number_of_try):
                try:
                    market_order = client.futures_create_order(symbol=symbol, positionSide=position_side, side = open_side, type=client.FUTURE_ORDER_TYPE_MARKET, quantity=quantity)

                    market_orderId = str(market_order['orderId']) # Assigning orderid in string format.

                    current_trade_orderId = market_orderId

                    print("Market open trade order placed successfully. market_orderId: ",market_orderId)
                    break

                except Exception as e: #Error when 3rd try is not successful
                    print("Error placing order:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying placing market order in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while placing market open trade order.\nException: {traceback.format_exc()}")
                        return 1009, f"Error occurred while placing market open trade order.\nException: {e}"
                    
            time.sleep(retry_time)        
            # Trying to check market open trade order status n number of times.
            print("Checking market open trade order status if FILLED or NOT.")
            for i in range(number_of_try):
                try:
                    order_status = client.futures_get_order(
                        symbol=symbol,
                        orderId= market_orderId
                        )

                    if order_status['status'] == "FILLED":       # check new , earlier orderStatus SUCCESS was written, 'status': 'FILLED', or 'NEW'
                        print(f"Market open order status is FILLED, orderId: {order_status['orderId']}")
                        break
                    else:
                        if i <= (number_of_try - 2):
                            print(f"Market open order status is NOT FILLED. orderId: {order_status['orderId']}")
                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Market open order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED).")
                            return 1010, f"Market open order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED)."
                            
                except Exception as e: #Error when 3rd try is not successful
                    print("Error checking order status:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while checking status of market open trade order.\nException: {traceback.format_exc()}")
                        return 1011, f"Error occurred while checking status of market open trade order.\nException: {e}"

            marketOrderQty, marketOrderPrice = float(order_status['executedQty']), float(order_status['avgPrice'])
            new_our_transaction_amount = marketOrderQty * marketOrderPrice
            print("marketOrderQty: ", marketOrderQty)
            print("marketOrderPrice: ", marketOrderPrice)
            
            # Calculating new total holds & avg coin price
            new_leads_total_hold = round((transaction_quantity + leads_total_hold), quantity_precision_integer)   # coins
            new_leads_total_investment = (transaction_amount + leads_total_investment)
            new_avg_leads_coin_price = (new_leads_total_investment) / (new_leads_total_hold) 
            new_our_total_hold = round((marketOrderQty + our_total_hold), quantity_precision_integer)             # coins
            new_our_total_investment = (new_our_transaction_amount) + (our_total_investment)
            new_avg_coin_price = ((new_our_transaction_amount) + (our_total_investment)) / (new_our_total_hold)
            new_total_hold_ratio = (new_our_total_hold / new_leads_total_hold)

            print(f"new_leads_total_hold: {new_leads_total_hold}")
            print(f"new_leads_total_investment: {new_leads_total_investment}")
            print(f"new_avg_leads_coin_price: {new_avg_leads_coin_price}")
            print(f"new_our_total_hold: {new_our_total_hold}")
            print(f"new_our_total_investment: {new_our_total_investment}")
            print(f"new_avg_coin_price: {new_avg_coin_price}")
            print(f"new_total_hold_ratio: {new_total_hold_ratio}")

            # ------------ Resetting Stoploss
            # Try to cancel_older_stoploss for upto number_of_try times
            if stop_loss_order_id is not None:
                print(f"Old stoploss orderId: {stop_loss_order_id}")
                print('Trying to cancel old stop loss')
                for i in range(number_of_try):  
                    try:
                        cancel_older_stoploss = client.futures_cancel_order(symbol=symbol, orderId=stop_loss_order_id)

                        canceled_order_orderId = str(cancel_older_stoploss['orderId']) # Assigning orderid in string format.
                        print("Older stoploss cancelation order placed successfully.")
                        break

                    except Exception as e: #Error when 3rd try is not successful
                        print("Error canceling older stoploss order:", e)
                        if i <= (number_of_try - 2): 
                            print(f"Retrying cancel_older_stoploss in {retry_time} seconds...(try no: {i}/{number_of_try})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Exception happened while canceling old stop_loss.\nException: {traceback.format_exc()}")
                            return 1011, f"Exception happened while canceling old stop_loss.\nException: {e}"
                time.sleep(retry_time)
                #Checking cancelation status n number of time
                for i in range(number_of_try): 
                    try:                    
                        order_status_stop_loss = client.futures_get_order(   # check new
                            symbol=symbol,
                            orderId= canceled_order_orderId
                        )
                        if order_status_stop_loss['status'] == "CANCELED":
                            print(f"Stoploss order status is CANCELED. orderID: {order_status_stop_loss['orderId']}")
                            break
                        else:
                            if i <= (number_of_try - 2):
                                print(f"Stoploss order cancelation status is NOT CANCELED. orderID: {order_status_stop_loss['orderId']}")
                                print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                time.sleep(retry_time)
                                continue
                            else:
                                print(f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED).")
                                return 1010, f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED)."

                    except Exception as e: #Error when 3rd try is not successful
                        print("Error checking cancelation order status:", e)
                        if i <= (number_of_try - 2):
                            print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Error occurred while checking status of older stop_loss cancelation order.\nException: {traceback.format_exc()}")
                            return 1011, f"Error occurred while checking status of older stop_loss cancelation order.\nException: {e}"
                        
            else:
                print("Older stop_loss_order_id was None. No cancellation needed")



            #------------------ Placing Stoploss order
            info = None

            # Using new_leads_leverage_for_stoploss, as new_leads_leverage can be sometimes very low and we cannot allot money that much over out actual leverage our_leverage, also calcualtions will get stop price 0 or negative if new leads leerage is 1 or less.
            if new_leads_leverage < min_leverage_for_stop_price:
                print(f"As new_leads_leverage({new_leads_leverage}) < min_leverage_for_stop_price({min_leverage_for_stop_price}), taking (new_leads_leverage = min_leverage_for_stop_price)")
                new_leads_leverage_for_stoploss = min_leverage_for_stop_price
            elif new_leads_leverage > max_leverage_for_stop_price:
                print(f"As new_leads_leverage({new_leads_leverage}) > max_leverage_for_stop_price({max_leverage_for_stop_price}), taking (new_leads_leverage = max_leverage_for_stop_price)")
                new_leads_leverage_for_stoploss = max_leverage_for_stop_price
            else:
                new_leads_leverage_for_stoploss = new_leads_leverage

            
            x = 1 if position_side == "LONG" else -1
            print('Trying to place stop loss')
            stoploss_percent = percent_we_can_loose_stop_loss                         # Not using it anymore
            new_stop_loss_price = round((new_avg_coin_price - (new_avg_coin_price / new_leads_leverage_for_stoploss) * (x)), price_precision_integer) # using new_leads_leverage_for_stoploss, as new_leads_leverage can be sometime very low and we cannot allot money that much over out actual leverage our_leverage.
            print(f"new_stop_loss_price: {new_stop_loss_price}")

            # Try to place stop_loss_order for up to number_of_try times
            for i in range(number_of_try):
                try:
                    stop_loss_order = client.futures_create_order(symbol=symbol, positionSide=position_side, side=close_side,
                                                            type=client.FUTURE_ORDER_TYPE_STOP_MARKET,
                                                            quantity=new_our_total_hold,
                                                            stopPrice=new_stop_loss_price)

                    stop_loss_orderId = str(stop_loss_order['orderId']) # Assigning orderid in string format.
                    print("Stoploss order placed successfully. stop_loss_orderId: ", stop_loss_orderId)
                    break
                    
                except Exception as e:

                    if hasattr(e, 'code') and e.code == -2021:
                        print(f"Order would Immediately trigger error encountered.\nException: {e}")
                        print("Closing complete position immediately.")
                        # Immediately close the postiion.
                        # Try to place stop_loss_market_order for upto number_of_try times
                        for i in range(number_of_try):
                            try:
                                stop_loss_market_order = client.futures_create_order(symbol=symbol, positionSide=position_side,
                                                                                side=close_side,
                                                                                type=client.FUTURE_ORDER_TYPE_MARKET,
                                                                                quantity=new_our_total_hold)
                                
                                stop_loss_orderId = str(stop_loss_market_order['orderId']) # Assigning orderid in string format.
                                print("Stoploss market order placed successfully. stop_loss_orderId: ", stop_loss_orderId)
                                break
                                
                            except Exception as e: #Error when 3rd try is not successful
                                print("Error placing stop_loss_market_order:", e)
                                if i <= (number_of_try - 2):           #--------------------- check
                                    print(f"Retrying stop_loss_market_order in {retry_time} seconds...(try no: {i}/{number_of_try})")
                                    time.sleep(retry_time)
                                    continue
                                else:
                                    stop_loss_orderId = None
                                    print(f"Error occurred while placing stoploss_market_order also.\nException: {traceback.format_exc()}")
                                    return 1012, f"Error occurred while placing stoploss_market_order ordern also.\nException: {e}"
                        time.sleep(retry_time)        
                        for i in range(number_of_try):
                            try:    
                                order_status_stop_loss_market_order = client.futures_get_order(   # check new
                                    symbol = symbol,
                                    orderId = stop_loss_orderId)
                                
                                if order_status_stop_loss_market_order['status'] == "FILLED":
                                    print(f"Stoploss market order is FILLED for: {order_status_stop_loss_market_order['orderId']}")
                                    info = "stop_loss_error"
                                    break
                                else:
                                    if i <= (number_of_try - 2):
                                        print(f"Stoploss market order status is NOT FILLED. orderID: {order_status_stop_loss_market_order['orderId']}")
                                        print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                        time.sleep(retry_time)
                                        continue
                                    else:
                                        print(f"Stoploss market order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id FILLED).")
                                        return 1010, f"Stoploss market order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id FILLED)."

                                
                            except Exception as e: #Error when 3rd try is not successful
                                print("Error checking cancelation order status:", e)
                                if i <= (number_of_try - 2):
                                    print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                                    time.sleep(retry_time)
                                    continue
                                else:
                                    print(f"Error occurred while checking status of Stoploss market order.\nException: {traceback.format_exc()}")
                                    return 1011, f"Error occurred while checking status of Stoploss market order.\nException: {e}"
            
                        # Calculations with new data
                        stopmarketOrderQty, stopmarketOrderPrice = float(order_status_stop_loss_market_order['executedQty']), float(order_status_stop_loss_market_order['avgPrice'])
                        stopmarket_our_transaction_amount = (stopmarketOrderQty) * (stopmarketOrderPrice)
                        # PNL Calculation
                        y = 1 if position_side == "LONG" else -1
                        stop_PNL = stopmarketOrderQty * (stopmarketOrderPrice - new_avg_coin_price) * (y)                                      
                        print(f"stop_PNL: {stop_PNL}")
                        break 

                    elif i <= (number_of_try - 2):                     #--------------------- check
                        print(f"Retrying to place stop_loss_order in {retry_time} seconds...(try no: {i}/{number_of_try})")
                        time.sleep(retry_time)
                        continue
                    
                    else:
                        print(f"Exception happened while placing stop_loss_order after 3rd attempt also.\nException: {traceback.format_exc()}")
                        return 1022, f"Exception happened while placing stop_loss_order after 3rd attempt also.\nException: {e}"
            time.sleep(retry_time)
            if info == None:
                for i in range(number_of_try):
                    try:
                        order_status_stop_loss = client.futures_get_order(   # check new
                            symbol = symbol,
                            orderId = stop_loss_orderId
                        )
                        if order_status_stop_loss['status'] == "NEW":       # check new
                            print(f"Stoploss order status is NEW. orderId: {order_status_stop_loss['orderId']}")
                            break  # Exit the loop if order is placed successfully
                        else:
                            if i <= (number_of_try - 2):
                                print(f"Stoploss order status is NOT NEW. orderID: {order_status_stop_loss['orderId']}")
                                print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                time.sleep(retry_time)
                                continue
                            else:
                                print(f"Stoploss order status is NOT NEW after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED).")
                                return 1010, f"Stoploss order status is NOT NEW after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED)."
                            
                    except Exception as e: #Error when 3rd try is not successful
                        print("Error checking cancelation order status:", e)
                        if i <= (number_of_try - 2):
                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Error occurred while checking status of older stop_loss cancelation order.\nException: {traceback.format_exc()}")
                            return 1011, f"Error occurred while checking status of older stop_loss cancelation order.\nException: {e}"


            # Append new row in the Trading_df with all updated details details.
            self.add_to_trading_data_df(
                time=self.get_current_time(),
                trade_order_id=market_orderId,
                address=address, 
                symbol=symbol, 
                is_long_short=position_side,
                trade_type=open_side,
                leads_price=asset_price,
                price=marketOrderPrice,
                weighted_score_ratio=weighted_score_ratio,
                leads_max_volume=leads_max_volume,
                leads_leverage=new_leads_leverage,
                leads_transaction_quantity=transaction_quantity,
                leads_transaction_amount=transaction_amount,
                our_leverage=our_leverage,
                our_transaction_quantity=marketOrderQty,
                our_transaction_amount=new_our_transaction_amount,
                leads_total_hold=new_leads_total_hold, 
                leads_total_investment=new_leads_total_investment,
                avg_leads_coin_price=new_avg_leads_coin_price,
                our_total_hold=new_our_total_hold,
                our_total_investment=new_our_total_investment,
                avg_coin_price=new_avg_coin_price,
                total_hold_ratio=new_total_hold_ratio,
                stop_loss_price=new_stop_loss_price,
                stop_loss_order_id=stop_loss_orderId,
                is_stop_loss_executed=False,
                is_liquidated=False,
                take_profit_price=0,
                take_profit_order_id=None,
                PNL=0
            )


            # If error happened during placing the general stop_loss order
            if info == "stop_loss_error":  # this means stop_loss price conflicted with market price and we have sold the coins immediately.
                self.add_to_trading_data_df(
                    time= self.get_current_time(),
                    trade_order_id=stop_loss_orderId,
                    address=address,
                    symbol=symbol,
                    is_long_short=position_side,
                    trade_type=close_side,
                    leads_price=0,
                    price=stopmarketOrderPrice,
                    weighted_score_ratio=weighted_score_ratio,
                    leads_max_volume=leads_max_volume,
                    leads_leverage=new_leads_leverage,
                    leads_transaction_quantity=0,
                    leads_transaction_amount=0,
                    our_leverage=our_leverage,
                    our_transaction_quantity=stopmarketOrderQty,
                    our_transaction_amount=stopmarket_our_transaction_amount,
                    leads_total_hold=0, 
                    leads_total_investment=0,
                    avg_leads_coin_price=0,
                    our_total_hold=0,
                    our_total_investment=new_our_total_investment,
                    avg_coin_price=new_avg_coin_price,
                    total_hold_ratio=0,
                    stop_loss_price=0,
                    stop_loss_order_id=None,
                    is_stop_loss_executed=True,
                    is_liquidated=False,
                    take_profit_price=0,
                    take_profit_order_id=None,
                    PNL=stop_PNL
                )

            # Return the code as True and error description as None if everything goes succesfully
            return True, None


        collector = Collector()
        collector.start_collecting()

        response, description = openTrade( client, traders_list, address, symbol, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage)

        collector.stop_collecting()
        content_prints = collector.content

        if response == True:
            pass
        else:
            if current_trade_orderId is not None:
                Alert_note = f"Panic, Open (in ultimate_openTrade fucntion) trade taken before error(Now banning the position for {ban_time_hours}hrs). current_trade_orderId:{current_trade_orderId}"
                current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price, market_order_status = self.error_return_latest_data(address, symbol, position_side, current_trade_orderId, client)
                #Writing content for email
                print(Alert_note)
                content = f"{Alert_note}\nError code: {response},\nDescription: {description},\n\naddress: {address},\ncoin:{coin},\nis_long_short: {position_side},\ntime: {self.get_current_time()},\ntransaction_quantity: {transaction_quantity},\ntransaction_amount: {transaction_amount}\n\ncurrent_market_OrderQty:{current_market_OrderQty}, current_market_OrderPrice:{current_market_OrderPrice}, new_our_total_hold:{new_our_total_hold}, new_avg_coin_price:{new_avg_coin_price},\nmarket_order_status:{market_order_status}\n\n\n{content_prints}"
                self.send_message("ALERT", content)
                self.add_to_ban_list(address, symbol, position_side, current_trade_orderId, current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price) # Added to "ban_positions_info_list"
            else:
                Alert_note = "Relax, Open (in ultimate_openTrade fucntion) trade not taken before error"
                leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)
                #Writing content for email
                print(Alert_note)
                content = f"{Alert_note}\nError code: {response},\nDescription: {description},\n\naddress: {address},\ncoin:{coin},\nis_long_short: {position_side},\ntime: {self.get_current_time()},\ntransaction_quantity: {transaction_quantity},\ntransaction_amount: {transaction_amount}\n,\nour_total_hold:{our_total_hold},\navg_coin_price:{avg_coin_price}\n\n\n\n{content_prints}"
                self.send_message("ALERT", content)




#---Closing----------
    def ultimate_closeTrade(self, client, traders_list, address, coin, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage):

        print("Time:", self.get_current_time())

        symbol = coin + "USDT"
        current_trade_orderId = None

        # Closing Trades
        def closeTrade(client, address, symbol, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage):


            PNL = 0
            stop_PNL = 0
            nonlocal current_trade_orderId
            
            weighted_score_ratio = traders_list['Ranking_Score'][traders_list['account'] == address].iloc[0] / traders_list['Ranking_Score'].sum()
            leads_max_volume = traders_list['max_volume'][traders_list['account'] == address].iloc[0]

            #---------------------------
            try:                                                                                                                     #  added new check
                exchange_information = client.futures_exchange_info()
                symbol_info = next((s for s in exchange_information['symbols'] if s['symbol'] == symbol), None)  # corrected line
                if symbol_info:
                    # Precision for the quantity
                    quantity_precision = next((f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'MARKET_LOT_SIZE'), None)
                    # Precision for the price in dollar
                    price_precision =  next((f['tickSize'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'), None)
                    # Minimum notional value(minimum dollars)
                    min_notional = float(next((f['notional'] for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None))
                    # Get integer value of precision
                    quantity_precision_integer = 0 if '.' not in str(quantity_precision) else len(
                        str(quantity_precision).split('.')[1].rstrip('0')) if str(quantity_precision) else None
                    price_precision_integer = 0 if '.' not in str(price_precision) else len(
                        str(price_precision).split('.')[1].rstrip('0')) if str(price_precision) else None

                    #Printing lead's qunatity and amount
                    transaction_amount = float(self.floor_decimal(transaction_amount, price_precision_integer))
                    transaction_quantity = float(self.floor_decimal(transaction_quantity, quantity_precision_integer))
                    print(f"Lead's transaction amaount: ", transaction_amount)
                    print(f"Lead's transaction quantity: ", transaction_quantity)
                    if transaction_amount == 0 or transaction_quantity == 0:
                        print("Lead's Quantites are zero when rounded. Rejecting trade.")
                        return True, None
                    print(f"min_notional: {min_notional}")
                    print(f"quantity_precision_integer: {quantity_precision_integer}")
                    print(f"price_precision_integer: {price_precision_integer}")
                    
                    quantity_precision_integer = int(quantity_precision_integer)
                    price_precision_integer = int(price_precision_integer)
                    
                    try:                                                                                             #  added new check
                        ticker = client.futures_symbol_ticker(symbol=symbol)
                        price_on_bin = float(ticker['price'])
                        print(f"Current market price of {symbol}: {price_on_bin}")
                    except Exception as e:
                        print(f"Error occurred during coin {symbol} price fetching from Binance.\nException: {traceback.format_exc()}")
                        return 2001, f"Error occurred during coin {symbol} price fetching from Binance.\nException: {e}"
                    
                    # Minimum quantity to buy
                    minimum_quantity = min_notional / price_on_bin * 1.02
                    min_qty = self.round_up_to_ceil_with_precision(minimum_quantity, quantity_precision_integer)
                    
                else:
                    print(f"Symbol {symbol} not found in exchange information.")
                    return 2002, f"Symbol {symbol} not found in exchange information."  # Error code and description , above we used 1005 and its same error check
                
            except Exception as e:
                print(f"Error occurred during coin info fetching from Binance.\nException: {traceback.format_exc()}")
                return 2003, f"Error occurred during coin info fetching from Binance.\nException: {e}"

            
            # Rechecking old stop loss and filling df if executed
            response_from_old_stop_loss = self.check_old_stop_loss(client, trading_data_df, address, symbol, position_side) 
            print('Trying to check old stop loss status before moving on.')
            if response_from_old_stop_loss == False:
                print(f"Exception happened while check_old_stop_loss.")
                return False, f"Exception happened while check_old_stop_loss."


            # Now check the last row through below function & fetch last row values from Trading_df about the current position
            leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)


            # Check if the trader had any last row present that is able to let us close it
            if our_total_hold == 0:  # As ultimately if last row was not present or was not eligible, we return our_total_hold=0
                print("No asset or open-position present to close")
                return True, "No asset or open-position present to close"  # Error code and description
            else:
                pass


            #-------------------------------------------------
            # Calculating parameters for closing                                          
            if transaction_quantity >= leads_total_hold:
                quantity_to_close = our_total_hold
                print("--Closing completely.--")
            else:
                quantity_to_close = round((total_hold_ratio * transaction_quantity), quantity_precision_integer)
                print("ideal_quantity_to_close: ",quantity_to_close)
                min_qty_to_close = 1/(10**(quantity_precision_integer)) #For closing, minimum quantity is equal to lowest number in precesion possible.
                if quantity_to_close >= our_total_hold:
                    quantity_to_close = our_total_hold
                elif quantity_to_close > 0.98 * our_total_hold:
                    quantity_to_close = our_total_hold
                elif quantity_to_close < min_qty_to_close:
                    quantity_to_close = min_qty_to_close
                

            print(f"Our hold: {our_total_hold}")
            print(f"Quantity to close: {quantity_to_close}")


            # Fetching open_side value i.e buy or sell
            open_side, close_side = self.sideAndCounterSideForBinance(position_side)


            # Try to palce order for upto number_of_try times
            #Clsoing order market.
            for i in range(number_of_try):
                try:
                    market_order = client.futures_create_order(symbol=symbol, positionSide=position_side, side=close_side,
                                            type=client.FUTURE_ORDER_TYPE_MARKET, quantity=quantity_to_close)

                    market_orderId = str(market_order['orderId']) # Assigning orderid in string format.

                    current_trade_orderId = market_orderId
                    
                    print("Market close trade order placed successfully. market_orderId: ", market_orderId)
                    break

                except Exception as e: #Error when 3rd try is not successful
                    print("Error placing order:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying placing market order in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while placing market close trade order.\nException: {traceback.format_exc()}")
                        return 1009, f"Error occurred while placing market close trade order.\nException: {e}"

            time.sleep(retry_time)        
            # Trying to check market close trade order status n number of times.
            print("Checking market close trade order status if FILLED or NOT.")
            for i in range(number_of_try):
                try:
                    order_status = client.futures_get_order(
                        symbol=symbol,
                        orderId= market_orderId
                        )

                    if order_status['status'] == "FILLED":       # check new , earlier orderStatus SUCCESS was written, 'status': 'FILLED', or 'NEW'
                        print(f"Market close order status is FILLED, orderId: {market_order['orderId']}")
                        break
                    else:
                        if i <= (number_of_try - 2):
                            print(f"Market close order status is NOT FILLED. orderId: {market_order['orderId']}")
                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Market close order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED).")
                            return 1010, f"Market close order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED)."
                            
                except Exception as e: #Error when 3rd try is not successful
                    print("Error checking order status:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while checking status of market close trade order.\nException: {traceback.format_exc()}")
                        return 1011, f"Error occurred while checking status of market closeopen trade order.\nException: {e}"


            marketOrderQty, marketOrderPrice = float(order_status['executedQty']), float(order_status['avgPrice'])
            new_our_transaction_amount = marketOrderQty * marketOrderPrice

            # PNL
            y = 1 if position_side == "LONG" else -1
            PNL = marketOrderQty * (marketOrderPrice - avg_coin_price) * (y)                                         # check
            print(f"PNL: {PNL}")

            # Calculating leads values
            if (transaction_quantity >= leads_total_hold) or (quantity_to_close == our_total_hold):
                new_leads_total_hold = 0
                new_leads_total_investment = 0
            else:
                new_leads_total_hold =  round((leads_total_hold - transaction_quantity), quantity_precision_integer)   # coins
                new_leads_total_investment = (leads_total_investment - transaction_amount)
            new_avg_leads_coin_price = avg_leads_coin_price

            # Calculating out values
            new_our_total_hold = round((our_total_hold - marketOrderQty), quantity_precision_integer)             # coins
            if new_our_total_hold != 0:
                new_our_total_investment = (our_total_investment) - (new_our_transaction_amount)
            else:
                new_our_total_investment = 0
            new_avg_coin_price = avg_coin_price
            new_total_hold_ratio = total_hold_ratio

            print(f"new_leads_total_hold: {new_leads_total_hold}")
            print(f"new_leads_total_investment: {new_leads_total_investment}")
            print(f"new_avg_leads_coin_price: {new_avg_leads_coin_price}")
            print(f"new_our_total_hold: {new_our_total_hold}")
            print(f"new_our_total_investment: {new_our_total_investment}")
            print(f"new_avg_coin_price: {new_avg_coin_price}")
            print(f"new_total_hold_ratio: {new_total_hold_ratio}")

            # ------------ Resetting Stoploss
            # Try to cancel_older_stoploss for upto number_of_try times
            if stop_loss_order_id is not None:
                print(f"Old stoploss orderId: {stop_loss_order_id}")
                print('Trying to cancel old stop loss')
                for i in range(number_of_try):  
                    try:
                        cancel_older_stoploss = client.futures_cancel_order(symbol=symbol, orderId=stop_loss_order_id)

                        canceled_order_orderId = str(cancel_older_stoploss['orderId']) # Assigning orderid in string format.
                        print("Older stoploss cancelation order placed successfully.")
                        break

                    except Exception as e: #Error when 3rd try is not successful
                        print("Error canceling older stoploss order:", e)
                        if i <= (number_of_try - 2): 
                            print(f"Retrying cancel_older_stoploss in {retry_time} seconds...(try no: {i}/{number_of_try})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Exception happened while canceling old stop_loss.\nException: {traceback.format_exc()}")
                            return 1011, f"Exception happened while canceling old stop_loss.\nException: {e}"
                time.sleep(retry_time)
                #Checking cancelation status n number of time
                for i in range(number_of_try): 
                    try:                    
                        order_status_stop_loss = client.futures_get_order(   # check new
                            symbol=symbol,
                            orderId= canceled_order_orderId
                        )
                        if order_status_stop_loss['status'] == "CANCELED":
                            print(f"Stoploss order status is CANCELED. orderID: {order_status_stop_loss['orderId']}")
                            break
                        else:
                            if i <= (number_of_try - 2):
                                print(f"Stoploss order cancelation status is NOT CANCELED. orderID: {order_status_stop_loss['orderId']}")
                                print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                time.sleep(retry_time)
                                continue
                            else:
                                print(f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED).")
                                return 1010, f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED)."

                    except Exception as e: #Error when 3rd try is not successful
                        print("Error checking cancelation order status:", e)
                        if i <= (number_of_try - 2):
                            print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Error occurred while checking status of older stop_loss cancelation order.\nException: {traceback.format_exc()}")
                            return 1011, f"Error occurred while checking status of older stop_loss cancelation order.\nException: {e}"
                        
            else:
                print("Older stop_loss_order_id was None. Not possible, as our_hold was not zero, i.e old stoploss should be their.") # Not expected to ever come to this part if older stoploss was not there, as if stoploss was not there i.e our_hold must be 0, so trade should be rejected in before condition.
                return 2023, "Older stop_loss_order_id was None. Not possible, as our_hold was not zero, i.e old stoploss should be their."
        

        #-------------------------------------------------------------------------------------------
            # Now place new stop-loss with updated coin quantityand price after cancelling older stop_loss
            # Calculating new total holds & new avg coin price
            info = None
            stop_loss_orderId = None # Initializing the variable
            new_stop_loss_price = None


                
            if new_our_total_hold !=0:
                
                # Using new_leads_leverage_for_stoploss, as new_leads_leverage can be sometimes very low and we cannot allot money that much over out actual leverage our_leverage, also calcualtions will get stop price 0 or negative if new leads leerage is 1 or less.
                if new_leads_leverage < min_leverage_for_stop_price:
                    print(f"As new_leads_leverage({new_leads_leverage}) < min_leverage_for_stop_price({min_leverage_for_stop_price}), taking (new_leads_leverage = min_leverage_for_stop_price)")
                    new_leads_leverage_for_stoploss = min_leverage_for_stop_price
                elif new_leads_leverage > max_leverage_for_stop_price:
                    print(f"As new_leads_leverage({new_leads_leverage}) > max_leverage_for_stop_price({max_leverage_for_stop_price}), taking (new_leads_leverage = max_leverage_for_stop_price)")
                    new_leads_leverage_for_stoploss = max_leverage_for_stop_price
                else:
                    new_leads_leverage_for_stoploss = new_leads_leverage

                
                x = 1 if position_side == "LONG" else -1
                stoploss_percent = percent_we_can_loose_stop_loss  # it is the amount ratio we are ready to lose
                new_stop_loss_price = round((new_avg_coin_price - (new_avg_coin_price / new_leads_leverage_for_stoploss) * (x)), price_precision_integer) # using new_leads_leverage_for_stoploss, as new_leads_leverage can be sometime very low and we cannot allot money that much over out actual leverage our_leverage.
                print(f"new_stop_loss_price: {new_stop_loss_price}")
                print('Trying to place stop loss')

                # Try to place stop_loss_order for up to number_of_try times
                for i in range(number_of_try):
                    try:
                        stop_loss_order = client.futures_create_order(symbol=symbol, positionSide=position_side, side=close_side,
                                                                type=client.FUTURE_ORDER_TYPE_STOP_MARKET,
                                                                quantity=new_our_total_hold,
                                                                stopPrice=new_stop_loss_price)

                        stop_loss_orderId = str(stop_loss_order['orderId']) # Assigning orderid in string format.
                        print("Stoploss order placed successfully. stop_loss_orderId: ", stop_loss_orderId)
                        break
                        
                    except Exception as e:

                        if hasattr(e, 'code') and e.code == -2021:
                            print(f"Order would Immediately trigger error encountered.\nException: {e}")
                            print("Closing complete position immediately.")
                            # Immediately close the postiion.
                            # Try to place stop_loss_market_order for upto number_of_try times
                            for i in range(number_of_try):
                                try:
                                    stop_loss_market_order = client.futures_create_order(symbol=symbol, positionSide=position_side,
                                                                                    side=close_side,
                                                                                    type=client.FUTURE_ORDER_TYPE_MARKET,
                                                                                    quantity=new_our_total_hold)
                                    
                                    stop_loss_orderId = str(stop_loss_market_order['orderId']) # Assigning orderid in string format.
                                    print("Stoploss market order placed successfully. stop_loss_orderId: ", stop_loss_orderId)
                                    break
                                    
                                except Exception as e: #Error when 3rd try is not successful
                                    print("Error placing stop_loss_market_order:", e)
                                    if i <= (number_of_try - 2):           #--------------------- check
                                        print(f"Retrying stop_loss_market_order in {retry_time} seconds...(try no: {i}/{number_of_try})")
                                        time.sleep(retry_time)
                                        continue
                                    else:
                                        stop_loss_orderId = None
                                        print(f"Error occurred while placing stoploss_market_order also.\nException: {traceback.format_exc()}")
                                        return 1012, f"Error occurred while placing stoploss_market_order ordern also.\nException: {e}"
                            time.sleep(retry_time)        
                            for i in range(number_of_try):
                                try:    
                                    order_status_stop_loss_market_order = client.futures_get_order(   # check new
                                        symbol = symbol,
                                        orderId = stop_loss_orderId)
                                    
                                    if order_status_stop_loss_market_order['status'] == "FILLED":
                                        print(f"Stoploss market order is FILLED for: {order_status_stop_loss_market_order['orderId']}")
                                        info = "stop_loss_error"
                                        break
                                    else:
                                        if i <= (number_of_try - 2):
                                            print(f"Stoploss market order status is NOT FILLED. orderID: {order_status_stop_loss_market_order['orderId']}")
                                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                            time.sleep(retry_time)
                                            continue
                                        else:
                                            print(f"Stoploss market order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id FILLED).")
                                            return 1010, f"Stoploss market order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id FILLED)."

                                    
                                except Exception as e: #Error when 3rd try is not successful
                                    print("Error checking cancelation order status:", e)
                                    if i <= (number_of_try - 2):
                                        print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                                        time.sleep(retry_time)
                                        continue
                                    else:
                                        print(f"Error occurred while checking status of Stoploss market order.\nException: {traceback.format_exc()}")
                                        return 1011, f"Error occurred while checking status of Stoploss market order.\nException: {e}"
                
                            # Calculations with new data
                            stopmarketOrderQty, stopmarketOrderPrice = float(order_status_stop_loss_market_order['executedQty']), float(order_status_stop_loss_market_order['avgPrice'])
                            stopmarket_our_transaction_amount = (stopmarketOrderQty) * (stopmarketOrderPrice)
                            # PNL Calculation
                            y = 1 if position_side == "LONG" else -1
                            stop_PNL = stopmarketOrderQty * (stopmarketOrderPrice - new_avg_coin_price) * (y)                                      
                            print(f"stop_PNL: {stop_PNL}")
                            break 

                        elif i <= (number_of_try - 2):                     #--------------------- check
                            print(f"Retrying to place stop_loss_order in {retry_time} seconds...(try no: {i}/{number_of_try})")
                            time.sleep(retry_time)
                            continue
                        
                        else:
                            print(f"Exception happened while placing stop_loss_order after 3rd attempt also.\nException: {traceback.format_exc()}")
                            return 1022, f"Exception happened while placing stop_loss_order after 3rd attempt also.\nException: {e}"
                time.sleep(retry_time)
                if info == None:
                    for i in range(number_of_try):
                        try:
                            order_status_stop_loss = client.futures_get_order(   # check new
                                symbol = symbol,
                                orderId = stop_loss_orderId
                            )
                            if order_status_stop_loss['status'] == "NEW":       # check new
                                print(f"Stoploss order status is NEW. orderId: {order_status_stop_loss['orderId']}")
                                break  # Exit the loop if order is placed successfully
                            else:
                                if i <= (number_of_try - 2):
                                    print(f"Stoploss order status is NOT NEW. orderID: {order_status_stop_loss['orderId']}")
                                    print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                    time.sleep(retry_time)
                                    continue
                                else:
                                    print(f"Stoploss order status is NOT NEW after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED).")
                                    return 1010, f"Stoploss order status is NOT NEW after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED)."

                        except Exception as e: #Error when 3rd try is not successful
                            print("Error checking cancelation order status:", e)
                            if i <= (number_of_try - 2):
                                print(f"Retrying checking order status in {retry_time} seconds...({i})")
                                time.sleep(retry_time)
                                continue
                            else:
                                print(f"Error occurred while checking status of older stop_loss cancelation order.\nException: {traceback.format_exc()}")
                                return 1011, f"Error occurred while checking status of older stop_loss cancelation order.\nException: {e}"


            # Append new row in the Trading_df with all updated details details.
            self.add_to_trading_data_df(
                time= self.get_current_time(),
                trade_order_id=market_orderId,
                address=address,
                symbol=symbol,
                is_long_short=position_side,
                trade_type=close_side,
                leads_price=asset_price,
                price=marketOrderPrice,
                weighted_score_ratio=weighted_score_ratio,
                leads_max_volume=leads_max_volume,
                leads_leverage=new_leads_leverage,
                leads_transaction_quantity=transaction_quantity,
                leads_transaction_amount=transaction_amount,
                our_leverage=our_leverage,
                our_transaction_quantity=marketOrderQty,
                our_transaction_amount=new_our_transaction_amount,
                leads_total_hold=new_leads_total_hold,
                leads_total_investment=new_leads_total_investment,
                avg_leads_coin_price=new_avg_leads_coin_price,
                our_total_hold=new_our_total_hold,
                our_total_investment=new_our_total_investment,
                avg_coin_price=new_avg_coin_price,
                total_hold_ratio=new_total_hold_ratio,
                stop_loss_price=new_stop_loss_price,
                stop_loss_order_id=stop_loss_orderId,
                is_stop_loss_executed=False,
                is_liquidated=False,
                take_profit_price=0,
                take_profit_order_id=None,
                PNL=PNL
            )

            # If error happened during palcing the general stop_loss order
            if info == "stop_loss_error":  # this means stop_loss price conflicted with market price and we have sold the coins immideately.
                self.add_to_trading_data_df(
                    time= self.get_current_time(),
                    trade_order_id=stop_loss_orderId,
                    address=address,
                    symbol=symbol,
                    is_long_short=position_side,
                    trade_type=close_side,
                    leads_price=0,
                    price=stopmarketOrderPrice,
                    weighted_score_ratio=weighted_score_ratio,
                    leads_max_volume=leads_max_volume,
                    leads_leverage=new_leads_leverage,
                    leads_transaction_quantity=0,
                    leads_transaction_amount=0,
                    our_leverage=our_leverage,
                    our_transaction_quantity=stopmarketOrderQty,
                    our_transaction_amount=stopmarket_our_transaction_amount,
                    leads_total_hold=0, 
                    leads_total_investment=0,
                    avg_leads_coin_price=new_avg_leads_coin_price,
                    our_total_hold=0,
                    our_total_investment=new_our_total_investment,
                    avg_coin_price=new_avg_coin_price,
                    total_hold_ratio=0,
                    stop_loss_price=0,
                    stop_loss_order_id=None,
                    is_stop_loss_executed=True,
                    is_liquidated=False,
                    take_profit_price=0,
                    take_profit_order_id=None,
                    PNL=stop_PNL
                )
            
            # Return the code as True and error description as None if everything goes succesfully
            return True, None 

        collector = Collector()
        collector.start_collecting()

        response, description = closeTrade(client, address, symbol, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage)

        collector.stop_collecting()
        content_prints = collector.content

        if response == True:
            pass
        else:
            if current_trade_orderId is not None:
                Alert_note = f"Panic, Close (ultimate_closeTrade function) trade taken before error(Now banning the position for {ban_time_hours}hrs). current_trade_orderId:{current_trade_orderId}"
                current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price, market_order_status = self.error_return_latest_data(address, symbol, position_side, current_trade_orderId, client)
                #Writing content for email
                print(Alert_note)
                content = f"{Alert_note}\nError code: {response},\nDescription: {description},\n\naddress: {address},\ncoin:{coin}, is_long_short: {position_side},\ntime: {self.get_current_time()},\ntransaction_quantity: {transaction_quantity},\ntransaction_amount: {transaction_amount}\n\ncurrent_market_OrderQty:{current_market_OrderQty},\ncurrent_market_OrderPrice:{current_market_OrderPrice},\nnew_our_total_hold:{new_our_total_hold},\nnew_avg_coin_price:{new_avg_coin_price},\nmarket_order_status:{market_order_status}\n\n\n{content_prints}"
                self.send_message("ALERT", content)
                self.add_to_ban_list(address, symbol, position_side, current_trade_orderId, current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price) # Added to "ban_positions_info_list"
            else:
                Alert_note = "Relax, Close (ultimate_closeTrade function) trade not taken before error"
                leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)
                #Writing content for email
                print(Alert_note)
                content = f"{Alert_note}\nError code: {response},\nDescription: {description},\n\naddress: {address},\ncoin:{coin},\nis_long_short: {position_side},\ntime: {self.get_current_time()},\ntransaction_quantity: {transaction_quantity},\ntransaction_amount: {transaction_amount}\n,\nour_total_hold:{our_total_hold},\navg_coin_price:{avg_coin_price}\n\n\n\n{content_prints}"
                self.send_message("ALERT", content)




#---Liquidation----------
    def ultimate_liquidateTrade(self,client, address, coin, position_side):

        print("Time:", self.get_current_time())
        # Symbol value
        symbol = coin + "USDT"

        # Setting takeprofit also for liquia=dated trades
        def liquidateTrade(client, address, coin, position_side):

        #---------------------------
            weighted_score_ratio = traders_list['Ranking_Score'][traders_list['account'] == address].iloc[0] / traders_list['Ranking_Score'].sum()
            leads_max_volume = traders_list['max_volume'][traders_list['account'] == address].iloc[0]

            try:                                                                                                                  #  added new check
                exchange_information = client.futures_exchange_info()
                symbol_info = next((s for s in exchange_information['symbols'] if s['symbol'] == symbol), None)  # corrected line
                if symbol_info:
                    # Precision for the quantity
                    quantity_precision = next((f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'MARKET_LOT_SIZE'), None)
                    # Precision for the price in dollar
                    price_precision =  next((f['tickSize'] for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER'), None)
                    # Minimum notional value (minimum dollars)
                    min_notional = float(next((f['notional'] for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None))
                    # Get integer value of precision
                    quantity_precision_integer = 0 if '.' not in str(quantity_precision) else len(
                        str(quantity_precision).split('.')[1].rstrip('0')) if str(quantity_precision) else None
                    price_precision_integer = 0 if '.' not in str(price_precision) else len(
                        str(price_precision).split('.')[1].rstrip('0')) if str(price_precision) else None
                    
                    quantity_precision_integer = int(quantity_precision_integer)
                    price_precision_integer = int(price_precision_integer)
                    
                    try:                                                                                             #  added new check
                        ticker = client.futures_symbol_ticker(symbol=symbol)
                        price_on_bin = float(ticker['price'])
                        print(f"Current market price of {symbol}: {price_on_bin}")
                    except Exception as e:
                        print(f"Error occurred during coin {symbol} price fetching from Binance.\nException: {traceback.format_exc()}")
                        return 3001, f"Error occurred during coin {symbol} price fetching from Binance.\nException: {e}"
                    # Minimum quantity to buy
                    minimum_quantity_usdt = min_notional/price_on_bin
                    min_qty = self.round_up_to_ceil_with_precision(minimum_quantity_usdt, quantity_precision_integer)
                else:
                    print(f"Symbol {symbol} not found in exchange information.")
                    return 3002, f"Symbol {symbol} not found in exchange information."  # Error code and description , above we used 1005 and its same error check
            except Exception as e:
                print(f"Error occurred during coin info fetching from Binance.\nException: {traceback.format_exc()}")
                return 3003, f"Error occurred during coin info fetching from Binance.\nException: {e}"


            # Rechecking old stop loss and filling df if executed
            response_from_old_stop_loss = self.check_old_stop_loss(client, trading_data_df, address, symbol, position_side) 
            print('Trying to check old stop loss status before moving on.')
            if response_from_old_stop_loss == False:
                print(f"Exception happened while check_old_stop_loss.")
                return False, f"Exception happened while check_old_stop_loss."
            
            # Getting Data from leads last row in this position
            leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)

            # Check if we have any hold for that trader or not
            if our_total_hold == 0:
                print("No holding for the lead to close in liquidation trade.")
                return True, "No holding for the lead to close in liquidation trade."
            
            quantity_to_close = our_total_hold
            print("our_total_hold: ",our_total_hold)
            print("avg_coin_price: ",avg_coin_price)
            
            # Fetching open_side value i.e buy or sell
            open_side, close_side = self.sideAndCounterSideForBinance(position_side)

            print("Canceling older stop_loss.")

            print(f"Old stoploss orderId: {stop_loss_order_id}")
            print('Trying to cancel old stop loss')
            for i in range(number_of_try):  
                try:
                    cancel_older_stoploss = client.futures_cancel_order(symbol=symbol, orderId=stop_loss_order_id)

                    canceled_order_orderId = str(cancel_older_stoploss['orderId']) # Assigning orderid in string format.
                    print("Older stoploss cancelation order placed successfully.")
                    break

                except Exception as e: #Error when 3rd try is not successful
                    print("Error canceling older stoploss order:", e)
                    if i <= (number_of_try - 2): 
                        print(f"Retrying cancel_older_stoploss in {retry_time} seconds...(try no: {i}/{number_of_try})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Exception happened while canceling old stop_loss.\nException: {traceback.format_exc()}")
                        return 1011, f"Exception happened while canceling old stop_loss.\nException: {e}"
            time.sleep(retry_time)
            #Checking cancelation status n number of time
            for i in range(number_of_try): 
                try:                    
                    order_status_stop_loss = client.futures_get_order(   # check new
                        symbol=symbol,
                        orderId= canceled_order_orderId
                    )
                    if order_status_stop_loss['status'] == "CANCELED":
                        print(f"Stoploss order status is CANCELED. orderID: {cancel_older_stoploss['orderId']}")
                        break
                    else:
                        if i <= (number_of_try - 2):
                            print(f"Stoploss order cancelation status is NOT CANCELED. orderID: {cancel_older_stoploss['orderId']}")
                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED).")
                            return 1010, f"Stoploss order cancelation status is NOT CANCELED after checking {number_of_try} times, exiting the trade(check the status now and close postion manually if status id CANCELED)."

                except Exception as e: #Error when 3rd try is not successful
                    print("Error checking cancelation order status:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while checking status of older stop_loss cancelation order.\nException: {traceback.format_exc()}")
                        return 1011, f"Error occurred while checking status of older stop_loss cancelation order.\nException: {e}"
                       

            print("Closing our_total_hold.")
            #Clsoing order market.
            for i in range(number_of_try):
                try:
                    market_order = client.futures_create_order(symbol=symbol, positionSide=position_side, side=close_side,
                                            type=client.FUTURE_ORDER_TYPE_MARKET, quantity=quantity_to_close)

                    market_orderId = str(market_order['orderId']) # Assigning orderid in string format.

                    current_trade_orderId = market_orderId

                    print("Market close trade order placed successfully. market_orderId: ", market_orderId)
                    break

                except Exception as e: #Error when 3rd try is not successful
                    print("Error placing order:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying placing market order in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while placing market close trade order.\nException: {traceback.format_exc()}")
                        return 1009, f"Error occurred while placing market close trade order.\nException: {e}"
            time.sleep(retry_time)
            # Trying to check market close trade order status n number of times.
            print("Checking market close trade order status if FILLED or NOT.")
            for i in range(number_of_try):
                try:
                    order_status = client.futures_get_order(
                        symbol=symbol,
                        orderId= market_orderId
                        )

                    if order_status['status'] == "FILLED":       # check new , earlier orderStatus SUCCESS was written, 'status': 'FILLED', or 'NEW'
                        print(f"Market close order status is FILLED, orderId: {order_status['orderId']}")
                        break
                    else:
                        if i <= (number_of_try - 2):
                            print(f"Market close order status is NOT FILLED. orderId: {order_status['orderId']}")
                            print(f"Retrying checking order status in {retry_time} seconds...({i})")
                            time.sleep(retry_time)
                            continue
                        else:
                            print(f"Market close order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED).")
                            return 1010, f"Market close order status is NOT FILLED after checking {number_of_try} times, exiting the trade(check the status now and close it manually if status id FILLED)."
                            
                except Exception as e: #Error when 3rd try is not successful
                    print("Error checking order status:", e)
                    if i <= (number_of_try - 2):
                        print(f"Retrying requesting order status in {retry_time} seconds...({i})")
                        time.sleep(retry_time)
                        continue
                    else:
                        print(f"Error occurred while checking status of market close trade order.\nException: {traceback.format_exc()}")
                        return 1011, f"Error occurred while checking status of market closeopen trade order.\nException: {e}"

            marketOrderQty, marketOrderPrice = float(order_status['executedQty']), float(order_status['avgPrice'])
            new_our_transaction_amount = marketOrderQty * marketOrderPrice
            print("marketOrderQty: ",marketOrderQty)
            print("marketOrderPrice: ",marketOrderPrice)
            # PNL
            y = 1 if position_side == "LONG" else -1
            PNL = marketOrderQty * (marketOrderPrice - avg_coin_price) * (y)                                         # check
            print(f"PNL: {PNL}")


            # Append new row in the Trading_df with all updated details details.
            self.add_to_trading_data_df(
                time= self.get_current_time(), 
                trade_order_id=market_orderId,
                address=address, 
                symbol=symbol, 
                is_long_short=position_side,
                trade_type="LIQUIDATED",
                leads_price=0,
                price=marketOrderPrice,
                weighted_score_ratio=weighted_score_ratio,
                leads_max_volume=leads_max_volume,
                leads_leverage=leads_leverage,
                leads_transaction_quantity=leads_total_hold,
                leads_transaction_amount=leads_total_investment,
                our_leverage=our_leverage,
                our_transaction_quantity=marketOrderQty,
                our_transaction_amount=new_our_transaction_amount,
                leads_total_hold=leads_total_hold,
                leads_total_investment=leads_total_investment,
                avg_leads_coin_price=avg_leads_coin_price,
                our_total_hold=0,
                our_total_investment=our_total_investment,
                avg_coin_price=avg_coin_price,
                total_hold_ratio=total_hold_ratio,
                stop_loss_price=0,
                stop_loss_order_id= None,
                is_stop_loss_executed=False,
                is_liquidated= True,
                take_profit_price=0,
                take_profit_order_id=None,
                PNL=PNL
            )
            
            # Return the code as True and error description as None if everything goes succesfully
            return True, None

        collector = Collector()
        collector.start_collecting()

        response, description = liquidateTrade(client, address, coin, position_side)

        collector.stop_collecting()
        content_prints = collector.content

        if response == True:
            pass
        else:
            # Getting Data from leads last row in this position
            leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)
            #Writing content for email
            content = f"Position liquidated and some error occoured.\nError code: {response},\nDescription: {description},\n\naddress: {address},\ncoin:{coin},\nis_long_short: {position_side},\ntime: {self.get_current_time()},\nour_total_hold: {our_total_hold},\n,avg_coin_price: {avg_coin_price}\n\n\n{content_prints}"
            self.send_message("ALERT", content)




#---Others----------
    # Function to add a dictionary to the list with a timestamp
    def add_to_ban_list(self, address, symbol, position_side, market_orderId, current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price):
        trade_info = {
            "address": address,
            "symbol": symbol,
            "is_long_short": position_side,
            "timestamp": self.get_current_time()  # Add current timestamp
        }

        ban_positions_info_list.append(trade_info)
        print("Position successfully added to Ban list.")
        print(f"Position banned for (hours= {ban_time_hours})")
        try:
            message_trade =  f"{dex_name}: Banned Position Update (Banned at {self.get_current_time()}, for the next {ban_time_hours} hours)"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email)
            message["Subject"] = message_trade

            # Get the current time in IST
            now = self.get_current_time()

            rows = [
                    ["Time", self.get_current_time()],
                    ["ban_time_hours", ban_time_hours],
                    ["address", address],
                    ["symbol", symbol],
                    ["position_side", position_side],
                    ["current_market_OrderQty", current_market_OrderQty],
                    ["current_market_OrderPrice", current_market_OrderPrice],
                    ["new_our_total_hold", new_our_total_hold],
                    ["new_avg_coin_price", new_avg_coin_price],
                    ["DEX", dex_name],
                ]
            
            self.add_to_trading_data_df(
                    time= self.get_current_time(),
                    trade_order_id=market_orderId,
                    address=address,
                    symbol=symbol,
                    is_long_short=position_side,
                    trade_type='BANNED',
                    leads_price=0,
                    price=current_market_OrderPrice,
                    weighted_score_ratio=0,
                    leads_max_volume=0,
                    leads_leverage=0,
                    leads_transaction_quantity=0,
                    leads_transaction_amount=0,
                    our_leverage=our_leverage,
                    our_transaction_quantity=current_market_OrderQty,
                    our_transaction_amount=current_market_OrderPrice*current_market_OrderQty,
                    leads_total_hold=0,
                    leads_total_investment=0,
                    avg_leads_coin_price=0,
                    our_total_hold=new_our_total_hold,
                    our_total_investment=new_our_total_hold*new_avg_coin_price,
                    avg_coin_price=new_avg_coin_price,
                    total_hold_ratio=0,
                    stop_loss_price=0,
                    stop_loss_order_id=None,
                    is_stop_loss_executed=False,
                    is_liquidated=False,
                    take_profit_price=0,
                    take_profit_order_id=None,
                    PNL=0
                )
            

            table_html = self.create_table_html(rows)
            message.attach(MIMEText(self.generate_html_with_date(), "html")) 
            # Attach table as HTML to the email
            message.attach(MIMEText(table_html, "html"))     

            print("\n**ban_positions_info_list: \n",ban_positions_info_list, "\n")

            email_server = smtplib.SMTP("smtp.gmail.com", 587)
            email_server.starttls()
            email_server.login(sender_email, email_password)
            email_server.sendmail(sender_email, receiver_email, message.as_string())
            
        except Exception as e:
            print(f"Error occurred while constructing or sending the email for banned position update. \nException: {traceback.format_exc()}")


    # Fucntion to check if position is banned
    def is_position_banned(self, address, symbol, position_side):
        for trade_info in ban_positions_info_list:
            if (trade_info["address"] == address and
                    trade_info["symbol"] == symbol and
                    trade_info["is_long_short"] == position_side):
                # Check if time is more than 48 hours ago
                trade_time_str = trade_info.get("timestamp")
                if trade_time_str:
                    try:
                        # Parse the timestamp string to datetime using the specified format
                        trade_time = datetime.strptime(trade_time_str, "%H:%M:%S %d %B %Y")
                        if datetime.now() - trade_time > timedelta(hours=ban_time_hours):
                            # Remove the trade info from the list
                            ban_positions_info_list.remove(trade_info)
                            return False  # Trade info found but expired
                    except ValueError:
                        print(f"Invalid timestamp format in ban_positions_info_list: {trade_time_str}")
                        return False  # Invalid timestamp format
                return True  # Trade info found and within 48 hours
        return False  # Trade info not found


    # Returns total hold and other useful data for email when error happens. 
    def error_return_latest_data(self, address, symbol, position_side, current_trade_orderId, client):
        
        current_market_OrderQty = 0
        current_market_OrderPrice = 0
        market_order_status = None
        try:
            market_order_status = client.futures_get_order(symbol=symbol, orderId=current_trade_orderId)
            current_market_OrderQty, current_market_OrderPrice = float(market_order_status['executedQty']), float(market_order_status['avgPrice'])
        except:
            print(f"Exception happened while error_return_latest_data.\nException: {traceback.format_exc()}")

        print(f"market_order_status of the trade taken before error:\n{market_order_status}")

        # Now check the last row through below function & fetch last row values from Trading_df about the current position
        leads_total_hold, leads_total_investment, avg_leads_coin_price, leads_leverage, our_total_hold, our_total_investment, avg_coin_price, total_hold_ratio, stop_loss_order_id, stop_loss_price, was_last_row_present = self.get_last_row_of_trader_in_trading_data_df(trading_data_df, address, symbol, position_side)

        # Calculating new total holds & avg coin price
        new_our_total_hold = float(current_market_OrderQty) + float(our_total_hold) * 1
        if float(new_our_total_hold) == 0:
            new_avg_coin_price = 0
        else:
            new_avg_coin_price = (float(current_market_OrderQty) * float(current_market_OrderPrice) + float(avg_coin_price) * float(our_total_hold)) / float(new_our_total_hold)

        return current_market_OrderQty, current_market_OrderPrice, new_our_total_hold, new_avg_coin_price, market_order_status





collateral_map = {
    1: ["DAI", 18],
    2: ["WETH", 18],
    3: ["USDC", 6],
}

orderType_category_map = {
    ("MARKET_OPEN", "LIMIT_OPEN", "STOP_OPEN"): "OPEN",
    ("MARKET_CLOSE", "TP_CLOSE", "SL_CLOSE"): "CLOSE",
    ("LIQ_CLOSE",): "LIQUIDATED"
}

def get_order_type_category(order_type):
    for key, value in orderType_category_map.items():
        if order_type in key:
            return value
    return "UNKNOWN"  # Default if the order type is not found


class livePositionExtractiontest: # Runs the loop function to return information on a trader, if any of the 3 events are run.

    def __init__(self, proxy_contract, client, traders_list):

        self.client = client
        self.traders_list = traders_list

        # Initializing the node here
        self.w3 = Web3(Web3.HTTPProvider(alchemy_url))
        print(self.w3.is_connected())



        self.proxy_address = Web3.to_checksum_address(proxy_contract)
        self.contract = self.w3.eth.contract(address=self.proxy_address, abi=ABI)


        # Define all the event methods here itself, called in the log function.
        self.marketex = self.contract.events.MarketExecuted.create_filter(fromBlock='latest').get_new_entries
        self.limitex = self.contract.events.LimitExecuted.create_filter(fromBlock='latest').get_new_entries
        

        # ----Calling the main trading thigns class for trading assistance----
        self.trade = Trading_Things()
        
        

    def loop(self):
        
        # Basically here, all of them will run at the same time.
        while True:
            
            # Main loop to fetch and process events
            self.events_list = []
            # print(self.marketex, self.limitex)
            for marketex_event in self.marketex(): # Make sure to call it
                
                event = marketex_event
                args = marketex_event['args']
                address = args['t']['user'].lower()
                blockNumber = marketex_event['blockNumber']
                pair_index = args['t']['pairIndex']

                new_leads_leverage = args['t']['leverage'] / 1e3

                collateralIndex = args['t']['collateralIndex']
                asset_price = args['t']['openPrice'] / 1e10      #This price equal to price in opening trades. basically we can use it for closing trades as it helps to get the quantity which was originally bought.

                collateral = collateral_map.get(collateralIndex, ["UNKNOWN", 0])
                collateral_token = collateral[0]
                
                collateralAmount_raw = args['t']['collateralAmount']

                collateralAmount = args['t']['collateralAmount'] / 10**(collateral[1])
                collateralPriceUsd =  args['collateralPriceUsd'] / 1e8    #(confirmed)
                
                collateral_usd_volume = collateralAmount * collateralPriceUsd 
                
                transaction_amount = collateral_usd_volume * new_leads_leverage

                if collateralIndex == 2:
                    fake_collateral_token_price = 3400
                else:
                    fake_collateral_token_price = 1

                fake_transaction_amount = collateralAmount * fake_collateral_token_price * new_leads_leverage
                transaction_quantity = fake_transaction_amount / asset_price   # We use fake price so that the values become nearly close to the actual quantity and is fixed always. If we use actual collateral token price, the transaction amount during closing may be different form when we bought and the transaction amount will change, subsequesntly (transaction_quantity = transaction_amount/asset_price) this changes, which is wrong, as in gains transaction quantity during opening adn closing are same.

                coin_data = self.contract.functions.pairs(pair_index).call() 
                is_usd = coin_data[1] == "USD" and coin_data[0] is not None
                coin = coin_data[0]

                position_side = 'LONG' if args['t']['long'] else 'SHORT'

                trade_side = 'MARKET_OPEN' if args['open'] else 'MARKET_CLOSE'
                orderType_enum = 0 if trade_side == 'MARKET_OPEN' else 1

                order_type = get_order_type_category(trade_side)


                event_data = {
                    'event': event,
                    'order_type': order_type,
                    'position_side': position_side,
                    'trade_type': trade_side,
                    'trade_type_enum': orderType_enum,
                    'address': address,
                    'coin':coin,
                    'coin_data': coin_data[0:2],
                    'collateral_token': f"{collateral_token} ({collateralIndex})",
                    'asset_price': asset_price,
                    'collateral_usd_volume': collateral_usd_volume,
                    'transaction_amount': transaction_amount,
                    'transaction_quantity': transaction_quantity,
                    'new_leads_leverage': new_leads_leverage,
                    'blockNumber': blockNumber,
                }
                
                if collateral_token == 'UNKNOWN':
                    print("UNKOWN Collateral Token Appeared. Not adding the event into list for processing.")
                    continue
                
                # Check if trade is in USD or not
                if is_usd:
                    self.events_list.append(event_data)                        
                else:
                    continue

            for limitex_event in self.limitex():
                orderType_map = {
                                0: "MARKET_OPEN",
                                1: "MARKET_CLOSE",
                                2: "LIMIT_OPEN",
                                3: "STOP_OPEN",
                                4: "TP_CLOSE",
                                5: "SL_CLOSE",
                                6: "LIQ_CLOSE",
                            }
                
                event = limitex_event
                args = limitex_event['args']

                address = args['t']['user'].lower()
    
                pair_index = args['t']['pairIndex']

                asset_price = args['t']['openPrice'] / 1e10      #This price equal to price in opening trades. basically we can use it for closing trades as it helps to get the quantity which was originally bought.
                new_leads_leverage = args['t']['leverage'] / 1e3

                collateralIndex = args['t']['collateralIndex']

                collateral = collateral_map.get(collateralIndex, ["UNKNOWN", 0])
                collateral_token = collateral[0]

                new_leads_leverage = args['t']['leverage'] / 1e3
                collateralAmount_raw = args['t']['collateralAmount']
                collateralAmount = args['t']['collateralAmount'] / 10**(collateral[1])
                collateralPriceUsd =  args['collateralPriceUsd'] / 1e8    #(confirmed)
                
                collateral_usd_volume = collateralAmount * collateralPriceUsd
                
                transaction_amount = collateral_usd_volume * new_leads_leverage

                if collateralIndex == 2: # it is ETH
                    fake_collateral_token_price = 3200
                else:
                    fake_collateral_token_price = 1

                fake_transaction_amount = collateralAmount * fake_collateral_token_price * new_leads_leverage
                transaction_quantity = fake_transaction_amount / asset_price   # We use fake price so that the values become nearly close to the actual quantity and is fixed always. If we use actual collateral token price, the transaction amount during closing may be different form when we bought and the transaction amount will change, subsequesntly (transaction_quantity = transaction_amount/asset_price) this changes, which is wrong, as in gains transaction quantity during opening adn closing are same.

                coin_data = self.contract.functions.pairs(pair_index).call() 
                is_usd = coin_data[1] == "USD" and coin_data[0] is not None

                coin = coin_data[0]

                position_side = 'LONG' if args['t']['long'] else 'SHORT'

                blockNumber =  limitex_event['blockNumber']

                orderType_enum = args["orderType"]

                trade_side = orderType_map.get(orderType_enum, "UNKNOWN")

                order_type = get_order_type_category(trade_side)

                event_data = {
                    'event': event,
                    'order_type': order_type,
                    'position_side': position_side,
                    'trade_type': trade_side,
                    'trade_type_enum': orderType_enum,
                    'address': address,
                    'coin':coin,
                    'coin_data': coin_data[0:2],
                    'collateral_token': f"{collateral_token} ({collateralIndex})",
                    'asset_price': asset_price,
                    'collateral_usd_volume': collateral_usd_volume,
                    'transaction_amount': transaction_amount,
                    'transaction_quantity': transaction_quantity,
                    'new_leads_leverage': new_leads_leverage,
                    'blockNumber': blockNumber,
                }

                if collateral_token == 'UNKNOWN':
                    print("UNKOWN Collateral Token Appeared. Not adding the event into list for processing.")
                    continue

                # Check if trade is in USD or not
                if is_usd:
                    self.events_list.append(event_data)


            # Sort events list by orderId
            self.events_list.sort(key=lambda x: x['blockNumber'])


            # Main loop in which trades are processed
            for event in self.events_list:

                if event['address'].lower in self.traders_list['account'].values:

                    try:
                        if os.path.exists(stop_signal_path):
                            with open(stop_signal_path, "r") as file:
                                stop_signal = file.read().strip()
                        else:
                            stop_signal = ""
                    except:
                        stop_signal = ""

                    if event["order_type"]== "OPEN":
                        if stop_signal != "STOP":
                            
                            print("\n\n")

                            position_side = event['position_side']
                            address = event['address']
                            coin = event['coin']
                            asset_price = event['asset_price']
                            transaction_amount = event['transaction_amount']
                            transaction_quantity = event['transaction_quantity']
                            new_leads_leverage = event['new_leads_leverage']
                            
                            for key, value in event.items():
                                print(f'{key}: {value}')

                            #Symbol
                            symbol = coin + "USDT"
                            # Checking if banned
                            if self.trade.is_position_banned(address, symbol, position_side):
                                print("--Banned position, rejecting further processing--")
                                continue

                            # Checking if the parameters are valid
                            if transaction_quantity!= 0:
                                try:
                                    self.trade.ultimate_openTrade(self.client, self.traders_list, address, coin, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage)
                                except Exception as e: 
                                    print(f"Exception happened while OPEN trade.\nException: {traceback.format_exc()}\n\n")
                                    content = f"Exception happened while OPEN trade.\n\nPosition Side: {position_side}\nAddress: {address}\nCoin: {coin}\nAsset Price: {asset_price}\nTransaction Amount: {transaction_amount}\nTransaction Quantity: {transaction_quantity}\nNew Leads Leverage: {new_leads_leverage}\nException: {traceback.format_exc()}\n\n"
                                    self.trade.send_message("ALERT", content)
                                    continue

                            else:
                                print("Trade transaction_quantity = 0, rejecting trade.")
                                continue

                        else:
                            print(f"\n\n\n\n\n---------------** STOP ** Signal Received. Rejecting: OPEN TRADE.---------------\n\n\n\n\n")


                    elif event["order_type"]== "CLOSE":

                        print("\n\n")

                        position_side = event['position_side']
                        address = event['address']
                        coin = event['coin']
                        asset_price = event['asset_price']
                        transaction_amount = event['transaction_amount']
                        transaction_quantity = event['transaction_quantity']
                        new_leads_leverage = event['new_leads_leverage']
                        
                        for key, value in event.items():
                            print(f'{key}: {value}')

                        #Symbol
                        symbol = coin + "USDT"
                        # Checking if banned
                        if self.trade.is_position_banned(address, symbol, position_side):
                            print("--Banned position, rejecting further processing--")
                            continue
                        # Checking if the parameters are valid
                        if transaction_quantity!= 0:
                            try:
                                self.trade.ultimate_closeTrade(self.client, self.traders_list, address, coin, position_side, asset_price, transaction_amount, transaction_quantity, new_leads_leverage)
                            except Exception as e: 
                                print(f"Exception happened while CLOSE trade.\nException: {traceback.format_exc()}\n\n")
                                content = f"Exception happened while CLOSE trade.\n\nPosition Side: {position_side}\nAddress: {address}\nCoin: {coin}\nAsset Price: {asset_price}\nTransaction Amount: {transaction_amount}\nTransaction Quantity: {transaction_quantity}\nNew Leads Leverage: {new_leads_leverage}\nException: {traceback.format_exc()}\n\n"
                                self.trade.send_message("ALERT", content)
                                continue

                        else:
                            print("Trade transaction_quantity = 0, rejecting trade.")
                            continue


                    elif event["order_type"]== "LIQUIDATED":
                        
                        print("\n\n")
                        position_side = event['position_side']
                        address = event['address']
                        coin = event['coin']
                        asset_price = event['asset_price']
                        transaction_amount = event['transaction_amount']
                        transaction_quantity = event['transaction_quantity']
                        new_leads_leverage = event['new_leads_leverage']
                        
                        for key, value in event.items():
                            print(f'{key}: {value}')

                        #Symbol
                        symbol = coin + "USDT"
                        # Checking if banned
                        if self.trade.is_position_banned(address, symbol, position_side):
                            print("--Banned position, rejecting further processing--")
                            continue

                        try:
                            self.trade.ultimate_liquidateTrade(self.client, address, coin, position_side)
                        except Exception as e: 
                            print(f"Exception happened while LIQUIDATE trade.\nException: {traceback.format_exc()}\n\n")
                            content = f"Exception happened while LIQUIDATE trade.\n\nPosition Side: {position_side}\nAddress: {address}\nCoin: {coin}\nException: {traceback.format_exc()}\n\n"
                            self.trade.send_message("ALERT", content)
                            continue


                    else:
                        print("\n\n")
                        content = f"----UNKNOWN order_type occoured out of open close liquidated in GAINS, so rejecting the trade.----\nevent: {event}"
                        for key, value in event.items():
                            print(f'{key}: {value}')      
                        self.trade.send_message("ALERT", content)
                        print("----UNKNOWN order_type occoured, so rejecting the trade.----")
                        continue



            # # #Checking older stop_loss orders status.
            self.trade.check_last_stop_loss_order_id_status(self.client, trading_data_df)

            global trading_data_df_length_stored  # Access the global variable
            current_length = len(trading_data_df)
            if current_length != trading_data_df_length_stored:
                trading_data_df_length_stored = current_length
                self.trade.get_and_upload_open_positions_to_sheets()
                print(f"Executed get_and_upload_open_positions_to_sheets.")
            else:
                pass


            # Check if the current time is 6 PM and the email has not been sent today or last_email_sent_date is None or older than today
            global last_email_sent_date
            now_str = self.trade.get_current_time()
            now = datetime.strptime(now_str, "%H:%M:%S %d %B %Y")
            if now.hour == summary_sending_hour and (last_email_sent_date is None or last_email_sent_date < now.date()):
                self.trade.get_summary_and_send_email()

            time.sleep(0.5) #This is to decrease the alchemy url usage

#binance testnet API. here own binance API can be added from binance future testnet . this is for testing purpose
binance_api = "ff13435846836cbc93bfb350774608416375ca47994d39f734692ae0788c08fc"
binance_secret = "ae7c720857c6bedec60d55fabe487901d0c3cf55b0315d0cbeeedf591d04f40f"
# binance_api = "UvsLH9YOdEZJnk6yEyceDhMQIHAIhV1C1BEMI37GfXGU2y81MD55ic4E9D0iaUns"      these are mainnet API
# binance_secret = "RzgGyPV59iejem1y10PghWrMtsfBIfNHqaRAv2oh2VxxjBxPSsqfJZM0CtM3Uspj"
dots = 0
# Initialize the Binance client instance
while True:
    try:
        client = Client(binance_api, binance_secret, testnet=True)  #testnet= True is added if running in testnet account otherwise it will be removed.
        print("\nConnected")
        break
    except:
        message = f"Not Connected{'.' * dots}"
        print(f"\r{message:<20}", end="", flush=True)  # Add padding to ensure overwriting
        # Increase the number of dots, resetting after 3
        dots = (dots + 1) % 4




# Open a file for writing both stdout and stderr
log_filename = f"{DEX[0]}_log.txt"
log_file = open(log_filename, 'a', buffering=1)
sys.stdout = sys.stderr = log_file


xyz = Trading_Things()
try:
    # Main code
    print(f"\n\n\n\n--------------------------------------{DEX[0]}-Program Starting Time: {xyz.get_current_time()}--------------------------------------\n")

    livePositionExtractiontest(proxy_contract, client, traders_list).loop()

except Exception as e:
    # Capture any unhandled exceptions and write to log
    print(f"\n\n\n----Exception occurred outside the loop at {xyz.get_current_time()}----\n")
    traceback.print_exc()

    content = f"Exception occurred outside the loop in {DEX[0]} at {xyz.get_current_time()}\nException: {traceback.format_exc()}"
    xyz.send_message("CRASHED", content)

finally:
    # Close the log file
    log_file.flush()
    log_file.close()
