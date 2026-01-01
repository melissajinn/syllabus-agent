import { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState(''); // holds input message
  const [chat, setChat] = useState([]); // holds array of chat history 
  const [loading, setLoading] = useState(false); // tracks when agent is processing message
  const [uploading, setUploading] = useState(false); // tracks when file is being uploaded

  const sendMessage = async () => { //nmessage function
    if (!message.trim()) return; // checks for empty message, returns early if empty
    
    setLoading(true);
    const userMsg = { role: 'user', content: message }; // creates user message object
    setChat([...chat, userMsg]); // update chat history state
    
    try {
      const response = await fetch('http://localhost:8000/chat', { // make request to backend
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      
      const data = await response.json();
      setChat(prev => [...prev, { role: 'assistant', content: data.response }]); // update history
    } catch (error) {
      console.error('Error:', error);
      setChat(prev => [...prev, { role: 'assistant', content: 'Error connecting to agent' }]);
    }
    
    setMessage(''); // clear input so user can type another message
    setLoading(false); // no longer loading
  };

  const handleFileUpload = async (event) => { // file upload handler
    const file = event.target.files[0];
    if (!file) return; // exit if no file

    setUploading(true);
    setChat(prev => [...prev, { role: 'user', content: `Uploading ${file.name}...` }]); // shows "uploading syllabus.pdf"

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
    event.target.value = '';
  };

  const resetChat = async () => { // reset entire chat
    try {
      await fetch('http://localhost:8000/reset', { method: 'POST' });
      setChat([]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return ( // JSX structure
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
            <div key={i} className={`message ${msg.role}`}> // identifies user vs assistant message
              <strong>{msg.role === 'user' ? 'You' : 'Assistant'}:</strong> // if user message, show "You", else "Assistant"
              <div>{msg.content}</div> // display content
            </div>
          ))}
          {(loading || uploading) && <div className="loading">Agent is thinking...</div>} // if loading or uploading, show this message
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
            onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()} // send message on Enter key
            placeholder="Type a message or upload a PDF..." // what to show on input box
            disabled={loading} // disables input while loading is true
          />
          <button onClick={sendMessage} disabled={loading || !message.trim()}> // disable send button if loading or empty message
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;