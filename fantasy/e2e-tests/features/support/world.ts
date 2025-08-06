import { setWorldConstructor, World, IWorldOptions } from '@cucumber/cucumber';
import { Browser, BrowserContext, Page, chromium } from 'playwright';

export interface CustomWorldOptions extends IWorldOptions {
  baseUrl?: string;
  apiUrl?: string;
}

export class CustomWorld extends World {
  public browser!: Browser;
  public context!: BrowserContext;
  public page!: Page;
  public baseUrl: string;
  public apiUrl: string;
  public expectedData: { [key: string]: any } = {};

  constructor(options: CustomWorldOptions) {
    super(options);
    this.baseUrl = options.parameters?.baseUrl || 'http://localhost:3001';
    this.apiUrl = options.parameters?.apiUrl || 'http://localhost:8000';
  }

  async init() {
    this.browser = await chromium.launch({ 
      headless: process.env.HEADED !== 'true',
      slowMo: process.env.SLOW_MO ? parseInt(process.env.SLOW_MO) : 0
    });
    this.context = await this.browser.newContext({
      viewport: { width: 1280, height: 720 },
      ignoreHTTPSErrors: true,
    });
    this.page = await this.context.newPage();
    
    // Set up console logging
    this.page.on('console', (msg) => {
      if (msg.type() === 'error') {
        console.error(`Browser Console Error: ${msg.text()}`);
      }
    });

    // Set up error handling
    this.page.on('pageerror', (error) => {
      console.error(`Page Error: ${error.message}`);
    });
  }

  async cleanup() {
    if (this.page) await this.page.close();
    if (this.context) await this.context.close();
    if (this.browser) await this.browser.close();
  }
}

setWorldConstructor(CustomWorld);
