# Frontend CPI

## Direção visual

Interface editorial com fundo marfim, verde-oliva, tipografia Newsreader/DM Sans,
ícones SVG locais, imagens naturais e cards com bordas e sombras discretas.
O CSS público é independente do painel administrativo. A navegação, as perguntas
frequentes e os conteúdos continuam disponíveis sem JavaScript.

## Interações

- Revelação única de seções por IntersectionObserver, sem ocultar o conteúdo inicial.
- Rolagem suave, indicação da seção ativa e progresso de leitura.
- Transições entre páginas nos navegadores compatíveis com View Transitions.
- Menu móvel com dialog nativo: foco contido, Escape e retorno de foco ao botão.
- Preferência de movimento reduzido respeitada, inclusive quando muda durante a visita.
- Blog, eventos, artigos e erros compartilham o mesmo sistema visual.
- Depoimentos só são exibidos quando cadastrados e visíveis; o estado vazio apresenta
  a proposta do CPI. Não há métricas ou depoimentos ilustrativos apresentados como reais.

## Imagens

Geração realizada com a ferramenta integrada **imagegen**, sem uso da API/CLI.
A fotografia é ilustrativa e não representa mentores ou clientes reais.

- `app/static/images/jornada-casal.webp`: imagem principal, 1536 × 1024.
- `app/static/images/jornada-casal-768.webp`: variante responsiva, 768 × 512.
- `app/static/images/tempo-juntos.webp`: versão WebP otimizada da fotografia
  `sobre-bg.jpg` já existente no projeto.

Apenas conversão de formato e redimensionamento foram usados após a geração.

### Prompt da imagem principal

Use case: photorealistic-natural. Asset type: principal editorial lifestyle photograph for a Brazilian Christian marriage mentoring website, clean premium warm natural visual identity. Create a photorealistic candid photograph of one Brazilian married couple in their late 30s, woman with shoulder-length dark brown wavy hair in an ivory linen blouse, man with short dark hair and subtle beard in an olive linen shirt, walking closely together hand in hand on a quiet sunlit garden path. They are looking at each other with a subtle genuine relaxed smile, a tender everyday moment, not posing at the camera. Lush soft olive green trees and sun-dappled leaves, warm late afternoon light, slightly nostalgic fine film grain and natural skin texture, editorial magazine photography, soft highlights, subdued earthy colors, high-end but unpretentious. Landscape image 1536x1024, couple grouped together centrally with both bodies visible from knees up and ample garden surrounding them so image can also crop into a portrait 4:5. Faces crisp and authentic, realistic hands. No wedding dresses, no religious props, no lettering, no text, no watermark, no collage. This is an illustrative image, not real mentors or a testimonial.

## Desenvolvimento

O projeto continua usando Flask/Jinja, CSS e JavaScript nativos. Não há etapa de
build ou dependência adicional. A versão dos assets públicos no template base
evita que o navegador reutilize o CSS/JS da interface anterior.

## Validação

- `python -m unittest discover -s tests -v`: quatro testes de integração com banco
  temporário, cobrindo estados vazios, conteúdos publicados/ocultos, paginação,
  JSON-LD, âncoras, assets, páginas 404/500 e login com acesso ao painel.
- `node --check app/static/js/script.js` e `git diff --check`.
- Navegador: home, blog, artigo, eventos, apoio e login em 320, 768 e 1440 px,
  sem transbordamento horizontal; inspeção visual adicional em 390 px.
- Rolagem para âncoras, indicação da seção ativa, menu móvel, Escape, retorno e
  contenção de foco, e abertura das perguntas frequentes.
- Home em 320 px com scripts bloqueados: menu acessível e conteúdo visível.

Os dados usados para testar artigos, eventos e depoimentos ficam em um banco
temporário. Os testes não alteram o banco de conteúdo do projeto.
