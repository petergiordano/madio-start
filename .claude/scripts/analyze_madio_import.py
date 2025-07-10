#!/usr/bin/env python3
"""
MADIO Document Analysis Script
Analyzes existing MADIO documents to determine structure, hierarchy, and relationships
"""

import json
import os
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class MADIODocumentAnalyzer:
    """Analyzes MADIO documents to understand structure and relationships"""
    
    def __init__(self):
        self.tier_patterns = {
            'tier1': {
                'patterns': ['project_system_instructions', 'system_instructions'],
                'content_markers': ['Primary Directive', 'Supreme Authority', 'Tier 1'],
                'required': True
            },
            'tier2': {
                'patterns': ['orchestrator'],
                'content_markers': ['Workflow', 'Step-by-Step', 'Tier 2'],
                'required': True
            },
            'tier3': {
                'patterns': [
                    'character_voice', 'content_operations', 'methodology_framework',
                    'rubrics_evaluation', 'strategic_framework', 'research_protocols',
                    'implementation_roadmap', 'document_reference_map', 'visual_design',
                    'visual_asset', 'standard'
                ],
                'content_markers': ['Tier 3', 'Supporting Document'],
                'required': False
            }
        }
        
        self.template_signatures = {
            'character_voice_authority': ['Personality', 'Voice', 'Tone', 'Communication Style'],
            'content_operations': ['Content Validation', 'Quality Standards', 'Curation'],
            'methodology_framework': ['8-Step', 'Analysis Process', 'Methodology'],
            'rubrics_evaluation': ['Scoring', 'Evaluation Criteria', 'Assessment'],
            'strategic_framework': ['Strategic', 'Planning', 'Vision'],
            'research_protocols': ['Research', 'Evidence', 'Validation'],
            'implementation_roadmap': ['Implementation', 'Phases', 'Timeline'],
            'document_reference_map': ['Cross-Reference', 'Document Map', 'Relationships'],
            'visual_design_standards': ['Visual', 'Brand', 'Design Guidelines'],
            'visual_asset_generation': ['Image', 'Graphics', 'Visual Creation'],
            'standard': ['Template', 'Format', 'Structure']
        }
    
    def analyze_files(self, file_list: List[str]) -> Dict:
        """Analyze a list of files and return structured analysis"""
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'documents': {
                'tier1': [],
                'tier2': [],
                'tier3': [],
                'unknown': []
            },
            'summary': {
                'total_files': len(file_list),
                'tier1_count': 0,
                'tier2_count': 0,
                'tier3_count': 0,
                'unknown_count': 0,
                'complexity': 'unknown',
                'compliance': 0,
                'warnings': [],
                'template_matches': {}
            },
            'relationships': {
                'cross_references': [],
                'dependencies': []
            }
        }
        
        # Analyze each file
        for file_path in file_list:
            if os.path.exists(file_path):
                doc_info = self.analyze_document(file_path)
                tier = doc_info['tier']
                
                if tier in ['tier1', 'tier2', 'tier3']:
                    analysis['documents'][tier].append(doc_info)
                    analysis['summary'][f'{tier}_count'] += 1
                else:
                    analysis['documents']['unknown'].append(doc_info)
                    analysis['summary']['unknown_count'] += 1
        
        # Post-analysis calculations
        analysis['summary']['complexity'] = self._determine_complexity(analysis)
        analysis['summary']['compliance'] = self._calculate_compliance(analysis)
        analysis['summary']['warnings'] = self._generate_warnings(analysis)
        analysis['relationships'] = self._analyze_relationships(analysis)
        
        return analysis
    
    def analyze_document(self, file_path: str) -> Dict:
        """Analyze a single document"""
        
        doc_info = {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'tier': 'unknown',
            'template_match': None,
            'size': os.path.getsize(file_path),
            'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            'content_summary': {},
            'cross_references': [],
            'validation': {
                'is_valid': True,
                'issues': []
            }
        }
        
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            
            # Detect tier
            doc_info['tier'] = self._detect_tier(doc_info['filename'], content)
            
            # Match template
            doc_info['template_match'] = self._match_template(content)
            
            # Extract content summary
            doc_info['content_summary'] = self._extract_content_summary(content)
            
            # Find cross-references
            doc_info['cross_references'] = self._find_cross_references(content)
            
            # Validate document
            doc_info['validation'] = self._validate_document(doc_info, content)
            
        except Exception as e:
            doc_info['validation']['is_valid'] = False
            doc_info['validation']['issues'].append(f"Error reading file: {str(e)}")
        
        return doc_info
    
    def _detect_tier(self, filename: str, content: str) -> str:
        """Detect document tier from filename and content"""
        
        filename_lower = filename.lower()
        
        # Check filename patterns
        for tier, config in self.tier_patterns.items():
            for pattern in config['patterns']:
                if pattern in filename_lower:
                    return tier
        
        # Check content markers
        for tier, config in self.tier_patterns.items():
            for marker in config['content_markers']:
                if marker in content:
                    return tier
        
        # Special content analysis
        if re.search(r'Primary\s+Directive|Supreme\s+Authority', content, re.IGNORECASE):
            return 'tier1'
        elif re.search(r'Workflow|Step\s+\d+:|Orchestrat', content, re.IGNORECASE):
            return 'tier2'
        elif re.search(r'Tier\s+3|Supporting\s+Document', content, re.IGNORECASE):
            return 'tier3'
        
        return 'unknown'
    
    def _match_template(self, content: str) -> Optional[str]:
        """Match content against known MADIO templates"""
        
        best_match = None
        best_score = 0
        
        for template_name, signatures in self.template_signatures.items():
            score = sum(1 for sig in signatures if sig.lower() in content.lower())
            if score > best_score and score >= len(signatures) * 0.5:
                best_score = score
                best_match = template_name
        
        return best_match
    
    def _extract_content_summary(self, content: str) -> Dict:
        """Extract key information from document content"""
        
        summary = {
            'title': None,
            'purpose': None,
            'key_sections': [],
            'word_count': len(content.split()),
            'line_count': len(content.splitlines())
        }
        
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            summary['title'] = title_match.group(1).strip()
        
        # Extract purpose/description
        purpose_match = re.search(r'Purpose:\s*(.+)|Description:\s*(.+)', content, re.IGNORECASE)
        if purpose_match:
            summary['purpose'] = (purpose_match.group(1) or purpose_match.group(2)).strip()
        
        # Extract section headings
        headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        summary['key_sections'] = headings[:10]  # First 10 sections
        
        return summary
    
    def _find_cross_references(self, content: str) -> List[str]:
        """Find references to other MADIO documents"""
        
        references = []
        
        # Find markdown links
        link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        for _, link in link_matches:
            references.append(os.path.basename(link))
        
        # Find document mentions
        for pattern in ['orchestrator.md', 'project_system_instructions.md']:
            if pattern in content:
                references.append(pattern)
        
        # Find tier references
        tier_refs = re.findall(r'Tier\s+[123]\s+document[s]?\s*:\s*([^\n]+)', content, re.IGNORECASE)
        references.extend(tier_refs)
        
        return list(set(references))
    
    def _validate_document(self, doc_info: Dict, content: str) -> Dict:
        """Validate document structure and content"""
        
        validation = {
            'is_valid': True,
            'issues': []
        }
        
        # Check for required content based on tier
        if doc_info['tier'] == 'tier1':
            if 'Primary Directive' not in content and 'Purpose' not in content:
                validation['issues'].append("Missing Primary Directive or Purpose section")
            if not re.search(r'Tier\s+2\s+document|orchestrator', content, re.IGNORECASE):
                validation['issues'].append("No reference to Tier 2 orchestrator")
        
        elif doc_info['tier'] == 'tier2':
            if not re.search(r'Step\s+\d+|Workflow', content, re.IGNORECASE):
                validation['issues'].append("Missing workflow steps")
            if 'Tier 3' not in content and not doc_info['cross_references']:
                validation['issues'].append("No references to Tier 3 documents")
        
        # Check document size
        if doc_info['size'] < 100:
            validation['issues'].append("Document appears to be empty or minimal")
        
        # Check for placeholder content
        if '[PLACEHOLDER]' in content or 'TODO' in content:
            validation['issues'].append("Contains placeholder or TODO content")
        
        validation['is_valid'] = len(validation['issues']) == 0
        
        return validation
    
    def _determine_complexity(self, analysis: Dict) -> str:
        """Determine project complexity based on document count and structure"""
        
        total_docs = analysis['summary']['total_files']
        
        if total_docs <= 4:
            return 'simple'
        elif total_docs <= 7:
            return 'moderate'
        elif total_docs <= 10:
            return 'complex'
        else:
            return 'enterprise'
    
    def _calculate_compliance(self, analysis: Dict) -> int:
        """Calculate MADIO compliance percentage"""
        
        score = 100
        
        # Check for required documents
        if analysis['summary']['tier1_count'] == 0:
            score -= 30
            
        if analysis['summary']['tier2_count'] == 0:
            score -= 30
        
        # Check for validation issues
        total_issues = 0
        for tier_docs in analysis['documents'].values():
            for doc in tier_docs:
                if not doc['validation']['is_valid']:
                    total_issues += len(doc['validation']['issues'])
        
        # Deduct for issues (max 20 points)
        issue_penalty = min(total_issues * 2, 20)
        score -= issue_penalty
        
        # Check for unknown documents
        if analysis['summary']['unknown_count'] > 0:
            score -= 10
        
        return max(0, score)
    
    def _generate_warnings(self, analysis: Dict) -> List[str]:
        """Generate warnings based on analysis"""
        
        warnings = []
        
        if analysis['summary']['tier1_count'] == 0:
            warnings.append("No Tier 1 (project_system_instructions) document found")
        elif analysis['summary']['tier1_count'] > 1:
            warnings.append("Multiple Tier 1 documents found - only one should exist")
        
        if analysis['summary']['tier2_count'] == 0:
            warnings.append("No Tier 2 (orchestrator) document found")
        elif analysis['summary']['tier2_count'] > 1:
            warnings.append("Multiple Tier 2 documents found - only one should exist")
        
        if analysis['summary']['unknown_count'] > 0:
            warnings.append(f"{analysis['summary']['unknown_count']} documents could not be classified")
        
        return warnings
    
    def _analyze_relationships(self, analysis: Dict) -> Dict:
        """Analyze relationships between documents"""
        
        relationships = {
            'cross_references': [],
            'dependencies': []
        }
        
        # Build cross-reference map
        for tier_docs in analysis['documents'].values():
            for doc in tier_docs:
                for ref in doc['cross_references']:
                    relationships['cross_references'].append({
                        'from': doc['filename'],
                        'to': ref
                    })
        
        # Identify dependencies based on tier
        if analysis['summary']['tier1_count'] > 0 and analysis['summary']['tier2_count'] > 0:
            tier1_doc = analysis['documents']['tier1'][0]['filename']
            tier2_doc = analysis['documents']['tier2'][0]['filename']
            
            relationships['dependencies'].append({
                'parent': tier1_doc,
                'child': tier2_doc,
                'type': 'authority'
            })
            
            # Tier 2 depends on all Tier 3
            for tier3_doc in analysis['documents']['tier3']:
                relationships['dependencies'].append({
                    'parent': tier2_doc,
                    'child': tier3_doc['filename'],
                    'type': 'orchestration'
                })
        
        return relationships


def main():
    parser = argparse.ArgumentParser(description='Analyze MADIO documents')
    parser.add_argument('--file-list', required=True, help='File containing list of documents to analyze')
    parser.add_argument('--output', required=True, help='Output JSON file for analysis results')
    parser.add_argument('--log', help='Log file for detailed output')
    
    args = parser.parse_args()
    
    # Set up logging
    if args.log:
        import logging
        logging.basicConfig(filename=args.log, level=logging.DEBUG,
                          format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        # Read file list
        with open(args.file_list, 'r') as f:
            files = [line.strip() for line in f if line.strip()]
        
        # Analyze documents
        analyzer = MADIODocumentAnalyzer()
        analysis = analyzer.analyze_files(files)
        
        # Write results
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✅ Analysis complete. Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        if args.log:
            import logging
            logging.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
