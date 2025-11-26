// chat.js
let currentChatId = null;

document.addEventListener('DOMContentLoaded', function() {
    const chatItems = document.querySelectorAll('.chat-item');
    const mainArea = document.getElementById('mainArea');
    const messagesContainer = document.getElementById('messagesContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    // Обработчики для чатов
    chatItems.forEach(function(chatItem) {
        chatItem.addEventListener('click', function() {
            const chatId = this.getAttribute('data-chat-id');
            const username = this.querySelector('.username').textContent;
            
            openChat(chatId, username);
        });
    });

    // Обработчик отправки сообщения
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function openChat(chatId, username) {
        currentChatId = chatId;
        
        // Показываем основную область
        mainArea.style.display = 'block';
        
        // Загружаем сообщения
        loadMessages(chatId);
        
        // Можно добавить заголовок с именем пользователя
        console.log('Открыт чат с:', username, 'ID:', chatId);
    }

    function loadMessages(chatId) {
        fetch(`/get_messages/${chatId}`)
            .then(response => response.json())
            .then(messages => {
                displayMessages(messages);
            })
            .catch(error => {
                console.error('Ошибка загрузки сообщений:', error);
            });
    }

    function displayMessages(messages) {
        messagesContainer.innerHTML = '';
        
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = 'message';
            messageElement.innerHTML = `
                <div class="message-sender">${message.sender}</div>
                <div class="message-text">${message.text}</div>
                <div class="message-time">${message.time}</div>
            `;
            messagesContainer.appendChild(messageElement);
        });
        
        // Прокрутка вниз
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendMessage() {
        const messageText = messageInput.value.trim();
        
        if (!messageText || !currentChatId) {
            return;
        }

        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat_id: currentChatId,
                message: messageText
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                messageInput.value = '';
                // Перезагружаем сообщения
                loadMessages(currentChatId);
            }
        })
        .catch(error => {
            console.error('Ошибка отправки сообщения:', error);
        });
    }
});