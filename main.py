import sys
import os
from pathlib import Path
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer
from PySide6.QtGui import QGuiApplication
from backend import OptionAnalyzer, OptionRecommendation

class Backend(QObject):
    recommendationChanged = Signal()
    filterStatsChanged = Signal()
    hasRecommendationChanged = Signal()

    def __init__(self):
        super().__init__()
        self._analyzer = OptionAnalyzer()
        self._recommendation = None
        self._filter_stats = []
        self._has_recommendation = False
        
        # 显示属性
        self._option_type = ""
        self._strike_price = ""
        self._expiration = ""
        self._premium = ""
        self._delta = ""
        self._implied_volatility = ""
        self._iv_rank = ""
        self._iv_hv_ratio = ""
        self._win_rate = ""
        self._take_profit = ""
        self._stop_loss = ""

    @Property(bool, notify=hasRecommendationChanged)
    def has_recommendation(self):
        return self._has_recommendation

    @Property('QVariant', notify=recommendationChanged)
    def recommendation(self):
        return self._recommendation

    @Property('QVariant', notify=filterStatsChanged)
    def filter_stats(self):
        return self._filter_stats

    @Property(str, notify=recommendationChanged)
    def option_type(self):
        return self._option_type

    @Property(str, notify=recommendationChanged)
    def strike_price(self):
        return self._strike_price

    @Property(str, notify=recommendationChanged)
    def expiration(self):
        return self._expiration

    @Property(str, notify=recommendationChanged)
    def premium(self):
        return self._premium

    @Property(str, notify=recommendationChanged)
    def delta(self):
        return self._delta

    @Property(str, notify=recommendationChanged)
    def implied_volatility(self):
        return self._implied_volatility

    @Property(str, notify=recommendationChanged)
    def iv_rank(self):
        return self._iv_rank

    @Property(str, notify=recommendationChanged)
    def iv_hv_ratio(self):
        return self._iv_hv_ratio

    @Property(str, notify=recommendationChanged)
    def win_rate(self):
        return self._win_rate

    @Property(str, notify=recommendationChanged)
    def take_profit(self):
        return self._take_profit

    @Property(str, notify=recommendationChanged)
    def stop_loss(self):
        return self._stop_loss

    @Slot(str)
    def analyze_ticker(self, ticker):
        if not ticker:
            return

        try:
            recommendation = self._analyzer.find_best_option(ticker)
            
            if recommendation:
                print(f"Debug: Got recommendation for {ticker}")
                
                # 更新显示属性
                self._option_type = f"Sell {recommendation.type}"
                self._strike_price = f"${recommendation.strike:.2f}"
                self._expiration = recommendation.expiration
                self._premium = f"${recommendation.premium:.2f}"
                self._delta = f"{recommendation.delta:.2f}"
                self._implied_volatility = f"{recommendation.implied_volatility:.2f}%"
                self._iv_rank = f"{recommendation.iv_rank:.2f}%"
                self._iv_hv_ratio = f"{recommendation.iv_hv_ratio:.2f}"
                self._win_rate = f"{recommendation.win_rate:.2f}%"
                self._take_profit = f"${recommendation.take_profit:.2f}"
                self._stop_loss = f"${recommendation.stop_loss:.2f}"
                
                # 创建一个包含所有必要属性的字典
                self._recommendation = {
                    "type": recommendation.type,
                    "strike": f"{recommendation.strike:.2f}",
                    "expiration": recommendation.expiration,
                    "implied_volatility": f"{recommendation.implied_volatility:.2f}",
                    "iv_rank": f"{recommendation.iv_rank:.2f}",
                    "iv_hv_ratio": f"{recommendation.iv_hv_ratio:.2f}",
                    "delta": f"{recommendation.delta:.2f}",
                    "win_rate": f"{recommendation.win_rate:.2f}",
                    "take_profit": f"{recommendation.take_profit:.2f}",
                    "stop_loss": f"{recommendation.stop_loss:.2f}"
                }
                self._has_recommendation = True
                self._filter_stats = []
                
                self.recommendationChanged.emit()
                self.hasRecommendationChanged.emit()
                
                print("Debug: Updated all display properties")
            else:
                df = self._analyzer.get_option_data(ticker)
                df = self._analyzer.calculate_metrics(df, ticker)
                stats = self._analyzer.get_filter_stats(df)
                self._filter_stats = stats
                self._has_recommendation = False
                self._recommendation = None

            self.filterStatsChanged.emit()

        except Exception as e:
            print(f"Error analyzing ticker: {str(e)}")
            self._has_recommendation = False
            self._recommendation = None
            self.hasRecommendationChanged.emit()
            self.recommendationChanged.emit()

def main():
    print("Starting application...")
    app = QGuiApplication(sys.argv)
    
    # Create QML engine
    print("Creating QML engine...")
    engine = QQmlApplicationEngine()
    
    # Create and expose backend to QML
    print("Creating backend...")
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    
    # Load main QML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_file = os.path.join(current_dir, "qml", "main.qml")
    print(f"Loading QML file from: {qml_file}")
    
    if not os.path.exists(qml_file):
        print(f"Error: QML file not found at {qml_file}")
        sys.exit(1)
        
    engine.load(os.path.abspath(qml_file))
    
    if not engine.rootObjects():
        print("Error: Failed to load QML file")
        sys.exit(-1)
    
    print("Starting event loop...")    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
