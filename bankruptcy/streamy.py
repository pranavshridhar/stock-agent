import streamlit as st
from web3 import Web3

# Connect to local or testnet node (use Infura/Alchemy for live)
web3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/YOUR_API_KEY"))

# Load ABI and contract
with open("InvestmentSignals_abi.json") as f:
    abi = f.read()

contract_address = "0xYourDeployedContractAddress"
contract = web3.eth.contract(address=contract_address, abi=abi)

st.title("📊 AI On-Chain Investment Signals")

signal_count = contract.functions.getSignalCount().call()
st.write(f"📦 Total Signals Logged: {signal_count}")

for i in reversed(range(signal_count)):
    symbol, decision, timestamp = contract.functions.getSignal(i).call()
    st.markdown(f"**{symbol}** → `{decision}` at ⏱️ {timestamp}")