document.addEventListener("DOMContentLoaded", () => {
    const isLocalhost = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
    const WS_BASE_URL = isLocalhost ? "ws://127.0.0.1:8000" : "wss://sereniq-row2.onrender.com";

    const token = localStorage.getItem("sereniq_token");
    if (!token) {
        alert("You must be logged in to access the chat.");
        window.location.href = "sign_in.html";
        return;
    }

   
    let currentUserEmail = "";
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        currentUserEmail = payload.sub;
    } catch (e) {
        console.error("Invalid token format.");
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const chatPartnerEmail = urlParams.get('friend');

    if (!chatPartnerEmail) {
        alert("No friend selected to chat with!");
    }

    const formatName = (email) => {
        if (!email || !email.includes('@')) return email || "Unknown";
        const name = email.split('@')[0];
        return name.charAt(0).toUpperCase() + name.slice(1);
    };

    const currentUserName = formatName(currentUserEmail);
    const chatPartnerName = formatName(chatPartnerEmail);

    const profileSVG = `
        <svg viewBox="0 0 120 120" class="profile-pic-svg">
            <circle cx="60" cy="60" r="58" fill="#d7eedb"/>
            <circle cx="60" cy="45" r="22" fill="#8fc9a2"/>
            <path d="M18 108 Q60 68 102 108 L102 120 L18 120 Z" fill="#8fc9a2"/>
        </svg>
    `;

    
    function renderHeader() {
        document.getElementById('dynamic-chat-header').innerHTML = `
            <div class="avatar md">${profileSVG}</div>
            <div class="header-info">
                <h2>${chatPartnerName}</h2>
                <div class="status">
                    <span class="dot"></span>
                    <span>Active now</span>
                </div>
            </div>
            <div class="header-actions">
                <button class="action-btn" title="Call">📞</button>
                <button class="action-btn" title="Video">📹</button>
            </div>
        `;
    }

    function renderParticipants() {
        document.getElementById('participant-count').innerText = "2 participants";
        document.getElementById('dynamic-participants').innerHTML += `
            <button class="participant-btn active">
                <div class="avatar-wrapper">
                    <div class="avatar sm">${profileSVG}</div>
                    <span class="status-dot"></span>
                </div>
                <div class="participant-info">
                    <div class="name active-text">${currentUserName}</div>
                    <div class="status-text">Active now</div>
                </div>
                <div class="check-icon">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                        <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                </div>
            </button>
        `;
        document.getElementById('dynamic-sender-name').innerText = currentUserName;
    }

    function appendMessage(text, isSelf) {
        const msgContainer = document.getElementById('dynamic-messages');
        const alignClass = isSelf ? 'self' : 'other';
        const bubbleClass = isSelf ? 'bubble-self' : 'bubble-other';
        const contentClass = isSelf ? 'self-content' : '';
        const senderName = isSelf ? currentUserName : chatPartnerName;
        
        const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        const msgHTML = `
            <div class="message-row ${alignClass}">
                ${!isSelf ? `<div class="avatar sm">${profileSVG}</div>` : ''}
                <div class="message-content ${contentClass}">
                    ${!isSelf ? `<span class="sender-name partner-text">${senderName}</span>` : ''}
                    <div class="bubble ${bubbleClass}">${text}</div>
                    <div class="message-meta">
                        <span class="time">${timeString}</span>
                        ${isSelf ? `<span class="read-receipt read">✓✓</span>` : ''}
                    </div>
                </div>
            </div>
        `;
        
        msgContainer.insertAdjacentHTML('beforeend', msgHTML);
        msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    renderHeader();
    renderParticipants();
    document.getElementById('dynamic-messages').innerHTML = `
        <div class="date-container">
            <span class="date-pill">Today · ${new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
        </div>
    `;


    const chatSocket = new WebSocket(`${WS_BASE_URL}/ws/chat/${currentUserEmail}`);

    chatSocket.onopen = () => {
        console.log("Connected to SerenIQ Live Chat server!");
    };

    
    chatSocket.onmessage = (event) => {
        const incomingData = JSON.parse(event.data);
      
        if (incomingData.sender === chatPartnerEmail) {
            appendMessage(incomingData.message, false);
        }
    };

    chatSocket.onerror = (error) => {
        console.error("WebSocket Error:", error);
    };


    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        
        const payload = {
            target_email: chatPartnerEmail,
            message: text
        };

        chatSocket.send(JSON.stringify(payload));

        appendMessage(text, true);

        chatInput.value = '';
        chatInput.focus();
    }

   
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); 
            sendMessage();
        }
    });
});