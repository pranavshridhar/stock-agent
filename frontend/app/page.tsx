import Image from "next/image";
import Tickerbar from "./components/Tickerbar";
import NewsHeader from "./components/NewsHeader";
import ChatbotBox from "./components/ChatboxBox";

export default function Home() {
  return (
    <div className="flex min-h-screen w-full">
      <div className="text-center w-[200px] bg-gray-200">
        <Tickerbar />
      </div>

      {/* Right side content */}
      <div className="flex flex-col w-full h-screen">
        {/* News Header */}
        <div className="flex items-center justify-center flex-1 border">
          <NewsHeader/>
        </div>

        {/* Chatbot */}
        <div className="flex flex-1 border">
          <ChatbotBox/>
        </div>
      </div>
    </div>
  );
}
