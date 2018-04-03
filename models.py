from scorum.constants import Method


class StatusCodeError(Exception):
    pass


class Request:
    def __init__(self, params: list, method: str = Method.CALL,
                 id: int = 0, jsonrpc: str = "2.0"):
        self.params = params
        self.method = method
        self.id = id
        self.jsonrpc = jsonrpc


class BlockResponse:
    def __init__(self, id: int, result: dict):
        self.id = id
        self.result = self.Result(**result) if result else None

    class Result:
        def __init__(self, previous: str, timestamp: str,
                     witness: str, transaction_merkle_root: str,
                     extensions: list, witness_signature: str,
                     transactions: list, block_id: str,
                     signing_key: str, transaction_ids: list):
            self.previous = previous
            self.timestamp = timestamp
            self.witness = witness
            self.transaction_merkle_root = transaction_merkle_root
            self.extensions = extensions
            self.witness_signature = witness_signature
            self.transactions = transactions
            self.block_id = block_id
            self.signing_key = signing_key
            self.transaction_ids = transaction_ids


class DynamicGlobalPropertiesResponse:
    def __init__(self, id: int, result: dict):
        self.id = id
        self.result = self.Result(**result)

    class Result:
        def __init__(self, id: int, head_block_number: int,
                     head_block_id: int, time: str,
                     current_witness: str, total_supply: str,
                     circulating_capital: str, total_scorumpower: str,
                     median_chain_props: dict, majority_version: str,
                     current_aslot: int, recent_slots_filled: str,
                     participation_count: int, last_irreversible_block_num: int,
                     vote_power_reserve_rate: int, average_block_size: int,
                     current_reserve_ratio: int, max_virtual_bandwidth: str,
                     registration_pool_balance: str, fund_budget_balance: str,
                     reward_pool_balance: str, content_reward_balance: str
                     ):
            self.id = id
            self.head_block_number = head_block_number
            self.head_block_id = head_block_id
            self.time = time
            self.current_witness = current_witness
            self.total_supply = total_supply
            self.circulating_capital = circulating_capital
            self.total_scorumpower = total_scorumpower
            self.median_chain_props = self.MedianChainProps(**median_chain_props)
            self.majority_version = majority_version
            self.current_aslot = current_aslot
            self.recent_slots_filled = recent_slots_filled
            self.participation_count = participation_count
            self.last_irreversible_block_num = last_irreversible_block_num
            self.vote_power_reserve_rate = vote_power_reserve_rate
            self.average_block_size = average_block_size
            self.current_reserve_ratio = current_reserve_ratio
            self.max_virtual_bandwidth = max_virtual_bandwidth
            self.registration_pool_balance = registration_pool_balance
            self.fund_budget_balance = fund_budget_balance
            self.reward_pool_balance = reward_pool_balance
            self.content_reward_balance = content_reward_balance

        class MedianChainProps:
            def __init__(self, account_creation_fee: str, maximum_block_size: str):
                self.account_creation_fee: account_creation_fee
                self.maximum_block_size: maximum_block_size

