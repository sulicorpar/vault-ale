// MORTIMER CLI - Modo Interativo
// Use com: node mortimer-cli.js

const readline = require("readline");
const { mortimer } = require("./mortimer");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function iniciar() {
  console.log(`
╔════════════════════════════════════════╗
║  🤖 MORTIMER 2.0 — Super Assistente  ║
║     Seu Assistente Pessoal IA          ║
╚════════════════════════════════════════╝

Digite seu comando ou 'sair' para encerrar
Tipo 'ajuda' para ver exemplos

  `);
  
  const executar = async () => {
    rl.question("mortimer> ", async (comando) => {
      if (comando.toLowerCase() === "sair") {
        console.log("\n👋 Até logo!\n");
        rl.close();
        return;
      }
      
      if (comando.toLowerCase() === "ajuda") {
        console.log(`
📚 EXEMPLOS DE COMANDOS:

CAMPANHAS:
  criar campanha Raio X, R$500/dia, SP, donos negócio
  diagnosticar Ojas, CPA alto, ROAS caindo
  otimizar campanha, pausar audiences ruins

CONTEÚDO:
  post instagram sobre SEO local para dentistas
  vídeo 60s roteiro, TikTok, hook marketing local
  newsletter sobre tráfego pago

PROPOSTAS:
  estruturar proposta para CRN-9, consultoria SEO, R$50k, 6 meses
  gerar orcamento para novo cliente e-commerce

AUTOMAÇÕES:
  criar automação WhatsApp para qualificar leads
  estruturar email sequence pós-venda

ANÁLISES:
  analisar concorrente, tema SEO local
  benchmark CPA média para dentistas SP

REUNIÕES/LEMBRETES:
  agendar reunião quinta 14h com Ojas, tema proposta
  lembrete quarta 17h revisar relatório, alta prioridade
  task obsidian enviar proposta segunda

TUDO JUNTO:
  campanha Raio X + posts + proposta + automação WhatsApp

  `);
        executar();
        return;
      }
      
      if (!comando.trim()) {
        executar();
        return;
      }
      
      await mortimer(comando);
      
      console.log("\n" + "─".repeat(50) + "\n");
      executar();
    });
  };
  
  executar();
}

iniciar();
