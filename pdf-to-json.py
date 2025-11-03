#!/usr/bin/env python3
"""
Mealime PDF to JSON Converter
Extracts recipe data from Mealime PDF files and converts to structured JSON format.

Usage:
    python pdf_to_json.py --input recipe-pdfs/ --output public/recipes.json
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
try:
    from PyPDF2 import PdfReader
except ImportError:
    print("ERROR: PyPDF2 not installed. Please run:")
    print("  pip install PyPDF2 --break-system-packages")
    exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def generate_recipe_id(title: str) -> str:
    """Generate a URL-safe ID from recipe title."""
    # Convert to lowercase, replace special chars with hyphens
    recipe_id = re.sub(r'[^\w\s-]', '', title.lower())
    recipe_id = re.sub(r'[-\s]+', '-', recipe_id)
    return recipe_id.strip('-')


def parse_title_and_metadata(text: str) -> Dict[str, Any]:
    """Extract recipe title, cook time, and servings."""
    lines = text.split('\n')
    
    # Find the title (usually the first substantial line)
    title = None
    cook_time = None
    servings = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Title is usually before the time/servings line
        if not title and len(line) > 20 and not line.startswith('Find cookware'):
            # Check if next line has time/servings
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if 'minutes' in next_line and 'servings' in next_line:
                    title = line
                    # Parse time and servings from next line
                    time_match = re.search(r'(\d+)\s*minutes', next_line)
                    servings_match = re.search(r'(\d+)\s*servings?', next_line)
                    if time_match:
                        cook_time = f"{time_match.group(1)} minutes"
                    if servings_match:
                        servings = int(servings_match.group(1))
                    break
    
    return {
        'title': title or 'Unknown Recipe',
        'cookTime': cook_time or '30 minutes',
        'servings': servings or 2
    }


def parse_cookware(text: str) -> List[str]:
    """Extract cookware list from 'Find cookware' section."""
    cookware = []
    
    # Find the cookware section
    cookware_match = re.search(r'Find cookware\n(.*?)\nGrab ingredients', text, re.DOTALL)
    if not cookware_match:
        return cookware
    
    cookware_text = cookware_match.group(1)
    
    # Split by newlines and clean up
    items = cookware_text.split('\n')
    for item in items:
        item = item.strip()
        if item and not item.startswith('Find') and len(item) > 2:
            # Remove optional markers
            item = re.sub(r'\s*\(optional\)', '', item)
            cookware.append(item)
    
    return cookware


def parse_ingredients(text: str) -> List[Dict[str, str]]:
    """Extract ingredients from 'Grab ingredients' section."""
    ingredients = []
    
    # Find the ingredients section
    ingredients_match = re.search(r'Grab ingredients\n(.*?)\n(?:Cook & enjoy|$)', text, re.DOTALL)
    if not ingredients_match:
        return ingredients
    
    ingredients_text = ingredients_match.group(1)
    
    # Split by newlines
    lines = ingredients_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and section headers
        if not line or line.startswith('Grab') or len(line) < 3:
            continue
        
        # Categorize ingredient (simple heuristic)
        category = categorize_ingredient(line)
        
        # Parse quantity and name
        # Common patterns: "1 cup flour", "2 medium carrots", "1 (15 oz) can beans"
        quantity_match = re.match(r'^([\d\/\.\s]+(?:\([^)]+\))?\s*(?:cup|tbsp|tsp|oz|lb|fl oz|pkg|can|bunch|stick|clove|medium|small|large)?s?)\s+(.+)$', line)
        
        if quantity_match:
            quantity = quantity_match.group(1).strip()
            name = quantity_match.group(2).strip()
        else:
            # No quantity detected, treat entire line as ingredient
            quantity = ""
            name = line
        
        ingredients.append({
            'name': name.lower(),
            'quantity': quantity,
            'category': category,
            'original': line
        })
    
    return ingredients


def categorize_ingredient(ingredient: str) -> str:
    """Categorize ingredient based on common patterns."""
    ingredient_lower = ingredient.lower()
    
    # Produce
    if any(word in ingredient_lower for word in ['carrot', 'celery', 'onion', 'garlic', 'tomato', 
                                                   'pepper', 'kale', 'lettuce', 'spinach', 'bean',
                                                   'apple', 'kiwi', 'berry', 'fruit', 'lime', 'lemon']):
        return 'produce'
    
    # Protein
    if any(word in ingredient_lower for word in ['chicken', 'beef', 'pork', 'fish', 'turkey', 
                                                   'salmon', 'tuna', 'shrimp', 'tofu']):
        return 'protein'
    
    # Dairy
    if any(word in ingredient_lower for word in ['milk', 'cheese', 'yogurt', 'butter', 'cream', 
                                                   'cheddar', 'mozzarella', 'parmesan']):
        return 'dairy'
    
    # Spices
    if any(word in ingredient_lower for word in ['salt', 'pepper', 'cumin', 'paprika', 'oregano',
                                                   'basil', 'thyme', 'cinnamon', 'turmeric', 
                                                   'chili powder', 'italian seasoning']):
        return 'spices'
    
    # Default to pantry
    return 'pantry'


def parse_instructions(text: str) -> List[Dict[str, Any]]:
    """Extract cooking instructions from 'Cook & enjoy' section."""
    instructions = []
    
    # Find the instructions section
    instructions_match = re.search(r'Cook & enjoy\n(.*?)(?:\n\d+\sof\s\d+|$)', text, re.DOTALL)
    if not instructions_match:
        return instructions
    
    instructions_text = instructions_match.group(1)
    
    # Split by numbered steps
    # Pattern: line starts with a number (1, 2, 3, etc.)
    lines = instructions_text.split('\n')
    
    current_step = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        # Check if line starts with a step number
        step_match = re.match(r'^(\d+)\s*$', line)
        
        if step_match:
            # Save previous step
            if current_step is not None and current_text:
                instructions.append({
                    'step': current_step,
                    'text': ' '.join(current_text).strip()
                })
            
            # Start new step
            current_step = int(step_match.group(1))
            current_text = []
        else:
            # Add to current step text
            if current_step is not None:
                current_text.append(line)
    
    # Save last step
    if current_step is not None and current_text:
        instructions.append({
            'step': current_step,
            'text': ' '.join(current_text).strip()
        })
    
    return instructions


def parse_recipe_pdf(pdf_path: str) -> Dict[str, Any]:
    """Parse a single Mealime PDF and extract all recipe data."""
    print(f"Processing: {os.path.basename(pdf_path)}")
    
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print(f"  ⚠️  Warning: Could not extract text from {pdf_path}")
        return None
    
    # Extract all components
    metadata = parse_title_and_metadata(text)
    cookware = parse_cookware(text)
    ingredients = parse_ingredients(text)
    instructions = parse_instructions(text)
    
    # Validate we got the essentials
    if not ingredients or not instructions:
        print(f"  ⚠️  Warning: Missing ingredients or instructions in {pdf_path}")
        print(f"     Ingredients: {len(ingredients)}, Instructions: {len(instructions)}")
    
    recipe = {
        'id': generate_recipe_id(metadata['title']),
        'title': metadata['title'],
        'cookTime': metadata['cookTime'],
        'servings': metadata['servings'],
        'cookware': cookware,
        'ingredients': ingredients,
        'instructions': instructions,
        'tags': []  # Can be added manually later
    }
    
    print(f"  ✓ Extracted: {len(ingredients)} ingredients, {len(instructions)} steps")
    
    return recipe


def process_directory(input_dir: str, output_file: str):
    """Process all PDF files in a directory and create JSON output."""
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"ERROR: Input directory '{input_dir}' does not exist")
        return
    
    # Find all PDF files
    pdf_files = list(input_path.glob('*.pdf'))
    
    if not pdf_files:
        print(f"ERROR: No PDF files found in '{input_dir}'")
        return
    
    print(f"\nFound {len(pdf_files)} PDF files")
    print("=" * 60)
    
    recipes = []
    failed = []
    
    for pdf_file in sorted(pdf_files):
        try:
            recipe = parse_recipe_pdf(str(pdf_file))
            if recipe:
                recipes.append(recipe)
            else:
                failed.append(pdf_file.name)
        except Exception as e:
            print(f"  ❌ Error processing {pdf_file.name}: {e}")
            failed.append(pdf_file.name)
    
    # Create output
    output_data = {
        'recipes': recipes,
        'metadata': {
            'total': len(recipes),
            'generated': 'Generated by pdf_to_json.py',
            'source': input_dir
        }
    }
    
    # Write JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✓ Successfully processed: {len(recipes)} recipes")
    if failed:
        print(f"❌ Failed: {len(failed)} recipes")
        for name in failed:
            print(f"   - {name}")
    print(f"\n📄 Output written to: {output_file}")
    print(f"📊 Total file size: {output_path.stat().st_size / 1024:.1f} KB")


def validate_json(json_file: str):
    """Validate the generated JSON file."""
    print(f"\nValidating {json_file}...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        recipes = data.get('recipes', [])
        
        print(f"✓ Valid JSON with {len(recipes)} recipes")
        
        # Check for required fields
        issues = []
        for i, recipe in enumerate(recipes):
            missing = []
            if not recipe.get('title'):
                missing.append('title')
            if not recipe.get('ingredients'):
                missing.append('ingredients')
            if not recipe.get('instructions'):
                missing.append('instructions')
            
            if missing:
                issues.append(f"Recipe {i+1} ({recipe.get('id', 'unknown')}): missing {', '.join(missing)}")
        
        if issues:
            print("\n⚠️  Validation warnings:")
            for issue in issues[:10]:  # Show first 10
                print(f"   - {issue}")
            if len(issues) > 10:
                print(f"   ... and {len(issues) - 10} more")
        else:
            print("✓ All recipes have required fields")
        
        # Statistics
        total_ingredients = sum(len(r.get('ingredients', [])) for r in recipes)
        total_steps = sum(len(r.get('instructions', [])) for r in recipes)
        
        print(f"\nStatistics:")
        print(f"  Total recipes: {len(recipes)}")
        print(f"  Total ingredients: {total_ingredients}")
        print(f"  Total instruction steps: {total_steps}")
        print(f"  Avg ingredients per recipe: {total_ingredients / len(recipes):.1f}")
        print(f"  Avg steps per recipe: {total_steps / len(recipes):.1f}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
    except Exception as e:
        print(f"❌ Error validating: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Mealime PDF recipes to JSON format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all PDFs in a directory
  python pdf_to_json.py --input recipe-pdfs/ --output public/recipes.json
  
  # Convert and validate
  python pdf_to_json.py -i recipe-pdfs/ -o recipes.json --validate
  
  # Validate existing JSON
  python pdf_to_json.py --validate-only recipes.json
        """
    )
    
    parser.add_argument('-i', '--input', 
                        help='Input directory containing PDF files')
    parser.add_argument('-o', '--output', 
                        default='recipes.json',
                        help='Output JSON file (default: recipes.json)')
    parser.add_argument('-v', '--validate', 
                        action='store_true',
                        help='Validate JSON after conversion')
    parser.add_argument('--validate-only', 
                        metavar='FILE',
                        help='Only validate an existing JSON file')
    
    args = parser.parse_args()
    
    # Validate only mode
    if args.validate_only:
        validate_json(args.validate_only)
        return
    
    # Conversion mode
    if not args.input:
        parser.error("--input directory is required (or use --validate-only)")
    
    process_directory(args.input, args.output)
    
    # Validate if requested
    if args.validate:
        validate_json(args.output)


if __name__ == '__main__':
    main()
