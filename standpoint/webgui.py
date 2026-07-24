"""The single-page Standpoint GUI as one self-contained HTML string.

No build step, no framework, no npm: vanilla JavaScript + Tailwind (Play CDN) +
vega-embed (to render the Vega-Lite spec live in the browser) + marked (to render the
Markdown analysis). `standpoint.api` serves this at ``GET /gui``.

Kept as a Python string (rather than a static file) so it ships inside the package
and the ``dev-gui`` investigation stays a two-file backend + one-string frontend.
"""

from __future__ import annotations

# The whole page. Tailwind classes carry the styling; the <script> holds a small,
# dependency-free controller: build an editable grid, serialize it to CSV, POST it,
# then render the returned Vega-Lite spec and Markdown.
GUI_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Standpoint — table to quadrant</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    /* Neutral, calm surface; the map is the star. */
    body { font-family: Roboto, -apple-system, Helvetica, Arial, sans-serif; }
    .cell { width: 4.5rem; }
    #chart.checker { background-image:
      linear-gradient(45deg,#eee 25%,transparent 25%),
      linear-gradient(-45deg,#eee 25%,transparent 25%),
      linear-gradient(45deg,transparent 75%,#eee 75%),
      linear-gradient(-45deg,transparent 75%,#eee 75%);
      background-size: 20px 20px;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800">
  <div class="max-w-6xl mx-auto p-6 space-y-6">
    <header class="flex items-baseline justify-between">
      <h1 class="text-2xl font-bold">Standpoint</h1>
      <p class="text-sm text-slate-500">Edit a table → get a positioning quadrant + written analysis.</p>
    </header>

    <!-- Table editor -->
    <section class="bg-white rounded-xl shadow-sm p-4 space-y-3">
      <div class="flex items-center gap-2 flex-wrap">
        <button id="addRow" class="px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-sm">+ Option (row)</button>
        <button id="addCol" class="px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-sm">+ Criterion (column)</button>
        <button id="loadExample" class="px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-sm">Reset to example</button>
        <span class="text-xs text-slate-400 ml-2">Higher = better. Toggle <b>↓</b> on a column where lower is better.</span>
      </div>
      <div class="overflow-x-auto">
        <table class="border-collapse text-sm" id="grid"></table>
      </div>
    </section>

    <!-- Controls -->
    <section class="bg-white rounded-xl shadow-sm p-4 flex items-center gap-4 flex-wrap">
      <label class="flex items-center gap-2 text-sm">Reference (top-right)
        <select id="reference" class="border rounded-md px-2 py-1"></select>
      </label>
      <label class="flex items-center gap-2 text-sm">
        <input type="checkbox" id="useLlm" class="w-4 h-4" />
        Name axes + write analysis with the local model (slower)
      </label>
      <label class="flex items-center gap-2 text-sm">Background
        <select id="bg" class="border rounded-md px-2 py-1">
          <option value="transparent">transparent</option>
          <option value="white" selected>white</option>
        </select>
      </label>
      <button id="run" class="ml-auto px-4 py-2 rounded-md bg-blue-600 text-white font-medium hover:bg-blue-700">Generate quadrant</button>
    </section>

    <p id="status" class="text-sm text-slate-500 hidden"></p>
    <p id="error" class="text-sm text-red-600 hidden"></p>

    <!-- Output -->
    <section class="grid md:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-sm p-4">
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-semibold">Quadrant</h2>
          <div class="flex gap-2">
            <button id="dlYaml" class="text-xs px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 hidden">YAML</button>
          </div>
        </div>
        <div id="chart" class="min-h-[420px] flex items-center justify-center text-slate-400">
          Generate to see the map.
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-4">
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-semibold">Analysis</h2>
          <button id="dlMd" class="text-xs px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 hidden">Markdown</button>
        </div>
        <div id="comments" class="prose prose-sm max-w-none text-slate-400">
          The written interpretation appears here.
        </div>
      </div>
    </section>
  </div>

<script>
// --- tiny state: header cells, lower-is-better flags, and data rows -----------
let headers = [];      // criteria names (excluding the first "option" column)
let firstCol = "Option";
let lowerCols = new Set();  // indices (into headers) marked lower-is-better
let rows = [];         // each: {name: string, values: string[]}

const $ = (id) => document.getElementById(id);

// Parse CSV text into our state (first column = option names, rest numeric).
function loadCsv(text) {
  const lines = text.trim().split(/\r?\n/).filter((l) => l.length);
  const head = lines[0].split(",");
  firstCol = head[0];
  headers = head.slice(1);
  lowerCols = new Set();
  rows = lines.slice(1).map((l) => {
    const c = l.split(",");
    return { name: c[0], values: headers.map((_, i) => c[i + 1] ?? "") };
  });
  renderGrid();
}

// Rebuild the editable table and the reference dropdown from state.
function renderGrid() {
  const g = $("grid");
  g.innerHTML = "";
  // header row: first-column name, then each criterion with ↓ toggle + delete
  const htr = document.createElement("tr");
  htr.innerHTML = `<th class="p-1"><input class="cell font-semibold border rounded px-1 py-0.5"
      value="${firstCol}" oninput="firstCol=this.value"/></th>`;
  headers.forEach((h, i) => {
    const th = document.createElement("th");
    th.className = "p-1 align-bottom";
    th.innerHTML = `
      <div class="flex flex-col items-center gap-1">
        <input class="cell border rounded px-1 py-0.5 text-center" value="${h}"
               oninput="headers[${i}]=this.value"/>
        <div class="flex gap-1 text-xs">
          <button title="lower is better" class="px-1 rounded ${lowerCols.has(i) ? 'bg-amber-200' : 'bg-slate-100'}"
                  onclick="toggleLower(${i})">↓</button>
          <button title="delete column" class="px-1 rounded bg-slate-100 hover:bg-red-100"
                  onclick="delCol(${i})">✕</button>
        </div>
      </div>`;
    htr.appendChild(th);
  });
  g.appendChild(htr);
  // data rows
  rows.forEach((r, ri) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td class="p-1"><input class="cell border rounded px-1 py-0.5" value="${r.name}"
        oninput="rows[${ri}].name=this.value; syncReference()"/></td>`;
    r.values.forEach((v, ci) => {
      const td = document.createElement("td");
      td.className = "p-1";
      td.innerHTML = `<input class="cell border rounded px-1 py-0.5 text-center" value="${v}"
          oninput="rows[${ri}].values[${ci}]=this.value"/>`;
      tr.appendChild(td);
    });
    const del = document.createElement("td");
    del.innerHTML = `<button class="px-1 text-xs rounded bg-slate-100 hover:bg-red-100"
        onclick="delRow(${ri})">✕</button>`;
    tr.appendChild(del);
    g.appendChild(tr);
  });
  syncReference();
}

function toggleLower(i) { lowerCols.has(i) ? lowerCols.delete(i) : lowerCols.add(i); renderGrid(); }
function delCol(i) { headers.splice(i, 1); rows.forEach((r) => r.values.splice(i, 1));
                     lowerCols = new Set(); renderGrid(); }
function delRow(i) { rows.splice(i, 1); renderGrid(); }

// Keep the reference dropdown in step with the option names.
function syncReference() {
  const sel = $("reference"); const cur = sel.value;
  sel.innerHTML = rows.map((r, i) => `<option value="${i}">${r.name || ("row " + i)}</option>`).join("");
  if (cur && cur < rows.length) sel.value = cur;
}

$("addRow").onclick = () => { rows.push({ name: "New", values: headers.map(() => "3") }); renderGrid(); };
$("addCol").onclick = () => { headers.push("Criterion"); rows.forEach((r) => r.values.push("3")); renderGrid(); };
$("loadExample").onclick = () => fetch("/api/example").then((r) => r.text()).then(loadCsv);

// Serialize the grid back to CSV, tagging lower-is-better columns with "(↓)".
function toCsv() {
  const head = [firstCol, ...headers.map((h, i) => (lowerCols.has(i) ? `${h} (↓)` : h))];
  const body = rows.map((r) => [r.name, ...r.values].join(","));
  return [head.join(","), ...body].join("\n");
}

// --- generate: POST the table, render the spec + markdown --------------------
let lastYaml = "", lastMd = "";
$("run").onclick = async () => {
  $("error").classList.add("hidden");
  $("status").textContent = $("useLlm").checked
    ? "Running PCA and asking the local model… (this can take ~10–25 s)"
    : "Running PCA…";
  $("status").classList.remove("hidden");
  try {
    const res = await fetch("/api/position", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        table: toCsv(),
        reference: $("reference").value,
        lower: "",                 // lower-is-better is carried by the (↓) markers
        use_llm: $("useLlm").checked,
      }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
    const data = await res.json();
    // Render the quadrant. Background toggle applies to the preview only.
    const spec = data.vega;
    spec.background = $("bg").value === "white" ? "white" : null;
    $("chart").classList.toggle("checker", $("bg").value === "transparent");
    $("chart").textContent = "";
    await vegaEmbed("#chart", spec, { actions: { export: true, source: false, editor: false, compiled: false } });
    // Render the analysis.
    lastMd = data.markdown; lastYaml = data.yaml;
    $("comments").className = "prose prose-sm max-w-none";
    $("comments").innerHTML = marked.parse(data.markdown || "*(no analysis — enable the model)*");
    $("dlYaml").classList.remove("hidden"); $("dlMd").classList.remove("hidden");
    $("status").classList.add("hidden");
  } catch (e) {
    $("status").classList.add("hidden");
    $("error").textContent = "Error: " + e.message;
    $("error").classList.remove("hidden");
  }
};

// Client-side downloads for the text deliverables (the figure uses vega-embed's menu).
function download(name, text, type) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], { type }));
  a.download = name; a.click(); URL.revokeObjectURL(a.href);
}
$("dlYaml").onclick = () => download("standpoint.yaml", lastYaml, "text/yaml");
$("dlMd").onclick = () => download("standpoint.md", lastMd, "text/markdown");

// Start with the shipped example so the page is alive on load.
fetch("/api/example").then((r) => r.text()).then(loadCsv);
</script>
</body>
</html>
"""
