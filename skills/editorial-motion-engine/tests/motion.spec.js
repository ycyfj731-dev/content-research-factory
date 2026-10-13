// Run: npm install && npm test (inside this skill directory).
// Playwright requires Chromium: npx playwright install chromium
const {test,expect}=require('@playwright/test');
const {resolve}=require('path');
const url='file://'+resolve(__dirname,'../demo/index.html');
test('direct seek deterministic and required questions remain visible',async({page})=>{
 await page.goto(url);const t=[0,1.3,3,5.8,6,6.5,7.2,9,11.9];
 for(const seconds of t){
  await page.evaluate(s=>window.motionEngine.seek(s),seconds);
  const a=await page.locator('#canvas').evaluate(el=>el.outerHTML);
  await page.evaluate(()=>window.motionEngine.seek(0));
  await page.evaluate(s=>window.motionEngine.seek(s),seconds);
  const b=await page.locator('#canvas').evaluate(el=>el.outerHTML);
  expect(b).toBe(a);
  const expected=seconds<6?'extract':'compare';
  expect(await page.locator('#'+expected).getAttribute('visibility')).toBe('visible');
  if(seconds>=6){
    for(let i=1;i<=3;i++){
      const q=page.locator('#q'+i);
      expect(await q.textContent()).toBeTruthy();
      expect(Number(await q.getAttribute('opacity'))).toBeGreaterThanOrEqual(.55);
      const bounds=await q.boundingBox();
      expect(bounds).not.toBeNull();
      const frame=await page.locator('#canvas').boundingBox();
      expect(bounds.x).toBeGreaterThanOrEqual(frame.x);
      expect(bounds.x+bounds.width).toBeLessThanOrEqual(frame.x+frame.width+1);
    }
  }
 }
});
test('source extraction contains only words in source and fits within video frame',async({page})=>{
 await page.goto(url);
 await page.evaluate(()=>window.motionEngine.seek(3));
 const words=await page.locator('#extract .body').allTextContents();
 for(const id of ['token-denying','token-overreacting']){
  const token=await page.locator('#'+id+' .keyword').textContent();
  expect(words.join(' ').includes(token)).toBe(true);
  const bbox=await page.locator('#'+id).boundingBox();
  const svg=await page.locator('#canvas').boundingBox();
  expect(bbox.x).toBeGreaterThanOrEqual(svg.x);
  expect(bbox.x+bbox.width).toBeLessThanOrEqual(svg.x+svg.width+1);
 }
});
test('capture QA frames for review',async({page})=>{
 await page.goto(url);await page.setViewportSize({width:1920,height:1200});
 for(const second of [0,1.5,3,5.5,6,7,8,9,11.5]){
  await page.evaluate(s=>window.motionEngine.seek(s),second);
  await page.locator('#canvas').screenshot({path:'test-results/frame-'+String(second).replace('.','_')+'.png'});
 }
});