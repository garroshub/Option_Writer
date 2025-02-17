import unittest
from backend import OptionAnalyzer

class TestOptionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = OptionAnalyzer()

    def test_tsla_recommendation(self):
        print("\nTesting TSLA:")
        recommendation = self.analyzer.find_best_option("TSLA")
        self.assertIsNotNone(recommendation)
        print(f"\nRecommended Option: {recommendation.type} {recommendation.strike} @ {recommendation.expiration}")
        print(f"Implied Volatility: {recommendation.implied_volatility}%")
        print(f"IV Rank: {recommendation.iv_rank}")
        print(f"IV/HV Ratio: {recommendation.iv_hv_ratio}")
        print(f"Delta: {recommendation.delta}")
        print(f"Win Rate: {recommendation.win_rate}%")
        print(f"Take Profit: {recommendation.take_profit}")
        print(f"Stop Loss: {recommendation.stop_loss}")

    def test_msft_recommendation(self):
        print("\nTesting MSFT:")
        recommendation = self.analyzer.find_best_option("MSFT")
        self.assertIsNotNone(recommendation)
        print(f"\nRecommended Option: {recommendation.type} {recommendation.strike} @ {recommendation.expiration}")
        print(f"Implied Volatility: {recommendation.implied_volatility}%")
        print(f"IV Rank: {recommendation.iv_rank}")
        print(f"IV/HV Ratio: {recommendation.iv_hv_ratio}")
        print(f"Delta: {recommendation.delta}")
        print(f"Win Rate: {recommendation.win_rate}%")
        print(f"Take Profit: {recommendation.take_profit}")
        print(f"Stop Loss: {recommendation.stop_loss}")

    def test_meta_recommendation(self):
        print("\nTesting META:")
        recommendation = self.analyzer.find_best_option("META")
        self.assertIsNotNone(recommendation)
        print(f"\nRecommended Option: {recommendation.type} {recommendation.strike} @ {recommendation.expiration}")
        print(f"Implied Volatility: {recommendation.implied_volatility}%")
        print(f"IV Rank: {recommendation.iv_rank}")
        print(f"IV/HV Ratio: {recommendation.iv_hv_ratio}")
        print(f"Delta: {recommendation.delta}")
        print(f"Win Rate: {recommendation.win_rate}%")
        print(f"Take Profit: {recommendation.take_profit}")
        print(f"Stop Loss: {recommendation.stop_loss}")

if __name__ == '__main__':
    unittest.main()
