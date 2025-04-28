import { assistantAId, assistantBId } from "@/app/assistant-config";
import { openai } from "@/app/openai";

export const runtime = "nodejs";

// Send a new message to a thread
export async function POST(request, { params: { threadId } }) {
  const { content } = await request.json();

  await openai.beta.threads.messages.create(threadId, {
    role: "user",
    content: content,
  });

  // Call Assistant A (non-stream) to get a complete first-pass
  await openai.beta.threads.runs.createAndPoll(threadId, {
    assistant_id: assistantAId,
  });

  // Now stream Assistant B, which sees both messages in the thread
  const streamB = openai.beta.threads.runs.stream(threadId, {
    assistant_id: assistantBId,
  });

  // Pipe B’s streaming response straight back to the client
  return new Response(streamB.toReadableStream());
}
//   const stream = openai.beta.threads.runs.stream(threadId, {
//     assistant_id: assistantId,
//   });

//   return new Response(stream.toReadableStream());
// }
