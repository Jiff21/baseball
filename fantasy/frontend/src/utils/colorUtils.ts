/**
 * Utility functions for color calculations and gradients.
 */

export interface ColorRGB {
  r: number;
  g: number;
  b: number;
}

export class ColorUtils {
  /**
   * Convert a score (0-1) to a color based on category
   */
  static scoreToColor(score: number): string {
    // Use discrete colors based on score
    if (score >= 1.0) {
      // Good = Green
      return 'rgb(40, 167, 69)';  // Bootstrap success green
    } else if (score <= 0.0) {
      // Bad = Red  
      return 'rgb(220, 53, 69)';  // Bootstrap danger red
    } else {
      // Average = Dark gray (for borders/text)
      return 'rgb(108, 117, 125)'; // Bootstrap secondary gray
    }
  }

  /**
   * Get background color with opacity for better readability
   */
  static scoreToBackgroundColor(score: number, opacity: number = 0.1): string {
    if (score >= 1.0) {
      // Good = Light green background
      return `rgba(40, 167, 69, ${opacity})`;
    } else if (score <= 0.0) {
      // Bad = Light red background
      return `rgba(220, 53, 69, ${opacity})`;
    } else {
      // Average = White background (no tint)
      return 'rgba(255, 255, 255, 1)';
    }
  }

  /**
   * Get text color that contrasts well with the background
   */
  static getContrastTextColor(score: number): string {
    // For very light backgrounds, use dark text
    // For darker backgrounds, use light text
    return score > 0.7 ? '#ffffff' : '#000000';
  }

  /**
   * Get color category based on score
   */
  static getColorCategory(score: number): 'good' | 'average' | 'bad' {
    if (score >= 1.0) return 'good';
    if (score <= 0.0) return 'bad';
    return 'average';
  }

  /**
   * Get CSS class name based on color category
   */
  static getCategoryClassName(category: string): string {
    switch (category) {
      case 'good':
        return 'matchup-good';
      case 'average':
        return 'matchup-average';
      case 'bad':
        return 'matchup-bad';
      default:
        return 'matchup-average';
    }
  }

  /**
   * Generate CSS custom properties for dynamic coloring
   */
  static generateColorProperties(score: number): React.CSSProperties {
    const backgroundColor = this.scoreToBackgroundColor(score, 0.15);
    const borderColor = this.scoreToColor(score);
    const textColor = this.getContrastTextColor(score);
    
    return {
      '--matchup-bg-color': backgroundColor,
      '--matchup-border-color': borderColor,
      '--matchup-text-color': textColor,
    } as React.CSSProperties;
  }
}

export default ColorUtils;
