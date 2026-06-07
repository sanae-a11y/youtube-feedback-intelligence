"use client";

import { useState } from "react";
import { analyzeVideo, Analysis } from "@/lib/api";
import SentimentChart from "@/components/SentimentChart";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState<Analysis | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const data = await analyzeVideo(url);
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="hero">
        <span className="badge">Soft AI Studio · Qwen + FastAPI + Next.js</span>

        <h1>YouTube Feedback Intelligence</h1>

        <p>
          A pastel AI dashboard that turns YouTube comments and transcripts into
          pretty, clear creator insights.
        </p>

        <form className="form" onSubmit={handleSubmit}>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste a YouTube video link"
            required
          />

          <button disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}
      </section>

      {analysis && (
        <section>
          <div className="grid">
            <div className="card">
              {analysis.metadata.thumbnail_url && (
                <img
                  className="thumbnail"
                  src={analysis.metadata.thumbnail_url}
                  alt="Video thumbnail"
                />
              )}

              <h2>{analysis.metadata.title}</h2>
              <p>{analysis.metadata.channel_title}</p>

              <span className="metric-pill">
                {analysis.raw_comment_count} comments analyzed · Transcript{" "}
                {analysis.transcript_available ? "available" : "unavailable"}
              </span>
            </div>

            <div className="card">
              <h2>Audience Sentiment</h2>
              <SentimentChart sentiment={analysis.sentiment} />
            </div>
          </div>

          <div className="grid">
            <InsightCard title="💖 Best parts" items={analysis.best_parts} />
            <InsightCard
              title="🌷 Things to enhance"
              items={analysis.improvements}
            />
            <InsightCard
              title="🎀 Viewer requests"
              items={analysis.viewer_requests}
            />
          </div>

          <div className="card" style={{ marginTop: 18 }}>
            <h2>✨ Next video ideas</h2>

            {analysis.next_video_ideas.map((idea, index) => (
              <div className="idea" key={index}>
                <h3>
                  {idea.title} — {idea.confidence}%
                </h3>
                <p>{idea.why}</p>
              </div>
            ))}
          </div>

          <div className="card" style={{ marginTop: 18 }}>
            <h2>💌 Creator advice</h2>
            <p>{analysis.creator_advice}</p>
          </div>
        </section>
      )}

      <footer
        style={{
          marginTop: "70px",
          padding: "32px 20px",
          textAlign: "center",
          borderRadius: "28px",
          background: "rgba(255, 255, 255, 0.45)",
          backdropFilter: "blur(18px)",
          boxShadow: "0 20px 60px rgba(236, 72, 153, 0.15)",
        }}
      >
        <p
          style={{
            color: "#7c3a6b",
            opacity: 0.9,
            fontWeight: 600,
            marginBottom: "12px",
          }}
        >
          Built with 💖 by Sanae Attak
        </p>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "22px",
            flexWrap: "wrap",
          }}
        >
          <a
            href="https://github.com/sanae-a11y"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#d946ef",
              textDecoration: "none",
              fontWeight: 700,
            }}
          >
            GitHub
          </a>

          <a
            href="https://www.linkedin.com/in/sanaeattak/"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#d946ef",
              textDecoration: "none",
              fontWeight: 700,
            }}
          >
            LinkedIn
          </a>
        </div>
      </footer>
    </main>
  );
}

function InsightCard({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="card">
      <h2>{title}</h2>

      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}