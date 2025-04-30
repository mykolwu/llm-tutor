import { Chroma } from "langchain/vectorstores/chroma";
import { OpenAIEmbeddings } from "@langchain/openai";
import * as fs from "fs";
import * as path from "path";

// Constants
const CHROMA_DB_DIR = path.join(process.cwd(), "chroma_db");
const COLLECTION_NAME = "coding_tutor_rag";

// Helper: Build Chroma DB if it doesn't exist
async function buildChromaIfNotExists() {
  if (!fs.existsSync(CHROMA_DB_DIR)) {
    console.log("No Chroma DB found. Building embeddings...");

    // Dynamically import the indexing script
    const { default: indexDocuments } = await import("../../scripts/indexDocuments");
    await indexDocuments();
  }
}

// Main function: Get retriever
export async function getRetriever() {
  await buildChromaIfNotExists();

  const vectorStore = await Chroma.fromExistingCollection(
    new OpenAIEmbeddings({
      modelName: "text-embedding-ada-002",
    }),
    {
      collectionName: COLLECTION_NAME,
      persistDirectory: CHROMA_DB_DIR,
    }
  );

  return vectorStore.asRetriever();
}
