let questionsData = null; // Variable to store questions data from data.json

// Function to send message
function sendMessage(message) {
    // Set the input field value to the message before sending
    document.getElementById('user-input').value = message;

    displayMessage('user', message);

    // Disable input and button while waiting for response
    document.getElementById('user-input').disabled = true;
    document.getElementById('send-button').disabled = true;

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage('bot', data.message);
        loadHistory(); // Reload history after sending a message

        // Re-enable input and button after response is displayed
        document.getElementById('user-input').disabled = false;
        document.getElementById('send-button').disabled = false;

        if (data.askQuestions) {
            suggestQuestions(message); // Suggest questions based on user input
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
        // Handle error appropriately, e.g., display error message to user
        document.getElementById('user-input').disabled = false;
        document.getElementById('send-button').disabled = false;
    });
}

// Event listener for Enter key press in the input field
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const userInput = this.value.trim();
        if (userInput !== '') {
            sendMessage(userInput); // Call sendMessage function if Enter key is pressed with non-empty input
        }
    }
});

// Event listener for Send button click
document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput !== '') {
        sendMessage(userInput); // Call sendMessage function when Send button is clicked with non-empty input
    }
});

// Function to load questions data from data.json
function loadQuestionsData() {
    fetch('static/json/data.json') // Update with the actual path to your data.json file
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load questions data');
            }
            return response.json();
        })
        .then(data => {
            questionsData = data;
        })
        .catch(error => console.error('Error loading questions data:', error));
}

// Function to suggest questions based on user input
function suggestQuestions(userInput) {
    if (!questionsData) {
        console.error('Questions data not loaded.');
        return;
    }

    const suggestedQuestions = filterQuestions(userInput);
    displayQuestionButtons(suggestedQuestions);
}

// Function to filter questions based on user input using fuzzy matching
function filterQuestions(userInput) {
    let filteredQuestions = [];
    if (questionsData && questionsData.data && questionsData.data.length > 0) {
        questionsData.data.forEach(item => {
            if (item.paragraphs && item.paragraphs.length > 0) {
                item.paragraphs.forEach(para => {
                    if (para.qas && para.qas.length > 0) {
                        para.qas.forEach(qa => {
                            const questionText = qa.question.toLowerCase();
                            if (questionText.includes(userInput.toLowerCase())) {
                                filteredQuestions.push(qa.question);
                            }
                        });
                    }
                });
            }
        });
    }
    return filteredQuestions;
}

// Function to display clickable question buttons
function displayQuestionButtons(questions) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Clear previous messages

    questions.forEach(question => {
        const button = document.createElement('button');
        button.classList.add('question-button');
        button.textContent = question;
        button.addEventListener('click', function() {
            // Set the input value to the clicked question
            document.getElementById('user-input').value = question;
            sendMessage(question); // Send the selected question when button is clicked
        });
        chatBox.appendChild(button);
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to display message in chat box
function displayMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    
    // Add sender class for styling
    if (sender === 'user') {
        messageDiv.classList.add('user-message');
        messageDiv.textContent = `You: ${message}`;
    } else if (sender === 'bot') {
        messageDiv.classList.add('bot-message');
        messageDiv.textContent = `Bot: ${message}`;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to display chat history
function displayHistory(history) {
    const historyContainer = document.getElementById('history-container');
    historyContainer.innerHTML = ''; // Clear previous history

    Object.keys(history).forEach(day => {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('history-day');
        dayDiv.textContent = day;

        history[day].forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('history-message');
            messageDiv.classList.add(msg.sender === 'user' ? 'user-message' : 'bot-message');
            messageDiv.textContent = `${msg.sender.charAt(0).toUpperCase() + msg.sender.slice(1)}: ${msg.message}`;
            dayDiv.appendChild(messageDiv);
        });

        historyContainer.appendChild(dayDiv);
    });

    // Show history container
    historyContainer.style.display = 'block';
}

// Function to load chat history via API
function loadHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            displayHistory(data);
        })
        .catch(error => console.error('Error loading history:', error));
}

// Load questions data and chat history when the page loads
window.onload = function() {
    loadQuestionsData();
    loadHistory();

    // Optionally, you can keep your existing show/hide history button logic here
    document.getElementById('show-history-button').addEventListener('click', function() {
        const historyContainer = document.getElementById('history-container');
        if (historyContainer.style.display === 'none') {
            historyContainer.style.display = 'block';
            document.getElementById('show-history-button').textContent = 'Masquer l’historique';
        } else {
            historyContainer.style.display = 'none';
            document.getElementById('show-history-button').textContent = 'Afficher l’historique';
        }
    });

    // Monitor user input for suggestions
    document.getElementById('user-input').addEventListener('input', function() {
        const userInput = this.value.trim();
        if (userInput === '') {
            document.getElementById('chat-box').innerHTML = ''; // Clear suggestions if input is empty
        } else {
            suggestQuestions(userInput); // Suggest questions based on current input
        }
    });
};
