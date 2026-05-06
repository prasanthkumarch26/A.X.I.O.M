import PaperCard from "@/components/PaperCard";
import SearchBar from "@/components/SearchBar";

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const params = await searchParams;
  const query = params.q;
  let results = [];

  if (query) {
    const response = await fetch(`http://127.0.0.1:8000/search?query=${query}`, {cache: "no-store"});
    results = await response.json();
  }
  return (
    <main className="min-h-screen flex flex-col px-4 py-6">
      <div className="flex flex-col items-center text-center mt-4">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-semibold">
          A<span className="text-red-500">.</span>X
          <span className="text-red-500">.</span>I
          <span className="text-red-500">.</span>O
          <span className="text-red-500">.</span>M
        </h1>

        <h2 className="text-xs sm:text-sm md:text-base text-gray-400 mt-2 max-w-md">
          Adaptive eXplanatory Intelligence for Optimization and Modeling
        </h2>

        <p className="text-xs sm:text-sm text-gray-500 mt-2">
          Thank you to arXiv for use of its open access interoperability.
        </p>
      </div>

      <div className="flex-1 w-full max-w-2xl mx-auto mt-6 space-y-4">
        {results.map((paper : any) => (
          <PaperCard key={paper.arxiv_id} paper={paper} />
        ))}
      </div>

      <SearchBar />
    </main>
  );
}
