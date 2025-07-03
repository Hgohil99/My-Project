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

  const fetchSummary = async () => {
    try {
      const res = await fetch("http://localhost:8000/summary");
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
      await fetch("http://localhost:8000/log/now", { method: "POST" });
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

      <button
        onClick={triggerLog}
        className="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        disabled={logging}
      >
        {logging ? "Saving..." : "Trigger Snapshot Log"}
      </button>

      {loading ? (
        <p>Loading stock data...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stocks.map((stock) => (
            <div
              key={stock.ticker}
              className="bg-white shadow p-4 rounded border-l-4 border-green-500"
            >
              <h2 className="text-xl font-semibold">{stock.ticker}</h2>
              <p className="text-gray-600">Price: ₹{stock.current_price}</p>
              <p className="text-sm text-gray-500">Circuit: {stock.circuit_event}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
