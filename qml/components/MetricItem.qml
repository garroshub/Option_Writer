import QtQuick
import QtQuick.Layouts

RowLayout {
    property string label: ""
    property string value: ""
    spacing: 10

    Text {
        text: label + ":"
        color: "#7f8c8d"
        font.pixelSize: 14
    }

    Text {
        text: value
        color: "#2c3e50"
        font.pixelSize: 14
        font.weight: Font.Medium
    }
}
