#!/bin/bash
# Customize bc-ai-wp template for kriskrug.co

echo "🔧 Customizing repository for kriskrug.co..."

# Find and replace bc-ai → kk (code prefix)
find . -type f \( -name "*.md" -o -name "*.php" -o -name "*.js" -o -name "*.css" -o -name "*.yml" -o -name "*.yaml" \) -not -path "./.git/*" -exec sed -i '' 's/bc_ai_/kk_/g' {} +
find . -type f \( -name "*.md" -o -name "*.php" -o -name "*.js" -o -name "*.css" -o -name "*.yml" -o -name "*.yaml" \) -not -path "./.git/*" -exec sed -i '' 's/BC_AI_/KK_/g' {} +
find . -type f \( -name "*.md" -o -name "*.php" -o -name "*.js" -o -name "*.css" -o -name "*.yml" -o -name "*.yaml" \) -not -path "./.git/*" -exec sed -i '' 's/bc-ai/kk/g' {} +

# Replace BC+AI with Kris Krug
find . -type f \( -name "*.md" -o -name "*.php" \) -not -path "./.git/*" -exec sed -i '' 's/BC+AI/Kris Krug/g' {} +
find . -type f \( -name "*.md" -o -name "*.php" \) -not -path "./.git/*" -exec sed -i '' 's/BC\+AI/Kris Krug/g' {} +

# Replace URLs
find . -type f \( -name "*.md" -o -name "*.php" -o -name "*.yml" \) -not -path "./.git/*" -exec sed -i '' 's/bc-ai\.ca/kriskrug.co/g' {} +
find . -type f \( -name "*.md" -o -name "*.php" -o -name "*.yml" \) -not -path "./.git/*" -exec sed -i '' 's|https://bc-ai\.ca|https://kriskrug.co|g' {} +

# Replace repository references
find . -type f -name "*.md" -not -path "./.git/*" -exec sed -i '' 's/WalksWithASwagger\/bc-ai-wp/WalksWithASwagger\/kriskrug-wp/g' {} +

echo "✓ Find/replace complete!"
echo ""
echo "Next: Update these files manually with Kris Krug specific content:"
echo "  - .claude/context/project-context.md"
echo "  - .claude/agents-vibe.md"
echo "  - docs/vision.md"
echo "  - docs/roadmap.md"
