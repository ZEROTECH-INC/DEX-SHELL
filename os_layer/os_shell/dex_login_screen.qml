import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: login
    width: 800
    height: 600
    color: "#0A0A0A"
    radius: 12
    border.color: "cyan"
    border.width: 2

    Text {
        text: "DEX Shell Login"
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20
        color: "cyan"
        font.pixelSize: 28
    }

    TextField {
        id: username
        placeholderText: "Username"
        anchors.centerIn: parent
        width: 300
    }

    Button {
        text: "Login"
        anchors.top: username.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20
        onClicked: console.log("User logged in as " + username.text)
    }
}