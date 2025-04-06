'use client'

import { useState, useEffect, useRef } from 'react'
import ChatInput from './chat_components/ChatInput'

type ChatMessage = {
  role: 'user' | 'model'
  parts: string[]
}

const ChatboxBox = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
  ])

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSend = async (text: string) => {
    const userMessage: ChatMessage = { role: 'user', parts: [text] }

    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)

    try {
      const res = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ history: updatedMessages }),
      })

      const data = await res.json()

      const aiMessage: ChatMessage = {
        role: 'model',
        parts: [data.response],
      }

      setMessages((prev) => [...prev, aiMessage])
    } catch (err) {
      console.error('Failed to fetch AI reply:', err)
      setMessages((prev) => [
        ...prev,
        {
          role: 'model',
          parts: ['⚠️ There was an error contacting the AI.'],
        },
      ])
    }
    // You’ll add async Gemini fetch here later
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])



  return (
    <div className="flex flex-col w-full h-full">
      {/* Scrollable message area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-100">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-xs ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-black'
              }`}
            >
              {msg.parts[0]}
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
