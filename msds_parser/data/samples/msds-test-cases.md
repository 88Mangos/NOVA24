# Test Cases for MSDS Parser

## test_case_1_simple.txt
```
MATERIAL SAFETY DATA SHEET - ETHANOL

SECTION 1: IDENTIFICATION
Chemical Name: Ethanol
CAS Number: 64-17-5

SECTION 2: HAZARDS IDENTIFICATION
Signal Word: DANGER
Hazard Statements:
- Highly flammable liquid and vapor
- Causes eye irritation

SECTION 4: FIRST AID MEASURES
Eye Contact: Rinse with water for 15 minutes
Skin Contact: Wash with soap and water
```

## test_case_2_missing_data.txt
```
MATERIAL SAFETY DATA SHEET - METHANOL

SECTION 1: IDENTIFICATION
Chemical Name: Methanol

SECTION 2: HAZARDS IDENTIFICATION
Signal Word: DANGER

SECTION 4: FIRST AID MEASURES
Eye Contact: Rinse with water
```

## test_case_3_complex.txt
```
MATERIAL SAFETY DATA SHEET - SULFURIC ACID

SECTION 1: IDENTIFICATION
Chemical Name: Sulfuric Acid
Synonyms: Oil of Vitriol, Battery Acid
CAS Number: 7664-93-9

SECTION 2: HAZARDS IDENTIFICATION
Signal Word: DANGER
GHS Classification:
- Skin Corrosion (Category 1A)
- Serious Eye Damage (Category 1)
- Corrosive to Metals (Category 1)

Multiple Hazard Statements:
- Causes severe skin burns and eye damage
- May be corrosive to metals
- Harmful if inhaled

SECTION 4: FIRST AID MEASURES
Complex procedures:
Eye Contact: Rinse cautiously with water for at least 30 minutes. Remove contact lenses if present and easy to do. Continue rinsing.
Skin Contact: 
1. Remove contaminated clothing immediately
2. Rinse skin with water/shower
3. Seek immediate medical attention
```

## test_case_4_formatting.txt
```
MATERIAL   SAFETY    DATA    SHEET    -    ACETONE
  
SECTION      1:        IDENTIFICATION
Chemical    Name:     Acetone
CAS         Number:   67-64-1

SECTION 2: HAZARDS
Signal Word:DANGER
Hazards:Flammable,Irritant
```
