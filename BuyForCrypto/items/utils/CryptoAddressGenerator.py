from bip_utils import Bip44Changes, Bip44Coins, Bip44, Bip39SeedGenerator, Bip84, Bip84Coins

class CryptoAddressGenerator:
    def __init__(self, seed: str = 'cloud broom leaf moment apple advance vocal fence envelope word arm ten hen struggle giant'):
        self.seed_bytes = Bip39SeedGenerator(seed).Generate()

    def __generate_btc_address(self, i: int):
        bip84_mst_ctx = Bip84.FromSeed(self.seed_bytes, Bip84Coins.BITCOIN)
        bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0)
        bip84_chg_ctx = bip84_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip84_addr_ctx = bip84_chg_ctx.AddressIndex(i).PublicKey().ToAddress()
        return bip84_addr_ctx

    def __generate_ltc_address(self, i: int):
        bip44_mst_ctx = Bip44.FromSeed(self.seed_bytes, Bip44Coins.LITECOIN)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i).PublicKey().ToAddress()
        return bip44_addr_ctx

    def __generate_trx_address(self, i: int):
        bip44_mst_ctx = Bip44.FromSeed(self.seed_bytes, Bip44Coins.TRON)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i).PublicKey().ToAddress()
        return bip44_addr_ctx
    def get_addresses(self, i):
        return {'btc': self.__generate_btc_address(i),
                'ltc': self.__generate_ltc_address(i),
                'trx': self.__generate_trx_address(i)}
