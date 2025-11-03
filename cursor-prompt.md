# Cursor Prompt: Personal Recipe Manager Application

Copy and paste this entire prompt into Cursor to generate your recipe management application.

---

## PROJECT REQUEST

Create a complete personal recipe management web application using React, Vite, and Tailwind CSS. This is a client-side only application with no backend - all data is stored in a static JSON file.

## REQUIREMENTS

### Core Functionality
1. **Recipe Selection Page**: Display all recipes in a checkbox list
   - Allow selecting up to 5 recipes at a time
   - Disable checkboxes once 5 are selected
   - Show recipe title, cook time, and servings for each
   - Alphabetically sorted list

2. **Shopping List Generation**: 
   - Combine ingredients from all selected recipes
   - Aggregate duplicate ingredients (show quantities from each recipe)
   - Display in a clean, printable format
   - Include ingredient categories (produce, protein, dairy, pantry, spices)

3. **Recipe Detail View**:
   - Show full recipe when clicked
   - Display: title, cook time, servings, ingredients, step-by-step instructions
   - Modal overlay or side panel (your choice for best UX)

### Technical Requirements
- **Framework**: React 18+ with Vite
- **Styling**: Tailwind CSS (utility-first approach)
- **State Management**: React Context API or component state
- **Data Source**: `public/recipes.json` file (structure provided below)
- **No authentication or backend** - personal use only
- **Responsive design** - works on desktop and mobile

## PROJECT STRUCTURE

```
recipe-manager/
├── public/
│   └── recipes.json          # Recipe data (I'll provide this)
├── src/
│   ├── components/
│   │   ├── RecipeList.jsx    # Main recipe checkbox list
│   │   ├── ShoppingList.jsx  # Combined shopping list view
│   │   ├── RecipeDetail.jsx  # Full recipe modal/view
│   │   └── Header.jsx        # App header (optional)
│   ├── context/
│   │   └── RecipeContext.jsx # State management (if using Context)
│   ├── utils/
│   │   └── aggregateIngredients.js  # Shopping list aggregation logic
│   ├── App.jsx               # Main app component
│   ├── App.css               # Custom styles
│   ├── index.css             # Tailwind directives
│   └── main.jsx              # Entry point
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

## DATA STRUCTURE

The `recipes.json` file has this structure:

```json
{
  "recipes": [
    {
      "id": "minestrone-soup-kidney-beans",
      "title": "Minestrone Soup with Kidney Beans, Green Beans, Carrots & Pasta",
      "cookTime": "30 minutes",
      "servings": 2,
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
        }
      ],
      "instructions": [
        {
          "step": 1,
          "text": "Wash and dry the fresh produce."
        },
        {
          "step": 2,
          "text": "Peel, trim, and small dice carrot; trim and small dice celery."
        }
      ],
      "tags": []
    }
  ]
}
```

## COMPONENT SPECIFICATIONS

### App.jsx
- Load recipes from `public/recipes.json` on mount
- Manage selected recipe IDs (up to 5)
- Handle view switching (recipe list, shopping list, recipe detail)
- Pass data to child components

### RecipeList.jsx
**Props**: `recipes`, `selectedIds`, `onToggleRecipe`, `onViewRecipe`, `maxSelections`

**Display**:
- Scrollable list of all recipes with checkboxes
- Each item shows: checkbox, title, cook time, servings
- "Generate Shopping List" button (only enabled when 1+ recipes selected)
- "Clear Selection" button
- Disable checkboxes after 5 selections

**Styling**:
- Fixed height container with scroll
- Hover effects on recipe items
- Clear visual indication of selected recipes

### ShoppingList.jsx
**Props**: `selectedRecipes`, `onClose`

**Logic**:
- Aggregate ingredients from all selected recipes
- Group duplicate ingredients (same name) and show all quantities
- Sort alphabetically or by category

**Display**:
- Modal or full-page view
- Recipe titles included in shopping list
- List of ingredients with quantities
- Each ingredient shows which recipe(s) it's from if duplicate
- "Back to Recipes" button
- Optional: Print button with print-friendly CSS

**Example output**:
```
Shopping List

Recipes:
- Minestrone Soup
- Chicken Thighs with Kale Salad

Ingredients:

Produce:
□ carrot - 2 medium (1 from Minestrone Soup, 1 from Kale Salad)
□ green onions - ½ bunch (Kale Salad)

Pantry:
□ chicken broth - 32 fl oz (Minestrone Soup)
```

### RecipeDetail.jsx
**Props**: `recipe`, `onClose`

**Display**:
- Modal overlay or slide-in panel
- Recipe title
- Cook time and servings
- Full ingredient list with quantities
- Numbered step-by-step instructions
- Close/back button

## INGREDIENT AGGREGATION LOGIC

Create a utility function in `src/utils/aggregateIngredients.js`:

```javascript
/**
 * Aggregate ingredients from multiple recipes
 * Combines duplicate ingredients and tracks which recipe they're from
 */
export function aggregateIngredients(recipes) {
  const ingredientMap = new Map();
  
  recipes.forEach(recipe => {
    recipe.ingredients.forEach(ingredient => {
      const key = ingredient.name.toLowerCase().trim();
      
      if (ingredientMap.has(key)) {
        // Add to existing ingredient
        const existing = ingredientMap.get(key);
        existing.quantities.push({
          amount: ingredient.quantity,
          recipe: recipe.title
        });
      } else {
        // Create new ingredient entry
        ingredientMap.set(key, {
          name: ingredient.name,
          category: ingredient.category || 'other',
          quantities: [{
            amount: ingredient.quantity,
            recipe: recipe.title
          }]
        });
      }
    });
  });
  
  // Convert to array and sort by category, then name
  const categories = ['produce', 'protein', 'dairy', 'pantry', 'spices', 'other'];
  
  return Array.from(ingredientMap.values())
    .sort((a, b) => {
      const catDiff = categories.indexOf(a.category) - categories.indexOf(b.category);
      return catDiff !== 0 ? catDiff : a.name.localeCompare(b.name);
    });
}
```

## STYLING GUIDELINES

### Tailwind Setup
1. Install Tailwind: `npm install -D tailwindcss postcss autoprefixer`
2. Initialize: `npx tailwindcss init -p`
3. Configure `tailwind.config.js`:
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

4. Add to `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
  
  .shopping-list-item {
    break-inside: avoid;
  }
}
```

### Design System
- **Colors**: Use Tailwind's default palette (blue for primary, gray for neutral)
- **Spacing**: Consistent padding/margin (p-4, m-2, etc.)
- **Typography**: Clear hierarchy (text-2xl for titles, text-base for body)
- **Borders**: Subtle borders (border-gray-200) to separate sections
- **Hover states**: Add hover:bg-gray-50 for interactive elements
- **Focus states**: Ensure keyboard navigation is clear

### Component Styling Examples

**RecipeList Item**:
```jsx
<div className="flex items-center p-4 border-b hover:bg-gray-50 cursor-pointer">
  <input type="checkbox" className="mr-4 h-5 w-5" />
  <div className="flex-1">
    <h3 className="font-semibold text-gray-900">{title}</h3>
    <p className="text-sm text-gray-600">{cookTime} • {servings} servings</p>
  </div>
</div>
```

**Shopping List**:
```jsx
<div className="fixed inset-0 bg-white overflow-y-auto p-6">
  <div className="max-w-2xl mx-auto">
    <div className="flex justify-between items-center mb-6">
      <h2 className="text-3xl font-bold">Shopping List</h2>
      <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Print
      </button>
    </div>
    {/* Content */}
  </div>
</div>
```

## DEVELOPMENT SETUP

### Initial Setup Commands
```bash
# Create Vite project
npm create vite@latest recipe-manager -- --template react
cd recipe-manager
npm install

# Install Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Start development server
npm run dev
```

### Package.json Scripts
Ensure these scripts exist:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## USER FLOW

1. **App loads** → Fetch recipes.json → Display recipe list
2. **User checks recipes** → Update selected state (max 5)
3. **User clicks "Generate Shopping List"** → Navigate to shopping list view
4. **Shopping list displays** → Aggregated ingredients by category
5. **User clicks recipe name** (optional) → Show recipe detail modal
6. **User returns** → Back to recipe list, selection preserved

## ADDITIONAL FEATURES (NICE TO HAVE)

If time permits, add these enhancements:
- [ ] Recipe count badge showing "X of 5 selected"
- [ ] Smooth animations for modal/view transitions
- [ ] Keyboard shortcuts (ESC to close modal)
- [ ] Local storage to persist selections between sessions
- [ ] "Select All" / "Clear All" buttons
- [ ] Recipe search/filter (future enhancement placeholder)

## ERROR HANDLING

- Show loading spinner while fetching recipes.json
- Display error message if recipes.json fails to load
- Handle empty recipe list gracefully
- Validate that recipes.json has correct structure

## TESTING CHECKLIST

Before considering complete, verify:
- [ ] All recipes load from JSON
- [ ] Can select up to 5 recipes (6th checkbox disabled)
- [ ] Shopping list correctly aggregates duplicate ingredients
- [ ] Recipe detail modal shows all information
- [ ] Can navigate back from shopping list and detail views
- [ ] Responsive on mobile (320px+) and desktop
- [ ] Print shopping list works (print-friendly CSS)
- [ ] No console errors
- [ ] Build succeeds: `npm run build`

## SAMPLE recipes.json (FOR TESTING)

Create a minimal `public/recipes.json` with 3 recipes to test with:

```json
{
  "recipes": [
    {
      "id": "minestrone-soup",
      "title": "Minestrone Soup with Kidney Beans",
      "cookTime": "30 minutes",
      "servings": 2,
      "ingredients": [
        {"name": "carrot", "quantity": "1 medium", "category": "produce"},
        {"name": "celery", "quantity": "1 stick", "category": "produce"},
        {"name": "kidney beans", "quantity": "1 can (15 oz)", "category": "pantry"},
        {"name": "pasta", "quantity": "3 oz", "category": "pantry"},
        {"name": "salt", "quantity": "½ tsp", "category": "spices"}
      ],
      "instructions": [
        {"step": 1, "text": "Wash and dry the fresh produce."},
        {"step": 2, "text": "Dice carrot and celery."},
        {"step": 3, "text": "Add broth and bring to boil."}
      ]
    },
    {
      "id": "chicken-salad",
      "title": "Pan-Fried Chicken with Kale Salad",
      "cookTime": "30 minutes",
      "servings": 2,
      "ingredients": [
        {"name": "chicken thighs", "quantity": "1 lb", "category": "protein"},
        {"name": "kale", "quantity": "½ bunch", "category": "produce"},
        {"name": "carrot", "quantity": "1 medium", "category": "produce"},
        {"name": "peanut butter", "quantity": "2 tbsp", "category": "pantry"},
        {"name": "salt", "quantity": "½ tsp", "category": "spices"}
      ],
      "instructions": [
        {"step": 1, "text": "Wash and dry the fresh produce."},
        {"step": 2, "text": "Pat chicken thighs dry and season."},
        {"step": 3, "text": "Pan fry until golden brown."}
      ]
    },
    {
      "id": "quesadilla",
      "title": "Mushroom & Cheddar Quesadilla",
      "cookTime": "25 minutes",
      "servings": 2,
      "ingredients": [
        {"name": "mushrooms", "quantity": "2 caps", "category": "produce"},
        {"name": "cheddar cheese", "quantity": "4 oz", "category": "dairy"},
        {"name": "tortillas", "quantity": "2 large", "category": "pantry"},
        {"name": "garlic", "quantity": "1 clove", "category": "produce"}
      ],
      "instructions": [
        {"step": 1, "text": "Slice mushrooms thinly."},
        {"step": 2, "text": "Grate cheese."},
        {"step": 3, "text": "Assemble quesadilla and cook until golden."}
      ]
    }
  ]
}
```

## DEPLOYMENT (AFTER DEVELOPMENT)

Once the app is working locally:

1. **Build**: `npm run build`
2. **Test build**: `npm run preview`
3. **Deploy to Vercel**:
   - Push to GitHub
   - Connect repository to Vercel
   - Vercel auto-detects Vite and deploys
4. **OR deploy to Netlify**:
   - Drag `dist/` folder to Netlify
   - Or connect GitHub repository

## FINAL DELIVERABLES

Please generate:
1. ✅ Complete React application with all components
2. ✅ Vite configuration
3. ✅ Tailwind configuration
4. ✅ Sample recipes.json with 3 test recipes
5. ✅ Package.json with all dependencies
6. ✅ README.md with setup instructions
7. ✅ Working shopping list aggregation logic
8. ✅ Responsive, clean UI

## NOTES

- This is for personal use only - no authentication needed
- Keep the UI clean and simple - prioritize usability over fancy features
- Use semantic HTML for accessibility
- Ensure keyboard navigation works
- Make it print-friendly for shopping lists
- Code should be well-commented for easy modification later

---

## ONCE COMPLETE

After generating the code, please provide:
1. Instructions on how to run the app locally
2. How to add the real `recipes.json` file (109 recipes)
3. Any manual steps needed
4. Brief explanation of the code structure

Thank you!
