const config = {
  require: [
    'features/step_definitions/**/*.ts',
    'features/support/**/*.ts'
  ],
  requireModule: ['ts-node/register'],
  loader: ['ts-node/esm'],
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
