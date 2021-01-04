var globals = {
  cell_size: 1,
  font_size: .8,
  wb_font_size: .6,
  wb_max_rows: 1,
  wb_max_cols: 3,
  puzzle_margin_x: 1,
  puzzle_margin_y: 1,
  frame_rx: 10,
  frame_ry: 10,
  word: '',
  wordbank: {},
  solution: {},
  highlighted: null,
  found: [],
  buttons: [],
  selected: [],
  selected_buttons: [],
  svg: document.createElementNS("http://www.w3.org/2000/svg", "svg"),
  styles: {
    "grid-header": "fill:white;stroke:black;stroke-width:0px",
    "grid-board": "fill:white;stroke:black;stroke-width:1px",
    "grid-frame": "fill:none;stroke:black;stroke-width:1px",
    "word-highlight": "stroke:red;stroke-width:2px",
    "word-crossout": "text-decoration:line-through",
    "button-over": "fill:white;opacity:50%;stroke-width:0px",
    "button-out": "fill:white;opacity:0%;stroke-width:0px",
    "button-selected": "fill:white;opacity:90%;stroke-width:0px"
  }
};

function maySelect(r, c) {
  if (globals.selected.length == 0) {
    return true;
  } else if (globals.selected.length == 1 && Math.abs(r - globals.selected[0].r) <= 1 && Math.abs(c - globals.selected[0].c) <= 1 && (r != globals.selected[0].r || c != globals.selected[0].c)) {
    return true;
  }
  else if (globals.selected.length > 1) {
    dr = globals.selected[1].r - globals.selected[0].r;
    dc = globals.selected[1].c - globals.selected[0].c;
    last_r = globals.selected[globals.selected.length-1].r;
    last_c = globals.selected[globals.selected.length-1].c;
    if (r - last_r == dr && c - last_c == dc) {
      return true;
    }
  }
  return false;
}

function flickerButton(r, c, style) {
  for (i = 0; i < globals.selected.length; i++) {
    if (globals.selected[i].r == r && globals.selected[i].c == c) {
      globals.buttons[r][c].setAttribute("style", globals.styles["button-selected"]);
      return;
    }
  }
  globals.buttons[r][c].setAttribute("style", globals.styles[style]);
  return;
}

function deselectAll() {
  globals.selected = [];
  for (i = 0; i < globals.selected_buttons.length; i++) {
    globals.selected_buttons[i].setAttribute("style", globals.styles["button-out"]);
  }
  globals.selected_buttons = [];
  globals.word = '';
}

function getButtonCenter(r, c) {
  button_x = parseFloat(globals.buttons[r][c].getAttribute("x"));
  button_y = parseFloat(globals.buttons[r][c].getAttribute("y"));
  button_w = parseFloat(globals.buttons[r][c].getAttribute("width"));
  button_h = parseFloat(globals.buttons[r][c].getAttribute("height"));
  return {
    x: button_x + button_w / 2,
    y: button_y + button_h / 2
  };
}

function rotate(x, y, x0, y0, theta) {
  theta = (theta - 0) * Math.PI / 180;
  return {
    x: (x - x0) * Math.cos(theta) + (y - y0) * Math.sin(theta) + x0,
    y: -(x - x0) * Math.sin(theta) + (y - y0) * Math.cos(theta) + y0
  };
}

function highlightFrame(x1, y1, x2, y2, radius, angle) {
  points = [];
  points.push([x1, y1, 0, -radius]);
  for (i = -Math.PI / 2; i > -3 * Math.PI / 2; i -= .1) {
    points.push([x1, y1, radius * Math.cos(i), radius * Math.sin(i)]);
  }
  points.push([x1, y1, 0, radius]);
  points.push([x2, y2, 0, radius]);
  for (i = Math.PI / 2; i > -Math.PI / 2; i -= .1) {
    points.push([x2, y2, radius * Math.cos(i), radius * Math.sin(i)]);
  }
  points.push([x2, y2, 0, -radius]);
  points.push([x1, y1, 0, -radius]);
  lines = [];
  for (i = 0; i < points.length - 1; i++) {
    from = rotate(points[i][0] + points[i][2], points[i][1] + points[i][3], points[i][0], points[i][1], angle);
    to = rotate(points[i+1][0] + points[i+1][2], points[i+1][1] + points[i+1][3], points[i+1][0], points[i+1][1], angle);
    lines.push(document.createElementNS("http://www.w3.org/2000/svg", "line"));
    lines[lines.length-1].setAttribute("style", globals.styles["word-highlight"]);
    lines[lines.length-1].setAttribute("x1", from.x + "cm");
    lines[lines.length-1].setAttribute("y1", from.y + "cm");
    lines[lines.length-1].setAttribute("x2", to.x + "cm");
    lines[lines.length-1].setAttribute("y2", to.y + "cm");
  }
  return lines;
}

function highlightWord(r1, c1, r2, c2) {
  centerButton1 = getButtonCenter(r1, c1);
  centerButton2 = getButtonCenter(r2, c2);
  if (centerButton1.y == centerButton2.y) {
    // horizontal
    angle = 0;
    if (centerButton1.x < centerButton2.x) {
      from = centerButton1;
      to = centerButton2;
    }
    else {
      from = centerButton2;
      to = centerButton1;
    }
  }
  else {
    if (centerButton1.x == centerButton2.x) {
      // vertical
      angle = -90;
      if (centerButton1.y < centerButton2.y) {
        from = centerButton1;
        to = centerButton2;
      }
      else {
        from = centerButton2;
        to = centerButton1;
      }
    }
    else {
      // diagonal
      if (centerButton1.x < centerButton2.x) {
        from = centerButton1;
        to = centerButton2;
      }
      else {
        from = centerButton2;
        to = centerButton1;
      }
      if (from.y < to.y) {
        angle = -45;
      }
      else {
        angle = 45;
      }
    }
  }
  frame = highlightFrame(from.x, from.y, to.x, to.y, globals.cell_size * .4, angle);
  for (i = 0; i < frame.length; i++) {
    globals.svg.appendChild(frame[i]);
  }
  return frame;
}

function locateWord(word) {
  r1 = globals.solution[word]['y1'];
  c1 = globals.solution[word]['x1'];
  r2 = globals.solution[word]['y2'];
  c2 = globals.solution[word]['x2'];
  globals.highlighted = highlightWord(r1, c1, r2, c2);
}

function hideWordFrame() {
  for (i = 0; i < globals.highlighted.length; i++) {
    globals.svg.removeChild(globals.highlighted[i]);
  }
  globals.highlighted = null;
}

function recordLetter(r, c, letter) {
  deselect = false;
  if (!maySelect(r, c)) {
    if (globals.selected.length == 1 && r == globals.selected[0].r && c == globals.selected[0].c) {
      deselect = true;
    }
    deselectAll();
  }
  if (!deselect) {
    globals.selected.push({r: r, c: c});
    globals.selected_buttons.push(globals.buttons[r][c]);
    flickerButton(r, c, 'button-selected');
    globals.word += letter;
    if (globals.wordbank[globals.word] != undefined && !(globals.found.includes(globals.word))) {
      globals.found.push(globals.word);
      highlightWord(
        globals.selected[0].r,
        globals.selected[0].c,
        globals.selected[globals.selected.length - 1].r,
        globals.selected[globals.selected.length - 1].c
      );
      globals.wordbank[globals.word].setAttribute("style", globals.styles["word-crossout"]);
      deselectAll();
    }
  }
}

function noPuzzle() {
  message = document.createElementNS("http://www.w3.org/2000/svg", "text");
  message.setAttribute("x", "1cm");
  message.setAttribute("y", "0cm");
  message.setAttribute("font-size", globals.font_size + "cm");
  message.setAttribute("dominant-baseline", "hanging");
  message.setAttribute("text-anchor", "start");
  message.appendChild(document.createTextNode("Puzzle came empty :("));
  globals.svg.appendChild(message);
  document.body.appendChild(globals.svg);
}

function renderCell(grid, n, m, x, y, puzzle, r, c) {
  grid[n][m].setAttribute("x", x + "cm");
  grid[n][m].setAttribute("y", y + "cm");
  grid[n][m].setAttribute("width", globals.cell_size + "cm");
  grid[n][m].setAttribute("height", globals.cell_size + "cm");
  grid[n][m].setAttribute("shape-rendering", "crispEdges");
  if (r * c != 0 && puzzle[r][c] != "#") {
    grid[n][m].setAttribute("style", globals.styles["grid-board"]);
  } else {
    grid[n][m].setAttribute("style", globals.styles["grid-header"]);
  }
}

function renderLetter(letters, n, m, x, y, puzzle, r, c) {
  letters[n][m].setAttribute("x", x + globals.cell_size / 2 + "cm");
  letters[n][m].setAttribute("y", y + globals.cell_size / 2 + "cm");
  if (r * c != 0) {
    letters[n][m].setAttribute("font-size", globals.font_size + "cm");
  } else {
    letters[n][m].setAttribute("font-size", globals.font_size / 2 + "cm");
  }
  letters[n][m].setAttribute("dominant-baseline", "middle");
  letters[n][m].setAttribute("text-anchor", "middle");
  if (puzzle[r][c] != "#") {
    letters[n][m].appendChild(document.createTextNode(puzzle[r][c]));
  }
}

function renderButton(buttons, n, m, x, y, puzzle, r, c) {
  buttons[n][m].setAttribute("x", x + "cm");
  buttons[n][m].setAttribute("y", y + "cm");
  buttons[n][m].setAttribute("width", globals.cell_size + "cm");
  buttons[n][m].setAttribute("height", globals.cell_size + "cm");
  buttons[n][m].setAttribute("style", globals.styles["button-out"]);
  if (r * c != 0 && puzzle[r][c] != "#") {
    buttons[n][m].setAttribute("onmouseover", "flickerButton(" + r + ", " + c + ", \"button-over\");");
    buttons[n][m].setAttribute("onmouseout", "flickerButton(" + r + ", " + c + ", \"button-out\");");
    buttons[n][m].setAttribute("onmousedown", "recordLetter(" + r + ", " + c + ", \"" + puzzle[r][c] + "\");");
  }
}

function renderLastElement(item, fn, x, y, puzzle, r, c) {
  n = item.length - 1;
  m = item[n].length - 1;
  fn(item, n, m, x, y, puzzle, r, c);
}

function renderFrame(puzzle_width, puzzle_height) {
  var frame = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  frame.setAttribute("width", (puzzle_width + 1) * globals.cell_size + globals.puzzle_margin_x * 2 + "cm");
  frame.setAttribute("height", (puzzle_height + 1) * globals.cell_size + globals.puzzle_margin_y * 2 + "cm");
  frame.setAttribute("style", globals.styles["grid-frame"]);
  frame.setAttribute("rx", globals.frame_rx);
  frame.setAttribute("ry", globals.frame_ry);
  globals.svg.appendChild(frame);
}

function renderWordbank(words, svg_width, puzzle_height) {
  var wordbank = {};
  var wordbank_group = 0;
  var wordbank_row = 0;
  var wordbank_col = 0;
  for (i = 0; i < words.length; i++) {
    word = words[i];
    wordbank[word] = document.createElementNS("http://www.w3.org/2000/svg", "text");
    wordbank[word].setAttribute("x", wordbank_col * svg_width / globals.wb_max_cols + "cm");
    wordbank[word].setAttribute("y", globals.cell_size * (puzzle_height + 1) + globals.puzzle_margin_y * 2 + 1 + wordbank_row * globals.wb_font_size + "cm");
    wordbank[word].setAttribute("font-size", globals.wb_font_size + "cm");
    wordbank[word].setAttribute("onmouseover", "locateWord(\"" + word + "\");");
    wordbank[word].setAttribute("onmouseout", "hideWordFrame();");
    wordbank[word].appendChild(document.createTextNode(word));
    globals.svg.appendChild(wordbank[word]);
    wordbank_row += 1;
    if (wordbank_row == (wordbank_group + 1) * globals.wb_max_rows) {
      wordbank_col += 1;
      wordbank_row = wordbank_group * globals.wb_max_rows;
    }
    if (wordbank_col == globals.wb_max_cols) {
      wordbank_col = 0;
      wordbank_group += 1;
      wordbank_row += globals.wb_max_rows;
    }
  }
  return wordbank;
}

function render(words, puzzle, solution) {
  if (puzzle.length == 0) {
    return noPuzzle();
  }
  globals.solution = solution;
  var grid = [];
  var letters = [];
  var buttons = [];
  var x = globals.puzzle_margin_x;
  var y = globals.puzzle_margin_y;
  var wordbank_height = globals.wb_max_rows * Math.ceil(words.length / (globals.wb_max_rows * globals.wb_max_cols)) * globals.wb_font_size;
  var puzzle_width = puzzle[0].length;
  var puzzle_height = puzzle.length;
  var svg_width = (puzzle_width + 1) * globals.cell_size + globals.puzzle_margin_x * 2;
  var svg_height = (puzzle_height + 1) * globals.cell_size + globals.puzzle_margin_y * 2 + wordbank_height + 1;
  globals.svg.setAttribute("width", svg_width + "cm");
  globals.svg.setAttribute("height", svg_height + "cm");
  document.body.appendChild(globals.svg);
  for (r = 0; r < puzzle.length; r++) {
    x = globals.puzzle_margin_x;
    grid.push([]); letters.push([]); buttons.push([]);
    for (c = 0; c < puzzle[r].length; c++) {
      grid[grid.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));
      renderLastElement(grid, renderCell, x, y, puzzle, r, c);
      letters[letters.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "text"));
      renderLastElement(letters, renderLetter, x, y, puzzle, r, c);
      buttons[buttons.length - 1].push(document.createElementNS("http://www.w3.org/2000/svg", "rect"));
      renderLastElement(buttons, renderButton, x, y, puzzle, r, c);
      globals.svg.appendChild(grid[grid.length - 1][grid[grid.length - 1].length - 1]);
      globals.svg.appendChild(letters[letters.length - 1][letters[letters.length - 1].length - 1]);
      globals.svg.appendChild(buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1]);
      x += globals.cell_size;
    }
    y += globals.cell_size;
  }
  globals.buttons = buttons;
  renderFrame(puzzle_width, puzzle_height);
  globals.wordbank = renderWordbank(words, svg_width, puzzle_height);
}
