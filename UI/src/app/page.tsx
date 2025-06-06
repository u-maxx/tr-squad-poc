"use client";
import React, { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null as null | {
    squad: { name: string; surname: string; dob: string; position: string }[];
    total_tokens_used: number;
    total_elapsed_time: number;
  });

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v2/squad-finder";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      setError("Query cannot be empty.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const data = await response.json();
      if (!data.result || !data.result.squad) {
        setError("No squad data found.");
        setLoading(false);
        return;
      }
      setResult({
        squad: data.result.squad,
        total_tokens_used: data.total_tokens_used,
        total_elapsed_time: data.total_elapsed_time,
      });
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-100 flex items-center justify-center py-8">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-3xl p-8 flex flex-col items-center">
        <h1 className="text-4xl font-bold mb-2 text-center">TR Squad Finder</h1>
        <p className="text-lg text-gray-600 mb-6 text-center">
          Enter a Premier League team query to get squad information.
        </p>
        <form
          onSubmit={handleSubmit}
          className="flex w-full max-w-2xl mb-8"
        >
          <div className="flex items-center bg-blue-100 rounded-l-md px-4 w-full">
            <span className="text-xl text-blue-500 mr-2">🔍</span>
            <input
              type="text"
              className="bg-blue-100 outline-none border-none w-full py-3 text-base"
              placeholder="Show me the Liverpool squad"
              value={query}
              onChange={e => setQuery(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="bg-orange-400 hover:bg-orange-500 text-white font-semibold px-6 rounded-r-md transition-colors"
            disabled={loading}
          >
            {loading ? "..." : "Get Squad"}
          </button>
        </form>
        {error && <div className="text-red-600 font-semibold mb-4">{error}</div>}
        {loading && (
          <div className="flex justify-center items-center mb-6">
            <div className="w-8 h-8 border-4 border-blue-400 border-t-transparent rounded-full animate-spin" role="status" aria-label="Loading"></div>
          </div>
        )}
        {result && (
          <div className="w-full">
            <h2 className="text-2xl font-semibold text-center mb-6">Squad Information</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-base border-separate border-spacing-0">
                <thead>
                  <tr className="bg-blue-50">
                    <th className="py-3 px-4 text-left font-semibold">First Name</th>
                    <th className="py-3 px-4 text-left font-semibold">Surname</th>
                    <th className="py-3 px-4 text-left font-semibold">Date of Birth</th>
                    <th className="py-3 px-4 text-left font-semibold">Position</th>
                  </tr>
                </thead>
                <tbody>
                  {result.squad.map((player, idx) => (
                    <tr key={player.name + player.surname + idx} className="border-b last:border-b-0">
                      <td className="py-2 px-4 font-semibold">{player.name}</td>
                      <td className="py-2 px-4">{player.surname}</td>
                      <td className="py-2 px-4">{player.dob}</td>
                      <td className="py-2 px-4">{player.position}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
