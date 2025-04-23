'use client';

type Props = {
  tiersShown: Record<string, boolean>;
  setTiersShown: (value: Record<string, boolean>) => void;
  showRisk: boolean;
  setShowRisk: (val: boolean) => void;
  tagFilters: string[];
  setTagFilters: (tags: string[]) => void;
  sortBy: string;
  setSortBy: (val: string) => void;
};

const TIERS = ['T1', 'T2', 'T3'];
const TAGS = ['Strong Setup', 'Squeeze Watch', 'Early Watch'];

export default function WatchlistControls({
  tiersShown,
  setTiersShown,
  showRisk,
  setShowRisk,
  tagFilters,
  setTagFilters,
  sortBy,
  setSortBy
}: Props) {
  const toggleTier = (tier: string) => {
    setTiersShown({ ...tiersShown, [tier]: !tiersShown[tier] });
  };

  const toggleTag = (tag: string) => {
    setTagFilters(
      tagFilters.includes(tag)
        ? tagFilters.filter((t) => t !== tag)
        : [...tagFilters, tag]
    );
  };

  return (
    <div className="flex flex-wrap items-center gap-3 bg-gray-800 p-3 rounded-lg mb-6">
      {/* Tier Toggles */}
      <div className="flex gap-2">
        {TIERS.map((tier) => (
          <button
            key={tier}
            onClick={() => toggleTier(tier)}
            className={`px-3 py-1 rounded-full text-sm font-semibold transition ${
              tiersShown[tier]
                ? 'bg-gray-600 text-white'
                : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
            }`}
          >
            {tier}
          </button>
        ))}
      </div>

      {/* Risk Toggle */}
      <button
        onClick={() => setShowRisk(!showRisk)}
        className={`px-3 py-1 rounded-full text-xs font-medium transition ${
          showRisk
            ? 'bg-red-500/70 text-white'
            : 'bg-gray-700 text-red-300 hover:bg-red-400/40 hover:text-white'
        }`}
      >
        {showRisk ? 'Risk: ON' : 'Risk: OFF'}
      </button>

      {/* Tag Filters */}
      <div className="flex gap-2">
        {TAGS.map((tag) => (
          <button
            key={tag}
            onClick={() => toggleTag(tag)}
            className={`px-3 py-1 rounded-full text-xs font-medium transition ${
              tagFilters.includes(tag)
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {tag}
          </button>
        ))}
      </div>

      {/* Sort Selector */}
      <div className="ml-auto">
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-gray-700 text-gray-200 text-sm px-3 py-1 rounded-md"
        >
          <option value="score">Sort: Score</option>
          <option value="symbol">Sort: Symbol</option>
        </select>
      </div>
    </div>
  );
}
