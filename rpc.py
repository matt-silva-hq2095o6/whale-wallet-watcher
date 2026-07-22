import httpx

class RPCError(Exception):
    """Raised when JSON-RPC returns an error response."""
    pass

class RPCClient:
    """Direct EVM JSON-RPC client."""
    def __init__(self, rpc_url: str):
        self.url = rpc_url
        self._id = 0

    def _call(self, method: str, params: list) -> dict:
        self._id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._id
        }
        # Some RPC nodes fail with short timeouts on eth_getLogs
        response = httpx.post(self.url, json=payload, timeout=25.0)
        response.raise_for_status()
        res_json = response.json()
        if "error" in res_json:
            raise RPCError(res_json["error"].get("message", "Unknown RPC error"))
        return res_json.get("result")

    def get_latest_block(self) -> int:
        res = self._call("eth_blockNumber", [])
        return int(res, 16)

    def get_block(self, number: int) -> dict:
        # hex() adds 0x prefix automatically
        hex_num = hex(number)
        res = self._call("eth_getBlockByNumber", [hex_num, True])
        if not res:
            return {}
        return res

    def get_erc20_transfers(self, block_number: int) -> list:
        hex_num = hex(block_number)
        # Topic 0 for Transfer(address,address,uint256)
        transfer_sig = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        
        params = {
            "fromBlock": hex_num,
            "toBlock": hex_num,
            "topics": [transfer_sig]
        }
        
        logs = self._call("eth_getLogs", [params])
        if not logs:
            return []
            
        transfers = []
        for log in logs:
            topics = log.get("topics", [])
            # A valid ERC20 transfer must have 3 topics (sig, from, to)
            # Some anonymous transfer events can have fewer topics, we skip those
            if len(topics) < 3:
                continue
            
            # debug print left for local parsing inspection
            # print(f"Processing log: {log['transactionHash']}")
            
            from_addr = "0x" + topics[1][-40:]
            to_addr = "0x" + topics[2][-40:]
            
            data = log.get("data", "")
            if not data or data == "0x":
                amount = 0
            else:
                amount = int(data, 16)
                
            transfers.append({
                "token": log.get("address", "").lower(),
                "from": from_addr.lower(),
                "to": to_addr.lower(),
                "amount": amount,
                "tx_hash": log.get("transactionHash", "")
            })
        return transfers
