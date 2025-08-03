# Fantasy Baseball Frontend - Scoring Settings

This React TypeScript component provides a comprehensive interface for managing fantasy baseball league scoring settings.

## Features

### FantasyExpectedStart Component

The `FantasyExpectedStart.tsx` component includes:

1. **League Type Dropdown** - Select from:
   - Custom
   - ESPN
   - CBS
   - Yahoo

2. **Scoring Settings Section** with two main categories:

#### Batting Statistics
- Singles, Doubles, Triples, Home Runs
- Walks, Intentional Walks, Hit By Pitch
- Runs, Runs Batted In
- Stolen Base, Caught Stealing, Strike Outs

#### Pitching Statistics
- Walks Issued, Intentional Base on Balls
- Earned Runs, Hits allowed, Hit Batters
- Home Runs Allowed, Innings, Strikeouts
- Wins, Losses, Saves, Blown Saves
- Quality Starts, Total Bases

## League-Specific Scoring Values

### Custom League
- Singles=1.0, Doubles=2.0, Triples=3.0, Home Runs=4.0
- Walks=1.0, Intentional Walks=1.0, Hit By Pitch=1.0
- Runs=1.0, Runs Batted In=1.0, Stolen Base=1.0
- Caught Stealing=-1.0, Strike Outs=0.5
- Walks Issued=-1.0, Intentional Base on Balls=-1.0
- Earned Runs=-1.0, Hits allowed=-1.0, Hit Batters=-1.0
- Home Runs Allowed=-1.0, Innings=3.0, Strikeouts=0.5
- Wins=2.0, Losses=-1.0, Saves=2.0, Blown Saves=-1.0
- Quality Starts=2.0, Total Bases=0.0

### ESPN League
- Singles=1.0, Doubles=2.0, Triples=3.0, Home Runs=4.0
- Walks=1.0, Intentional Walks=0.0, Hit By Pitch=0.0
- Runs=1.0, Runs Batted In=1.0, Stolen Base=1.0
- Caught Stealing=0.0, Strike Outs=-1.0
- Walks Issued=-1.0, Intentional Base on Balls=-1.0
- Earned Runs=-1.0, Hits allowed=-1.0, Hit Batters=0.0
- Home Runs Allowed=-1.0, Innings=3.0, Strikeouts=1.0
- Wins=2.0, Losses=-1.0, Saves=2.0, Blown Saves=0.0
- Quality Starts=0.0, Total Bases=0.0

### CBS League
- Singles=1.0, Doubles=2.0, Triples=3.0, Home Runs=4.0
- Walks=1.0, Intentional Walks=1.0, Hit By Pitch=1.0
- Runs=1.0, Runs Batted In=1.0, Stolen Base=2.0
- Caught Stealing=-1.0, Strike Outs=-1.0
- Walks Issued=-1.0, Intentional Base on Balls=-1.0
- Earned Runs=-1.0, Hits allowed=-1.0, Hit Batters=0.0
- Home Runs Allowed=-1.0, Innings=3.0, Strikeouts=1.0
- Wins=5.0, Losses=-3.0, Saves=2.0, Blown Saves=-2.0
- Quality Starts=0.0, Total Bases=0.0

### Yahoo League
- Singles=1.0, Doubles=2.0, Triples=3.0, Home Runs=4.0
- Walks=1.0, Intentional Walks=1.0, Hit By Pitch=1.0
- Runs=1.0, Runs Batted In=1.0, Stolen Base=2.0
- Caught Stealing=-1.0, Strike Outs=-1.0
- Walks Issued=-1.0, Intentional Base on Balls=-1.0
- Earned Runs=-1.0, Hits allowed=-1.0, Hit Batters=0.0
- Home Runs Allowed=-1.0, Innings=3.0, Strikeouts=1.0
- Wins=5.0, Losses=-3.0, Saves=2.0, Blown Saves=-2.0
- Quality Starts=0.0, Total Bases=0.0

## Visual Features

- **Color-coded values**: 
  - Green for positive scoring (points awarded)
  - Red for negative scoring (points deducted)
  - Gray for neutral scoring (no points)
- **Responsive grid layout** that adapts to different screen sizes
- **Interactive input fields** that allow manual customization
- **Automatic updates** when league type changes

## Usage

```tsx
import FantasyExpectedStart from './components/FantasyExpectedStart';

function App() {
  return (
    <div className="App">
      <FantasyExpectedStart />
    </div>
  );
}
```

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

The component is fully self-contained and manages its own state for scoring settings and league type selection.
