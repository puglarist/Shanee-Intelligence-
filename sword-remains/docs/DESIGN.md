# Design System — The Sword Remains

## Overview

The design system embodies the principles of **Shanee Nation**: ceremonial weight, earthy authenticity, elegant efficiency (sleek), and accessibility for all.

Every color, typeface, spacing decision reflects the philosophy:
- **Gold**: Precious knowledge, ancestral wealth
- **Earth tones**: Connection to Appalachian land
- **Cinzel**: Ceremonial, sovereign authority
- **Space**: Breathing room, respect for contemplation

---

## COLOR PALETTE

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Gold** | `#c8960c` | 200, 150, 12 | Primary accent, icons, borders |
| **Light Gold** | `#f0d060` | 240, 208, 96 | Headings, emphasis, glow effects |
| **Dim Gold** | `#7a5a10` | 122, 90, 16 | Secondary text, subtle accents |
| **Gold Pale** | `rgba(200,150,12,0.15)` | — | Backgrounds, very subtle |

### Neutral Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Ink** | `#0a0806` | 10, 8, 6 | Main background, deep text |
| **Stone** | `#1a1610` | 26, 22, 16 | Secondary backgrounds, structure |
| **Parchment** | `#e8d9a0` | 232, 217, 160 | Body text, readable content |
| **Blade** | `#c8d0d8` | 200, 208, 216 | Sword/metal elements |

### CSS Variables

```css
:root {
  --gold: #c8960c;
  --gold-light: #f0d060;
  --gold-dim: #7a5a10;
  --gold-pale: rgba(200,150,12,0.15);
  --ink: #0a0806;
  --stone: #1a1610;
  --parchment: #e8d9a0;
  --blade: #c8d0d8;
}
```

---

## TYPOGRAPHY

### Font Families

#### Cinzel Decorative
- **Purpose**: Ceremony, sacred declarations, main headings
- **Weights**: 400, 700, 900
- **Import**: Google Fonts
- **Usage**: 
  - H1, main titles
  - Section headings (when ceremonial)
  - Pillar names
  - Signature blocks

```css
font-family: 'Cinzel Decorative', serif;
```

#### Cinzel
- **Purpose**: Primary body text, strong structure
- **Weights**: 400, 600, 700
- **Import**: Google Fonts
- **Usage**:
  - Navigation
  - Body paragraphs
  - Labels
  - Structured information

```css
font-family: 'Cinzel', serif;
```

#### IM Fell English
- **Purpose**: Contemplative, italic, historical
- **Styles**: Normal, Italic
- **Import**: Google Fonts
- **Usage**:
  - Subtitles
  - Italicized sections
  - Pillar descriptions
  - Poetic passages
  - Decree text

```css
font-family: 'IM Fell English', serif;
```

### Font Sizes & Hierarchy

```css
/* Main heading */
font-size: clamp(28px, 6vw, 52px);  /* Responsive */
font-weight: 900;

/* Sub-heading */
font-size: clamp(13px, 2.5vw, 16px);
font-style: italic;

/* Section title */
font-size: clamp(11px, 2.5vw, 14px);
font-weight: 700;

/* Body text */
font-size: 14px;
line-height: 1.6;

/* Small text (labels, captions) */
font-size: 10px;
letter-spacing: 0.1em;
text-transform: uppercase;
```

### Letter Spacing

- **Headings**: `0.08em` (ceremonial weight)
- **Labels**: `0.1em` to `0.5em` (small caps, distinctive)
- **Body**: `0.02em` (comfortable reading)
- **Decree text**: `0.06em` (poetic, spaced)

---

## SPACING & LAYOUT

### Responsive Container
- **Max width**: 760px (readable column width)
- **Padding**: `4rem 2rem` (desktop), `2rem` (mobile)
- **Centered**: `margin: 0 auto`

### Section Spacing

| Element | Margin Top | Margin Bottom |
|---------|------------|---------------|
| Page body | 4rem | 6rem |
| Main heading | — | 0.4rem |
| Sub-heading | — | 4rem |
| Pillars container | — | 1rem |
| Rule ornament | 2rem | 2rem |
| Decree section | — | —varies— |
| Roots section | — | —varies— |

### Grid System

**Pillars (3-column responsive)**
```css
.pillars {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

@media (max-width: 520px) {
  grid-template-columns: 1fr;
}
```

---

## COMPONENTS

### Navigation Header
- **Position**: `fixed top 0`
- **Background**: `rgba(10,8,6,0.95)` (semi-transparent ink)
- **Border**: `0.5px solid rgba(200,150,12,0.2)` (subtle gold)
- **Padding**: `1rem 2rem`
- **Height**: Approx 60px (space account for in page padding-top)

### Button / CTA
```css
.cta-button {
  padding: 0.75rem 2rem;
  background: rgba(200,150,12,0.1);
  border: 1px solid var(--gold-dim);
  color: var(--gold-light);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  transition: all 0.3s;
}

.cta-button:hover {
  background: rgba(200,150,12,0.2);
  border-color: var(--gold-light);
}
```

### Cards / Pillars
```css
.pillar {
  background: rgba(200,150,12,0.04);
  border: 0.5px solid rgba(200,150,12,0.2);
  border-top: 1.5px solid var(--gold-dim);
  padding: 1.25rem 1rem;
  transition: border-color 0.3s, background 0.3s;
}

.pillar:hover {
  background: rgba(200,150,12,0.08);
  border-color: rgba(200,150,12,0.4);
  border-top-color: var(--gold);
}
```

### Rules / Dividers
```css
.rule {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
  margin: 2.5rem 0;
  opacity: 0.5;
}

.rule-ornament {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rule-ornament::before,
.rule-ornament::after {
  content: '';
  flex: 1;
  height: 0.5px;
  background: linear-gradient(90deg, transparent, var(--gold-dim));
}
```

---

## ANIMATIONS

### Fade In (Entrance)
```css
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Applied with staggered delays */
.element { animation: fade-in 1.5s ease-out forwards; }
.element-2 { animation: fade-in 1.8s ease-out 0.2s both; }
```

### Float (Gentle upward motion)
```css
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.scene-svg { animation: float 6s ease-in-out infinite; }
```

### Orbit (Rotating rings)
```css
@keyframes orbit {
  to { transform: rotate(360deg); }
}

.orbit-1 { animation: orbit 25s linear infinite; }
.orbit-2 { animation: orbit 15s linear infinite reverse; }
.orbit-3 { animation: orbit 40s linear infinite; }
```

### Grow (Progress bars)
```css
@keyframes grow {
  to { width: var(--w, 60%); }
}

.root-fill {
  animation: grow 3s cubic-bezier(0.25, 1, 0.5, 1) forwards;
}
```

---

## RESPONSIVE BREAKPOINTS

### Mobile (< 520px)
- Grid becomes single column
- Smaller font sizes (clamp handles this)
- Reduced padding
- Simplified navigation

```css
@media (max-width: 520px) {
  .pillars { grid-template-columns: 1fr; max-width: 320px; }
  .decree { padding: 1.75rem 1.25rem; }
  .scene-wrap { height: 380px; }
  .scene-svg { width: 160px; height: 360px; }
}
```

### Tablet (520px - 900px)
- Default styles, maybe slight padding adjustments

### Desktop (900px+)
- Full layout with breathing room

---

## ACCESSIBILITY

### Color Contrast
- **Gold on Ink**: Checked for WCAG AA compliance
- **Parchment on Ink**: High contrast (232,217,160 on 10,8,6)
- **All interactive elements**: Maintain 4.5:1+ contrast ratio

### Focus States
```css
a:focus,
button:focus {
  outline: 2px solid var(--gold-light);
  outline-offset: 2px;
}
```

### Font Sizing
- Minimum font size: 10px (for small labels)
- Body text minimum: 14px
- Use `clamp()` for responsive sizing without media queries

### Readability
- Line height: 1.6+ for body text
- Max line length: 760px
- Proper letter spacing for small caps

---

## VISUAL HIERARCHY

### Ceremony & Weight
1. **Page background**: Deep ink (ceremonial darkness)
2. **Main heading**: Largest, brightest (Light Gold)
3. **Sub-heading**: Smaller, italicized (Dim Gold, italic)
4. **Pillars**: Equal visual weight (emphasize three-fold)
5. **Decree**: Framed, centered, authoritative
6. **Root system**: Data visualization, subtle animation
7. **Signature**: Diminished scale (humble signature of authority)

### Visual Cues
- **Hover states**: Add background, brighten border
- **Active states**: Maintain hover with additional indicator
- **Disabled states**: Reduce opacity, gray out gold
- **Loading states**: Use subtle pulse or animation

---

## IMPLEMENTATION CHECKLIST

When adding new pages or components:

- [ ] Use CSS variables for colors (never hardcode)
- [ ] Use `clamp()` for responsive font sizes
- [ ] Maintain 4.5:1+ contrast on interactive elements
- [ ] Add transitions to interactive elements (0.3s recommended)
- [ ] Apply fade-in animation (with appropriate delay)
- [ ] Test on mobile (< 520px)
- [ ] Ensure parchment text is readable (14px minimum)
- [ ] Respect the gold accent color hierarchy
- [ ] Use Cinzel/Cinzel Decorative for headers
- [ ] Use IM Fell English for italicized/contemplative text
- [ ] Center content with max-width container
- [ ] Add proper spacing between sections (2.5rem standard)

---

## REFERENCES

- **Design inspiration**: Ceremonial, medieval manuscripts, Appalachian sovereignty
- **Font source**: Google Fonts
- **Color philosophy**: Precious (gold), earthy (stone), clear (parchment)
- **Layout philosophy**: Centered, breathable, respectful of white space

---

*The Sword Remains — Design System · In service of sleek, accessible, ceremonial clarity*
