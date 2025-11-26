let currentChatId = null;
let currentChatUsername = null;
let currentUser = null; // Добавляем переменную для текущего пользователя

document.addEventListener('DOMContentLoaded', function() {
    // Получаем текущего пользователя из data-атрибута
    currentUser = document.getElementById('currentUser').getAttribute('data-username');
    
    const chatItems = document.querySelectorAll('.chat-item');
    const messagesContainer = document.getElementById('messagesContainer');
    const chatHeader = document.getElementById('chatHeader');
    const inputArea = document.getElementById('inputArea');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    console.log('Текущий пользователь:', currentUser); // Для отладки

    // Обработчики для чатов
    chatItems.forEach(function(chatItem) {
        chatItem.addEventListener('click', function() {
            // Убираем активный класс у всех чатов
            chatItems.forEach(item => item.classList.remove('active'));
            // Добавляем активный класс текущему чату
            this.classList.add('active');
            
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
        currentChatUsername = username;
        
        // Показываем заголовок чата
        chatHeader.innerHTML = `<div class="chat-title">Чат с ${username}</div>`;
        
        // Показываем поле ввода
        inputArea.classList.remove('hidden');
        
        // Загружаем сообщения
        loadMessages(chatId);
        
        // Фокусируемся на поле ввода
        messageInput.focus();
        
        console.log('Открыт чат с:', username, 'ID:', chatId);
    }

    function loadMessages(chatId) {
        fetch(`/get_messages/${chatId}`)
            .then(response => response.json())
            .then(messages => {
                // Если этот чат сейчас открыт - показываем сообщения
                if (chatId === currentChatId) {
                    displayMessages(messages);
                }
            })
            .catch(error => {
                console.error('Ошибка загрузки сообщений:', error);
            });
    }

    function displayMessages(messages) {
        messagesContainer.innerHTML = '';
        
        if (messages.length === 0) {
            messagesContainer.innerHTML = '<div class="no-messages">Нет сообщений</div>';
            return;
        }
        
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            
            // Определяем класс для сообщения (мое или чужое)
            const isMyMessage = message.sender === currentUser;
            const messageClass = isMyMessage ? 'message my' : 'message other';
            
            messageElement.className = messageClass;
            
            // Для своих сообщений не показываем отправителя, для чужих - показываем
            if (isMyMessage) {
                messageElement.innerHTML = `
                    <div class="message-text">${message.text}</div>
                    <div class="message-time">${message.time}</div>
                `;
            } else {
                messageElement.innerHTML = `
                    <div class="message-sender">${message.sender}</div>
                    <div class="message-text">${message.text}</div>
                    <div class="message-time">${message.time}</div>
                `;
            }
            
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
            } else {
                console.error('Ошибка отправки сообщения:', result.error);
            }
        })
        .catch(error => {
            console.error('Ошибка отправки сообщения:', error);
        });
    }

    // Автоматическое обновление сообщений каждые 2 секунды
    setInterval(function() {
        if (currentChatId) {
            loadMessages(currentChatId);
        }
    }, 500);
});