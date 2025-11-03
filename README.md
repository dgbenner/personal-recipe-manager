# Personal Recipe Manager

A simple, browser-based recipe management application for organizing your Mealime recipes, creating shopping lists, and viewing cooking instructions.

## Overview

This application allows you to:
- Browse your collection of 109+ recipes
- Select 1-5 recipes for meal planning
- Generate a combined shopping list from selected recipes
- View detailed cooking instructions for each recipe
- No login required - designed for personal, local use

## Features

### Core Functionality
- **Recipe Selection**: Checkbox list to select multiple recipes
- **Shopping List Generation**: Automatically combines and consolidates ingredients from selected recipes
- **Recipe Instructions**: View step-by-step cooking instructions
- **Ingredient Quantities**: Automatically calculates total amounts needed

### Future Enhancements (Optional)
- Recipe categories/tags
- Shopping list item checkoff
- Print-friendly views
- Recipe search functionality

## Project Structure

```
recipe-manager/
├── public/
│   └── recipes.json          # All recipe data
├── src/
│   ├── components/
│   │   ├── RecipeList.jsx    # Checkbox list of recipes
│   │   ├── ShoppingList.jsx  # Combined ingredient list
│   │   └── RecipeDetail.jsx  # Full recipe instructions
│   ├── App.jsx                # Main application component
│   ├── index.css              # Tailwind styles
│   └── main.jsx               # Application entry point
├── scripts/
│   └── pdf_to_json.py         # PDF conversion script
├── package.json
└── README.md
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Python 3.7+ (for PDF conversion)

### Installation

1. **Clone or create the project directory**
   ```bash
   mkdir recipe-manager
   cd recipe-manager
   ```

2. **Initialize React application**
   ```bash
   npm create vite@latest . -- --template react
   npm install
   ```

3. **Install Tailwind CSS**
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

4. **Convert your PDFs to JSON**
   ```bash
   # Install Python dependencies
   pip install pypdf2 --break-system-packages
   
   # Run the conversion script
   python scripts/pdf_to_json.py
   ```

5. **Start the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to `http://localhost:5173`

## Converting Your Recipe PDFs

Place all your Mealime PDF files in a folder (e.g., `recipe-pdfs/`) and run:

```bash
python scripts/pdf_to_json.py --input recipe-pdfs/ --output public/recipes.json
```

The script will extract:
- Recipe titles
- Cook time and servings
- Ingredients with quantities
- Step-by-step instructions
- Cookware needed (optional)

## Deployment

### Deploy to Vercel (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Vite and deploy

### Deploy to Netlify (Alternative)

1. **Build your application**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**
   - Visit [netlify.com](https://netlify.com)
   - Drag and drop your `dist` folder
   - Or connect your GitHub repository for automatic deployments

## Usage

### Selecting Recipes
1. Browse the checkbox list of all your recipes
2. Check 1-5 recipes you want to cook
3. Click "Generate Shopping List"

### Shopping List
- View combined ingredients from all selected recipes
- Quantities are automatically totaled for duplicate ingredients
- Organized by ingredient type (future enhancement)

### Viewing Instructions
- Click any recipe name to view full cooking instructions
- Instructions appear in a separate view or modal
- Navigate back to recipe list when done

## Data Format

Recipes are stored in `public/recipes.json` with the following structure:

```json
{
  "recipes": [
    {
      "id": "unique-id",
      "title": "Recipe Name",
      "cookTime": "30 minutes",
      "servings": 2,
      "ingredients": [
        {
          "name": "carrot",
          "quantity": "1 medium",
          "category": "produce"
        }
      ],
      "instructions": [
        {
          "step": 1,
          "text": "Wash and dry the fresh produce."
        }
      ]
    }
  ]
}
```

## Customization

### Adding Categories
Edit `recipes.json` to add category tags:
```json
"tags": ["dinner", "vegetarian", "quick"]
```

### Styling
Modify `src/index.css` or component styles using Tailwind utility classes.

### Adding Features
The modular component structure makes it easy to add:
- Recipe filtering
- Print functionality
- Recipe ratings
- Notes/comments

## Troubleshooting

### PDFs not converting properly
- Ensure all PDFs follow the same Mealime format
- Check the Python script output for errors
- Manually edit `recipes.json` if needed

### Application not loading recipes
- Verify `recipes.json` is in the `public/` folder
- Check browser console for errors
- Ensure JSON is valid (use a JSON validator)

### Deployment issues
- Run `npm run build` locally to test
- Check build logs for errors
- Ensure all dependencies are in `package.json`

## License

This is a personal project for individual use. Mealime recipes are property of their respective owners.

## Support

This is a self-hosted, personal application. For technical issues:
1. Check the Technical Documentation
2. Review browser console errors
3. Verify `recipes.json` format
4. Test with a smaller subset of recipes first

## Acknowledgments

- Recipe format based on Mealime meal planning service
- Built with React, Vite, and Tailwind CSS
