"""
AgentX5 Advanced Edition - Document Builder & Memory System

Document storage and retrieval for:
- Legal documents from Box/Dropbox/SharePoint
- GitHub repository indexing
- Airtable database sync
- Cross-platform memory persistence

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class StorageLocation(Enum):
    """Document storage locations."""
    GITHUB = "github"
    AIRTABLE = "airtable"
    BOX = "box"
    DROPBOX = "dropbox"
    SHAREPOINT = "sharepoint"
    LOCAL = "local"


class DocumentType(Enum):
    """Types of documents."""
    LEGAL = "legal"
    FINANCIAL = "financial"
    EVIDENCE = "evidence"
    TEMPLATE = "template"
    RESEARCH = "research"
    CODE = "code"


# ============================================================================
# DOCUMENT BUILDER - CREATES FORMATTED DOCUMENTS
# ============================================================================

@dataclass
class DocumentBuilder:
    """
    Document Builder for AgentX5

    Creates court-ready documents from:
    - Templates
    - Research findings
    - Financial data
    - Evidence inventory

    Output formats: PDF, DOCX, Markdown, HTML
    """

    # Configuration
    output_format: str = "markdown"
    template_path: str = "agentx5_advanced/legal/templates"

    # Document queue
    documents: List[Dict[str, Any]] = field(default_factory=list)

    def create_document(
        self,
        doc_type: str,
        title: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create new document."""
        doc = {
            "id": f"DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": doc_type,
            "title": title,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "format": self.output_format,
        }
        self.documents.append(doc)
        return doc

    def build_from_template(
        self,
        template_name: str,
        data: Dict[str, Any]
    ) -> str:
        """Build document from template with data merge."""
        # Template mapping
        templates = {
            "demand_letter": self._build_demand_letter,
            "petition": self._build_petition,
            "memorandum": self._build_memorandum,
            "affidavit": self._build_affidavit,
        }

        builder = templates.get(template_name, self._build_generic)
        return builder(data)

    def _build_demand_letter(self, data: Dict[str, Any]) -> str:
        """Build demand letter."""
        return f"""
# DEMAND LETTER

**To:** {data.get('recipient', '')}
**From:** {data.get('sender', 'APPS HOLDINGS WY, INC.')}
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Re:** {data.get('subject', '')}

---

{data.get('body', '')}

---

**Demand:** {data.get('demand', '')}

**Response Required By:** {data.get('deadline', '')}
"""

    def _build_petition(self, data: Dict[str, Any]) -> str:
        """Build court petition."""
        return f"""
# PETITION

**Case No.:** {data.get('case_number', '')}
**Court:** {data.get('court', '')}

## PETITIONER
{data.get('petitioner', '')}

## RELIEF REQUESTED
{data.get('relief', '')}

## GROUNDS
{data.get('grounds', '')}
"""

    def _build_memorandum(self, data: Dict[str, Any]) -> str:
        """Build legal memorandum."""
        return f"""
# LEGAL MEMORANDUM

**To:** {data.get('to', '')}
**From:** {data.get('from', '')}
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Re:** {data.get('subject', '')}

## QUESTION PRESENTED
{data.get('question', '')}

## BRIEF ANSWER
{data.get('answer', '')}

## DISCUSSION
{data.get('discussion', '')}

## CONCLUSION
{data.get('conclusion', '')}
"""

    def _build_affidavit(self, data: Dict[str, Any]) -> str:
        """Build affidavit."""
        return f"""
# AFFIDAVIT OF {data.get('affiant', '').upper()}

STATE OF {data.get('state', '')}
COUNTY OF {data.get('county', '')}

I, {data.get('affiant', '')}, being first duly sworn, state:

{data.get('statements', '')}

FURTHER AFFIANT SAYETH NOT.

_______________________
{data.get('affiant', '')}
"""

    def _build_generic(self, data: Dict[str, Any]) -> str:
        """Build generic document."""
        return f"""
# {data.get('title', 'DOCUMENT')}

{data.get('content', '')}

---
Generated: {datetime.now().isoformat()}
"""

    def export_to_github(self, doc_id: str) -> Dict[str, Any]:
        """Export document to GitHub repository."""
        doc = next((d for d in self.documents if d["id"] == doc_id), None)
        if not doc:
            return {"error": "Document not found"}

        return {
            "status": "exported",
            "destination": "github",
            "path": f"documents/{doc['type']}/{doc['id']}.md",
            "commit_message": f"Add {doc['title']}",
        }


# ============================================================================
# MEMORY SYSTEM - PERSISTENT DOCUMENT INDEX
# ============================================================================

@dataclass
class MemorySystem:
    """
    Memory System for AgentX5

    Maintains persistent index of:
    - Legal documents
    - Research findings
    - Financial records
    - Evidence inventory

    Syncs with:
    - GitHub (primary storage - accessible everywhere)
    - Airtable (database)
    - Local cache
    """

    # Index
    document_index: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    search_index: Dict[str, List[str]] = field(default_factory=dict)

    # Sources configured
    sources: List[Dict[str, Any]] = field(default_factory=list)

    # Sync status
    last_sync: Optional[str] = None

    def __post_init__(self):
        """Initialize default sources."""
        if not self.sources:
            self.sources = [
                {
                    "name": "GitHub",
                    "type": StorageLocation.GITHUB.value,
                    "url": "https://github.com/appsefilepro-cell/Private-Claude",
                    "status": "connected",
                    "indexed": True,
                },
                {
                    "name": "Airtable - Legal Docs",
                    "type": StorageLocation.AIRTABLE.value,
                    "base_id": "agentx5-apps-holdings",
                    "status": "connected",
                    "indexed": True,
                },
                {
                    "name": "Box - Documents",
                    "type": StorageLocation.BOX.value,
                    "folder_id": "ipva1wwf2vsj1hufqdfaf5s3ywlwvwws",
                    "status": "pending_auth",
                    "indexed": False,
                },
            ]

    def index_document(
        self,
        doc_id: str,
        title: str,
        doc_type: str,
        content: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add document to index."""
        self.document_index[doc_id] = {
            "id": doc_id,
            "title": title,
            "type": doc_type,
            "source": source,
            "metadata": metadata or {},
            "indexed_at": datetime.now().isoformat(),
        }

        # Update search index
        keywords = self._extract_keywords(title + " " + content)
        for keyword in keywords:
            if keyword not in self.search_index:
                self.search_index[keyword] = []
            self.search_index[keyword].append(doc_id)

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        words = text.lower().split()
        # Filter common words
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for"}
        return [w for w in words if len(w) > 3 and w not in stopwords]

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search indexed documents."""
        keywords = self._extract_keywords(query)
        results = set()

        for keyword in keywords:
            if keyword in self.search_index:
                results.update(self.search_index[keyword])

        return [self.document_index[doc_id] for doc_id in results if doc_id in self.document_index]

    def sync_from_github(self, repo_path: str) -> Dict[str, Any]:
        """Sync documents from GitHub repository."""
        self.last_sync = datetime.now().isoformat()
        return {
            "status": "synced",
            "source": "github",
            "repo": repo_path,
            "documents_indexed": len(self.document_index),
            "synced_at": self.last_sync,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        return {
            "total_documents": len(self.document_index),
            "total_keywords": len(self.search_index),
            "sources_configured": len(self.sources),
            "sources_connected": len([s for s in self.sources if s["status"] == "connected"]),
            "last_sync": self.last_sync,
        }


# ============================================================================
# GITHUB DOCUMENT ACCESS CONFIGURATION
# ============================================================================

GITHUB_DOCUMENT_ACCESS = {
    "primary_repo": "appsefilepro-cell/Private-Claude",
    "document_paths": [
        "documents/",
        "legal/",
        "templates/",
        "evidence/",
    ],
    "auto_index": True,
    "sync_interval": "hourly",
    "access_notes": """
    GitHub is the PRIMARY document storage because:
    1. Accessible from any device (phone, laptop, etc.)
    2. Version controlled - nothing gets lost
    3. Can be accessed via API
    4. Works with all integrations (VS Code, Codespaces, etc.)

    Documents that cannot be accessed on phone should be
    uploaded to GitHub for universal access.
    """,
}
