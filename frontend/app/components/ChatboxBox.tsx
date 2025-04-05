'use client'

import { useState, useEffect, useRef } from 'react'
import ChatInput from './chat_components/ChatInput'

const ChatboxBox = () => {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Welcome!' },
    { sender: 'user', text: 'Hi!' },
  ])

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSend = (text: string) => {
    setMessages(prev => [...prev, { sender: 'user', text }])
  }

  useEffect(() => { // scrolling down
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex flex-col w-full h-full">
      {/* Scrollable message area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-100">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-xs ${
                msg.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-black'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSend={handleSend} />
    </div>
  )
}

export default ChatboxBox
