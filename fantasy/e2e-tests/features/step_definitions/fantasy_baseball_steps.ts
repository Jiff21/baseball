import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { CustomWorld } from '../support/world';

// Navigation steps
Given('I navigate to the Fantasy Baseball application', async function (this: CustomWorld) {
  await this.page.goto(this.baseUrl);
});

Given('the application loads successfully', async function (this: CustomWorld) {
  await expect(this.page.locator('h1')).toContainText('Fantasy Expected Start');
  await this.page.waitForLoadState('networkidle');
});

Given('I am on the Fantasy Baseball page', async function (this: CustomWorld) {
  await this.page.goto(this.baseUrl);
  await expect(this.page.locator('h1')).toContainText('Fantasy Expected Start');
});

// League selection steps
When('I select {string} from the league type dropdown', async function (this: CustomWorld, leagueType: string) {
  await this.page.selectOption('#leagueType', leagueType);
  // Wait for scoring settings to load
  await this.page.waitForTimeout(1000);
});

// Button interaction steps
When('I click the {string} button', async function (this: CustomWorld, buttonText: string) {
  await this.page.click(`button:has-text("${buttonText}")`);
});

// Error validation steps
Then('I should not see any error messages', async function (this: CustomWorld) {
  const errorElements = await this.page.locator('.alert-danger').count();
  expect(errorElements).toBe(0);
});

// Results validation steps
Then('I should see the team matchup analysis results', async function (this: CustomWorld) {
  await expect(this.page.locator('.results-section')).toBeVisible({ timeout: 10000 });
  await expect(this.page.locator('h2')).toContainText('Team Matchup Analysis');
});

Then('the results should contain expected fantasy points for all teams', async function (this: CustomWorld) {
  const teamCards = await this.page.locator('.team-card').count();
  expect(teamCards).toBeGreaterThan(0);
  
  // Check that each team card has expected points
  const firstTeamCard = this.page.locator('.team-card').first();
  await expect(firstTeamCard.locator('.expected-points')).toBeVisible();
});

// Scoring settings validation steps
Then('I should see the {string} section', async function (this: CustomWorld, sectionName: string) {
  await expect(this.page.locator('h3')).toContainText(sectionName);
});

Then('all scoring values should display with one decimal point', async function (this: CustomWorld) {
  const inputs = await this.page.locator('.stat-input').all();
  
  for (const input of inputs) {
    const value = await input.inputValue();
    // Check that the value has exactly one decimal place
    const decimalMatch = value.match(/\.\d$/);
    expect(decimalMatch).toBeTruthy();
  }
});

Then('I should see the {string} subsection with all required fields', async function (this: CustomWorld, subsectionName: string) {
  await expect(this.page.locator('h4')).toContainText(subsectionName);
});

// Custom league steps
When('I modify the batting {string} value to {string}', async function (this: CustomWorld, fieldName: string, value: string) {
  // Find the input by its label
  const labelText = fieldName + ':';
  const input = this.page.locator(`label:has-text("${labelText}") + input`);
  await input.fill(value);
});

When('I modify the pitching {string} value to {string}', async function (this: CustomWorld, fieldName: string, value: string) {
  // Find the input by its label
  const labelText = fieldName + ':';
  const input = this.page.locator(`label:has-text("${labelText}") + input`);
  await input.fill(value);
});

When('I enter {string} as the league name', async function (this: CustomWorld, leagueName: string) {
  await this.page.fill('#leagueName', leagueName);
});

Then('I should see a success message', async function (this: CustomWorld) {
  // Wait for the alert dialog
  this.page.on('dialog', async dialog => {
    expect(dialog.message()).toContain('saved successfully');
    await dialog.accept();
  });
});

Then('the batting {string} value should be {string}', async function (this: CustomWorld, fieldName: string, expectedValue: string) {
  const labelText = fieldName + ':';
  const input = this.page.locator(`label:has-text("${labelText}") + input`);
  await expect(input).toHaveValue(expectedValue);
});

Then('the pitching {string} value should be {string}', async function (this: CustomWorld, fieldName: string, expectedValue: string) {
  const labelText = fieldName + ':';
  const input = this.page.locator(`label:has-text("${labelText}") + input`);
  await expect(input).toHaveValue(expectedValue);
});

// Field validation steps
Then('I should see the following batting fields:', async function (this: CustomWorld, dataTable) {
  const expectedFields = dataTable.hashes();
  
  for (const field of expectedFields) {
    const fieldName = field['Field Name'];
    const labelText = fieldName + ':';
    await expect(this.page.locator(`label:has-text("${labelText}")`)).toBeVisible();
  }
});

Then('I should see the following pitching fields:', async function (this: CustomWorld, dataTable) {
  const expectedFields = dataTable.hashes();
  
  for (const field of expectedFields) {
    const fieldName = field['Field Name'];
    const labelText = fieldName + ':';
    await expect(this.page.locator(`label:has-text("${labelText}")`)).toBeVisible();
  }
});

// Error handling steps
Given('the backend API is unavailable', async function (this: CustomWorld) {
  // Mock API to return error
  await this.page.route('**/api/**', route => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'API unavailable' })
    });
  });
});

Then('I should see an appropriate error message', async function (this: CustomWorld) {
  await expect(this.page.locator('.alert-danger')).toBeVisible({ timeout: 5000 });
});

Then('the application should remain functional', async function (this: CustomWorld) {
  // Check that the form is still interactive
  await expect(this.page.locator('#leagueType')).toBeEnabled();
  await expect(this.page.locator('#handedness')).toBeEnabled();
});

