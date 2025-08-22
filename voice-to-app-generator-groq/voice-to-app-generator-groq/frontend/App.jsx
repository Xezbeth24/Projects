import React, { useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from 'axios';
import { LiveProvider, LiveEditor, LivePreview } from 'react-live';

function App() {
  const [query, setQuery] = useState('');
  const [code, setCode] = useState('<h1>Start creating!</h1>');
  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  const handleGenerate = async () => {
    const prompt = transcript || query;
    if (!prompt) return;
    const res = await axios.post('http://localhost:5000/generate', { prompt });
    setCode(res.data.code || '<h1>Error generating code</h1>');
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h1>Voice-to-App Generator (Groq Powered)</h1>
      <p>Listening: {listening ? 'Yes' : 'No'}</p>
      <button onClick={SpeechRecognition.startListening}>🎤 Start Voice</button>
      <button onClick={SpeechRecognition.stopListening}>🛑 Stop</button>
      <button onClick={resetTranscript}>Clear</button>
      <p>Transcript: {transcript}</p>
      <input 
        type="text" 
        placeholder="Type your app idea..." 
        value={query} 
        onChange={e => setQuery(e.target.value)} 
        style={{ width: '80%', marginTop: 10 }}
      />
      <button onClick={handleGenerate} style={{ marginLeft: 10 }}>Generate</button>
      <LiveProvider code={code}>
        <div style={{ display: 'flex', gap: '20px', marginTop: 20 }}>
          <div style={{ width: '50%' }}><LiveEditor /></div>
          <div style={{ width: '50%', border: '1px solid #ddd', padding: 10 }}><LivePreview /></div>
        </div>
      </LiveProvider>
    </div>
  );
}

export default App;
