// Checks _routes.json the way Cloudflare Pages reads it: the city pages must run the function in
// functions/panchang/[slug].js, and nothing else under /panchang may (the data files, the monthly and muhurat pages,
// and the old addresses that _redirects moves, since a redirect is not applied where a function runs).
//
// Cloudflare reads a rule that ends in "/*" as also matching the address without it: "/foo/*" matches "/foo". So the
// exclude rule "/panchang/*/*" matched "/panchang/london" too, and from 15 to 16 Nov 2026 the function never ran on
// any city page. The matching below follows isRoutingRuleMatch in Cloudflare's workers-sdk
// (packages/wrangler/templates/pages-dev-util.ts); exclude rules win over include rules.
//
//     node tools/check_routes.mjs        (from the repo root)
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const routes = JSON.parse(fs.readFileSync(path.join(ROOT, '_routes.json'), 'utf8'));

function ruleRegExp(rule) {
  let r;
  if (rule === '/' || rule === '/*') { r = rule; }
  else if (rule.endsWith('/*')) { r = rule.slice(0, -2) + '(/*)?'; }      // "/foo/*" also matches "/foo"
  else if (rule.endsWith('/')) { r = rule.slice(0, -1) + '(/)?'; }
  else if (rule.endsWith('*')) { r = rule; }
  else { r = rule + '(/)?'; }
  return new RegExp('^' + r.replace(/\./g, '\\.').replace(/\*/g, '.*') + '$');
}
function runsFunction(address) {
  if (routes.exclude.some((rule) => ruleRegExp(rule).test(address))) { return false; }
  return routes.include.some((rule) => ruleRegExp(rule).test(address));
}

const must = [], mustNot = [];
const dir = path.join(ROOT, 'panchang');
for (const f of fs.readdirSync(dir)) {
  const full = path.join(dir, f);
  if (f.endsWith('.html')) {
    const address = '/panchang/' + f.slice(0, -5);
    (fs.readFileSync(full, 'utf8').includes('<script>window.PANCHANG = ') ? must : mustNot).push(address);
  } else if (fs.statSync(full).isDirectory()) {
    for (const g of fs.readdirSync(full)) {
      mustNot.push('/panchang/' + f + '/' + g.replace(/\.(html|json)$/, ''));
    }
  }
}
for (const line of fs.readFileSync(path.join(ROOT, '_redirects'), 'utf8').split('\n')) {
  const from = line.trim().split(/\s+/)[0];
  if (from && from.startsWith('/panchang/')) { mustNot.push(from); }
}
mustNot.push('/panchang/data/london.json');

// a city page must still run the function: the festival, country and method pages read no data and are let through
const wrong = must.filter((a) => !runsFunction(a)).map((a) => 'not run on ' + a)
  .concat(mustNot.filter((a) => runsFunction(a) && !/^\/panchang\/[a-z-]+$/.test(a)).map((a) => 'run on ' + a));
console.log(`${must.length} city pages run the function; ${mustNot.filter((a) => !runsFunction(a)).length} of `
  + `${mustNot.length} other addresses go straight to the files (the rest are top-level pages the function skips)`);
for (const w of wrong) { console.log('WRONG: ' + w); }
process.exit(wrong.length ? 1 : 0);
