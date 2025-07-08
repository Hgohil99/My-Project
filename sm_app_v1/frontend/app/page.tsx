"use client";
import { useEffect, useState } from "react";

type StockSummary = {
  ticker: string;
  current_price: number;
  circuit_event: string;
};

export default function Page() {
  const [stocks, setStocks] = useState<StockSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [logging, setLogging] = useState(false);
  const [timestamp, setTimestamp] = useState("");

  useEffect(() => {
    const now = new Date();
    setTimestamp(now.toLocaleTimeString());
  }, []);

  const fetchSummary = async () => {
    try {
      const res = await fetch("http://localhost:8000/stocks");
      const data = await res.json();
      setStocks(data);
    } catch (err) {
      console.error("Error fetching summary:", err);
    } finally {
      setLoading(false);
    }
  };

  const triggerLog = async () => {
    try {
      setLogging(true);
      const res = await fetch("http://localhost:8000/log/now", { method: "POST" });
      alert("✅ Snapshot triggered and will be saved to CSV.");
    } catch (err) {
      console.error("Error triggering log:", err);
      alert("⚠️ Error triggering log.");
    } finally {
      setLogging(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  return (
    <main className="min-h-screen p-6 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4 text-indigo-700">📈 Stock Summary Dashboard</h1>
      <div className="flex items-center justify-between bg-indigo-100 text-indigo-800 px-4 py-2 rounded mb-4">
        <p className="text-sm font-medium">✅ Scheduler Status: <span className="font-bold">Active</span></p>
        <p className="text-sm">🕓 Last updated: {timestamp || "--"}</p>
      </div>

      <button
        onClick={triggerLog}
        className="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        disabled={logging}
      >
        {logging ? "Saving..." : "Trigger Snapshot Log"}
      </button>

      {loading ? (
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        </div>      
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stocks.map((stock) => (
            <div
              key={stock.ticker}
              className="bg-white shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-300 p-5 rounded-lg border-l-4 border-green-500"

            >
              <h2 className="text-xl font-semibold">{stock.ticker}</h2>
              <p className="text-gray-600">Price: ₹{stock.current_price}</p>
                <span
                className={`inline-block px-3 py-1 text-xs font-semibold text-white rounded-full 
                  ${
                    stock.circuit_event === "Upper Hit"
                    ? "bg-red-500 animate-pulse"
                    : stock.circuit_event === "Lower Hit"
                    ? "bg-blue-500 animate-pulse"
                    : "bg-gray-400"
                  }`}
                  >
                    {stock.circuit_event}
                  </span>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
