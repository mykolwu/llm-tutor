import { openai } from "@/app/openai";
import { getRetriever } from "@/app/api/rag";

export const runtime = "nodejs";

export async function POST(req: Request) {
  const body = await req.json();
  const query = body.query;

  if (!query) {
    return new Response("Query not provided", { status: 400 });
  }

  //  Use retriever to get relevant docs
  const retriever = await getRetriever();
  const docs = await retriever.getRelevantDocuments(query);

  const context = docs.map((doc) => `Source: ${doc.metadata.source}\nType: ${doc.metadata.type}\nContent: ${doc.pageContent}`).join("\n\n");

  //  Send to assistant with context
  const thread = await openai.beta.threads.create();
  const message = await openai.beta.threads.messages.create(thread.id, {
    role: "user",
    content: `${context}\n\nAnswer the question: ${query}`,
  });

  const run = await openai.beta.threads.runs.create(thread.id, {
    assistant_id: process.env.ASSISTANT_ID!,
  });

  return Response.json({ run, thread });
}
