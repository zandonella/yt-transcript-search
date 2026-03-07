import { useState } from 'react';
import SearchBar from './components/SearchBar';
import ResultCard from './components/ResultCard';

export interface SearchResult {
    score: number;
    video_id: string;
    start_time: string;
    end_time?: string;
    start_seconds: number;
    end_seconds?: number;
    text: string;
    url: string;
}

interface SearchResponse {
    query: string;
    index: string;
    count: number;
    results: SearchResult[];
    error?: string;
}

function getYouTubeThumbnail(videoId: string) {
    return `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
}

export default function App() {
    const [indexName, setIndexName] = useState('');
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [count, setCount] = useState<number | null>(null);

    async function handleSearch(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault();

        setLoading(true);
        setError('');

        try {
            const res = await fetch(
                `http://127.0.0.1:5000/search?index=${encodeURIComponent(indexName)}&q=${encodeURIComponent(query)}`,
            );

            const data: SearchResponse = await res.json();

            if (!res.ok) {
                setError(data.error || 'Search failed.');
                setResults([]);
                setCount(null);
                return;
            }

            setResults(data.results || []);
            setCount(data.count ?? 0);
        } catch (err) {
            setError(
                err instanceof Error ? err.message : 'Something went wrong.',
            );
            setResults([]);
            setCount(null);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100">
            <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                        Transcript Search
                    </h1>
                    {/* <p className="mt-2 text-sm text-zinc-400 sm:text-base">
                        Search your Elasticsearch transcript index and open
                        matching clips on YouTube.
                    </p> */}
                </div>
                <SearchBar
                    indexName={indexName}
                    setIndexName={setIndexName}
                    query={query}
                    setQuery={setQuery}
                    loading={loading}
                    handleSearch={handleSearch}
                />

                {error && (
                    <div className="mb-6 rounded-2xl border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
                        {error}
                    </div>
                )}

                {count !== null && !error && (
                    <div className="mb-6 text-sm text-zinc-400">
                        Found{' '}
                        <span className="font-semibold text-zinc-200">
                            {count}
                        </span>{' '}
                        result{count === 1 ? '' : 's'}
                    </div>
                )}

                <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
                    {results.map((result, i) => (
                        <ResultCard
                            key={i}
                            result={result}
                            thumbnail={getYouTubeThumbnail(result.video_id)}
                        />
                    ))}
                </div>

                {!loading && count === 0 && !error && (
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/60 px-6 py-10 text-center text-zinc-400">
                        No results found.
                    </div>
                )}
            </div>
        </div>
    );
}
