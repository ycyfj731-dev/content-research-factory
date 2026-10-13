const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'./tests',use:{headless:true,browserName:'chromium',viewport:{width:1920,height:1200}},reporter:'list'});
