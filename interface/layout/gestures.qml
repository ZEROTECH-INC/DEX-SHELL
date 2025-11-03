import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12

Item {
    id: gesturesRoot
    width: 600
    height: 400

    Rectangle {
        anchors.fill: parent
        color: theme.background
    }

    Column {
        anchors.centerIn: parent
        spacing: 12

        Text {
            text: "Gesture Map"
            font.family: theme.font
            font.pixelSize: 18
            color: theme.accent
        }

        Repeater {
            model: ctrl.gestureMap
            delegate: Row {
                spacing: 12
                Image { source: model.icon; width: 40; height: 40 }
                Column {
                    Text { text: model.name; font.family: theme.font; color: theme.text }
                    Text { text: model.desc; font.family: theme.font; color: theme.muted; font.pixelSize: 12 }
                }
            }
        }
    }
}



import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Shapes 1.15

Item {
    anchors.fill: parent

    Column {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8
        Text { text: "Gesture Monitor"; color: "#dff"; font.pixelSize: 16 }

        Rectangle {
            id: gestureArea
            anchors.left: parent.left
            anchors.right: parent.right
            height: parent.height - 60
            color: "#001018"
            radius: 8
            Text {
                anchors.centerIn: parent
                text: "No gesture detected"
                color: "#9ff"
            }
        }
    }
}