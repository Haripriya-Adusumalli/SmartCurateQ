import json
from typing import Dict, Any, List
try:
    from google.cloud import pubsub_v1, bigquery
except ImportError:
    pubsub_v1 = None
    bigquery = None
from config import Config, InvestorPreferences
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
except ImportError:
    vertexai = None
    GenerativeModel = None

class ScoringEngine:
    """Evaluates startups against 350 curation metrics with investor preferences"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient() if pubsub_v1 else None
        self.bq_client = bigquery.Client(project=project_id) if bigquery else None
        if vertexai:
            try:
                vertexai.init(project=project_id, location=Config.LOCATION)
                self.model = GenerativeModel('gemini-2.5-pro')
            except Exception:
                self.model = None
        else:
            self.model = None
        
        # Load scoring rules from BigQuery
        self.scoring_rules = self._load_scoring_rules()
        self.default_weights = Config.SCORING_SEGMENTS
    
    def score_startup(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Score startup against 350 metrics with investor preferences"""
        
        app_id = message['app_id']
        run_id = message['run_id']
        canonical_json = message['canonical_json']
        investor_weights = message.get('investor_weights_json', {})
        
        # Calculate scores for each segment
        segment_scores = {
            'founder_profile_score': self._score_founder_profile(
                canonical_json.get('founder_profile_metrics', {}),
                investor_weights
            ),
            'problem_market_score': self._score_problem_market(
                canonical_json.get('problem_market_metrics', {}),
                investor_weights
            ),
            'differentiator_score': self._score_differentiator(
                canonical_json.get('differentiator_metrics', {}),
                investor_weights
            ),
            'team_traction_score': self._score_team_traction(
                canonical_json.get('team_traction_metrics', {}),
                investor_weights
            )
        }
        
        # Calculate overall score with investor preferences
        overall_score = self._calculate_overall_score(segment_scores, investor_weights)
        
        # Generate curation decision
        decision = self._generate_curation_decision(overall_score, segment_scores, canonical_json)
        
        # Identify evidence and explanations
        evidence_refs = self._generate_evidence_references(canonical_json, segment_scores)
        
        # Check if voice interview is needed
        requires_voice_interview = self._requires_voice_interview(segment_scores, canonical_json)
        
        scoring_result = {
            'segment_scores': segment_scores,
            'overall_score': overall_score,
            'decision': decision,
            'evidence_refs': evidence_refs,
            'requires_voice_interview': requires_voice_interview,
            'confidence_score': self._calculate_confidence_score(canonical_json),
            'risk_flags': self._identify_risk_flags(canonical_json),
            'investor_alignment': self._assess_investor_alignment(segment_scores, investor_weights)
        }
        
        # Publish scoring completion
        self._publish_message('scoring-completed', {
            'run_id': run_id,
            'app_id': app_id,
            'scoring_result': scoring_result,
            'requires_voice_interview': requires_voice_interview
        })
        
        return scoring_result
    
    def rescore_with_voice_data(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Re-score startup incorporating voice interview insights"""
        
        app_id = message['app_id']
        run_id = message['run_id']
        voice_data = message['voice_data']
        
        # Get original canonical data and enhance with voice insights
        enhanced_canonical = self._enhance_with_voice_data(message.get('canonical_json', {}), voice_data)
        
        # Re-run scoring with enhanced data
        return self.score_startup({
            'app_id': app_id,
            'run_id': run_id,
            'canonical_json': enhanced_canonical,
            'investor_weights_json': message.get('investor_weights_json', {})
        })
    
    def _score_founder_profile(self, founder_metrics: Dict[str, Any], investor_weights: Dict[str, float]) -> Dict[str, Any]:
        """Score founder profile segment (87 metrics)"""
        
        # Core founder scoring
        founder_market_fit = founder_metrics.get('founder_market_fit_score', 5.0)
        experience_score = min(founder_metrics.get('founder_experience_years', 0) / 10.0 * 10, 10)
        domain_expertise = founder_metrics.get('founder_domain_expertise', 5.0)
        previous_exits = min(founder_metrics.get('founder_previous_exits', 0) * 2, 10)
        
        # Verification scores
        verification_bonus = 0
        if founder_metrics.get('linkedin_verified', False):
            verification_bonus += 1
        if founder_metrics.get('education_verified', False):
            verification_bonus += 1
        if founder_metrics.get('previous_companies_verified', False):
            verification_bonus += 1
        
        # Leadership and commitment
        leadership_score = founder_metrics.get('leadership_experience', 5.0)
        commitment_score = 10 if founder_metrics.get('full_time_commitment', True) else 5
        
        # Calculate weighted score
        base_score = (
            founder_market_fit * 0.3 +
            experience_score * 0.2 +
            domain_expertise * 0.2 +
            leadership_score * 0.15 +
            commitment_score * 0.1 +
            verification_bonus * 0.05
        )
        
        # Apply investor preferences
        investor_weight = investor_weights.get('founder_weight', self.default_weights['founder_profile'])
        weighted_score = base_score * investor_weight / self.default_weights['founder_profile']
        
        return {
            'base_score': base_score,
            'weighted_score': min(weighted_score, 10.0),
            'key_strengths': self._identify_founder_strengths(founder_metrics),
            'key_concerns': self._identify_founder_concerns(founder_metrics),
            'evidence_points': [
                f"Founder-market fit score: {founder_market_fit}/10",
                f"Years of experience: {founder_metrics.get('founder_experience_years', 0)}",
                f"Domain expertise: {domain_expertise}/10"
            ]
        }
    
    def _score_problem_market(self, market_metrics: Dict[str, Any], investor_weights: Dict[str, float]) -> Dict[str, Any]:
        """Score problem/market segment (88 metrics)"""
        
        # Market size scoring
        tam = market_metrics.get('total_addressable_market', 0)
        market_size_score = min(tam / 1e9, 10)  # $1B = 1 point, $10B+ = 10 points
        
        # Market growth
        growth_rate = market_metrics.get('market_growth_rate', 0)
        growth_score = min(growth_rate * 50, 10)  # 20% growth = 10 points
        
        # Problem validation
        problem_urgency = market_metrics.get('problem_urgency_score', 5.0)
        problem_frequency = market_metrics.get('problem_frequency_score', 5.0)
        market_validation = market_metrics.get('problem_market_validation', 5.0)
        
        # Competitive landscape
        competitive_intensity = market_metrics.get('competitive_intensity', 5.0)
        competitive_score = 10 - (competitive_intensity * 0.5)  # Less competition = higher score
        
        # Market timing
        timing_score = market_metrics.get('market_timing_score', 5.0)
        
        base_score = (
            market_size_score * 0.25 +
            growth_score * 0.2 +
            problem_urgency * 0.15 +
            market_validation * 0.15 +
            competitive_score * 0.15 +
            timing_score * 0.1
        )
        
        # Apply investor preferences
        investor_weight = investor_weights.get('market_weight', self.default_weights['problem_market_size'])
        weighted_score = base_score * investor_weight / self.default_weights['problem_market_size']
        
        return {
            'base_score': base_score,
            'weighted_score': min(weighted_score, 10.0),
            'key_strengths': self._identify_market_strengths(market_metrics),
            'key_concerns': self._identify_market_concerns(market_metrics),
            'evidence_points': [
                f"Total addressable market: ${tam/1e9:.1f}B",
                f"Market growth rate: {growth_rate:.1%}",
                f"Problem urgency score: {problem_urgency}/10"
            ]
        }
    
    def _score_differentiator(self, diff_metrics: Dict[str, Any], investor_weights: Dict[str, float]) -> Dict[str, Any]:
        """Score unique differentiator segment (87 metrics)"""
        
        # Technology differentiation
        tech_novelty = diff_metrics.get('technology_novelty_score', 5.0)
        ip_strength = diff_metrics.get('ip_portfolio_strength', 5.0)
        tech_complexity = diff_metrics.get('technical_complexity', 5.0)
        
        # Business model innovation
        bm_novelty = diff_metrics.get('business_model_novelty', 5.0)
        revenue_model = diff_metrics.get('revenue_model_strength', 5.0)
        scalability = diff_metrics.get('scalability_potential', 5.0)
        
        # Market positioning
        value_prop = diff_metrics.get('value_proposition_clarity', 5.0)
        customer_focus = diff_metrics.get('customer_segment_focus', 5.0)
        
        # Competitive advantages
        first_mover = diff_metrics.get('first_mover_advantage', 5.0)
        switching_costs = diff_metrics.get('switching_costs', 5.0)
        network_effects = diff_metrics.get('network_effects_potential', 5.0)
        
        base_score = (
            tech_novelty * 0.2 +
            ip_strength * 0.15 +
            bm_novelty * 0.15 +
            scalability * 0.15 +
            value_prop * 0.1 +
            first_mover * 0.1 +
            network_effects * 0.1 +
            switching_costs * 0.05
        )
        
        # Apply investor preferences
        investor_weight = investor_weights.get('differentiation_weight', self.default_weights['unique_differentiator'])
        weighted_score = base_score * investor_weight / self.default_weights['unique_differentiator']
        
        return {
            'base_score': base_score,
            'weighted_score': min(weighted_score, 10.0),
            'key_strengths': self._identify_diff_strengths(diff_metrics),
            'key_concerns': self._identify_diff_concerns(diff_metrics),
            'evidence_points': [
                f"Technology novelty: {tech_novelty}/10",
                f"IP portfolio strength: {ip_strength}/10",
                f"Scalability potential: {scalability}/10"
            ]
        }
    
    def _score_team_traction(self, traction_metrics: Dict[str, Any], investor_weights: Dict[str, float]) -> Dict[str, Any]:
        """Score team & traction segment (88 metrics)"""
        
        # Revenue metrics
        arr = traction_metrics.get('annual_recurring_revenue', 0)
        revenue_score = min(arr / 1e6, 10)  # $1M ARR = 1 point
        
        revenue_growth = traction_metrics.get('revenue_growth_rate', 0)
        growth_score = min(revenue_growth * 10, 10)  # 100% growth = 10 points
        
        # Unit economics
        ltv_cac_ratio = traction_metrics.get('ltv_cac_ratio', 0)
        unit_econ_score = min(ltv_cac_ratio / 3, 10)  # 3:1 ratio = 10 points
        
        # Customer metrics
        customer_count = traction_metrics.get('total_customers', 0)
        customer_score = min(customer_count / 1000, 10)  # 1000 customers = 1 point
        
        retention_rate = traction_metrics.get('customer_retention_rate', 0)
        retention_score = retention_rate * 10  # 90% retention = 9 points
        
        # Team metrics
        team_size = traction_metrics.get('team_size', 0)
        team_score = min(team_size / 10, 10)  # 10 employees = 1 point
        
        # Funding efficiency
        funding_efficiency = traction_metrics.get('funding_efficiency', 0)
        efficiency_score = min(funding_efficiency * 10, 10)
        
        base_score = (
            revenue_score * 0.25 +
            growth_score * 0.2 +
            unit_econ_score * 0.15 +
            retention_score * 0.15 +
            customer_score * 0.1 +
            team_score * 0.1 +
            efficiency_score * 0.05
        )
        
        # Apply investor preferences
        investor_weight = investor_weights.get('traction_weight', self.default_weights['team_traction'])
        weighted_score = base_score * investor_weight / self.default_weights['team_traction']
        
        return {
            'base_score': base_score,
            'weighted_score': min(weighted_score, 10.0),
            'key_strengths': self._identify_traction_strengths(traction_metrics),
            'key_concerns': self._identify_traction_concerns(traction_metrics),
            'evidence_points': [
                f"Annual recurring revenue: ${arr:,.0f}",
                f"Revenue growth rate: {revenue_growth:.1%}",
                f"LTV/CAC ratio: {ltv_cac_ratio:.1f}"
            ]
        }
    
    def _calculate_overall_score(self, segment_scores: Dict[str, Dict], investor_weights: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        
        # Get weighted scores from each segment
        founder_score = segment_scores['founder_profile_score']['weighted_score']
        market_score = segment_scores['problem_market_score']['weighted_score']
        diff_score = segment_scores['differentiator_score']['weighted_score']
        traction_score = segment_scores['team_traction_score']['weighted_score']
        
        # Apply segment weights
        founder_weight = investor_weights.get('founder_weight', self.default_weights['founder_profile'])
        market_weight = investor_weights.get('market_weight', self.default_weights['problem_market_size'])
        diff_weight = investor_weights.get('differentiation_weight', self.default_weights['unique_differentiator'])
        traction_weight = investor_weights.get('traction_weight', self.default_weights['team_traction'])
        
        # Normalize weights
        total_weight = founder_weight + market_weight + diff_weight + traction_weight
        if total_weight > 0:
            founder_weight /= total_weight
            market_weight /= total_weight
            diff_weight /= total_weight
            traction_weight /= total_weight
        
        overall_score = (
            founder_score * founder_weight +
            market_score * market_weight +
            diff_score * diff_weight +
            traction_score * traction_weight
        )
        
        return min(overall_score, 10.0)
    
    def _generate_curation_decision(self, overall_score: float, segment_scores: Dict, canonical_json: Dict) -> str:
        """Generate pass/hold/reject decision"""
        
        risk_metrics = canonical_json.get('risk_metrics', {})
        verification_metrics = canonical_json.get('verification_metrics', {})
        
        # Check for automatic rejection criteria
        if overall_score < 4.0:
            return 'reject'
        
        if risk_metrics.get('reputation_risk_score', 0) > 8.0:
            return 'reject'
        
        if verification_metrics.get('overall_verification_score', 10) < 3.0:
            return 'hold'
        
        # Decision based on overall score
        if overall_score >= 7.0:
            return 'pass'
        elif overall_score >= 5.5:
            return 'hold'
        else:
            return 'reject'
    
    def _requires_voice_interview(self, segment_scores: Dict, canonical_json: Dict) -> bool:
        """Determine if voice interview is needed for clarification"""
        
        # Voice interview needed if:
        # 1. Borderline overall score (5-7 range)
        # 2. Conflicting segment scores
        # 3. Verification concerns
        # 4. Ambiguous claims in original data
        
        overall_score = self._calculate_overall_score(segment_scores, {})
        
        if 5.0 <= overall_score <= 7.0:
            return True
        
        # Check for conflicting segment scores
        scores = [s['base_score'] for s in segment_scores.values()]
        if max(scores) - min(scores) > 4.0:
            return True
        
        # Check verification concerns
        verification_metrics = canonical_json.get('verification_metrics', {})
        if verification_metrics.get('overall_verification_score', 10) < 6.0:
            return True
        
        return False
    
    def _calculate_confidence_score(self, canonical_json: Dict) -> float:
        """Calculate confidence in the scoring"""
        
        verification_score = canonical_json.get('verification_metrics', {}).get('overall_verification_score', 5.0)
        data_completeness = self._assess_data_completeness(canonical_json)
        
        confidence = (verification_score * 0.6 + data_completeness * 0.4) / 10.0
        return min(confidence, 1.0)
    
    def _identify_risk_flags(self, canonical_json: Dict) -> List[str]:
        """Identify risk flags from metrics"""
        
        risk_flags = []
        risk_metrics = canonical_json.get('risk_metrics', {})
        
        if risk_metrics.get('reputation_risk_score', 0) > 6.0:
            risk_flags.append('reputation_concerns')
        
        if risk_metrics.get('financial_risk_score', 0) > 7.0:
            risk_flags.append('financial_instability')
        
        if risk_metrics.get('market_risk_score', 0) > 7.0:
            risk_flags.append('market_uncertainty')
        
        if risk_metrics.get('execution_risk_score', 0) > 7.0:
            risk_flags.append('execution_challenges')
        
        # Check verification issues
        verification_metrics = canonical_json.get('verification_metrics', {})
        if verification_metrics.get('market_size_verification') == 'inflated':
            risk_flags.append('inflated_market_claims')
        
        if verification_metrics.get('revenue_verification') == 'unverified':
            risk_flags.append('unverified_revenue')
        
        return risk_flags
    
    def _assess_investor_alignment(self, segment_scores: Dict, investor_weights: Dict) -> Dict[str, Any]:
        """Assess alignment with investor preferences"""
        
        alignment_score = 0
        focus_areas = []
        
        # Identify investor focus based on weights
        weights = {
            'founder': investor_weights.get('founder_weight', 0.25),
            'market': investor_weights.get('market_weight', 0.25),
            'differentiation': investor_weights.get('differentiation_weight', 0.25),
            'traction': investor_weights.get('traction_weight', 0.25)
        }
        
        max_weight = max(weights.values())
        for area, weight in weights.items():
            if weight >= max_weight * 0.8:  # Within 80% of max weight
                focus_areas.append(area)
        
        # Calculate alignment based on performance in focus areas
        if 'founder' in focus_areas:
            alignment_score += segment_scores['founder_profile_score']['base_score'] * weights['founder']
        if 'market' in focus_areas:
            alignment_score += segment_scores['problem_market_score']['base_score'] * weights['market']
        if 'differentiation' in focus_areas:
            alignment_score += segment_scores['differentiator_score']['base_score'] * weights['differentiation']
        if 'traction' in focus_areas:
            alignment_score += segment_scores['team_traction_score']['base_score'] * weights['traction']
        
        return {
            'alignment_score': alignment_score,
            'investor_focus_areas': focus_areas,
            'recommendation_fit': 'high' if alignment_score > 7.0 else 'medium' if alignment_score > 5.0 else 'low'
        }
    
    def _enhance_with_voice_data(self, canonical_json: Dict, voice_data: Dict) -> Dict:
        """Enhance canonical data with voice interview insights"""
        
        enhanced = canonical_json.copy()
        extracted_fields = voice_data.get('extracted_fields', {})
        
        # Update metrics based on voice clarifications
        if 'founder_profile_metrics' in enhanced:
            enhanced['founder_profile_metrics'].update({
                'vision_clarity': extracted_fields.get('vision_clarity_score', 
                    enhanced['founder_profile_metrics'].get('vision_clarity', 5.0)),
                'execution_track_record': extracted_fields.get('execution_score',
                    enhanced['founder_profile_metrics'].get('execution_track_record', 5.0))
            })
        
        # Update market metrics with clarifications
        if 'problem_market_metrics' in enhanced:
            enhanced['problem_market_metrics'].update({
                'problem_market_validation': extracted_fields.get('market_validation_score',
                    enhanced['problem_market_metrics'].get('problem_market_validation', 5.0))
            })
        
        return enhanced
    
    def _generate_evidence_references(self, canonical_json: Dict, segment_scores: Dict) -> List[str]:
        """Generate evidence references for scoring decisions"""
        
        evidence_refs = []
        
        # Collect evidence from each segment
        for segment_name, segment_data in segment_scores.items():
            evidence_refs.extend(segment_data.get('evidence_points', []))
        
        # Add verification evidence
        verification_metrics = canonical_json.get('verification_metrics', {})
        for metric, status in verification_metrics.items():
            if isinstance(status, dict) and 'evidence' in status:
                evidence_refs.append(f"{metric}: {status['evidence']}")
        
        return evidence_refs
    
    def _assess_data_completeness(self, canonical_json: Dict) -> float:
        """Assess completeness of data for scoring"""
        
        total_metrics = 0
        complete_metrics = 0
        
        for segment, metrics in canonical_json.items():
            if isinstance(metrics, dict):
                for metric, value in metrics.items():
                    total_metrics += 1
                    if value is not None and value != 0 and value != '':
                        complete_metrics += 1
        
        return (complete_metrics / total_metrics * 10) if total_metrics > 0 else 5.0
    
    # Helper methods for identifying strengths and concerns
    def _identify_founder_strengths(self, founder_metrics: Dict) -> List[str]:
        strengths = []
        if founder_metrics.get('founder_market_fit_score', 0) >= 8.0:
            strengths.append('Strong founder-market fit')
        if founder_metrics.get('founder_experience_years', 0) >= 10:
            strengths.append('Extensive industry experience')
        if founder_metrics.get('founder_previous_exits', 0) > 0:
            strengths.append('Previous successful exits')
        return strengths
    
    def _identify_founder_concerns(self, founder_metrics: Dict) -> List[str]:
        concerns = []
        if founder_metrics.get('founder_market_fit_score', 10) < 5.0:
            concerns.append('Weak founder-market fit')
        if not founder_metrics.get('full_time_commitment', True):
            concerns.append('Part-time founder commitment')
        return concerns
    
    def _identify_market_strengths(self, market_metrics: Dict) -> List[str]:
        strengths = []
        if market_metrics.get('total_addressable_market', 0) >= 10e9:
            strengths.append('Large addressable market')
        if market_metrics.get('market_growth_rate', 0) >= 0.15:
            strengths.append('High market growth rate')
        return strengths
    
    def _identify_market_concerns(self, market_metrics: Dict) -> List[str]:
        concerns = []
        if market_metrics.get('competitive_intensity', 0) >= 8.0:
            concerns.append('Highly competitive market')
        if market_metrics.get('total_addressable_market', 0) < 1e9:
            concerns.append('Limited market size')
        return concerns
    
    def _identify_diff_strengths(self, diff_metrics: Dict) -> List[str]:
        strengths = []
        if diff_metrics.get('ip_portfolio_strength', 0) >= 8.0:
            strengths.append('Strong IP portfolio')
        if diff_metrics.get('network_effects_potential', 0) >= 8.0:
            strengths.append('Strong network effects potential')
        return strengths
    
    def _identify_diff_concerns(self, diff_metrics: Dict) -> List[str]:
        concerns = []
        if diff_metrics.get('technology_novelty_score', 10) < 5.0:
            concerns.append('Limited technology differentiation')
        if diff_metrics.get('switching_costs', 10) < 5.0:
            concerns.append('Low customer switching costs')
        return concerns
    
    def _identify_traction_strengths(self, traction_metrics: Dict) -> List[str]:
        strengths = []
        if traction_metrics.get('annual_recurring_revenue', 0) >= 1e6:
            strengths.append('Strong revenue traction')
        if traction_metrics.get('ltv_cac_ratio', 0) >= 3.0:
            strengths.append('Healthy unit economics')
        return strengths
    
    def _identify_traction_concerns(self, traction_metrics: Dict) -> List[str]:
        concerns = []
        if traction_metrics.get('customer_retention_rate', 1.0) < 0.8:
            concerns.append('High customer churn')
        if traction_metrics.get('ltv_cac_ratio', 10) < 2.0:
            concerns.append('Poor unit economics')
        return concerns
    
    def _load_scoring_rules(self) -> Dict[str, Any]:
        """Load scoring rules from BigQuery"""
        if not self.bq_client:
            return self._get_fallback_rules()
        try:
            query = f"""
            SELECT category, weight_default, rule_type, rule_payload
            FROM `{self.project_id}.{Config.BIGQUERY_DATASET}.scoring_rules`
            """
            results = self.bq_client.query(query).to_dataframe()
            rules = {}
            for _, row in results.iterrows():
                rules[row['category']] = {
                    'weight': row['weight_default'],
                    'rule_type': row['rule_type'],
                    'rule_payload': row['rule_payload']
                }
            return rules
        except:
            return self._get_fallback_rules()
    
    def _get_fallback_rules(self) -> Dict[str, Any]:
        """Fallback rules when BigQuery is not available"""
        return {
            'founder_profile': {'weight': 0.25, 'rules': []},
            'problem_market': {'weight': 0.25, 'rules': []},
            'differentiator': {'weight': 0.25, 'rules': []},
            'team_traction': {'weight': 0.25, 'rules': []}
        }
    
    def _publish_message(self, topic: str, message: Dict[str, Any]):
        """Publish message to Pub/Sub"""
        if self.publisher:
            topic_path = self.publisher.topic_path(self.project_id, topic)
            message_json = json.dumps(message).encode('utf-8')
            self.publisher.publish(topic_path, message_json)