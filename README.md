# Ethereum Wallet Creator

This Python script automates the creation of Ethereum wallets, checks their balances, and performs actions based on the balance. If a new wallet has a non-zero balance, the script sends an email to an administrator and saves the wallet's details to a text file. The script also sends an hourly email with the count of wallets created within the last hour.

## Features

- **Wallet Creation**: Automatically generates Ethereum wallets.
- **Balance Check**: Checks and reports the balance of each newly created wallet.
- **Email Notifications**: Sends an email if the wallet has a non-zero balance and hourly updates on the number of wallets created.
- **Logging**: Saves the wallet address and private key to a text file for later use.

## Prerequisites

Before you can use this script, you need to have the following installed:

- Python 3.6 or higher
- `web3` Python library
- `aiohttp` Python library for asynchronous HTTP requests (if applicable)

You also need to have access to an Ethereum node. This can be done through services like Infura.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ethereum-wallet-creator.git
   cd ethereum-wallet-creator
2. **Install Required Libraries**:
   ```bash
   pip install web3 aiohttp
   

## Usage

To run the script, execute the following command in the terminal:
    ```bash
    python wallet.py