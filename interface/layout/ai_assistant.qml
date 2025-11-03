import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: aiRoot
    width: 700
    height: 500

    Rectangle { anchors.fill: parent; color: theme.background }

    Column { anchors.fill: parent; anchors.margins: 12; spacing: 8
        Text { text: "DEX Assistant"; font.family: theme.font; color: theme.accent }

        ListView {
            id: convoList
            model: ctrl.aiConversation
            anchors.fill: parent
            delegate: Column { spacing: 4
                Text { text: model.role + ":"; font.family: theme.font; color: theme.muted }
                Text { text: model.text; wrapMode: Text.Wrap; font.family: theme.font; color: theme.text }
            }
        }

        Row { spacing: 8
            TextField { id: userInput; placeholderText: "Ask DEX..."; font.family: theme.font }
            Button { text: "Send"; onClicked: ctrl.sendMessage(userInput.text); userInput.text = "" }
        }
    }
}