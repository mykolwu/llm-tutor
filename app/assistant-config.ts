export let assistantAId = "asst_4hJw4hJkX0nV55fGFk8ZqTOz"; // set your assistant ID here
export let assistantBId = "asst_UAFPPt9P9GDUFAh7WTMF63nT"; // set your assistant ID here
export let assistantId = ""; // set your assistant ID here
if (assistantId === "") {
  assistantId = process.env.OPENAI_ASSISTANT_ID;
}
