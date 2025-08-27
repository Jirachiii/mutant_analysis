# Beginner's Guide to Labeling Software Mutants

## What are Software Mutants?

Software mutants are slightly modified versions of your original program, created by making small, intentional changes (mutations) to the source code. These are used in **mutation testing** to evaluate how good your test suite is at detecting bugs.

## Types of Mutants You Need to Label

### 1. Equivalent Mutants 🟰

**Definition:** A mutant that behaves identically to the original program for ALL possible inputs.

**Key Characteristics:**
- Produces the same output as the original program
- Cannot be detected by any test case, no matter how comprehensive
- Represents changes that don't affect program behavior

**How to Identify:**
- Look for changes that are mathematically or logically equivalent
- Check if the mutation affects unreachable code

**Common Examples:**
```java
// Original
if (0) return true;

// Equivalent mutant (the change takes place in unreachable code)
if (0) return false;
```

```python
# Original
result = x + 0

# Equivalent mutant
result = x - 0
```

**Labeling Decision:** Mark as **EQUIVALENT** if the mutant behavior cannot be distinguished from the original program.


### 2. Natural Mutants ✅

**Definition:** Mutants that represent realistic bugs and can potentially be detected by good test cases.

**Key Characteristics:**
- Behave differently from the original program for some inputs
- Represent common programming mistakes
- Can be "killed" (detected) by well-designed test cases

**How to Identify:**
- The mutant produces different output for at least some input
- The change represents a plausible programmer error

**Common Examples:**
```java
// Original
if (x < 10) { ... }

// Natural mutant (boundary condition error)
if (x <= 10) { ... }
```

```python
# Original
for i in range(len(array)):

# Unnatural mutant (variable name that a developer would not set)
for isskalajdha in range(len(array) - 1):
```

**Labeling Decision:** Mark as **NATURAL** if the mutant reflects changes a developer can realistically make.

## Step-by-Step Labeling Process

### Step 1: Setup
1. Install the repo and dependencies
```bash
    git clone https://github.com/Jirachiii/mutant_analysis.git
    pip install requests
```
2. You'll be provided an input file(for example, ```test_sampled_mutants.json```). Save it inside the installed repository
3. Change the ```filename``` variable at line 134 of ```object_browser.py``` to the name of the input file
4. Run the labeling program
```bash
    cd mutant_analysis
    python object_browser.py
```

### Step 2: Analyse the mutants
1. A diff between the original program and the mutant program is displayed. Examine the diff to see what specific change was made to the original program
For example:
```
    def check_even_number(number: int) -> Bool:
        if number % 2 == 0:
-            return True
+            return number % 2
        else:
            return False
```
2. Understand the change: In this example, when number is even, the original code returns True, while the mutant returns 0 (which is ```number % 2``` for even numbers)
3. Consider the impact of the change - Could this change affect program behavior? Is this change something you would see in a real-life program?
4. Answer two questions:
- Equivalent? Does it behave the same for ALL inputs? (1 = yes, 0 = no)
- Natural? Is this a realistic developer mistake? (1 = yes, 0 = no)

### Step 3: Use Additional Information when Uncertain
1. Below each mutant ID, you'll find a commit URL
2. Open the URL to view the original code context on GitHub
3. Use GitHub's "Search within code" to locate the relevant file
4. Use "View file" to see the complete file for better context

### Step 4: Return result file
All labeled data will be saved in the file ```label_{input_filename}.json```. Use this file to turn in your label results.
