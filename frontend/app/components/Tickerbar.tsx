"use client"; // Only needed if you're using Next.js App Router (v13+)

import React, { useEffect, useState } from "react";

type TickerData = {
  [symbol: string]: {
    price: number;
    change: number;
    percent_change: number;
    direction: "up" | "down" | "unchanged";
  };
};

const Tickerbar = () => {
  const ticker_list = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOGL"];
  const [data, setData] = useState<TickerData | null>(null);

  useEffect(() => {
    const query = ticker_list.join(",");
    fetch(`http://localhost:5000/tickers?symbols=${query}`)
      .then((res) => res.json())
      .then(setData)
      .catch((err) => console.error("Error fetching tickers:", err));
  }, []);

  return (
    <div className="pt-5 flex flex-wrap gap-4 justify-center items-center">
      {data ? (
        ticker_list.map((symbol) => {
          const ticker = data[symbol];
          if (!ticker || "error" in ticker) {
            return (
              <div
                key={symbol}
                className="px-4 py-2 bg-gray-200 rounded shadow text-sm"
              >
                {symbol}: N/A
              </div>
            );
          }

          const color =
            ticker.direction === "up"
              ? "text-green-600"
              : ticker.direction === "down"
              ? "text-red-600"
              : "text-gray-600";

          const arrow =
            ticker.direction === "up"
              ? "▲"
              : ticker.direction === "down"
              ? "▼"
              : "→";

          return (
            <div
              key={symbol}
              className="px-4 py-2 bg-white rounded shadow text-sm flex flex-col items-center"
            >
              <div className="font-semibold">{symbol}</div>
              <div className="flex items-center gap-1">
                <span>${ticker.price.toFixed(2)}</span>
                <span className={color}>
                  {arrow} {ticker.percent_change.toFixed(2)}%
                </span>
              </div>
            </div>
          );
        })
      ) : (
        <div className="text-sm text-gray-500">Loading tickers...</div>
      )}
    </div>
  );
};

export default Tickerbar;
