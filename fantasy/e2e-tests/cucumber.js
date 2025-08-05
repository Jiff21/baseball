const config = {
  require: [
    'features/step_definitions/fantasy_baseball_steps.ts',
    'features/support/world.ts',
    'features/support/hooks.ts'
  ],
  requireModule: ['ts-node/register'],
  format: [
    'progress-bar',
    'json:reports/cucumber_report.json',
    'html:reports/cucumber_report.html',
    'allure-cucumberjs/reporter'
  ],
  formatOptions: {
    resultsDir: 'allure-results'
  },
  publishQuiet: true,
  dryRun: false,
  failFast: false,
  strict: true,
  worldParameters: {
    baseUrl: process.env.BASE_URL || 'http://localhost:3001',
    apiUrl: process.env.API_URL || 'http://localhost:8000'
  }
};

module.exports = config;
