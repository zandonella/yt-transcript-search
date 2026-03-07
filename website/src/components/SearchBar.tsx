interface SearchBarProps {
    indexName: string;
    setIndexName: React.Dispatch<React.SetStateAction<string>>;
    query: string;
    setQuery: React.Dispatch<React.SetStateAction<string>>;
    loading: boolean;
    handleSearch: (e: React.SubmitEvent<HTMLFormElement>) => Promise<void>;
}

export default function SearchBar({
    indexName,
    setIndexName,
    query,
    setQuery,
    loading,
    handleSearch,
}: SearchBarProps) {
    return (
        <form
            onSubmit={handleSearch}
            className="mb-8 grid gap-3 rounded-2xl border border-zinc-800 bg-zinc-900/70 p-4 shadow-lg sm:grid-cols-[180px_1fr_auto]"
        >
            <input
                type="text"
                value={indexName}
                onChange={(e) => setIndexName(e.target.value)}
                placeholder="Index name"
                className="rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 ring-0 outline-none placeholder:text-zinc-500 focus:border-zinc-500"
            />

            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for a quote, phrase, or topic..."
                className="rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 ring-0 outline-none placeholder:text-zinc-500 focus:border-zinc-500"
            />

            <button
                type="submit"
                disabled={loading}
                className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-zinc-900 transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {loading ? 'Searching...' : 'Search'}
            </button>
        </form>
    );
}
