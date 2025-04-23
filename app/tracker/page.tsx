'use client';

import { useState } from 'react';
import AutoWatchlist from './components/AutoWatchlist'; // Ensure the file exists at this path
import Screener from './components/Screener';
import SectorRotation from './components/SectorRotation';

const TABS = ['Auto-Watchlist', 'Screener', 'Sector Rotation'];

export default function TrackerPage() {
  const [activeTab, setActiveTab] = useState('Auto-Watchlist');

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4">
      {/* Tab Switcher */}
      <div className="flex justify-center gap-2 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-md font-semibold transition ${
              activeTab === tab
                ? 'bg-gray-700 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* View Renderer */}
      {activeTab === 'Auto-Watchlist' && <AutoWatchlist />}
      {activeTab === 'Screener' && <Screener />}
      {activeTab === 'Sector Rotation' && <SectorRotation />}
    </div>
  );
}
