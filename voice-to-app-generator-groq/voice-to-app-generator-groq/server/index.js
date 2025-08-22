const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const GROQ_API_KEY = process.env.GROQ_API_KEY;
const GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions';

app.post('/generate', async (req, res) => {
  const { prompt } = req.body;
  try {
    const response = await axios.post(GROQ_URL, {
      model: "llama3-70b-8192",
      messages: [
        { role: "system", content: "You are a React code generator. Generate clean functional React component code without comments." },
        { role: "user", content: `Create a React component for: ${prompt}` }
      ]
    }, {
      headers: {
        "Authorization": `Bearer ${GROQ_API_KEY}`,
        "Content-Type": "application/json"
      }
    });
    const code = response.data.choices[0].message.content;
    res.json({ code });
  } catch (error) {
    console.error(error.response?.data || error.message);
    res.status(500).json({ error: "Failed to generate code" });
  }
});

app.listen(5000, () => console.log('Server running on http://localhost:5000'));
