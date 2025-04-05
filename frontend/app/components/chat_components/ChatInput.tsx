'use client'

import React, { useState } from 'react'
import { Send } from 'lucide-react'

type ChatInputProps = {
  onSend: (message: string) => void
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed) return

    onSend(trimmed)
    setInput('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center p-4 border-t bg-white">
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className="ml-2 bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600"
      >
        <Send size={20} />
      </button>
    </form>
  )
}

export default ChatInput
