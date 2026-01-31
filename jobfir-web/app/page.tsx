"use client";

import { useMemo, useState } from "react";

type AnalyzeResult = {
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  missing_by_category?: {
    core?: string[];
    important?: string[];
    nice?: string[];
  };
  tailored_summary?: string[];
  keyword_suggestions?: string[];
  warnings?: string[];
  role?: string;
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJdFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [result, setResult] = useState<AnalyzeResult | null>(null);

  const canSubmit = useMemo(
    () => !!resumeFile && !!jdFile && !loading,
    [resumeFile, jdFile, loading]
  );

  function handleReset() {
    setResumeFile(null);
    setJdFile(null);
    setResult(null);
    setError("");
  }

  function downloadJSON(data: any) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "jobfit_report.json";
    a.click();
    URL.revokeObjectURL(url);
  }
  
  function downloadTXT(r: AnalyzeResult) {
    const lines: string[] = [];
  
    lines.push("JOBFIT REPORT");
    lines.push("====================");
    lines.push(`Match Score: ${r.score?.toFixed(1)}%`);
    lines.push("");
  
    if (r.role) lines.push(`Role: ${r.role}`);
    lines.push("");
  
    lines.push(`Matched Skills (${r.matched_skills?.length ?? 0}):`);
    (r.matched_skills ?? []).forEach((s) => lines.push(`- ${s}`));
    lines.push("");
  
    lines.push(`Missing Skills (${r.missing_skills?.length ?? 0}):`);
    (r.missing_skills ?? []).forEach((s) => lines.push(`- ${s}`));
    lines.push("");
  
    if (r.missing_by_category) {
      lines.push("Missing Skills by Priority:");
      lines.push(`Core (${r.missing_by_category.core?.length ?? 0}):`);
      (r.missing_by_category.core ?? []).forEach((s) => lines.push(`- ${s}`));
      lines.push("");
  
      lines.push(`Important (${r.missing_by_category.important?.length ?? 0}):`);
      (r.missing_by_category.important ?? []).forEach((s) => lines.push(`- ${s}`));
      lines.push("");
  
      lines.push(`Nice-to-have (${r.missing_by_category.nice?.length ?? 0}):`);
      (r.missing_by_category.nice ?? []).forEach((s) => lines.push(`- ${s}`));
      lines.push("");
    }
  
    if (r.tailored_summary && r.tailored_summary.length > 0) {
      lines.push("Tailored Summary:");
      r.tailored_summary.forEach((l) => lines.push(`- ${l}`));
      lines.push("");
    }
  
    if (r.keyword_suggestions && r.keyword_suggestions.length > 0) {
      lines.push("Keyword Suggestions:");
      r.keyword_suggestions.forEach((k) => lines.push(`- ${k}`));
      lines.push("");
    }
  
    const content = lines.join("\n");
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "jobfit_report.txt";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function handleAnalyze() {
    setError("");
    setResult(null);

    if (!resumeFile || !jdFile) {
      setError("Please upload both Resume PDF and Job Description PDF.");
      return;
    }

    if (
      !resumeFile.name.toLowerCase().endsWith(".pdf") ||
      !jdFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Only PDF files are allowed.");
      return;
    }

    try {
      setLoading(true);

      const form = new FormData();
      form.append("resume", resumeFile);
      form.append("jd", jdFile);

      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: form,
      });

      const data = await res.json().catch(() => null);

      if (!res.ok) {
        const detail =
          typeof data?.detail === "string"
            ? data.detail
            : Array.isArray(data?.detail)
            ? "Validation error: please upload both PDFs."
            : "Request failed. Please try again.";
        throw new Error(detail);
      }

      setResult(data as AnalyzeResult);
    } catch (e: any) {
      setError(e?.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Top bar */}
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-black text-white flex items-center justify-center font-bold">
              JF
            </div>
            <div>
              <div className="text-lg font-semibold text-gray-900">JobFit</div>
              <div className="text-xs text-gray-500">
                Resume ↔ JD match analyzer
              </div>
            </div>
          </div>

          <div className="text-xs text-gray-500">
            API:{" "}
            <span className="font-medium text-gray-700">{API_BASE}</span>
          </div>
        </div>
      </header>

      {/* Body */}
      <div className="mx-auto max-w-5xl px-4 py-10">
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Left: Upload */}
          <section className="bg-white rounded-xl shadow-md border p-6">
            <h1 className="text-2xl font-bold text-gray-900">
              Check your match before you apply
            </h1>
            <p className="mt-2 text-gray-600">
              Upload your Resume PDF and Job Description PDF. JobFit will compute
              a skill match score and suggest what to improve.
            </p>

            <div className="mt-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Resume (PDF)
                </label>
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  className="mt-1 w-full rounded-md border border-gray-300 p-2"
                  onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)}
                />
                {resumeFile && (
                  <p className="mt-1 text-xs text-gray-500">
                    Selected:{" "}
                    <span className="font-medium">{resumeFile.name}</span>
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Job Description (PDF)
                </label>
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  className="mt-1 w-full rounded-md border border-gray-300 p-2"
                  onChange={(e) => setJdFile(e.target.files?.[0] ?? null)}
                />
                {jdFile && (
                  <p className="mt-1 text-xs text-gray-500">
                    Selected: <span className="font-medium">{jdFile.name}</span>
                  </p>
                )}
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  onClick={handleAnalyze}
                  disabled={!canSubmit}
                  className={`flex-1 py-2 rounded-md transition flex items-center justify-center gap-2 ${
                    canSubmit
                      ? "bg-black text-white hover:bg-gray-800"
                      : "bg-gray-200 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  {loading ? <Spinner /> : null}
                  {loading ? "Analyzing..." : "Analyze Match"}
                </button>

                <button
                  onClick={handleReset}
                  disabled={loading}
                  className="px-4 py-2 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-50 transition disabled:opacity-50"
                >
                  Reset
                </button>
              </div>

              {error && (
                <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                  {error}
                </div>
              )}

              <p className="text-xs text-gray-500 pt-2">
                Privacy: Files are processed in-memory and not stored. This tool
                helps optimize applications but does not guarantee hiring.
              </p>
            </div>
          </section>

          {/* Right: Results */}
          <section className="bg-white rounded-xl shadow-md border p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Results</h2>
                <p className="text-sm text-gray-600 mt-1">
                  Upload files and click analyze to see your match score and
                  suggestions.
                </p>
              </div>

              {result && (
                <div className="flex flex-col items-end gap-2">
                  <div className="inline-flex items-center gap-2">
                    <span className="text-sm text-gray-600">Match</span>
                    <span className="rounded-full bg-black px-3 py-1 text-sm font-semibold text-white">
                      {result.score?.toFixed(1)}%
                    </span>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => downloadTXT(result)}
                      className="rounded-md border px-3 py-1 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Download TXT
                    </button>

                    <button
                      onClick={() => downloadJSON(result)}
                      className="rounded-md border px-3 py-1 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Download JSON
                    </button>
                  </div>
                </div>
              )}
            </div>

            {!result ? (
              <div className="mt-6 rounded-lg border border-dashed p-6 text-sm text-gray-500">
                No analysis yet. Upload PDFs and click <b>Analyze Match</b>.
              </div>
            ) : (
              <div className="mt-6 space-y-6">
                {/* Warnings */}
                {result.warnings && result.warnings.length > 0 && (
                  <div className="rounded-md border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
                    <div className="font-medium">Warnings</div>
                    <ul className="mt-1 list-disc pl-5">
                      {result.warnings.map((w, i) => (
                        <li key={i}>{w}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="grid gap-4 md:grid-cols-2">
                  <Card title={`Matched Skills (${result.matched_skills?.length ?? 0})`}>
                    <BulletList items={result.matched_skills ?? []} emptyText="None" />
                  </Card>

                  <Card title={`Missing Skills (${result.missing_skills?.length ?? 0})`}>
                    <BulletList items={result.missing_skills ?? []} emptyText="None" />
                  </Card>
                </div>

                {/* Priority */}
                {result.missing_by_category && (
                  <Card title="Missing Skills by Priority">
                    <div className="grid gap-3 md:grid-cols-3">
                      <PriorityCol
                        title="Core"
                        items={result.missing_by_category.core ?? []}
                      />
                      <PriorityCol
                        title="Important"
                        items={result.missing_by_category.important ?? []}
                      />
                      <PriorityCol
                        title="Nice-to-have"
                        items={result.missing_by_category.nice ?? []}
                      />
                    </div>
                  </Card>
                )}

                {/* Summary */}
                {result.tailored_summary && result.tailored_summary.length > 0 && (
                  <Card title={`Tailored Summary${result.role ? ` (${result.role})` : ""}`}>
                    <BulletList items={result.tailored_summary} emptyText="—" />
                  </Card>
                )}

                {/* Keywords */}
                {result.keyword_suggestions && result.keyword_suggestions.length > 0 && (
                  <Card title="Keyword Suggestions">
                    <div className="flex flex-wrap gap-2">
                      {result.keyword_suggestions.map((kw) => (
                        <span
                          key={kw}
                          className="rounded-full border bg-gray-50 px-3 py-1 text-sm text-gray-700"
                        >
                          {kw}
                        </span>
                      ))}
                    </div>
                  </Card>
                )}
              </div>
            )}
          </section>
        </div>

        <footer className="mt-10 text-center text-xs text-gray-400">
          Built locally • Frontend: localhost:3000 • Backend: localhost:8000
        </footer>
      </div>
    </main>
  );
}

function Spinner() {
  return (
    <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
  );
}

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg border p-4">
      <div className="font-semibold text-gray-900">{title}</div>
      <div className="mt-2">{children}</div>
    </div>
  );
}

function BulletList({ items, emptyText }: { items: string[]; emptyText: string }) {
  if (!items || items.length === 0) {
    return <p className="text-sm text-gray-500">{emptyText}</p>;
  }
  return (
    <ul className="list-disc pl-5 text-sm text-gray-700 space-y-1">
      {items.map((s, i) => (
        <li key={`${s}-${i}`}>{s}</li>
      ))}
    </ul>
  );
}

function PriorityCol({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-md bg-gray-50 p-3">
      <div className="text-sm font-semibold text-gray-900">{title}</div>
      {items.length === 0 ? (
        <p className="mt-2 text-sm text-gray-500">None</p>
      ) : (
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-700 space-y-1">
          {items.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
      )}
    </div>
  );
}