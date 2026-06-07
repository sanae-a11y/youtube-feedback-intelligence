export type Analysis = {
  metadata: {
    title: string;
    thumbnail_url: string;
    channel_title: string;
    view_count: number;
  };

  sentiment: {
    positive: number;
    neutral: number;
    negative: number;
  };

  best_parts: string[];
  improvements: string[];
  viewer_requests: string[];

  next_video_ideas: {
    title: string;
    why: string;
    confidence: number;
  }[];

  creator_advice: string;

  raw_comment_count: number;
  transcript_available: boolean;
};

export async function analyzeVideo(videoUrl: string): Promise<Analysis> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const response = await fetch(`${apiUrl}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: videoUrl,
      language: "en",
      max_comments: 120,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to analyze video");
  }

  return await response.json();
}