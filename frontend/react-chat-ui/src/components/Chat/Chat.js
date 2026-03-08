import { useState } from "react";
import "./Chat.css";

function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (message.trim() === "") return;

    // add user message
    const newChat = [...chat, { sender: "user", text: message }];
    setChat(newChat);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        "https://genai-chat-assistant-wt18.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        }
      );

      const data = await response.json();

      setLoading(false);

      // add each bot response
      const updatedChat = [...newChat];

      data.responses.forEach((answer) => {
        updatedChat.push({ sender: "bot", text: answer });
      });

      setChat(updatedChat);
    } catch (error) {
      setLoading(false);

      setChat([...newChat, { sender: "bot", text: "Server error occurred" }]);
    }
  };

  return (
    <div className="chat-container">
      <h2>GenAI Chat Assistant</h2>

      <div className="chat-box">
        {chat.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <div className="bubble">Typing...</div>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          placeholder="Ask something..."
        />

        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chat;
