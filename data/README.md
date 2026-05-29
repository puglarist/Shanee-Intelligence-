# Shanee Intelligence - Product Analysis Database

## Overview

This directory contains comprehensive product analysis data for the Shanee-Intelligence Omniverse OS. Each product entry provides a deep, evidence-based evaluation to support informed decision-making.

## Data Structure

Each product is stored as a JSON file following the schema defined in `schema.json`. Products are evaluated across multiple dimensions:

### Evaluation Dimensions

1. **Health & Safety** (35% weight in overall score)
   - Inhalation/contact risks
   - Chemical composition concerns
   - Effects on vulnerable populations
   - Long-term health implications

2. **Environmental Impact** (30% weight)
   - Manufacturing footprint
   - Packaging sustainability
   - Pollutant emissions
   - Persistence in ecosystems

3. **Effectiveness** (20% weight)
   - Does it work as advertised?
   - Duration of effect
   - Comparison to alternatives
   - Root-cause vs. temporary solutions

4. **Cost/Value** (15% weight)
   - Price per use
   - Comparison to alternatives
   - Long-term cost-effectiveness
   - Value for money

### Scoring System

- **Scale**: 1-10 for each dimension
  - 1 = Poor (dangerous, ineffective, expensive, harmful)
  - 5 = Neutral (acceptable but unremarkable)
  - 10 = Excellent (safe, effective, affordable, beneficial)

- **Overall Score**: Weighted calculation
  ```
  Overall = (Health×0.35) + (Environment×0.30) + (Effectiveness×0.20) + (Value×0.15)
  ```

### Data File Format

```json
{
  "metadata": { /* Basic info: title, manufacturer, date added */ },
  "overview": { /* What the product is and typical uses */ },
  "analysis": {
    "pros": [ /* Advantages with importance ratings */ ],
    "cons": [ /* Disadvantages with severity ratings */ ],
    "healthSafety": [ /* Health concerns with evidence */ ],
    "environmental": [ /* Environmental impacts with severity */ ],
    "effectiveness": { /* How well it works */ },
    "costValue": { /* Price and value analysis */ }
  },
  "scoring": {
    "health": 1-10,
    "environment": 1-10,
    "effectiveness": 1-10,
    "value": 1-10,
    "overall": 1-10,
    "weights": { /* Weighting rationale */ }
  },
  "sources": [ /* Academic, governmental, consumer sources */ ],
  "researchNotes": [ /* Additional findings and nuances */ ],
  "alternatives": [ /* Better options to consider */ ],
  "decisionMatrix": { /* When to use, when to avoid */ }
}
```

## Current Products

### Febreze Aerosol Spray
- **File**: `febreze-aerosol.json`
- **Overall Score**: 4.35/10
- **Key Finding**: Effective quick-fix for odor masking but poses health and environmental concerns; far cheaper alternatives available
- **Recommendation**: Use sparingly for emergency situations; switch to baking soda or charcoal for regular use

## Adding New Products

To add a new product analysis:

1. **Research Phase**
   - Gather information on health effects, environmental impact, effectiveness
   - Find scientific evidence, governmental guidance, consumer reviews
   - Identify alternatives and root causes

2. **Create JSON File**
   - Copy the structure from `febreze-aerosol.json`
   - Follow the schema in `schema.json`
   - Populate all sections with evidence-based information

3. **Calculate Scores**
   - Rate each dimension (1-10)
   - Calculate overall score using the weighted formula
   - Include rationale for each score

4. **Validate & Review**
   - Ensure JSON is syntactically correct (use jsonlint or similar)
   - Verify all claims have sources
   - Check that scoring aligns with analysis
   - Review for balance and objectivity

5. **Commit & Document**
   - Commit with clear message describing the product
   - Update this README with new product entry

## Using This Data

### For Analysis
```bash
# Validate JSON syntax
cat data/products/febreze-aerosol.json | python -m json.tool > /dev/null

# Extract scoring
cat data/products/febreze-aerosol.json | jq '.scoring'

# Find all health concerns
cat data/products/febreze-aerosol.json | jq '.analysis.healthSafety'
```

### For Decision-Making
1. Review the **summary** section for quick overview
2. Check the **decisionMatrix** for when to use vs. avoid
3. Examine **alternatives** for better options
4. Read detailed **analysis** for evidence-based reasoning

## Philosophy

This database is built on the principle that informed decisions require:

- **Evidence-based analysis** - Claims backed by research, not marketing
- **Holistic evaluation** - Considering health, environment, effectiveness, and cost together
- **Transparency** - Clear sourcing and methodology
- **Practical guidance** - "When to use" and "when to avoid" recommendations
- **Continuous improvement** - Updating as new evidence emerges

## Notes

- Scores are snapshot evaluations based on available information
- Products and formulations change; entries should be updated annually
- Individual circumstances vary; recommendations are general guidance
- Always consult health professionals for personal health decisions
