import type { SearchResult } from '.././App';
import { LuArrowRight } from 'react-icons/lu';

interface ResultCardProps {
    result: SearchResult;
    thumbnail: string;
}

export default function ResultCard({ result, thumbnail }: ResultCardProps) {
    return (
        <>
            <a
                href={result.url}
                target="_blank"
                rel="noreferrer"
                className="group overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 shadow-lg transition hover:-translate-y-1 hover:border-zinc-700 hover:shadow-2xl"
            >
                <div className="aspect-video w-full overflow-hidden bg-zinc-800">
                    <img
                        src={thumbnail}
                        alt={`Thumbnail for ${result.video_id}`}
                        className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]"
                        loading="lazy"
                        onError={(e) => {
                            e.currentTarget.style.display = 'none';
                        }}
                    />
                </div>

                <div className="p-4">
                    <div className="mb-3 flex items-center justify-between gap-3 text-xs text-zinc-400">
                        <span className="rounded-full border border-zinc-700 px-2 py-1">
                            Score {result.score.toFixed(2)}
                        </span>
                        <span>{result.start_time}</span>
                    </div>

                    <p className="mb-4 line-clamp-5 text-sm leading-6 text-zinc-200">
                        {result.text}
                    </p>

                    <div className="flex items-center justify-between text-xs text-zinc-500">
                        <span className="truncate">{result.video_id}</span>
                        <span className="flex items-center font-medium text-zinc-300 group-hover:text-white">
                            Watch <LuArrowRight size={24} className="inline" />
                        </span>
                    </div>
                </div>
            </a>
        </>
    );
}
