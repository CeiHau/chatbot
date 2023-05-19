class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox'),
            sendButton: document.querySelector('.send__button'),
            contextButton: document.querySelector('.set__button'),
        }

        this.state = false;
        this.messages = [];
        this.init()
    }

    init() {
        const {chatBox, sendButton, contextButton} = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        contextButton.addEventListener('click', () => this.onContextButton(chatBox))

    }


    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        console.log(textField.value)
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = {name: "User", message: text1, type: "message"}
        this.messages.push(msg1);
        //
        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = {name: "bot", message: r.answer};
                this.messages.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''

            }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.type === "context"){

            } else{
                if (item.name === "bot") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                } else {
                    html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                }
            }

        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    onContextButton(chatbox) {
        console.log('context button')
        var textField = chatbox.querySelectorAll('input')[1];
        console.log(textField.value)
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = {name: "user", message: text1, type:"context"}
        this.messages.push(msg1);
        //
        fetch('http://127.0.0.1:5000/context', {
            method: 'POST',
            body: JSON.stringify({context: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = {name: "bot", message: r.answer};
                this.messages.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''

            }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }
}

const chatbax = new Chatbox();
