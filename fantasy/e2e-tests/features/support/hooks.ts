import { Before, After, BeforeAll, AfterAll } from '@cucumber/cucumber';
import { CustomWorld } from './world';

BeforeAll(async function () {
  console.log('Starting E2E test suite...');
});

Before(async function (this: CustomWorld) {
  await this.init();
});

After(async function (this: CustomWorld, scenario) {
  if (scenario.result?.status === 'FAILED') {
    // Take screenshot on failure
    const screenshot = await this.page.screenshot({ 
      path: `reports/screenshots/${scenario.pickle.name.replace(/\s+/g, '_')}_${Date.now()}.png`,
      fullPage: true 
    });
    this.attach(screenshot, 'image/png');
  }
  
  await this.cleanup();
});

AfterAll(async function () {
  console.log('E2E test suite completed.');
});

