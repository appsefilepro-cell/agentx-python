"""
AgentX AI Tools Integrations Configuration

This module provides configuration for integrating various AI tools
with the AgentX SDK. Includes both paid and free alternatives.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ToolCategory(Enum):
    IMAGE_GENERATION = "image_generation"
    RESEARCH = "research"
    PRESENTATION = "presentation"
    AGENTIC_AI = "agentic_ai"
    IMAGE_TO_VIDEO = "image_to_video"
    CODING = "coding"
    WEBSITE = "website"
    VIDEO_GENERATION = "video_generation"


class PricingTier(Enum):
    FREE = "free"
    PAID = "paid"


@dataclass
class AITool:
    name: str
    category: ToolCategory
    pricing: PricingTier
    api_endpoint: Optional[str] = None
    api_docs: Optional[str] = None
    description: Optional[str] = None


# AI Tools Registry - Paid vs Free Alternatives
AI_TOOLS_REGISTRY: Dict[ToolCategory, Dict[PricingTier, AITool]] = {
    ToolCategory.IMAGE_GENERATION: {
        PricingTier.PAID: AITool(
            name="MidJourney",
            category=ToolCategory.IMAGE_GENERATION,
            pricing=PricingTier.PAID,
            api_docs="https://docs.midjourney.com/",
            description="Advanced AI image generation with artistic styles"
        ),
        PricingTier.FREE: AITool(
            name="Nano Banana Pro",
            category=ToolCategory.IMAGE_GENERATION,
            pricing=PricingTier.FREE,
            description="Free AI image generation alternative"
        ),
    },
    ToolCategory.RESEARCH: {
        PricingTier.PAID: AITool(
            name="ChatGPT",
            category=ToolCategory.RESEARCH,
            pricing=PricingTier.PAID,
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_docs="https://platform.openai.com/docs/api-reference",
            description="OpenAI's conversational AI for research and analysis"
        ),
        PricingTier.FREE: AITool(
            name="Perplexity",
            category=ToolCategory.RESEARCH,
            pricing=PricingTier.FREE,
            api_endpoint="https://api.perplexity.ai/chat/completions",
            api_docs="https://docs.perplexity.ai/",
            description="AI-powered research assistant with citations"
        ),
    },
    ToolCategory.PRESENTATION: {
        PricingTier.PAID: AITool(
            name="Beautiful AI",
            category=ToolCategory.PRESENTATION,
            pricing=PricingTier.PAID,
            api_docs="https://www.beautiful.ai/",
            description="AI-powered presentation design tool"
        ),
        PricingTier.FREE: AITool(
            name="Gamma",
            category=ToolCategory.PRESENTATION,
            pricing=PricingTier.FREE,
            api_docs="https://gamma.app/",
            description="Free AI presentation and document creator"
        ),
    },
    ToolCategory.AGENTIC_AI: {
        PricingTier.PAID: AITool(
            name="Manus",
            category=ToolCategory.AGENTIC_AI,
            pricing=PricingTier.PAID,
            description="Advanced agentic AI platform"
        ),
        PricingTier.FREE: AITool(
            name="Genspark",
            category=ToolCategory.AGENTIC_AI,
            pricing=PricingTier.FREE,
            api_docs="https://www.genspark.ai/",
            description="Free AI agent platform"
        ),
    },
    ToolCategory.IMAGE_TO_VIDEO: {
        PricingTier.PAID: AITool(
            name="Kling AI",
            category=ToolCategory.IMAGE_TO_VIDEO,
            pricing=PricingTier.PAID,
            description="AI-powered image to video conversion"
        ),
        PricingTier.FREE: AITool(
            name="Grok AI",
            category=ToolCategory.IMAGE_TO_VIDEO,
            pricing=PricingTier.FREE,
            api_endpoint="https://api.x.ai/v1/chat/completions",
            api_docs="https://docs.x.ai/",
            description="xAI's free multimodal AI assistant"
        ),
    },
    ToolCategory.CODING: {
        PricingTier.PAID: AITool(
            name="Cursor",
            category=ToolCategory.CODING,
            pricing=PricingTier.PAID,
            api_docs="https://cursor.sh/",
            description="AI-first code editor"
        ),
        PricingTier.FREE: AITool(
            name="Trae AI",
            category=ToolCategory.CODING,
            pricing=PricingTier.FREE,
            api_docs="https://www.trae.ai/",
            description="Free AI coding assistant"
        ),
    },
    ToolCategory.WEBSITE: {
        PricingTier.PAID: AITool(
            name="Lovable",
            category=ToolCategory.WEBSITE,
            pricing=PricingTier.PAID,
            api_docs="https://lovable.dev/",
            description="AI-powered website builder"
        ),
        PricingTier.FREE: AITool(
            name="Google AI Studio",
            category=ToolCategory.WEBSITE,
            pricing=PricingTier.FREE,
            api_endpoint="https://generativelanguage.googleapis.com/v1beta/",
            api_docs="https://ai.google.dev/",
            description="Google's free AI development platform"
        ),
    },
    ToolCategory.VIDEO_GENERATION: {
        PricingTier.PAID: AITool(
            name="Google Veo3",
            category=ToolCategory.VIDEO_GENERATION,
            pricing=PricingTier.PAID,
            api_docs="https://deepmind.google/technologies/veo/",
            description="Google's advanced video generation model"
        ),
        PricingTier.FREE: AITool(
            name="Sora 2",
            category=ToolCategory.VIDEO_GENERATION,
            pricing=PricingTier.FREE,
            api_docs="https://openai.com/sora",
            description="OpenAI's video generation model"
        ),
    },
}


def get_tool(category: ToolCategory, pricing: PricingTier) -> Optional[AITool]:
    """Get a specific AI tool by category and pricing tier."""
    return AI_TOOLS_REGISTRY.get(category, {}).get(pricing)


def get_free_alternative(category: ToolCategory) -> Optional[AITool]:
    """Get the free alternative for a given category."""
    return get_tool(category, PricingTier.FREE)


def get_all_free_tools() -> List[AITool]:
    """Get all free AI tools."""
    return [
        tools[PricingTier.FREE]
        for tools in AI_TOOLS_REGISTRY.values()
        if PricingTier.FREE in tools
    ]


def get_all_tools() -> List[AITool]:
    """Get all registered AI tools."""
    all_tools = []
    for tools in AI_TOOLS_REGISTRY.values():
        all_tools.extend(tools.values())
    return all_tools


def list_categories() -> List[str]:
    """List all available tool categories."""
    return [cat.value for cat in ToolCategory]


# Integration helper for AgentX
class IntegrationManager:
    """Manager for AI tool integrations with AgentX."""

    def __init__(self):
        self.active_integrations: Dict[ToolCategory, AITool] = {}

    def activate(self, category: ToolCategory, prefer_free: bool = True) -> AITool:
        """Activate an integration for a category."""
        pricing = PricingTier.FREE if prefer_free else PricingTier.PAID
        tool = get_tool(category, pricing)
        if tool:
            self.active_integrations[category] = tool
        return tool

    def activate_all_free(self) -> Dict[ToolCategory, AITool]:
        """Activate all free tool integrations."""
        for category in ToolCategory:
            self.activate(category, prefer_free=True)
        return self.active_integrations

    def get_active(self, category: ToolCategory) -> Optional[AITool]:
        """Get the active integration for a category."""
        return self.active_integrations.get(category)

    def list_active(self) -> Dict[str, str]:
        """List all active integrations."""
        return {
            cat.value: tool.name
            for cat, tool in self.active_integrations.items()
        }
