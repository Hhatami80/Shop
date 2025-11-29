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

const defaultHeadingOpen =
  md.renderer.rules.heading_open ||
  function (tokens, idx, opts, env, self) {
    return self.renderToken(tokens, idx, opts);
  };

md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx];

  // Only modify <h2>
  if (token.tag === "h2") {
    // Add class or inline styles
    token.attrSet("class", "my-h2");
    token.attrSet(
      "style",
      "font-size: 22px; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #444;"
    );
  }

  // Render normally afterwards
  return defaultHeadingOpen(tokens, idx, options, env, self);
};

const defaultParagraphOpen =
  md.renderer.rules.paragraph_open ||
  function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };

md.renderer.rules.paragraph_open = function (tokens, idx, options, env, self) {
  const token = tokens[idx];

  // Add class + styles
  token.attrSet("class", "my-paragraph");
  token.attrSet(
    "style",
    "line-height: 1.75; margin: 0.75rem 0; font-size: 15px; color: #333;"
  );

  return defaultParagraphOpen(tokens, idx, options, env, self);
};

export default md;
