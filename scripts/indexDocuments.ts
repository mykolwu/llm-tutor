import { Chroma } from "langchain/vectorstores/chroma";
import { OpenAIEmbeddings } from "@langchain/openai";
import * as fs from "fs";
import * as path from "path";

const DATA_DIR = path.join(process.cwd(), "data"); // Your json files directory
const CHROMA_DB_DIR = path.join(process.cwd(), "chroma_db"); // Where to persist
const COLLECTION_NAME = "coding_tutor_rag"; // Collection name in chroma

async function loadDocuments(): Promise<{ id: string; content: string; metadata: any }[]> {
  const files = fs.readdirSync(DATA_DIR);
  const allChunks: { id: string; content: string; metadata: any }[] = [];

  for (const file of files) {
    if (file.endsWith(".json")) {
      const raw = fs.readFileSync(path.join(DATA_DIR, file), "utf-8");
      const json = JSON.parse(raw);

      // Derive 'source' field from filename (e.g., chap_2.5 from chap_2.5.json)
      const source = file.replace(".json", "");

      if (Array.isArray(json)) {
        json.forEach((entry, i) => {
          if (entry.content && entry.type) {
            let mappedType = entry.type;
            if (entry.type === "h2") mappedType = "section_title";
            else if (entry.type === "h3") mappedType = "subsection";

            allChunks.push({
              id: `${file}#${i}`, // for uniqueness
              content: entry.content,
              metadata: {
                type: mappedType,
                source: source,
              },
            });
          }
        });
      }
    }
  }

  return allChunks;
}

export default async function main() {
  console.log("Loading documents...");
  const documents = await loadDocuments();

  const embeddingModel = new OpenAIEmbeddings({
    modelName: "text-embedding-ada-002", // Or other if you want
  });

  console.log("Embedding and saving to Chroma...");
  const vectorStore = await Chroma.fromTexts(
    documents.map((doc) => doc.content),
    documents.map((doc) => ({
      id: doc.id,
      ...doc.metadata, // type + source
    })),
    embeddingModel,
    {
      collectionName: COLLECTION_NAME,
      persistDirectory: CHROMA_DB_DIR,
    }
  );

  await vectorStore.persist();
  console.log(`✅ Successfully indexed ${documents.length} chunks into ${CHROMA_DB_DIR}`);
}

main().catch((err) => {
  console.error("Error indexing documents:", err);
  process.exit(1);
});
