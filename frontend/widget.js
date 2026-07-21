(function() {
    const script = document.currentScript;
    const companyId = script.getAttribute('data-company-id');
    const API = 'http://localhost:5000';

    // Floating button
    const button = document.createElement('button');
    button.innerText = '💬';
    Object.assign(button.style, {
        position: 'fixed', bottom: '20px', right: '20px',
        width: '60px', height: '60px', borderRadius: '50%',
        background: '#667eea', border: 'none', fontSize: '24px',
        cursor: 'pointer', zIndex: 9999
    });
    document.body.appendChild(button);

    // Chat box
    const chatBox = document.createElement('div');
    Object.assign(chatBox.style, {
        display: 'none', position: 'fixed', bottom: '90px', right: '20px',
        width: '300px', height: '400px', background: 'white',
        border: '1px solid #ccc', borderRadius: '10px',
        flexDirection: 'column', overflow: 'hidden', zIndex: 9999
    });
    chatBox.innerHTML = `
        <div id="messages" style="flex:1; overflow-y:auto; padding:10px;"></div>
        <div style="display:flex; border-top:1px solid #ccc;">
            <input id="userInput" placeholder="Type a message..." style="flex:1; border:none; padding:10px;">
            <button id="sendBtn" style="background:#667eea; color:white; border:none; padding:10px;">Send</button>
        </div>
    `;
    document.body.appendChild(chatBox);

    // Toggle open/close
    button.onclick = () => {
        chatBox.style.display = chatBox.style.display === 'none' ? 'flex' : 'none';
    };

    // Send message
    let conversationId = null;
    document.getElementById('sendBtn').onclick = sendMessage;

    async function sendMessage() {
        const input = document.getElementById('userInput');
        const text = input.value.trim();
        if (!text) return;

        addBubble(text, 'user');
        input.value = '';

    const res = await fetch(`${API}/api/chat/public-chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                company_id: companyId,
                conversation_id: conversationId
            })
        });

        const data = await res.json();
        conversationId = data.conversation_id;
        addBubble(data.ai_response, 'bot');
    }

    function addBubble(text, sender) {
        const messages = document.getElementById('messages');
        const bubble = document.createElement('div');
        bubble.innerText = text;
        bubble.style.margin = '5px 0';
        bubble.style.textAlign = sender === 'user' ? 'right' : 'left';
        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;
    }
})();
