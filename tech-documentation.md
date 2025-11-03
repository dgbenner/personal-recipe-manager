# Technical Documentation: Personal Recipe Manager

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Data Model](#data-model)
4. [Component Structure](#component-structure)
5. [State Management](#state-management)
6. [PDF Conversion Process](#pdf-conversion-process)
7. [Deployment Architecture](#deployment-architecture)
8. [Performance Considerations](#performance-considerations)

---

## System Architecture

### Overview
This is a **client-side only** web application with no backend server. All data is stored in a static JSON file and processed entirely in the browser.

```
┌─────────────────────────────────────────────────────────┐
│                     User Browser                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              React Application                     │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │  │
│  │  │   Recipe    │  │  Shopping   │  │  Recipe   │ │  │
│  │  │    List     │  │    List     │  │  Detail   │ │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘ │  │
│  │         │                │                │        │  │
│  │         └────────────────┴────────────────┘        │  │
│  │                        │                           │  │
│  │                   ┌────▼────┐                      │  │
│  │                   │  State  │                      │  │
│  │                   │ (React) │                      │  │
│  │                   └────┬────┘                      │  │
│  │                        │                           │  │
│  │                   ┌────▼────┐                      │  │
│  │                   │ recipes │                      │  │
│  │                   │  .json  │                      │  │
│  │                   └─────────┘                      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Application Flow

1. **Initial Load**: Application fetches `recipes.json` from public folder
2. **Recipe Selection**: User checks recipes, state updates in React
3. **Shopping List**: Selected recipes trigger ingredient aggregation
4. **Recipe View**: Clicking recipe shows full instructions

---

## Technology Stack

### Frontend
- **React 18+**: Component-based UI framework
- **Vite**: Build tool and dev server (faster than Create React App)
- **Tailwind CSS**: Utility-first styling framework

### Development Tools
- **Node.js**: JavaScript runtime for development
- **npm**: Package manager
- **ESLint**: Code linting (included with Vite)

### Deployment
- **Vercel** or **Netlify**: Static site hosting with CDN
- **GitHub**: Version control and deployment trigger

### PDF Processing (One-time Setup)
- **Python 3.7+**: Script runtime
- **PyPDF2**: PDF text extraction library

---

## Data Model

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "recipes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "cookTime", "servings", "ingredients", "instructions"],
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier (generated from title slug)"
          },
          "title": {
            "type": "string",
            "description": "Full recipe name"
          },
          "cookTime": {
            "type": "string",
            "description": "Total time in minutes (e.g., '30 minutes')"
          },
          "servings": {
            "type": "integer",
            "description": "Number of servings"
          },
          "cookware": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "Optional: List of required cookware"
          },
          "ingredients": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "quantity"],
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Ingredient name (lowercase, normalized)"
                },
                "quantity": {
                  "type": "string",
                  "description": "Amount with unit (e.g., '1 medium', '2 tbsp')"
                },
                "category": {
                  "type": "string",
                  "enum": ["produce", "protein", "dairy", "pantry", "spices"],
                  "description": "Optional: Shopping list category"
                },
                "original": {
                  "type": "string",
                  "description": "Original text from PDF (for reference)"
                }
              }
            }
          },
          "instructions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["step", "text"],
              "properties": {
                "step": {
                  "type": "integer",
                  "description": "Sequential step number"
                },
                "text": {
                  "type": "string",
                  "description": "Instruction text"
                },
                "ingredients": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "Optional: Ingredients used in this step"
                }
              }
            }
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "Optional: Categories for future filtering"
          }
        }
      }
    }
  }
}
```

### Example Recipe Object

```json
{
  "id": "minestrone-soup-kidney-beans",
  "title": "Minestrone Soup with Kidney Beans, Green Beans, Carrots & Pasta",
  "cookTime": "30 minutes",
  "servings": 2,
  "cookware": [
    "medium saucepan",
    "chef's knife",
    "cutting board"
  ],
  "ingredients": [
    {
      "name": "carrot",
      "quantity": "1 medium",
      "category": "produce",
      "original": "1 medium carrot"
    },
    {
      "name": "chicken broth",
      "quantity": "32 fl oz",
      "category": "pantry",
      "original": "32 fl oz chicken or vegetable broth"
    },
    {
      "name": "kidney beans",
      "quantity": "1 (15 oz) can",
      "category": "pantry",
      "original": "1 (15 oz) can kidney beans"
    }
  ],
  "instructions": [
    {
      "step": 1,
      "text": "Wash and dry the fresh produce.",
      "ingredients": ["carrot", "celery", "green beans"]
    },
    {
      "step": 2,
      "text": "Peel, trim, and small dice carrot; trim and small dice celery. Place both in a small bowl."
    }
  ],
  "tags": ["soup", "vegetarian-option", "quick"]
}
```

---

## Component Structure

### Component Hierarchy

```
App
├── Header (static)
├── RecipeList
│   └── RecipeCheckbox (multiple)
├── SelectedRecipesPanel
│   ├── RecipeChip (multiple)
│   └── GenerateListButton
├── ShoppingList
│   └── IngredientItem (multiple)
└── RecipeDetail (modal or route)
    ├── RecipeHeader
    ├── IngredientList
    └── InstructionList
```

### Component Specifications

#### App.jsx
**Purpose**: Root component managing application state

```javascript
// State Structure
{
  recipes: [],              // All recipes from JSON
  selectedRecipeIds: [],    // Array of selected recipe IDs
  shoppingList: [],         // Aggregated ingredients
  currentRecipe: null       // Recipe being viewed in detail
}
```

**Responsibilities**:
- Load recipes.json on mount
- Manage selected recipes
- Calculate shopping list
- Handle navigation between views

---

#### RecipeList.jsx
**Purpose**: Display all recipes with checkboxes

**Props**:
```javascript
{
  recipes: Array,
  selectedIds: Array,
  onToggle: Function,
  maxSelections: Number (default: 5)
}
```

**State**: None (controlled component)

**Features**:
- Checkbox list of all recipes
- Display recipe title, cook time, servings
- Disable checkboxes after 5 selections
- Sort alphabetically

**Styling Notes**:
- Fixed height with scroll
- Sticky header
- Hover states for better UX

---

#### ShoppingList.jsx
**Purpose**: Display aggregated ingredients from selected recipes

**Props**:
```javascript
{
  selectedRecipes: Array,
  onClose: Function
}
```

**State**:
```javascript
{
  aggregatedIngredients: Array,
  checkedItems: Set
}
```

**Key Functions**:
```javascript
// Aggregate ingredients from multiple recipes
function aggregateIngredients(recipes) {
  const ingredientMap = new Map();
  
  recipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
      const key = ingredient.name.toLowerCase();
      if (ingredientMap.has(key)) {
        // Combine quantities (if same unit)
        const existing = ingredientMap.get(key);
        existing.quantities.push(ingredient.quantity);
      } else {
        ingredientMap.set(key, {
          name: ingredient.name,
          quantities: [ingredient.quantity],
          category: ingredient.category
        });
      }
    });
  });
  
  return Array.from(ingredientMap.values());
}
```

**Features**:
- Group ingredients by category (optional)
- Show quantities from each recipe
- Checkbox to mark items as purchased
- Print button (CSS print styles)

---

#### RecipeDetail.jsx
**Purpose**: Show full recipe instructions

**Props**:
```javascript
{
  recipe: Object,
  onClose: Function
}
```

**Display**:
- Recipe title
- Cook time and servings
- Full ingredient list with quantities
- Step-by-step numbered instructions
- Cookware list (optional)

**Implementation Options**:
1. **Modal**: Overlay on top of recipe list
2. **Separate route**: Navigate to `/recipe/:id`
3. **Side panel**: Slide in from right

Recommendation: **Modal** for simplicity (no routing needed)

---

## State Management

### Option 1: React Context (Recommended for this app)

```javascript
// RecipeContext.js
import { createContext, useState, useEffect } from 'react';

export const RecipeContext = createContext();

export function RecipeProvider({ children }) {
  const [recipes, setRecipes] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [currentRecipe, setCurrentRecipe] = useState(null);

  // Load recipes on mount
  useEffect(() => {
    fetch('/recipes.json')
      .then(res => res.json())
      .then(data => setRecipes(data.recipes));
  }, []);

  // Computed: selected recipes
  const selectedRecipes = recipes.filter(r => 
    selectedIds.includes(r.id)
  );

  // Actions
  const toggleRecipe = (id) => {
    setSelectedIds(prev =>
      prev.includes(id)
        ? prev.filter(i => i !== id)
        : prev.length < 5 ? [...prev, id] : prev
    );
  };

  const clearSelections = () => setSelectedIds([]);
  
  const viewRecipe = (id) => {
    const recipe = recipes.find(r => r.id === id);
    setCurrentRecipe(recipe);
  };

  return (
    <RecipeContext.Provider value={{
      recipes,
      selectedIds,
      selectedRecipes,
      currentRecipe,
      toggleRecipe,
      clearSelections,
      viewRecipe,
      closeRecipe: () => setCurrentRecipe(null)
    }}>
      {children}
    </RecipeContext.Provider>
  );
}
```

### Option 2: Component State (Simpler, also works)

Keep all state in `App.jsx` and pass props down. Works fine for small app.

---

## PDF Conversion Process

### Extraction Strategy

The PDF-to-JSON script parses Mealime PDFs using pattern matching:

1. **Title Extraction**: First page, largest text before time/servings
2. **Metadata**: Parse "X minutes | Y servings" line
3. **Sections**: Identify "Find cookware", "Grab ingredients", "Cook & enjoy"
4. **Ingredients**: Parse lines between "Grab ingredients" and "Cook & enjoy"
5. **Instructions**: Parse numbered steps after "Cook & enjoy"

### Parsing Challenges & Solutions

**Challenge 1**: Inconsistent ingredient formats
- Solution: Regex patterns for common formats, manual review

**Challenge 2**: Special characters in quantities (fractions)
- Solution: Unicode fraction mapping or keep as-is

**Challenge 3**: Multi-line instructions
- Solution: Detect step numbers, concatenate until next number

### Quality Assurance

After conversion:
1. Validate JSON structure
2. Check all recipes have required fields
3. Spot-check 10-15 recipes manually
4. Test app with generated JSON

---

## Deployment Architecture

### Build Process

```bash
npm run build
```

Vite outputs to `dist/` folder:
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   └── index-[hash].css
└── recipes.json (copied from public/)
```

### Vercel Deployment

**Configuration** (automatic with Vite detection):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install"
}
```

**Environment**:
- Node version: 18.x or higher
- Build time: ~30 seconds
- CDN: Global edge network

### Netlify Deployment

**Configuration** (`netlify.toml`):
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Performance Optimizations

1. **recipes.json size**: ~100KB for 109 recipes (acceptable)
2. **Code splitting**: Vite handles automatically
3. **Image optimization**: No images needed for MVP
4. **Caching**: Vercel/Netlify handle via CDN

---

## Performance Considerations

### Loading Time
- Initial load: ~200-300ms (recipes.json fetch)
- Subsequent interactions: Instant (client-side)

### Memory Usage
- 109 recipes: ~2-3MB memory
- Well within browser limits

### Scalability
- Current approach works up to ~500 recipes
- Beyond that, consider pagination or search

### Optimization Opportunities

1. **Lazy load recipe details**: Don't load instructions until clicked
2. **Virtual scrolling**: For 500+ recipes (not needed now)
3. **Service worker**: Offline support (future enhancement)

---

## Development Workflow

### Local Development

1. Start dev server: `npm run dev`
2. Make changes to components
3. Hot reload shows changes instantly
4. Test shopping list aggregation logic

### Testing Checklist

- [ ] All 109 recipes load
- [ ] Can select up to 5 recipes
- [ ] Shopping list combines ingredients correctly
- [ ] Recipe detail view shows all information
- [ ] Works on mobile viewport
- [ ] Print shopping list works

### Git Workflow

```bash
# Feature development
git checkout -b feature/shopping-list-categories
# Make changes
git add .
git commit -m "Add category grouping to shopping list"
git push origin feature/shopping-list-categories

# Deploy: Push to main branch
git checkout main
git merge feature/shopping-list-categories
git push origin main
# Vercel auto-deploys
```

---

## Future Enhancements

### Phase 2 Features
1. Recipe categories/tags with filtering
2. Shopping list item checkoff (persisted to localStorage)
3. Print-optimized views
4. Recipe notes/modifications

### Phase 3 Features
1. Recipe search
2. Favorite recipes
3. Recent recipes
4. Export shopping list to other apps

### Technical Improvements
1. Unit tests for aggregation logic
2. E2E tests with Playwright
3. TypeScript migration
4. PWA support for offline access

---

## Troubleshooting Guide

### Issue: Recipes not loading

**Check**:
1. Is `recipes.json` in `public/` folder?
2. Is JSON valid? (Use jsonlint.com)
3. Browser console errors?
4. Network tab: Is fetch successful?

**Fix**: Verify file path and JSON syntax

---

### Issue: Ingredient aggregation incorrect

**Check**:
1. Are ingredient names normalized (lowercase)?
2. Are quantities in consistent format?
3. Console log aggregation function output

**Fix**: Update normalization logic or manually fix JSON

---

### Issue: Build fails

**Check**:
1. Run `npm install` to ensure dependencies
2. Check for import errors
3. Verify all components have valid JSX

**Fix**: Check build logs, fix syntax errors

---

### Issue: Deployed app shows blank page

**Check**:
1. Browser console for errors
2. Network tab: Is recipes.json loading?
3. Check build output includes recipes.json

**Fix**: Ensure recipes.json is in `public/` before build

---

## API Reference (Internal Functions)

### Recipe Selection

```javascript
/**
 * Toggle recipe selection
 * @param {string} recipeId - Unique recipe identifier
 * @param {Array} currentSelections - Currently selected IDs
 * @param {number} maxSelections - Maximum allowed (default: 5)
 * @returns {Array} Updated selection array
 */
function toggleRecipeSelection(recipeId, currentSelections, maxSelections = 5) {
  if (currentSelections.includes(recipeId)) {
    return currentSelections.filter(id => id !== recipeId);
  }
  if (currentSelections.length >= maxSelections) {
    return currentSelections;
  }
  return [...currentSelections, recipeId];
}
```

### Ingredient Aggregation

```javascript
/**
 * Aggregate ingredients from multiple recipes
 * @param {Array} recipes - Array of recipe objects
 * @returns {Array} Aggregated ingredients with combined quantities
 */
function aggregateIngredients(recipes) {
  const ingredientMap = new Map();
  
  recipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
      const key = ingredient.name.toLowerCase().trim();
      
      if (ingredientMap.has(key)) {
        const existing = ingredientMap.get(key);
        existing.quantities.push({
          amount: ingredient.quantity,
          recipe: recipe.title
        });
      } else {
        ingredientMap.set(key, {
          name: ingredient.name,
          quantities: [{
            amount: ingredient.quantity,
            recipe: recipe.title
          }],
          category: ingredient.category || 'other'
        });
      }
    });
  });
  
  return Array.from(ingredientMap.values())
    .sort((a, b) => a.name.localeCompare(b.name));
}
```

### Quantity Parsing (Advanced)

```javascript
/**
 * Parse quantity string to extract amount and unit
 * @param {string} quantityStr - e.g., "1 medium", "2 tbsp", "1 (15 oz) can"
 * @returns {Object} { amount: number, unit: string, modifier: string }
 */
function parseQuantity(quantityStr) {
  // Regex patterns for common formats
  const patterns = [
    /^(\d+(?:\/\d+)?)\s+(.+)$/,           // "1 cup", "1/2 tsp"
    /^(\d+)\s+\((.+?)\)\s+(.+)$/,         // "1 (15 oz) can"
    /^(\d+)\s+(small|medium|large)\s+(.+)$/ // "1 medium carrot"
  ];
  
  // Implementation details...
  // Returns structured object for quantity math
}
```

---

## Appendix A: File Structure

```
recipe-manager/
├── public/
│   ├── recipes.json           # Recipe data (generated from PDFs)
│   └── vite.svg              # Default Vite logo (optional)
├── src/
│   ├── components/
│   │   ├── RecipeList.jsx
│   │   ├── RecipeCheckbox.jsx
│   │   ├── ShoppingList.jsx
│   │   ├── IngredientItem.jsx
│   │   ├── RecipeDetail.jsx
│   │   └── Header.jsx
│   ├── context/
│   │   └── RecipeContext.jsx  # State management (if using Context)
│   ├── utils/
│   │   ├── aggregateIngredients.js
│   │   └── parseQuantity.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.css              # Tailwind directives
│   └── main.jsx
├── scripts/
│   ├── pdf_to_json.py         # PDF conversion script
│   └── validate_json.py       # Optional: JSON validator
├── recipe-pdfs/               # Your 109 PDF files (not committed)
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── postcss.config.js          # Tailwind config
├── tailwind.config.js         # Tailwind config
├── vite.config.js             # Vite configuration
├── README.md
└── TECHNICAL_DOCS.md          # This file
```

---

## Appendix B: Tailwind Configuration

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors if needed
      },
    },
  },
  plugins: [],
}
```

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom print styles */
@media print {
  .no-print {
    display: none;
  }
  
  .shopping-list {
    break-inside: avoid;
  }
}
```

---

## Appendix C: Vite Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: undefined // Single chunk for small app
      }
    }
  },
  server: {
    port: 5173,
    open: true
  }
})
```

---

## Appendix D: Package.json Example

```json
{
  "name": "recipe-manager",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  }
}
```

---

## Summary

This technical documentation provides a complete blueprint for building a personal recipe management application. The architecture is intentionally simple: a client-side React app with JSON data storage, requiring no backend infrastructure.

Key design decisions:
- **No authentication**: Personal use only
- **Static JSON**: Simple, no database needed
- **Client-side only**: Easy deployment, low cost
- **React + Tailwind**: Modern, maintainable stack
- **Vercel/Netlify**: One-click deployment

The modular component structure allows for future enhancements while keeping the MVP simple and functional.
