import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: window
    width: 1280
    height: 720
    visible: true
    title: "DEX Shell - Interface Preview"

    Rectangle {
        anchors.fill: parent
        color: "#0b0f14"

        Column {
            anchors.fill: parent
            anchors.margins: 24
            spacing: 12

            Text {
                text: "DEX Shell (Interface Preview)"
                font.pixelSize: 28
                color: "#e6eef8"
            }

            Rectangle {
                id: termArea
                width: parent.width
                height: parent.height - 120
                color: "#071019"
                radius: 6
                border.color: "#12212b"
                border.width: 1

                TextArea {
                    id: console
                    anchors.fill: parent
                    wrapMode: TextArea.Wrap
                    readOnly: true
                    font.family: "JetBrains Mono"
                    font.pixelSize: 14
                    color: "#cfe8ff"
                    text: "Connecting to local DEX Core API...\n"
                }
            }

            Row {
                spacing: 8
                TextField {
                    id: input
                    placeholderText: "Type command or perform gesture..."
                    width: parent.width - 120
                    height: 36
                    font.pixelSize: 14
                }
                Button {
                    text: "Send"
                    onClicked: {
                        console.append("> " + input.text + "\n")
                        input.text = ""
                    }
                }
            }
        }
    }
}
