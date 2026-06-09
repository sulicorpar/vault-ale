const Anthropic = require("@anthropic-ai/sdk");

const apiKey = process.env.CLAUDE_API_KEY;

if (!apiKey) {
  console.error("❌ Erro: CLAUDE_API_KEY não configurada!");
  console.error("Execute: export CLAUDE_API_KEY=sk-ant-...");
  process.exit(1);
}

const client = new Anthropic({
  apiKey: apiKey
});

console.log("🔑 Chave carregada: " + apiKey.substring(0, 20) + "...");

const SYSTEM_PROMPT = `Você é MORTIMER, Super Assistente Pessoal de Alejandro Sulichin (ADS Consultor).

VOCÊ TEM ACESSO COMPLETO A VAULT-ALE e faz tudo: campanhas, posts, propostas, automações, análises.

Sempre responda em JSON estruturado.
Seja direto e acionável.
`;

async function mortimer(comando) {
  try {
    console.log(`\n🤖 MORTIMER processando...\n`);
    
    const response = await client.messages.create({
      model: "claude-opus-4-1",
      max_tokens: 2048,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: "user",
          content: comando
        }
      ]
    });

    const resposta = response.content[0].text;
    
    console.log("\n✅ Mortimer respondeu:\n");
    console.log(resposta);
    
  } catch (error) {
    console.error("\n❌ Erro:", error.message);
  }
}

if (require.main === module) {
  const comando = process.argv.slice(2).join(" ");
  if (!comando) {
    console.log(`\n🤖 MORTIMER 2.0\n`);
    process.exit(0);
  }
  mortimer(comando);
}

module.exports = { mortimer };
