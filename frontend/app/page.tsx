import Image from "next/image";
import Tickerbar from "./components/Tickerbar";

export default function Home() {
  return (
    <div className="flex flex-row items-center justify-between min-h-screen p-24 border">
      <Tickerbar/>
      <div className="flex flex-col h-full w-full">
        <div className="flex items-center justify-center p-5 border">
          news header
        </div>
        <div className="flex items-center justify-center border">
          chatbot box
        </div>
      </div>
    </div>
  );
}
