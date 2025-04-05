import React from 'react'
import { Send } from 'lucide-react'

const ChatboxBox = () => {
  return (
    <div className="flex flex-col w-full h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-100">
        {/* AI Message - Left */}
        <div className="flex justify-end">
          <div className="bg-gray-200 text-black px-4 py-2 rounded-2xl max-w-xs">
            Hello AI.
          </div>
        </div>

        {/* User Message - Right */}
        <div className="flex justify-start">
          <div className="bg-blue-500 text-white px-4 py-2 rounded-2xl max-w-xs">
            Hi! What's up?
          </div>
        </div>
      </div>

      {/* Input area at the bottom */}
      <form className="flex items-center p-4 border-t bg-white">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="ml-2 bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600"
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  )
}

export default ChatboxBox
