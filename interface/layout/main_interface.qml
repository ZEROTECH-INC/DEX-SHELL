import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.15

Window {
    id: root
    width: 1280
    height: 720
    visible: true
    color: "#07070a"
    title: "DEX Shell - Cognitive Kernel"

    // Background shader
    Item {
        id: bg
        anchors.fill: parent

        ShaderEffect {
            id: neonBg
            anchors.fill: parent
            property real time: Qt.formatDateTime(new Date(), "hhmmss").toInt()   // trivial time prop
            fragmentShader: Qt.resolvedUrl("../shaders/neon_effect.glsl")
        }
    }

    Row {
        anchors.fill: parent
        spacing: 12
        anchors.margins: 16

        // Left: Terminal panel
        Rectangle {
            id: terminalPanel
            width: parent.width * 0.62
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            radius: 10
            color: "#020213aa"
            border.color: "#00ffff22"
            border.width: 1
            column: Column { }

            // Title
            Row {
                spacing: 8
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 12
                Text { text: "Terminal"; color: "#cfeeee"; font.pixelSize: 16 }
            }

            // Terminal loader
            Loader {
                id: termLoader
                anchors.top: parent.top
                anchors.topMargin: 48
                anchors.left: parent.left
                anchors.right: parent.right
                source: Qt.resolvedUrl("terminal.qml")
            }
        }

        // Right: Dashboard + controls
        Column {
            width: parent.width * 0.36
            spacing: 12

            Rectangle {
                id: dash
                height: parent.height * 0.5
                radius: 10
                color: "#020213cc"
                border.color: "#00ffff22"
                border.width: 1

                Loader {
                    anchors.fill: parent
                    source: Qt.resolvedUrl("system_dashboard.qml")
                }
            }

            Rectangle {
                id: gestures
                height: parent.height * 0.48
                radius: 10
                color: "#020213cc"
                border.color: "#00ffff22"
                border.width: 1

                Loader {
                    anchors.fill: parent
                    source: Qt.resolvedUrl("gestures.qml")
                }
            }
        }
    }
}