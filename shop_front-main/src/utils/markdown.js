import MarkdownIt from "markdown-it";

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

const defaultImageRenderer = md.renderer.rules.image;

md.renderer.rules.image = function (tokens, idx, options, env, self) {
  const token = tokens[idx];

  // get the src and alt
  const src = token.attrGet('src');
  const alt = token.content;

  // Add your own attributes (e.g., class, loading, width…)
  token.attrSet('loading', 'lazy');
  token.attrSet('class', 'my-image');
  token.attrSet('style', 'min-width: 50%;max-width: 100%; height: auto; display: block; margin: 5px auto; border-radius: 8px');

  // Render as usual with your modifications
  return self.renderToken(tokens, idx, options);
};

export default md;
