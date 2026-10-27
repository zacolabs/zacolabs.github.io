// Run with: node --test scripts/8billion/test_language.cjs
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const script=fs.readFileSync(__dirname+'/language.js','utf8');
function visit({languages=['en-US'],saved=null,path='/8billion/',search='',hash='',blocked=false}={}){
 let target=null,click;
 const storage={value:saved,getItem(){if(blocked)throw Error('blocked');return this.value},setItem(k,v){if(blocked)throw Error('blocked');this.value=v},removeItem(){if(blocked)throw Error('blocked');this.value=null}};
 const location={pathname:path,search,hash,replace(url){target=url}};
 vm.runInNewContext(script,{navigator:{languages,language:languages[0],userAgent:'Mozilla/5.0'},localStorage:storage,location,URLSearchParams,document:{addEventListener(event,handler){click=handler}}});
 return {target,storage,choose(lang){const a={dataset:{lang},href:lang==='system'?'/8billion/':lang==='en'?'/8billion/':`/8billion/${lang}/`};click({target:{closest:()=>a}});return a.href}};
}
test('uses browser language and supported fallback preferences',()=>{
 for(const [languages,expected] of [[['ko-KR'],'ko'],[['ja-JP'],'ja'],[['zh-CN'],'zh-hans'],[['zh-SG'],'zh-hans'],[['zh-TW'],'zh-hant'],[['zh-HK'],'zh-hant'],[['zh-MO'],'zh-hant'],[['zh-Hans-TW'],'zh-hans'],[['zh-Hant-CN'],'zh-hant'],[['fr-FR','ja'],'ja']]){
  assert.equal(visit({languages}).target,`/8billion/${expected}/`,languages.join(','));
 }
 assert.equal(visit({languages:['en-GB']}).target,null);
 assert.equal(visit({languages:['fr']}).target,null);
});
test('manual choice overrides browser and persists',()=>{
 assert.equal(visit({languages:['ko'],saved:'ja'}).target,'/8billion/ja/');
 assert.equal(visit({languages:['ko'],saved:'en'}).target,null);
 const state=visit();state.choose('zh-hant');assert.equal(state.storage.value,'zh-hant');
});
test('system setting clears manual preference',()=>{
 const state=visit({saved:'ja',path:'/8billion/ja/'});assert.equal(state.choose('system'),'/8billion/');assert.equal(state.storage.value,null);
});
test('explicit URLs remain readable and redirects preserve query and fragment',()=>{
 assert.equal(visit({languages:['ko'],path:'/8billion/ja/'}).target,null);
 assert.equal(visit({languages:['ja'],search:'?source=store',hash:'#faq'}).target,'/8billion/ja/?source=store#faq');
 assert.equal(visit({languages:['ko'],search:'?lang=en'}).target,null);
});
test('blocked storage still allows detection and explicit English selection',()=>{
 assert.equal(visit({languages:['ko'],blocked:true}).target,'/8billion/ko/');
 assert.equal(visit({languages:['ko'],blocked:true}).choose('en'),'/8billion/?lang=en');
 assert.equal(visit({languages:['ko'],saved:'bogus'}).target,'/8billion/ko/');
});
