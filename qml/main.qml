import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 600
    title: "Option Writer"
    color: "#f8f9fa"

    // Set application icon
    Component.onCompleted: {
        window.icon.source = "qrc:/logo.png"
    }

    ScrollView {
        id: scrollView
        anchors.fill: parent
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: Math.min(parent.width, 1200)
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 0

            // Header
            Text {
                text: "Option Writer"
                font.pixelSize: 28
                font.weight: Font.Bold
                color: "#212529"
                Layout.topMargin: 16
                Layout.bottomMargin: 8
                Layout.alignment: Qt.AlignHCenter
            }

            // Description
            Text {
                text: "Enter a stock ticker to find the best option writing opportunities"
                font.pixelSize: 14
                color: "#6c757d"
                Layout.alignment: Qt.AlignHCenter
                Layout.bottomMargin: 24
            }

            // Criteria and Analysis Section
            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 120
                Layout.maximumHeight: 180
                Layout.margins: 16
                color: "#f8f9fa"
                radius: 4

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 24

                    // Option Criteria Column
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 4

                        Text {
                            text: "Option Writing Criteria"
                            font.pixelSize: 14
                            font.weight: Font.Bold
                            color: "#212529"
                        }

                        Text {
                            text: "• Delta: 0.2 - 0.3\n• IV Rank > 50\n• IV/HV > 1.0\n• Exp: 30-45 days"
                            font.pixelSize: 12
                            color: "#495057"
                            Layout.fillWidth: true
                        }
                    }

                    // Technical Analysis Column
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 4

                        Text {
                            text: "Technical Analysis"
                            font.pixelSize: 14
                            font.weight: Font.Bold
                            color: "#212529"
                        }

                        Text {
                            text: "• EMAs: 10, 20, 50 days\n• RSI(14): <40 Bear, >60 Bull\n• BB Position vs Middle\n• Price vs 20-day EMA"
                            font.pixelSize: 12
                            color: "#495057"
                            Layout.fillWidth: true
                        }
                    }

                    // Strategy Selection Column
                    ColumnLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        spacing: 4

                        Text {
                            text: "Strategy Selection"
                            font.pixelSize: 14
                            font.weight: Font.Bold
                            color: "#212529"
                        }

                        Text {
                            text: "• Bearish (RSI<40): Covered Calls\n• Bullish (RSI>60): Cash Puts\n• Price vs 20-EMA\n• Confirm with BB Position"
                            font.pixelSize: 12
                            color: "#495057"
                            Layout.fillWidth: true
                        }
                    }
                }
            }

            // Search Box
            RowLayout {
                Layout.fillWidth: true
                Layout.margins: 16
                spacing: 16

                TextField {
                    id: tickerInput
                    Layout.fillWidth: true
                    placeholderText: "Enter a stock ticker to find the best option writing opportunities"
                    font.pixelSize: 14
                    color: "#212529"
                    background: Rectangle {
                        color: "#ffffff"
                        radius: 4
                        border.width: 1
                        border.color: parent.focus ? "#0d6efd" : "#dee2e6"
                    }
                }

                Button {
                    text: "Analyze"
                    font.pixelSize: 14
                    Layout.preferredWidth: 100
                    Layout.preferredHeight: tickerInput.height

                    background: Rectangle {
                        color: parent.down ? "#0b5ed7" : "#0d6efd"
                        radius: 4
                    }

                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    onClicked: {
                        resultsArea.visible = false
                        backend.analyze_ticker(tickerInput.text)
                    }
                }
            }

            // Loading Indicator
            BusyIndicator {
                id: busyIndicator
                running: false
                Layout.alignment: Qt.AlignHCenter
                visible: running
                Layout.topMargin: 16
            }

            // Results Area
            ColumnLayout {
                id: resultsArea
                Layout.fillWidth: true
                Layout.preferredWidth: Math.min(parent.width * 0.9, 800)
                Layout.alignment: Qt.AlignHCenter
                Layout.margins: 16
                visible: false
                spacing: 24

                Text {
                    text: "Final Recommendation"
                    font.pixelSize: Math.max(16, Math.min(24, parent.width / 30))
                    font.weight: Font.Bold
                    color: "#212529"
                    Layout.alignment: Qt.AlignHCenter
                }

                // Trend Analysis Text
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    color: "#f8f9fa"
                    radius: 4
                    
                    Text {
                        anchors.centerIn: parent
                        text: "Market Analysis: " + (backend.option_type === "Sell Call" ? 
                              "Bearish trend detected - Selling Covered Calls recommended" :
                              "Bullish trend detected - Selling Cash Secured Puts recommended")
                        font.pixelSize: Math.max(12, Math.min(16, parent.width / 40))
                        color: "#212529"
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                // Results Grid
                GridLayout {
                    Layout.fillWidth: true
                    Layout.preferredWidth: Math.min(parent.width, 600)
                    Layout.alignment: Qt.AlignHCenter
                    columns: {
                        if (parent.width < 500) return 2
                        return 4
                    }
                    rowSpacing: 16
                    columnSpacing: 24

                    // Headers
                    Rectangle {
                        Layout.columnSpan: parent.width < 500 ? 2 : 2
                        Layout.fillWidth: true
                        color: "#f8f9fa"
                        height: 40
                        radius: 4

                        Text {
                            anchors.centerIn: parent
                            text: "Basic Information"
                            font.pixelSize: Math.max(12, Math.min(16, parent.width / 40))
                            font.weight: Font.Bold
                            color: "#212529"
                        }
                    }

                    Rectangle {
                        Layout.columnSpan: parent.width < 500 ? 2 : 2
                        Layout.fillWidth: true
                        color: "#f8f9fa"
                        height: 40
                        radius: 4

                        Text {
                            anchors.centerIn: parent
                            text: "Analysis Metrics"
                            font.pixelSize: Math.max(12, Math.min(16, parent.width / 40))
                            font.weight: Font.Bold
                            color: "#212529"
                        }
                    }

                    // Content remains the same but with adaptive font sizes
                    Text {
                        text: "Option Type"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.option_type
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Implied Volatility"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.implied_volatility
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Strike Price"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.strike_price
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "IV Rank"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.iv_rank
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Expiration Date"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.expiration
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "IV/HV Ratio"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.iv_hv_ratio
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Premium"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.premium
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Win Rate"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.win_rate
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Delta"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.delta
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Take Profit"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.take_profit
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }

                    Text {
                        text: "Stop Loss"
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        font.weight: Font.Bold
                        color: "#212529"
                    }
                    Text {
                        text: backend.stop_loss
                        font.pixelSize: Math.max(12, Math.min(14, parent.width / 45))
                        color: "#495057"
                    }
                }
            }

            // Connect signals
            Connections {
                target: backend
                function onRecommendationChanged() {
                    console.log("QML: Recommendation changed signal received")
                    console.log("QML: Strike price: " + backend.strike_price)
                    console.log("QML: Premium: " + backend.premium)
                    console.log("QML: Delta: " + backend.delta)
                    console.log("QML: IV Rank: " + backend.iv_rank)
                    busyIndicator.running = false
                    resultsArea.visible = true
                }
            }
        }
    }
}
