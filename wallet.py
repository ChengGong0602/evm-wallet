import asyncio
from web3 import Web3
import smtplib
from email.message import EmailMessage
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Email settings (configure these properly)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
YOUR_INFURA_PROJECT_ID =  os.getenv('YOUR_INFURA_PROJECT_ID')

# Counter and list to track created wallets
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{YOUR_INFURA_PROJECT_ID}'))
count_wallets_created = 0


async def attempt_wallet_operations():
    global count_wallets_created  # Declare the use of the global variable
    while True:
        try:

            # Generate wallet
            acct = w3.eth.account.create()
            address = acct.address
            private_key = acct._private_key.hex()
            # Check balance
            balance = w3.eth.get_balance(address)
            if balance > 0:
                balance_in_ether = w3.from_wei(balance, 'ether')

                # Send email to admin
                await send_email(address, balance_in_ether)

                # Save wallet details
                save_wallet_details(address, private_key)
            count_wallets_created += 1
            print("Created wallet numbers:", count_wallets_created)
            # Break the loop if successful
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

async def hourly_update():
    global count_wallets_created

    while True:
        await asyncio.sleep(3600)  # Wait for one hour
        if count_wallets_created > 0:
            await send_email(str(count_wallets_created))

async def send_email(address,  balance=None):
    msg = EmailMessage()
    if balance is not None:
        msg.set_content(f'Wallet {address} has a balance of {balance} ETH.')
        msg['Subject'] = 'ETH Wallet Notification'
    else:
        msg.set_content(f'Number of wallets created in the last hour: {address}')
        msg['Subject'] = 'Hourly Wallet Creation Update'
    msg['From'] = SMTP_USERNAME
    msg['To'] = ADMIN_EMAIL

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    try:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
    finally:
        server.quit()

def save_wallet_details(address, private_key):
    with open('wallet_details.txt', 'a') as file:
        file.write(f'{address} {private_key}\n')

async def continuously_create_wallet():
    while True:
        start_time = time.time()
        await attempt_wallet_operations()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        print("Operation completed successfully. Starting again...")
        await asyncio.sleep(2)  # Pause for 10 seconds before starting the process again

async def main():
    wallet_task = asyncio.create_task(continuously_create_wallet())
    update_task = asyncio.create_task(hourly_update())
    await asyncio.gather(wallet_task, update_task)

if __name__ == '__main__':
    asyncio.run(main())
