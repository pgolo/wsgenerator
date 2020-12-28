var button_styles = {
  "over": "fill:white;opacity:50%;stroke-width:0px",
  "out": "fill:white;opacity:0%;stroke-width:0px",
  "selected": "fill:white;opacity:90%;stroke-width:0px"
}

var cell_size = 1;
var font_size = 0.8;

var g_word = '';
var g_wordbank = {};
var g_buttons = [];
var selected = [];
var selected_buttons = [];
var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
  var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;

  return {
    x: centerX + (radius * Math.cos(angleInRadians)),
    y: centerY + (radius * Math.sin(angleInRadians))
  };
}

function describeArc(x, y, radius, startAngle, endAngle){

    var start = polarToCartesian(x, y, radius, endAngle);
    var end = polarToCartesian(x, y, radius, startAngle);

    var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

    var d = [
        "M", start.x, start.y, 
        "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
    ].join(" ");

    return d;       
}

function maySelect(r, c) {
  if (selected.length == 0) {
    return true;
  } else if (selected.length == 1 && Math.abs(r - selected[0].r) <= 1 && Math.abs(c - selected[0].c) <= 1 && (r != selected[0].r || c != selected[0].c)) {
    return true;
  }
  else if (selected.length > 1) {
    dr = selected[1].r - selected[0].r;
    dc = selected[1].c - selected[0].c;
    last_r = selected[selected.length-1].r;
    last_c = selected[selected.length-1].c;
    if (r - last_r == dr && c - last_c == dc) {
      return true;
    }
  }
  return false;
}

function flickerButton(r, c, style) {
  for (i = 0; i < selected.length; i++) {
    if (selected[i].r == r && selected[i].c == c) {
      g_buttons[r][c].setAttribute("style", button_styles["selected"]);
      return;
    }
  }
  if (style == 'over') {
    g_buttons[r][c].setAttribute("style", button_styles["over"]);
    return;
  }
  if (style == 'out') {
    g_buttons[r][c].setAttribute("style", button_styles["out"]);
    return;
  }
}

function deselectAll() {
  selected = [];
  for (i = 0; i < selected_buttons.length; i++) {
    selected_buttons[i].setAttribute("style", button_styles["out"]);
  }
  selected_buttons = [];
  g_word = '';
}

function getButtonCenter(r, c) {
  button_x = parseFloat(g_buttons[r][c].getAttribute("x"));
  button_y = parseFloat(g_buttons[r][c].getAttribute("y"));
  button_w = parseFloat(g_buttons[r][c].getAttribute("width"));
  button_h = parseFloat(g_buttons[r][c].getAttribute("height"));
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

function highlightFrame(x1, y1, x2, y2, y_offset, x_offset, angle) {
  points = [
    [x1,  y1, -x_offset,                -y_offset],
    [x1,  y1, -x_offset-0.1*cell_size,  -y_offset+0.1*cell_size],
    [x1,  y1, -x_offset-0.1*cell_size,   y_offset-0.1*cell_size],
    [x1,  y1, -x_offset,                 y_offset],
    [x2,  y2,  x_offset,                 y_offset],
    [x2,  y2,  x_offset+0.1*cell_size,   y_offset-0.1*cell_size],
    [x2,  y2,  x_offset+0.1*cell_size,  -y_offset+0.1*cell_size],
    [x2,  y2,  x_offset,                -y_offset],
    [x1,  y1, -x_offset,                -y_offset]
  ];
  lines = [];
  for (i = 0; i < points.length - 1; i++) {
    from = rotate(points[i][0] + points[i][2], points[i][1] + points[i][3], points[i][0], points[i][1], angle);
    to = rotate(points[i+1][0] + points[i+1][2], points[i+1][1] + points[i+1][3], points[i+1][0], points[i+1][1], angle);
    lines.push(document.createElementNS("http://www.w3.org/2000/svg", "line"));
    lines[lines.length-1].setAttribute("style", "stroke:black;stroke-width:1px");
    lines[lines.length-1].setAttribute("x1", from.x + "cm");
    lines[lines.length-1].setAttribute("y1", from.y + "cm");
    lines[lines.length-1].setAttribute("x2", to.x + "cm");
    lines[lines.length-1].setAttribute("y2", to.y + "cm");
  }
  return lines;
}

function highlightWord() {
  r1 = selected[0].r;
  c1 = selected[0].c;
  r2 = selected[selected.length - 1].r;
  c2 = selected[selected.length - 1].c;
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
  frame = highlightFrame(from.x, from.y, to.x, to.y, cell_size * 0.4, cell_size * 0.3, angle);
  for (i = 0; i < frame.length; i++) {
    svg.appendChild(frame[i]);
  }
}

function recordLetter(r, c, letter) {
  deselect = false;
  if (!maySelect(r, c)) {
    if (selected.length == 1 && r == selected[0].r && c == selected[0].c) {
      deselect = true;
    }
    deselectAll();
  }
  if (!deselect) {
    selected.push({r: r, c: c});
    selected_buttons.push(g_buttons[r][c]);
    flickerButton(r, c, 'selected');
    g_word += letter;
    if (g_wordbank[g_word] != undefined) {
      highlightWord();
      g_wordbank[g_word].setAttribute("style", "text-decoration:line-through");
      deselectAll();
    }
  }
}

function render(words, puzzle) {
  var wordbank_max_rows = 1;
  var wordbank_max_cols = 3;
  var wordbank_row = 0;
  var wordbank_col = 0;
  var wordbank_font_size = 0.6;
  var wordbank_height = wordbank_max_rows * Math.ceil(words.length / (wordbank_max_rows * wordbank_max_cols)) * wordbank_font_size;
  var grid = []; var letters = []; var buttons = [];
  var x_margin = 1; var y_margin = 1;
  var x = x_margin; var y = y_margin;
  var svg_width = (puzzle[0].length + 1) * cell_size + x_margin * 2;
  var svg_height = (puzzle.length + 1) * cell_size + y_margin * 2 + wordbank_height + 1;
  //var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
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
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseover", "flickerButton(" + r + ", " + c + ", \"over\");");
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmouseout", "flickerButton(" + r + ", " + c + ", \"out\");");
        buttons[buttons.length - 1][buttons[buttons.length - 1].length - 1].setAttribute("onmousedown", "recordLetter(" + r + ", " + c + ", \"" + puzzle[r][c] + "\");");
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
  for (i = 0; i < words.length; i++) {
    word = words[i];
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
  g_wordbank = wordbank;
  g_buttons = buttons;
}
