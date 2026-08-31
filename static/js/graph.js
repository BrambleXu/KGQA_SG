"use strict";

const chart = echarts.init(document.getElementById("graph"));
const mode = document.body.dataset.mode;
const status = document.getElementById("status");
const categories = Array.from(document.querySelectorAll("#legend li"), item => ({name: item.textContent}));
let graphRequest = 0;
let profileRequest = 0;

async function getJSON(path, parameters = {}) {
  const response = await fetch(`${path}?${new URLSearchParams(parameters)}`);
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || `请求失败（${response.status}）`);
  }
  return response.json();
}

function renderGraph(graph) {
  chart.setOption({
    color: ["#276a99", "#a93f43", "#26704b", "#616875"],
    tooltip: {renderMode: "richText", formatter: item => item.dataType === "edge"
      ? `${item.data.source} → ${item.data.target}：${item.data.value}` : item.name},
    series: [{
      type: "graph", layout: "force", roam: true, draggable: true,
      zoom: Math.min(1, chart.getWidth() / 550),
      categories, data: graph.data, links: graph.links,
      symbolSize: graph.data.length > 40 ? 18 : 32,
      label: {show: true, position: "right", fontSize: 11},
      edgeSymbol: ["none", "arrow"], edgeSymbolSize: 6,
      edgeLabel: {show: graph.data.length <= 30, formatter: "{c}", fontSize: 10},
      lineStyle: {color: "#8f9aab", opacity: .65, curveness: .15},
      emphasis: {focus: "adjacency", lineStyle: {opacity: 1, width: 2}},
      force: {repulsion: graph.data.length > 40 ? 90 : 350, edgeLength: [50, 100], gravity: .15}
    }]
  }, true);
  const list = document.getElementById("person-list");
  list.replaceChildren();
  for (const person of graph.data) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = person.name;
    button.addEventListener("click", () => showProfile(person.name));
    list.append(button);
  }
}

async function showProfile(name) {
  const request = ++profileRequest;
  try {
    const person = await getJSON("/get_profile", {character_name: name});
    if (request !== profileRequest) return;
    document.getElementById("person-name").textContent = person.name;
    document.getElementById("person-category").textContent = person.category;
    document.getElementById("summary").textContent = person.summary;
    const portrait = document.getElementById("portrait");
    portrait.alt = `${person.name}的历史收集画像`;
    portrait.hidden = false;
    portrait.onerror = () => { portrait.hidden = true; };
    portrait.src = `/portrait?${new URLSearchParams({name: person.name})}`;
  } catch (error) {
    if (request === profileRequest) status.textContent = error.message;
  }
}

async function loadGraph(path, parameters = {}, question = false) {
  const request = ++graphRequest;
  status.textContent = "正在查询…";
  chart.showLoading();
  try {
    const data = await getJSON(path, parameters);
    if (request !== graphRequest) return;
    const graph = question ? data.graph : data;
    renderGraph(graph);
    status.textContent = question ? data.message : `${graph.data.length} 人 · ${graph.links.length} 条关系`;
    if (question && data.answers.length) await showProfile(data.answers[0]);
    else if (!question && parameters.name) await showProfile(parameters.name);
  } catch (error) {
    if (request === graphRequest) status.textContent = error.message;
  } finally {
    if (request === graphRequest) chart.hideLoading();
  }
}

document.getElementById("query-form").addEventListener("submit", event => {
  event.preventDefault();
  const name = document.getElementById("query").value.trim();
  loadGraph(mode === "qa" ? "/KGQA_answer" : "/search_name", {name}, mode === "qa");
});
document.getElementById("reset").addEventListener("click", () => loadGraph("/graph_data"));
chart.on("click", event => { if (event.dataType === "node") showProfile(event.name); });
new ResizeObserver(() => chart.resize()).observe(document.getElementById("graph"));
loadGraph("/graph_data");
