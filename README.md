# Shanee-Intelligence Omniverse OS

## What is This?

Shanee-Intelligence is a personal intelligence system designed to research, analyze, and catalog products, practices, and choices to support informed decision-making. It's an "Omniverse OS" - an operating system for your knowledge and choices.

Rather than relying on marketing, brand loyalty, or incomplete information, Shanee-Intelligence provides comprehensive, evidence-based analysis across multiple dimensions:

- **Health & Safety** - What are the real health impacts?
- **Environmental Impact** - What's the ecological cost?
- **Effectiveness** - Does it actually work as advertised?
- **Cost & Value** - Is it worth the money?

## How It Works

Each product or topic is evaluated with:

1. **Comprehensive research** - Academic studies, governmental guidance, consumer evidence
2. **Multi-dimensional scoring** - Rating across health, environment, effectiveness, and value
3. **Transparent methodology** - All sources cited, scoring rationale explained
4. **Practical guidance** - "When to use" vs "when to avoid" decision matrices
5. **Alternative solutions** - Better options you might not know about

## Current Analysis

### Febreze Aerosol Spray
**Overall Score: 4.35/10** - Below average when weighing all factors

A convenient quick-fix for odor masking that poses health and environmental concerns, with far cheaper and safer alternatives available for regular use.

**Key Findings:**
- ✅ **Pros**: Convenient, effective odor masking, quick results
- ❌ **Cons**: Masks rather than eliminates odors, VOC emissions, endocrine disruptors, poor cost-value
- 🏥 **Health Risk**: Respiratory irritation, inhalation hazards, fragrance sensitivities
- 🌍 **Environmental**: VOC emissions, persistent aluminum packaging, aquatic toxicity

**Recommendation**: Use sparingly for emergencies only. Switch to baking soda (~$0.01/use), charcoal, or ventilation for regular odor control.

**See**: `/data/products/febreze-aerosol.json` for complete analysis

## Repository Structure

```
Shanee-Intelligence/
├── README.md                    # This file
├── data/
│   ├── schema.json             # Data structure definition
│   ├── README.md               # Data documentation
│   └── products/
│       ├── febreze-aerosol.json    # Product analysis examples
│       └── [more products...]
```

## Adding Your Own Analysis

To research and add a new product:

1. Navigate to `/data/products/`
2. Create a new JSON file following the schema
3. Research thoroughly across all dimensions
4. Score based on evidence
5. Include sources and alternatives
6. Commit with clear documentation

See `/data/README.md` for detailed instructions.

## Philosophy

This system is built on the belief that:

- **Marketing is incomplete** - Companies don't tell you about health risks or environmental costs
- **Individual choice matters** - Small decisions accumulate; informed choices multiply impact
- **Evidence exists** - Research, data, and knowledge are available if you know where to look
- **Transparency builds trust** - Show your work, cite sources, explain methodology
- **Alternatives exist** - There's almost always a better option if you look

## Future Expansion

Planned product categories:
- Household products (cleaning, air freshening, personal care)
- Food & nutrition (common foods, dietary products)
- Technology & devices (electronics, appliances)
- Services & subscriptions
- Practices & habits (behaviors, routines)

## Contributing

Have a product you'd like analyzed? Research you think should be included? Edge cases or disagreements with the analysis?

This is a living system. As your knowledge grows and new evidence emerges, the database should evolve.

---

**Last Updated**: 2026-05-29
**Current Products**: 1
**Overall Recommendation**: Check `/data/products/` for detailed analyses