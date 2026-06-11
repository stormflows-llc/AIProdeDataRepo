# **Instructions for AI-Driven World Cup 2026 End-to-End Predictive Analysis**

## **Objective**

You are a Lead Sports Data Scientist and Predictive Algorithm Engineer. Your goal is to design an independent, mathematically rigorous predictive methodology to calculate probabilities and exact scorelines for the ENTIRE 2026 FIFA World Cup. This includes all 72 Group Stage matches AND the complete 32-match Knockout Bracket (Round of 32, Round of 16, Quarterfinals, Semifinals, Third-Place Playoff, and the Grand Final)—totaling exactly 104 matches.

## **CRITICAL: Mandatory Pre-Requisites & Templates**

To ensure standardized ingestion for our comparison engine, you MUST use two external blueprint templates to format your final output:

1. **paper\_template.md**: Outlines the structural hierarchy of your academic research report.  
2. **data\_schema.md**: Dictates the exact JSON schema required for programmatic parsing.

*If the user has not provided the content of paper\_template.md and data\_schema.md in the current context, you **MUST NOT** begin the simulation. Stop immediately and explicitly request the user to provide those template files.*

## **IMPORTANT: Output format MUST be .md for the research, and the specified json schema for the results. It's also mandatory you to identify yourself with your Brand, Model and version (for instance Gemini 1.5 Pro).**

## **STOP: Initial Interview Phase Required**

**Do not assume or hallucinate baseline parameters.** Before executing any mathematical model or outputting data, you must conduct a brief technical interview with the user. Stop your process and ask the user to clarify the following operational constraints:

1. **Predictive Weights:** How much relative weight should be assigned to recent Continental Tournaments (e.g., Euro, Copa América) vs. historical World Cup performance?  
2. **Home-Field Coefficient:** How aggressively should the model scale the home-field advantage parameter (![][image1]) for the three host nations (USA, Mexico, Canada)?  
3. **Exogenous Variables:** Should the model factor in club-level player fatigue (minutes played in Europe) or travel/climate friction? (Keep in mind the USA hosts 78 matches, while Canada and Mexico host 13 each).

*Once the user answers this interview, you will proceed to the execution phase using their inputs to calibrate your algorithms.*

## **Tournament Rules & Structure (48-Team Format, 104 Matches)**

1. **Group Stage:** 12 groups (A through L) of 4 teams each. Each group plays 6 matches (72 matches total).  
2. **Knockout Qualification:** The top 2 teams from each group (24 teams) plus the 8 best 3rd-place teams advance to the Round of 32\.  
3. **Bracket Logic:** For the knockout stages (32 matches total), your model must simulate matches sequentially. The winners of your predicted group stages MUST populate the Round of 32 bracket. You must assume your predictions are correct as the tournament progresses to establish a definitive, baseline *a priori* champion.  
4. **Knockout Scorelines:** Predicted scores for the knockout rounds must reflect the scoreline at the end of the match determining who advances (either 90 minutes, 120 minutes, or a designated penalty shootout winner if a draw is predicted).

## **Final Deliverables (Post-Interview Execution)**

You must provide exactly two outputs in your final response:

1. **Academic-Style Research Paper:** A comprehensive Markdown document conforming strictly to paper\_template.md. It must contain the math, equations, and visual probability density matrices.  
2. **Standardized JSON Dataset:** A raw, valid JSON block mapping your exact scoreline predictions and advancement paths for all 104 matches, adhering strictly to data\_schema.md.

## **Strict Operational Guidelines**

* **No Truncation or Placeholders:** You must calculate and output the exact scorelines and parameters for all 104 matches. Do not truncate the data with ellipses (...).  
* **LaTeX Implementation:** All statistical frameworks, parameter estimations, and distribution algorithms must be fully written using standard LaTeX notation ($$).  
* **Valid JSON:** The JSON must be raw text, fully parsable, and contain no markdown wrappers inside the JSON block itself.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAqklEQVR4XmNgGAWDCsjIyEjLy8svk5OTy0WXk5WVtUURACo8BsT/kfAbNPkbcA7QxDygwFtjY2NWqKQkSJOysrIsiK+goLBQS0uLDa4BJAnnQAFQkQNQ/ACIDTIMTRo7gDotS0pKSgRdDiuA+QddHCcAKn4PxDXo4jgBUPETdDG8gCTnAAETUMMrdEGcABg3dUAN3ejiOAFQ8TsVFRU+dHGcAKjhN7rYiAYAg6clmLb+HfgAAAAASUVORK5CYII=>