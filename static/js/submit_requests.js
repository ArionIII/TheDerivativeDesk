// ✅ Ouvrir le modal
function openToolRequestModal(type) {
    document.getElementById('tool-modal-title').innerText = 
        type === 'feature' ? 'Request New Feature' : 'Report Issue';

    document.getElementById('tool-request-modal').classList.add('show'); // ✅ Corrigé : on ajoute bien la classe 'show'
    window.toolRequestType = type;
}

// ✅ Fermer le modal
function closeToolRequestModal() {
    document.getElementById('tool-request-modal').classList.remove('show'); // ✅ Corrigé : on retire la classe 'show'
}

// ✅ Soumettre la requête
async function submitToolRequest() {
    const description = document.getElementById('tool-request-description').value;
    console.log(description)
    const toolKey = window.location.pathname; // Récupère l'URL actuelle à partir de /tools
    console.log(toolKey)
    if (!description.trim()) {
        alert("Description cannot be empty");
        return;
    }

    const payload = {
        type: window.toolRequestType,
        tool_key: toolKey,
        description: description
    };

    console.log("Payload being sent:", payload); // ✅ Vérifie le contenu envoyé

    try {
        const response = await fetch('/requests/create', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Request submitted successfully!');
            closeToolRequestModal();
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error submitting request:', error);
        alert('Something went wrong. Please try again.');
    }
}


// ✅ Ajouter les event listeners lors du chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ DOM Loaded - JS ready!");

    // 🔎 Boutons pour ouvrir le modal
    const featureButton = document.querySelector('.tool-btn-feature');
    const issueButton = document.querySelector('.tool-btn-issue');

    console.log("➡️ Feature button found: ", featureButton);
    console.log("➡️ Issue button found: ", issueButton);

    if (featureButton) {
        featureButton.addEventListener('click', () => {
            console.log("➡️ Feature button clicked");
            openToolRequestModal('feature');
        });
    } else {
        console.error("❌ Feature button not found");
    }

    if (issueButton) {
        issueButton.addEventListener('click', () => {
            console.log("➡️ Issue button clicked");
            openToolRequestModal('issue');
        });
    } else {
        console.error("❌ Issue button not found");
    }

    // ✅ Bouton de soumission dans le modal
    const submitButton = document.querySelector('.tool-submit-btn');
    if (submitButton) {
        submitButton.addEventListener('click', async () => {
            console.log("➡️ Submit button clicked");
            await submitToolRequest();
        });
    } else {
        console.error("❌ Submit button not found");
    }

    // ✅ Fermer le modal en cliquant sur le fond noir
    const modal = document.getElementById('tool-request-modal');
    if (modal) {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeToolRequestModal();
            }
        });
    }
});
