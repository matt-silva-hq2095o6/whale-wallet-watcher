# whale-wallet-watcher

A lightweight CLI utility to monitor high-value Ethereum/EVM addresses. It polls standard JSON-RPC nodes to track native coin (ETH/BNB/etc) and ERC-20 token transfers matching a watch list, dispatching alerts to Slack or Discord webhooks.

I built this because I wanted a self-hosted, dependency-light tracker that didn't require heavy SDKs, local node databases, or expensive third-party platform subscriptions.

## Installation

Clone the repository and install the single dependency:

```cmd
pip install -r requirements.txt
```

## Setup

Create a `wallets.json` file in the same directory to define the addresses you want to watch:

```json
{
  "0x742d35Cc6634C0532925a3b844Bc454e4438f44e": "Kraken Cold Wallet",
  "0x28C6c06298d514Db089934071355E5743bf21d60": "Binance Cold Wallet"
}
```

## Running

To run the watcher, point it to an RPC provider (like Cloudflare, Ankr, or your own local/infura node):

```cmd
python watcher.py --rpc https://cloudflare-eth.com --webhook https://discord.com/api/webhooks/... --threshold 10.0
```

Options:
* `--rpc`: The HTTP URL of the target EVM JSON-RPC node.
* `--webhook`: Discord or Slack webhook URL for alerts.
* `--threshold`: Minimum transfer volume in native coin to trigger an alert (defaults to 5.0).
* `--interval`: Poll interval in seconds (defaults to 12).
* `--state`: Path to the state file tracking the last processed block (defaults to `last_block.txt`).

<!-- last-checked: 2026-09-23 -->
