#!/usr/bin/env python3
"""
MADIO Context Generator
Generates AI_CONTEXT.md from analyzed MADIO documents
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class MADIOContextGenerator:
    """Generates AI_CONTEXT.md from document analysis"""
    
    def __init__(self):
        self.context_template = """# MADIO Framework - AI Context Bridge

**Generated**: {generation_date}  
**Last Updated**: {update_date}  
**Purpose**: Context bridge for {purpose_description}  
**Status**: {status}

## Current Project Status

**Project Name**: {project_name}  
**Import Date**: {import_date}  
**Source**: {source_type}  
**Document Count**: {document_count}  
**Complexity**: {complexity}  
**Template Compliance**: {compliance}%

## Major Capabilities

{capabilities_section}

## Document Hierarchy

### **Tier 1 - Primary Authority**
{tier1_section}

### **Tier 2 - Orchestration**
{tier2_section}

### **Tier 3 - Supporting Documents**
{tier3_section}

## Key Architectural Decisions

{architecture_section}

## Import Analysis

{import_analysis}

## Workflow Patterns

### **Development Cycle**
1. **Document Management**: Local editing in synced_docs/
2. **Version Control**: Git-based tracking
3. **Cloud Sync**: Google Docs integration via /push-to-docs
4. **Multi-Platform**: {platform_support}

### **Framework Validation**
- **Document Hierarchy**: {hierarchy_status}
- **Cross-References**: {xref_status}
- **Template Matching**: {template_status}

## Technical Specifications

### **Dependencies**
- **MADIO Framework**: madio-start template
- **Google Sync**: Optional Google Docs integration
- **Local Tools**: VS Code, Git, Python 3

### **File Organization**
```
{project_name}/
├── synced_docs/          # Imported MADIO documents
├── AI_CONTEXT.md         # This file
├── .madio                # Configuration
└── .claude/              # Commands and scripts
```

## Strategic Context

{strategic_context}

## Integration Instructions

### **For Local Development**
- Edit documents in synced_docs/
- Use Git for version control
- Run /push-to-docs for cloud sync

### **For AI Platforms**
- **OpenAI**: Use project_system_instructions.md as GPT instructions
- **Gemini**: Combine documents per platform requirements
- **Claude**: Upload to project knowledge with this context

### **For Ongoing Maintenance**
- Monitor with /sync-status
- Update context with significant changes
- Maintain document relationships

---

**Import Note**: This project was imported from existing MADIO documents. The structure has been analyzed and validated for framework compatibility. {import_notes}
"""

    def generate_context(self, analysis: Dict, import_mode: bool = False, timestamp: str = None) -> str:
        """Generate AI_CONTEXT.md from analysis results"""
        
        # Extract project information
        project_info = self._extract_project_info(analysis)
        
        # Build context sections
        context_data = {
            'generation_date': datetime.now().strftime('%B %d, %Y'),
            'update_date': datetime.now().strftime('%B %d, %Y'),
            'purpose_description': project_info['purpose'],
            'status': 'Imported from existing documents' if import_mode else 'Active development',
            'project_name': project_info['name'],
            'import_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_type': 'Imported MADIO documents' if import_mode else 'Template generation',
            'document_count': analysis['summary']['total_files'],
            'complexity': analysis['summary']['complexity'].title(),
            'compliance': analysis['summary']['compliance'],
            'capabilities_section': self._build_capabilities_section(analysis),
            'tier1_section': self._build_tier_section(analysis, 'tier1'),
            'tier2_section': self._build_tier_section(analysis, 'tier2'),
            'tier3_section': self._build_tier_section(analysis, 'tier3'),
            'architecture_section': self._build_architecture_section(analysis),
            'import_analysis': self._build_import_analysis(analysis),
            'platform_support': self._determine_platform_support(analysis),
            'hierarchy_status': self._assess_hierarchy(analysis),
            'xref_status': self._assess_cross_references(analysis),
            'template_status': self._assess_templates(analysis),
            'strategic_context': self._build_strategic_context(analysis, project_info),
            'import_notes': self._build_import_notes(analysis) if import_mode else ''
        }
        
        return self.context_template.format(**context_data)
    
    def _extract_project_info(self, analysis: Dict) -> Dict:
        """Extract project information from analyzed documents"""
        
        info = {
            'name': 'Unknown Project',
            'purpose': 'MADIO-compliant AI system',
            'domain': 'General',
            'target_audience': 'Users'
        }
        
        # Try to extract from Tier 1 document
        if analysis['documents']['tier1']:
            tier1_doc = analysis['documents']['tier1'][0]
            summary = tier1_doc.get('content_summary', {})
            
            # Extract project name from title or filename
            if summary.get('title'):
                info['name'] = summary['title'].replace('Project System Instructions', '').strip(' -:')
            else:
                # Derive from filename
                filename = tier1_doc['filename'].replace('project_system_instructions', '').strip('_-.')
                if filename and filename != '.md':
                    info['name'] = filename.replace('_', ' ').title()
            
            # Extract purpose
            if summary.get('purpose'):
                info['purpose'] = summary['purpose']
        
        return info
    
    def _build_capabilities_section(self, analysis: Dict) -> str:
        """Build capabilities section based on detected templates"""
        
        capabilities = []
        
        # Map templates to capabilities
        template_capabilities = {
            'character_voice_authority': '**Character & Voice**: Consistent personality and communication style',
            'content_operations': '**Content Management**: Validation and quality control systems',
            'methodology_framework': '**Analysis Framework**: Structured 8-step methodology',
            'rubrics_evaluation': '**Evaluation System**: Multi-dimensional scoring rubrics',
            'strategic_framework': '**Strategic Planning**: High-level strategic assessment',
            'research_protocols': '**Research Validation**: Evidence collection and verification',
            'implementation_roadmap': '**Implementation Planning**: Phased execution roadmaps',
            'visual_design_standards': '**Visual Consistency**: Brand and design guidelines',
            'visual_asset_generation': '**Asset Creation**: Automated visual content generation'
        }
        
        # Check which capabilities are present
        for tier_docs in analysis['documents'].values():
            for doc in tier_docs:
                template = doc.get('template_match')
                if template and template in template_capabilities:
                    capabilities.append(template_capabilities[template])
        
        # Add hierarchy capability
        if analysis['summary']['tier1_count'] > 0 and analysis['summary']['tier2_count'] > 0:
            capabilities.insert(0, '**Hierarchical Architecture**: Tier-based authority and control flow')
        
        if not capabilities:
            capabilities.append('**Core System**: Basic MADIO document structure')
        
        return '\n'.join(f"- {cap}" for cap in capabilities)
    
    def _build_tier_section(self, analysis: Dict, tier: str) -> str:
        """Build section for a specific tier"""
        
        docs = analysis['documents'][tier]
        if not docs:
            return "No documents found for this tier."
        
        lines = []
        for doc in docs:
            summary = doc.get('content_summary', {})
            title = summary.get('title', doc['filename'])
            purpose = summary.get('purpose', 'Supporting document')
            
            lines.append(f"**{doc['filename']}**")
            lines.append(f"- Purpose: {purpose}")
            
            if doc.get('template_match'):
                lines.append(f"- Template: {doc['template_match']}")
            
            if doc.get('validation', {}).get('issues'):
                lines.append(f"- ⚠️ Issues: {', '.join(doc['validation']['issues'])}")
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def _build_architecture_section(self, analysis: Dict) -> str:
        """Build architectural decisions section"""
        
        sections = []
        
        # Document organization
        sections.append("### **Document Organization**")
        sections.append(f"- Total Documents: {analysis['summary']['total_files']}")
        sections.append(f"- Hierarchy: Tier 1 ({analysis['summary']['tier1_count']}) → "
                       f"Tier 2 ({analysis['summary']['tier2_count']}) → "
                       f"Tier 3 ({analysis['summary']['tier3_count']})")
        
        # Template usage
        if any(doc.get('template_match') for tier_docs in analysis['documents'].values() for doc in tier_docs):
            sections.append("\n### **Template Usage**")
            template_counts = {}
            for tier_docs in analysis['documents'].values():
                for doc in tier_docs:
                    if doc.get('template_match'):
                        template_counts[doc['template_match']] = template_counts.get(doc['template_match'], 0) + 1
            
            for template, count in sorted(template_counts.items()):
                sections.append(f"- {template}: {count} document(s)")
        
        # Validation status
        sections.append("\n### **Validation Status**")
        valid_count = sum(1 for tier_docs in analysis['documents'].values() 
                         for doc in tier_docs if doc.get('validation', {}).get('is_valid', True))
        sections.append(f"- Valid Documents: {valid_count}/{analysis['summary']['total_files']}")
        sections.append(f"- Compliance Score: {analysis['summary']['compliance']}%")
        
        return '\n'.join(sections)
    
    def _build_import_analysis(self, analysis: Dict) -> str:
        """Build import analysis section"""
        
        sections = []
        
        # Warnings
        if analysis['summary'].get('warnings'):
            sections.append("### **Import Warnings**")
            for warning in analysis['summary']['warnings']:
                sections.append(f"- ⚠️ {warning}")
            sections.append("")
        
        # Document health
        sections.append("### **Document Health**")
        sections.append(f"- Recognized Documents: {analysis['summary']['total_files'] - analysis['summary']['unknown_count']}")
        sections.append(f"- Unknown Documents: {analysis['summary']['unknown_count']}")
        sections.append(f"- Validation Issues: {sum(len(doc.get('validation', {}).get('issues', [])) for tier_docs in analysis['documents'].values() for doc in tier_docs)}")
        
        # Relationships
        relationships = analysis.get('relationships', {})
        if relationships.get('cross_references'):
            sections.append("\n### **Document Relationships**")
            sections.append(f"- Cross-references found: {len(relationships['cross_references'])}")
            sections.append(f"- Dependency links: {len(relationships.get('dependencies', []))}")
        
        return '\n'.join(sections)
    
    def _determine_platform_support(self, analysis: Dict) -> str:
        """Determine which platforms are supported"""
        
        platforms = []
        
        # All MADIO systems support these by default
        if analysis['summary']['tier1_count'] > 0:
            platforms.append("OpenAI CustomGPT")
            platforms.append("Claude Project")
        
        if analysis['summary']['tier2_count'] > 0:
            platforms.append("Google Gemini Gem")
        
        return ', '.join(platforms) if platforms else "Platform support unclear"
    
    def _assess_hierarchy(self, analysis: Dict) -> str:
        """Assess document hierarchy status"""
        
        if analysis['summary']['tier1_count'] == 1 and analysis['summary']['tier2_count'] == 1:
            return "✅ Valid (Tier 1 → Tier 2 → Tier 3)"
        elif analysis['summary']['tier1_count'] == 0:
            return "❌ Missing Tier 1 authority document"
        elif analysis['summary']['tier2_count'] == 0:
            return "❌ Missing Tier 2 orchestrator"
        else:
            return "⚠️ Multiple authority documents detected"
    
    def _assess_cross_references(self, analysis: Dict) -> str:
        """Assess cross-reference status"""
        
        total_refs = len(analysis.get('relationships', {}).get('cross_references', []))
        
        if total_refs > 5:
            return f"✅ Strong ({total_refs} references)"
        elif total_refs > 0:
            return f"⚠️ Limited ({total_refs} references)"
        else:
            return "❌ No cross-references found"
    
    def _assess_templates(self, analysis: Dict) -> str:
        """Assess template matching status"""
        
        matched = sum(1 for tier_docs in analysis['documents'].values() 
                     for doc in tier_docs if doc.get('template_match'))
        
        if matched == analysis['summary']['total_files']:
            return "✅ All documents matched"
        elif matched > 0:
            return f"⚠️ Partial ({matched}/{analysis['summary']['total_files']} matched)"
        else:
            return "❌ No template matches found"
    
    def _build_strategic_context(self, analysis: Dict, project_info: Dict) -> str:
        """Build strategic context section"""
        
        sections = []
        
        sections.append("### **Import Context**")
        sections.append(f"- **Source**: Pre-existing MADIO documents")
        sections.append(f"- **Method**: Document analysis and structure detection")
        sections.append(f"- **Validation**: {analysis['summary']['compliance']}% MADIO compliance")
        
        sections.append("\n### **Recommended Actions**")
        if analysis['summary']['compliance'] < 100:
            sections.append("- Review and address validation warnings")
        if analysis['summary']['unknown_count'] > 0:
            sections.append("- Classify or remove unknown documents")
        if not any(doc.get('template_match') for tier_docs in analysis['documents'].values() for doc in tier_docs):
            sections.append("- Consider aligning documents with MADIO templates")
        
        sections.append("- Set up Google Docs sync for cloud collaboration")
        sections.append("- Customize imported content for specific use case")
        
        return '\n'.join(sections)
    
    def _build_import_notes(self, analysis: Dict) -> str:
        """Build import-specific notes"""
        
        notes = []
        
        if analysis['summary']['compliance'] == 100:
            notes.append("All documents successfully validated against MADIO standards.")
        else:
            notes.append(f"Some validation issues detected (compliance: {analysis['summary']['compliance']}%).")
        
        if analysis['summary']['unknown_count'] > 0:
            notes.append(f"{analysis['summary']['unknown_count']} documents could not be automatically classified.")
        
        return ' '.join(notes)
    
    def save_context(self, content: str, filename: str = "AI_CONTEXT.md") -> bool:
        """Save context to file"""
        
        try:
            # Backup existing file if it exists
            if os.path.exists(filename):
                backup_name = f"{filename}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(filename, backup_name)
                print(f"📋 Backed up existing {filename} to {backup_name}")
            
            # Write new context
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save context: {str(e)}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Generate MADIO AI_CONTEXT.md')
    parser.add_argument('--analysis', required=True, help='Analysis JSON file from analyze_madio_import.py')
    parser.add_argument('--import-mode', action='store_true', help='Generate context for imported documents')
    parser.add_argument('--timestamp', help='Import timestamp for tracking')
    parser.add_argument('--output', default='AI_CONTEXT.md', help='Output filename')
    
    args = parser.parse_args()
    
    try:
        # Load analysis
        with open(args.analysis, 'r') as f:
            analysis = json.load(f)
        
        # Generate context
        generator = MADIOContextGenerator()
        context = generator.generate_context(
            analysis,
            import_mode=args.import_mode,
            timestamp=args.timestamp
        )
        
        # Save context
        success = generator.save_context(context, args.output)
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Context generation failed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
