import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: desktop
    width: 1920
    height: 1080
    color: "#101010"

    Text {
        text: "Welcome to DEX OS Layer"
        color: "cyan"
        anchors.centerIn: parent
        font.pixelSize: 48
    }

    Button {
        id: startButton
        text: "Launch Terminal"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 20
        onClicked: {
            console.log("Launching DEX Terminal...")
        }
    }
}