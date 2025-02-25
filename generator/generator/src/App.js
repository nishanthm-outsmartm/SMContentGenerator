import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // Import the CSS file

function App() {
  const [formData, setFormData] = useState({
    topic: '',
    tone: 'professional',
    platform: 'instagram',
    useHashtags: true,
  });
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:5000/generate', formData);
      setResult(response.data.content);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating content');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Social Media Content Generator</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Topic/URL:</label>
          <input
            type="text"
            value={formData.topic}
            onChange={(e) => setFormData({...formData, topic: e.target.value})}
            required
          />
        </div>

        <div>
          <label>Tone:</label>
          <select
            value={formData.tone}
            onChange={(e) => setFormData({...formData, tone: e.target.value})}
          >
            <option value="professional">Professional</option>
            <option value="persuasive">Persuasive</option>
            <option value="humorous">Humorous</option>
            <option value="casual">Casual</option>
          </select>
        </div>

        <div>
          <label>Platform:</label>
          <select
            value={formData.platform}
            onChange={(e) => setFormData({...formData, platform: e.target.value})}
          >
            <option value="instagram">Instagram</option>
            <option value="twitter">X (Twitter)</option>
            <option value="facebook">Facebook</option>
            <option value="linkedin">LinkedIn</option>
          </select>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              checked={formData.useHashtags}
              onChange={(e) => setFormData({...formData, useHashtags: e.target.checked})}
            />
            Use Hashtags
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Content'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h2>Generated Content:</h2>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
