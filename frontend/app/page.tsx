import Image from "next/image";
import Tickerbar from "./components/Tickerbar";
import NewsHeader from "./components/NewsHeader";
import ChatbotBox from "./components/ChatboxBox";
import ChatboxBox from "./components/ChatboxBox";

export default function Home() {
  return (
    <div className="flex min-h-screen w-full">
      <div className="text-center w-[200px] bg-gray-200">
        <Tickerbar />
      </div>

      {/* Right side content */}
      <div className="flex flex-col flex-1">
        {/* News Header — top 50% */}
        <div className="h-1/2 border">
          <NewsHeader />
        </div>

        {/* Chatbox — bottom 50% */}
        <div className="h-1/2 border">
          <ChatboxBox />
        </div>
      </div>
    </div>
  );
}
