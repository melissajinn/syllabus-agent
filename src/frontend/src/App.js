import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    const userMsg = { role: 'user', content: message };
    setChat([...chat, userMsg]);
    
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      
      const data = await response.json();
      setChat(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setChat(prev => [...prev, { role: 'assistant', content: 'Error connecting to agent' }]);
    }
    
    setMessage('');
    setLoading(false);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setChat(prev => [...prev, { role: 'user', content: `Uploading ${file.name}...` }]);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/upload-pdf', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      
      if (data.error) {
        setChat(prev => [...prev, { role: 'assistant', content: `Error: ${data.error}` }]);
      } else {
        setChat(prev => [...prev, { role: 'assistant', content: data.response }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setChat(prev => [...prev, { role: 'assistant', content: 'Error uploading file' }]);
    }

    setUploading(false);
    event.target.value = ''; // Reset file input
  };

  const resetChat = async () => {
    try {
      await fetch('http://localhost:8000/reset', { method: 'POST' });
      setChat([]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <h1>Syllabus Assistant</h1>
          <button onClick={resetChat} className="reset-btn">Reset</button>
        </div>
        
        <div className="chat-box">
          {chat.length === 0 && (
            <div className="welcome">
              <p>Welcome! To get started, load your syllabus:</p>
              <p>• Upload a PDF using the button below</p>
              <p>• Or type: <code>web https://course-website.com</code></p>
            </div>
          )}
          {chat.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <strong>{msg.role === 'user' ? 'You' : 'Assistant'}:</strong>
              <div>{msg.content}</div>
            </div>
          ))}
          {(loading || uploading) && <div className="loading">Agent is thinking...</div>}
        </div>
        
        <div className="input-area">
          <label className="upload-btn">
            📎 Upload PDF
            <input 
              type="file" 
              accept=".pdf" 
              onChange={handleFileUpload}
              disabled={uploading}
              style={{ display: 'none' }}
            />
          </label>
          
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
            placeholder="Type a message, load website, or upload PDF..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !message.trim()}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;