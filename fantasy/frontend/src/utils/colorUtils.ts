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
   * Convert a score (0-1) to a color gradient from red to green
   */
  static scoreToColor(score: number): string {
    // Clamp score between 0 and 1
    const clampedScore = Math.max(0, Math.min(1, score));
    
    // Define color points for gradient
    const red: ColorRGB = { r: 220, g: 53, b: 69 };    // Bootstrap danger red
    const yellow: ColorRGB = { r: 255, g: 193, b: 7 }; // Bootstrap warning yellow
    const green: ColorRGB = { r: 40, g: 167, b: 69 };  // Bootstrap success green
    
    let color: ColorRGB;
    
    if (clampedScore < 0.5) {
      // Interpolate between red and yellow
      const t = clampedScore * 2; // Scale to 0-1
      color = {
        r: Math.round(red.r + (yellow.r - red.r) * t),
        g: Math.round(red.g + (yellow.g - red.g) * t),
        b: Math.round(red.b + (yellow.b - red.b) * t),
      };
    } else {
      // Interpolate between yellow and green
      const t = (clampedScore - 0.5) * 2; // Scale to 0-1
      color = {
        r: Math.round(yellow.r + (green.r - yellow.r) * t),
        g: Math.round(yellow.g + (green.g - yellow.g) * t),
        b: Math.round(yellow.b + (green.b - yellow.b) * t),
      };
    }
    
    return `rgb(${color.r}, ${color.g}, ${color.b})`;
  }

  /**
   * Get background color with opacity for better readability
   */
  static scoreToBackgroundColor(score: number, opacity: number = 0.1): string {
    const rgb = this.scoreToColor(score);
    // Convert rgb to rgba with opacity
    return rgb.replace('rgb', 'rgba').replace(')', `, ${opacity})`);
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
  static getColorCategory(score: number): 'excellent' | 'good' | 'average' | 'poor' {
    if (score >= 0.7) return 'excellent';
    if (score >= 0.5) return 'good';
    if (score >= 0.3) return 'average';
    return 'poor';
  }

  /**
   * Get CSS class name based on color category
   */
  static getCategoryClassName(category: string): string {
    switch (category) {
      case 'excellent':
        return 'matchup-excellent';
      case 'good':
        return 'matchup-good';
      case 'average':
        return 'matchup-average';
      case 'poor':
        return 'matchup-poor';
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

