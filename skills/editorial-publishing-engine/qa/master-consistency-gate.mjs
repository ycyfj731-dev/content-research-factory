#!/usr/bin/env node
import fs from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("usage: node qa/master-consistency-gate.mjs <deck.html>");
  process.exit(2);
}
const html = fs.readFileSync(file, "utf8");
const pages = [...html.matchAll(/<section\b[^>]*class="[^"]*editorial-page[^"]*"[^>]*>/g)].map(m=>m[0]);
const masters = pages.map(p => (p.match(/data-master="([^"]+)"/)||[])[1]).filter(Boolean);
const accounts = (html.match(/@每天读一点哲学/g)||[]).length;
const sections = [...html.matchAll(/class="section-no"[^>]*>(\d{2})</g)].map(m=>m[1]);
const expected = Array.from({length:sections.length},(_,i)=>String(i+1).padStart(2,"0"));
const essayCount = masters.filter(x=>x==="essay").length;
const statementCount = masters.filter(x=>x==="statement").length;
const coverCount = masters.filter(x=>x==="cover").length;
const creditsCount = masters.filter(x=>x==="credits").length;

const checks = [
  ["PAGE_COUNT_MAX_10", pages.length <= 10, String(pages.length)],
  ["MASTER_DECLARED", masters.length === pages.length, masters.join(", ")],
  ["ESSAY_MAJORITY", pages.length===0 ? false : essayCount/pages.length >= 0.5, essayCount+"/"+pages.length],
  ["STATEMENT_MAX_2", statementCount <= 2, String(statementCount)],
  ["SPECIAL_COUNTS", coverCount===1 && creditsCount===1, "cover="+coverCount+" credits="+creditsCount],
  ["ACCOUNT_CHROME_FIXED", accounts===pages.length, accounts+"/"+pages.length],
  ["SECTION_MARKER_RULES", JSON.stringify(sections)===JSON.stringify(expected), sections.join(",")],
  ["NO_INTERNAL_FREEZE_METADATA", !/正文冻结|FROZEN|LECTURE_\d+_FINAL_FROZEN|editorial-publishing-engine/.test(html), "public deck only"],
  ["NO_STANDALONE_TOOL_CARD", !/阅读工具|怎么读古代哲学/.test(html), "TOOL stays internal unless organically required"]
];

let failed=0;
for (const [name,ok,detail] of checks){
  console.log((ok?"PASS":"FAIL")+"\t"+name+"\t"+detail);
  if(!ok) failed++;
}
console.log("\nVERDICT\t"+(failed?"FAIL":"PASS"));
process.exit(failed?1:0);
