# Tribunal do Amor — votação ao vivo

Votação em tempo real para o evento "Tribunal do Amor" (2gether · #CCRP minha casa). Os participantes entram pelo
QR Code ou pelo link e votam pelo celular. O telão mostra as barras subindo ao vivo, o cronômetro, a opção mais
votada de cada caso e o veredito final.

**Não há resposta certa ou errada.** Cada caso é uma enquete: o resultado é o percentual de votos de cada opção,
com destaque para a mais votada (ou para as empatadas).

Servidor único em Node.js, **sem dependências** (nada de `npm install`). Precisa de Node 18 ou mais novo.

## Rodar

```bash
node server.js
```

O terminal mostra os três endereços:

| Quem usa | Endereço | Para quê |
|---|---|---|
| Participantes | `/` | votam pelo celular (é o que o QR Code abre) |
| Telão | `/screen?key=SUA_CHAVE` | QR Code, barras ao vivo, cronômetro, mais votada, veredito |
| Apresentador | `/admin?key=SUA_CHAVE` | controle pelo celular ou por outro computador |

A chave de admin é gerada a cada início. Para fixar uma (recomendado), defina `ADMIN_KEY`:

```bash
ADMIN_KEY=uma-chave-longa node server.js
```

## Os casos

Os 5 casos do evento estão em `questions.json`. Formato (de 2 a 8 opções por caso; o servidor avisa se algo estiver errado):

```json
{
  "title": "Tribunal do Amor",
  "voteSeconds": 40,
  "questions": [
    {
      "text": "Como o casal deve administrar o dinheiro?",
      "options": ["Primeira opção", "Segunda", "Terceira", "Quarta"]
    }
  ]
}
```

O telão monta o título como na arte: "CASO 1 - " + o texto da pergunta, e diminui a fonte sozinho quando a pergunta
ou as opções são longas. Ponto final no fim das opções é removido na exibição.

## Como operar no evento

1. Abra o telão (`/screen?key=...`) no computador ligado ao projetor e aperte **F** para tela cheia.
   A capa com o QR Code e o contador de pessoas conectadas aparecem sozinhos.
2. Quando todos tiverem entrado, **Começar**: o caso 1 aparece (hora de lê-lo em voz alta). Os celulares mostram o caso e aguardam.
3. **Iniciar votação**: o cronômetro de 40 s corre no telão e nos celulares; as barras e percentuais sobem em tempo real.
4. Ao zerar, a votação **encerra sozinha**: o telão destaca a **mais votada** (ou o empate) e esmaece as demais;
   cada celular passa a mostrar o percentual de todas as opções, com a mais votada e o voto da pessoa marcados.
5. **Próximo caso**. Depois do último, **Veredito final**: o telão mostra a opção mais votada de cada caso.

Controles: botões que aparecem ao mexer o mouse no telão, ou o `/admin` no celular.
Atalhos no telão: **Espaço / Enter / →** = ação principal (começar, iniciar, encerrar, próximo),
**←** volta (antes de iniciar a votação), **F** tela cheia.
Também há **Refazer caso** (apaga os votos dele) e **Reiniciar tudo** — ambos pedem confirmação.

## Colocar no ar (grátis)

Os participantes precisam de um endereço público com HTTPS. O caminho gratuito que funciona para este projeto é o **Render**
(plano Free). Planos gratuitos mudam: confira antes do evento.

1. Crie um repositório no GitHub com esta pasta (pode ser privado). Use um repositório novo, separado do evento anterior.
2. No [Render](https://render.com): **New → Blueprint** (ele lê o `render.yaml` e já escolhe o plano Free) e aponte para o repositório.
   Sem Blueprint: **New → Web Service**, build `npm install`, start `node server.js`, instância **Free**.
3. Em **Environment**, adicione `ADMIN_KEY` com uma chave só de letras e números (12+ caracteres).
4. Quando terminar o deploy, abra o telão pelo endereço público: `https://SEU-APP.onrender.com/screen?key=SUA_CHAVE`.
   O QR Code já sai apontando para esse endereço.

Cuidados com o plano gratuito:

- **Hiberna após 15 min sem tráfego de entrada** e leva cerca de 1 min para acordar. O telão e o `/admin` fazem um ping a cada
  4 min enquanto abertos; mesmo assim, abra o telão uns 15 minutos antes e deixe aberto.
- **O Render pode reiniciar o serviço a qualquer momento** e o disco é temporário: se isso acontecer no meio do evento, a votação
  volta ao início. Por isso, faça o teste geral antes e use **Reiniciar tudo** para zerar antes de começar.

**O que não serve para este projeto:** o *quick tunnel* do Cloudflare (não suporta a conexão em tempo real usada aqui, SSE)
e a Vercel (estado em memória e conexões longas).

Se o endereço público for diferente do que o telão abre, defina `PUBLIC_URL=https://seu-endereco`.

## Configurações (variáveis de ambiente)

| Variável | Padrão | O que faz |
|---|---|---|
| `PORT` | 3000 | porta do servidor |
| `ADMIN_KEY` | aleatória | chave do telão com controles e do `/admin` |
| `PUBLIC_URL` | endereço aberto no telão | endereço que vai no QR Code |
| `VOTE_SECONDS` | 40 (ou o de `questions.json`) | duração de cada votação |
| `QUESTIONS_FILE` | `questions.json` | outro arquivo de perguntas |
| `STATE_FILE` | `data/state.json` | onde o andamento é salvo |

O andamento (fase, votos) é salvo em disco a cada 2 s: se o servidor reiniciar no meio do evento, ele continua
de onde parou (e se o cronômetro já tiver vencido, a votação é encerrada).

## Boas práticas para 300+ pessoas

- **Internet do local**: Wi-Fi de evento costuma engasgar com 300 celulares. Avise que quem tiver 4G/5G pode usar os dados móveis.
- **Um voto por aparelho** por caso (identificação guardada no navegador). Abrir em aba anônima permite votar de novo; para um evento único isso costuma ser aceitável.
- Os celulares **não veem a parcial** durante a votação (evita influenciar quem ainda não votou); o resultado aparece neles só depois de encerrar.
- **Teste antes**: `node test/load.mjs` simula 300 participantes votando ao mesmo tempo e confere contagem, mais votada, empate, voto duplicado, cronômetro e reconexão.

## Identidade visual

Aplicada a partir das artes "Tribunal do Amor" (capa vermelha e base creme, 1920×1200):

- `public/img/capa.jpg` — fundo do telão na abertura (capa com corações e o texto do QR Code).
- `public/img/fundo.jpg` — fundo creme dos casos e do veredito (com "2gether" e os selos do rodapé).
- `public/img/gavel.png` — martelo recortado da arte, sobreposto à faixa vinho da pergunta.
- `public/img/capa-celular.jpg` e `fundo-celular.jpg` — versões leves para os celulares.
- Cores e fontes ficam no topo de `public/theme.css`.
- Se as artes mudarem, coloque os 4 JPGs novos na pasta "Tribunal do Amor" (mesmos nomes) e rode
  `python3 tools/gen_assets.py "../" public/img` para recriar as imagens (precisa de Python com Pillow).

O telão é desenhado em 1920×1200 (o formato das artes) e se ajusta a qualquer tela; num projetor 16:9 aparecem faixas
finas nas laterais, na cor do fundo.

**Fontes:** Inter Tight (títulos e opções) e Playfair Display itálico (o "Caso 1", "do amor"), carregadas do Google Fonts.
Precisam de internet no telão e nos celulares; sem ela, entram fontes do sistema (Helvetica/Arial e Georgia).
Se tiverem os arquivos das fontes originais da arte, dá para trocá-las em `--sans` e `--serif` no `theme.css`.

## Créditos

O QR Code é gerado no navegador com o codificador "QRCode for JavaScript" de Kazuhiko Arase (licença MIT),
em `public/vendor/qrcode.js`. "QR Code" é marca registrada da DENSO WAVE INCORPORATED.
