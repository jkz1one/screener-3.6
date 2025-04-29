'use client';

import { useEffect, useState } from 'react';
import WatchlistControls from './WatchlistControls';

type Stock = {
  symbol: string;
  score: number;
  tags: string[];
  tierHits: Record<string, string[]>;
  isBlocked: boolean;
  reasons: string[];
};

export default function AutoWatchlist() {
  const [data, setData] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);

  const [expanded, setExpanded] = useState<string[]>([]);
  const [tiersShown, setTiersShown] = useState<Record<string, boolean>>({
    T1: true,
    T2: true,
    T3: true,
  });
  const [showRisk, setShowRisk] = useState(true);
  const [tagFilters, setTagFilters] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<'score' | 'symbol'>('score');

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch('/api/autowatchlist');
        const json = await res.json();
        const mapped = json.map((stock: any) => ({
          symbol: stock.symbol,
          score: stock.score,
          tags: stock.tags || [],
          isBlocked: stock.isBlocked || false,
          reasons: stock.reasons || [],
          tierHits: {
            T1: stock.tier1 || [],
            T2: stock.tier2 || [],
            T3: stock.tier3 || [],
          },
        }));
        setData(mapped);
      } catch (err) {
        console.error('Failed to fetch autowatchlist', err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const toggleRow = (symbol: string, isCmdOrCtrl: boolean) => {
    setExpanded((prev) => {
      const isOpen = prev.includes(symbol);
      if (isCmdOrCtrl) {
        return isOpen ? prev.filter((s) => s !== symbol) : [...prev, symbol];
      } else {
        return isOpen ? [] : [symbol];
      }
    });
  };

  const filtered = data
    .filter((stock) => {
      const matchesTier =
        (tiersShown.T1 && stock.tierHits.T1.length > 0) ||
        (tiersShown.T2 && stock.tierHits.T2.length > 0) ||
        (tiersShown.T3 && stock.tierHits.T3.length > 0);
      const riskDisqualified = stock.isBlocked;
      const matchesTags =
        tagFilters.length === 0 || tagFilters.some((tag) => stock.tags.includes(tag));
      return matchesTier && matchesTags && (showRisk || !riskDisqualified);
    })
    .sort((a, b) => {
      if (sortBy === 'score') return b.score - a.score;
      if (sortBy === 'symbol') return a.symbol.localeCompare(b.symbol);
      return 0;
    });

  if (loading) {
    return <div className="text-gray-400 text-sm">Loading watchlist...</div>;
  }

  return (
    <div className="space-y-4">
      <WatchlistControls
        tiersShown={tiersShown}
        setTiersShown={setTiersShown}
        showRisk={showRisk}
        setShowRisk={setShowRisk}
        tagFilters={tagFilters}
        setTagFilters={setTagFilters}
        sortBy={sortBy}
        setSortBy={setSortBy}
      />

      {filtered.map((stock) => {
        const isOpen = expanded.includes(stock.symbol);

        return (
          <div key={stock.symbol} className="bg-gray-800 rounded-lg shadow-md">
            <div
              className="flex justify-between items-center px-4 py-3 cursor-pointer"
              onClick={(e) => toggleRow(stock.symbol, e.metaKey || e.ctrlKey)}
            >
              <div className="flex items-center gap-4">
                <div className="text-lg font-bold">{stock.symbol}</div>
                <div className="text-sm text-gray-400">Score: {stock.score}</div>
                {stock.tags.map((tag) => (
                  <span
                    key={tag}
                    className="bg-gray-700 text-xs px-2 py-0.5 rounded-full text-gray-200"
                  >
                    {tag}
                  </span>
                ))}
                {tiersShown.T1 && stock.tierHits.T1.length > 0 && (
                  <span className="bg-green-600 text-white text-xs px-2 py-0.5 rounded-full font-semibold">T1</span>
                )}
                {tiersShown.T2 && stock.tierHits.T2.length > 0 && (
                  <span className="bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full font-semibold">T2</span>
                )}
                {tiersShown.T3 && stock.tierHits.T3.length > 0 && (
                  <span className="bg-purple-600 text-white text-xs px-2 py-0.5 rounded-full font-semibold">T3</span>
                )}
              </div>
              <div className="text-gray-400 text-sm">{isOpen ? '▲' : '▼'}</div>
            </div>

            {isOpen && (
              <div className="grid grid-cols-3 gap-4 bg-gray-700 px-4 py-3 text-sm text-gray-200 border-t border-gray-600">
                <div>
                  <h4 className="text-green-400 font-bold mb-1">Tier 1</h4>
                  <ul className="space-y-1">
                    {stock.tierHits.T1.map((s) => (
                      <li key={s}>✓ {s}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-blue-400 font-bold mb-1">Tier 2</h4>
                  <ul className="space-y-1">
                    {stock.tierHits.T2.map((s) => (
                      <li key={s}>✓ {s}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-purple-400 font-bold mb-1">Tier 3</h4>
                  <ul className="space-y-1">
                    {stock.tierHits.T3.map((s) => (
                      <li key={s}>✓ {s}</li>
                    ))}
                  </ul>
                </div>

                {stock.reasons.length > 0 && (
                  <div className="col-span-3 pt-2 border-t border-gray-600">
                    <h4 className="text-red-400 font-semibold text-sm mb-1">Risk Flags</h4>
                    <ul className="flex gap-3 text-xs text-red-300">
                      {stock.reasons.map((flag) => (
                        <li key={flag}>⚠ {flag}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
