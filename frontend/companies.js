const API = 'https://chatbot-backend-kbpn.onrender.com';
const token = localStorage.getItem('token');

async function createCompany() {
  const name = document.getElementById('name').value;
  const description = document.getElementById('description').value;
  const system_prompt = document.getElementById('prompt').value;

  const res = await fetch(`${API}/api/companies/?token=${token}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description, system_prompt })
  });

  if (res.ok) {
    alert('Chatbot created!');
    loadCompanies();
  } else {
    alert('Error creating company');
  }
}

async function loadCompanies() {
  const res = await fetch(`${API}/api/companies/?token=${token}`);
  const data = await res.json();

  const list = document.getElementById('companies-list');
  list.innerHTML = data.companies.map(c => `
    <div class="card">
      <h3>${c.name}</h3>
      <p>${c.description}</p>
      <button onclick="testBot(${c.id})">💬 Test Chatbot</button>
      <button onclick="showEmbed(${c.id})">📋 Get Embed Code</button>
    </div>
  `).join('');
}

function testBot(companyId) {
  window.location.href = `chat.html?company_id=${companyId}`;
}

function showEmbed(companyId) {
  const code = `<script src="${API}/widget.js" data-company="${companyId}"><\/script>`;
  prompt('Copy this embed code:', code);
}

loadCompanies(); // run once on page load