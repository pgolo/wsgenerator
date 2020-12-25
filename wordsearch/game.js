g_word = '';
g_words = [];

function recordLetter(r, c, letter) {
  g_word += letter;
  alert(g_word);
}

function render(words, puzzle) {
  g_words = words;
  var wordbank_max_rows = 1;
  var wordbank_max_cols = 3;
  var wordbank_row = 0;
  var wordbank_col = 0;
  var wordbank_font_size = 0.6;
  var wordbank_height = wordbank_max_rows * Math.ceil(words.length / (wordbank_max_rows * wordbank_max_cols)) * wordbank_font_size;
  var grid = []; var letters = []; var buttons = [];
  var x_margin = 1; var y_margin = 1;
  var x = x_margin; var y = y_margin;
  var cell_size = 1; var font_size = 0.8;
  var svg_width = (puzzle[0].length + 1) * cell_size + x_margin * 2;
  var svg_height = (puzzle.length + 1) * cell_size + y_margin * 2 + wordbank_height + 1;
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", svg_width + "cm");
  svg.setAttribute("height", svg_height + "cm");
  document.body.appendChild(svg);
  for (r = 0; r < puzzle.length; r++) {
    x = x_margin;
    grid.push([]); letters.push([]); buttons.push([]);
    for (c = 0; c < puzzle[r].length; c++) {
      grid[grid.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));
      grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("x", x + "cm");
      grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("y", y + "cm");
      grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("width", cell_size + "cm");
      grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("height", cell_size + "cm");
      grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("shape-rendering", "crispEdges");
      if (r * c != 0) {
        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("style", "fill:white;stroke:black;stroke-width:1px");
      } else {
        grid[grid.length - 1][grid[grid.length - 1].length - 1].setAttribute("style", "fill:white;stroke:black;stroke-width:0px");
      }
      letters[letters.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "text"));
      letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("x", x + cell_size / 2 + "cm");
      letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("y", y + cell_size / 2 + "cm");
      if (r * c != 0) {
        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("font-size", font_size + "cm");
      } else {
        letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("font-size", font_size / 2 + "cm");
      }
      letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("dominant-baseline", "middle");
      letters[letters.length - 1][letters[letters.length - 1].length - 1].setAttribute("text-anchor", "middle");
      letters[letters.length - 1][letters[letters.length - 1].length - 1].appendChild(document.createTextNode(puzzle[r][c]));
      buttons[buttons.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));
      buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("x", x + "cm");
      buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("y", y + "cm");
      buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("width", cell_size + "cm");
      buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("height", cell_size + "cm");
      buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("style", "fill:white;opacity:0%;stroke-width:0px");
      if (r * c != 0) {
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseover", "evt.target.setAttribute('style', 'fill:white;opacity:50%;stroke-width:0px');");
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseout", "evt.target.setAttribute('style', 'fill:white;opacity:0%;stroke-width:0px');");
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmousedown", "recordLetter(" + r + ", " + c + ", '" + puzzle[r][c] + "');");
      }
      svg.appendChild(grid[grid.length - 1][grid[grid.length - 1].length - 1]);
      svg.appendChild(letters[letters.length - 1][letters[letters.length - 1].length - 1]);
      svg.appendChild(buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1]);
      x += cell_size;
    }
    y += cell_size;
  }
  var frame = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  frame.setAttribute("width", (puzzle[0].length + 1) * cell_size + x_margin * 2 + "cm");
  frame.setAttribute("height", (puzzle.length + 1) * cell_size + x_margin * 2 + "cm");
  frame.setAttribute("style", "fill:none;stroke:black;stroke-width:1px");
  frame.setAttribute("rx", "10");
  frame.setAttribute("ry", "10");
  svg.appendChild(frame);

  var wordbank = {};
  var wordbank_group = 0;
  for (i = 0; i < g_words.length; i++) {
    word = g_words[i];
    wordbank[word] = document.createElementNS("http://www.w3.org/2000/svg", "text");
    wordbank[word].setAttribute("x", wordbank_col * svg_width / wordbank_max_cols + "cm");
    wordbank[word].setAttribute("y", cell_size * puzzle.length + 4 + wordbank_row * wordbank_font_size + "cm");
    wordbank[word].setAttribute("font-size", wordbank_font_size + "cm");
    wordbank[word].appendChild(document.createTextNode(word));
    svg.appendChild(wordbank[word]);
    wordbank_row += 1;
    if (wordbank_row == (wordbank_group + 1) * wordbank_max_rows) {
      wordbank_col += 1;
      wordbank_row = wordbank_group * wordbank_max_rows;
    }
    if (wordbank_col == wordbank_max_cols) {
      wordbank_col = 0;
      wordbank_group += 1;
      wordbank_row += wordbank_max_rows;
    }
  }
}
