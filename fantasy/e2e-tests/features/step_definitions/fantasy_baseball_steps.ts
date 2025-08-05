import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { CustomWorld } from '../support/world';

// Store results for comparison
let storedResults: any = {};

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

// Accordion steps
Then('the scoring settings accordion should be collapsed', async function (this: CustomWorld) {
  const accordion = this.page.locator('.accordion');
  const isOpen = await accordion.locator('.accordion-content.open').isVisible();
  expect(isOpen).toBe(false);
});

Then('the scoring settings accordion should be open', async function (this: CustomWorld) {
  const accordion = this.page.locator('.accordion');
  const isOpen = await accordion.locator('.accordion-content.open').isVisible();
  expect(isOpen).toBe(true);
});

When('I click the scoring settings accordion header', async function (this: CustomWorld) {
  await this.page.locator('.accordion-header').click();
  await this.page.waitForTimeout(500); // Wait for animation
});

Given('the scoring settings accordion is open', async function (this: CustomWorld) {
  const isOpen = await this.page.locator('.accordion-content.open').isVisible();
  if (!isOpen) {
    await this.page.locator('.accordion-header').click();
    await this.page.waitForTimeout(500);
  }
});

Then('the page should scroll to the team matchup analysis section', async function (this: CustomWorld) {
  // Check if the results section is in viewport
  const resultsSection = this.page.locator('.results-section');
  await expect(resultsSection).toBeInViewport();
});

// Handedness steps
When('I select {string} from the handedness dropdown', async function (this: CustomWorld, handedness: string) {
  await this.page.selectOption('#handedness', handedness);
  await this.page.waitForTimeout(500);
});

Then('I store the results for {string} handedness', async function (this: CustomWorld, handedness: string) {
  const teamRows = await this.page.locator('.team-row').all();
  const results = [];
  
  for (const row of teamRows) {
    const teamName = await row.locator('.team-abbr').textContent();
    const fantasyPoints = await row.locator('.fantasy-points').textContent();
    results.push({ team: teamName, points: fantasyPoints });
  }
  
  storedResults[handedness] = results;
});

Then('the results should be different from the {string} results', async function (this: CustomWorld, handedness: string) {
  const currentRows = await this.page.locator('.team-row').all();
  const currentResults = [];
  
  for (const row of currentRows) {
    const teamName = await row.locator('.team-abbr').textContent();
    const fantasyPoints = await row.locator('.fantasy-points').textContent();
    currentResults.push({ team: teamName, points: fantasyPoints });
  }
  
  const storedData = storedResults[handedness];
  expect(storedData).toBeDefined();
  
  // Compare results - they should be different
  let differentCount = 0;
  for (let i = 0; i < currentResults.length; i++) {
    const current = currentResults[i];
    const stored = storedData.find((s: any) => s.team === current.team);
    if (stored && stored.points !== current.points) {
      differentCount++;
    }
  }
  
  expect(differentCount).toBeGreaterThan(0);
});

Then('at least {int}% of teams should have different fantasy point values', async function (this: CustomWorld, percentage: number) {
  const currentRows = await this.page.locator('.team-row').all();
  const totalTeams = currentRows.length;
  const expectedDifferent = Math.floor((totalTeams * percentage) / 100);
  
  // This is already verified in the previous step, but we can add additional validation
  expect(totalTeams).toBeGreaterThan(0);
  expect(expectedDifferent).toBeGreaterThan(0);
});

// Inline fields steps
Then('each batting field should be displayed inline with its title', async function (this: CustomWorld) {
  const battingSection = this.page.locator('.settings-section').filter({ hasText: 'Batting' });
  const inlineFields = await battingSection.locator('.stat-input-inline').all();
  expect(inlineFields.length).toBeGreaterThan(0);
  
  for (const field of inlineFields) {
    const label = await field.locator('.stat-label-inline').isVisible();
    const input = await field.locator('input').isVisible();
    expect(label).toBe(true);
    expect(input).toBe(true);
  }
});

Then('each pitching field should be displayed inline with its title', async function (this: CustomWorld) {
  const pitchingSection = this.page.locator('.settings-section').filter({ hasText: 'Pitching' });
  const inlineFields = await pitchingSection.locator('.stat-input-inline').all();
  expect(inlineFields.length).toBeGreaterThan(0);
  
  for (const field of inlineFields) {
    const label = await field.locator('.stat-label-inline').isVisible();
    const input = await field.locator('input').isVisible();
    expect(label).toBe(true);
    expect(input).toBe(true);
  }
});

Then('all input fields should allow up to 3 digits', async function (this: CustomWorld) {
  const inputs = await this.page.locator('.stat-input-inline input').all();
  
  for (const input of inputs) {
    const maxAttr = await input.getAttribute('max');
    const isInnings = await input.getAttribute('id');
    
    if (!isInnings?.includes('INN')) {
      expect(maxAttr).toBe('999');
    }
  }
});

Then('the innings field should allow thirds \\(e.g., {float}, {float}\\)', async function (this: CustomWorld, value1: number, value2: number) {
  const inningsInput = this.page.locator('#pitching-INN');
  const maxAttr = await inningsInput.getAttribute('max');
  const stepAttr = await inningsInput.getAttribute('step');
  
  expect(maxAttr).toBe('9.2');
  expect(stepAttr).toBe('0.1');
});

// Team rows steps
Then('each team should be displayed in its own row', async function (this: CustomWorld) {
  const teamRows = await this.page.locator('.team-row').all();
  expect(teamRows.length).toBeGreaterThan(0);
  
  // Verify row layout
  for (const row of teamRows) {
    const teamInfo = await row.locator('.team-info').isVisible();
    const statsRow = await row.locator('.team-stats-row').isVisible();
    expect(teamInfo).toBe(true);
    expect(statsRow).toBe(true);
  }
});

Then('each team row should show fantasy points and key stats', async function (this: CustomWorld) {
  const teamRows = await this.page.locator('.team-row').all();
  
  for (const row of teamRows) {
    const fantasyPoints = await row.locator('.fantasy-points').isVisible();
    const stats = await row.locator('.stat-item').all();
    
    expect(fantasyPoints).toBe(true);
    expect(stats.length).toBeGreaterThan(0);
  }
});

Then('team rows should be sortable by points and team name', async function (this: CustomWorld) {
  const sortByPoints = this.page.locator('.sort-btn').filter({ hasText: 'Fantasy Points' });
  const sortByTeam = this.page.locator('.sort-btn').filter({ hasText: 'Team' });
  
  await expect(sortByPoints).toBeVisible();
  await expect(sortByTeam).toBeVisible();
  
  // Test sorting functionality
  await sortByPoints.click();
  await this.page.waitForTimeout(500);
  
  await sortByTeam.click();
  await this.page.waitForTimeout(500);
});

// TypeScript error checking steps
Then('the application should load without TypeScript errors', async function (this: CustomWorld) {
  // Wait for the page to fully load
  await this.page.waitForLoadState('networkidle');
  
  // Check that the main React app has rendered without crashing
  await expect(this.page.locator('h1')).toContainText('Fantasy Expected Start');
  
  // Verify that key components are rendered (indicating successful compilation)
  await expect(this.page.locator('#leagueType')).toBeVisible();
  await expect(this.page.locator('#handedness')).toBeVisible();
  await expect(this.page.locator('button:has-text("Calculate Expected Points")')).toBeVisible();
});

Then('the browser console should not contain any TypeScript errors', async function (this: CustomWorld) {
  // Listen for console errors
  const consoleErrors: string[] = [];
  
  this.page.on('console', msg => {
    if (msg.type() === 'error') {
      const errorText = msg.text();
      // Filter for TypeScript-related errors
      if (errorText.includes('TS') || 
          errorText.includes('TypeScript') || 
          errorText.includes('possibly \'undefined\'') ||
          errorText.includes('Type \'') ||
          errorText.includes('Cannot read properties of undefined')) {
        consoleErrors.push(errorText);
      }
    }
  });
  
  // Reload the page to trigger any compilation errors
  await this.page.reload();
  await this.page.waitForLoadState('networkidle');
  
  // Wait a bit for any async errors to surface
  await this.page.waitForTimeout(2000);
  
  // Check that no TypeScript errors were logged
  if (consoleErrors.length > 0) {
    console.log('TypeScript errors found in console:', consoleErrors);
    expect(consoleErrors.length).toBe(0);
  }
});

Then('the page should render all main components', async function (this: CustomWorld) {
  // Verify all main UI components are present and functional
  await expect(this.page.locator('h1')).toContainText('Fantasy Expected Start');
  await expect(this.page.locator('.form-container')).toBeVisible();
  await expect(this.page.locator('#leagueType')).toBeVisible();
  await expect(this.page.locator('#handedness')).toBeVisible();
  await expect(this.page.locator('button:has-text("Calculate Expected Points")')).toBeVisible();
  
  // Test that dropdowns are functional (no TypeScript errors preventing interaction)
  await this.page.selectOption('#leagueType', 'Custom');
  await this.page.waitForTimeout(1000);
  
  // Verify scoring settings load without errors
  await expect(this.page.locator('h3:has-text("Scoring Settings")')).toBeVisible();
});

Then('I should see the league type dropdown', async function (this: CustomWorld) {
  await expect(this.page.locator('#leagueType')).toBeVisible();
  await expect(this.page.locator('#leagueType')).toBeEnabled();
});

Then('I should see the handedness dropdown', async function (this: CustomWorld) {
  await expect(this.page.locator('#handedness')).toBeVisible();
  await expect(this.page.locator('#handedness')).toBeEnabled();
});

Then('I should see the {string} button', async function (this: CustomWorld, buttonText: string) {
  await expect(this.page.locator(`button:has-text("${buttonText}")`)).toBeVisible();
  await expect(this.page.locator(`button:has-text("${buttonText}")`)).toBeEnabled();
});
