import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12

Item {
    id: dashboardRoot
    width: 1000
    height: 600

    Rectangle { anchors.fill: parent; color: theme.background }

    Grid {
        id: grid
        columns: 3
        anchors.fill: parent
        anchors.margins: 16
        rowSpacing: 12
        columnSpacing: 12

        // System Stats Card
        Rectangle {
            color: theme.panel; radius: 8; border.color: theme.glow
            width: parent.width / 3 - 20; height: 200
            Column { anchors.fill: parent; anchors.margins: 12; spacing: 6
                Text { text: "System"; color: theme.accent; font.family: theme.font }
                Text { text: "CPU: " + ctrl.cpuUsage + "%"; color: theme.text; font.family: theme.font }
                Text { text: "Memory: " + ctrl.memUsage + "%"; color: theme.text; font.family: theme.font }
            }
        }

        // Plugins Card
        Rectangle {
            color: theme.panel; radius: 8; border.color: theme.glow
            width: parent.width / 3 - 20; height: 200
            Column { anchors.fill: parent; anchors.margins: 12; spacing: 6
                Text { text: "Plugins"; color: theme.accent; font.family: theme.font }
                Repeater { model: ctrl.plugins; delegate: Text { text: "- " + modelData; color: theme.text } }
            }
        }

        // AI Status Card
        Rectangle {
            color: theme.panel; radius: 8; border.color: theme.glow
            width: parent.width / 3 - 20; height: 200
            Column { anchors.fill: parent; anchors.margins: 12; spacing: 6
                Text { text: "AI"; color: theme.accent; font.family: theme.font }
                Text { text: "Model: " + ctrl.aiModel; color: theme.text }
                Text { text: "Status: " + ctrl.aiStatus; color: theme.text }
            }
        }
    }
}


import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    anchors.fill: parent

    Column {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        Text { text: "System Dashboard"; color: "#dff"; font.pixelSize: 16 }

        // Simple CPU / Memory placeholders
        Rectangle {
            height: 40; radius: 6; color: "#001016"
            Row { anchors.fill: parent; spacing: 12; anchors.margins: 8
                Text { text: "CPU: " }
                ProgressBar { id: cpuBar; value: 0.34; from: 0; to: 1; width: 200 }
                Text { text: Math.round(cpuBar.value*100) + "%" }
            }
        }

        Rectangle {
            height: 40; radius: 6; color: "#001016"
            Row { anchors.fill: parent; spacing: 12; anchors.margins: 8
                Text { text: "Memory: " }
                ProgressBar { id: memBar; value: 0.27; width: 200 }
                Text { text: Math.round(memBar.value*100) + "%" }
            }
        }

        Text { text: "Activity Log:"; color: "#9ff"; font.pixelSize: 12 }
        Rectangle {
            color: "#020213"
            radius: 6
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: parent.height - 140
            Text { text: "No recent events."; color: "#7ff"; anchors.margins: 8 }
        }
    }
}