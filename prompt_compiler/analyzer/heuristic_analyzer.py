from __future__ import annotations

from prompt_compiler.compiler.contracts import Analyzer
from prompt_compiler.models.prompt_models import Intent, IntentCategory, Prompt, PromptAnalysis, PromptScore, Technique, TechniqueKind


class HeuristicAnalyzer(Analyzer):
    """A deterministic analyzer that infers intent and simple prompt quality signals."""

    def analyze(self, prompt: Prompt) -> PromptAnalysis:
        """Analyze a prompt using simple heuristics based on its content."""
        lowered = prompt.content.lower()
        intent = self._infer_intent(lowered)
        techniques = self._detect_techniques(lowered)
        score = self._score_prompt(lowered)

        summary = self._build_summary(intent, techniques)
        concerns = self._find_concerns(lowered)

        return PromptAnalysis(
            prompt=prompt,
            intent=intent,
            detected_techniques=techniques,
            score=score,
            summary=summary,
            concerns=concerns,
        )

    def _infer_intent(self, text: str) -> Intent:
        if any(keyword in text for keyword in ("summarize", "summary", "tl;dr")):
            category = IntentCategory.SUMMARIZATION
            explanation = "The prompt asks for a concise summary."
        elif any(keyword in text for keyword in ("classify", "category", "label")):
            category = IntentCategory.CLASSIFICATION
            explanation = "The prompt asks for classification or labeling."
        elif any(keyword in text for keyword in ("write", "draft", "generate", "create")):
            category = IntentCategory.GENERATION
            explanation = "The prompt requests content generation."
        elif any(keyword in text for keyword in ("extract", "find", "identify")):
            category = IntentCategory.EXTRACTION
            explanation = "The prompt requests extraction of specific information."
        else:
            category = IntentCategory.GENERATION
            explanation = "The prompt does not clearly match a specialized intent category."

        return Intent(category=category, confidence=0.8, explanation=explanation)

    def _detect_techniques(self, text: str) -> list[Technique]:
        techniques: list[Technique] = []
        if "example" in text or "examples" in text:
            techniques.append(Technique(kind=TechniqueKind.FEW_SHOT, confidence=0.75, rationale="Example-based prompting was detected."))
        if "think" in text or "reason" in text:
            techniques.append(Technique(kind=TechniqueKind.CHAIN_OF_THOUGHT, confidence=0.7, rationale="The prompt asks for reasoning steps."))
        if "act as" in text or "role" in text:
            techniques.append(Technique(kind=TechniqueKind.ROLE_PROMPTING, confidence=0.8, rationale="Role prompting was detected."))
        return techniques

    def _score_prompt(self, text: str) -> PromptScore:
        clarity = 0.8 if len(text.split()) >= 4 else 0.6
        specificity = 0.75 if any(token in text for token in ("specific", "detailed", "exactly", "clearly")) else 0.5
        completeness = 0.7 if any(token in text for token in ("context", "format", "tone", "audience")) else 0.45
        overall = (clarity + specificity + completeness) / 3
        return PromptScore(clarity=clarity, specificity=specificity, completeness=completeness, overall=overall)

    def _build_summary(self, intent: Intent, techniques: list[Technique]) -> str:
        technique_names = ", ".join(tech.kind.value for tech in techniques) if techniques else "none"
        return f"Intent: {intent.category.value}; techniques: {technique_names}"

    def _find_concerns(self, text: str) -> list[str]:
        concerns: list[str] = []
        if "?" not in text:
            concerns.append("The prompt does not contain a question or explicit request.")
        if len(text.split()) < 5:
            concerns.append("The prompt is very short and may lack required context.")
        return concerns
