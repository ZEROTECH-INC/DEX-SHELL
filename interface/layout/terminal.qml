import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12

Item {
    id: terminalRoot
    width: 800
    height: 480

    Rectangle {
        id: bg
        anchors.fill: parent
        color: theme.background
    }

    Column {
        anchors.fill: parent
        spacing: 8
        padding: 12

        Text {
            id: title
            text: "DEX Terminal"
            font.family: theme.font
            font.pixelSize: 20
            color: theme.accent
        }

        Rectangle {
            id: console
            width: parent.width
            height: parent.height - title.height - 40
            color: theme.panel
            radius: 6
            border.color: theme.glow ? theme.glow : theme.accent
            implicitHeight: 360

            Column {
                anchors.fill: parent
                spacing: 6
                padding: 8

                Flickable {
                    id: outputArea
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    contentWidth: parent.width
                    contentHeight: textContent.height
                    clip: true

                    Text {
                        id: textContent
                        text: ctrl.consoleText
                        wrapMode: Text.NoWrap
                        font.family: theme.font
                        color: theme.text
                    }
                }

                Row {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    spacing: 8

                    TextField {
                        id: inputLine
                        placeholderText: "Type a command or ask DEX..."
                        font.family: theme.font
                        onAccepted: {
                            ctrl.handleCommand(text)
                            text = ""
                        }
                    }

                    Button {
                        text: "Run"
                        onClicked: {
                            ctrl.handleCommand(inputLine.text)
                            inputLine.text = ""
                        }
                    }
                }
            }
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: t
    anchors.fill: parent
    color: "transparent"

    property alias consoleText: consoleTextArea.text

    ScrollView {
        anchors.fill: parent
        Rectangle {
            width: parent.width
            height: parent.height
            color: "transparent"

            TextArea {
                id: consoleTextArea
                anchors.fill: parent
                readOnly: false
                wrapMode: TextEdit.NoWrap
                font.family: "JetBrains Mono"
                font.pixelSize: 14
                color: "#bfefff"
                background: Rectangle { color: "transparent" }
                text: "Welcome to DEX Terminal...\n"
            }
        }
    }

    Row {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        spacing: 8
        TextField {
            id: cmdInput
            anchors.left: parent.left
            anchors.margins: 12
            placeholderText: "Type a command (e.g. help)"
            onAccepted: {
                consoleTextArea.text += "\\n> " + text + "\\n"
                // send to ctrl (if bound)
                if (typeof ctrl !== 'undefined') ctrl.handleCommand(text)
                text = ""
                // scroll bottom
                consoleTextArea.forceActiveFocus()
            }
        }
        Button { text: "Send"; onClicked: cmdInput.onAccepted() }
    }
}